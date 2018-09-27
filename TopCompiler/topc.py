__author__ = 'antonellacalvia'

import sys
from TopCompiler import Error

from time import *

from TopCompiler import Lexer
from TopCompiler import Parser
from TopCompiler import CodeGen
from TopCompiler import ImportParser
import sys
import os
import json
from TopCompiler import ResolveSymbols
from optimization import *
from TopCompiler import VarParser
from TopCompiler import saveParser
import datetime
from PostProcessing import SimplifyAst
import collections as coll
import pprint
# is class

def handleOptions(jsonLoad, names):
    t = ()
    for i in names:
        t += (jsonLoad[i] if i in jsonLoad else [],)
    return t

def traverse(parsed, indent=""):
    if parsed.isEnd():
        print(indent + str(parsed))
    else:
        print(indent + str(parsed))
        indent += "\t"
        for iter in parsed:
            traverse(iter, indent)
        indent = indent[:-1]

def newProj(name):
    if name[0].upper() != name[0]:
        Error.error("project name must be uppercase")
    try:
        os.mkdir(name)
        os.mkdir(name + "/" + "src")

        file = open(name + "/src/port.json", mode="w")
        file.write("""
{
    "name": \"""" + name + """\",
    "version": 0.0,
    "link": [],
    "linkCSS": []
}
        """)

        file.close()

        os.mkdir(name + "/" + "lib")
        os.mkdir(name + "/" + "bin")
    except:
        Error.error("project already created")

def linkWith(name):
    try:
        file = open("src/port.json", mode="r+")
    except:
        Error.error("missing port.json file in project")

    port = json.loads(file.read())

    if name.endswith(".css"):
        port["linkCSS"].append(name)
    else:
        port["link"].append(name)

        file.write(json.dumps(port))

    file.close()


def newPack(name):
    if name[0].lower() != name[0]:
        Error.error("package name must be lowercase")
    try:
        os.mkdir("src/" + name)
        f = open("src/"+name+"/port.json", mode= "w")
        f.write("""
{
    "files": []
}
        """)
    except:
        Error.error("directory has no src folder")


global_parser = None

def getCompilationFiles(target):
    try:
        proj = open("src/port.json", mode="r")
        proj.close()
    except:
        Error.error("missing port.json in src folder")

    file = {}

    def getCompFiles(start, dir):
        linkWith = []
        headerIncludePath = []


        for root, dirs, files in os.walk(dir, topdown=False, followlinks=True):
            hasPort = False

            if root != "src/":
                for i in files:
                    if i == "port.json":
                        hasPort = True

            for i in files:
                if not hasPort and i != "port.json" and i.endswith(".top"):
                    package = i[:-4]
                    if package in file and not package == "main":
                        Error.error("multiple packages named " + package)
                    file[package] = [(root, i)]
                    #file[package].append((root, f + ".top"))

            package = root
            if package == start: continue
            package = package[package.find("src/")+len("src/"):]

            if package in file and not package == "main":
                Error.error("multiple packages named "+package)

            file[package] = []

            try:
                port = open(start+package+"/port.json", mode= "r")
            except:
                continue
                Error.error("missing file port.json in package "+package+"")

            files = []
            try:
                j = json.loads(port.read())
                port.close()
                files = j["files"]
            except KeyError:
                Error.error("In file port.js, in directory "+package+", expecting attribute files")
            except json.decoder.JSONDecodeError as e:
                Error.error("In file port.json, in directory "+package+", "+str(e))

            (_linkWith, _headerIncludePath) = handleOptions(j, ["linkWith", "headerIncludePath"])
            (_linkWith, _headerIncludePath) = [
                ["src/" + package + "/" + c for c in i] for i in (_linkWith, _headerIncludePath)]

            linkWith += _linkWith
            headerIncludePath += _headerIncludePath

            for f in files:
                file[package].append((root, f+".top"))

            if root[0].lower() != root[0]:
                Error.error("package name must be lowercase")


        return (linkWith, headerIncludePath)

    try:
        (_, dirs, _) = next(os.walk("packages", followlinks=True))
    except StopIteration:
        dirs = {}

    (linkWith, headerIncludePath) = [[],[]]

    for name in dirs:
        f = open("packages/"+name+"/src/port.json")
        jsonLoads = json.loads(f.read())

        (_linkWith, _headerIncludePath) = handleOptions(jsonLoads, ["linkWith", "headerIncludePath"])

        (_linkWith, _headerIncludePath) = [[(name, "packages/"+name+"/"+c) for c in i] for i in (_linkWith, _headerIncludePath)]

        linkWith += _linkWith
        headerIncludePath += _headerIncludePath

        (_linkWith, _headerIncludePath, _files) = getCompFiles("packages/"+name+"/src/", "packages/"+name+"/src/")
        (_linkWith, _headerIncludePath, _files) = [
            [(name, "packages/" + name + "/" + c) for c in i] for i in
            (_linkWith, _headerIncludePath, _files)]

        linkWith += _linkWith
        headerIncludePath += _headerIncludePath

    (_linkWith, _headerIncludePath) = getCompFiles("src/", "src/")
    (_linkWith, _headerIncludePath) = [
        [("", c) for c in i] for i in
        (_linkWith, _headerIncludePath)]

    linkWith += _linkWith
    headerIncludePath += _headerIncludePath

    return (linkWith, headerIncludePath, file)

compiled = []

error = ""

filenames_sources = {}

global_parser = 0

def start(run= False, _raise=False, dev= False, doc= False, init= False, _hotswap= False, cache= False, debug= False, compileRuntime=False):
    global modified_
    modified_ = {}
    time1 = time()


    hotswap = dev and not run
    global outputFile
    global didCompile
    global global_parser

    didCompile = False

    try:
        opt = 0
        skip = 0

        outputFile = ""

        for (iter, i) in enumerate(sys.argv[2:]):
            if skip > 0:
                continue

            skip -= 1
            if i == "-O3":
                opt = 3
            elif i == "-O2":
                opt = 2
            elif i == "-o":
                outputFile = sys.argv[iter + 3]
                skip = 1
            elif i == "-O1":
                opt = 1
            else:
                Error.error("unknown argument '" + i + "'.")

        if not _hotswap and opt == 0:
            #cache = saveParser.load(compileRuntime)
            pass
        beforeLoad = time()

        try:
            port = open("src/port.json")
            data = port.read()
            port.close()
        except FileNotFoundError:
            Error.error("Missing file port.json in folder src")

        try:
            jsonLoad = json.loads(data)
        except Exception as e:
            Error.error("invalid json in port.json, "+str(e))

        try:
            target = jsonLoad["target"]
            if not target in ["osx", "windows"]:
                Error.error("In global port.json file: unknown compile target, " + target)
        except KeyError:
            Error.error("must specify compilation target in port.json file")

        (linkWith, headerIncludePath, files) = handleOptions(jsonLoad, ["linkWith", "headerIncludePath", "files"])
        (linkWith, headerIncludePath, files) = [
            [("", c) for c in i] for i in (linkWith, headerIncludePath, files)]

        (_linkWith, _headerIncludePath, files) = getCompilationFiles(target)

        linkWith += _linkWith
        headerIncludePath += _headerIncludePath


        global filenames_sources

        sources = {}
        filenames = {}

        for package in files:
            #if not hotswap or (hotswap and modified(files[runtime], runtime)):


            def iterate(i):
                try:
                    file = open(os.path.join(i[0], i[1]), mode="r")
                    r = file.read()

                    filenames_sources[package][i[1][:-4]] = r
                    sources[package].append(r)

                    if i[1][0] != i[1][0].lower():
                        Error.error("File name must be lowercase")

                    filenames[package].append((i[0], i[1][:-4]))

                    file.close()
                except FileNotFoundError:
                    Error.error("File " + os.path.join(i[0], i[1]) + ", not found")

            sources[package] = []
            if not hotswap or (hotswap and modified(target, cache.files[package], package)):
                filenames[package] = []
                filenames_sources[package] = {}


                for i in files[package]:
                    iterate(i)
            else:
                for (pkg, name) in cache.files[package]:
                    sources[package].append(filenames_sources[package][name[:-4]])

                filenames[package] = cache.files[package]

        if outputFile == "":
            outputFile = (jsonLoad["name"])

        if not "main" in filenames_sources:
            Error.error("Project must have a main package, from where to start the code for the client")

        """
        import cProfile
        profile = cProfile.Profile()
        profile.enable()
        #"""

        globalTarget = target

        didCompile = False

        def compile(target, sources, filenames, former = None):
            global global_parser

            global_parser = cache

            #print(cache.usedModules)

            lexed = Lexer.lex(target, sources, filenames, files, cache, {})

            print("Lexed and parsed : " + str(Lexer.linesOfCode))

            declarations = Parser.Parser(lexed, filenames)
            declarations.hotswap = False
            declarations.shouldCompile = {}
            declarations.atoms = 0
            declarations.atomTyp = False
            declarations.outputFile = outputFile
            declarations.usedModules = {}
            declarations.path = os.path.abspath("")

            global_parser = declarations

            if cache:
                declarations.scope = cache.scope
                declarations.interfaces = cache.interfaces
                declarations.structs = cache.structs
                declarations.hotswap = hotswap
                declarations.allImports = cache.allImports
                declarations.atomTyp = cache.atomTyp
                declarations.hotswap = True
                declarations.usedModules = cache.usedModules

            if former:
                #print("inserting", target)
                ResolveSymbols.insert(former, declarations, only= True, copy= False)
                #print(declarations.scope["_global"])

            declarations.files = files
            declarations.lexed = lexed
            declarations.filenames = filenames
            declarations.opt = opt
            declarations.compiled = coll.OrderedDict()
            declarations.externFuncs = {"main": []}
            declarations.filenames_sources = filenames_sources
            declarations.global_target = target
            declarations.output_target = target
            declarations.didCompile = False

            declarations.setGlobalData(compileRuntime)

            if (dev and run):
                clearMain(declarations)

            ResolveSymbols.resolve(declarations)

            #print("declarations")

            #print(declarations.shouldCompile)

            if opt == 3 or doc or ImportParser.shouldCompile(False, "main", declarations):
                parser = Parser.Parser(lexed["main"], filenames["main"])
                parser.package = "main"
                ResolveSymbols.insert(declarations, parser, only= True)

                parser.files = files
                parser.global_target = target
                parser.output_target = target
                parser.lexed = lexed
                parser.filenames = filenames
                parser.compiled = declarations.compiled
                parser.compiled["main"] = None
                parser.contextFields["main"] = {}
                parser.dev = dev

                parsed = parser.parse()

                parser.compiled["main"] = (True, (parsed, []))


                global_parser = parser

                import AST as Tree
                allCode = Tree.Root()

                """
                if opt > 0:
                    for d in parser.compiled:
                        allCode.addNode(parser.compiled[d][1][0])
                    optimize(allCode, opt)
                """

                #print("parsing")

                if doc:
                    return parser

                canStartWith = ['']

                order_of_modules = []

                compiled = parser.order_of_modules  # order_of_modules #parser.compiled
                print(parser.order_of_modules)

                typesInContext = []

                def removeTypes(typesInContext, tmpTypesInContext):
                    tmp = []
                    for name in typesInContext:
                        Types.genericTypes[name] = None
                        tmp.append((True, name))

                    for name in tmpTypesInContext:
                        Types.tmpTypes[name] = None
                        tmp.append((False, name))

                    return tmp

                def addTypes(tmp):
                    for (inGeneric, name) in tmp:
                        if inGeneric:
                            del Types.genericTypes[name]
                        else:
                            del Types.tmpTypes[name]


                for i in parser.compiled:
                    parser.package = i
                    if parser.compiled[i][0]:
                        SimplifyAst.resolveGeneric(parser, parser.compiled[i][1][0])

                if compileRuntime:
                    contextCCode = CodeGen.buildContext(parser.contextType)
                else:
                    removedTypes = removeTypes(["_global_Allocator"], [
                        "typedef void*(*prnonec_SizeTp___rnone)(void*,unsigned int,struct _global_Context*)",
                        "typedef unsigned int(*prnonep___uint)(void*,struct _global_Context*)"
                    ])

                if not compileRuntime:
                    addTypes(removedTypes)
                    contextCCode = CodeGen.buildContext(parser.contextType)

                for i in compiled:
                    tmp = os.path.dirname(parser.filenames[i][0][0])

                    dir = tmp[tmp.find("packages")+len("packages")+1:tmp.rfind("src")-1]
                    canStartWith.append(dir)

                    if parser.compiled[i][0]:
                        CodeGen.CodeGen(parser, order_of_modules, i, parser.compiled[i][1][0], parser.compiled[i][1][1], target, opt, debug= debug).compile(opt=opt)

                order_of_modules.append("main")

                for i in parser.lexed:
                    parser.usedModules[i] = datetime.datetime.now()

                _linkWith = [i for (d, i) in linkWith if d in canStartWith]
                _headerIncludePath = [i for (d, i) in headerIncludePath if d in canStartWith]

                timeForCodeAnalysis = time() - beforeLoad
                if compileRuntime:   #not dev and not _raise:
                    parser.generatedGenericTypes = Types.genericTypes
                    deleteQue = []
                    for c in parser.generatedGenericTypes:
                        parser.generatedGenericTypes[c] = None
                        if c in ["_global_Allocator"]:
                            deleteQue.append(c)

                    for c in deleteQue:
                        del parser.generatedGenericTypes[c]

                saveParser.save(parser, compileRuntime)

                l = CodeGen.link(compiled, outputFile, opt=opt, dev=dev, hotswap= hotswap, debug= debug, linkWith=_linkWith, headerIncludePath=_headerIncludePath, target=target, context=contextCCode, runtimeBuild=compileRuntime)

                print(compiled)
                print("Code Analysis : " + str(timeForCodeAnalysis))
                print("\n======== recompiling =========")
                print("Compilation took : " + str(time() - time1))
                print("")

                if run:
                    CodeGen.exec(outputFile)

                didCompile = True

                parser.didCompile = True
                return parser
            elif run:
                CodeGen.exec(outputFile)

            return declarations


        fil = filenames
        sour = sources

        c = compile(target, sour, fil)

        return c
    except (EOFError, ArithmeticError) as e:
        if dev or _raise:
            Error.error(str(e))
        else:
            print(e, file= sys.stderr)

    if didCompile:
        print("Compilation took : " + str(time() - time1))

    #profile.print_stats("time")

import datetime
modified_ = {}
def modified(_target, files, outputfile, jsFiles=[]):
    return True #while developing incremental compilation sucks

    def inner():
        target = _target
        if target == "full":
            target = "node"

        if not outputfile in global_parser.usedModules:
            return True
        else:
            t = global_parser.usedModules[outputfile]

        if outputfile == "main": #linking is done globally not module specific
            for i in global_parser.jsFiles:
                file = os.path.getmtime(i)
                file = datetime.datetime.fromtimestamp(int(file))

                if file > t:
                    return True

        import time
        o = compiled

        for i in files:
            joined = os.path.join(i[0], i[1])
            file = os.path.getmtime(joined)
            file = datetime.datetime.fromtimestamp(int(file))

            if file > t:
                return True

        return False

    if outputfile in modified_:
        return modified_[outputfile]
    else:
        res = inner()
        modified_[outputfile] = res
        return res

def clearMain(parser):
    try:
        del parser.usedModules["main"]
        del parser.scope["main"]
        del parser.interfaces["main"]
        del parser.structs["main"]
    except KeyError:
        pass