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
        print(type(node.nodes[0]))
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



Parser.stmts["#addToContext"] = addToContext