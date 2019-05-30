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
        parser.specifications["_global"].funcs = {}
        parser.specifications["_global"].genericFuncs = {}
        parser.specifications["_global"].packageGenericFuncs = {}


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
            #parser.structs[package][s].actualfields = list(parser.structs[package][s].actualfields.keys())
            parser.structs[package][s].node = 0
            parser.structs[package][s].actualfields = []

    def removeRedundantProperties(ast):
        #ast._filename = None
        if type(ast) in [Tree.FuncBody, Tree.FuncBraceOpen, Tree.FuncStart]:
            ast.owner = None
        #ast.token = None

        for node in ast.nodes:
            removeRedundantProperties(node)

    for package in parser.specifications:
        parser.specifications[package].root = None
        for funcName in parser.specifications[package].genericFuncs:
            (funcStart, funcBrace, funcBody) = parser.specifications[package].genericFuncs[funcName]
            removeRedundantProperties(funcStart)
            removeRedundantProperties(funcBrace)
            removeRedundantProperties(funcBody)

    for name in parser.generatedGenericTypes:
        parser.generatedGenericTypes[name] = None



    pickle.dump(parser, f)

import time

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