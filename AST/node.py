__author__ = 'antonellacalvia'

from TopCompiler import Types
from TopCompiler import Error
import AST as Tree
import copy

variables = [{}]
destructors = [[]]

def addFrame(self):

    v = variables
    variables.append({})
    destructors.append([])

def readVar(self, name):
    v = variables
    for i in reversed(variables):
        try:
            return i[name]
        except KeyError:
            pass

def delFrame(codegen):
    v = variables
    d = destructors

    glob = codegen.isGlobal

    variables.pop()
    for i in destructors.pop():
        b = i.destruct(codegen)

        if b:
            if glob:
                codegen.main_parts.append(b)
            else: codegen.append(b)

def addDestructor(node):
    destructors[-1].append(node)

class Root:
    def __init__(self):
        self.nodes = []
        self.type = Types.Null()
        self.names = []
        self.global_target = "full"

        self.name = ""
        self.inline = False
        self.called = 0
        self.perCall = 0

        self.before = []

    def case(self, codegen, number, node):
        codegen.append("case "+number+":")

    def addNode(self, node):
        node.owner = self
        self.nodes.append(node)

    def insertNode(self, index, node):
        node.owner = self
        self.nodes.insert(index, node)

    def iterator(self):
        for i in copy.copy(self.nodes):
            yield i

    def isEnd(self):
        return len(self.nodes) == 0

    def __iter__(self):
        return self.iterator()

    def __str__(self):
        return "root"

    def destruct(self, codegen):
        pass

    def validate(self, parser): pass

def isUseless(i):
    if i.repl:
        return

    if type(i) in [Tree.ReadVar, Tree.ArrRead]:
        i.error("useless read")
    elif type(i) in [Tree.Int, Tree.Array, Tree.ArrRead, Tree.String, Tree.Bool, Tree.Float]:
        i.error("useless literal")
    elif type(i) is Tree.Operator:
        i.error("useless operator")
    elif type(i) is Tree.FuncCall and not i.nodes[0].type.do:
        if i.type != Types.Null():
            i.error("not using return of function")
    try:
        t = i.curry
        if t: i.error("useless curry")
        t = i.partial
        if t: i.error("useless function application")
    except AttributeError:
        pass

def checkOther(self, parser, function, block, iter=0):
    if type(self) in [Tree.FuncStart, Tree.FuncBraceOpen]: return

    for (c, i) in enumerate(self.nodes):
        if type(self) in [Tree.While, Tree.For]:
            checkOther(i, parser, function, self, c)
        elif type(self) is Tree.FuncBody:
            checkOther(i, parser, self, block, c)
        else:
            checkOther(i, parser, function, block, c)
    if type(self) in [Tree.Continue, Tree.Break] and not type(block) in [Tree.While, Tree.For]:
        statement  = "continue" if type(self) is Tree.Continue else "break"
        self.error(f"unexpected {statement}, outside of a loop")
    elif type(self) is Tree.Return:
        if not function:
            self.error(f"unexpected return statement, outside of a function")
        try:
            actReturnType = self.nodes[0].type
            function.returnType.duckType(parser,actReturnType, self, self ,0)
            Tree.insertCast(self, actReturnType, function.returnType, iter)
        except EOFError as e:
            Error.beforeError(e, "Return Type: ")
    else:
        self.validate(parser)

def validate(parser, self, function=None, block=None):
    checkUseless(self)
    checkOther(self, parser, None, None)

def checkUseless(self):
    if type(self) is Tree.FuncBody and self.returnType.name == "none":
        checkNodes = self.nodes
    elif type(self) is Tree.For:
        checkNodes = self.nodes
    elif type(self) is Tree.While:
        checkNodes = self.nodes
    else:
        checkNodes = self.nodes[:-1]


    for (iter, i) in enumerate(checkNodes):
        isUseless(i)

        if type(i) in [Tree.FuncBody, Tree.While, Tree.WhileBlock, Tree.If, Tree.Block, Tree.For]:
            checkUseless(i)

def toStr(array):  # turn names list into something for llvm
    return ", ".join(array)

class Node(Root):
    def __init__(self, parser):
        Root.__init__(self)
        self.owner = None

        self.token = parser.thisToken()
        self.selfpackage = parser.opackage
        self.opackage = parser.opackage

        self._filename = parser._filename
        self.path = parser.path

        try:
            self.filename = [a + "/" + parser.filename for (a, b) in parser._filename if b == parser.filename][0]
        except IndexError:
            self.filename = parser.filename

        self.curry = False
        self.repl = parser.repl
        self.first = True

        self.global_target = parser.global_target

    def error(self, message):
        Error.errorAst(message, self.selfpackage, self.filename, self.token)

    def fullFilePath(self):
        return self.path + "/" + self.filename

    def __str__(self):
        "root"

    def __len__(self):
        return len(self.nodes)

    def thisToken(self):
        return self.token

    def validate(self, parser):
        pass
        #raise NotImplementedError(str(self))

    def compileToC(self, codegen):
        raise NotImplementedError(str(self))

class Place(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "placeholder"

    def compileToC(self, codegen):
        codegen.append(self.name)

class PlaceHolder(Node):
    def __init__(self, owner= None):
        Node.__init__(self, owner)

    def compile(self, codegen):
        return ""

    def __str__(self):
        return "Placeholder"

    def validate(self, parser):
        pass

    def compileToC(self, codegen):
        pass