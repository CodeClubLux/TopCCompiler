__author__ = 'antonellacalvia'

from .node import *
from .Struct import *
from PostProcessing import SimplifyAst
from PostProcessing import SimplifyAst

def simplifyArray(parser, self, iter):
    if len(self.nodes) == 0:
        func = Tree.FuncCall(self)
        var = Tree.ReadVar("empty_array", True, self)
        var.type = parser.scope["_global"][0]["empty_array"].type
        var.package = "_global"
        func.addNode(var)
        func.replaced = var.type.generic
        self.owner.nodes[iter] = func
        func.owner = self.owner
        func.type = self.type
        return func
    elif self.init:
        func = Tree.FuncCall(self)
        if self.type.static:
            return self
            s = self.type.toCType().replace("struct ", "")
            var = Tree.ReadVar(s+ "fill_array", True, self)
            var.package = "_global"
            var.type = parser.scope["_global"][0]["fill_array"].type
            func.replaced = {}
        else:
            var = Tree.ReadVar("fill_array", True, self)
            var.package = "_global"
            var.type = parser.scope["_global"][0]["fill_array"].type
            func.replaced = {i: self.type.elemT for i in var.type.generic}
        func.addNode(var)
        func.addNode(self.nodes[0])
        func.addNode(self.nodes[1])

        self.owner.nodes[iter] = func
        func.owner = self.owner
        return func
    return self

class Array(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

        self.range = False
        self.init = False
        self.mutable = False
        #self.type = Types.Array(False,Types.Null(),empty=True)

    def __str__(self):
        return "[]"

    def compileToC(self, codegen):

        if self.init and self.type.static:
            name = self.type.toCType().replace("struct ", "")
            codegen.append(name + "Fill_array(")
            self.nodes[1].compileToC(codegen)
            codegen.append(")")
        else:
            name = self.type.toCType().replace("struct ", "")
            codegen.append(f"{name}Init(")
            count = 0
            for i in self.nodes:
                i.compileToC(codegen)
                if count != len(self.nodes) - 1:
                    codegen.append(",")
                count += 1
            codegen.append(")")


    def validate(self, parser):
        return

        arr = self
        mutable = self.mutable
        if self.range:
            arr.type = Types.Array(mutable, Types.I32())
            if len(arr.nodes) != 2 or arr.nodes[1].type != Types.I32():
                Error.parseError(parser, "expecting integer range")
            return
        elif self.init:
            arr.type = Types.Array(mutable, arr.nodes[1].type)
            if len(arr.nodes) != 2 or arr.nodes[1].type == Types.Null():
                Error.parseError(parser, "expecting single non-null expression")
            return

        if not len(arr.nodes) < 1:
            typ = self.type.elemT
            if typ == Types.Null():
                Error.parseError(parser, "array elements must non none")

class ArrRead(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.pointer = False
        self.newValue = False

    def __str__(self):
        return ".[]"

    def compileToC(self, codegen): #ignore will be handled by simplify ast
        #method = SimplifyAst.getMethod("op_get")
        codegen.append("(")
        self.nodes[0].compileToC(codegen)
        codegen.append(")->data[")
        self.nodes[1].compileToC(codegen)
        codegen.append("]")

    def validate(self, parser): pass

from AST import Cast

class ArrDataType(Node):
    def __init__(self, package, structName,  parser):
        Node.__init__(self, parser)
        self.package = package
        self.structName = structName

    def replaceT(self, arrType, structName):
        self.structName = self.package + "_" + structName
        self.arrType = arrType

    def compileToC(self, codegen):
        codegen.inFunction()

        elemT = self.arrType.remainingGen["StaticArray.T"]
        numElements = self.arrType.remainingGen["StaticArray.S"]

        codegen.append(f"struct {self.structName} {{\n")
        codegen.append(f"{elemT.toCType()} data[{numElements}];\n")
        codegen.append("};\n")

        #fill Array, -syntax [8: 3] == [3,3,3,3,3,3,3,3,3,3]
        codegen.append(f"struct {self.structName} {self.structName}Fill_array(")
        codegen.append(elemT.toCType() + " with")
        codegen.append("){\n")
        codegen.append(f"struct {self.structName} tmp;\n")
        codegen.append(f"for (unsigned int i = 0; i < {numElements}; i++) {{\n")
        codegen.append("tmp.data[i] = with;\n")
        codegen.append("}; return tmp; }\n")


        codegen.append(f"struct {self.structName} {self.structName}Init(")

        names = []
        cElemT = elemT.toCType()
        for i in range(numElements):
            name = codegen.getName()
            names.append(name)

            codegen.append(cElemT + " " + name)
            if i < numElements-1:
                codegen.append(",")
        codegen.append("){\n")
        codegen.append(f"struct {self.structName} tmp;\n")
        for (it, name) in enumerate(names):
            codegen.append(f"tmp.data[{it}] = {name};\n")
        codegen.append("return tmp; }\n")


        # Introspection
        def as_string(s):
            return f'_global_StringInit({len(s)}, "{s}")'
        structName = self.structName



        nameOfI = f"{structName}Type"

        codegen.append("struct _global_ArrayType " + nameOfI + ";")

        codegen.append(f"struct _global_ArrayType* {self.structName}_get_type(struct {structName}* self, struct _global_Context* c)" + "{")
        codegen.append(f"return &{self.structName}Type;")
        codegen.append("}\n")

        codegen.append(f"struct _global_ArrayType* {self.structName}_get_typeByValue(struct {structName} self, struct _global_Context* c)" + "{")
        codegen.append(f"return &{self.structName}Type;")
        codegen.append("}\n")

        codegen.append(f"{Parser.ArrayType.toCType()} {self.structName}Type;")

        codegen.outFunction()

        codegen.append(f"{nameOfI}.size = malloc(sizeof(struct _global_ArraySize));")
        codegen.append(f"{nameOfI}.size->tag = 0;")
        codegen.append(f"{nameOfI}.size->cases.Static.field0 = {numElements};" )
        codegen.append(f"{nameOfI}.array_type = ")

        t = Tree.Typeof(self, elemT)
        Cast.castFrom(t.type, Parser.IType, t, "", codegen)

        codegen.append(";")



