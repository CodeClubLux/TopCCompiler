__author__ = 'antonellacalvia'

from .Parser import *
from .Types import *
import AST as Tree
from .ExprParser import *
from .Error import *

def arrayLiteral(parser):
    if not isUnary(parser, parser.lookBehind()):
        arrayRead(parser)
        return

    mutable = parser.lookBehind().token == "mut"
    parser.nextToken()

    lastSize = 0
    typ = None

    arr = Tree.Array(parser)
    parser.currentNode.addNode(arr)
    parser.currentNode = arr

    rang = False
    init = False

    while parser.thisToken().token != "]":
        t = parser.thisToken()
        if parser.thisToken().token == ",":
            endExpr(parser)
            if lastSize == 0:
                if len(arr.nodes) < 1:
                    parseError(parser, "expecting single expression, per element in array")

            lastSize = len(parser.currentNode.nodes)
            parser.nextToken()
            continue
        elif parser.thisToken().token == "..":
            endExpr(parser)
            if init:
                parseError(parser, "unexpected ..")

            if lastSize != 0:
                parseError(parser, "unexpected ..")

            rang = True
            arr.range = rang
            parser.nextToken()
            continue
        elif parser.thisToken().token == ":":
            endExpr(parser)
            if rang:
                parseError(parser, "unexpected :")
            if lastSize != 0:
                parseError(parser, "unexpected ..")
            if len(arr.nodes) != 1 or arr.nodes[0].type != Types.I32():
                parseError(parser, "expecting single integer size")
            init = True
            arr.init = True
            parser.nextToken()
            continue

        Parser.callToken(parser)
        parser.nextToken()

    endExpr(parser)

    parser.currentNode = arr.owner
    arr.mutable = mutable

    if len(arr.nodes) < 1 :
        #emtpy array
        parser.nextToken()
        typ = parseType(parser)
        arr.type = Array(False, typ)

from .Scope import *
from .VarParser import *

def arrayRead(parser):
    parser.nextToken()
    arr = parser.currentNode.nodes[-1]

    del parser.currentNode.nodes[-1]

    arrRead = Tree.ArrRead(parser)
    arrRead.addNode(arr)

    parser.currentNode.addNode(arrRead)
    parser.currentNode = arrRead

    while parser.thisToken().token != "]":
        Parser.callToken(parser)
        parser.nextToken()

    parser.currentNode = arrRead.owner


Parser.exprToken["["] = arrayLiteral
Parser.exprToken[".."] = lambda parser: Error.parseError(parser, "unexpected ..")