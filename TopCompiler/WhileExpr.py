__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import IfExpr
from TopCompiler import Scope
from TopCompiler import Error

def whileExpr(parser):
    toplevel = Tree.While(parser)

    parser.currentNode.addNode(toplevel)
    parser.currentNode = toplevel

    n = Tree.WhilePreCondition(parser)
    cond = Tree.WhileCondition(parser)

    parser.currentNode.addNode(n)
    parser.currentNode.addNode(cond)
    parser.currentNode = cond

    while not Parser.isEnd(parser):
        token = parser.nextToken()

        iter = parser.iter
        if token.token == "do" :
            ExprParser.endExpr(parser)

            block = Tree.WhileBlock(parser)
            cond.owner.addNode(block)
            parser.currentNode = block

            continue

        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = n.owner.owner

Parser.exprToken["while"] = whileExpr

Parser.exprToken["break"] = lambda parser: parser.currentNode.addNode(Tree.Break(parser))
Parser.exprToken["continue"] = lambda parser: parser.currentNode.addNode(Tree.Continue(parser))

Parser.exprToken["then"] = lambda parser: Error.parseError(parser, "unexpected then keyword")
Parser.exprToken["do"] = lambda parser: Error.parseError(parser, "unexpected do keyword")
