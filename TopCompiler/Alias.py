from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import Struct
from TopCompiler import FuncParser
import collections as coll

def aliasParser(parser, name, decl, generic):
    parser.nextToken()

    typ = False
    while not Parser.isEnd(parser):
        if parser.thisToken().token != "\n" and parser.thisToken().type != "indent":
            if typ:
                Error.parseError(parser, "Unexpected token " + parser.thisToken().token)
            typ = Types.parseType(parser)
        parser.nextToken()

    alias = Types.Alias(parser.package, name, typ, generic)

    if decl:
        del parser.structs[parser.package][name]# = Struct.Struct(name, args, fields, coll.OrderedDict())

        parser.interfaces[parser.package][name] = alias

    Scope.decrScope(parser)