__author__ = 'antonellacalvia'

from TopCompiler import Types
from TopCompiler import Error

variables = [{}]
destructors = [[]]

def addFrame(self):

    v = variables
    variables.append({})
    destructors.append([])

def createVar(self, name, isglobal= False):
    v = variables

    if isglobal:
        variables[0][name] = "@var_"+name
        return

    variables[-1][name] = getName(self, "var")

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

        self.name = ""
        self.inline = False
        self.called = 0
        self.perCall = 0

    def addNode(self, node):
        node.owner = self
        self.nodes.append(node)

    def insertNode(self, index, node):
        node.owner = self
        self.nodes.insert(index, node)

    def iterator(self):
        for i in self.nodes:
            yield i

    def isEnd(self):
        return len(self.nodes) == 0

    def __iter__(self):
        return self.iterator()

    def __str__(self):
        return "root"

    def destruct(self, codegen):
        pass

def getName(codegen, name):
    if name in codegen.names:
        codegen.names[name] += 1
    else:
        codegen.names[name] = 0

    return " %" + name + str(codegen.names[name])


def toStr(array):  # turn names list into something for llvm
    return ", ".join(array)

class Node(Root):  # partially immutable data structure
    def __init__(self, parser):
        Root.__init__(self)
        self.owner = None

        self.token = parser.thisToken()
        self.selfpackage = parser.opackage
        self.opackage = parser.opackage

        self.filename = parser.filename
        self.curry = False

    def error(self, message):
        Error.errorAst(message, self.selfpackage, self.filename, self.token)

    def __str__(self):
        "root"

    def thisToken(self):
        return self.token

    def validate(self, parser):
        raise NotImplementedError(str(self))

    def compileToJS(self, codegen):
        raise NotImplementedError(str(self))


class PlaceHolder(Node):
    def __init__(self, owner= None):
        Node.__init__(self, owner)
    def compile(self, codegen):
        return ""
    def compileToJS(self, codegen):
        pass