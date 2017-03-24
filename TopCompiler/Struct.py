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

class Struct:
    def __init__(self, name, fieldType, actualfields, gen, node, package):
        self.fieldType = fieldType

        self.offsets = {}
        self.types = {}

        self.package = package

        self.generic = gen

        self.name = name
        self.normalName = name

        self.node = node

        for i in range(len(actualfields)):
            self.offsets[actualfields[i].name] = i
            self.types[actualfields[i].name] = self.fieldType[i]

        self.methods = {}

    def addMethod(self, parser, name, method):
        package = parser.package

        if package in self.methods:
            if name in self.methods[package]:
                Error.parseError(parser, "method "+self.name+"."+name+" already exists")
            self.methods[package][name] = method
        else:
            self.methods[package] = {name: method}

    def __str__(self):
        return "'type "+self.package+"."+self.name+"'"

    def hasMethod(self, parser, name):
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
        if parser.thisToken().token in ["with", "either"]:
            tmp = parser.currentNode
            if parser.thisToken().token == "either":
                Enum.enumParser(parser, name, decl, gen)
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
        types = parser.structs[parser.package][name].types

        parser.structs[parser.package][name] = Struct(name, args, fields, gen, typ, parser.package)
        tmp =  parser.structs[parser.package][name].types
        parser.structs[parser.package][name].methods = meth
        parser.structs[parser.package][name].package = parser.package
        parser.structs[parser.package][name].types = types
        types.update(tmp)

        Scope.changeType(parser, name, parser.structs[parser.package][name] )

    typ.struct = parser.structs[parser.package][name]

    Scope.decrScope(parser)

def initStruct(parser, package= ""):
    numB = parser.curly
    unary = False
    if ExprParser.isUnary(parser, parser.lookBehind()):
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

    if not field.type in ["identifier", "i32"]:
        Error.parseError(parser, "field name must be an identifer")

    acess = Tree.Field(0, Types.Null(), parser)
    acess.number = field.type == "i32"

    field = field.token

    acess.addNode(parser.currentNode.nodes[-1])
    acess.owner = parser.currentNode

    acess.field = field

    parser.currentNode.nodes[-1] = acess

Parser.exprToken["type"] = typeParser
Parser.exprToken["."] = index


def offsetsToList(offsets):
    array = [0] * len(offsets)
    for key in offsets:
        array[offsets[key]] = key
    return array

Parser.exprToken["{"] = initStruct
Parser.exprToken["}"] = closeCurly