__author__ = 'antonellacalvia'

from .node import *
from AST import Func
from TopCompiler import CodeGen

class Cast(Node):
    def __init__(self, f, to, owner=None):
        Node.__init__(self, owner)
        self.f = f
        self.to = to

    def __str__(self):
        return f"{self.f} to {self.to}"

    def compileToC(self, codegen):
        castFrom(self.f, self.to, self.nodes[0], codegen)

    def validate(self, parser):
        checkCast(self.f, self.to, self.nodes[0], parser)

from TopCompiler import Types
from PostProcessing import SimplifyAst

def insertCast(ast, fromT, toT, iter):
    if fromT != toT:
        c = Cast(fromT, toT, ast)
        c.type = toT
        ast.owner.nodes[iter] = c
        c.owner = ast.owner
        c.addNode(ast)

def notSpecified(self):
    generics = self.generic

    for genName in generics:
        b = generics[genName]
        if b.isType(Types.T) and b.owner == (self.package + "." if self.package != "_global" else "") + self.normalName:
            return True

def checkCast(originalType, newType, node, parser):
    if type(newType) is Types.Interface:
        if not type(originalType) is Types.Pointer:
            node.error("Can only upcast to interface from pointer, not "+str(originalType))

def castFrom(originalType, newType, node, codegen):
    if type(newType) is Types.Interface:
        if not type(originalType) is Types.Pointer:
            node.error("Can only upcast to interface from pointer, not "+str(originalType))
        originalType = originalType.pType
        n = SimplifyAst.sanitize(newType.name if newType.package != "_global" else "_global_" + newType.name )
        codegen.append(n+"FromStruct(")
        node.compileToC(codegen)
        for field in newType.types: #@cleanup handle recursive cast
            codegen.append(f", offsetof({originalType.pType.toCType()},{field})")
        for field in newType.methods:
            codegen.append(f", &{originalType.package}_{originalType.normalName}_{field}")
        codegen.append(")")
        return
    elif type(newType) in [Types.Enum, Types.Struct] and notSpecified(originalType):
        funcName = CodeGen.genGlobalTmp()
        tmp = codegen.getName()
        inputT = codegen.getName()

        inFunc = codegen.inAFunction
        codegen.inGenerateFunction()

        typNewC = newType.toCType()

        codegen.append(f"{typNewC} {funcName}({originalType.toCType()} {inputT}) {{\n")
        codegen.append(f"{typNewC} {tmp};")

        if type(newType) is Types.Enum: #@cleanup maybe optimization will cause this not to be valid
            codegen.append(f"{tmp}.tag = {inputT}.tag;")
            unionTyp = typNewC.replace("struct", "union", 1) + "_cases"
            codegen.append(f"{tmp}.cases = *({unionTyp}*) &({inputT}.cases);")
        else:
            for field in newType.types: #change this when using comes out
                codegen.append(f"{tmp}.{field} = {inputT}.{field};")

        codegen.append(f"return {tmp};\n}}\n")

        newType.toCType()
        codegen.setInAFunction(inFunc)

        codegen.append(funcName + "(")
        node.compileToC(codegen)
        codegen.append(")")
        return

    codegen.append("(" + newType.toCType() + ")")
    node.compileToC(codegen)