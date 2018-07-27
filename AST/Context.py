#Jonathan Blow style allocators passed through context

from .node import *

class AddToContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        inFunc = codegen.inAFunction

        codegen.inAFunction = False

        createAssign = self.nodes[0]
        create = createAssign.nodes[0]
        assign = createAssign.nodes[1]
        codegen.append(codegen.getContext() + "->" + create.name)
        codegen.append(" = ")

        assign.nodes[0].compileToC(codegen)

        codegen.inAFunction = inFunc

class PushContext(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.contexts.append(self.nodes[0].name)
        for i in self.nodes[1:]:
            i.compileToC(codegen)

        codegen.contexts.pop()
