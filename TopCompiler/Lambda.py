from TopCompiler import Scope
from TopCompiler import Types
from TopCompiler import Parser
from TopCompiler import VarParser
from TopCompiler import ExprParser
import AST as Tree

def func(parser):
    place = Tree.Lambda(parser)
    parser.currentNode.addNode(place)

    brace = Tree.FuncBraceOpen(parser)
    place.addNode(brace)

    parser.currentNode = brace

    b = parser.nextToken()

    count = -1

    while parser.thisToken().token != "|":
        if b.type == "identifier" and parser.lookInfront().token != ":":
            count += 1
            VarParser.createParser(parser, b, typ= Types.Unknown(count, place), check= False)
            b = parser.nextToken()
            continue
        elif parser.thisToken().token == ":":
            count += 1
        elif b.token == ",":
            b = parser.nextToken()
            continue

        Parser.declareOnly(parser)
        b = parser.nextToken()

    vars = [i.varType for i in brace]

    typ = False
    do = False

    parser.nextToken()

    if parser.thisToken().token == "->":
        parser.nextToken()
        typ = Types.parseType(parser)
        parser.nextToken()

    body = Tree.FuncBody(parser)

    place.addNode(body)
    parser.currentNode = body

    if parser.thisToken().token == "do":
        do = True
        parser.nextToken()

    brace.do = do
    brace.body = body
    body.do = do

    first = True

    parser.iter -= 1

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.callToken(parser, lam=first)
        first = False

    ExprParser.endExpr(parser)

    if typ:
        place.type = Types.Lambda(place, vars, typ = typ, do=do)
    else:
        place.type = Types.Lambda(place, vars, do= do)

    parser.currentNode = place.owner


Parser.exprToken["|"] = func