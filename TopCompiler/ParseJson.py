from TopCompiler import FuncParser
from TopCompiler import Error
from TopCompiler import Parser
from TopCompiler import Scope
from TopCompiler import Types
import AST as Tree

def parseJson(parser):
    parse = Tree.ParseJson(parser)
    parser.currentNode.addNode(parse)
    parser.currentNode = parse

    parser.nextToken()

    typ = Types.parseType(parser)

    if parser.lookInfront().token == ",":
        parser.nextToken()
        while not Parser.isEnd(parser):
            parser.nextToken()
            Parser.callToken(parser)

    if len(parse.nodes) > 1:
        Error.parseError(parser, "expecting only 1 node")

    parse.shouldBeTyp = typ

    if len(parse.nodes) == 0:
        parse.type = Types.FuncPointer([Types.String(0)], typ)
    else:
        parse.type = typ

    parser.currentNode = parse.owner

Parser.exprToken["parseJson"] = parseJson