__author__ = 'antonellacalvia'

import ctypes as c
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
        elif token == "enum":
            return EnumT()
        elif token == "[" or parser.thisToken().type == "whiteOpenS":
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return other.name == self.name

    def duckType(self, parser, other, node, mynode, iter):
        if self != other:
            mynode.error("expecting type "+str(self)+" and got type "+str(other))

    def hasMethod(self, parser, field): pass

class EnumT:
    def __init__(self):
        self.name = "enumT"
        self.types = {}

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is Enum:
            self.error("type "+str(self)+" is not a enum")

class Assign(Type):
    def __init__(self, const):
        self.const = const
        self.name = str(self.const) + "{}"
        self.types = {}

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

class Pointer(Type):
    def __init__(self, pointerType):
        self.name = "&"+pointerType.name

        self.pType = pointerType

class String(Type):
    def __init__(self, length):
        self.name = "string"
        self.types = {"toString": FuncPointer([], self), "toInt": FuncPointer([], I32()), "toFloat": FuncPointer([], Float()),
            "slice": FuncPointer([I32(), I32()], self),
            "length": I32(),
            "indexOf": FuncPointer([self], I32()),
            "replace": FuncPointer([self, self], self),
            "toLowerCase": FuncPointer([], self),
            "operator_eq": FuncPointer([self], Bool()),
        }

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

def isPart(i, name):
    return ".".join(i.split(".")[:-1]) == name

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

        #print(self.gen)

        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

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
            return replaceT(m, self.gen)

    def duckType(self, parser, other, node, mynode, iter=0):
        if self.name == other.name:
            return

        if not type(other) is Struct:
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

            if not (type(b) is T and b.owner == self.package+"."+self.normalName):
                try:
                    a.duckType(parser, b, node, mynode, iter)
                except EOFError as e:
                    beforeError(e, "For generic parameter " + name + ": " + "Expecting type " + str(a) + ", but got type " + str(b))

class Tuple(Type):
    def __init__(self, types):
        self.list = types
        self.types = dict([(str(index), i) for (index, i) in enumerate(types)])

        array = list(range(0, len(self.types)))
        for i in self.types:
            array[int(i)] = str(self.types[i])
        self.name = "(" + ",".join(array) + ")"

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is Tuple:
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

class Array(Pointer):
    def __init__(self, mutable, elemT, empty=False):
        self.name = "[]"+elemT.name

        self.elemT = elemT

        self.package = "_global"
        self.normalName = "array"

        self.mutable = mutable
        self.__types = None
        self.empty = empty

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
                "operator_add": FuncPointer(
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
        if not type(other) is Array:
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
    def __init__(self, mutable, args, generic= coll.OrderedDict(), name=""):
        generic = areParts(generic, name)
        if name != "":
            gen = generic
            genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""
            self.name = name+genericS
        else:
            self.name = "{"+", ".join([str(i + ": " + str(args[i])) for i in args])+"}"
        self.mutable = False
        self.types = args
        self.generic = generic
        self.normalName = name

    def fromObj(self, obj):
        self.name = obj.name
        self.types = obj.types
        self.generic = obj.generic
        self.normalName = obj.normalName

    def hasMethod(self, parser, field):
        """if field in self.types:
            return self.types[field]
        """
        pass
    def duckType(self, parser, other, node, mynode, iter):
        if self.name == other.name:
            return

        try:
            isStruct = other
            isStruct.types
            isStruct.hasMethod
        except:
            mynode.error("expecting type "+str(self)+" not "+str(other))

        notInField = False

        ended = True

        for name in self.generic:
            a = self.generic[name]
            try:
                b = other.generic[name]
            except:
                ended = False
                continue

            if not (type(b) is T and b.owner == self.normalName):
                if a != b:
                    Error.error("For generic parameter " + name + ": " + "Expecting type " + str(a) + ", but got type " + str(b))
        if ended and len(self.generic) > 0: return

        i = 0
        try:
            for field in self.types:
                if field in isStruct.types:
                    self.types[field].duckType(parser, isStruct.types[field], node, mynode, iter)
                else:
                    meth = isStruct.hasMethod(parser, field)
                    if meth:
                        if type(meth) is FuncPointer:
                            self.types[field].duckType(parser, FuncPointer(meth.args[1:], meth.returnType, do= meth.do, generic=meth.generic), node, mynode, iter)
                        else:
                            self.types[field].duckType(parser, meth, node, mynode, iter)
                            #mynode.error("field "+str(other)+"."+field+" is supposed to be type "+str(self.types[field])+", not "+str(meth))
                    else:
                        notInField = True
                        mynode.error("type "+str(other)+" missing field "+field+" to be upcasted to "+str(self))

                i += 1
        except EOFError as e:
            if notInField:
                beforeError(e, "")
            else:
                beforeError(e, "Field '" + field + "' in " + str(other) + ": ")

class T(Type):
    def __init__(self, name, typ, owner):
        self.type = typ
        self.normalName = owner+"."+name
        self.name = owner+"."+name
        self.types = self.type.types
        self.owner = owner
        self.realName = name

    def duckType(self, parser, other, node, mynode, iter):
        if self.name == other.name:
            return True

        if type(other) is T and self.normalName != other.normalName and self.type == other.type:
            return True

        Type.duckType(self, parser, other, node, mynode, iter)
        #self.type.duckType(parser, other, node, mynode, iter)

    def hasMethod(self, parser, name):
        self.type.hasMethod(parser, name)

class Enum(Type):
    def __init__(self, package, name, const, generic):
        self.generic = generic

        self.const = const
        self.types = {}

        self.package = package
        self.normalName = name

        self.remainingGen = generic
        self.methods = {}

        gen = self.remainingGen

        # print(self.gen)

        genericS = "[" + ",".join([str(gen[i]) for i in gen]) + "]" if len(gen) > 0 else ""

        self.name = (package + "." if package != "_global" else "") + name + genericS

    def addMethod(self, parser, name, method):
        package = parser.package

        if package in self.methods:
            if name in self.methods[package]:
                Error.parseError(parser, "method "+self.name+"."+name+" already exists")
            self.methods[package][name] = method
        else:
            self.methods[package] = {name: method}

    def hasMethod(attachTyp, parser, name):
        self = parser.interfaces[attachTyp.package][attachTyp.normalName]

        packages = []
        b = None
        for i in parser.imports+[parser.package]+["_global"]:
            if not i in self.methods: continue
            if name in self.methods[i]:
                b = self.methods[i][name]
                b.package = i

                if not i in packages:
                    packages.append(i)

        if len(packages) > 1:
            self.node.error("ambiguous, multiple definitions of the method "+self.name+"."+name+" in packages: "+", ".join(packages[:-1])+" and "+packages[-1])

        return replaceT(b, attachTyp.generic)

    def duckType(self, parser, other, node, mynode, iter):
        if self.normalName != other.normalName:
            node.error("expecting type "+self.name+", not "+str(other))

        for name in self.generic:
            a = self.generic[name]
            b = other.generic[name]

            if not (type(b) is T and b.owner == (self.package+"." if self.package != "_global" else "")+self.normalName):
                if a != b:
                    Error.error("For generic parameter "+name+": "+"Expecting type "+str(a)+", but got type "+str(b))

All = Interface(False, {})

def isGeneric(t):
    if type(t) in [FuncPointer]:
        if not (type(t.generic) in [dict,coll.OrderedDict]):
            print(type(t.generic))

        if t.generic != {}: return True
        for i in t.args:
            if isGeneric(i): return True
        return isGeneric(t.returnType)
    elif type(t) is Array and isGeneric(t.elemT): return True
    elif type(t) is T: return True
    elif type(t) is Interface: return t.normalName != t.name
    elif type(t) is Struct: return t.normalName != t.name
    elif type(t) is Assign: return True
    elif type(t) is Tuple:
        for i in t.list:
            if isGeneric(i):
                return True

    return False

class Null(Type):
    name = "none"
    types = {}

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
        gen = s.gen
        for i in gen:
            if ".".join(i.split(".")[:-1]) == s.package+"."+s.normalName:
                args[i] = gen[i]

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
                "operator_mul": FuncPointer([self], self),
                "operator_eq": FuncPointer([self], Bool()),
                "operator_gt": FuncPointer([self], Bool()),
                "operator_lt": FuncPointer([self], Bool()),
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

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) in [I32,Float]:
            mynode.error("expecting type " + str(self) + ", or "+str(I32())+" and got type " + str(other))

class Bool(Type):
    name = "bool"
    normalName = "bool"

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

def replaceT(typ, gen, acc={}):
    if typ in acc:
        return acc[typ]

    if type(typ) is T:
        if typ.normalName in gen:
            r = gen[typ.normalName]
            if type(r) is Underscore:
                #if type(typ.type) is Assign:
                return T(typ.realName, replaceT(typ.type, gen, acc), typ.owner)
                #return typ

            return r
        else:
            #if type(typ.type) is Assign:
            return T(typ.realName, replaceT(typ.type, gen, acc), typ.owner)
            #return typ
    elif type(typ) is Struct:
        rem = {}
        for i in typ.remainingGen:
            rem[i] = replaceT(typ.remainingGen[i], gen, acc)
        return Struct(False, typ.normalName, typ.types, typ.package, rem)
    elif type(typ) is Assign:
        return Assign(replaceT(typ.const, gen, acc))
    elif type(typ) is Interface:
        types = typ.types

        c = Interface(False,{})

        if acc == {}:
            acc = {typ: c}
        else:
            acc[typ] = c

        types = {i: replaceT(types[i], gen, acc) for i in types}

        new = Interface(False, types, gen, typ.normalName)
        c.fromObj(new)

        """
        if len(gen) != 0:
            c.name = typ.normalName+genericS
            c.normalName = typ.normalName
            c.generic = {i: gen[i] for i in gen if ".".join(i.split(".")[:-1]) == typ.normalName}
        """
        return c
    elif type(typ) is Enum:
        const = coll.OrderedDict()
        g = {}

        for name in typ.const:
            const[name] = [replaceT(i, gen, acc) for i in typ.const[name]]

        for name in typ.generic:
            g[name] = replaceT(typ.generic[name], gen, acc)

        return Enum(typ.package, typ.normalName, const, g)
    elif type(typ) is Tuple:
        arr = []
        for i in typ.list:
            arr.append(replaceT(i, gen, acc))

        return Types.Tuple(arr)

    elif isGeneric(typ):
        if type(typ) is Array:
            return Array(False, replaceT(typ.elemT, gen, acc))
        generics = typ.generic
        if type(typ) is FuncPointer:
            arr = []
            for i in typ.args:
                arr.append(replaceT(i, gen, acc))

            newTyp = replaceT(typ.returnType, gen, acc)
            return FuncPointer(arr, newTyp, remainingT(newTyp), do= typ.do)
    else:
        return typ

def Lambda(func, vars, typ= False, do= False):
    if not typ:
        typ = Unknown(-1, func)
    f = FuncPointer(vars, typ, do= do)
    f.already = False
    f.scope = False
    f.func = func

    def duckType(self, parser, other, node, mynode, iter):
        if not type(other) is FuncPointer:
            mynode.error("expecting function type " + str(self) + " and got type " + str(other))

        if len(other.args) != len(self.args):
            mynode.error("expecting function type " + str(self) + " and got type " + str(other))

        if not self.do and other.do:
            mynode.error("Expecting pure function " + str(self) + " and got effectfull function " + str(other))
        elif self.do and not other.do:
            mynode.error("Expecting effectfull function " + str(self) + " and got pure function " + str(other))

        count = -1
        for (a, i) in zip(self.args, other.args):
            count += 1
            try:
                if type(a) is Unknown:
                    self.args[count] = i
                else:
                    i.duckType(parser, a, mynode, node, iter)
            except EOFError as e:
                beforeError(e, "Function type argument " + str(count) + ": ")

        try:
            self.returnType.duckType(parser, other.returnType, node, mynode, iter)
        except EOFError as e:
            beforeError(e, "Function type return type: ")

    def check(self, parser):
        name = ("do " if do else "") + "|" + ", ".join([i.name for i in self.args]) + "| -> " + self.returnType.name

        self.name = name

        if self.already:
            return

        for i in self.args:
            if type(i) is Unknown: return

        from TopCompiler import TypeInference
        from TopCompiler import Scope



        for (a,b) in zip(func.nodes[0], func.type.args):
            a.varType = b

        if self.scope:
            self.already = True
            s = parser.scope[parser.package]

            parser.scope[parser.package] = self.scope
            Scope.incrScope(parser)

            err = False
            try:
                TypeInference.infer(parser, func.nodes[0])
                TypeInference.infer(parser, func.nodes[1])
            except EOFError as e:
                err = str(e)

            Scope.decrScope(parser)
            parser.scope[parser.package] = s

            if err:
                e = EOFError(err)
                e.special = True

                raise e

            if len(func.nodes[1]) == 0:
                typ = Types.Null()
            else:
                typ = func.nodes[1].nodes[-1].type
            self.returnType = typ
            func.nodes[1].returnType = typ

        name = ("do " if do else "") + "|" + ", ".join([i.name for i in self.args]) + "| -> " + self.returnType.name
        self.name = name

    def getstate(self):
        self = f
        if self.already:
            c = FuncPointer(self.args, self.returnType)
            c.do = self.do
            c.generic = self.generic
            c.name = self.name

            return c.__dict__

    import types

    f.duckType = types.MethodType(duckType, f)
    f.check = types.MethodType(check, f)
    f.__getstate__ = types.MethodType(getstate, f)
    f.isLambda = True

    return f


class Unknown(Type):
    def __init__(self, index, func):
        Type.__init__(self)

        self.name = "Unkown type"
        self.types = {}
        self.index = index
        self.func = func

    def __eq__(self, other):

        self.func.check()

    def duckType(self, parser, other, node, mynode, iter):
        if self.index == -1:
            self.func.type.returnType = other
        else:
            self.func.type.args[self.index] = other
        self.func.type.check(parser)







