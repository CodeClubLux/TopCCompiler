#Jonathan Blow style allocators passed through context

from .node import *
from AST import Vars

class AddToContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        inFunc = codegen.inAFunction

        createAssign = self.nodes[0]
        create = createAssign.nodes[0]
        assign = createAssign.nodes[1]
        codegen.append(codegen.getContext() + "->" + create.name)
        codegen.append(" = ")

        assign.nodes[0].compileToC(codegen)

    def validate(self, parser):
        if not type(self.owner) is Tree.Root:
            self.error("Can only add to context outside of function")

class PushContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.contexts.append("&" + Vars.getVar(self.nodes[0], codegen))

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        codegen.contexts.pop()

class Defer(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        names = []
        funcCall = self.nodes[0]
        for i in funcCall.nodes[1:]:
            n = codegen.getName()
            names.append(n)
            codegen.append(f"{i.type.toCType()} {n} = ")
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        names.append(codegen.getContext())

        def func():
            funcCall.nodes[0].compileToC(codegen)
            codegen.append("(")
            codegen.append(",".join(names))
            codegen.append(")")
            codegen.addSemicolon(self)

        codegen.getDeferred().append(func)