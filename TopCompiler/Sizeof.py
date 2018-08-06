from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
import AST as Tree

def sizeofParser(parser):
    parser.nextToken()

    s = Tree.Sizeof(parser)
    typ = Types.parseType(parser)

    s.typ = typ
    s.type = Types.I32(unsigned= True)
    parser.currentNode.addNode(s)

def castParser(parser):
    if len(parser.currentNode.nodes) == 0:
        Error.parseError(parser, "Unexpected cast")

    parser.nextToken()

    node = Tree.CastToType(parser)
    node.type = Types.parseType(parser)
    node.addNode(parser.currentNode.nodes[-1])
    parser.currentNode.nodes[-1] = node
    node.owner = parser.currentNode


Parser.exprToken["sizeof"] = sizeofParser
Parser.exprToken["cast"] = castParser