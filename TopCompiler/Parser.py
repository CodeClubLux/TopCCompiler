__author__ = 'antonellacalvia'


# recursive imports


def parenOpen(parser):
    parser.paren += 1
    paren = parser.paren

    if not ExprParser.isUnary(parser, parser.lookBehind()):
        FuncParser.callFunc(parser, paren= True)
    else:
        t0 = Tree.Tuple(parser)
        parser.currentNode.addNode(t0)
        parser.currentNode = t0

        while not parser.paren < paren:
            parser.nextToken()
            callToken(parser)
        parser.currentNode = t0.owner

def parenClose(parser):
    parser.paren -= 1

    if parser.paren < 1:
        Error.parseError(parser, "unexpected )")
    layer = -1 if len(parser.bookmark) < 2 else -2
    ExprParser.endExpr(parser, layer= layer)


def newLine(parser):

    parser.lineNumber += 1

    indent = int(parser.lookInfront().token)

    if parser.normalIndent == 0:
        if indent > parser.indent[-1]:
            # indent
            parser.normalIndent = indent / 2
    else:
        diff = indent - parser.indent[-1]
        if diff > 0 and diff % parser.normalIndent != 0:
            Error.parseError(parser, "inconsistent indentation")
        elif diff < 0 and ((-diff) / 2) % parser.normalIndent != 0:
            Error.parseError(parser, "unindent does not match any outer indentation level")

    parser.indentLevel = indent

mapping = {
    "i32": "int",
    "i1": "bool",
    "double": "float",
    "": "none",
    None: "none",
    "void": "none"
}

mappingTo = {
    "i32": "i32",
    "int": "i32",
    "bool": "i1",
    "float": "double",
    "none": ""
}

precidences = {}  # what operator goes first!

exprType = {}  # depends on parser, needs type information to figure out
exprToken = {"\n": newLine, "(": parenOpen, ")": parenClose}  # depends on parser, needs token information
stmts = {}  # for all statements

from .Types import *

from .Lexer import *
import AST as Tree
from .Error import *
from .ExprParser import *
from .VarParser import *
from .ResolveSymbols import *
from .WhileExpr import *
from .Scope import *
from .IfExpr import *
from .PackageParser import *
from .ElseExpr import *
from .FuncParser import *
from .String import *
from .ImportParser import *
import os
from .Array import *
from .MethodParser import *
from .Struct import *
from .TypeInference import *

def isEnd(parser):
    token = parser.thisToken()
    if token.token == "\n" or token.token == ";" or parser.parenBookmark[-1] > parser.paren:
        return maybeEnd(parser)
    return False


def declareOnly(self, noVar=False):
    s1 = selectStmt(self, self.thisToken())
    s2 = selectStmt(self, self.lookInfront())

    declaration = ["var", ":", "(", ")", ",", "\n"]
    if noVar:
        declaration = declaration[1:]

    def declare(token):
        if not (token.token in declaration):
            Error.parseError(self, "unexpected  " + token.token)

    tok = self.thisToken().token

    if self.thisToken().type == "indent":
        pass
    elif s1 != None:
        addBookmark(self)
        declare(self.thisToken())
        s1(self)
        returnBookmark(self)
    elif s2 != None and self.thisToken().token != ")" and self.thisToken().token != "(":
        declare(self.lookInfront())
    else:
        declare(self.thisToken())
        selectExpr(self, self.thisToken())


def maybeEnd(parser):
    if parser.indent[-1] >= parser.indentLevel and parser.paren <= parser.parenBookmark[-1]:
        #parser.iter -= 1
        return True
    return False

class Opcode:
    def __init__(self, parser, opcode, func):
        self.func = func

        self.precidence = precidences[opcode][0] + (parser.paren * 1000)  # 0 is type
        self.right = precidences[opcode][1]  # 1 is if is right-associative
        self.kind = opcode

        def tryIt():
            if len(parser.bookmark) > 1:
                if len(parser.stack) - parser.bookmark[-2] > 0:  # -2 to compensate bookmark, being added by, when calling Opcode
                    same = parser.stack[-1].precidence == self.precidence and parser.stack[-1].right  # right
                    greater = parser.stack[-1].precidence > self.precidence

                    if greater or same:
                        parser.stack.pop().func()
                        tryIt()

        try:
            tryIt()
        except:
            Error.parseError(parser, "Unexpected " + opcode)

        parser.stack.append(self)

        return


def addBookmark(parser):
    parser.bookmark.append(len(parser.stack))
    parser.indent.append(parser.indentLevel)
    parser.parenBookmark.append(parser.paren)


def returnBookmark(parser):
    parser.bookmark.pop()
    parser.indent.pop()
    parser.parenBookmark.pop()


def selectExpr(parser, token):
    addBookmark(parser)

    type = token.type
    tok = token.token

    if tok in exprToken:
        exprToken[tok](parser)
    elif type in exprType:
        exprType[type](parser, tok)

    returnBookmark(parser)

def selectStmt(parser, token):
    if token.token in stmts:
        return stmts[token.token]


def callToken(self):
    s1 = selectStmt(self, self.thisToken())

    b = self.thisToken()

    iter = self.iter
    if s1 != None:
        addBookmark(self)
        s1(self)
        returnBookmark(self)
    else:
        if (b.token == "_" or not b.type in ["symbol", "operator", "indent"]) and not ExprParser.isUnary(self, self.lookBehind()):
            addBookmark(self)
            FuncParser.callFunc(self, False)
            returnBookmark(self)
            return

        selectExpr(self, b)

class Func:
    def __init__(self, args, returnType):
        self.args = args
        self.returnType = returnType

class Parser:  # all mutable state
    def nextToken(parser):
        parser.iter += 1
        try:
            t = parser.thisToken()
            if t.token == "," and parser.lookBehind().token == ",":
                Error.parseError(parser, "unexpected ,")
            return t
        except IndexError:
            parser.iter -= 1
            if parser.paren > 1:
                Error.parseError(parser, "unmatched (")
            Error.parseError(parser, "EOF")

    def lookBehind(parser):
        return parser.tokens[parser.iter - 1]

    def lookInfront(parser):
        try:
            return parser.tokens[parser.iter + 1]
        except:
            if parser.paren != 1:
                Error.parseError(parser, "unmatched (")
            Error.parseError(parser, "EOF")

    def thisToken(parser):
        return parser.tokens[parser.iter]

    def __init__(self, tokens, filename):
        self.paren = 1  # must be atleast 1, otherwise multiplication = 0
        self.parenBookmark = []
        self.indentLevel = 0

        self.lineNumber = 1
        self.stack = []

        self.indent = []
        self.normalIndent = 0

        self.bookmark = [0]

        Stringable = Types.Interface(False, {"toString": Types.FuncPointer([], Types.String(0) )})

        self.scope = {"_global": [{
            "alert": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null())),
            "log": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null())),
            "newString": Scope.Type(True, Types.FuncPointer([Stringable], Types.String(0))),
            "println": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null())),
            "print": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null()))
        }]}

        self.iter = 0

        self.package = "_global"
        self.opackage = ""
        self.imports = []

        self.rootAst = Tree.Root()
        self.currentNode = self.rootAst

        self.allImports = {}

        self.filename = ""
        self.tokens = [None]

        self.structs = {"_global": {}}

        self.func = {"_global": {}}

        types = {
            "int": Types.I32(),
            "vector": Types.Array(False, Types.I32()),
            "float": Types.Float(),
            "string": Types.String(0)
        }

        for name in self.structs["_global"]:
            i = self.structs["_global"][name]
            i.addMethod(self, "toString", Types.FuncPointer([types[name]], Types.String(0)))

        self.interfaces = {
            "_global": {
                "Stringable": Stringable
            }
        }

        self.filename = filename
        self.tokens = tokens

    def parse(self):
        tokens = self.tokens
        filenames = self.filename

        for i in range(len(tokens)):
            PackageParser.packDec(self, filenames[i][0])
            self._parse(tokens[i], filenames[i][1])
            self.imports = []

        self.tokens = tokens
        self.filename = filenames

        infer(self, self.currentNode)
        validate(self, self.currentNode)


        return self.currentNode

    def _parse(self, tokens, filename):
        self.tokens = tokens
        self.filename = filename

        self.iter = 0
        while self.iter < len(tokens) - 1:
            callToken(self)
            self.nextToken()

        return self.currentNode
