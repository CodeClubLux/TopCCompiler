from .node import *
from TopCompiler import Types


class Enum(Node):
    def __init__(self, const, normalName, parser):
        Node.__init__(self, parser)
        self.const = const
        self.package = parser.package
        self.normalName = normalName

    def compileToJS(self, codegen):
        count = 0
        codegen.inFunction()

        tmp = codegen.getName()

        codegen.append("function " + self.package + "_" + self.normalName + "(" + tmp + "){this[0]=" + tmp + "}")
        for name in self.const:
            args = self.const[name]
            names = [codegen.getName() for _ in args]

            if len(names) > 0:
                codegen.append("function " + self.package + "_" + name + "(")
                codegen.append(",".join(names))
                codegen.append("){")
                codegen.append("var " + tmp + " = new "+self.package + "_" + self.normalName+"("+str(count)+");")

                c = 0
                for i in names:
                    c += 1
                    codegen.append(tmp + "[" + str(c) + "]=" + i + ";")

                codegen.append("return " + tmp + "}")
            else:
                codegen.append("var " + self.package + "_" + name + "= new "+self.package + "_" + self.normalName+"("+str(count)+");")

                c = 0
                for i in names:
                    c += 1
                    codegen.append(self.package + "_" + name + "[" + c + "]=" + i + ";")

            count += 1
        codegen.outFunction()

    def validate(self, parser):
        pass

class Match(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False
        self.yielding = False
        self.next = ""
        self.ending = ""

    def compileToJS(self, codegen):
        tmp = codegen.getName()
        self.tmp = tmp

        if not self.yielding:
            codegen.append("(function(){")
            codegen.append("var " + tmp + "=")
            self.nodes[0].compileToJS(codegen)
            codegen.append(";")

            for iter in range(1, len(self.nodes)):
                self.nodes[iter].compileToJS(codegen)

            codegen.append("})()")
        else:
            codegen.count += 1
            self.ending = str(codegen.count)

            for i in self.nodes[1:]:
                i.yielding = True

            codegen.append("var " + tmp + "=")
            self.nodes[0].compileToJS(codegen)
            codegen.append(";")

            next = self.next

            for iter in range(1, len(self.nodes), 2):
                if iter > 2:
                    codegen.append("/*if*/")
                    if self.next == next:
                        codegen.count += 1
                        self.next = codegen.count

                    codegen.append("case " + str(self.next) + ":")
                    next = self.next
                    codegen.append("/*notif*/")

                self.nodes[iter].compileToJS(codegen)
                self.nodes[iter + 1].compileToJS(codegen)

            codegen.append("case " + str(self.ending) + ":")

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

    def compileToJS(self, _codegen):
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

                codegen.append(tmp + "[0]==" + str(count))

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) != Tree.ReadVar:
                        codegen.append("&&")
                        loop(i, tmp + "[" + str(index + 1) + "]")

                codegen.checking = False

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) is Tree.ReadVar:
                        if not self.yielding:
                            name = codegen.createName(i.package + "_" + i.name)
                            codegen.append("var ")
                        else:
                            name = codegen.readName(i.package + "_" + i.name)
                        codegen.append(name + "=" + tmp + "[" + str(index + 1) + "];")
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
                codegen.append(tmp + "[0]==" + str(count))
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
