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

class Struct:
    def __init__(self, name, fieldType, actualfields, gen):
        self.fieldType = fieldType

        self.offsets = {}
        self.types = {}

        self.generic = gen

        self.name = name
        self.normalName = name

        for i in range(len(actualfields)):
            self.offsets[actualfields[i].name] = i
            self.types[actualfields[i].name] = self.fieldType[i]

        self.methods = {}

    def addMethod(self, parser, name, method):
        package = parser.package

        if package in self.methods:
            if name in parser.structs[package][self.name].methods[package]:
                Error.parseError(parser, "method "+self.name+"."+name+" already exists")
            self.methods[package][name] = method
        else:
            self.methods[package] = {name: method}

    def hasMethod(self, parser, name):
        packages = []
        b = None
        for i in parser.imports+[parser.package]+["_global"]:
            if not i in self.methods: continue
            if name in self.methods[i]:
                b = self.methods[i][name]
                b.package = i
                packages.append(i)

        if len(packages) > 1:
            Error.parseError(parser, "ambiguous, multiple definitions of the method "+self.name+"."+name+" in packages: "+", ".join(packages[:-1])+" and "+packages[-1])

        return b

def typeParser(parser, decl= False):
    name = parser.nextToken()

    Scope.incrScope(parser)


    if name.type != "identifier":
        Error.parseError(parser, "type name must be an identifier")
    name = name.token

    if name[0].lower() == name[0]:
        Error.parseError(parser, "struct name must be upper case")

    import collections as coll
    gen = coll.OrderedDict()

    if parser.nextToken().token == "[":
        gen = FuncParser.generics(parser, name)

    if parser.thisToken().token != "=":
        if parser.thisToken().token == "with":
            tmp = parser.currentNode
            parser.currentNode = Tree.PlaceHolder(parser)
            Interface.traitParser(parser, name, decl, gen)
            parser.currentNode = tmp
            return

        Error.parseError(parser, "expecting =")
    tmp = parser.currentNode

    typ = Tree.Type(parser.package, name, parser)
    typ.package = parser.package
    typ.normalName = name

    tmp.addNode(typ)

    parser.currentNode = typ

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.declareOnly(parser, noVar=True)

    args = [i.varType for i in parser.currentNode]
    fields = parser.currentNode.nodes

    typ.fields = [i.name for i in typ]

    typ.nodes = []
    parser.currentNode = tmp

    if decl:
        meth = parser.structs[parser.package][name].methods
        parser.structs[parser.package][name] = Struct(name, args, fields, gen)
        parser.structs[parser.package][name].methods = meth
        parser.structs[parser.package][name].package = parser.package

    Scope.decrScope(parser)

def initStruct(parser, package= ""):
    numB = parser.curly
    if ExprParser.isUnary(parser, parser.lookBehind()):
        Error.parseError(parser, "unexpected {")

    parser.curly += 1

    if package == "": package = parser.package

    if len(parser.currentNode.nodes) == 0:
        Error.parseError(parser, "unexpected {")
    if not type(parser.currentNode.nodes[-1]) in [Tree.ReadVar, Tree.Field]:
        Error.parseError(parser, "unexpected {")

    readVar = type(parser.currentNode.nodes[-1]) is Tree.ReadVar

    name = parser.currentNode.nodes[-1].name if readVar else parser.currentNode.nodes[-1].field

    init = Tree.InitStruct(parser)

    if not readVar:
        package = parser.currentNode.nodes[-1].nodes[0].name
        t = (parser.currentNode.nodes[-1].nodes[0])
        if not package in parser.imports:
            t.error("no package called " + package)
        elif not type(t) is Tree.ReadVar:
            init.error("unexpected {")

    init.package = package

    del parser.currentNode.nodes[-1]

    try:
        s = parser.structs[package][name]
    except KeyError:
        init.error("no struct called "+package+"."+name)

    init.paramNames = offsetsToList(parser.structs[package][name].offsets)
    init.s = s
    init.mutable = False

    parser.currentNode.addNode(init)
    parser.currentNode = init

    parser.nextToken()

    while parser.thisToken().token != "}":

        if parser.thisToken().token == ",":
            ExprParser.endExpr(parser)
        else: Parser.callToken(parser)

        t = parser.thisToken().token

        if t == "}" and parser.curly <= numB:
            break
        parser.nextToken()
    else:
        closeCurly(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = init.owner

def closeCurly(parser):
    parser.curly -= 1
    if parser.curly < 0:
        Tree.PlaceHolder(parser).error("unexpected }")

def index(parser):
    if len(parser.currentNode.nodes) == 0:
        Error.parseError(parser, "unexpected .")

    field = parser.nextToken()

    if field.type != "identifier":
        Error.parseError(parser, "field name must be an identifer")
    field = field.token

    acess = Tree.Field(0, Types.Null(), parser)

    acess.addNode(parser.currentNode.nodes[-1])
    acess.owner = parser.currentNode

    acess.field = field

    parser.currentNode.nodes[-1] = acess

Parser.exprToken["type"] = typeParser
Parser.exprToken["."] = index


def offsetsToList(offsets):
    array = [0] * 100
    for key in offsets:
        array[offsets[key]] = key
    return array

Parser.exprToken["{"] = initStruct
Parser.exprToken["}"] = closeCurly