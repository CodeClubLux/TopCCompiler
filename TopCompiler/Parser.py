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
            if parser.thisToken().token in [",", "\n"]:
                endExpr(parser)
            else:
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
    maybeEnd(parser)

    ExprParser.endExpr(parser, -2)

    parser.lineNumber += 1

    indent = int(parser.lookInfront().token)

    if parser.iter + 2 < len(parser.tokens) and parser.tokens[parser.iter+2].token == "\n":
        parser.nextToken()

        return

    if parser.normalIndent == 0:
        if indent > parser.indent[-1]:
            # indent
            parser.normalIndent = indent / 2
    else:
        diff = indent - parser.indent[-1]
        if diff > 0 and diff % parser.normalIndent != 0:
            Error.parseError(parser, "inconsistent indentation")
        elif diff < 0 and -diff % parser.normalIndent != 0:
            Error.parseError(parser, "unindent does not match any outer indentation level")

    parser.indentLevel = indent

precidences = {}  # what operator goes first!

exprType = {}  # depends on parser, needs type information to figure out
exprToken = {"\n": newLine, "(": parenOpen, ")": parenClose}  # depends on parser, needs token information
stmts = {}  # for all statements

class TmpType:
    def __init__(self):
        self.name = "TmpType"
        self.package = "_global"
        self.normalName = "TmpType"
        self.types = {}
        self.methods = {}

    def isType(self, typ):
        return False

StringType = TmpType()
IntType = TmpType()
BoolType = TmpType()
FloatType = TmpType()
StructType = TmpType()
AliasType = TmpType()
CharType = TmpType()
InterfaceType = TmpType()
EnumType = TmpType()
PointerType = TmpType()
IType = TmpType()
ArrayType = TmpType()
NoneType = TmpType()

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
from .ExternParser import *
from .Array import *
from .MethodParser import *
from .Struct import *
from .ForParser import *
from .GuardParser import *
from .TypeInference import *
from .Enum import *
from .ParseJson import *
from .Lambda import *
from .ContextParser import *
from TopCompiler import Struct
from TopCompiler import Sizeof
from TopCompiler import saveParser

runtimeParser = None

def isEnd(parser):
    #if parser.thisToken().token == "\n" and parser.stack != [] and parser.stack[-1].kind == "<-" and parser.package == "main":
    #    print(parser.stack)

    token = parser.thisToken()

    if parser.fired:
        parser.fired = False
        return True

    if token.token in [ "->", "\n", "with", "do", ":="] or parser.parenBookmark[-1] > parser.paren or parser.bracketBookmark[-1] > parser.bracket or parser.curlyBookmark[-1] > parser.curly:
        #if token.token == "!" and len(parser.currentNode.nodes) > 1:
        #    return False

        if token.token == ":=" and type(parser.currentNode) == Tree.Assign:
            return False

        #"""
        if token.token == "|>" and type(parser.currentNode) in [Tree.Assign, Tree.CreateAssign, Tree.Block, Tree.FuncBody, Tree.Root]:
            return False
        #"""

        if token.token in ["with", "do"] and type(parser.currentNode) in [Tree.IfCondition, Tree.Match, Tree.PlaceHolder]:
            return False

        return maybeEnd(parser)
    return False

def declareOnly(self, noVar=False):
    s1 = selectStmt(self, self.thisToken())
    s2 = selectStmt(self, self.lookInfront())

    declaration = ["var", ":", "(", ")", ",", "\n", ":="]
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
        if s1 is VarParser.createParser:
            s1(self, lookBehind= True)
        else:
            s1(self)
        returnBookmark(self)
    elif s2 != None and self.thisToken().token != ")" and self.thisToken().token != "(":
        declare(self.lookInfront())
    else:
        declare(self.thisToken())
        selectExpr(self, self.thisToken())


def maybeEnd(parser):
    if parser.indent[-1] >= parser.indentLevel and parser.paren <= parser.parenBookmark[-1] and parser.bracket <= parser.bracketBookmark[-1]:
        if parser.stack != [] and type(parser.currentNode) in [Tree.FuncBody, Tree.Root]:
            #parser.nodeBookmark.pop()
            ExprParser.endExpr(parser, -2)
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
                        parser.stack[-1].func()
                        parser.stack.pop()
                        tryIt()

        try:
            #if parser.package == "math" and type(parser.currentNode) is Tree.ArrRead:
            #    print("hey")
            tryIt()
        except:
            Error.parseError(parser, "Unexpected " + opcode)

        self.pos = len(parser.currentNode.nodes)
        parser.stack.append(self)
        return

    def __repr__(self):
        return self.kind


def addBookmark(parser):
    parser.bookmark.append(len(parser.stack))
    parser.indent.append(parser.indentLevel)
    parser.parenBookmark.append(parser.paren)
    parser.bracketBookmark.append(parser.bracket)
    parser.curlyBookmark.append(parser.curly)

def returnBookmark(parser):
    parser.bookmark.pop()
    parser.indent.pop()
    parser.parenBookmark.pop()
    parser.bracketBookmark.pop()
    parser.curlyBookmark.pop()


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

def callToken(self, lam= False):

    s1 = selectStmt(self, self.thisToken())

    b = self.thisToken()

    iter = self.iter
    if s1 != None:
        addBookmark(self)
        s1(self)
        returnBookmark(self)
    else:
        l = self.lookBehind()
        moveForward = 0
        isIndentationCall = False
        if self.iter + 2 < len(self.tokens) and b.token == "\n" and (l.token in [")"] or l.type == "identifier") :
            if not (self.tokens[self.iter + 2].token == "\n"):
                if int(self.lookInfront().token) > self.indentLevel:
                    b = self.tokens[self.iter + 2]
                    moveForward = 2
                    #self.iter += 1
                    isIndentationCall = True


        if not lam and (b.token in ["_", "(", "\\", "|", "!"] or not b.type in ["symbol", "operator", "indent"]) and not b.token in ["as", "in", "not", "and", "or", "then", "with", "do", "else", "either", "cast", "->"] and (isIndentationCall or not ExprParser.isUnary(self, self.lookBehind(), onlyFact=True)):
            if b.token == "$": #what does this do
                ExprParser.endExpr(self, -2)
            addBookmark(self)
            if b.token == "!":
                FuncParser.callFunc(self, False, True)
            else:
                FuncParser.callFunc(self, False, False)
            returnBookmark(self)
            return
        else:
            self.iter += moveForward

        selectExpr(self, b)

class Func:
    def __init__(self, args, returnType):
        self.args = args
        self.returnType = returnType



class Parser:  # all mutable state
    def nextToken(parser):
        parser.iter += 1
        if parser.iter < len(parser.tokens):
            return parser.tokens[parser.iter]
            #if t.token == "," and parser.lookBehind().token == ",":
            #    Error.parseError(parser, "unexpected ,")
            #return t
        else:
            parser.iter -= 1
            if parser.paren > 1:
                Error.parseError(parser, "unmatched (")
            if parser.bracket > 0:
                Error.parseError(parser, "unmatched [")
            if parser.curly > 0:
                print(parser.curly)
                Error.parseError(parser, "unmatched {")


            Error.parseError(parser, "EOF")

    def on(self, ast):
        self.__filename = ast.filename
        self._token = ast.token

    def error(self, message):
        Error.errorAst(message, self.package, self.__filename, self._token)

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
        self.curly = 0
        self.parenBookmark = [0]
        self.bracketBookmark = [0]
        self.curlyBookmark = [0]
        self.indentLevel = 0

        self.fired = False

        self.lineNumber = 1
        self.stack = []

        self.nodeBookmark = [0]

        self.indent = []
        self.normalIndent = 0

        self.bookmark = [0]

        self.sc = True
        self.repl = False

        self.interfaces = {}
        self.scope = {}
        self.alwaysRecompile = []

        self.iter = 0

        self.package = "_global"
        self.opackage = ""
        self.imports = []
        self.transforms = []

        self.rootAst = Tree.Root()
        self.currentNode = self.rootAst

        self.allImports = {}

        self.filename = ""
        self.tokens = [None]

        self.structs = {"_global": {}}
        self.func = {"_global": {}}

        self.filename = filename
        self.tokens = tokens

        self.opt = 0
        self.specifications = {}

        self.order_of_modules = []
        self.contextFields = {}
        self.contextType = {}
        self.compiledTypes = {}
        self.generatedTypesPerPackage = {}
        self.includes = {}

        self.sc = True

    def setArrayTypes(self):
        global StaticArray
        global DynamicArray
        tmp = self.structs["_global"]["Array"]
        tmp3 = self.structs["_global"]["StaticArray"]

        DynamicArray = Types.Struct(False, tmp.normalName, tmp._types, tmp.package, tmp.generic)
        StaticArray = Types.Struct(False, tmp3.normalName, tmp3._types, tmp3.package, tmp3.generic)

    def setTypeIntrospection(self):
        global DynamicArray
        global Range
        global Char

        global StringType
        global IntType
        global BoolType
        global FloatType
        global StructType
        global AliasType
        global CharType
        global InterfaceType
        global EnumType
        global PointerType
        global IType
        global ArrayType
        global NoneType

        tmp2 = self.structs["_global"]["Range"]
        tmp4 = self.structs["_global"]["StringType"]
        tmp5 = self.structs["_global"]["IntType"]
        tmp6 = self.structs["_global"]["FloatType"]
        tmp7 = self.structs["_global"]["BoolType"]
        tmp8 = self.structs["_global"]["StructType"]
        tmp9 = self.structs["_global"]["AliasType"]
        tmp10 = self.structs["_global"]["CharType"]
        tmp11 = self.structs["_global"]["InterfaceType"]
        tmp12 = self.structs["_global"]["EnumType"]
        tmp13 = self.structs["_global"]["PointerType"]
        tmp14 = self.structs["_global"]["ArrayType"]
        tmp15 = self.structs["_global"]["NoneType"]

        self.setArrayTypes()
        Range = Types.Struct(False, tmp2.normalName, tmp2._types, tmp2.package)
        StringType = Types.Struct(False, tmp4.normalName, tmp4._types, tmp4.package)
        IntType = Types.Struct(False, tmp5.normalName, tmp5._types, tmp5.package)
        FloatType = Types.Struct(False, tmp6.normalName, tmp6._types, tmp6.package)
        BoolType = Types.Struct(False, tmp7.normalName, tmp7._types, tmp7.package)
        StructType = Types.Struct(False, tmp8.normalName, tmp8._types, tmp8.package)
        AliasType = Types.Struct(False, tmp9.normalName, tmp9._types, tmp9.package)
        CharType = Types.Struct(False, tmp10.normalName, tmp10._types, tmp10.package)
        InterfaceType = Types.Struct(False, tmp11.normalName, tmp11._types, tmp11.package)
        EnumType = Types.Struct(False, tmp12.normalName, tmp12._types, tmp12.package)
        PointerType = Types.Struct(False, tmp13.normalName, tmp13._types, tmp13.package)
        IType = self.interfaces["_global"]["Type"]
        ArrayType = Types.Struct(False, tmp14.normalName, tmp14._types, tmp14.package)
        NoneType = Types.Struct(False, tmp15.normalName, tmp15._types, tmp15.package)

    def setGlobalData(self, compileRuntime):
        global Stringable
        global runtimeParser

        Stringable = Types.Interface(False, {}, methods={"toString": Types.FuncPointer([], Types.String(0))},
                                     name="Stringer")

        All = Types.All
        self.Stringable = Stringable

        if not compileRuntime:
            if not runtimeParser:
                runtimeParser = saveParser.loadRuntimeTypeData()  # data containing runtime

            self.interfaces["_global"] = runtimeParser.interfaces["_global"]
            self.structs["_global"] = runtimeParser.structs["_global"]
            self.scope["_global"] = runtimeParser.scope["_global"]
            self.contextFields["_global"] = runtimeParser.contextFields["_global"]

            self.contextType.update(runtimeParser.contextType)
            self.specifications["_global"] = runtimeParser.specifications["_global"]
            self.scope["_global"][0]["console_input"] = Scope.Type(True, Types.FuncPointer([Types.String(0)], Types.String(0)))
            self.scope["_global"][0]["context"] = Scope.Type(False, Types.Pointer(Types.Struct(True, "Context", self.contextType,"_global"), True))

            tmp = self.tokens
            self.tokens = [0]
            self._filename = ""

            self.structs["_global"]["Context"] = Struct.Struct("Context", [], [], {}, Tree.PlaceHolder(self), "_global")

            self.tokens = tmp

            self.structs["_global"]["Context"]._types = self.contextType

            Types.genericTypes = runtimeParser.generatedGenericTypes
            Types.inProjectTypes = {name: None for name in Types.genericTypes}

            Tree.casted = runtimeParser.casted
            self.setTypeIntrospection()
            return

        tmp = self.tokens
        self.tokens = [0]
        self._filename = ""

        self.structs["_global"] = {
            "Context": Struct.Struct("Context", [], [], {}, Tree.PlaceHolder(self), "_global")
        }

        self.tokens = tmp
        self.structs["_global"]["Context"]._types = self.contextType

        if not "_global" in self.scope or len(self.scope["_global"]) == 0:
            self.scope["_global"] = [{}]

        self.interfaces["_global"] = {"Stringer": Stringable, "Any": All}
        #self.contextFields["_global"] = {}
        self.scope["_global"][0]["offsetPtr"] = Scope.Type(True,Types.FuncPointer([Types.Pointer(Types.Null(), True), Types.I32(size=64)],
                                                      Types.Pointer(Types.Null(), True)))
        self.scope["_global"][0]["context"] = Scope.Type(False,
                                  Types.Pointer(Types.Struct(True, "Context", self.contextType, "_global"), True))

        self.scope["_global"][0]["Stringer"] =  Scope.Type(True, Stringable)

    def parse(self):
        tokens = self.tokens
        filenames = self.filename

        self._tokens = tokens
        self._filename = filenames

        for i in range(len(tokens)):
            PackageParser.packDec(self, self.package)
            self._parse(tokens[i], filenames[i][1])

        self.order_of_modules.append(self.package)
            #self.imports = []
        self.iter = 0

        infer(self, self.currentNode)

        self.tokens = tokens
        self.filename = filenames

        if self.sc:
            validate(self, self.currentNode)

        return self.currentNode

    def _parse(self, tokens, filename):
        self.tokens = tokens
        self.filename = filename

        self.iter = 0
        while self.iter < len(tokens) - 1:
            t = self.thisToken()
            callToken(self)
            self.nextToken()

        ExprParser.endExpr(self)

        return self.currentNode
