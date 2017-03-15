__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import topc
from TopCompiler import ResolveSymbols
from TopCompiler import VarParser
from TopCompiler import Scope
from TopCompiler import Lexer

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
        #parser.externFuncs[parser.package] = []

        if not parser.hotswap:
            sp = shouldParse(decl, oname, parser)
        else:
            sp = shouldCompile(decl, oname, parser)

        if sp:
            p = Parser.Parser(parser.lexed[oname], parser.filenames[oname])
            p.package = oname

            ResolveSymbols.insert(parser, p)

            sc = shouldCompile(decl, oname, parser)

            p.sc = sc

            parser.compiled[name] = None
            #parser.externFuncs[name] = []

            parsed = p.parse()

            declar = [] #parser.externFuncs[name]

            parser.compiled[name] = (sc, (parsed, declar))

            ResolveSymbols.insert(p, parser)

            parser.currentNode.addNode(Tree.InitPack(name, parser))
        else:
            if not name in parser.compiled:
                parser.compiled[name] = (False,)
                parser.currentNode.addNode(Tree.InitPack(name, parser))

    parser.imports.append(oname)

def fromParser(parser, decl= False, stage=False):
    importParser(parser, decl)
    name = parser.imports[-1]

    if parser.nextToken().token != "import":
        Error.parseError(parser, "Expecting import keyword")

    parser.nextToken()

    names = []
    if not decl:
        parser.currentNode.addNode(Tree.Import(name, parser.package, names, parser))

    def getName(token, nameOfVar=""):
        if nameOfVar == "":
            nameOfVar = token.token
        package = parser.package

        if nameOfVar in parser.structs[name]:
            if not decl: return

            if stage and nameOfVar in parser.structs[package]:
                Error.parseError(parser, nameOfVar + " is already a struct")
            parser.structs[package][nameOfVar] = parser.structs[name][nameOfVar]
            names.append((nameOfVar, parser.global_target))
        elif nameOfVar in parser.interfaces[name]:
            if not decl: return

            if stage and nameOfVar in parser.interfaces[package]:
                Error.parseError(parser, nameOfVar + " is already an interface")
            parser.interfaces[package][nameOfVar] = parser.interfaces[name][nameOfVar]
        elif not decl and nameOfVar in parser.scope[name][0]:
            token.error = lambda msg: Error.parseError(parser, msg)
            Scope.addVar(token, parser, nameOfVar, parser.scope[name][0][nameOfVar])
            names.append((nameOfVar, parser.scope[name][0][nameOfVar].target))
        elif not decl:
            Error.parseError(parser, "Package " + name + " does not have a variable, or type called " + nameOfVar)

    token = parser.thisToken()

    Parser.callToken(parser)
    elem = parser.currentNode.nodes.pop()

    def pattern(name):
        if type(name) in [Tree.Tuple, Tree.PlaceHolder]:
            for i in name:
                pattern(i)
        elif type(name) is Tree.ReadVar:
            return getName(name.token)
        elif type(name) is Lexer.Token and name.type == "identifier":
            return getName(name)
        else:
            p = Tree.PlaceHolder(parser)
            p.token = name
            p.error("Unexpected token " + name.token)

    pattern(elem)

Parser.stmts["import"] = importParser
Parser.stmts["from"] = fromParser