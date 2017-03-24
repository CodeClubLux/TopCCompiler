__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import Error
from TopCompiler import Scope

def iterForIf(ifNode):
    i = 0
    while i < len(ifNode.nodes):
        i += 1

        yield ifNode.nodes[i]

        i += 1

def checkIf(parser, i):
    typ = i.nodes[1].type

    for iter in i.nodes[3:][::2]:
        try:
            thisTyp = iter.type

            typ.duckType(parser, thisTyp, iter, i, 0)
        except EOFError as e:
            try:
                thisTyp.duckType(parser, typ, i, iter, 0)
                typ = thisTyp
            except EOFError:
                Error.beforeError(e, "Type mismatch in arms of if ")

        #if iter.type != typ:
        #    (iter.nodes[-1] if len(iter.nodes) > 0 else iter).error("type mismatch in arms of if, "+str(iter.type)+" and "+str(typ))

    i.type = i.nodes[1].type

def elseExpr(parser):
    toplevel = Tree.Else(parser)

    try:
        inside = parser.currentNode.nodes[-1].nodes[-2]
    except IndexError:
        Error.parseError(parser, "unexpected else")

    if not type(inside) is Tree.IfCondition:
        Error.parseError(parser, "unexpected else")

    parser.currentNode.nodes[-1].addNode(toplevel)
    parser.currentNode = toplevel

    block = Tree.Block(parser)
    parser.currentNode.owner.addNode(block)
    parser.currentNode = block

    opening = None
    single = 0

    while not Parser.isEnd(parser):
        token = parser.nextToken()

        Parser.callToken(parser)

    ExprParser.endExpr(parser)
    parser.currentNode = toplevel.owner.owner

Parser.exprToken["else"] = elseExpr
