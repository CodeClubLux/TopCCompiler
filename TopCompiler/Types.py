__author__ = 'antonellacalvia'

import AST as Tree
from .Scope import *
from .Error import *
import collections as coll
from TopCompiler import Scope

E = Tree.Enum


def parseType(parser, _package="", _mutable=False, _attachTyp=False, _gen={}):
    def before():
        if _package == "":
            package = parser.package
        else:
            package = _package

        gen = _gen
        attachTyp = _attachTyp
        mutable = _mutable

        token = parser.thisToken().token
        if token == "i32":
            return I32(size=32)
        elif token == "char":
            return Char()
        elif token == "i64":
            return I32(size=64)
        elif token == "i16":
            return I32(size=16)
        elif token == "i8":
            return I32(size=8)
        elif token == "uint":
            return I32(unsigned=True)
        elif token == "u8":
            return I32(unsigned=True, size=8)
        elif token == "u16":
            return I32(unsigned=True, size=16)
        elif token == "u32":
            return I32(unsigned=True, size=32)
        elif token == "u64":
            return I32(unsigned=True, size=64)
        elif token == "float":
            return Float()
        elif token == "f64":
            return Float(size=64)
        elif token == "string":
            return String(0)
        elif token == "int":
            return I32()
        elif token == "bool":
            return Bool()
        elif token == "(":
            args = []
            parser.nextToken()
            while parser.thisToken().token != ")":
                if parser.thisToken().token == ",":
                    if parser.lookBehind().token == ",":
                        parseError(parser, "unexpected ,")
                    parser.nextToken()
                    continue
                args.append(parseType(parser, package, mutable, attachTyp, gen))

                parser.nextToken()

            return Tuple(args)
        elif token == "enum":
            return EnumT()
        elif token in ["&", "&mut"]:
            mut = False
            parser.nextToken()
            pType = parseType(parser, package, mutable, attachTyp, gen)
            return Types.Pointer(pType, mut)
        elif token == "[" or parser.thisToken().type == "whiteOpenS":
            incrScope(parser)
            if parser.lookInfront().token != "]" and parser.lookInfront().type != "int" and parser.lookInfront().token != "..":
                from TopCompiler import FuncParser
                gen = FuncParser.generics(parser, "_")

                if parser.thisToken().token != "|":
                    parseError(parser, "expecting |")

                res = parseType(parser, package, mutable, attachTyp, gen)

                decrScope(parser)

                return res
            elif parser.lookInfront().type == "int":
                static = int(parser.nextToken().token)
                parser.nextToken()
                parser.nextToken()
                decrScope(parser)
                return Array(parseType(parser, package), static=True, numElements=static)
            elif parser.lookInfront().token == "..":
                parser.nextToken()
                parser.nextToken()
                parser.nextToken()
                decrScope(parser)
                return Array(parseType(parser, package), static=False)
            else:
                parser.nextToken()
                parser.nextToken()
                decrScope(parser)
                return Array(parseType(parser, package), both=True, static=False)
        elif token == "|":
            parser.nextToken()

            args = []
            while not (parser.thisToken().token == "|" and parser.lookInfront().token in ["->", "do"]):
                if parser.thisToken().token == ",":
                    if parser.lookBehind().token == ",":
                        parseError(parser, "unexpected ,")
                    parser.nextToken()
                    continue
                args.append(parseType(parser))

                parser.nextToken()

            ret = Null()

            do = False

            if parser.lookInfront().token == "->":
                parser.nextToken()
                parser.nextToken()

                ret = parseType(parser, package)

            if parser.lookInfront().token == "do":
                parser.nextToken()
                parser.nextToken()

                ret = parseType(parser, package)
                do = True

            return FuncPointer(args, ret, gen, do)
        elif token == "none":
            return Null()
        elif token in parser.imports:
            if parser.lookInfront().token == ".":
                parser.nextToken()
                parser.nextToken()
                return parseType(parser, token)
            else:
                parseError(parser, "expecting .")

        elif token == "{" or parser.thisToken().type == "bracketOpenS":
            args = {}
            parser.nextToken()
            while parser.thisToken().token != "}":
                if parser.thisToken().token == ",":
                    pass
                else:
                    name = parser.thisToken().token
                    if parser.thisToken().type != "identifier":
                        Error.parseError(parser, "expecting identifier")
                    if parser.nextToken().token != ":":
                        Error.parseError(parser, "expecting :")

                    parser.nextToken()
                    typ = parseType(parser)
                    args[name] = typ

                parser.nextToken()

            return Interface(False, args)

        elif (token in parser.interfaces[package]) or (
                token in parser.interfaces["_global"] and parser.package == package):
            if token in parser.interfaces["_global"]:
                package = "_global"

            if parser.interfaces[package][token].generic != coll.OrderedDict():
                if parser.lookInfront().token != "[":
                    # parseError(parser, "must specify generic parameters for generic type")
                    pass
                else:
                    parser.nextToken()
                    gen = parseGeneric(parser, parser.interfaces[package][token])
                    return replaceT(parser.interfaces[package][token], gen)
            elif parser.lookInfront().token == "[":
                parseError(parser, "Not a generic type")

            return parser.interfaces[package][token]

        elif token in parser.structs[package] or (token in parser.structs["_global"] and parser.package == package):
            if token in parser.structs["_global"]:
                package = "_global"

            gen = coll.OrderedDict()
            if attachTyp:
                return parser.structs[package][token]
            if parser.structs[package][token].generic != {}:
                if parser.nextToken().token != "[":
                    parseError(parser, "must specify generic parameters for generic type")
                gen = parseGeneric(parser, parser.structs[package][token])
            elif parser.lookInfront().token == "[":
                parseError(parser, "Not a generic type")

            return Struct(mutable, token, parser.structs[package][token]._types, parser.structs[package][token].package,
                          gen, using=parser.structs[package][token].using)

        elif varExists(parser, package, token):
            t = typeOfVar(Tree.PlaceHolder(parser), parser, package, token)
            if type(t) is T:
                return t
            parseError(parser, "unknown type " + token)
        elif token == "_":
            return Underscore()
        else:
            parseError(parser, "unknown type " + token)

    res = before()

    if parser.lookInfront().token == "{":
        parser.nextToken()
        if parser.nextToken().token != "}":
            Error.parseError(parser, "expecting }")
        return Assign(res)
    else:
        return res


from TopCompiler import CodeGen

info = CodeGen.Info()
gen = CodeGen.genNames(info)

from PostProcessing import SimplifyAst


def getTmpName():
    return next(gen)


from TopCompiler import CodeGen

gen_info = CodeGen.Info()
gen_of_names = CodeGen.genNames(gen_info)


class TmpCodegen:
    def __init__(self):
        self.out_parts = []
        self.initTypes = []
        self.inAFunction = True

    def inFunction(self):
        self.inAFunction = True

    def outFunction(self):
        self.inAFunction = False

    def getName(self):
        return next(gen_of_names)

    def append(self, x):
        if self.inAFunction:
            self.out_parts.append(x)
        else:
            self.initTypes.append(x)

    def getContext(self):
        return "(&_global_context)"


def getGeneratedDataTypes(package):
    # @cleanup use new way of generating

    (namedDataTypes, initializeTypes) = ([], [])
    gen_info.reset([0], 0)

    topc.global_parser.generatedTypesPerPackage[package] = list(compiledTypes.keys())

    for i in compiledTypes:
        tmpCodegen = genericTypes[i]

        # print(tmpCodegen.array[0])

        if type(tmpCodegen) is str:
            namedDataTypes.append(tmpCodegen)
        else:
            namedDataTypes.append("".join(tmpCodegen.out_parts))
            if len(tmpCodegen.initTypes) > 0:
                initializeTypes.append("\n".join(tmpCodegen.initTypes))

    return ("".join(namedDataTypes), "".join(initializeTypes))


def genCType(header, genContents):
    global dataTypes

    if header in genericTypes:
        return header  # tmpTypes[header]
    else:
        genericTypes[header] = f"{header} {genContents()};\n"
        compiledTypes[header] = None

    return header


from AST import Struct as S
from TopCompiler import topc

genericTypes = {}
compiledTypes = coll.OrderedDict()
inProjectTypes = {}


def genGenericCType(struct, func=S.Type, externalStruct=False):
    replaced = struct.remainingGen
    structName = struct.normalName
    package = struct.package

    global dataTypes
    newName = SimplifyAst.toUniqueID(package, structName, replaced)

    if not newName in genericTypes:
        if externalStruct:
            s = func(package, structName, topc.global_parser, True)
        else:
            s = func(package, structName, topc.global_parser)
        if struct.package in ["", "_global"]:
            s.replaceT(struct, newName.replace("_global_", ""))
        else:
            s.replaceT(struct, newName[newName.find("_") + 1:])

        tmpCodegen = TmpCodegen()
        genericTypes[newName] = tmpCodegen
        s.compileToC(tmpCodegen)

        compiledTypes[newName] = None  # genericTypes
        inProjectTypes[newName] = None
    elif newName in genericTypes and not newName in inProjectTypes:
        compiledTypes[newName] = None  # genericTypes
        inProjectTypes[newName] = None

    return "struct " + newName

def genInterface(interface):
    if interface.package == "_global":
        newName = SimplifyAst.sanitize(interface.package + "." + interface.name)
    else:
        newName = SimplifyAst.sanitize(interface.name)
    global genericTypes

    if not newName in genericTypes and not newName in compiledTypes:
        s = Tree.Interface(interface, newName)
        tmpCodegen = TmpCodegen()

        genericTypes[newName] = tmpCodegen
        s.compileToC(tmpCodegen)

        compiledTypes[newName] = None  # genericTypes
        inProjectTypes[newName] = None
    elif newName in genericTypes and not newName in inProjectTypes:
        compiledTypes[newName] = None  # genericTypes
        inProjectTypes[newName] = None

    return "struct " + newName


def parseGeneric(parser, typ):
    generic = []

    parser.nextToken()

    gen = typ.generic
    genL = list(gen.values())

    count = -1
    while parser.thisToken().token != "]":
        count += 1
        if parser.thisToken().token == ",":
            parser.nextToken()
            continue

        if parser.thisToken().token == "_":
            generic.append(genL[count])
        else:
            generic.append(parseType(parser))
        parser.nextToken()

    if len(gen) > len(generic):
        parseError(parser, "missing " + str(len(gen) - len(generic)) + " generic parameters")
    elif len(gen) < len(generic):
        parseError(parser, str(len(generic) - len(gen)) + " too many generic parameters")

    v = list(gen.keys())
    replace = {v[index]: i for index, i in enumerate(generic)}

    return replace

class Type:
    name = "type"
    normalName = ""
    methods = {}
    remainingGen = {}
    package = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return id(self)  # hash(self.name) #id(self)

    def toRealType(self):
        return self

    def getMethod(self, parser, field):
        try:
            return self.methods[field]
        except:
            return

    def using_types(self):
        return {}

    def __eq__(self, other):
        if type(self) is Alias:
            self = self.typ
        if type(other) is Alias:
            other = other.typ
        if type(other) is bool:
            print("error")

        return other.name == self.name

    def __ne__(self, other):
        return not self == other

    def duckType(self, parser, other, node, mynode, iter):
        if self != other:
            node.error("expecting type " + str(self) + " and got type " + str(other))

    def isType(self, other):
        return type(self) is other

    def hasMethod(self, parser, field, isP=False):
        try:
            return self.methods[field]
        except:
            return None


class EnumT(Type):
    def __init__(self):
        self.name = "enumT"
        self.types = {"tag": I32(unsigned=True, size=8)}

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) in [Enum, EnumT]:
            if type(other) is T:
                return self.duckType(parser, other.type, node, mynode, iter)
            node.error("type " + str(other) + " is not an enum")

class Assign(Type):
    def __init__(self, const):
        self.const = const
        self.name = str(self.const) + "{}"
        self.types = {}

    def toCType(self):
        return "void*"

    def duckType(self, parser, other, node, mynode, iter):

        const = self.const.types
        typ = other.types

        for i in typ:
            if not i in const:
                node.error("type " + str(other) + " has the field " + i + " to much to be casted into " + str(self))
            else:
                if not type(typ[i]) is Null:
                    try:
                        const[i].duckType(parser, typ[i], node, mynode, iter)
                    except EOFError as e:
                        Error.beforeError(e, "In field " + i + " : ")


class StructInit(Type):
    def __init__(self, name):
        self.name = name + " type"
        self.types = {}

    def __str__(self):
        return self.name


""""
def newType(n):
    class BasicType(Type):
        name=n
        normalName=n
        package= "_global"
        types = {"toString": FuncPointer([], String(0))}

    return BasicType
"""


class String(Type):
    def __init__(self, length):
        self.name = "string"
        self.normalName = "String"
        self.types = {"length": I32(unsigned=True)}

    def hasMethod(self, parser, field, isP=False):
        self.methods = {
            "slice": FuncPointer([self, I32(unsigned=True), I32(unsigned=True)], self),
            "starts_with": FuncPointer([self, self], Bool()),
            "ends_with": FuncPointer([self, self], Bool()),
            "indexOf": FuncPointer([self, self], I32()),
            "replace": FuncPointer([self, self, self], self),
            "toLowerCase": FuncPointer([self], self),
            "op_eq": FuncPointer([self, self], Bool()),
            "op_add": FuncPointer([self, self], self),
            "op_get": FuncPointer([self, I32(unsigned=True)], Char()),
            "toString": FuncPointer([self], self),
            "toInt": FuncPointer([self], I32()),
            "toFloat": FuncPointer([self], Float()),
            "to_c_string": FuncPointer([self], Types.Pointer(Types.Char())),
        }

        if field == "get_type":
            return FuncPointer([self], Pointer(Parser.StringType))

        try:
            return self.methods[field]
        except:
            return False

    def toCType(self):
        return "struct _global_String"


import string


class FuncPointer(Type):
    def __init__(self, argtypes, returnType, generic=coll.OrderedDict(), do=False):
        self.args = argtypes
        self.name = "|" + ", ".join([i.name for i in argtypes]) + "| " + ("do " if do else "-> ") + returnType.name

        self.returnType = returnType
        self.generic = generic
        self.types = {}
        self.do = do
        self.isLambda = False

    def check(self):
        pass

    def toCType(self):
        def genContents():
            return ""

        contextTyp = "struct _global_Context*"

        name = SimplifyAst.sanitize(self.name)
        s = ""
        for i in self.args:
            s += i.toCType() + ","

        funcP = f"typedef {self.returnType.toCType()}(*{name})(" + s + contextTyp + ")"
        genCType(funcP, genContents)
        return name

    def duckType(self, parser, other, node, mynode, iter=0):
        if not other.isType(FuncPointer):
            mynode.error("expecting function type " + str(self) + " and got type " + str(other))

        other = other.toRealType()
        if other.args.__len__() != len(self.args):
            mynode.error("expecting function type " + str(self) + " and got type " + str(other))

        count = -1
        for a in self.args:
            count += 1
            i = other.args[count]

            try:
                i.duckType(parser, a, mynode, node, iter)
            except EOFError as e:
                beforeError(e, "Function type argument " + str(count) + ": ")

        try:
            self.returnType.duckType(parser, other.returnType, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Function type return type: ")


def isPart(i, name, package):
    if package == "_global": return name == ".".join(i.split(".")[:-1])
    return ".".join(i.split(".")[:-1]) == name


def strGen(g):
    return str(g)

    if type(g) is T:
        return str(g)
    return str(g)


def compareFirstArg(self, firstArg, isP, parser):
    if type(firstArg) is Pointer and not isP:
        parser.error("Expecting pointer")

    if type(firstArg) is Types.Pointer:
        firstArg = firstArg.pType

    generic = firstArg.remainingGen

    for name in generic:
        a = replaceT(generic[name].type, self.remainingGen)
        b = self.remainingGen[name]

        if type(a) is T:
            a = a.type
        if type(b) is T:
            b = b.type

        if type(a) is int or type(b) is int: continue

        a.duckType(parser, b, parser, parser, 0)

class Struct(Type):
    def __init__(self, mutable, name, types, package, gen=coll.OrderedDict(), replaced=False, using=None):
        self._types = types
        self.lastReplace = 0

        # if gen:
        #    self.types = {i: replaceT(types[i], gen) for i in types}
        # else:
        #    self.types = types

        self.package = package
        #if using is None: self.using = []
        #else: self.using = using

        self.normalName = name
        self.mutable = mutable

        fullName = package + "." + name if package != "_global" else name

        self.gen = gen

        self.remainingGen = areParts(gen, fullName, self.package)
        # if replaced:
        #    self.lastReplace = len(self.remainingGen)

        # if replaced:
        #    print("really")
        gen = self.remainingGen

        genericS = "[" + ",".join([strGen(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = fullName + genericS
        # print(self.name)

    def using_types(self):
        typ = {}
        for u in self.using:
            for i in self.types[u].types:
                if not i in self.types:
                    typ[i] = self.types[u].types[i]
        return typ

    @property
    def types(self):
        if self.remainingGen:
            if len(self.remainingGen) != self.lastReplace:
                types = self._types
                self.lastReplace = len(self.remainingGen)

                self._types = {i: replaceT(types[i], self.gen) for i in types}

        return self._types

    @types.getter
    def set_types(self, typ):
        self._types = typ

    def hasMethod(self, parser, field, isP=False):
        if field == "get_type":
            return FuncPointer([Pointer(self)], Pointer(Parser.StructType))

        try:
            attachTyp = parser.structs[self.package][self.normalName]
            m = attachTyp.hasMethod(parser, field)
        except KeyError:
            return False
            # m = parser.interfaces[self.package][self.normalName].types[field]

        if m:
            func = replaceT(m, self.remainingGen)
            tmp = m.args[0]

            compareFirstArg(self, tmp, isP, parser)

            return func

    def getMethods(self, parser):
        return parser.structs[self.package][self.normalName].getMethods(parser)

    def toCType(self):
        if self.name == "Context": return "struct _global_Context"

        structType = topc.global_parser.structs[self.package][self.normalName]
        if structType.externalStruct:
            genGenericCType(self, externalStruct=True)
            if self.normalName.startswith("atomic") or self.normalName.startswith("pthread") or self.normalName.startswith("LLVM"):
                return self.normalName
            return "struct " + self.normalName

        return genGenericCType(self)
        # if self.remainingGen:
        #    return genGenericCType(self)
        # else:
        #    return "struct " + self.package + "_" + self.normalName

    def duckType(self, parser, other, node, mynode, iter=0):
        if self.remainingGen == {} and self.name == other.name:
            return

        # if self.name == "ui.UIElement":

        if not other.isType(Struct):
            node.error("expecting type " + str(self) + ", not " + str(other))
        if self.package + "_" + self.normalName != other.package + "_" + other.normalName:
            node.error("expecting type " + str(self) + ", not " + str(other))

        """
        for key in other.remainingGen:
            i = self.gen[key]
            othk = other.gen[key]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Generic argument "+key+": ")
        """

        for name in self.remainingGen:
            a = self.gen[name]
            b = other.gen[name]

            if type(a) is T:
                a = a.type
            if type(b) is T:
                b = b.type

            if type(b) is int: continue

            if not (b.isType(T) and b.owner == self.package + "." + self.normalName):
                try:
                    a.duckType(parser, b, node, mynode, iter)
                except EOFError as e:
                    beforeError(e, "For generic parameter " + name + ": ")


class Tuple(Type):
    def __init__(self, types):
        self.list = types
        self.types = dict([("field" + str(index), i) for (index, i) in enumerate(types)])

        array = []
        for i in self.list:
            array.append(str(i))
        self.name = "(" + ",".join(array) + ")"

    def duckType(self, parser, other, node, mynode, iter):

        if not other.isType(Tuple):
            node.error("expecting type " + str(self) + ", not " + str(other))

        if len(self.types) != len(other.types):
            node.error("expecting tuple of length " + str(len(self.types)) + ", not " + str(len(other.types)))

        for key in self.types:
            i = self.types[key]
            othk = other.types[key]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Tuple element #" + key + ": ")

    def toCType(self):
        name = SimplifyAst.sanitize(self.name)
        def genContents():
            s = [" { "]
            for (iter, i) in enumerate(self.list):
                s.append(i.toCType() + " field" + str(iter) + ";")

            s.append(" };\n")

            args =  ",".join((i.toCType() + " field" + str(iter) for (iter, i) in enumerate(self.list)))
            s.append(f"struct {name} {name}Init({args}) {{")
            s.append(f"struct {name} tuple;\n")

            for (iter, i) in enumerate(self.list):
                s.append(f"tuple.field{iter} = field{iter};\n")
            s.append("return tuple; }\n")

            return "".join(s)

        funcP = f"struct {name}"
        return genCType(funcP, genContents)

    def hasMethod(self, parser, field, isP=False):
        return False


class Array(Type):
    def __init__(self, elemT, static, numElements=None, both=False, empty=False):
        if empty:
            self.name = "[]"
        elif static:
            self.name = "[" + str(numElements) + "]" + elemT.name
        elif both:
            self.name = "[]" + elemT.name
        else:
            self.name = "[..]" + elemT.name

        self.elemT = elemT

        self.package = "_global"
        self.normalName = "Array"

        self.empty = empty
        self.static = static
        self.numElements = numElements
        self.both = both

        if not static and not both:
            self.arrT = replaceT(Parser.DynamicArray, {"Array.T": elemT})
            self.types = self.arrT.types
            self.remainingGen = self.arrT.remainingGen
        else:
            sizeT = T("S", Types.All, "StaticArray") if self.both else self.numElements
            self.arrT = replaceT(Parser.StaticArray, {"StaticArray.T": elemT, "StaticArray.S": sizeT})
            self.types = self.arrT.types
            self.remainingGen = self.arrT.remainingGen

            self.normalName = "StaticArray"

    def toCType(self):
        if self.empty:
            return "struct _global_Array_Array_T"
        if not self.static and not self.both:
            newName = SimplifyAst.toUniqueID(self.arrT.package, self.arrT.normalName, self.arrT.remainingGen)
            if not newName in genericTypes:
                compiledTypes[newName] = None
            return self.arrT.toCType()
        elif self.both:
            newName = SimplifyAst.toUniqueID(self.arrT.package, self.arrT.normalName, self.arrT.remainingGen)
            if not newName in genericTypes:
                compiledTypes[newName] = None
            return self.arrT.toCType()
        else:
            return genGenericCType(self, Tree.ArrDataType)
            # raise EOFError("not implemented yet")

    def isDynamic(self):
        return not self.static and not self.both

    def duckType(self, parser, other, node, mynode, iter):
        other = other.toRealType()

        if self.both and not (type(other) is Array and (other.both or not other.static)) and not (
                type(other) is Pointer and other.pType.isType(Array) and other.pType.static):
            mynode.error("expecting array type " + str(self) + " not " + str(other))
        elif not self.both and not other.isType(Array):
            mynode.error("expecting array type " + str(self) + " not " + str(other))

        if self.both and other.isType(Pointer):
            other = other.pType.toRealType()

        dynamic = self.isDynamic()
        otherDynamic = other.isDynamic()

        if (dynamic and otherDynamic) or (self.both) or (self.static and other.static):
            if not other.empty:
                if self.elemT != other.elemT:
                    node.error(f"Element type in array: Expecting {self.elemT} not {other.elemT}")
        else:
            node.error("Could not upcast from type " + str(other) + " to " + str(self))

    def hasMethod(self, parser, field, isP=False):
        # if self.both and field == "op_get":
        #    return Types.FuncPointer([self, Types.I32(unsigned=True)], self.elemT)
        if field == "get_type":
            return Parser.ArrayType

        return self.arrT.hasMethod(parser, field, isP)
        # args = [Types.Pointer(self)] + func.args[1:]
        # return FuncPointer(args, func.returnType, func.generic, func.do)


def isMutable(typ):
    if type(typ) in [Struct, Array]:
        return typ.mutable
    return False


def areParts(generic, name, package):
    c = coll.OrderedDict()

    for i in generic:
        if isPart(i, name, package):
            c[i] = generic[i]

    return c


class Interface(Type):
    def __init__(self, mutable, args, generic=coll.OrderedDict(), name="", methods={}):
        self.package = ""
        if name:
            index = name.find(".")
            if index >= 0:
                self.package = name[:name.find(".")]
                self.normalName = name[index + 1:]
            else:
                self.package = "_global"
                self.normalName = name

        generic = areParts(generic, name, self.package)
        if name != "":
            gen = generic
            genericS = "[" + ",".join([strGen(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""
            self.name = name + genericS
        else:
            combined = {**args, **methods}
            self.name = "{" + ", ".join([str(i + ": " + str(combined[i])) for i in combined]) + "}"
        self.mutable = False
        self.types = args
        self.generic = generic
        self.remainingGen = generic
        self.fullName = name

        self.methods = methods

        #if self.name == "EventHandler":
        #    print("what")

        #if self.name == "{handle: |ui.Event| -> none}":
        #    print("wtf")



    def fromObj(self, obj):
        self.name = obj.name
        self.types = obj.types
        self.generic = obj.generic
        self.normalName = obj.normalName
        self.types = obj.types
        self.package = obj.package
        self.methods = obj.methods
        self.remainingGen = obj.remainingGen
        self.fullName = obj.fullName

        return self

    def toCType(self):
        return genInterface(self)

    def duckType(self, parser, other, node, mynode, iter):
        if self.normalName == other.normalName and self.package == other.package:
            if self.name == other.name:
                return
            for name in self.generic:
                a = self.generic[name]
                try:
                    b = other.generic[name]
                except:
                    ended = False
                    continue

                if not (b.isType(T) and b.owner == self.normalName):
                    if a != b:
                        mynode.error("For generic parameter " + name + ": " + "Expecting type " + str(
                            a) + ", but got type " + str(b))
        try:
            isStruct = other
            isStruct.types
            isStruct.hasMethod
        except:
            mynode.error("expecting type " + str(self) + " not " + str(other))

        notInField = False
        inMethod = False

        try:
            for field in self.types:
                if field in isStruct.types:
                    self.types[field].duckType(parser, isStruct.types[field], node, mynode, iter)
                else:
                    mynode.error("type " + str(other) + " missing field " + field + " to be upcasted to " + str(self))

            inMethod = True
            for field in self.methods:
                try:
                    meth = isStruct.hasMethod(parser, field, isP=True)
                except EOFError as e:
                    notInField = True
                    beforeError(e, "type " + str(other) + "." + field + ", to be upcasted to " + str(
                        self) + ", only operates: ")
                if meth:
                    if meth.isType(FuncPointer):
                        self.methods[field].duckType(parser, FuncPointer(meth.args[1:], meth.returnType, do=meth.do,
                                                                         generic=meth.generic), node, mynode, iter)
                    else:
                        self.methods[field].duckType(parser, meth, node, mynode, 0)
                        # mynode.error("field "+str(other)+"."+field+" is supposed to be type "+str(self.types[field])+", not "+str(meth))
                else:
                    notInField = True
                    node.error("type " + str(other) + " missing field " + field + " to be upcasted to " + str(self))
        except EOFError as e:
            if notInField:
                beforeError(e, "")
            else:
                beforeError(e, ("Method" if inMethod else "Field") + " '" + field + "' in " + str(other) + ": ")

    def hasMethod(self, parser, field, isP=False):
        if field == "get_type":
            return FuncPointer([self], Parser.IType)
        elif field == "get_pointer_to_data":
            return FuncPointer([Pointer(self)], Pointer(Null()))

        if field in self.methods:
            meth = self.methods[field]
            return Types.FuncPointer([Types.Pointer(self)] + meth.args, meth.returnType, meth.generic, meth.do)


class T(Type):
    def __init__(self, name, typ, owner):
        self.type = typ
        self.normalName = owner + "." + name
        self.name = owner + "." + name

        self.types = self.type.types
        self.owner = owner
        self.realName = name
        # self.methods = typ.methods

    def fromObj(self, other):
        self.name = other.name
        self.normalName = other.normalName
        self.type = other.type
        self.types = other.types
        self.owner = other.owner
        self.realName = other.realName

    def toCType(self):
        return "void*"  # self.type.toCType()

    def duckType(self, parser, other, node, mynode, iter):
        if self.name == other.name:
            return True

        if other.isType(T) and self.normalName != other.normalName and self.type == other.type:
            return True

        Type.duckType(self, parser, other, node, mynode, iter)
        # self.type.duckType(parser, other, node, mynode, iter)

    def hasMethod(self, parser, name, isP=False):
        meth = self.type.hasMethod(parser, name, isP=isP)
        if meth:
            if not isP and self.type.isType(Interface):
                parser.error("on pointer")
            if not isP and meth.args[0].isType(Types.Pointer):
                parser.error("on pointer")
            return meth

    def __repr__(self):
        return self.name + ":" + str(self.type)


def addMethodEnum(self, i, parser, name, method):
    package = parser.package

    if package in self.methods:
        if name in self.methods[package]:
            i.error("Method called " + name + ", already exists")
        self.methods[package][name] = method
    else:
        self.methods[package] = {name: method}


def hasMethodEnum(attachTyp, parser, name, isP=False):
    self = parser.interfaces[attachTyp.package][attachTyp.normalName]

    packages = []
    b = None
    arr = [parser.package, attachTyp.package, "_global"] if parser.package != "_global" else ["_global"]
    for i in parser.imports + arr:
        if not i in self.methods: continue

        if name in self.methods[i]:
            b = self.methods[i][name]
            b.package = i

            if not i in packages:
                packages.append(i)

    if len(packages) > 1:
        self.node.error(
            "ambiguous, multiple definitions of the method " + self.name + "." + name + " in packages: " + ", ".join(
                packages[:-1]) + " and " + packages[-1])

    if b:
        firstArg = b.args[0]
        m = replaceT(b, attachTyp.generic)
        # replaceT(m.args[0], attachTyp.generic)
        compareFirstArg(self, firstArg, isP, parser)
        return m


def isMaybe(typ):
    typ = typ.toRealType()
    return type(typ) is Types.Enum and typ.package == "_global" and typ.normalName == "Maybe" and typ.remainingGen[
        "Maybe.T"].isType(Types.Pointer)


class Enum(Type):
    def __init__(self, package, name, const, generic, findRemaining=True):
        self.generic = generic
        self.gen = generic

        self.const = const

        self.package = package
        self.normalName = name

        if findRemaining:
            remaining = remainingT(self)
        else:
            remaining = generic

        self.remainingGen = remaining
        self.methods = {}

        gen = self.remainingGen

        # print(self.gen)

        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = (package + "." if package != "_global" else "") + name + genericS
        self.types = {"tag": Types.I32(unsigned=True, size=8)}

    def fromObj(self, other):
        self.remainingGen = other.remainingGen
        self.generic = other.generic
        self.gen = other.generic
        self.methods = other.methods
        self.name = other.name
        self.const = other.const
        self.package = other.package
        self.normalName = other.normalName

    def addMethod(self, i, parser, name, method):
        addMethodEnum(self, i, parser, name, method)

    def hasMethod(attachTyp, parser, name, isP=False):
        return hasMethodEnum(attachTyp, parser, name, isP)

    def toCType(self):
        # if self.remainingGen:

        Parser.EnumType.toCType()
        val = genGenericCType(self, E)
        if isMaybe(self):
            return self.remainingGen["Maybe.T"].toCType()
        # else:
        #    return "struct " + self.package + "_" + self.normalName

        return val

    def duckType(self, parser, other, node, mynode, iter):
        if self.normalName != other.normalName or not other.isType(Types.Enum):
            node.error("expecting type " + self.name + ", not " + str(other))

        for name in self.remainingGen:
            a = self.generic[name]
            b = other.generic[name]

            if not (b.isType(T) and b.owner == (
            self.package + "." if self.package != "_global" else "") + self.normalName) and not (a.isType(T) and b.isType(T)):
                if a != b:
                    node.error(
                        "For generic parameter " + name + ": " + "Expecting type " + str(a) + ", but got type " + str(
                            b))

class Alias(Type):
    def __init__(self, package, name, typ, generic):
        self.typ = typ
        self.types = typ.types
        self.normalName = name
        self.methods = {}

        self.generic = generic
        self.remainingGen = generic  # {**generic, **typ.remainingGen}
        # self.gen = typ.remainingGen

        self.package = package

        gen = generic
        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = (package + "." if package != "_global" else "") + name + genericS

    def toRealType(self):
        return self.typ

    def isType(self, other):
        return type(self.typ) is other

    def toCType(self):
        def func(package, structName, parser):
            return Tree.AliasType(self, package, structName, parser)

        genGenericCType(self, func)
        return self.typ.toCType()

    def duckType(self, parser, other, node, mynode, iter):
        if other.isType(Alias):
            self.typ.duckType(parser, other.typ, node, mynode, iter)
        else:
            self.typ.duckType(parser, other, node, mynode, iter)

    def addMethod(self, i, parser, name, method):
        meth = self.typ.hasMethod(parser, name)
        if meth:
            i.error(
                "The type alias " + self.name + " is aliasing the type " + self.typ.name + ", which already has the method " + name)
        else:
            addMethodEnum(self, i, parser, name, method)

    def hasMethod(attachTyp, parser, field, isP=False):
        meth = attachTyp.typ.hasMethod(parser, field, isP)  # could be problematic since it will call Alias.name

        if meth:
            return meth
        else:
            return hasMethodEnum(attachTyp, parser, field, isP)

All = Interface(False, {}, name="All")


def replaceT(typ, gen, acc=False, unknown=False):  # with bool replaces all
    if typ is None: return

    if not acc:
        acc = {}

    isGen = isGeneric(typ, unknown)

    if typ in acc:
        return acc[typ]

    if not isGen:
        return typ

    if type(typ) is T:
        if typ.normalName in gen:
            r = gen[typ.normalName]
            acc[typ] = r
            result = replaceT(r, gen, acc, unknown)
            return result
        else:
            # if type(typ.type) is Assign:
            return T(typ.realName, replaceT(typ.type, gen, acc, unknown), typ.owner)
            # return typ
    elif type(typ) is Struct:
        rem = {}  # gen
        types = typ._types
        for i in typ.remainingGen:
            if i in gen:
                rem[i] = gen[i]  # T(i[i.find(".")+1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)

        #types = {i: replaceT(types[i], gen, acc, unknown) for i in types}

        joined = {}
        for i in rem:
            joined[i] = rem[i]

        for i in gen:
            joined[i] = gen[i]
        return Struct(False, typ.normalName, typ.types, typ.package, joined)
    elif type(typ) is Alias:
        rem = {}
        for i in typ.generic:
            if i in gen:
                rem[i] = gen[i]  # T(i[i.find(".") + 1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)
        return Alias(typ.package, typ.normalName, replaceT(typ.typ, gen, acc, unknown), rem)
    elif type(typ) is Assign:
        return Assign(replaceT(typ.const, gen, acc, unknown))
    elif type(typ) is Interface:
        types = typ.types

        c = Interface(False, {})

        if acc == {}:
            acc = {typ: c}
        else:
            acc[typ] = c

        types = {i: replaceT(types[i], gen, acc, unknown) for i in types}
        methods = {i: replaceT(typ.methods[i], gen, acc, unknown) for i in typ.methods}

        g = coll.OrderedDict()
        for name in typ.remainingGen:
            g[name] = replaceT(typ.remainingGen[name], gen, acc, unknown)

        if typ.package == "" or typ.package == "_global":
            fullName = typ.normalName
        else:
            fullName = typ.package + "." + typ.normalName

        c.fromObj(Interface(False, types, g, methods=methods, name=fullName))
        return c
    elif type(typ) is Pointer:
        tmp = replaceT(typ.pType, gen, acc, unknown)

        newP = Pointer(tmp, typ.mutable)
        return newP
    elif type(typ) is Enum:
        const = coll.OrderedDict()
        g = {}

        c = Enum(typ.package, typ.normalName, const, g)

        # if acc == {}:
        #    acc = {typ: c}
        # else:
        acc[typ] = c

        for name in typ.const:
            const[name] = [replaceT(i, gen, acc, unknown) for i in typ.const[name]]

        for name in typ.remainingGen:
            g[name] = replaceT(typ.remainingGen[name], gen, acc, unknown)

        c.fromObj(Enum(typ.package, typ.normalName, const, g, findRemaining=False))
        return c

    elif type(typ) is Tuple:
        arr = []
        for i in typ.list:
            arr.append(replaceT(i, gen, acc, unknown))

        return Types.Tuple(arr)

    elif type(typ) is Array and isGen:
        return Array(replaceT(typ.elemT, gen, acc, unknown), both=typ.both, static=typ.static,
                     numElements=typ.numElements)
    elif type(typ) is FuncPointer:
        generics = typ.generic

        arr = []
        for i in typ.args:
            arr.append(replaceT(i, gen, acc, unknown))

        newTyp = replaceT(typ.returnType, gen, acc, unknown)
        r = FuncPointer(arr, newTyp, gen, do=typ.do)
        r.remainingGen = {}
        #for field in r.remainingGen:
        #    r.remainingGen[field] = replaceT(r.remainingGen[field], gen, acc, unknown)

        return r
    else:
        return typ


def isGeneric(t, unknown=False):
    #if unknown: return True
    if type(t) is FuncPointer: #return True
        if t.generic != {}: return True
        for i in t.args:
            if isGeneric(i): return True
        return isGeneric(t.returnType)
    elif type(t) is Array:
        return isGeneric(t.elemT)
    elif type(t) is T:
        return True
    elif type(t) is Pointer:
        return isGeneric(t.pType)
    elif type(t) in [Interface, Struct, Alias, Enum]:
        return len(t.remainingGen) > 0

    elif type(t) is Tuple: return True
        #for i in t.list:
        #    if isGeneric(i):
        #        return True

    return False

class Null(Type):
    name = "none"
    types = {}

    def toCType(self):
        return "void"


cache = {}
def remainingT(s):
    if s in cache:
        return cache[s]

    args = coll.OrderedDict()
    if type(s) is FuncPointer:
        for i in s.args:
            args.update(remainingT(i))
        args.update(remainingT(s.returnType))
    elif type(s) is Interface:
        for i in s.types:
            args.update(remainingT(s.types[i]))
    elif type(s) is Pointer:
        args.update(remainingT(s.pType))
    elif type(s) in [Struct, Enum]:
        gen = s.gen
        for i in gen:
            if s.package == "_global":
                if ".".join(i.split(".")[:-1]) == s.normalName:
                    args[i] = gen[i]
            else:
                if ".".join(i.split(".")[:-1]) == s.package + "." + s.normalName:
                    args[i] = gen[i]
    elif type(s) is T:
        args[s.name] = s
        try:
            s.count += 1
        except AttributeError:
            s.count = 1

    cache[s] = args
    return args

intTypeToString = {
    (None, True): "uint",
    (None, False): "int",
    (8, False): "i8",
    (16, False): "i16",
    (32, False): "i32",
    (64, False): "i64",
    (8, True): "u8",
    (16, True): "u16",
    (32, True): "u32",
    (64, True): "u64",
}


class Char(Type):
    def __init__(self, unsigned=False, size=None):
        #Type.__init__(self)

        self.name = "char"
        self.normalName = "char"
        self.__methods__ = None
        self.types = {}

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toU8": FuncPointer([self], I32(unsigned=True, size=8)),
                "toString": FuncPointer([self], String(0)),
                "op_eq": FuncPointer([self, self], Bool()),
                "op_gt": FuncPointer([self, self], Bool()),
                "op_lt": FuncPointer([self, self], Bool()),
            }

        return self.__methods__

    def toCType(self):
        return "char"


class I32(Type):
    def __init__(self, unsigned=False, size=None):
        #Type.__init__(self)

        self.name = intTypeToString[(size, unsigned)]
        self.normalName = self.name

        self.types = {}
        self.unsigned = unsigned

        self.__methods__ = None
        self.size = size

    def toCType(self):
        nameToC = {
            "int": "int",
            "uint": "unsigned int",
            "i8": "int8_t",
            "i16": "int16_t",
            "i32": "int32_t",
            "i64": "int64_t",
            "u8": "unsigned char",
            "u16": "uint16_t",
            "u32": "uint32_t",
            "u64": "uint64_t",
        }

        return nameToC[self.name]

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toInt": FuncPointer([self], self),
                "toFloat": FuncPointer([self], Float()),
                "toString": FuncPointer([self], String(0)),
                "op_add": FuncPointer([self, self], self),
                "op_sub": FuncPointer([self, self], self),
                "op_div": FuncPointer([self, self], self),
                "op_mul": FuncPointer([self, self], self),
                "op_eq": FuncPointer([self, self], Bool()),
                "op_gt": FuncPointer([self, self], Bool()),
                "op_lt": FuncPointer([self, self], Bool()),
            }

        return self.__methods__

    def hasMethod(self, parser, field, isP=False):
        if field == "get_type":
            return FuncPointer([self], Pointer(Parser.IntType))

        try:
            return self.methods[field]
        except:
            return

    def duckType(self, parser, other, node, mynode, iter):
        other = other.toRealType()
        if not type(other) is I32:
            node.error("Expecting " + self.name + ", not " + str(other))

        if self.unsigned and not other.unsigned:
            node.error("Expecting uint not int")

        sizeA = (self.size if self.size else 32)
        sizeB = (other.size if other.size else 32)

        if sizeA < sizeB:
            node.error("Truncating " + str(other) + " to " + str(self))


class Pointer(Type):
    def __init__(self, pType, mutable=False):
        self.pType = pType
        self.name = "&" + pType.name
        self.normalName = pType.normalName

        if not pType.isType(Pointer):
            self.types = pType.types
        else:
            self.types = {}
        self.methods = pType.methods
        self.mutable = mutable
        self.package = pType.package

        #if self.pType.name == "events.EventHandler":
        #    print("hey")

    def isMutable(self):
        return self.mutable

    def toCType(self):
        return self.pType.toCType() + "*"

    def getMethods(self, parser):
        return self.pType.getMethods(parser)

    def duckType(self, parser, other, node, mynode, iter=0):
        if not other.isType(Pointer):
            node.error("Expecting " + str(self) + ", not type " + other.name)

        if self.name == "&none":
            return
        Type.duckType(self, parser, other, node, node, iter)

    def hasMethod(self, parser, field, isP=False):
        if self.pType.isType(Pointer): return
        return self.pType.hasMethod(parser, field, isP=True)


class Float(Type):
    def __init__(self, size=None):
        #Type.__init__(self)

        if not size:
            self.name = "float"
        else:
            self.name = "f" + str(size)

        self.normalName = "Float"
        self.types = {}
        self.__methods__ = None

        self.size = size

    def toCType(self):
        if self.size:
            return "double"
        else:
            return "float"

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toInt": FuncPointer([self], I32()),
                "toFloat": FuncPointer([self], self),
                "toString": FuncPointer([self], String(0)),
                "op_add": FuncPointer([self, self], self),
                "op_sub": FuncPointer([self, self], self),
                "op_div": FuncPointer([self, self], self),
                "op_mul": FuncPointer([self, self], self),
                "op_gt": FuncPointer([self, self], Bool()),
                "op_lt": FuncPointer([self, self], Bool())
            }

        return self.__methods__

    def hasMethod(self, parser, field, isP=False):
        if field == "get_type":
            return FuncPointer([self], Pointer(Parser.FloatType))

        try:
            return self.methods[field]
        except:
            pass

    def duckType(self, parser, other, node, mynode, iter):
        if not (other.isType(I32) or other.isType(Float)):
            mynode.error("expecting type " + str(self) + ", or " + str(I32()) + " and got type " + str(other))

        other = other.toRealType()
        if type(other) is Float:
            self_size = self.size
            if self.size is None: self_size = 32
            other_size = other.size
            if other_size is None: other_size = 32

            if self_size < other_size :
                mynode.error("Cannot downcast " + str(other) + ", to " + str(self))


class Bool(Type):
    name = "bool"
    normalName = "Bool"
    types = {}

    __methods__ = None

    def toCType(self):
        return "_Bool"

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toString": FuncPointer([], String(0))
            }

        return self.__methods__

    def hasMethod(self, parser, field, isP=False):
        if field == "get_type":
            return FuncPointer([self], Pointer(Parser.BoolType))

        try:
            return self.methods[field]
        except:
            pass


package = "_global"
types = {"toString": FuncPointer([], String(0))}


class Func(Type):
    name = "Func"
    normalName = "Func"


class Package(Type):
    name = "package"
    normalName = "package"


class Underscore(Type):
    name = "_"
    normalName = "_"



from TopCompiler import topc
import AST as Tree


def output_type(node, typ, codegen):
    node = Tree.Typeof(node, typ)
    Parser.IType.toCType()
    Tree.castFrom(node.type, Parser.IType, node, {}, codegen)

