__author__ = 'antonellacalvia'


import AST as Tree
from .Scope import *
from .Error import *
import collections as coll

def parseType(parser, _package= "", _mutable= False, _attachTyp= False, _gen= {}):

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
            return I32()
        elif token == "uint":
            return I32()
        elif token == "float":
            return Float()
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
        elif token == "&":
            mut = False
            if parser.nextToken().token == "mut":
                mut = True
                parser.nextToken()
            pType = parseType(parser, package, mutable, attachTyp, gen)
            return Types.Pointer(pType, mut)
        elif token == "[" or parser.thisToken().type == "whiteOpenS":
            incrScope(parser)
            if parser.lookInfront().token != "]" and parser.lookInfront().type != "i32":
                from TopCompiler import FuncParser
                gen = FuncParser.generics(parser, "_")
                if parser.thisToken().token != "|":
                    parseError(parser, "expecting |")

                res = parseType(parser, package, mutable, attachTyp, gen)

                decrScope(parser)

                return res
            elif parser.lookInfront().type == "i32":
                static = int(parser.nextToken().token)
                parser.nextToken()
                parser.nextToken()
                decrScope(parser)
                return Array(False, parseType(parser, package), static)

            else:
                parser.nextToken()
                parser.nextToken()
                decrScope(parser)
                return Array(False, parseType(parser, package))
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

        elif (token in parser.interfaces[package]) or (token in parser.interfaces["_global"] and parser.package == package):
            if token in parser.interfaces["_global"]:
                package = "_global"

            if parser.interfaces[package][token].generic != coll.OrderedDict():
                if parser.lookInfront().token != "[":
                    #parseError(parser, "must specify generic parameters for generic type")
                    pass
                else:
                    parser.nextToken()
                    gen = parseGeneric(parser, parser.interfaces[package][token])
                    return replaceT(parser.interfaces[package][token], gen)

            return parser.interfaces[package][token]

        elif token in parser.structs[package]:
            gen = coll.OrderedDict()
            if attachTyp:
                return parser.structs[package][token]
            if parser.structs[package][token].generic != {}:
                if parser.nextToken().token != "[":
                    parseError(parser, "must specify generic parameters for generic type")
                gen = parseGeneric(parser, parser.structs[package][token])

            return Struct(mutable, token, parser.structs[package][token]._types, parser.structs[package][token].package, gen)

        elif varExists(parser, package, token):
            t = typeOfVar(Tree.PlaceHolder(parser), parser, package, token)
            if type(t) is T:
                return t
            parseError(parser, "unkown type "+token)
        elif token == "_":
            return Underscore()
        else:
            parseError(parser, "unknown type "+token)

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
dataTypes = []

from PostProcessing import SimplifyAst

def getTmpName():
    return next(gen)

from TopCompiler import CodeGen

class TmpCodegen:
    def __init__(self, array):
        self.array = array
        self.info = CodeGen.Info()
        self.gen = CodeGen.genNames(self.info)
    def inFunction(self):
        return

    def outFunction(self):
        return

    def getName(self):
        return next(self.gen)

    def append(self, x):
        self.array.append(x)

def getGeneratedDataTypes():
    global dataTypes
    namedDataTypes = []
    tmp = TmpCodegen(namedDataTypes)

    while True:
        keys = list(genericTypes.keys())
        for key in keys:
            if key in compiledTypes:
                continue
            genericTypes[key].compileToC(tmp)
            compiledTypes[key] = 0
        if len(genericTypes) == len(keys):
            break
    dataTypes += namedDataTypes
    return "".join(dataTypes)

tmpTypes = {}
def genCType(header, genContents):
    global dataTypes
    if header in tmpTypes:
        return tmpTypes[header]
    else:
        dataTypes.append(f"{header} {genContents()};\n")
        tmpTypes[header] = 0
    return header

from AST import Struct as S
from TopCompiler import topc

genericTypes = {}
compiledTypes = {}
def genGenericCType(struct):
    replaced = struct.gen
    structName = struct.normalName
    package = struct.package

    global dataTypes
    newName = SimplifyAst.toUniqueID(package, structName, replaced)
    if not newName in genericTypes:
        s = S.Type(structName, package, topc.global_parser)
        s.replaceT(struct, newName[newName.find("_")+1:])
        genericTypes[newName] = s

    return "struct " + newName

def genInterface(interface):
    newName = SimplifyAst.sanitize(interface.name)
    global genericTypes

    if not newName in genericTypes:
        s = Tree.Interface(interface, newName)
        genericTypes[newName] = s

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
            generic.append(genL[count].type)
        else:
            generic.append(parseType(parser))
        parser.nextToken()

    if len(gen) > len(generic):
        parseError(parser, "missing "+str(len(gen)-len(generic))+" generic parameters")
    elif len(gen) < len(generic):
        parseError(parser, str(len(generic)-len(gen))+" too many generic parameters")

    v = list(gen.keys())
    replace = {v[index]: i for index, i in enumerate(generic)}

    return replace

class Type:
    name = "type"
    normalName = ""
    methods = {}
    package = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def toRealType(self):
        return self

    def getMethod(self, parser, field):
        return self.methods[field]

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
            mynode.error("expecting type "+str(self)+" and got type "+str(other))
    
    def isType(self, other):
        return type(self) is other

    def hasMethod(self, parser, field):
        try:
            return self.methods[field]
        except:
            return None

class EnumT(Type):
    def __init__(self):
        self.name = "enumT"
        self.types = {}

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) in [Enum, EnumT]:
            node.error("type "+str(other)+" is not an enum")

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
                node.error("type "+str(other)+" has the field "+i+" to much to be casted into "+str(self))
            else:
                if not type(typ[i]) is Null:
                    try:
                        const[i].duckType(parser, typ[i], node, mynode, iter)
                    except EOFError as e:
                        Error.beforeError(e, "In field "+i+" : ")

class StructInit(Type):
    def __init__(self, name):
        self.name= name+" type"
        self.types= {}

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
        self.types = {"length": I32()}

        self.methods = {
            "slice": FuncPointer([self, I32(), I32()], self),
            "indexOf": FuncPointer([self, self], I32()),
            "replace": FuncPointer([self, self, self], self),
            "toLowerCase": FuncPointer([self], self),
            "op_eq": FuncPointer([self, self], Bool()),
            "op_add": FuncPointer([self, self], self),
            "toString": FuncPointer([self], self),
            "toInt": FuncPointer([self], I32()),
            "toFloat": FuncPointer([self], Float())
        }

    def toCType(self):
        return "struct _global_String"

import string

class FuncPointer(Type):
    def __init__(self, argtypes, returnType, generic= coll.OrderedDict(), do= False):
        if not (type(generic) in [dict,coll.OrderedDict]):
            raise Error()

        self.args = argtypes
        self.name = "|"+", ".join([i.name for i in argtypes])+"| " +  ("do " if do else "-> ") +returnType.name

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

        name = SimplifyAst.sanitize(self.name)
        funcP = f"typedef {self.returnType.toCType()}(*{name})(" + ",".join(i.toCType() for i in self.args) + ")"
        genCType(funcP, genContents)
        return name

    def duckType(self, parser, other, node, mynode, iter= 0):
        if not other.isType(FuncPointer):
            mynode.error("expecting function type "+str(self)+" and got type "+str(other))

        other = other.toRealType()
        if other.args.__len__() != len(self.args):
            mynode.error("expecting function type "+str(self)+" and got type "+str(other))

        count = -1
        for a in self.args:
            count += 1
            i = other.args[count]

            try:
                i.duckType(parser, a, mynode, node, iter)
            except EOFError as e:
                beforeError(e, "Function type argument "+str(count)+": ")

        try:
            self.returnType.duckType(parser, other.returnType, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Function type return type: ")

def isPart(i, name):
    return ".".join(i.split(".")[:-1]) == name

def strGen(g):
    if type(g) is T:
        return str(g)
    return str(g)

class Struct(Type):
    def __init__(self, mutable, name, types, package, gen=coll.OrderedDict()):
        self.types = types

        self.types = {i: replaceT(types[i], gen) for i in types}

        self.package = package

        self.normalName = name
        self.mutable = mutable

        self.gen = gen
        self.remainingGen = areParts(gen, package+"."+name)

        gen = self.remainingGen

        genericS = "[" + ",".join([strGen(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = package + "." + name + genericS
        #print(self.name)

    def hasMethod(self, parser, field):
        try:
            m = parser.structs[self.package][self.normalName].hasMethod(parser, field)
        except KeyError:
            try:
                m = parser.interfaces[self.package][self.normalName].types[field]
            except KeyError:
                m = False

        if m:
            func = replaceT(m, self.gen)
            firstArg = m.args[0].pType
            try:
                firstArg.duckType(parser, self, parser, parser)
            except EOFError as e:
                beforeError(e, "")
            return func

    def toCType(self):
        if self.gen:
            return genGenericCType(self)
        else:
            return "struct " + self.package + "_" + self.normalName

    def duckType(self, parser, other, node, mynode, iter=0):
        
        if self.gen != {} and self.name == other.name:
            return

        if not other.isType(Struct):
            node.error("expecting type "+str(self)+", not "+str(other))
        if self.package+"_"+self.normalName != other.package+"_"+other.normalName:
            node.error("expecting type "+str(self)+", not "+str(other))

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

            if not (b.isType(T) and b.owner == self.package+"."+self.normalName):
                try:
                    a.duckType(parser, b, node, mynode, iter)
                except EOFError as e:
                    beforeError(e, "For generic parameter " + name + ": ")

class Tuple(Type):
    def __init__(self, types):
        self.list = types
        self.types = dict([(str(index), i) for (index, i) in enumerate(types)])

        array = list(range(0, len(self.types)))
        for i in self.types:
            array[int(i)] = str(self.types[i])
        self.name = "(" + ",".join(array) + ")"

    def duckType(self, parser, other, node, mynode, iter):
        
        if not other.isType(Tuple):
            node.error("expecting type "+str(self)+", not "+str(other))

        if len(self.types) != len(other.types):
            node.error("expecting tuple of length "+str(len(self.types))+", not "+str(len(other.types)))

        for key in self.types:
            i = self.types[key]
            othk = other.types[key]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Tuple element #" + key + ": ")

class Array(Type):
    def __init__(self, mutable, elemT, empty=False, static=False):
        self.name = "[]"+elemT.name

        self.elemT = elemT

        self.package = "_global"
        self.normalName = "array"

        self.mutable = mutable
        self.__types = None
        self.empty = empty
        self.static = static

    def toCType(self):
        return "Array"

    @property
    def types(self):
        if not self.__types:
            self.__types = {
                "toString": FuncPointer([], String(0)),
                "append": FuncPointer([self.elemT], self),
                "insert": FuncPointer([I32(), self.elemT], self),
                "map": FuncPointer(
                    [FuncPointer([self.elemT], T("T", All, "Array"))],
                    Array(False, T("T", All,  "Array")),
                    coll.OrderedDict([("Array.T", All)])
                ),
                "remove": FuncPointer([I32()], self),
                "serial": FuncPointer(
                    [FuncPointer([self.elemT], T("T", All, "Array"), do=True)],
                    Array(False, T("T", All, "Array")),
                    generic=coll.OrderedDict([("Array.T", All)]),
                    do=True
                ),
                "parallel": FuncPointer(
                    [FuncPointer([self.elemT], T("T", All, "Array"), do=True)],
                    Array(False, T("T", All, "Array")),
                    generic=coll.OrderedDict([("Array.T", All)]),
                    do=True
                ),
                "set": FuncPointer([I32(), self.elemT], self)
                ,
                "filter": FuncPointer(
                    [FuncPointer([self.elemT], Bool())],
                    self,
                ),
                "get": FuncPointer([I32()], self.elemT),
                "reduce": FuncPointer(
                    [FuncPointer([self.elemT, self.elemT], self.elemT)],
                    self.elemT,
                ),
                "has": FuncPointer(
                    [self.elemT],
                    Bool()
                ),
                "indexOf": FuncPointer(
                    [self.elemT],
                    I32()
                ),
                "op_add": FuncPointer(
                    [self.elemT],
                    Array(False, self.elemT)
                ),
                "length": I32(),
                "join": FuncPointer([String(0)], String(0)),
                "shorten": FuncPointer([Types.I32()], self),
                "slice": FuncPointer([Types.I32(), Types.I32()], self)
            }
        return self.__types
    def duckType(self, parser, other, node, mynode, iter):
        
        if not other.isType(Array):
            mynode.error("expecting array type "+str(self)+" not "+str(other))

        if other.empty:
            return


        try:
            self.elemT.duckType(parser, other.elemT, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Element type in array: ")

def isMutable(typ):
    if type(typ) in [Struct, Array]:
        return typ.mutable
    return False

def areParts(generic, name):
    c = coll.OrderedDict()

    for i in generic:
        if isPart(i, name):
            c[i] = generic[i]

    return c

class Interface(Type):
    def __init__(self, mutable, args, generic= coll.OrderedDict(), name="", methods=None):
        generic = areParts(generic, name)
        if name != "":
            gen = generic
            genericS = "[" + ",".join([strGen(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""
            self.name = name+genericS
        else:
            self.name = "{"+", ".join([str(i + ": " + str(args[i])) for i in args])+"}"
        self.mutable = False
        self.types = args
        self.generic = generic
        self.normalName = ""
        self.package = ""
        if name:
            self.package = name[:name.find(".")]
            self.normalName = name[name.find(".")+1:]
        if not methods:
            self.methods = []
        else:
            self.methods = methods

    def fromObj(self, obj):
        self.name = obj.name
        self.types = obj.types
        self.generic = obj.generic
        self.normalName = obj.normalName
        self.types = obj.types
        self.package = obj.package

        return self

    def toCType(self):
        return genInterface(self)

    def duckType(self, parser, other, node, mynode, iter):
        if self.name == other.normalName and self.package == other.package:
            if self.generic != {} and self.name == other.name:
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
            mynode.error("expecting type "+str(self)+" not "+str(other))

        notInField = False
        inMethod = False

        try:
            for field in self.types:
                if field in isStruct.types:
                    self.types[field].duckType(parser, isStruct.types[field], node, mynode, iter)
                else:
                    mynode.error("type "+str(other)+" missing field "+field+" to be upcasted to "+str(self))

            inMethod = True
            for field in self.methods:
                try:
                    meth = isStruct.hasMethod(parser, field)
                except EOFError as e:
                    notInField = True
                    beforeError(e, "type "+str(other)+"."+field+", needed to be upcasted to " + str(self) + ", only operates: ")
                if meth:
                    if meth.isType(FuncPointer):
                        self.methods[field].duckType(parser, FuncPointer(meth.args[1:], meth.returnType, do= meth.do, generic=meth.generic), node, mynode, iter)
                    else:
                        self.methods[field].duckType(parser, meth, node, mynode, 0)
                            #mynode.error("field "+str(other)+"."+field+" is supposed to be type "+str(self.types[field])+", not "+str(meth))
                else:
                    notInField = True
                    mynode.error("type "+str(other)+" missing field "+field+" to be upcasted to "+str(self))
        except EOFError as e:
            if notInField:
                beforeError(e, "")
            else:
                beforeError(e, ("Method" if inMethod else "Field")  +" '" + field + "' in " + str(other) + ": ")


    def hasMethod(self, parser, field):
        if field in self.methods:
            return self.methods[field]

class T(Type):
    def __init__(self, name, typ, owner):
        self.type = typ
        self.normalName = owner+"."+name
        self.name = owner+"."+name

        self.types = self.type.types
        self.owner = owner
        self.realName = name
        #self.methods = typ.methods

    def toCType(self):
        return self.type.toCType()

    def duckType(self, parser, other, node, mynode, iter):
        
        if self.name == other.name:
            return True

        if other.isType(T) and self.normalName != other.normalName and self.type == other.type:
            return True

        Type.duckType(self, parser, other, node, mynode, iter)
        #self.type.duckType(parser, other, node, mynode, iter)

    def hasMethod(self, parser, name):
        print(self.type)
        return self.type.hasMethod(parser, name)

    def getMethod(self, parser, field):
        return self.type.getMethod(parser, field)

    def __repr__(self):
        return self.name+":"+str(self.type)

def addMethodEnum(self, i, parser, name, method):
    package = parser.package

    if package in self.methods:
        if name in self.methods[package]:
            i.error("Method called " + name + ", already exists")
        self.methods[package][name] = method
    else:
        self.methods[package] = {name: method}

def hasMethodEnum(attachTyp, parser, name):
    self = parser.interfaces[attachTyp.package][attachTyp.normalName]

    packages = []
    b = None
    for i in parser.imports + [parser.package, "_global"]:
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

    if not b:
        return

    return replaceT(b, attachTyp.generic)

class Enum(Type):
    def __init__(self, package, name, const, generic):
        self.generic = generic
        self.gen = generic

        self.const = const
        self.types = {}

        self.package = package
        self.normalName = name

        remaining = remainingT(self)

        self.remainingGen = remaining
        self.methods = {}

        gen = self.remainingGen

        # print(self.gen)

        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = (package + "." if package != "_global" else "") + name + genericS

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

    def hasMethod(attachTyp, parser, name):
        hasMethodEnum(attachTyp, parser, name)

    def toCType(self):
        return "struct " + self.package + "_" + self.normalName

    def duckType(self, parser, other, node, mynode, iter):
        if self.normalName != other.normalName:
            node.error("expecting type "+self.name+", not "+str(other))

        for name in self.remainingGen:
            a = self.generic[name]
            b = other.generic[name]

            if not (b.isType(T) and b.owner == (self.package+"." if self.package != "_global" else "")+self.normalName):
                if a != b:
                    mynode.error("For generic parameter "+name+": "+"Expecting type "+str(a)+", but got type "+str(b))

class Alias(Type):
    def __init__(self, package, name, typ, generic):
        self.typ = typ
        self.types = typ.types
        self.normalName = name

        self.generic = generic
        self.remainingGen = generic

        self.package = package

        gen = generic
        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = (package + "." if package != "_global" else "") + name + genericS

    def toRealType(self):
        return self.typ

    def isType(self, other):
        return type(self.typ) is other

    def toCType(self):
        return self.typ.toCType()

    def duckType(self, parser, other, node, mynode, iter):
        if other.isType(Alias):
            self.typ.duckType(parser, other.typ, node, mynode, iter)
        else:
            self.typ.duckType(parser, other, node, mynode, iter)

    def addMethod(self, i, parser, name, method):
        meth = self.typ.hasMethod(parser, name)
        if meth:
            i.error("The type alias "+self.name+" is aliasing the type "+self.typ.name+", which already has the method "+name)
        else:
            addMethodEnum(self, i, parser, name, method)

    def hasMethod(attachTyp, parser, field):
        meth = attachTyp.typ.hasMethod(parser, field) #could be problematic since it will call Alias.name

        if meth:
            return meth
        else:
            return hasMethodEnum(attachTyp, parser, field)


All = Interface(False, {})

def isGeneric(t, unknown=False):
    if unknown: return True
    if type(t) in [FuncPointer]:
        if not (type(t.generic) in [dict,coll.OrderedDict]):
            print(type(t.generic))

        if t.generic != {}: return True
        for i in t.args:
            if isGeneric(i): return True
        return isGeneric(t.returnType)
    elif type(t) is Array: return isGeneric(t.elemT)
    elif type(t) is T: return True
    elif type(t) is Pointer: return isGeneric(t.pType)
    elif type(t) in [Interface, Struct, Alias, Enum]: return t.normalName != t.name
    elif type(t) is Tuple:
        for i in t.list:
            if isGeneric(i):
                return True

    return False

class Null(Type):
    name = "none"
    types = {}

    def toCType(self):
        return "void"

def remainingT(s):
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
                if ".".join(i.split(".")[:-1]) == s.package+"."+s.normalName:
                    args[i] = gen[i]
    elif type(s) is T:
        args[s.name] = s
        try:
            s.count += 1
        except AttributeError:
            s.count = 1

    return args

class I32(Type):
    def __init__(self, unsigned=False):
        Type.__init__(self)
        if unsigned:
            self.name = "uint"
            self.normalName = "Uint"
        else:
            self.name = "int"
            self.normalName = "Int"

        self.types = {}
        self.unsigned = unsigned

        self.__methods__ = None

    def toCType(self):
        if self.unsigned:
            return "unsigned int"
        return "int"

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toInt": FuncPointer([self], self),
                "toFloat": FuncPointer([self], Float()),
                "toString": FuncPointer([self], String(0)),
                "op_add": FuncPointer([self, self], self),
                "op_sub": FuncPointer([self, self], self),
                "op_div": FuncPointer([self,self], self),
                "op_mul": FuncPointer([self,self], self),
                "op_eq": FuncPointer([self,self], Bool()),
                "op_gt": FuncPointer([self,self], Bool()),
                "op_lt": FuncPointer([self,self], Bool()),
            }

        return self.__methods__

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is I32:
            node.error("Expecting "+self.name+", not "+str(other))

        if self.unsigned and not other.unsigned:
            node.error("Expecting uint not int")

class Pointer(Type):
    def __init__(self, pType, mutable):
        self.pType = pType
        self.name = "&" + ("mut " if mutable else "") + pType.name
        self.normalName = "&" + pType.name
        self.types = pType.types
        self.methods = pType.methods
        self.mutable = mutable

    def isMutable(self):
        return self.mutable

    def toCType(self):
        return self.pType.toCType() + "*"

    def duckType(self, parser, other, node, mynode, iter):
        if not other.isType(Pointer):
            mynode.error("Expecting pointer, not type "+other.name)

        other = other.toRealType()
        if self.mutable and not other.mutable:
            mynode.error("Expecting an mutable pointer but instead got an immutable pointer")

    def hasMethod(self, parser, field):
        return self.pType.hasMethod(parser, field)

    def getMethod(self, parser, field):
        return self.pType.getMethod(parser, field)

class Float(Type):
    def __init__(self):
        Type.__init__(self)

        self.name = "float"
        self.normalName = "Float"
        self.types = {}
        self.__methods__ = None

    def toCType(self):
        return "float"

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toInt": FuncPointer([self], I32()),
                "toFloat": FuncPointer([self], self),
                "toString": FuncPointer([self], String(0)),
                "op_add": FuncPointer([self,self], self),
                "op_sub": FuncPointer([self,self], self),
                "op_div": FuncPointer([self,self], self),
                "op_mul": FuncPointer([self,self], self)
            }

        return self.__methods__

    def duckType(self, parser, other, node, mynode, iter):
        if not (other.isType(I32) or other.isType(Float)):
            mynode.error("expecting type " + str(self) + ", or "+str(I32())+" and got type " + str(other))

class Bool(Type):
    name = "bool"
    normalName = "Bool"
    types = {}

    __methods__ = None

    @property
    def methods(self):
        if self.__methods__ is None:
            self.__methods__ = {
                "toString": FuncPointer([], String(0))
            }

        return self.__methods__

package= "_global"
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


def replaceT(typ, gen, acc=False, unknown=False): #with bool replaces all
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
            if type(r) is Underscore:
                #if type(typ.type) is Assign:
                return T(typ.realName, replaceT(typ.type, gen, acc), typ.owner)
                #return typ

            return replaceT(r, gen, acc, unknown)
        else:
            #if type(typ.type) is Assign:
            return T(typ.realName, replaceT(typ.type, gen, acc, unknown), typ.owner)
            #return typ
    elif type(typ) is Struct:
        rem = {}
        for i in typ.remainingGen:
            if i in gen:
                rem[i] = T(i[i.find(".")+1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)
        return Struct(False, typ.normalName, typ.types, typ.package, rem)
    elif type(typ) is Alias:
        rem = {}
        for i in typ.generic:
            if i in gen:
                rem[i] = T(i[i.find(".") + 1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)
        return Alias(typ.package, typ.normalName, replaceT(typ.typ, gen, acc, unknown), rem)
    elif type(typ) is Assign:
        return Assign(replaceT(typ.const, gen, acc, unknown))
    elif type(typ) is Interface:
        types = typ.types

        c = Interface(False,{})

        if acc == {}:
            acc = {typ: c}
        else:
            acc[typ] = c

        types = {i: replaceT(types[i], gen, acc, unknown) for i in types}
        methods = {i: replaceT(typ.methods[i], gen, acc, unknown) for i in typ.methods}

        c.fromObj(Interface(False, types, gen, typ.normalName, methods=methods))
        return c
    elif type(typ) is Pointer:
        newP = Pointer(replaceT(typ.pType, gen, acc, unknown), typ.pType.mutable)
        return newP
    elif type(typ) is Enum:
        const = coll.OrderedDict()
        g = {}

        c = Enum(typ.package, typ.normalName, const, g)

        if acc == {}:
            acc = {typ: c}
        else:
            acc[typ] = c

        for name in typ.const:
            const[name] = [replaceT(i, gen, acc, unknown) for i in typ.const[name]]

        for name in typ.generic:
            g[name] = replaceT(typ.generic[name], gen, acc, unknown)

        c.fromObj(Enum(typ.package, typ.normalName, const, g))
        return c

    elif type(typ) is Tuple:
        arr = []
        for i in typ.list:
            arr.append(replaceT(i, gen, acc, unknown))

        return Types.Tuple(arr)

    elif type(typ) is Array and isGen:
        return Array(False, replaceT(typ.elemT, gen, acc, unknown))
    elif type(typ) is FuncPointer:
        generics = typ.generic

        arr = []
        for i in typ.args:
            arr.append(replaceT(i, gen, acc, unknown))

        newTyp = replaceT(typ.returnType, gen, acc, unknown)
        r = FuncPointer(arr, newTyp, {}, do= typ.do)
        r.generic = remainingT(r)
        return r
    else:
        return typ

from TopCompiler import topc

