__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import Error
from TopCompiler import Scope
from TopCompiler import IfExpr
import types

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

    i.type = typ

    for it in i.nodes[1:][::2]:
        if len(it.nodes) > 0:
            Tree.insertCast(it.nodes[-1], it.type, typ, -1)

def elseExpr(parser, canHaveElse=False):
    toplevel = Tree.Else(parser)
    ifexpr = False

    if not canHaveElse:
        try:
            inside = parser.currentNode.nodes[-1].nodes[-2]
        except IndexError:
            Error.parseError(parser, "unexpected else")

        if not type(inside) is Tree.IfCondition:
            ifexpr = IfExpr.ifPatternMatch(parser)

            if not ifexpr:
                Error.parseError(parser, "unexpected else")


    if not ifexpr:
        parser.currentNode.nodes[-1].addNode(toplevel)
        parser.currentNode = toplevel

        block = Tree.Block(parser)
        parser.currentNode.owner.addNode(block)
        parser.currentNode = block
    else:
        parser.currentNode = parser.currentNode.nodes[-1].nodes[-1]
        while len(parser.currentNode.nodes) > 0:
            parser.currentNode = parser.currentNode.nodes[-1]

        add_block = len(parser.currentNode.nodes) > 0
        if add_block:
            block = Tree.Block(parser)

            parser.currentNode.nodes[-1].addNode(toplevel)
            parser.currentNode.nodes[-1].addNode(block)
            parser.currentNode = parser.currentNode.nodes[-1]

            parser.currentNode = block

    opening = None
    single = 0

    while not Parser.isEnd(parser):
        token = parser.nextToken()

        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    if ifexpr:
        parser.currentNode = ifexpr
    else:
        parser.currentNode = toplevel.owner.owner

Parser.exprToken["else"] = elseExpr
