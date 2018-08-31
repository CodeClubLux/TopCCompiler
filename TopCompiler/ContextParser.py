from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
import AST as Tree

from TopCompiler import ExprParser

def addToContext(parser):
    previous = parser.currentNode
    node = Tree.AddToContext(parser)
    parser.currentNode = node

    if not type(previous) is Tree.Root:
        Error.parseError(parser, "Can only add field to context from global scope")

    if parser.nextToken().type != "identifier":
        Error.parseError(parser, "Expecting identifier")

    Parser.callToken(parser)
    parser.nextToken()
    iter = parser.iter+1
    line = parser.lineNumber
    Parser.callToken(parser)

    if not type(node.nodes[0]) is Tree.CreateAssign:
        parser.iter = iter
        parser.lineNumber = line
        Error.parseError(parser, "Expecting :=")

    createAssign = node.nodes[0]
    node.name = createAssign.nodes[0].name

    parser.currentNode = previous
    previous.addNode(node)

def typecheckAddToContext(parser, i):
    name = i.nodes[0].nodes[0].name
    typ = i.nodes[0].nodes[0].varType

    if name in parser.contextType:
        i.error("Context already has field "+name)
    parser.contextType[name] = typ
    parser.contextFields[parser.package][name] = typ

def pushContext(parser):
    parser.nextToken()

    node = Tree.PushContext(parser)
    previous = parser.currentNode
    previous.addNode(node)
    parser.currentNode = node

    Parser.callToken(parser)

    if len(node.nodes) == 0 or not type(node.nodes[0]) is Tree.ReadVar:
        Error.parseError(parser, "Expecting identifier")

    if parser.nextToken().token != "do":
        Error.parseError(parser, "Expecting do")

    while not Parser.isEnd(parser) or parser.thisToken().token == "do":
        parser.nextToken()
        Parser.callToken(parser)

    parser.currentNode = previous

def defer(parser):
    node = Tree.Defer(parser)
    previos = parser.currentNode
    previos.addNode(node)
    parser.currentNode = node

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.callToken(parser)

    if len(node.nodes) != 1:
        Error.parseError(parser, "Expecting single expression, not "+str(len(node.nodes)))

    if not type(node.nodes[0]) is Tree.FuncCall:
        Error.parseError(parser, "Expecting function call")

    parser.currentNode = previos



def typecheckPushContext(parser, i):
    contextTyp = parser.structs["_global"]["Context"]
    contextTyp = Types.Struct(False, "Context", contextTyp._types, "_global")

    contextTyp.duckType(parser,  i.nodes[0].type, i.nodes[0], i.nodes[0], 0)
    Tree.insertCast(i.nodes[0], i.nodes[0].type, contextTyp, 0)

Parser.stmts["#addToContext"] = addToContext
Parser.stmts["#pushContext"] = pushContext
Parser.stmts["defer"] = defer