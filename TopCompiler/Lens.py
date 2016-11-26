
import AST as Tree

from TopCompiler import Types
from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import VarParser
from TopCompiler import Scope
from TopCompiler import ExprParser

def parseLens(parser):
    parser.nextToken()
    Scope.incrScope(parser)
    lensType = Types.parseType(parser)
    Scope.decrScope(parser)

    place = Tree.PlaceHolder(parser)

    lens = Tree.Lens(parser)
    lens.place = place
    lens.lensType = lensType

    parser.currentNode.addNode(lens)

    parser.currentNode = lens


    place.type = lensType

    lens.addNode(place)

    parser.nextToken()

    while not Parser.isEnd(parser):
        Parser.callToken(parser)
        parser.nextToken()

    ExprParser.endExpr(parser)

    parser.currentNode = lens.owner


Parser.exprToken["lens"] = parseLens