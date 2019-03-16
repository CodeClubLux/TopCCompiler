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
import os

ignore = {}

def shouldCompile(decl, name, parser, mutated= (), dependency=False):
    return not name in parser.compiled
    #print(parser.alwaysRecompile)

    if not dependency and name in parser.alwaysRecompile and not decl:
        if name in parser.compiled:
            return not parser.compiled[name][0]

        return True

    if not decl and not name in parser.compiled and not name in mutated:


        mutated += (name,)

        if name in ignore:
            return False

        if name in parser.shouldCompile:
            return parser.shouldCompile[name]

        if not name in parser.allImports:
            return True

        for i in parser.allImports[name]:
            if shouldCompile(decl, i, parser, mutated, dependency=True):
                parser.shouldCompile[name] = True
                return True

        if name in topc.global_parser.files:
            res = topc.modified(parser.output_target, parser.files[name], name)
        else:
            res = False
        parser.shouldCompile[name] = res

        return res

    try:
        t = os.path.getmtime("lib/" + name.replace("/", ".") + ".c")
        t = datetime.datetime.fromtimestamp(int(t))
    except FileNotFoundError:
        sp = True

    return False

import datetime

def shouldParse(decl, name, parser):
    return not decl and not name in parser.compiled

def importParser(parser, decl= False):
    import os
    name = parser.nextToken()

    if name.type != "str":
        Error.parseError(parser, "expecting string")

    oname = name.token[1:-1]

    if not oname in parser.filenames and not oname in ignore:
        Error.parseError(parser, "package "+oname+" not found")

    name = os.path.basename(oname)


    if not decl:
        if not parser.hotswap:
            sp = shouldParse(decl, oname, parser)
        else:
            sp = shouldCompile(decl, oname, parser)

            outputfile = oname
                #print("Error ", outputfile)

        if sp:
            p = Parser.Parser(parser.lexed[oname], parser.filenames[oname])
            p.package = oname

            ResolveSymbols.insert(parser, p)

            global_target = parser.global_target

            p.global_target = "full"

            sc = shouldCompile(decl, oname, parser)


            p.sc = sc

            parser.compiled[name] = None
            #parser.externFuncs[name] = []

            parsed = p.parse()

            declar = [] #parser.externFuncs[name]

            parser.compiled[name] = (sc, (parsed, declar))

            ResolveSymbols.insert(p, parser)

            parser.global_target = global_target
            parser.currentNode.addNode(Tree.InitPack(name, parser))

        else:
            if not name in parser.compiled:
                def loop(name):
                    #if name in parser.alwaysRecompile:
                    parser.compiled[name] = (False,)
                    #return

                    parser.currentNode.addNode(Tree.InitPack(name, parser))

                    #print("not recompiling", name)
                    #print(parser.allImports[name])

                    for imports in parser.allImports[name]:
                        if not imports in parser.compiled:
                            parser.compiled[imports] = (False,)
                            #parser.compiled[imports] = (False,) #Assumption is correct as package has to be recompiled when it's dependencies change
                            parser.currentNode.addNode(Tree.InitPack(imports, parser))

                            loop(imports)
                            if not imports in parser.order_of_modules:
                                parser.order_of_modules.append(imports)

                    if not name in parser.order_of_modules:
                        parser.order_of_modules.append(name)

                loop(name)

    parser.imports.append(oname)

from TopCompiler import Struct

def fromParser(parser, decl= False, stage=False):
    place = Tree.PlaceHolder(parser)

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
            if decl:
                if stage and nameOfVar in parser.structs[package]:
                    Error.parseError(parser, nameOfVar + " is already a struct")
                parser.structs[package][nameOfVar] = parser.structs[name][nameOfVar]
            else:
                Scope.addVar(place, parser, nameOfVar, parser.scope[name][0][nameOfVar])

            names.append((nameOfVar, "full"))
        elif nameOfVar in parser.interfaces[name]:
            if not decl: return

            if stage and nameOfVar in parser.interfaces[package]:
                Error.parseError(parser, nameOfVar + " is already an interface")
            parser.interfaces[package][nameOfVar] = parser.interfaces[name][nameOfVar]
        elif not decl and nameOfVar in parser.scope[name][0]:
             #can't set lambda
            Scope.addAlias(place, package, name, nameOfVar, nameOfVar, parser)

            #Scope.addVar(place, parser, nameOfVar, parser.scope[name][0][nameOfVar])
            names.append((nameOfVar, ""))
        elif not decl:
            Error.parseError(parser, "Package " + name + " does not have a variable, or type called " + nameOfVar)

    token = parser.thisToken()

    if token.token == "all":
        _names = set()
        for i in parser.structs[name]:
            s = parser.structs[name][i]
            if s.package != name:
                continue

            _names.add(i)

        for i in parser.interfaces[name]:
            s = parser.interfaces[name][i]
            if s.package != name:
                continue
            _names.add(i)

        for i in parser.scope[name][0]:
            scope_typ = parser.scope[name][0][i]
            if not type(scope_typ) is Scope.Alias:
                if not (type(scope_typ.type) is Struct.Struct and scope_typ.type.package != name):
                    _names.add(i)

        for i in _names:
            getName(token, i)
        return

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