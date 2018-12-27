__author__ = 'antonellacalvia'

from TopCompiler import FuncParser
from TopCompiler import Error
from TopCompiler import Parser
from TopCompiler import Scope
import AST as Tree
from TopCompiler import VarParser
from TopCompiler import FuncParser
from TopCompiler import Struct
from TopCompiler import Types
from TopCompiler import PackageParser
from TopCompiler import ImportParser
from TopCompiler import MethodParser
import os

def funcHead(parser):
    (name, names, types, header, returnType, do) = FuncParser.funcHead(parser, True)
    Scope.decrScope(parser)

from time import time

def resolve(self):
    tokens = self.tokens
    filenames = self.filename

    for c in filenames:
        self._filename = self.filenames[c]
        if not self.hotswap or ImportParser.shouldCompile(False, c, self):
            if c in self.contextFields:
                for i in self.contextFields[c]:
                    del self.contextType[i]

            PackageParser.packDec(self, c, pack=True)
            if self.package != "_global":
                self.scope[self.package] = [{}]
                self.structs[self.package] = {}
                self.interfaces[self.package] = {}

        if not c in self.allImports:
            self.allImports[c] = []

        for i in range(len(tokens[c])):
            _resolve(self, tokens[c][i], self._filename[i][1], passN=0)

    for n in range(1,3):
        start = time()
        for c in filenames:
            self._filename = self.filenames[c]
            if len(filenames[c]) == 0:
                continue

            self.package = c
            self.opackage = c

            for i in range(len(tokens[c])):
                if self.package == "_global" and i == len(tokens[c])-1:
                    self.setArrayTypes()
                _resolve(self, tokens[c][i], self._filename[i][1], passN=n)

    self.rootAst = Tree.Root()
    self.currentNode = self.rootAst

    self.tokens = tokens
    self.filename = filenames

    return self

from TopCompiler import ImportParser
import collections as coll

def _resolve(self, tokens, filename, passN= 0 ):
    target = self.global_target
    if self.package != "main":
        self.global_target = "full"

    if self.hotswap and not ImportParser.shouldCompile(False, self.package, self):
        return

    self.filename = filename
    self.iter = 0

    self.tokens = tokens

    while self.iter < len(tokens) - 1 :
        b = self.thisToken().token

        if passN == 2:
            if b == "import":
                ImportParser.importParser(self, True)
            elif b == "from":
                ImportParser.fromParser(self, True)
            elif b == "def" :
                if self.indentLevel == 0:
                    nex = self.lookInfront()

                    Parser.addBookmark(self)
                    funcHead(self)
                    Parser.returnBookmark(self)
        elif passN == 1:
            if b == "import":
                ImportParser.importParser(self, True)
            elif b == "from":
                ImportParser.fromParser(self, True)
            elif b == "type":
                Parser.addBookmark(self)
                Struct.typeParser(self, decl= True)
                Parser.returnBookmark(self)

        elif passN == 0:
            if b == "type":
                name = self.nextToken().token
                if name == "ext":
                    name = self.nextToken().token

                ofType = None
                gen = {}

                if self.nextToken().token == "[":
                    Scope.incrScope(self)
                    gen = FuncParser.generics(self, name)
                    Scope.decrScope(self)
                    ofType = self.thisToken().token
                else:
                    ofType = self.thisToken().token

                Scope.addVar(Tree.Node(self), self, name,
                             Scope.Type(True, Types.StructInit(name)))

                if ofType is None or ofType == "=":
                    #"""
                    self.structs[self.package][name] = Struct.Struct(name, [],[], gen, self, self.package)
                    self.structs[self.package][name].methods = {}
                    #"""
                elif ofType == "either":
                    self.interfaces[self.package][name] = Types.Enum(self.package, name, coll.OrderedDict(), gen)
                elif ofType == "with":
                    self.interfaces[self.package][name] = Types.Interface(False, {}, name=self.package+"."+name)
                elif ofType == "is":
                    self.interfaces[self.package][name] = Types.Alias(self.package, name, Types.Null(), gen)

        if b == "\n":
            Parser.addBookmark(self)
            Parser.newLine(self)
            Parser.returnBookmark(self)

        self.nextToken()

    for i in self.imports:
        if not i in self.allImports[self.package]:
            self.allImports[self.package].append(i)

    self.imports = []

    self.lineNumber = 1
    self.normalIndent = 0

    self.global_target = target

import copy as _copy

def insert(parser, p, only= False, copy= False):
    if not only:
        p.files = parser.files
        p.filenames = parser.filenames
        p.lexed = parser.lexed
        p.opt = parser.opt

    if copy:
        scope = {}
        interfaces = {}
        structs = {}
        contextFields = {}
        for package in parser.scope:
            scope[package] = [_copy.copy(parser.scope[package][0])]
            interfaces[package] = _copy.copy(parser.interfaces[package])
            structs[package] = _copy.copy(parser.structs[package])
            contextFields[package] = _copy.copy(parser.contextFields[package])

        p.scope = scope
        p.interfaces = interfaces
        p.structs = structs
        p.contextFields = contextFields
        p.contextType = parser.contextType
    else:
        p.scope = parser.scope
        p.structs = parser.structs
        p.interfaces = parser.interfaces
        p.contextFields = parser.contextFields
        p.contextType = parser.contextType

    #p.func = parser.func
    p.allImports = parser.allImports
    p.compiled = parser.compiled
    #p.externFuncs = parser.externFuncs
    p.hotswap = parser.hotswap
    p.global_target = parser.global_target
    p.shouldCompile = parser.shouldCompile
    p.atoms = parser.atoms
    p.atomTyp = parser.atomTyp
    p.outputFile = parser.outputFile
    p.transforms = parser.transforms
    p.output_target = parser.output_target
    p.usedModules = parser.usedModules
    p.specifications  = parser.specifications
    p.path = parser.path
    p.order_of_modules = parser.order_of_modules
    p.linkWith = parser.linkWith
    p.contextFields = parser.contextFields
    p.contextType = parser.contextType
    p.compiledTypes = parser.compiledTypes
    p.includes = parser.includes

    return p

