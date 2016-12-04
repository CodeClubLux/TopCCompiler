__author__ = 'antonellacalvia'

from .Parser import *
from .Types import *
import AST as Tree
from .ExprParser import *
from .Error import *

def arrayLiteral(parser):
    numB = parser.bracket
    parser.bracket += 1

    if not isUnary(parser, parser.lookBehind()):
        return arrayRead(parser)

    parser.nextToken()

    lastSize = 0
    typ = None

    arr = Tree.Array(parser)
    parser.currentNode.addNode(arr)
    parser.currentNode = arr

    parser.nodeBookmark.append(0)

    rang = False
    init = False

    while parser.thisToken().token != "]" :
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
            parser.nodeBookmark[-1] = len(parser.currentNode.nodes)
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

        if parser.thisToken().token == "]" and parser.bracket <= numB:
            break

        parser.nextToken()
    else:
        closeBracket(parser)

    endExpr(parser)

    parser.currentNode = arr.owner
    arr.mutable = False

    if len(arr.nodes) < 1 :
        #emtpy array
        parser.nextToken()
        typ = parseType(parser)
        arr.type = Array(False, typ)

    if arr.range:
        if len(arr.nodes) != 2:
            Error.parseError(parser, "unexpected ]")

    parser.nodeBookmark.pop()

from .Scope import *
from .VarParser import *

def arrayRead(parser):
    parser.nextToken()
    parser.nodeBookmark.append(1)
    try:
        arr = parser.currentNode.nodes[-1]
    except IndexError:
        print(parser.tokens[parser.iter-2])
        Error.parseError(parser, "unexpected array read")

    del parser.currentNode.nodes[-1]

    arrRead = Tree.ArrRead(parser)
    arrRead.addNode(arr)

    parser.currentNode.addNode(arrRead)
    parser.currentNode = arrRead

    while parser.thisToken().token != "]":
        Parser.callToken(parser)

        if parser.thisToken().token == "]":
            break

        parser.nextToken()
    else:
        closeBracket(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = arrRead.owner
    parser.nodeBookmark.pop()

def closeBracket(parser):
    parser.bracket -= 1

    if parser.bracket < 0:
        Error.parseError(parser, "unexpected ], found no matching [")


Parser.exprToken["["] = arrayLiteral
Parser.exprToken["]"] = closeBracket
Parser.exprToken[".."] = lambda parser: Error.parseError(parser, "unexpected ..")