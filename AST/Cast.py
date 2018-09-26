__author__ = 'antonellacalvia'

from .node import *
from AST import Func
from TopCompiler import CodeGen

class Cast(Node):
    def __init__(self, f, to, owner=None):
        Node.__init__(self, owner)
        self.f = f
        self.to = to
        self.realName = {}

    def __str__(self):
        return f"{self.f} to {self.to}"

    def compileToC(self, codegen):
        castFrom(self.f, self.to, self.nodes[0], self.realName, codegen)

    def validate(self, parser):
        checkCast(self.f, self.to, self.nodes[0], parser)

from TopCompiler import Types
from PostProcessing import SimplifyAst

def canTakeRef(ast, struct):
    if struct.toRealType() is Types.Pointer:
        return False

    def loop(i):
        if type(i) is Tree.ReadVar: return True
        elif type(i) is Tree.Field:
            return loop(i.nodes[0])
        elif type(i) is Tree.ArrRead:
            return True
        return False

    return loop(ast)

def insertCast(ast, fromT, toT, iter, onlyToP=False):
    if fromT != toT:
        if toT.isType(Types.Pointer) and not fromT.isType(Types.Pointer):
            takeRef = Tree.Operator("&", ast)
            takeRef.owner = ast.owner
            takeRef.unary = True
            ast.owner.nodes[iter] = takeRef
            takeRef.addNode(ast)
            takeRef.type = Types.Pointer(ast.type)

            #insertCast(takeRef, takeRef.type, toT, iter)
            return

        if onlyToP:
            return

        c = Cast(fromT, toT, ast)
        c.type = toT
        ast.owner.nodes[iter] = c
        c.owner = ast.owner
        c.addNode(ast)
    return fromT

def notSpecified(self):
    generics = self.remainingGen

    for genName in generics:
        b = generics[genName]
        if b.isType(Types.T) and b.owner == (self.package + "." if self.package != "_global" else "") + self.normalName:
            return True

def checkCast(originalType, newType, node, parser):
    if type(newType) is Types.Interface:
        if not type(originalType) is Types.Pointer:
            node.error("Can only upcast to interface from pointer, not "+str(originalType))

def castFrom(originalType, newType, node, realName, codegen):
    if originalType.isType(Types.FuncPointer):
        return node.compileToC(codegen)
    elif type(newType) is Types.I32:
        return node.compileToC(codegen)
    elif type(newType) is Types.Interface:
        originalType = originalType.pType
        n = SimplifyAst.sanitize(newType.name if newType.package != "_global" else "_global_" + newType.name )
        codegen.append(n+"FromStruct(")
        node.compileToC(codegen)
        for field in newType.types: #@cleanup handle recursive cast
            codegen.append(f", offsetof({originalType.toCType()},{field})")
        for field in newType.methods:
            if field in realName:
                name = realName[field]
            else:
                name = f"{originalType.package}_{originalType.normalName}_{field}"
            codegen.append(f", &{name}")
        codegen.append(")")
        return
    elif type(newType) is Types.Array:
        if newType.both and originalType.isType(Types.Pointer) and originalType.pType.static:

            funcName = CodeGen.genGlobalTmp(codegen.filename)
            codegen.inGenerateFunction()

            inputT = codegen.getName()
            typNewC = newType.toCType()

            initCall = typNewC.replace("struct ", "") + "Init"

            codegen.append(f"{typNewC} {funcName}({originalType.toCType()} {inputT}) {{\n")
            codegen.append(f"return {initCall}({inputT}->data, {originalType.pType.numElements});")
            codegen.append("};\n")
            codegen.outFunction()

            codegen.append(f"{funcName}(")
            node.compileToC(codegen)
            codegen.append(")")

            return
        elif newType.both and originalType.empty:
            initCall = newType.toCType().replace("struct ", "") + "Init"
            codegen.append(initCall + "(NULL, 0)")
            return
        elif newType.both and not originalType.both and not originalType.static:
            if not type(node) is Tree.ReadVar:
                node.error("not handled yet")

            typNewC = newType.toCType()
            initCall = typNewC.replace("struct ", "") + "Init"

            codegen.append(f"{initCall}(")
            node.compileToC(codegen)
            codegen.append(".data, ")
            node.compileToC(codegen)
            codegen.append(".length)")
            return

        elif originalType.empty:
            funcName = CodeGen.genGlobalTmp(codegen.filename)
            codegen.inGenerateFunction()

            inputT = codegen.getName()
            typNewC = newType.toCType()

            codegen.append(f"{typNewC} {funcName}({originalType.toCType()} {inputT}) {{\n")
            codegen.append(f"return *(({typNewC}*) &{inputT});")
            codegen.append("};\n")
            codegen.outFunction()

            codegen.append(f"{funcName}(")
            node.compileToC(codegen)
            codegen.append(")")
            return

        print(newType.name)
        print(originalType.name)
        node.error("not handled yet")
    elif type(newType) in [Types.Enum, Types.Struct] and notSpecified(originalType):
        if Types.isMaybe(newType):
            codegen.append("NULL")
            return


        funcName = CodeGen.genGlobalTmp(codegen.filename)
        tmp = codegen.getName()
        inputT = codegen.getName()

        codegen.inGenerateFunction()

        typNewC = newType.toCType()

        codegen.append(f"static inline {typNewC} {funcName}({originalType.toCType()} {inputT}) {{\n")
        codegen.append(f"{typNewC} {tmp};")

        if type(newType) is Types.Enum: #@cleanup maybe optimization will cause this not to be valid
            codegen.append(f"{tmp}.tag = {inputT}.tag;")
            unionTyp = typNewC.replace("struct", "union", 1) + "_cases"
            codegen.append(f"{tmp}.cases = *({unionTyp}*) &({inputT}.cases);")
        else:
            for field in newType.types: #change this when using comes out
                codegen.append(f"{tmp}.{field} = {inputT}.{field};")

        codegen.append(f"return {tmp};\n}}\n")

        codegen.outFunction()

        codegen.append(funcName + "(")
        node.compileToC(codegen)
        codegen.append(")")
        return

    codegen.append("(" + newType.toCType() + ")")
    node.compileToC(codegen)