__author__ = 'antonellacalvia'

from .node import *
from TopCompiler import Types
class Int(Node):
    def __init__(self, number, parser, unsigned=True, size=None):
        Node.__init__(self, parser)
        self.number = number

        self.type = Types.I32(unsigned=unsigned, size=size)

    def __str__(self):
        return "int " + self.number

    def compileToC(self, codegen):
        codegen.append(self.number)

    def validate(self, parser): pass

class Bool(Node):
    def __init__(self, bool, parser):
        Node.__init__(self, parser)
        self.bool = bool

        self.type = Types.Bool()

    def __str__(self):
        return "bool " + self.bool

    def compileToC(self, codegen):
        if self.bool == "true":
            codegen.append("1")
        else:
            codegen.append("0")

    def validate(self, parser): pass

class Float(Node):
    def __init__(self, number, parser):
        Node.__init__(self, parser)
        self.number = number

        self.type = Types.Float()

    def __str__(self):
        return "float " + self.number

    def validate(self, parser): pass

    def compileToC(self, codegen):
        codegen.append(self.number)

class String(Node):
    def __init__(self, string, parser):
        super(String, self).__init__(parser)

        self.string = string
        self.type = Types.String(len(string))
        self.target = parser.global_target

    def __str__(self):
        return self.string

    def toString(self):
        return self.string. \
            replace("\n", "\\n").\
            replace("\\{", "{"). \
            replace("\\}", "}")

    def compileToC(self, codegen):
        stringified = self.toString()
        length = len(stringified) -2 - stringified.count(r"\\")
        codegen.append(f"_global_StringInit({length},{stringified})")

    def validate(self, parser): pass

class Char(Node):
    def __init__(self, string, parser):
        Node.__init__(self, parser)
        self.string = string
        self.type = Types.Char()

    def compileToC(self, codegen):
        codegen.append(f"'{self.string}'")

class Sizeof(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.append("sizeof(" + self.typ.toCType() + ")")

from TopCompiler import Parser
from PostProcessing import SimplifyAst
from AST import Cast

class Typeof(Node):
    def __init__(self, parser, typ):
        Node.__init__(self, parser)
        self.typ = typ

        if type(typ) is Types.T:
            self.typ = typ
            self.type = Parser.IType
        elif type(self.typ) is Types.I32:
            self.type = Types.Pointer(Parser.IntType)
        elif type(self.typ) is Types.Float:
            self.type = Types.Pointer(Parser.FloatType)
        elif type(self.typ) is Types.String:
            self.type = Types.Pointer(Parser.StringType)
        elif type(self.typ) is Types.Bool:
            self.type = Types.Pointer(Parser.BoolType)
        elif type(self.typ) is Types.Struct:
            self.type = Types.Pointer(Parser.StructType)
        elif type(self.typ) is Types.Alias:
            self.type = Types.Pointer(Parser.AliasType)
        elif type(self.typ) is Types.Enum:
            self.type = Types.Pointer(Parser.EnumType)
        elif type(self.typ) is Types.Pointer:
            self.type = Types.Pointer(Parser.PointerType)
        elif type(self.typ) is Types.Interface:
            self.type = Types.Pointer(Parser.InterfaceType)
        elif type(self.typ) is Types.Array:
            self.type = Types.Pointer(Parser.ArrayType)
        elif type(self.typ) is Types.FuncPointer:
            self.typ = Types.Null()
            self.type = Types.Pointer(Parser.NoneType) #Types.Pointer(Parser.FuncPointerType)
        elif type(self.typ) is Types.Char:
            self.type = Types.Pointer(Parser.CharType)
        elif type(self.typ) is Types.Null:
            self.type = Types.Pointer(Parser.NoneType)


    def compileToC(self, codegen):
        self.typ.toCType()

        #if self.typ.package == "_global" and type(self.typ) in [Types.Struct, Types.Enum]:
        #    codegen.append("NULL")
        #    return

        package = self.typ.package if self.typ.package != "" else "_global"
        fullName = SimplifyAst.toUniqueID(package, self.typ.normalName, self.typ.remainingGen)

        if not type(self.typ) in [Types.Interface, Types.Pointer, Types.Alias, Types.Null]:
            if type(self.typ) is Types.T:
                typeof_none = Typeof(self, Types.Null())
                Tree.castFrom(typeof_none.type, Parser.IType, typeof_none, "", codegen)
            else:
                codegen.append(f"{fullName}_get_type(NULL," + codegen.getContext() + ")")
        else:
            if type(self.typ) is Types.Pointer:
                codegen.append("_global_boxPointerType(_global_PointerTypeInit(")
                tmp = Typeof(self, self.typ.pType)
                Cast.castFrom(tmp.type, Parser.IType, tmp, "", codegen)
                codegen.append(")," + codegen.getContext() + ")")
            elif type(self.typ) is Types.Null:
                codegen.append(f"&None_Type")
            else:
                codegen.append(f"&{fullName}_Type")

class AliasType(Node):
    def __init__(self, typ, package, structName, parser):
        Node.__init__(self, parser)
        self.package = package
        self.structName = structName
        self.typ = typ

    def replaceT(self, s, newName):
        self.structName = newName

    def compileToC(self, codegen):
        def as_string(s):
            return f'_global_StringInit({len(s)}, "{s}")'

        iName = f"{self.package}_{self.structName}_Type"

        if type(Parser.AliasType) is Parser.TmpType: return

        codegen.inFunction()
        codegen.append(f"{Parser.AliasType.toCType()} {iName};")
        codegen.outFunction()

        codegen.append(f"{iName}.name = {as_string(self.structName)};" )
        codegen.append(f"{iName}.package = {as_string(self.package)};")
        codegen.append(f"{iName}.real_type = ")

        tmp = Typeof(self, self.typ.typ)
        Cast.castFrom(tmp.type, Parser.IType, tmp, "", codegen)
        codegen.append(";")

class PointerType(Node):
    def __init__(self, parser, pType):
        self.pType = pType

    def replaceT(self, s, newName):
        self.newName = newName

    def compileToC(self, codegen):
        codegen.inFunction()

        iName = f"{self.newName}_Type;"
        codegen.append(f"{Parser.PointerType.toCType()} {iName};")
        codegen.outFunction()

        codegen.append(f"{iName}.pType = ")
        tmp = Typeof(self, self.pType)
        Cast.castFrom(tmp.type, Parser.IType, tmp, "", codegen)
        codegen.append(";")

class Offsetof(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.append("offsetof(" + self.typ.toCType() + "," + self.field + ")")


class CastToType(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        codegen.append("(" + self.type.toCType() + ")")
        self.nodes[0].compileToC(codegen)
