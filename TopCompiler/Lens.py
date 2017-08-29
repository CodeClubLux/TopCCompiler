
import AST as Tree

from TopCompiler import Types
from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import VarParser
from TopCompiler import Scope
from TopCompiler import ExprParser
import collections as coll

def parseLens(parser):
    #parser.nextToken()
    Scope.incrScope(parser)
    #lensType = Types.parseType(parser)
    Scope.decrScope(parser)

    place = Tree.Place(parser)

    lens = Tree.Lens(parser)
    lens.place = place

    parser.currentNode.addNode(lens)

    parser.currentNode = lens

    lens.addNode(place)

    #parser.nextToken()

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = lens.owner

    B = Types.T("B", Types.All, "Lens")

    def loop(n):
        if type(n) in [Tree.PlaceHolder, Tree.Place]:
            return B
        elif type(n) is Tree.Field:
            inner = loop(n.nodes[0])
            return Types.Interface(False, {
                n.field: inner
            })
        elif type(n) is Tree.ArrRead:
            inner = loop(n.nodes[0])
            return Types.Array(False,inner)
        else:
            n.error("unexpected token "+n.token.token)

    lens_typ = loop(lens.nodes[0])

    A = Types.T("A", lens_typ, "Lens")

    self = Types.Interface(False, {
        "query": Types.FuncPointer([A], B),
        "set": Types.FuncPointer([A, B], A),
        "toString": Types.FuncPointer([], Types.String(0)),
    }, coll.OrderedDict([("Lens.A", A), ("Lens.B", B)]), name="Lens")

    Lens = Types.Interface(False, {
        "query": Types.FuncPointer([A], B),
        "set": Types.FuncPointer([A, B], A),
        "toString": Types.FuncPointer([], Types.String(0)),
    }, coll.OrderedDict([("Lens.A", A), ("Lens.B", B)]), name="Lens")

    #lens.type = Types.Interface(False, {
    #    #   "query": Types.FuncPointer([i.lensType], i.nodes[0].type),
    #    "set": Types.FuncPointer([i.lensType, i.nodes[0].type], i.lensType),
    #})

    lens.type = Lens

Parser.exprToken["lens"] = parseLens