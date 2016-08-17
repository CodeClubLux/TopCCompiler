__author__ = 'antonellacalvia'

from .node import  *

class InitInline(Node):
    def __init__(self, name, varType, parser):
        Node.__init__(self, parser)
        self.name = name
        self.varType = varType

    def __str__(self):
        return "initing "+str(self.name)

    def compileToJS(self, codegen):
        name = codegen.createName(self.package+"_"+self.name)
        codegen.append("var " + name + "=")
        self.nodes[0].compileToJS(codegen)
        codegen.append(";")


class InlineStart(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
    def __str__(self):
        return "inline start"

    def compileToJS(self, codegen):
        for i in self.nodes:
            i.compileToJS(codegen)
