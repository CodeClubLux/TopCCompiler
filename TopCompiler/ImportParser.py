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

        if name in parser.shouldCompile:
            return parser.shouldCompile[name]

        for i in parser.allImports[name]:
            if shouldCompile(decl, i, parser, mutated):
                parser.shouldCompile[name] = True
                return True

        res = topc.modified(parser.files[name], name, jsFiles= parser.jsFiles)
        parser.shouldCompile[name] = res

        return res

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

        if not parser.hotswap:
            sp = shouldParse(decl, oname, parser)
        else:
            sp = shouldCompile(decl, oname, parser)

        if sp:
            p = Parser.Parser(parser.lexed[oname], parser.filenames[oname])

            ResolveSymbols.insert(parser, p)

            sc = shouldCompile(decl, oname, parser)

            p.sc = sc

            parser.compiled[name] = None
            parser.externFuncs[name] = []

            parsed = p.parse()

            declar = parser.externFuncs[name]

            parser.compiled[name] = (sc, (parsed, declar))

            ResolveSymbols.insert(p, parser)

            parser.currentNode.addNode(Tree.InitPack(name, parser))
        else:
            if not name in parser.compiled:
                parser.compiled[name] = (False,)
                parser.currentNode.addNode(Tree.InitPack(name, parser))

    parser.imports.append(oname)


Parser.stmts["import"] = importParser