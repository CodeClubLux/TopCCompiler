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

def offsetof(parser):
    parser.nextToken()

    s = Tree.Offsetof(parser)
    typ = Types.parseType(parser)
    if parser.nextToken().token != ",":
        Error.parseError(parser, "Expecting comma")

    field = parser.nextToken()
    if field.type != "identifier":
        Error.parseError(parser, "Expecting identifier, not " + field.type)

    if not field.token in typ.types:
        Error.parseError(parser, str(typ) + " does not have the field " + field.token)

    if type(typ) is Types.Array and typ.both and field.token == "length":
        Error.parseError(parser, "Cannot get offsetof parameter length on static array")

    s.typ = typ
    s.field = field.token
    s.type = Types.I32(unsigned=True)
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

def typeofParser(parser):
    parser.nextToken()

    typ = Types.parseType(parser)
    node = Tree.Typeof(parser, typ)
    parser.currentNode.addNode(node)

Parser.exprToken["sizeof"] = sizeofParser
Parser.exprToken["offsetof"] = offsetof
Parser.exprToken["cast"] = castParser
Parser.exprToken["get_type"] = typeofParser