import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import PostProcessing
import os
import copy

from AST import Func

import subprocess
import collections as coll

runtimeFile = open(os.path.dirname(__file__) + "/runtime/runtime.c", "r")
cRuntimeCode = runtimeFile.read()
runtimeFile.close()

from TopCompiler import Types

class CodeGen:
    def __init__(self, parser, order_of_modules, filename, tree, externFunctions, target, opt, main=True):
        self.tree = tree
        self.filename = filename
        self.parser = parser

        self.contextType = parser.contextType

        self.opt = opt

        self.out = ""
        self.order_of_modules = order_of_modules

        self.target = target

        self.out_parts = []
        self.main_parts = []
        self.func_parts = []
        self.func_count = 0

        self.main = ""

        self.externs = externFunctions

        self.inAFunction = 0
        self.names = [{}]
        self.contexts = []
        self.nameCount = 0

        self.info = Info()
        self.gen = genNames(self.info)

        self.indent = 0

        self.out_scopes = []
        self.count = 0
        self.deferred = []

    def inFunction(self):
        self.inAFunction += 1
        self.func_parts.append([])

    def outFunction(self):
        self.info.reset([0], 0)

        self.inAFunction -= 1
        if self.inAFunction == 0:
            for i in reversed(self.func_parts):
                self.out_parts.extend(i)
            self.func_parts = []

    def inGenerateFunction(self):
        self.inFunction()

    """ 
    def setInAFunction(self, new):
        raise Exception()
        
        if new > 0:
            self.inAFunction = new + 1
            if self.inAFunction == 0:
                for i in reversed(self.func_parts):
                    self.out_parts.extend(i)
                self.func_parts = []

        else:
            self.outFunction()
    """

    def incrScope(self):
        self.names.append({})

    def getDeferred(self):
        return self.deferred[-1]

    def outputDeferred(self):
        for i in self.getDeferred():
            i()

    def incrDeferred(self):
        self.deferred.append([])

    def decrDeferred(self):
        self.outputDeferred()
        self.deferred.pop()

    def decrScope(self):
        self.names.pop()

    def readName(self, name):
        #return name

        for i in reversed(self.names):
            try:
                return i[name][1]
            except:
                pass

    def getParts(self):
        if self.inAFunction > 0:
            return self.func_parts[self.inAFunction - 1]
        else:
            return self.main_parts

    def addSemicolon(self, ast):
        if not type(ast) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
            self.append(";\n")
            return
            self.append(f';\n#line {ast.token.line+2} "{ast.fullFilePath()}.top"\n')

    def createName(self, name, typ):
        self.names[-1][name] = (typ, name)
        return name

    def append(self, value):
        self.getParts().append(value)

    def toCHelp(self, tree=None, isGlobal=True):
        if tree is None:
            tree = self.tree

        self.incrDeferred()

        for (iter, i) in enumerate(tree):
            if type(i) is Tree.FuncStart:
                funcStart = i
                funcBrace = i.owner.nodes[iter+1]
                funcBody = i.owner.nodes[iter+2]
                Func.forwardRef(funcStart, funcBrace, funcBody, self)

        for i in tree:
            i.compileToC(self)
            self.addSemicolon(i)

        self.decrDeferred()

    def getName(self):
        return next(self.gen)

    def getContext(self):
        return self.contexts[-1]

    def compile(self, opt):
        self.contexts = ["(&_global_context)"]

        self.parser.package = self.filename
        PostProcessing.simplifyAst(self.parser, self.tree)

        self.toCHelp()

        mainCode = "".join(self.main_parts)
        outerCode = "".join(self.out_parts)

        (generatedTypes, mainC) = Types.getGeneratedDataTypes()

        cCode = f"{generatedTypes}\n{outerCode}\nvoid {self.filename}Init() {{ \n{mainC}\n{mainCode};\n}};"

        #print("To C took :", time() - t)

        f = open("lib/" + self.filename + ".c", mode="w")
        f.write(cCode)
        f.close()

class Info:
    def __init__(self):
        self.pointer = 0
        self.array = [0]

    def reset(self, lastArr, pointer):
        self.array = lastArr
        self.pointer = pointer

def buildContext(contextType):
    # build context data type
    context = "_global_context"
    typesGeneratedByContext = ""

    types = {}
    for field in contextType:
        types[field] = contextType[field].toCType()

    string = []
    (typesGen, mainC) = Types.getGeneratedDataTypes()

    Types.compiledTypes = coll.OrderedDict()
    Types.dataTypes = []

    string.append(typesGen)

    string.append("struct _global_Context {\n")
    for field in contextType:
        string.append(f"{types[field]} {field};")
    string.append("};\n")

    string.append(f"struct _global_Context {context};")

    return ("".join(string), mainC)

import os



def link(compiled, outputFile, opt, hotswap, debug, linkWith, target, dev, context, runtimeBuild): #Add Option to change compiler
    topRuntime = ""
    (context, mainC) = context
    if not runtimeBuild:
        topRuntime = open(os.path.dirname(__file__) + "/TopRuntime/lib/_global.c")
        topRuntime = topRuntime.read()

    linkedCode = [context, cRuntimeCode, topRuntime, "struct _global_Context _global_context;"]

    for c in compiled:
        f = open("lib/" + c + ".c", mode="r")
        linkedCode.append(f.read())
        f.close()

    linkedCode.append(f"int main() {{ \n {mainC}; \n_globalInit(); \n mainInit(); return 0; }};")

    f = open("bin/" + outputFile + ".c", mode="w")
    f.write("\n".join(linkedCode))
    f.close()

    subprocess.call(["clang", "bin/" + outputFile + ".c", "-o", "bin/" + outputFile, "-Wno-incompatible-pointer-types", "-Wno-visibility", "-Wno-return-type"])

def exec(outputFile):
    try:
        subprocess.call(["./bin/"+outputFile])
    except:
        Error.error("running .exe failed")

def genNames(info):
    import string

    def overflow(id):
        return len(letters) <= info.array[id]

    letters = [i for i in string.ascii_letters if not i.lower() in ('a', 'e', 'i', 'o', 'u')]
    info.pointer = 0
    skip = False

    while True:
        if overflow(info.pointer):
            info.array[info.pointer] = 0
            if info.pointer == 0:
                info.array = [0] * (len(info.array) + 1)
                info.pointer = len(info.array) - 1
            else:
                info.pointer -= 1
                info.array[info.pointer] += 1
        elif info.pointer != len(info.array) - 1:

            yield ("".join((letters[i] for i in info.array)))
            info.pointer += 1
            info.array[info.pointer] += 1
        else:

            yield ("".join((letters[i] for i in info.array)))
            info.array[info.pointer] += 1

global_info = Info()
global_gen = genNames(global_info)

def genGlobalTmp(package):
    tmp = global_gen.__next__()

    return "tmp"+package + tmp

