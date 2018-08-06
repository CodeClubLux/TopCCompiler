import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import PostProcessing
import os
import copy

import subprocess

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

        self.main = ""

        self.externs = externFunctions

        self.inAFunction = False
        self.names = [{}]
        self.contexts = []
        self.nameCount = 0

        self.info = Info()
        self.gen = genNames(self.info)

        self.indent = 0

        self.out_scopes = []
        self.count = 0

    def inFunction(self):
        self.inAFunction = True

    def outFunction(self):
        self.inAFunction = False
        self.info.reset([0], 0)

    def incrScope(self):
        self.names.append({})

    def decrScope(self):
        self.names.pop()

    def readName(self, name):
        return name

        for i in reversed(self.names):
            try:
                return i[name]
            except:
                pass

    def addSemicolon(self, ast):
        if not type(ast) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
            self.append(";\n")

    def createName(self, name):
        #self.names[-1][name] = name
        return name

    def append(self, value):
        if self.inAFunction:
            self.out_parts.append(value)
        else:
            self.main_parts.append(value)

    def toCHelp(self, tree=None, isGlobal=True):
        if tree is None:
            tree = self.tree

        for i in tree:
            i.compileToC(self)
            self.addSemicolon(i)

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

    Types.genericTypes = {}
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

    linkedCode.append(f"int main() {{ \n {mainC}; \n mainInit(); return 0; }};")

    f = open("bin/" + outputFile + ".c", mode="w")
    f.write("\n".join(linkedCode))
    f.close()

    subprocess.call(["clang", "bin/" + outputFile + ".c", "-o", "bin/" + outputFile, "-Wno-incompatible-pointer-types", "-Wno-visibility"])

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

