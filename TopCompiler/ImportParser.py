__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import topc
from TopCompiler import ResolveSymbols
import AST as Tree
from TopCompiler import Types

def shouldCompile(decl, name, parser, mutated= ()):
    if not decl and not name in parser.compiled and not name in mutated:
        mutated += (name,)

        for i in parser.allImports[name]:
            if shouldCompile(decl, i, parser, mutated):
                return True

        return topc.modified(parser.files[name], name)
    return False

def shouldParse(decl, name, parser):
    return not decl and not name in parser.compiled


def importParser(parser, decl= False):
    import os
    name = parser.nextToken()
    if name.type != "str":
        Error.parseError(parser, "expecting string")

    oname = name.token[1:-1]

    if not oname in parser.filenames:
        Error.parseError(parser, "package "+oname+" not found")

    name = os.path.basename(oname)

    if not decl:
        parser.externFuncs[parser.package] = []

        if shouldParse(decl, oname, parser):
            p = Parser.Parser(parser.lexed[oname], parser.filenames[oname])

            ResolveSymbols.insert(parser, p)

            sc = shouldCompile(decl, oname, parser)

            parser.compiled[name] = None
            parser.externFuncs[name] = []

            if sc:
                parsed = p.parse()
            else:
                parsed = None

            declar = parser.externFuncs[name]

            parser.compiled[name] = (sc, (parsed, declar))

            ResolveSymbols.insert(p, parser)

            parser.currentNode.addNode(Tree.InitPack(name, parser))
        else:
            if not name in parser.compiled:
                parser.compiled[name] = None

    parser.imports.append(oname)


Parser.stmts["import"] = importParser