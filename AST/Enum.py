from .node import *
from TopCompiler import Types

class Enum(Node):
    def __init__(self, const, parser):
        Node.__init__(self, parser)
        self.const = const
        self.package = parser.package

    def compileToJS(self, codegen):
        count = 0

        for name in self.const:
            args = self.const[name]
            names = [codegen.getName() for _ in args]
            codegen.inFunction()
            if len(names) > 0:
                codegen.append("function "+self.package+"_"+name+"(")
                codegen.append(",".join(names))
                codegen.append("){return ["+str(count)+","+",".join(names)+"]}")
            else:
                codegen.append("var "+self.package+"_"+name+"=["+str(count)+","+",".join(names)+"];")

            codegen.outFunction()
            count += 1
    def validate(self, parser): pass

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
            codegen.append("function(){")
            codegen.append("var "+tmp+"=")
            self.nodes[0].compileToJS(codegen)
            codegen.append(";")

            for iter in range(1, len(self.nodes)):
                self.nodes[iter].compileToJS(codegen)

            codegen.append("}()")
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
                self.nodes[iter+1].compileToJS(codegen)

            codegen.append("case " + str(self.ending) + ":")

    def validate(self, parser):
        pass

    def __str__(self):
        return "match"

class MatchCase(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.yielding = False

    def compileToJS(self, codegen):
        node = self.nodes[0]
        tmp = self.owner.tmp

        if type(self.nodes[0]) is Tree.Operator and self.nodes[0].kind == "concat":
            arr = codegen.getName()
            codegen.append("var "+arr+"=new RegExp('")
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
            codegen.append("').exec(" + tmp + ");")
            codegen.append("if ("+arr+"){")

            for (index, i) in enumerate(names):
                if not self.yielding:
                    name = codegen.createName(i.package + "_" + i.name)
                    codegen.append("var ")
                else:
                    name = codegen.readName(i.package + "_" + i.name)
                codegen.append(name + "=" + arr + "[" + str(index + 1) + "];")

            return

        codegen.append(" if (")

        if type(self.nodes[0]) is Tree.FuncCall:
            count = list(node.type.const.keys()).index(node.nodes[0].name)

            codegen.append(tmp+"[0]=="+str(count))

            for (index, i) in enumerate(node.nodes[1:]):
                if type(i) != Tree.ReadVar:
                    codegen.append("&&(")
                    i.compileToJS(codegen)
                    if type(node.nodes[0].type) in [Types.I32, Types.Float, Types.String, Types.Bool]:
                        codegen.append(")=="+tmp+"["+str(index+1)+"]")
                    else:
                        codegen.append(").operator_eq("+tmp+"["+str(index+1)+"]")

            codegen.append("){")

            for (index, i) in enumerate(node.nodes[1:]):
                if type(i) is Tree.ReadVar:
                    if not self.yielding:
                        name = codegen.createName(i.package+"_"+i.name)
                        codegen.append("var ")
                    else:
                        name = codegen.readName(i.package+"_"+i.name)
                    codegen.append(name+"="+tmp+"["+str(index+1)+"];")

        elif type(self.nodes[0]) is Tree.ReadVar:
            count = list(node.type.const.keys()).index(node.name)
            codegen.append(tmp + "[0]==" + str(count))
            codegen.append("){")

        elif type(self.nodes[0]) is Tree.Under:
            codegen.append("1){")
        elif type(self.nodes[0]) is Tree.Operator and self.nodes[0].kind == "or":
            codegen.append(tmp+"==")
            node.nodes[0].compileToJS(codegen)
            codegen.append("||")
            codegen.append(tmp+"==")
            node.nodes[1].compileToJS(codegen)
            codegen.append("){")
        else:
            codegen.append(tmp+"==")
            node.compileToJS(codegen)
            codegen.append("){")

    def __str__(self):
        return "MatchCase"

    def validate(self, parser): pass
