__author__ = 'antonellacalvia'

from .node import *

class InitPack(Node):
    def __init__(self, package, parser):
        Node.__init__(self, parser)
        self.package = package

    def compileToJS(self, codegen):
        codegen.append(self.package+"_Init();")

    def validate(self, parser): pass