__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import FuncParser
from TopCompiler import Struct

def addMethod(node, parser, attachTyp, name, func, otherNode= False):
    if type(attachTyp) is Types.Struct:
        parser.structs[attachTyp.package][attachTyp.normalName].addMethod(parser, name,func)
    elif type(attachTyp) is Struct.Struct:
        if type(func) is Types.FuncPointer:
            if len(func.args) == 0:
                node.error("the function attached must have a first parameter with type "+attachTyp.package+"."+attachTyp.name)

            Types.Struct(False, attachTyp.name, attachTyp.types, attachTyp.package, attachTyp.generic).duckType(parser, func.args[0], node, otherNode, 0)

        attachTyp.addMethod(parser, name, func)
    else:
        node.error("Can't add method to "+attachTyp)
def checkIfOperator(parser, attachTyp, name, func):
    operators = {
        "add": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "sub": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "mul": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "div": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "eq": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
        "ne": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
        "mod": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "pow": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "getitem": Types.FuncPointer([attachTyp, Types.I32()], Types.I32() )
    }

    unary = {
        "add": Types.FuncPointer([attachTyp], attachTyp),
        "sub": Types.FuncPointer([attachTyp], attachTyp),
        "mul": Types.FuncPointer([attachTyp], attachTyp)
    }

    if name.startswith("operator_"):
        op = name[len("operator_"):]
        if not op in operators:
            Error.parseError(parser, "overload not found for operator_"+op)

        f = Types.FuncPointer(func.args, func.returnType)

        if f != operators[op]:
            Error.parseError(parser, "expecting function declaration "+str(operators[op])+", not "+str(f))
    elif name.startswith("unary_"):
        op = name[len("unary_"):]
        if not op in unary:
            Error.parseError(parser, "overload not found for unary_"+op)

        f = Types.FuncPointer(func.args, func.returnType)

        if f != unary[op]:
            Error.parseError(parser, "expecting function declaration "+str(unary[op])+", not "+str(f))


def methodHead(parser, attachTyp, decl):

    name = parser.nextToken()

    if name.type != "identifier":
        Error.parseError(parser, "function name must be of type identifier, not "+name.type)
    parser.nextToken()

    name = name.token

    if name[0].lower() != name[0]:
        Error.parseError(parser, "function name must be lower case")

    header = Tree.FuncStart(attachTyp.normalName+"_"+name, Types.Null(), parser)

    header.package = parser.package
    parser.currentNode.addNode(header)

    brace = Tree.FuncBraceOpen(parser)
    brace.name = attachTyp.normalName+"_"+name
    brace.package = header.package

    parser.currentNode.addNode(brace)

    parser.currentNode = brace

    if parser.thisToken().token != "(":
        Error.parseError(parser, "expecting (")

    parser.nextToken()
    parser.paren += 1

    returnType = Types.Null()

    self = parser.thisToken()
    if self.token == "var":
        imutable = False
        self = parser.nextToken()
    else: imutable = True

    typ = attachTyp

    if self.type != "identifier": Error.parseError(parser, "binding name must be identifier not "+self.type)
    self = self.token

    selfNode = Tree.Create(self, typ, parser)
    selfNode.package = parser.package
    selfNode.imutable = True
    #print(selfNode.varType)
    #print(attachTyp)

    parser.currentNode.addNode(selfNode)

    if not parser.nextToken().token in [")", ","]:
        Error.parseError(parser, "expecting comma not "+parser.thisToken().token)


    while parser.paren != parser.parenBookmark[-1] :
        b = parser.thisToken().token

        if b == ",":
            if parser.lookBehind().token == ",":
                Error.parseError(parser, "unexpected ,")
            parser.nextToken()
            continue
        Parser.declareOnly(parser)
        parser.nextToken()

    t = parser.thisToken()
    if t.token != "=":
        returnType = Types.parseType(parser)

        if parser.nextToken().token != "=":
            Error.parseError(parser, "expecting =")

    parser.currentNode = brace.owner

    names = [i.name for i in brace.nodes]
    types = [i.varType for i in brace.nodes]

    func = Types.FuncPointer(
        types,
        returnType,
    )

    header.method = True
    header.types = types[1:]
    header.attachTyp = attachTyp
    header.normalName = name

    checkIfOperator(parser, attachTyp, name, func)

    if decl:
        addMethod(brace, parser, attachTyp, name, func)

    return attachTyp.normalName+"_"+name, names, types, header, returnType