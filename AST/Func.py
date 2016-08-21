__author__ = 'antonellacalvia'

from .node import *
from TopCompiler import Scope

class InitArg(Node):
    def __init__(self, name, parser):
        Node.__init__(self, parser)
        self.name = name
        self.varType = ""

    def __str__(self):
        return self.name + " init "

    def compileToJS(self, codegen):
        pass

    def validate(self, parser):
        pass
class FuncStart(Node):
    def __init__(self, name, returnType, parser):
        Node.__init__(self, parser)
        self.returnType = returnType
        self.name = name
        self.method = False

    def __str__(self):
        return "def "+self.name+"("

    def compileToJS(self, codegen):
        codegen.incrScope()
        codegen.inFunction()
        if self.method:

            attachTyp = self.attachTyp
            codegen.append(attachTyp.package+"_"+attachTyp.normalName+".prototype."+self.normalName+"=(function(")
            names = [codegen.getName() for i in self.types]
            codegen.append(",".join(names)+"){return ")
            codegen.append(self.package + "_" + self.name+"("+",".join(["this"]+names)+")});")

        codegen.append("function "+self.package + "_" + self.name+"(")

    def validate(self, parser):
        Scope.incrScope(parser)

class FuncBraceOpen(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return ")"

    def compileToJS(self, codegen):
        for i in self.nodes[:-1]:
            i.compileToJS(codegen)
            codegen.append(", ")

        if len(self.nodes) > 0:
            self.nodes[-1].compileToJS(codegen)
        codegen.append('){')

    def validate(self, parser):
        pass


class FuncBody(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.returnType = "."
    def __str__(self):
        return "}"

    def compileToJS(self, codegen):
        for i in self.nodes[:-1]:
            i.compileToJS(codegen)
        if self.returnType != Types.Null():
            codegen.append("return ")

        if len(self.nodes) > 0:
            self.nodes[-1].compileToJS(codegen)
        codegen.append(";}")

        codegen.decrScope()

        import AST as Tree
        if type(self.owner) is Root or (type(self.owner) is Tree.Block and type(self.owner.owner) is Tree.Root):
            codegen.outFunction()

    def validate(self, parser):

        actReturnType = Types.Null()
        if self.returnType == Types.Null(): pass
        elif len(self.nodes) > 0:
            if self.nodes[-1].type == Types.Null():
                actReturnType = Types.Null()

            else:
                actReturnType = self.nodes[-1].type

        returnType = self.returnType
        name = self.name

        import AST as Tree

        returnType.duckType(parser,actReturnType,self, self.nodes[-1] if len(self.nodes) > 0 else Tree.Under(self),0)

        Scope.decrScope(parser)

class FuncCall(Node):
    def __init__(self, parser):
        super(FuncCall, self).__init__(parser)
        self.partial = False

    def __str__(self):
        return ""

    def compileToJS(self, codegen):
        if self.inline:
            if type(self.type) != Types.Null():
                codegen.append("(function(){")

            for i in self.nodes[1:-1]:
                i.compileToJS(codegen)

            if type(self.type) != Types.Null(): codegen.append("return ")
            if len(self.nodes) > 0:
                self.nodes[-1].compileToJS(codegen)
            if type(self.type) != Types.Null():
                codegen.append(";})()")
            return

        if self.partial:
            names = [codegen.getName() for i in self.nodes[1:]]

            partial = []
            missing = []
            for i in range(len(names)):
                if type(self.nodes[i+1]) is Under:
                    missing += names[i]
                else:
                    partial += names[i]

            codegen.append("(function("+",".join(partial)+"){return(function("+",".join(missing)+"){")
            codegen.append("return ")
            self.nodes[0].compileToJS(codegen)
            codegen.append("("+",".join(names)+");})})\n")
        else:
            self.nodes[0].compileToJS(codegen)
            if self.curry:
                codegen.append(".bind(undefined,")
            else:
                codegen.append("(")

        for iter in range(len(self.nodes[1:-1])):
            iter += 1
            i = self.nodes[iter]
            if not type(i) is Under:
                i.compileToJS(codegen)
                if not (iter+2 == len(self.nodes) and type(self.nodes[iter+1]) is Under):
                    codegen.append(",")

        if len(self.nodes) > 1 and not type(self.nodes[-1]) is Under:
            self.nodes[-1].compileToJS(codegen)

        codegen.append(")")

        if self.type == Types.Null():
            codegen.append(";")

    def validate(self, parser): pass

class Bind(Node):
    def __init__(self, func, module, parser):
        Node.__init__(self, parser)
        self.addNode(func)
        self.addNode(module)

    def validate(self, parser): pass

    def compileToJS(self, codegen):
        codegen.append("(")
        self.nodes[0].compileToJS(codegen)
        codegen.append(").bind(null,")
        self.nodes[1].compileToJS(codegen)
        codegen.append(")")

class Under(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def validate(self, parser): pass

    def compileToJS(self, codegen):
        codegen.append("null")

class Generic(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def validate(self, parser): pass

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)