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
        self.generated = False

    def __str__(self):
        return f"def {self.name}("

    def compileToC(self, codegen):
        import AST as Tree
        if not type(self.owner) is Tree.Root:
            name = codegen.createName(self.package + "_" + self.name)
        else:
            name = self.package + "_" + self.name

        if self.method and not self.ftype.args[0].isType(Types.Pointer):
            name += "ByValue"

        if type(self.owner) is Root or (type(self.owner) is Tree.Block and type(self.owner.owner) is Tree.Root):
            codegen.inFunction()

        codegen.append(f"{self.ftype.returnType.toCType()} {name}(")

        codegen.incrScope()
        codegen.incrDeferred()

    def validate(self, parser):
        Scope.incrScope(parser)



class FuncBraceOpen(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return ")"

    def compileToC(self, codegen):
        for i in self.nodes:
            i.compileToC(codegen)
            codegen.append(", ")

        context = codegen.getName()
        codegen.contexts.append(context)

        codegen.append("struct _global_Context* " + context)
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

        codegen.incrDeferred()

        for i in self.nodes[:-1]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        isDeferred = False

        if self.returnType != Types.Null():
            codegen.append(";")
            if not type(self.nodes[-1]) in [Tree.Match, Tree.If]:
                if len(codegen.getDeferred()) > 0:
                    isDeferred = codegen.getName()
                    codegen.append(f"{self.returnType.toCType()} {isDeferred} =")
                else:
                    codegen.decrDeferred()
                    codegen.append("return ")

        if len(self.nodes) > 0:
            self.nodes[-1].compileToC(codegen)
            codegen.addSemicolon(self.nodes[-1])

        if self.returnType == Types.Null():
            codegen.decrDeferred()

        codegen.decrScope()

        if isDeferred:
            codegen.decrDeferred()
            codegen.append(f"return {isDeferred};\n }}")
        else:
            codegen.append(";}\n")


        isToString = self.method and self.name.endswith("toString") and self.types[0].isType(Types.Pointer)

        if self.method and (not self.types[0].isType(Types.Pointer) or isToString):
            codegen.append(f"static inline {self.returnType.toCType()} {self.package}_{self.name}")
            if isToString:
                codegen.append("ByValue(")
            else:
                codegen.append("(")
            names = []
            for (iter, i) in enumerate(self.types):
                n = codegen.getName()
                names.append(n)
                if iter == 0:
                    if isToString:
                        codegen.append(f"{i.pType.toCType()} {n},")
                    else:
                        codegen.append(f"{Types.Pointer(i).toCType()} {n},")
                else:
                    codegen.append(f"{i.toCType()} {n},")
            codegen.append(f"struct _global_Context* {codegen.getContext()}")

            codegen.append("){\n")
            if self.returnType != Types.Null():
                codegen.append("return ")
            if not isToString:
                codegen.append(f"{self.package}_{self.name}ByValue(*")
            else:
                codegen.append(f"{self.package}_{self.name}(&")
            codegen.append(",".join(names))
            codegen.append(f",{codegen.getContext()}")
            codegen.append(");\n}")


        #if type(self.owner) is Root or (type(self.owner) is Tree.Block and type(self.owner.owner) is Tree.Root):
        codegen.outFunction()

        codegen.contexts.pop()

    def validate(self, parser):
        actReturnType = Types.Null()

        if self.returnType == Types.Null(): pass
        elif len(self.nodes) > 0:
            actReturnType = self.nodes[-1].type

        returnType = self.returnType
        name = self.name

        import AST as Tree

        try:
            s = self.nodes[-1] if len(self.nodes) > 0 else self
            returnType.duckType(parser,actReturnType, s, s ,0)
            Tree.insertCast(s, actReturnType, returnType, -1)
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
        Node.__init__(self, parser)
        self.replaced = {}

    def __str__(self):
        return ""

    def compileToC(self, codegen):
        firstNode = self.nodes[0]

        if type(firstNode) is Tree.ReadVar and firstNode.name.startswith("Some") and firstNode.package in ["", "_global"] and self.type.remainingGen["Maybe.T"].isType(Types.Pointer):
            self.nodes[1].compileToC(codegen)

            return

        if type(firstNode) is Tree.ReadVar and firstNode.name == "indexPtr" and firstNode.package == "":
            codegen.append("(")
            self.nodes[1].compileToC(codegen)
            codegen.append(" + ")
            self.nodes[2].compileToC(codegen)
            codegen.append(")")
            return

        self.nodes[0].compileToC(codegen)
        codegen.append("(")

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.append(",")
        codegen.append(codegen.getContext())
        codegen.append(")")

    def validate(self, parser): pass

class Return(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        if len(self.nodes) > 0 and type(self.nodes[0]) in [Tree.Match, Tree.If]:
            self.nodes[0].compileToC(codegen)
            return

        codegen.append("return ")
        if len(self.nodes) > 0:
            self.nodes[0].compileToC(codegen)
        codegen.addSemicolon(self)

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
        self.nodes[0].compileToC(codegen)

def forwardRef(funcStart, funcBrace, funcBody, codegen):
    if not funcStart.generated:
        return

    funcStart.compileToC(codegen)
    funcBrace.compileToC(codegen)

    codegen.getParts()[-1] = ");\n"

    self = funcBody

    if self.method and not self.types[0].isType(Types.Pointer):
        codegen.append(f"\nstatic inline {self.returnType.toCType()} {self.package}_{self.name}(")
        for (iter, i) in enumerate(self.types):
            if iter == 0:
                codegen.append(f"{Types.Pointer(i).toCType()},")
            else:
                codegen.append(f"{i.toCType()},")
        codegen.append(f"struct _global_Context* {codegen.getContext()}")
        codegen.append(");\n")
    elif self.method and funcStart.name.endswith("toString") and self.types[0].isType(Types.Pointer):
        codegen.append(f"\nstatic inline {self.returnType.toCType()} {self.package}_{self.name}(")
        for (iter, i) in enumerate(self.types):
            if iter == 0:
                codegen.append(f"{i.pType.toCType()},")
            else:
                codegen.append(f"{i.toCType()},")
        codegen.append(f"struct _global_Context* {codegen.getContext()}")
        codegen.append(");\n")

    codegen.decrScope()
    codegen.contexts.pop()

    codegen.outFunction()
