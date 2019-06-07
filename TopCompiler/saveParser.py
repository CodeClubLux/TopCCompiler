import pickle

import os
import pprint
import AST as Tree

import copy

from AST import Cast
import time

def save(parser, runtimeBuild):
    #return

    t = time.time()

    print("saving")

    f = open("lib/parser.p", "wb")
    parser.rootAst = 0
    parser.currentNode = 0
    parser.compiled = []
    parser.Stringable = 0
    parser.atomTyp = 0
    parser._tokens = 0
    parser.tokens = 0

    if not runtimeBuild:
        parser.structs["_global"] = {}
        parser.interfaces["_global"] = {}
        parser.scope["_global"] = []

    parser._filename = None
    parser.bracketBookmark = None
    parser.cssFiles = None
    parser.bookmark = None
    parser.filename = None
    parser.filenames = None
    parser.files = None
    parser.lexed = None
    parser._token = None
    parser.__filename = None
    parser.compiledTypes = None
    parser.casted = Cast.casted
    parser.shouldCompile = {}

    for typ in parser.typesInContext:
        if typ in parser.generatedGenericTypes:
            del parser.generatedGenericTypes[typ]


    for package in parser.structs:
        for s in parser.structs[package]:
            for i in parser.structs[package][s].actualfields:
                i.owner = None
            parser.structs[package][s].node = 0

    def removeRedundantProperties(ast):
        #ast._filename = None
        if type(ast) in [Tree.FuncBody, Tree.FuncBraceOpen, Tree.FuncStart]:
            ast.owner = None
        #ast.token = None

        #for node in ast.nodes:
        #    removeRedundantProperties(node)

    for package in parser.specifications:
        parser.specifications[package].root = None
        parser.specifications[package].genericFuncs = {}


        for funcName in parser.specifications[package].packageGenericFuncs:
            parser.specifications[package].genericFuncs[funcName] = parser.specifications[package].packageGenericFuncs[funcName]
            (funcStart, funcBrace, funcBody) = parser.specifications[package].packageGenericFuncs[funcName]
            removeRedundantProperties(funcStart)
            removeRedundantProperties(funcBrace)
            removeRedundantProperties(funcBody)

        for funcName in parser.specifications[package].funcs:
            parser.specifications[package].funcs[funcName] = None

        for funcName in parser.specifications[package].inImports:
            parser.specifications[package].inImports[funcName] = None

    pickle.dump(parser, f)

import time

def dontSaveGeneric(parser):
    #return
    threshold = 2

    remove = []
    for package in parser.specifications:
        if len(parser.specifications[package].packageGenericFuncs) > threshold:
            remove.append(package)
    for package in remove:
        print("removed", package)
        del parser.specifications[package]
        del parser.scope[package]
        del parser.structs[package]
        del parser.interfaces[package]

        if package == "_global": continue

    parser.alwaysRecompile = remove #.append(package) #parser.usedModules[package] = "must update self"

def load(runtimeBuild):
    try:
        f = open("lib/parser.p", "rb")
        if os.stat("lib/parser.p").st_size == 0:
            return False

        res = pickle.load(f)

        if runtimeBuild:
            res.scope["_global"]= [{}]
            res.interfaces["_global"] = {}
            res.structs["_global"] = {}
        return res
    except FileNotFoundError:
        return False

import os
from TopCompiler import Error

runtimeData = os.path.dirname(__file__) + "/TopRuntime/lib/parser.p"

def loadRuntimeTypeData():
    try:
        f = open(runtimeData, "rb")
        if os.stat(runtimeData).st_size == 0:
            Error.error("Runtime type data is empty, please recompile runtime")

        res = pickle.load(f)
        return res
    except FileNotFoundError:
        Error.error("Could not locate runtime")