L__author__ = 'antonellacalvia'

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

    while not (Parser.isEnd(parser) or parser.thisToken().token == "do"):
        token = parser.nextToken()
        if token.token == "do":
            break
        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.nodeBookmark.append(len(parser.currentNode.nodes))

    if parser.thisToken().token != "do":
        Error.parseError(parser, "Expecting do")

    if len(toplevel.nodes) != 1 or not type(toplevel.nodes[0]) is Tree.CreateAssign:
        Error.parseError(parser, "Expecting := and then do")

    count = 0
    while not (Parser.isEnd(parser) and count > 0): #avoid breaking on do keyword
        count += 1
        token = parser.nextToken()
        Parser.callToken(parser)

    parser.nodeBookmark.pop()

    parser.currentNode = toplevel.owner

Parser.exprToken["for"] = forExpr