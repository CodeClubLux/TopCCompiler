from .node import *
from TopCompiler import Types


class Enum(Node):
    def __init__(self, const, normalName, parser):
        Node.__init__(self, parser)
        self.const = const
        self.package = parser.package
        self.normalName = normalName

    def compileToC(self, codegen):
        count = 0
        codegen.inFunction()

        """ 
        struct Maybe_int_Some {
            int value;
        };
        
        union Maybe_int_cases {
            struct Maybe_int_Some some;
        };
        
        struct Maybe_int {
            unsigned short tag;
            union Maybe_int_cases cases;
        };
        """

        cType = f"struct {self.package}_{self.normalName}"

        for name in self.const:
            args = self.const[name]

            if len(args) > 0:
                codegen.append(f"struct {self.package}_{self.normalName}_{name} {{\n")
                names = ["field" + str(iter) for iter in range(len(args))]

                for i in range(len(args)):
                    codegen.append(f"{args[i].toCType()} field{i};\n")
                codegen.append("\n};")

        numCases = len(self.const)

        tag = ""
        sizes = ["char", "short", "int", "long"]
        for (iter, size) in enumerate(sizes):
            if numCases < 2 ^ ((iter+1) * 8):
                tag = size
                break

        tag += " tag;"

        codegen.append(f"struct {self.package}_{self.normalName} {{\n {tag}\n")
        codegen.append(f"union {{\n")
        for name in self.const:
            if len(self.const[name]) > 0:
                codegen.append(f"struct {self.package}_{self.normalName}_{name} {name};\n")
        codegen.append("\n};};\n")


        for (iter, name) in enumerate(self.const):
            args = self.const[name]
            if len(args) > 0:

                codegen.append(f"{cType} {self.package}_{name}(")
                vars = [codegen.getName() for i in args]
                types = [i.toCType() for i in args]
                codegen.append(",".join(a + " " + b for (a,b) in zip(types, vars)))
                codegen.append("){\n")

                tmp = codegen.getName()
                codegen.append(f"{cType} {tmp};\n")

                for (c, i) in enumerate(vars):
                    codegen.append(tmp + "." + name + ".field" + str(c) + " = " + i + ";")
                codegen.append(f"{tmp}.tag = {iter};\n")
                codegen.append("return " + tmp + ";}\n")
            else:
                codegen.append(f"{cType} {self.package}_{name};\n")

                codegen.outFunction()

                codegen.append(f"{self.package}_{name}.tag = {iter}")

        codegen.outFunction()

    def validate(self, parser):
        pass

class Match(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False
        self.next = ""
        self.ending = ""

    def compileToC(self, codegen):
        tmp = codegen.getName()
        self.tmp = tmp

        if not type(self.type) is Types.Null:
            print("not implemented yet")
            codegen.append("(function(){")
            codegen.append("var " + tmp + "=")
            self.nodes[0].compileToJS(codegen)
            codegen.append(";")

            for iter in range(1, len(self.nodes)):
                self.nodes[iter].compileToJS(codegen)

            codegen.append("})()")
        else:
            codegen.append(f"{self.nodes[0].type.toCType()} {tmp} =")
            self.nodes[0].compileToC(codegen)
            codegen.append(";")
            for iter in range(1, len(self.nodes)):
                self.nodes[iter].compileToC(codegen)
                codegen.addSemicolon(self.nodes[iter])

    def validate(self, parser):
        pass

    def __str__(self):
        return "match"

class Fake:
    def __init__(self, codegen):
        self.checking = True
        self.check = []
        self.body = []
        self.codegen = codegen

    def createName(self, a):
        return self.codegen.createName(a)

    def getName(self):
        return self.codegen.getName()

    def readName(self, a):
        return self.codegen.createName(a)

    def append(self, string):
        if self.checking:
            self.check.append(string)
        else:
            self.body.append(string)

    def appendToCodegen(self):
        tmp = "if("+"".join(self.check)+"){"+"".join(self.body)
        self.codegen.append(tmp)

class MatchCase(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.yielding = False

    def compileToC(self, _codegen):
        codegen = Fake(_codegen)

        def loop(node,tmp):
            codegen.checking = True

            if type(node) is Tree.Operator and node.kind == "concat":
                arr = codegen.getName()
                codegen.append(arr+" = new RegExp('")
                names = []

                def iterate(n):
                    if type(n) is Tree.String:
                        codegen.append(n.toString()[1:-1])
                    elif type(n) is Tree.Tuple:
                        codegen.append("(.*)")
                        names.append(n.nodes[0])
                    elif type(n) is Tree.Operator and n.kind == "concat":
                        iterate(n.nodes[0])
                        iterate(n.nodes[1])

                iterate(node)
                codegen.append("').exec(" + tmp + ")")

                codegen.checking = False

                for (index, i) in enumerate(names):
                    if not self.yielding:
                        name = codegen.createName(i.package + "_" + i.name)
                        codegen.append("var ")
                    else:
                        name = codegen.readName(i.package + "_" + i.name)
                    codegen.append(name + "=" + arr + "[" + str(index + 1) + "];")

            elif type(node) is Tree.FuncCall:
                count = list(node.type.const.keys()).index(node.nodes[0].name)
                nameOfCase = node.nodes[0].name

                codegen.append(tmp + ".tag==" + str(count))

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) != Tree.ReadVar:
                        codegen.append("&&")
                        loop(i, f"{tmp}.{nameOfCase}.field{index}")

                codegen.checking = False

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) is Tree.ReadVar:
                        name = codegen.createName(i.package + "_" + i.name)
                        typ = node.type.const[nameOfCase][index]
                        codegen.append(f"{typ.toCType()} {name}")
                        codegen.append(f" = {tmp}.{nameOfCase}.field{index};\n")
            elif type(node) is Tree.Tuple:
                if len(node.nodes) == 1:
                    loop(node.nodes[0], tmp)
                else:
                    codegen.append("(")
                    codegen.checking = True
                    iter = 0
                    for (index, i) in enumerate(node):
                        if not (type(i) is Tree.ReadVar and i.name[0].islower()):
                            if iter > 0:
                                codegen.check.append("&&")
                            loop(i, tmp + "[" + str(index) + "]")
                            iter += 1

                    codegen.check.append(")")
                    codegen.checking = False

                    for (index, i) in enumerate(node):
                        if type(i) is Tree.ReadVar and i.name[0].islower():
                            if not self.yielding:
                                name = codegen.createName(i.package + "_" + i.name)
                                codegen.append("var ")
                            else:
                                name = codegen.readName(i.package + "_" + i.name)
                            codegen.append(name + "=" + tmp + "[" + str(index) + "];")
            elif type(node) is Tree.Array:
                iter = 0
                end = node.nodes[-1] if len(node.nodes) > 0 else False

                ending = False
                if type(end) is Tree.Operator and end.kind == "..":
                    ending = True
                    codegen.append(tmp+".length>"+str(len(node.nodes)-2))
                else:
                    codegen.append(tmp+".length=="+str(len(node.nodes)))

                for (index, i) in enumerate(node):
                    if not (ending and index == len(node.nodes) - 1) and type(i) != Tree.ReadVar:
                        codegen.append("&&")
                        loop(i, tmp + ".get(" + str(index) + ")")
                        iter += 1

                codegen.checking = False

                for (index, i) in enumerate(node):
                    if type(i) is Tree.ReadVar or (type(i) is Tree.Operator and i.kind == ".."):
                        if type(i) is Tree.Operator:
                            i = i.nodes[0]
                        if not self.yielding:
                            name = codegen.createName(i.package + "_" + i.name)
                            codegen.append("var ")
                        else:
                            name = codegen.readName(i.package + "_" + i.name)
                        if ending and index == len(node) - 1:
                            codegen.append(name+"="+tmp + ".slice(" + str(index) + "," + tmp + ".length);")
                        else:
                            codegen.append(name + "=" + tmp + ".get(" + str(index) + ");")

            elif type(node) is Tree.ReadVar:
                count = list(node.type.const.keys()).index(node.name)
                codegen.append(tmp + ".tag==" + str(count))
                codegen.checking = False
            elif type(node) is Tree.Under:
                codegen.append("1")
            elif type(node) is Tree.Operator and node.kind == "or":
                codegen.append(tmp + "==")
                node.nodes[0].compileToJS(codegen)
                codegen.append("||")
                codegen.append(tmp + "==")
                node.nodes[1].compileToJS(codegen)
                codegen.checking = False
            else:
                if node.type in [Types.I32,Types.Float,Types.String,Types.Bool]:
                    codegen.append(tmp+"==")
                    node.compileToJS(codegen)
                else:
                    codegen.append(tmp+".op_eq(")
                    node.compileToJS(codegen)
                    codegen.append(")")
                codegen.checking = False

        codegen.checking = True
        tmp = self.owner.tmp
        loop(self.nodes[0], self.owner.tmp)
        codegen.appendToCodegen()

    def __str__(self):
        return "MatchCase"

    def validate(self, parser):
        pass
