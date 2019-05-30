__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import IfExpr
from TopCompiler import Scope
from TopCompiler import Error
import copy

def whileExpr(parser):
    toplevel = Tree.While(parser)

    parser.currentNode.addNode(toplevel)
    parser.currentNode = toplevel

    n = Tree.WhilePreCondition(parser)
    cond = Tree.WhileCondition(parser)

    parser.currentNode.addNode(n)
    parser.currentNode.addNode(cond)
    parser.currentNode = cond

    assign = False
    block = None

    while not (Parser.isEnd(parser) and not parser.thisToken().token in ["!", "do", ":="]):
        token = parser.nextToken()
        if token.token == ":=" and not block:
            assign = True

        iter = parser.iter
        if token.token == "do" :
            ExprParser.endExpr(parser)

            block = Tree.WhileBlock(parser)
            cond.owner.addNode(block)
            parser.currentNode = block

            continue

        Parser.callToken(parser)
        if parser.thisToken().token == ":=":
            assign = True

    ExprParser.endExpr(parser)

    parser.currentNode = n.owner.owner

    if assign:
        m = Tree.Match(cond.owner)
        m.addNode(cond.nodes[1])

        c = Tree.MatchCase(cond)
        c.addNode(cond.nodes[0])

        m.addNode(c)

        new_block = Tree.Block(block)
        new_block.nodes = block.nodes
        for i in new_block.nodes:
            i.owner = new_block

        m.addNode(new_block)

        c = Tree.MatchCase(cond)
        u = Tree.Under(cond)
        c.addNode(u)

        m.addNode(c)

        b = Tree.Block(cond.owner)
        b.addNode(Tree.Break(cond))

        m.addNode(b)

        cond.nodes = [Tree.Bool("true", cond)]
        cond.nodes[0].owner = cond

        block.nodes = [m]
        m.owner = block

        b.ifexpr = m.owner

Parser.exprToken["while"] = whileExpr

Parser.exprToken["break"] = lambda parser: parser.currentNode.addNode(Tree.Break(parser))
Parser.exprToken["continue"] = lambda parser: parser.currentNode.addNode(Tree.Continue(parser))

Parser.exprToken["then"] = lambda parser: Error.parseError(parser, "unexpected then keyword")
Parser.exprToken["do"] = lambda parser: Error.parseError(parser, "unexpected do keyword")
