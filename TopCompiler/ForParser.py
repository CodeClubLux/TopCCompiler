__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import IfExpr
from TopCompiler import Scope
from TopCompiler import Error

def forExpr(parser):
    toplevel = Tree.For(parser)

    parser.currentNode.addNode(toplevel)
    parser.currentNode = toplevel

    parser.nextToken()

    while not (Parser.isEnd(parser) and not parser.thisToken().token == "do"):
        token = parser.nextToken()
        Parser.callToken(token)

    if parser.thisToken().token != "do":
        Error.parseError(parser, "Expecting do")

    if len(toplevel.nodes) != 1 or not type(toplevel.nodes[0]) is Tree.CreateAssign:
        Error.parseError(parser, "Expecting := and then do")

    while not Parser.isEnd(parser):
        token = parser.nextToken()
        Parser.callToken(token)

    parser.currentNode = toplevel.owner

Parser.exprToken["for"] = forExpr
