__author__ = 'antonellacalvia'

from .node import *

class InitPack(Node):
    def __init__(self, package, parser):
        Node.__init__(self, parser)
        self.package = package
        self.target = parser.global_target

    def compileToJS(self, codegen):
        if self.target == "full":
            codegen.client_main_parts.append(self.package+"_clientInit();")
            codegen.node_main_parts.append(self.package+"_nodeInit();")
        else:
            codegen.append(self.package+"_" + self.target + "Init();")

    def validate(self, parser): pass