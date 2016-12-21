__author__ = 'antonellacalvia'

from .node import *

class Tuple(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.tuple = False

    def __str__(self):
        return "tuple"

    def validate(self, parser): pass
    def compileToJS(self, codegen):
        if len(self.nodes) == 1:
            codegen.append("(")
            self.nodes[0].compileToJS(codegen)
            codegen.append(")")
        else:
            codegen.append("[")
            for i in self.nodes[:-1]:
                i.compileToJS(codegen)
                codegen.append(",")
            if len(self.nodes) > 0:
                self.nodes[-1].compileToJS(codegen)
            codegen.append("]")