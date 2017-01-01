from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import Struct
from TopCompiler import FuncParser
import AST as Tree
import collections as coll

def enumParser(parser, name, decl, generic):
    const = coll.OrderedDict()
    enum = Types.Enum(parser.package, name, const, generic)

    if decl:
        del parser.structs[parser.package][name]# = Struct.Struct(name, args, fields, coll.OrderedDict())
        parser.interfaces[parser.package][name] = enum

    """if parser.lookInfront().token == "\n":
        parser.nextToken()
        Parser.callToken(parser)
        parser.nextToken()"" \
    """

    while not Parser.isEnd(parser):
        t = parser.nextToken()

        if t.token == "\n" or t.type == "indent":
            Parser.callToken(parser)
            continue


        if t.type != "identifier":
            Error.parseError(parser, "expecting identifier")

        varName = t.token

        if varName[0].upper() != varName[0]:
            Error.parseError(parser, "constructor type must be capitalized")

        args = []
        nextT = parser.nextToken()
        #print(varName)
        #print(nextT)
        if nextT.token == "(":
            args = Types.parseType(parser).list

        const[varName] = args

        if decl:
            Scope.addVar(Tree.PlaceHolder(parser), parser, varName, Scope.Type(True,
                Types.FuncPointer(args, enum, generic = generic)
            ), _global=True)

        t = parser.thisToken()
        if t.token == "\n" or t.type == "indent":
            Parser.callToken(parser)

    parser.currentNode.addNode(Tree.Enum(const, parser))

    Scope.decrScope(parser)