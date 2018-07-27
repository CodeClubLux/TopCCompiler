__author__ = 'antonellacalvia'

from .node import *
import AST as Tree
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

    def compileToC(self, codegen):
        pass

    def validate(self, parser):
        pass

class Lambda(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "lambda"

    def validate(self, parser): pass

    def compileToJS(self, codegen):
        codegen.append("(function(")
        codegen.incrScope()
        self.nodes[0].compileToJS(codegen)
        self.nodes[1].compileToJS(codegen)
        codegen.append(")")

    def compileToC(self, codegen):
        self.error("not implemented yet")

class FuncStart(Node):
    def __init__(self, name, returnType, parser):
        Node.__init__(self, parser)
        self.returnType = returnType
        self.name = name
        self.method = False

    def __str__(self):
        return f"def {self.name}("

    def compileToC(self, codegen):
        import AST as Tree
        if not type(self.owner) is Tree.Root:
            name = codegen.createName(self.package + "_" + self.name)
        else:
            name = self.package + "_" + self.name

        if type(self.owner) is Root or (type(self.owner) is Tree.Block and type(self.owner.owner) is Tree.Root):
            codegen.inFunction()

        codegen.append(f"{self.ftype.returnType.toCType()} {name}(")

        codegen.incrScope()

    def validate(self, parser):
        Scope.incrScope(parser)



class FuncBraceOpen(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return ")"

    def compileToC(self, codegen):
        for i in self.nodes[:-1]:
            i.compileToC(codegen)
            codegen.append(", ")

        if len(self.nodes) > 0:
            self.nodes[-1].compileToC(codegen)

        codegen.append('){')

    def validate(self, parser):
        pass

class FuncBody(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.returnType = ""
        self.before = []
        self.method = False

    def __str__(self):
        return "}"

    def case(self, codegen, number, node):
        codegen.append("case "+str(number)+":")

    def compileToC(self, codegen):
        if type(self.returnType) is str:
            codegen.append("}")
            return

        for i in self.nodes[:-1]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        if self.returnType != Types.Null():
            codegen.append(";return ")

        if len(self.nodes) > 0:
            self.nodes[-1].compileToC(codegen)

        codegen.decrScope()

        codegen.append(";}\n")

        if self.method:
            codegen.append(f"static inline {self.returnType.toCType()} {self.package}_{self.name}ByValue(")
            names = []
            for (iter, i) in enumerate(self.types):
                n = codegen.getName()
                names.append(n)
                if iter == 0:
                    codegen.append(f"{i.pType.toCType()} {n}")
                else:
                    codegen.append(f"{i.toCType()} {n}")
                if iter + 1 < len(self.types):
                    codegen.append(",")

            codegen.append("){\n")
            if self.returnType != Types.Null():
                codegen.append("return ")
            codegen.append(f"{self.package}_{self.name}(&")
            codegen.append(",".join(names))
            codegen.append(");\n}")

        if type(self.owner) is Root or (type(self.owner) is Tree.Block and type(self.owner.owner) is Tree.Root):
            codegen.outFunction()

    def validate(self, parser):
        checkUseless(self)

        actReturnType = Types.Null()

        if type(self.returnType) is str:
            Scope.decrScope(parser)
            return

        if self.returnType == Types.Null(): pass
        elif len(self.nodes) > 0:
            if self.nodes[-1].type == Types.Null():
                actReturnType = Types.Null()
            else:
                actReturnType = self.nodes[-1].type

        returnType = self.returnType
        name = self.name

        import AST as Tree

        try:
            returnType.duckType(parser,actReturnType,self, self.nodes[-1] if len(self.nodes) > 0 else Tree.Under(self),0)
        except EOFError as e:
            Error.beforeError(e, "Return Type: ")

class Context(Node):
    def __init__(self, body, parser):
        super(Context, self).__init__(parser)
        self.body = body

    def compileToJS(self, codegen):
        codegen.append(self.body.res)

    def __str__(self):
        return "context"

    def validate(self, parser): pass


class FuncCall(Node):
    def __init__(self, parser):
        super(FuncCall, self).__init__(parser)
        self.replaced = {}

    def __str__(self):
        return ""

    def compileToC(self, codegen):
        self.nodes[0].compileToC(codegen)
        codegen.append("(")

        for iter in range(len(self.nodes[1:-1])):
            iter += 1
            i = self.nodes[iter]
            if not type(i) is Under:
                i.compileToC(codegen)
                if not iter+1 == len(self.nodes):
                    codegen.append(",")

        if len(self.nodes) > 1:
            self.nodes[-1].compileToC(codegen)

        codegen.append(")")


    def validate(self, parser): pass

class Func(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "func"

    def validate(self, parser): pass

    def compileToC(self, codegen):
        for i in self:
            i.compileToC(codegen)

class Under(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "under"

    def validate(self, parser): pass

    def compileToC(self, codegen):
        codegen.append("NULL")

class Generic(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "::[]"

    def validate(self, parser): pass

    def compileToC(self, codegen):
        self.nodes[0].compileToJS(codegen)

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)