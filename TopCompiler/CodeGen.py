import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import MemoryOptimizer
import os
import copy

import subprocess

runtimeFile = open(os.path.dirname(__file__) + "/runtime/runtime.c", "r")
cRuntimeCode = runtimeFile.read()
runtimeFile.close()

class CodeGen:
    def __init__(self, parser, order_of_modules, filename, tree, externFunctions, target, opt, main=True):
        self.tree = tree
        self.filename = filename
        self.parser = parser

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
        self.nameCount = 0

        self.info = Info()
        self._level = []
        self._pointer = 0

        self.gen = genNames(self.info)

        self.indent = 0

        self.out_scopes = []
        self.count = 0

    def inFunction(self):
        self.inAFunction = True

    def outFunction(self):
        self.inAFunction = False


    def incrScope(self):
        self.names.append({})

    def decrScope(self):
        self.names.pop()

    def readName(self, name):
        for i in reversed(self.names):
            try:
                return i[name]
            except:
                pass

    def addSemicolon(self, ast):
        if not type(ast) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
            self.append(";\n")

    def createName(self, name):
        self.names[-1][name] = name
        return name

    def append(self, value):
        if self.inAFunction:
            self.out_parts.append(value)
        else:
            self.main_parts.append(value)

    def toCHelp(self, tree=None, isGlobal=True):
        if tree is None:
            tree = self.tree
        out = ""

        if self.opt > 0:
            # variable declarations
            self.inAFunction = True
            for i in tree.before:
                i.compileToC(self)
            self.inAFunction = False

        for i in tree:
            i.compileToC(self)
            self.addSemicolon(i)

    def getName(self):
        return next(self.gen)

    def compile(self, opt):
        beforeOptimization = time()
        MemoryOptimizer.simplifyAst(self.parser, self.tree)
        print("Simplifying AST took: ", time() - beforeOptimization)

        cCode = cRuntimeCode
        self.toCHelp()
        mainCode = "".join(self.main_parts)
        outerCode = "".join(self.out_parts)

        cCode += outerCode + "\nint main() {" + mainCode + "; return 0;};"
        #print(cCode)"

        f = open("lib/" + self.filename + ".c", mode="w")
        f.write(cCode)
        f.close()

        subprocess.call(["clang", "lib/" + self.filename + ".c", "-Wno-parentheses-equality", "-o", "bin/" + self.filename])

class Info:
    def __init__(self):
        self.pointer = 0
        self.array = [0]

    def reset(self, lastArr, pointer):
        self.array = lastArr
        self.pointer = pointer

def link(compiled, outputFile, opt, hotswap, debug, linkWith, target, dev):
    pass

def exec(outputFile):
    subprocess.call(["./bin/main"])

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

