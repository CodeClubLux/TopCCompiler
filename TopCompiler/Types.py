__author__ = 'antonellacalvia'

import ctypes as c
import AST as Tree
from .Scope import *
from .Error import *
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
    elif token == "(":
        args = []
        parser.nextToken()
        while parser.thisToken().token != ")":
            if parser.thisToken().token == ",":
                if parser.lookBehind().token == ",":
                    parseError(parser, "unexpected ,")
                parser.nextToken()
                continue
            args.append(parseType(parser))

            parser.nextToken()

        return Tuple(args)
    elif token == "[":
        incrScope(parser)
        if parser.lookInfront().token != "]":
            from TopCompiler import FuncParser
            gen = FuncParser.generics(parser, "anonymous")
            if parser.thisToken().token != "|":
                parseError(parser, "expecting |")

            res = parseType(parser, package, mutable, attachTyp, gen)

            decrScope(parser)

            return res
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
                return replaceT(Interface(False, parser.interfaces[package][token].types), gen)

        return Interface(False, parser.interfaces[package][token].types)

    elif token in parser.structs[package]:
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

    def __str__(self):
        return "'"+self.name+"'"

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other.name == self.name

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
        self.types = {"toString": FuncPointer([], self), "toInt": FuncPointer([], I32()), "toFloat": FuncPointer([], Float())}


class FuncPointer(Type):
    def __init__(self, argtypes, returnType, generic= coll.OrderedDict(), do= False):
        self.args = argtypes
        self.name = ("do " if do else "") + "|"+", ".join([i.name for i in argtypes])+"| -> "+returnType.name
        self.returnType = returnType
        self.generic = generic
        self.types = {}
        self.do = do

    def duckType(self, parser, other, node, mynode, iter= 0):
        if not type(other) is FuncPointer:
            mynode.error("expecting function type "+str(self)+" and got type "+str(other))

        if len(other.args) != len(self.args):
            mynode.error("expecting function type "+str(self)+" and got type "+str(other))

        if not self.do and other.do:
            mynode.error("Expecting pure function " + str(self) + " and got effectfull function " + str(other))
        elif self.do and not other.do:
            mynode.error("Expecting effectfull function " + str(self) + " and got pure function " + str(other))

        count = -1
        for (a, i) in zip(self.args, other.args):
            count += 1
            try:
                i.duckType(parser, a, mynode, node, iter)
            except EOFError as e:
                beforeError(e, "Function type argument "+str(count)+": ")

        try:
            self.returnType.duckType(parser, other.returnType, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Function type return type: ")
class Struct(Type):
    def __init__(self, mutable, name, types, package, gen):
        self.types = types

        self.types = {i: replaceT(types[i], gen) for i in types}

        self.package = package

        self.normalName = name
        self.mutable = mutable

        self.gen = gen
        self.remainingGen = remainingT(self)

        gen = self.remainingGen

        genericS = "[" + ",".join([i + ": " + str(gen[i].type) for i in gen]) + "]" if len(gen) > 0 else ""
        self.name = package + "." + name + genericS

    def hasMethod(self, parser, field):
        m = parser.structs[self.package][self.normalName].hasMethod(parser, field)
        if m:
            return replaceT(m, self.gen)

    def duckType(self, parser, other, node, mynode, iter=0):
        if not type(other) is Struct:
            node.error("expecting type "+str(self)+", not "+str(other))
        if self.package+"_"+self.normalName != other.package+"_"+other.normalName:
            node.error("expecting type "+str(self)+", not "+str(other))

        for key in self.remainingGen:
            i = self.gen[key]
            othk = other.gen[key]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Generic argument "+key+": ")

class Tuple(Type):
    def __init__(self, types):
        self.types = dict([(str(index), i) for (index, i) in enumerate(types)])

    def __str__(self):
        array = list(range(0,len(self.types)))
        for i in self.types:
            array[int(i)] = str(self.types[i])
        return "("+",".join(array)+")"

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is Tuple:
            node.error("expecting type "+str(self)+", not "+str(other))
        for key in self.types:
            i = self.types[key]
            othk = other.types[key]

            try:
                i.duckType(parser, othk, node, mynode, iter)
            except EOFError as e:
                beforeError(e, "Tuple element #" + key + ": ")

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
                    [FuncPointer([self.elemT], T("T", All, "Array"))],
                    Array(False, T("T", All,  "Array")),
                    coll.OrderedDict([("Array.T", All)])
                ),
                "set": FuncPointer([Types.I32(), self.elemT], self)
                ,
                "filter": FuncPointer(
                    [FuncPointer([self.elemT], Bool())],
                    self,
                ),
                "reduce": FuncPointer(
                    [FuncPointer([self.elemT, self.elemT], self.elemT)],
                    self.elemT,
                ),
                "has": FuncPointer(
                    [self.elemT],
                    Bool()
                ),
                "operator_add": FuncPointer(
                    [self.elemT],
                    Array(False, self.elemT)
                ),
                "length": I32(),
                "join": FuncPointer([String(0)], String(0)),
                "shorten": FuncPointer([Types.I32()], self)
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
    def __init__(self, mutable, args, generic= coll.OrderedDict()):
        self.name = "{"+", ".join([str(i)+": "+str(args[i]) for i in args])+"}"
        self.mutable = False
        self.types = args
        self.generic = generic

    def hasMethod(self, parser, field):
        """if field in self.types:
            return self.types[field]
        """
        pass
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
                            self.types[field].duckType(parser, FuncPointer(meth.args[1:], meth.returnType, do= meth.do, generic=meth.generic), node, mynode, iter)
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
        self.normalName = owner+"."+name
        self.name = owner+"."+name
        self.types = self.type.types

    """def duckType(self, parser, other, node, mynode, iter):
        self.type.duckType(parser, other, node, mynode, iter)
    """

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
    elif type(t) is Interface: return True
    return False


class Null(Type):
    name = "none"
    types = {}
    pass

def remainingT(s):
    args = coll.OrderedDict()
    if type(s) is FuncPointer:
        for i in s.args:
            args.update(remainingT(i))
        args.update(remainingT(s.returnType))
    elif type(s) is Interface:
        for i in s.types:
            args.update(remainingT(s.types[i]))
    elif type(s) is Struct:
        for i in s.types:
            args.update(remainingT(s.types[i]))
    elif type(s) is T:
        args[s.name] = s

    return args

class I32(Type):
    def __init__(self):
        Type.__init__(self)
        self.name = "int"

        self.__types__ = None

    @property
    def types(self):
        if self.__types__ is None:
            self.__types__ = {
                "toInt": FuncPointer([], self),
                "toFloat": FuncPointer([], Float()),
                "toString": FuncPointer([], String(0)),
                "operator_add": FuncPointer([self], self),
                "operator_sub": FuncPointer([self], self),
                "operator_div": FuncPointer([self], self),
                "operator_mul": FuncPointer([self], self)
            }
        return self.__types__

class Float(Type):
    def __init__(self):
        Type.__init__(self)

        self.name = "float"
        self.__types__ = None

    @property
    def types(self):
        if self.__types__ is None:
            self.__types__ = {
                "toInt": FuncPointer([], I32()),
                "toFloat": FuncPointer([], self),
                "toString": FuncPointer([], String(0)),
                "operator_add": FuncPointer([self], self),
                "operator_sub": FuncPointer([self], self),
                "operator_div": FuncPointer([self], self),
                "operator_mul": FuncPointer([self], self)
            }

        return self.__types__

Bool = newType("bool")
Func = newType("Func")

Package = newType("package")

Underscore = newType("_")

def replaceT(typ, gen):
    if type(typ) is T:
        if typ.normalName in gen:
            r = gen[typ.normalName]
            if type(r) is Underscore:
                return typ
            return r
        else:
            return typ
    elif type(typ) is Struct:
        return Struct(False, typ.normalName, typ.types, typ.package, gen)
    elif type(typ) is Interface:
        types = typ.types
        types = {i: replaceT(types[i], gen) for i in types}

        return Interface(False, types)
    elif isGeneric(typ):
        if type(typ) is Array:
            return Array(False, replaceT(typ.elemT, gen))
        generics = typ.generic
        if type(typ) is FuncPointer:
            arr = []
            for i in typ.args:
                arr.append(replaceT(i, gen))

            newTyp = replaceT(typ.returnType, gen)
            return FuncPointer(arr, newTyp, remainingT(newTyp), do= typ.do)
    else:
        return typ





