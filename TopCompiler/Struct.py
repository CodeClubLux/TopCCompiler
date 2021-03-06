__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Types
import AST as Tree
from TopCompiler import Error
from TopCompiler import Scope
from TopCompiler import VarParser
from TopCompiler import ExprParser
from TopCompiler import PackageParser
from TopCompiler import MethodParser
from TopCompiler import Interface
from TopCompiler import FuncParser
from TopCompiler import Enum
from TopCompiler import Alias

class Struct:
    def __init__(self, name, fieldType, actualfields, gen, node, package):
        self.fieldType = fieldType

        self.offsets = {}
        self.types = {}
        self._types = {}

        self.package = package

        self.generic = gen

        self.name = name
        self.normalName = name

        self.node = node

        self.externalStruct = False

        for i in range(len(actualfields)):
            self.offsets[actualfields[i].name] = i
            self._types[actualfields[i].name] = self.fieldType[i]

        self.methods = {}
        self.actualfields = actualfields

        self.using = []

    def toCType(self):
        Error.error("no type introspection yet")

    def addMethod(self, i, parser, name, method):
        package = parser.package

        if package in self.methods:
            if name in self.methods[package]:
                i.error("method "+self.name+"."+name+" already exists")
            self.methods[package][name] = method
        else:
            self.methods[package] = {name: method}

    def __str__(self):
        return "'type "+self.package+"."+self.name+"'"

    def isType(self, other):
        return type(self) is other

    def hasMethod(self, parser, name, isP=False):
        packages = []
        b = None
        for i in [parser.package,self.package, "_global"]+parser.imports:
            if not i in self.methods: continue
            if name in self.methods[i]:
                b = self.methods[i][name]
                b.package = i

                if not i in packages:
                    packages.append(i)

        if len(packages) > 1:
            self.node.error("ambiguous, multiple definitions of the method "+self.name+"."+name+" in packages: "+", ".join(packages[:-1])+" and "+packages[-1])

        return b

    def getMethods(self, parser):
        meths = {}
        for i in parser.imports + [parser.package] + ["_global"]:
            if not i in self.methods: continue
            meths.update(self.methods[i])

        return meths
def typeParser(parser, decl= False):
    name = parser.nextToken()

    Scope.incrScope(parser)


    if name.type != "identifier" and name.token != "ext":
        Error.parseError(parser, "type name must be an identifier")

    externalStruct = False
    if name.token == "ext":
        externalStruct = True
        name = parser.nextToken()

        if name.type != "identifier" and name.token != "ext":
            Error.parseError(parser, "type name must be an identifier")

    name = name.token

    if name[0].lower() == name[0] and not externalStruct:
        Error.parseError(parser, "struct name must be upper case")

    import collections as coll
    gen = coll.OrderedDict()

    if parser.nextToken().token == "[":
        if externalStruct:
            Error.parseError(parser, "External structs cannot be generic")
        gen = FuncParser.generics(parser, name)

    if parser.thisToken().token != "=":
        if parser.thisToken().token in ["with", "either", "is"]:
            if externalStruct:
                Error.parseError(parser, "Can only define external structs not interfaces, enums or aliases")
            tmp = parser.currentNode
            if parser.thisToken().token == "either":
                Enum.enumParser(parser, name, decl, gen)
            elif parser.thisToken().token == "is":
                Alias.aliasParser(parser, name, decl, gen)
            else:
                parser.currentNode = Tree.PlaceHolder(parser)
                Interface.traitParser(parser, name, decl, gen)
                parser.currentNode = tmp
            return

        Error.parseError(parser, "expecting =")
    tmp = parser.currentNode

    typ = Tree.Type(parser.package, name, parser)
    typ.package = parser.package
    typ.normalName = name
    typ.externalStruct = externalStruct

    tmp.addNode(typ)

    parser.currentNode = typ

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.declareOnly(parser, noVar=True)

    args = [i.varType for i in parser.currentNode]
    fields = parser.currentNode.nodes

    if not decl:
        using = parser.structs[parser.package][name].using
        for i in parser.currentNode:
            if type(i) is Tree.Using:
                using.append(i.name)

    typ.fields = [i.name for i in typ]
    typ.args = args
    typ.generics = gen

    typ.nodes = []
    parser.currentNode = tmp

    if decl:
        meth = parser.structs[parser.package][name].methods
        _types = parser.structs[parser.package][name]._types

        #if name == "Channel":
        #    print("Channel make")
        #    print(id(_types))

        parser.structs[parser.package][name] = Struct(name, args, fields, gen, typ, parser.package)
        tmp =  parser.structs[parser.package][name]._types
        parser.structs[parser.package][name].methods = meth
        parser.structs[parser.package][name].package = parser.package
        parser.structs[parser.package][name]._types = _types
        parser.structs[parser.package][name].externalStruct = externalStruct
        _types.update(tmp)

        Scope.changeType(parser, name, parser.structs[parser.package][name] )

    typ.struct = parser.structs[parser.package][name]

    Scope.decrScope(parser)

def initStruct(parser, package= "", shouldRead=True):
    numB = parser.curly
    unary = not shouldRead
    if shouldRead and ExprParser.isUnary(parser, parser.lookBehind()):
        unary = True

    parser.curly += 1

    readVar = True

    if not unary:
        if package == "": package = parser.package

        if len(parser.currentNode.nodes) == 0:
            Error.parseError(parser, "unexpected {")
        if not type(parser.currentNode.nodes[-1]) in [Tree.ReadVar, Tree.Field]:
            Error.parseError(parser, "unexpected {")

        readVar = type(parser.currentNode.nodes[-1]) is Tree.ReadVar

        name = parser.currentNode.nodes[-1].name if readVar else parser.currentNode.nodes[-1].field

    init = Tree.InitStruct(parser)

    if not readVar:
        if type(parser.currentNode.nodes[-1].nodes[0]) is Tree.ReadVar:
            package = parser.currentNode.nodes[-1].nodes[0].name
            t = (parser.currentNode.nodes[-1].nodes[0])
            if not package in parser.imports:
                t.error("no package called " + package)

    init.package = package

    if not unary:
        init.constructor = parser.currentNode.nodes[-1]
        init.addNode(parser.currentNode.nodes[-1])

        del parser.currentNode.nodes[-1]

    init.mutable = False
    init.unary = unary

    parser.currentNode.addNode(init)
    parser.currentNode = init

    parser.nextToken()

    parser.nodeBookmark.append(0)

    while parser.thisToken().token != "}":
        if parser.thisToken().token in [",", "\n"]:
            ExprParser.endExpr(parser)
            parser.nodeBookmark[-1] = len(parser.currentNode.nodes)
        if parser.thisToken().token != ",": Parser.callToken(parser)

        t = parser.thisToken().token

        if t == "}" and parser.curly <= numB:
            break
        parser.nextToken()
    else:
        closeCurly(parser)

    ExprParser.endExpr(parser)

    parser.nodeBookmark.pop()

    parser.currentNode = init.owner

def closeCurly(parser):
    parser.curly -= 1
    if parser.curly < 0:
        Tree.PlaceHolder(parser).error("unexpected }")

def popAt(parser):
    pass

def index(parser, unary=False):

    if not unary:
        unary = ExprParser.isUnary(parser, parser.lookBehind())

    if not unary and len(parser.currentNode.nodes) == 0:
        Error.parseError(parser, "unexpected .")
    elif unary:
        Error.parseError(parser, "unexpected .")

    c = parser.thisToken()
    if c.token != ".":
        print("whattttt")

    field = parser.nextToken()

    if not field.type in ["identifier", "i32"]:
        print(c)
        print(field)
        Error.parseError(parser, "field name must be an identifier")

    acess = Tree.Field(0, Types.Null(), parser)
    acess.unary = unary
    acess.number = field.type == "i32"

    field = field.token

    acess.owner = parser.currentNode
    acess.field = field

    if not unary:
        acess.addNode(parser.currentNode.nodes[-1])
        parser.currentNode.nodes[-1] = acess
    else:
        Error.parseError(parser, "unexpected .")

Parser.exprToken["type"] = typeParser
Parser.exprToken["."] = index
Parser.exprType["dotS"] = lambda parser, token: index(parser, unary=True)

def offsetsToList(offsets):
    #print(offsets)
    array = [0] * len(offsets)
    for key in offsets:
        array[offsets[key]] = key
    return array

Parser.exprToken["{"] = initStruct
Parser.exprType["bracketOpenS"] = lambda parser, tok: initStruct(parser, shouldRead=False)
Parser.exprToken["}"] = closeCurly