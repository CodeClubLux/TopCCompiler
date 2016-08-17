__author__ = 'antonellacalvia'

from .node import *
from TopCompiler import Error
from TopCompiler import Types

class Println(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.newline = False

    def __str__(self):
        return "println"

    def validate(self, parser):
        if len(self.nodes) == 0:
            self.error("expecting expression")
        elif len(self.nodes) > 1:
            self.nodes[-1].error( "expecting single expression, not multiple")
        elif self.nodes[0].type == Types.Null():
            self.nodes[-1].error("cannot print nothing")

    def compileToJS(self, codegen):
        codegen.append("print((")
        self.nodes[0].compileToJS(codegen)

        if self.newline:
            codegen.append(").toString() + \"<br>\");")
        else:
            codegen.append(").toString());")

