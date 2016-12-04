__author__ = 'antonellacalvia'


# recursive imports


def parenOpen(parser):
    parser.paren += 1
    paren = parser.paren

    """
    if not ExprParser.isUnary(parser, parser.lookBehind()):
        FuncParser.callFunc(parser, paren= True)
    """

    if True:
        t0 = Tree.Tuple(parser)
        parser.currentNode.addNode(t0)
        parser.currentNode = t0

        parser.nodeBookmark.append(0)

        while not parser.paren < paren:
            parser.nextToken()
            callToken(parser)

        parser.nodeBookmark.pop()
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
from .Lens import *
import os
from .ExternParser import *
from .Array import *
from .MethodParser import *
from .Struct import *
from .TypeInference import *

def isEnd(parser):
    token = parser.thisToken()

    if token.token in ["!", "\n", ";"] or parser.parenBookmark[-1] > parser.paren or parser.bracketBookmark[-1] > parser.bracket:
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
    if parser.indent[-1] >= parser.indentLevel and parser.paren <= parser.parenBookmark[-1] and parser.bracket <= parser.bracketBookmark[-1]:
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
    parser.bracketBookmark.append(parser.bracket)

def returnBookmark(parser):
    parser.bookmark.pop()
    parser.indent.pop()
    parser.parenBookmark.pop()
    parser.bracketBookmark.pop()

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
        if (b.token in ["!", "_", "(", "\\", "!>"] or not b.type in ["symbol", "operator", "indent", "keyword"]) and not ExprParser.isUnary(self, self.lookBehind()):
            if b.token == "!>":
                print("weird symbol thing")
                ExprParser.endExpr(self, -2)
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
        self.bracket = 0
        self.parenBookmark = [[]]
        self.bracketBookmark = [0]
        self.indentLevel = 0

        self.lineNumber = 1
        self.stack = []

        self.nodeBookmark = [0]

        self.indent = []
        self.normalIndent = 0

        self.bookmark = [0]

        self.sc = True

        Stringable = Types.Interface(False, {"toString": Types.FuncPointer([], Types.String(0) )})
        Lengthable = Types.Interface(False, {"length": Types.I32()})
        Intable = Types.Interface(False, {"toInt": Types.FuncPointer([], Types.I32() )})
        Floatable = Types.Interface(False, {"toFloat": Types.FuncPointer([], Types.Float())})

        T = Types.T("T", All, "Atom")

        Atom = Types.Interface(False, {
            "unary_read": FuncPointer([], T, do= True),
            "operator_set": FuncPointer([T], Null(), do= True),
            "watch": FuncPointer([FuncPointer([T], Types.Null(), do= True)], Types.Null(), do= True)
        }, coll.OrderedDict([("Atom.T", T)]))

        A = Types.T("A", All, "Lens")
        B = Types.T("B", All, "Lens")

        Lens = Types.Interface(False, {
            "query": Types.FuncPointer([A], B),
            "set": Types.FuncPointer([A, B], A),
        }, coll.OrderedDict([("Lens.A", A), ("Lens.B", B)]))

        defer_T = Types.T("T", All, "defer")
        defer_X = Types.T("X", All, "defer")

        defer = Types.FuncPointer([Types.FuncPointer(
            [defer_T], defer_X, do= True)], Types.FuncPointer([defer_T], Types.FuncPointer([], defer_X, do= True))
        , generic= coll.OrderedDict([("defer.T", defer_T), ("defer.X", defer_X)]))

        parallel_T = Types.T("T", All, "parallel_T")

        parallel = Types.FuncPointer([Types.Array(False,
            Types.FuncPointer([], parallel_T, do=True)
        )], Types.Array(False, parallel_T), do= True, generic=coll.OrderedDict([("parallel.T", parallel_T)]))

        serial_T = Types.T("T", All, "parallel_T")

        serial = Types.FuncPointer([Types.Array(False,
            Types.FuncPointer([], serial_T, do=True)
        )], Types.Array(False, serial_T), do=True, generic=coll.OrderedDict([("serial.T", serial_T)]))

        self.scope = {"_global": [{
            "alert": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null(), do= True)),
            "log": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null(), do= True)),
            "toString": Scope.Type(True, Types.FuncPointer([Stringable], Types.String(0))),
            "println": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null(), do= True)),
            "print": Scope.Type(True, Types.FuncPointer([Stringable], Types.Null(), do= True)),
            "isEven": Scope.Type(True, Types.FuncPointer([Types.I32()], Types.Bool)),
            "isOdd": Scope.Type(True, Types.FuncPointer([Types.I32()], Types.Bool)),
            "len": Scope.Type(True, Types.FuncPointer([Lengthable], Types.I32())),
            "toInt": Scope.Type(True, Types.FuncPointer([Intable], Types.I32())),
            "toFloat": Scope.Type(True, Types.FuncPointer([Floatable], Types.Float())),
            "Stringable": Stringable,
            "Atom": Scope.Type(True, Atom),
            "Lens": Scope.Type(True, Lens),
            "All": Scope.Type(True, All),
            "newAtom": Scope.Type(True, Types.FuncPointer([T], Atom, coll.OrderedDict([("Atom.T", T)]))),
            "defer": Scope.Type(True, defer),
            "sleep": Scope.Type(True, Types.FuncPointer([Types.I32()], Types.Null(), do= True)),
            "parallel": Scope.Type(True, parallel),
            "serial": Scope.Type(True, serial),
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
                "Stringable": Stringable,
                "Atom": Atom,
                "Lens": Lens,
                "All": All,
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

            #self.imports = []

        self.tokens = tokens
        self.filename = filenames

        infer(self, self.currentNode)


        if self.sc:
            Tree.transform(self.currentNode)
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
