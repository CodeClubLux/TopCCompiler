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
    (name, names, types, header, returnType) = FuncParser.funcHead(parser, True)
    Scope.decrScope(parser)

def resolve(self):

    tokens = self.tokens
    filenames = self.filename

    for c in filenames:
        for i in range(len(tokens[c])):
            self.allImports[filenames[c][i][0]] = []
            PackageParser.packDec(self, os.path.basename(filenames[c][i][0]), pack= True)
            _resolve(self, tokens[c][i], filenames[c][i][1], passN=0)

    for n in range(1,3):
        for c in filenames:
            for i in range(len(tokens[c])):
                PackageParser.packDec(self, os.path.basename(filenames[c][i][0]))
                _resolve(self, tokens[c][i], filenames[c][i][1], passN=n)

    self.rootAst = Tree.Root()
    self.currentNode = self.rootAst

    self.tokens = tokens
    self.filename = filenames

    return self


def _resolve(self, tokens, filename, passN= 0 ):
    self.filename = filename
    self.iter = 0

    self.tokens = tokens

    while self.iter < len(tokens) - 1 :
        b = self.thisToken().token

        if passN == 2:
            if b == "import":
                ImportParser.importParser(self, True)
            elif b == "def" and self.indent == 0:
                Parser.addBookmark(self)
                funcHead(self)
                Parser.returnBookmark(self)
        elif passN == 1:
            if b == "import":
                ImportParser.importParser(self, True)

            elif b == "type":
                Parser.addBookmark(self)
                Struct.typeParser(self, decl= True)
                Parser.returnBookmark(self)

        elif passN == 0:
            if b == "type":
                Scope.addVar(Tree.Node(self), self, self.nextToken().token, Scope.Type(True, Types.StructInit(self.thisToken().token)))

                self.structs[self.package][self.thisToken().token] = Struct.Struct(self.thisToken().token, [],[], {})
                self.structs[self.package][self.thisToken().token].methods = {}

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

def insert(parser, p, only= False):
    if not only:
        p.files = parser.files
        p.filenames = parser.filenames
        p.lexed = parser.lexed

    p.scope = parser.scope
    p.structs = parser.structs
    p.interfaces = parser.interfaces
    p.func = parser.func
    p.allImports = parser.allImports
    p.compiled = parser.compiled
    p.opt = parser.opt
    p.externFuncs = parser.externFuncs

