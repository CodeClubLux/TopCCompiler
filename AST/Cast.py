__author__ = 'antonellacalvia'

from .node import *

class Cast(Node):
    def __init__(self, f, to, owner=None):
        Node.__init__(self, owner)
        self.f = f
        self.to = to

    def __str__(self):
        return f"{self.f} to {self.to}"

from TopCompiler import Types
from PostProcessing import SimplifyAst

def castFrom(originalType, newType, node, codegen):
    if type(newType) is Types.Interface:
        if not type(originalType) is Types.Pointer:
            node.error("Can only upcast to interface from pointer, not "+str(originalType))
        originalType = originalType.pType
        n = SimplifyAst.sanitize(newType.name)
        codegen.append(n+"FromStruct(")
        node.compileToC(codegen)
        for field in newType.types: #@cleanup handle recursive cast
            codegen.append(f", offsetof({originalType.pType.toCType()},{field})")
        for field in newType.methods:
            codegen.append(f", &{originalType.package}_{originalType.normalName}_{field}")
        codegen.append(")")
        return
    codegen.append("(" + newType.toCType() + ")")
    node.compileToC(codegen)

