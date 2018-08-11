#Jonathan Blow style allocators passed through context

from .node import *
from AST import Vars

class AddToContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        inFunc = codegen.inAFunction

        codegen.outFunction()

        createAssign = self.nodes[0]
        create = createAssign.nodes[0]
        assign = createAssign.nodes[1]
        codegen.append(codegen.getContext() + "->" + create.name)
        codegen.append(" = ")

        assign.nodes[0].compileToC(codegen)

        codegen.setInAFunction(inFunc)

class PushContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.contexts.append("&" + Vars.getVar(self.nodes[0], codegen))

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        codegen.contexts.pop()
