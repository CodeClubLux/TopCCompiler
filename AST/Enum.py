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
            if len(args) > 0:
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

    def compileToJS(self, codegen):
        tmp = codegen.getName()
        self.tmp = tmp
        codegen.append("function(){")
        codegen.append("var "+tmp+"=")
        self.nodes[0].compileToJS(codegen)
        codegen.append(";")

        for iter in range(1, len(self.nodes)):
            self.nodes[iter].compileToJS(codegen)

        codegen.append("}()")

    def validate(self, parser): pass

class MatchCase(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToJS(self, codegen):
        codegen.append(" if (")
        tmp = self.owner.tmp
        if type(self.nodes[0]) is Tree.FuncCall:
            node = self.nodes[0]
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
                    name = codegen.createName(i.package+"_"+i.name)
                    codegen.append("var "+name+"="+tmp+"["+str(index+1)+"];")

        elif type(self.nodes[0]) is Tree.ReadVar:
            node = self.nodes[0]
            count = list(node.type.const.keys()).index(node.name)
            codegen.append(tmp + "[0]==" + str(count))
            codegen.append("){")

        else:
            node = self.nodes[0]
            codegen.append(tmp+"==")
            node.compileToJS(codegen)
            codegen.append("){")

    def validate(self, parser): pass
