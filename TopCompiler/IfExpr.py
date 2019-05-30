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
    assign = False

    while not (Parser.isEnd(parser) and then) :
        if parser.thisToken().token == ":=":
            assign = True

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

        token = parser.thisToken()

        if token.token == "then" and not then:
            then = True
            ExprParser.endExpr(parser)

            parser.nodeBookmark.pop()

            block = Tree.Block(parser)
            cond.owner.addNode(block)
            parser.currentNode = block
            continue

        next = parser.lookInfront()
        if (next.token == "else" or next.token == "elif") and isEnd:
            break

    ExprParser.endExpr(parser)

    cond.type = Types.Bool()

    parser.currentNode = cond.owner.owner

    if assign:
        m = Tree.Match(cond.owner)
        m.addNode(cond.nodes[1])

        c = Tree.MatchCase(cond)
        c.addNode(cond.nodes[0])

        m.addNode(c)

        m.addNode(cond.owner.nodes[1])

        c = Tree.MatchCase(cond)
        u = Tree.Under(cond)
        c.addNode(u)

        m.addNode(c)

        b = Tree.Block(cond.owner)

        m.addNode(b)

        parser.currentNode.nodes[-1] = m
        m.owner = parser.currentNode

        b.ifexpr = m.owner

def ifExpr(parser):
    toplevel = Tree.If(parser)

    parser.currentNode.addNode(toplevel)
    parser.currentNode = toplevel

    ifBody(parser)

def ifPatternMatch(parser):
    return parser.currentNode.nodes[-1].nodes[-1].ifexpr

def elifExpr(parser, canHaveElse=False):
    ifexpr = False
    if not canHaveElse:
        try:
            inside = parser.currentNode.nodes[-1].nodes[-2]
        except IndexError:
            Error.parseError(parser, "unexpected elif")

        if not type(inside) is Tree.IfCondition:
            ifexpr = ifPatternMatch(parser)
            if not ifexpr:
                Error.parseError(parser, "unexpected elif")

    if ifexpr:
        parser.currentNode = parser.currentNode.nodes[-1].nodes[-1]

        while len(parser.currentNode.nodes) > 0:
            parser.currentNode = parser.currentNode.nodes[-1]

        ifExpr(parser)
        parser.currentNode = ifexpr
    else:
        parser.currentNode = parser.currentNode.nodes[-1]
        ifBody(parser)

import copy

def return_some_error(parser, case_name = "Some"):
    prev = parser.currentNode

    m = Tree.Match(parser)
    parser.currentNode.addNode(m)
    parser.currentNode = m


    while not (Parser.isEnd(parser)):
        parser.nextToken()
        Parser.callToken(parser)

    #ExprParser.endExpr(parser, -2)
    parser.currentNode = m.owner

    case = Tree.MatchCase(parser)
    m.addNode(case)

    r = Tree.ReadVar("Some", True, parser)
    r.package = "_global"

    f = Tree.FuncCall(parser)
    f.addNode(r)

    case.addNode(f)

    r = Tree.ReadVar("_x", False, parser)
    r.package = parser.package

    f.addNode(r)

    block = Tree.Block(parser)
    m.addNode(block)

    ret = Tree.Return(parser)
    block.addNode(ret)

    f2 = Tree.FuncCall(parser)

    some = Tree.ReadVar(case_name, True, parser)
    some.package = "_global"

    f2.addNode(copy.copy(some))
    f2.addNode(copy.copy(r))

    ret.addNode(f2)

    case = Tree.MatchCase(parser)
    m.addNode(case)

    case.addNode(Tree.Under(parser))

    m.addNode(Tree.Block(parser))

    parser.currentNode = prev

Parser.exprToken["if"] = ifExpr
Parser.exprToken["elif"] = elifExpr
Parser.exprToken["?"] = return_some_error
Parser.exprToken["?e"] = lambda p: return_some_error(p, case_name="Error")