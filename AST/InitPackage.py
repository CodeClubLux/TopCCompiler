__author__ = 'antonellacalvia'

from .node import *
from AST import Vars

class InitPack(Node):
    def __init__(self, package, parser):
        Node.__init__(self, parser)
        self.package = package
        self.target = parser.output_target
        self.thisPackage = parser.package

    def compileToC(self, codegen):
        codegen.init_types.append(self.package+"InitTypes();")
        codegen.append(self.package+"Init();")

        if not self.package in codegen.order_of_modules:
            codegen.order_of_modules.append(self.package)

    def validate(self, parser): pass

class Import(Node):
    def __init__(self, package, thisPackage, names, parser):
        Node.__init__(self, parser)
        self.package = package
        self.thisPackage = thisPackage
        self.names = names

    def compileToC(self, codegen):
        return
        for (i, target) in self.names:
            varName = self.package+"_"+i
            codegen.append(self.thisPackage+"_"+i+"= typeof "+varName+"=='undefined'||"+varName+";")

    def validate(self, parser):
        for (i, target) in self.names:
            c = Vars.Create(i, Types.Null(), self)
            c.package = self.thisPackage;
            c.isGlobal = True

            self.owner.before.append(c)


