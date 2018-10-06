from .node import *

class Using(Node):
    def __init__(self, create):
        Node.__init__(self, create)
        self.addNode(create)

    @property
    def varType(self):
        return self.nodes[0].varType

    @varType.setter
    def varType(self, varType):
        self.nodes[0].varType = varType

    @property
    def imutable(self):
        return self.nodes[0].imutable

    def compileToC(self, codegen):
        pass
