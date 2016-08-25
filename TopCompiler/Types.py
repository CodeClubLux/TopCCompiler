__author__ = 'antonellacalvia'

import ctypes as c
import AST as Tree
from .Scope import *
import collections as coll

def parseType(parser, package= "", mutable= False, attachTyp= False, gen= {}):
    if package == "": package = parser.package
    token = parser.thisToken().token
    if token == "i32":
        return I32()
    elif token == "float":
        return Float()
    elif token == "string":
        return String(0)
    elif token == "int":
        return I32()
    elif token == "bool":
        return Bool()
    elif token == "[":
        if parser.lookInfront().token != "]":
            from TopCompiler import FuncParser
            gen = FuncParser.generics(parser, "anonymous")
            if parser.thisToken().token != "|":
                parseError(parser, "expecting |")
            return parseType(parser, package, mutable, attachTyp, gen)
        else:
            parser.nextToken()
            parser.nextToken()
            return Array(False, parseType(parser, package))
    elif token == "|":
        parser.nextToken()

        args = []
        while parser.thisToken().token != "|":
            if parser.thisToken().token == ",":
                if parser.lookBehind().token == ",":
                    parseError(parser, "unexpected ,")
                parser.nextToken()
                continue
            args.append(parseType(parser))

            parser.nextToken()

        ret = Null()

        parser.nextToken()

        if parser.thisToken().token == "->":
            parser.nextToken()
            ret = parseType(parser, package)

        return FuncPointer(args, ret, gen)
    elif token == "none":
        return Null()
    elif token in parser.imports:
        if parser.lookInfront().token == ".":
            parser.nextToken()
            parser.nextToken()
            return parseType(parser, token)
        else:
            parseError(parser, "expecting .")
    elif (token in parser.interfaces[package]) or (token in parser.interfaces["_global"] and parser.package == package):
        if token in parser.interfaces["_global"]:
            package = "_global"
        return Interface(mutable, parser.interfaces[package][token].types)
    elif token in parser.structs[package]:
        import collections as coll
        gen = coll.OrderedDict()
        if attachTyp:
            return parser.structs[package][token]
        if parser.structs[package][token].generic != {}:
            if parser.nextToken().token != "[":
                parseError(parser, "must specify generic parameters for generic type")
            gen = parseGeneric(parser, parser.structs[package][token])
        return Struct(mutable, token, parser.structs[package][token].types, package, gen)

    elif varExists(parser, package, token):
        t = typeOfVar(Tree.PlaceHolder(parser), parser, package, token)
        if type(t) is T:
            return t
        parseError(parser, "unkown type "+token)
    elif token == "_":
        return Underscore()
    else:
        parseError(parser, "unknown type "+token)

def parseGeneric(parser, typ):
    generic = []

    parser.nextToken()

    while parser.thisToken().token != "]":
        if parser.thisToken().token == ",":
            parser.nextToken()
            continue

        generic.append(parseType(parser))
        t = parser.thisToken().token
        parser.nextToken()

    gen = typ.generic
    if len(gen) > len(generic):
        parseError(parser, "missing "+str(len(gen)-len(generic))+" generic parameters")
    elif len(gen) < len(generic):
        parseError(parser, str(len(generic)-len(gen))+" too many generic parameters")

    v = list(gen.keys())
    replace = {v[index]: i for index, i in enumerate(generic)}

    return replace

class Type:
    name = "type"

    def __str__(self):
        return "'"+self.name+"'"

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other.name == self.name

    def __ne__(self, other):
        return other.name != self.name

    def duckType(self, parser, other, node, mynode, iter):
        if self != other:
            mynode.error("expecting type "+str(self)+" and got type "+str(other))

    def hasMethod(self, parser, field): pass
class StructInit(Type):
    def __init__(self, name):
        self.name= name+" type"
        self.types= {}

def newType(n):
    class BasicType(Type):
        name=n
        normalName=n
        package= "_global"
        types = {"toString": FuncPointer([], String(0))}
    return BasicType

class Pointer(Type):
    def __init__(self, pointerType):
        self.name = "&"+pointerType.name

        self.pType = pointerType

class String(Type):
    def __init__(self, length):
        self.name = "string"
        self.types = {"toString": FuncPointer([], self)}


class FuncPointer(Type):
    def __init__(self, argtypes, returnType, generic= coll.OrderedDict()):
        self.args = argtypes
        self.name = "|"+", ".join([i.name for i in argtypes])+"| -> "+returnType.name
        self.returnType = returnType
        self.generic = generic

    def duckType(self, parser, other, node, mynode, iter= 0):
        if not type(other) is FuncPointer:
            mynode.error("expecting type "+str(self)+" and got type "+str(other))

        if len(other.args) != len(self.args):
            mynode.error("expecting type "+str(self)+" and got type "+str(other))

        count = -1
        for (a, i) in zip(self.args, other.args):
            count += 1
            try:
                a.duckType(parser, i, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Function argument "+str(count)+": ")

        self.returnType.duckType(parser, other.returnType, node, mynode, iter)


class Struct(Type):
    def __init__(self, mutable, name, types, package, gen):
        self.name = ("mut " if mutable else "")+ package+"."+name+"["+",".join([i+": "+str(gen[i]) for i in gen]) + "]"

        self.types = {i: replaceT(types[i], gen) for i in types}

        self.package = package

        self.normalName = name
        self.mutable = mutable

        self.gen = gen

    def hasMethod(self, parser, field):
        m = parser.structs[self.package][self.normalName].hasMethod(parser, field)
        if m:
            return replaceT(m, self.gen)

    def __eq__(self, other):
        if self.name != other.name:
            return False

        for i in self.types:
            if self.types[i] != other.types[i]:
                return False
    def __ne__(self, other):
        return not self == other

    def duckType(self, parser, other, node, mynode, iter=0):
        if self.package+"_"+self.normalName != other.package+"_"+other.normalName:
            node.error("expecting type "+str(self)+", not "+str(other))

        for key in self.gen:
            i = self.gen[i]
            othk = other.gen[i]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Generic argument "+key+": ")

class Array(Pointer):
    def __init__(self, mutable, elemT):
        self.name = ("mut " if mutable else "") + "[]"+elemT.name

        self.elemT = elemT

        self.package = "_global"
        self.normalName = "array"

        self.mutable = mutable
        self.__types = None

    @property
    def types(self):
        if not self.__types:
            self.__types = {
                "toString": FuncPointer([], String(0)),
                "append": FuncPointer([self.elemT], self),
                "insert": FuncPointer([I32(), self.elemT], self),
                "map": FuncPointer(
                    [FuncPointer([self.elemT], T("T", All, str(self)))],
                    Array(False, T("T", All,  str(self))),
                    coll.OrderedDict([("T", All)])
                ),
                "filter": FuncPointer(
                    [FuncPointer([self.elemT], Bool())],
                    self,
                ),
                "reduce": FuncPointer(
                    [FuncPointer([self.elemT, self.elemT], self.elemT)],
                    self.elemT
                ),
                "length": I32(),
                "join": FuncPointer([String(0)], String(0))
            }
        return self.__types
    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is Array:
            mynode.error("expecting array type "+str(self)+" not "+str(other))

        try:
            self.elemT.duckType(parser, other.elemT, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Element type in array: ")



def isMutable(typ):
    if type(typ) in [Struct, Array]:
        return typ.mutable
    return False

class Interface(Type):
    def __init__(self, mutable, args):
        self.name = "{"+", ".join([str(i)+": "+str(args[i]) for i in args])+"}"
        self.mutable = mutable
        self.types = args

    def hasMethod(self, parser, field):
        if field in self.types:
            return self.types[field]

    def duckType(self, parser, other, node, mynode, iter):
        try:
            isStruct = other
            isStruct.types
            isStruct.hasMethod
        except:
            mynode.error("expecting type "+str(self)+" not "+str(other))

        i = 0
        for field in self.types:
            if field in isStruct.types:
                try:
                    self.types[field].duckType(parser, isStruct.types[field], node, mynode, iter)
                except EOFError as e:
                    beforeError(e, "Field '"+ field+ "' in " + str(other) +": ")
            else:
                meth = isStruct.hasMethod(parser, field)
                if meth:
                    if type(meth) is FuncPointer:
                        try:
                            self.types[field].duckType(parser, FuncPointer(meth.args[1:], meth.returnType), node, mynode, iter)
                        except EOFError as e:
                            beforeError(e, "Field '"+ field+ "' in " + str(other) +": ")
                    else:
                        mynode.error("field "+str(other)+"."+field+" is supposed to be type "+str(self.types[field])+", not "+str(meth))
                else:
                    mynode.error("type "+str(other)+" missing field "+field+" to be upcasted to "+str(self))
            i += 1

class T(Type):
    def __init__(self, name, typ, owner):
        self.type = typ
        self.normalName = name
        self.name = owner+"."+name
        self.types = self.type.types

    def duckType(self, parser, other, node, mynode, iter):
        self.type.duckType(parser, other, node, mynode, iter)

    def hasMethod(self, parser, name):
        self.type.hasMethod(parser, name)
All = Interface(False, {})

def isGeneric(t):
    if type(t) in [FuncPointer]:
        if t.generic != {}: return True
        for i in t.args:
            if isGeneric(i): return True
        return isGeneric(t.returnType)
    elif type(t) is Array and isGeneric(t.elemT): return True
    elif type(t) is T: return True
    return False

def replaceT(typ, gen):
    if type(typ) is T:
        if typ.normalName in gen:
            r = gen[typ.normalName]
            if type(r) is Underscore:
                return typ
            return r
        else:
            return typ
    elif isGeneric(typ):
        if type(typ) is Array:
            return Array(False, replaceT(typ.elemT, gen))
        generics = typ.generic
        if type(typ) is FuncPointer:
            arr = []
            for i in typ.args:
                arr.append(replaceT(i, gen))

            newTyp = replaceT(typ.returnType, gen)
            return FuncPointer(arr, newTyp, remainingT(newTyp))
    else:
        return typ

def remainingT(s):
    args = coll.OrderedDict()
    if type(s) is FuncPointer:
        for i in s.args:
            args += remainingT(i)
        args += remainingT(s.returnType)
    elif type(s) is T:
        args[s.name] = s.type

    return args


I32 = newType("int")
Null = newType("none")

Bool = newType("bool")

Float = newType("float")
Func = newType("Func")

Package = newType("package")

Underscore = newType("_")






