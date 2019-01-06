__author__ = 'antonellacalvia'

from .node import *

class Tuple(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.tuple = False

    def __str__(self):
        return "tuple"

    def validate(self, parser): pass
    def compileToC(self, codegen):
        if len(self.nodes) == 1:
            codegen.append("(")
            self.nodes[0].compileToC(codegen)
            codegen.append(")")
        else:
            typ = self.type.toCType().replace("struct ", "")
            codegen.append(f"{typ}Init(")
            for i in self.nodes[:-1]:
                i.compileToC(codegen)
                codegen.append(",")
            if len(self.nodes) > 0:
                self.nodes[-1].compileToC(codegen)
            codegen.append(")")