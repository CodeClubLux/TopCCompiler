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

    if decl:
        alias = parser.interfaces[parser.package][name]

        tmp = Types.Alias(parser.package, name, typ, generic)
        alias.name = tmp.name
        alias.normalName = tmp.normalName
        alias.typ = tmp.typ
        alias.generic = tmp.generic
        alias.remainingGen = tmp.remainingGen
        alias.types = tmp.types
        alias.methods = tmp.methods
    if decl:
        parser.interfaces[parser.package][name] = alias

    Scope.decrScope(parser)