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
        count += 1

        if b.type == "identifier":
            VarParser.createParser(parser, b, typ= Types.Unknown(count, place), check= False)
            b = parser.nextToken()
            continue
        elif b.token == ",":
            b = parser.nextToken()
            continue

        Parser.declareOnly(parser)
        b = parser.Parser.nextToken(parser)

    vars = [i.varType for i in brace]

    typ = False
    do = False

    if parser.nextToken().token == "->":
        typ = Types.parseType(parser)

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

    while not Parser.isEnd(parser):
        Parser.callToken(parser, lam = first)
        parser.nextToken()
        first = False

    ExprParser.endExpr(parser)

    if typ:
        place.type = Types.Lambda(place, vars, typ = typ, do=do)
    else:
        place.type = Types.Lambda(place, vars, do= do)

    parser.currentNode = place.owner


Parser.exprToken["|"] = func