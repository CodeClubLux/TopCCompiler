__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import Error
from TopCompiler import ExprParser
from TopCompiler import Scope
from TopCompiler import Types

def isBoolCondition(parser, cond):
    if len(cond.nodes) > 0 :
        if cond.nodes[0].type != Types.Bool() or len(cond.nodes) != 1:
            cond.error( "expecting single boolean expression")


def ifBody(parser):
    cond = Tree.IfCondition(parser)

    parser.currentNode.addNode(cond)
    parser.currentNode = cond

    single = 0

    parser.nodeBookmark.append(0)

    then = False
    while not (Parser.isEnd(parser) and then) :
        token = parser.nextToken()

        if token.token == "then" and not then:
            then = True
            ExprParser.endExpr(parser)

            parser.nodeBookmark.pop()

            block = Tree.Block(parser)
            cond.owner.addNode(block)
            parser.currentNode = block
            continue

        isEnd = Parser.maybeEnd(parser)

        if (token.token in ["else", "elif"]) and isEnd:
            break

        token = parser.thisToken()

        Parser.callToken(parser)

        next = parser.lookInfront()
        if (next.token == "else" or next.token == "elif") and isEnd:
            break

    ExprParser.endExpr(parser)

    cond.type = Types.Bool()

    parser.currentNode = cond.owner.owner

def ifExpr(parser):
    toplevel = Tree.If(parser)

    parser.currentNode.addNode(toplevel)
    parser.currentNode = toplevel

    ifBody(parser)

def elifExpr(parser):
    try:
        inside = parser.currentNode.nodes[-1].nodes[-2]
    except IndexError:
        Error.parseError(parser, "unexpected elif")

    if not type(inside) is Tree.IfCondition:
        Error.parseError(parser, "unexpected elif")
    parser.currentNode = parser.currentNode.nodes[-1]

    ifBody(parser)

Parser.exprToken["if"] = ifExpr
Parser.exprToken["elif"] = elifExpr
