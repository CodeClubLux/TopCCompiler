__author__ = 'antonellacalvia'

import sys
from TopCompiler import Error

from time import *

from TopCompiler import Lexer
from TopCompiler import Parser
from TopCompiler import CodegenJS as CodeGen
from TopCompiler import ImportParser
import sys
import os
import json
from TopCompiler import ResolveSymbols
from optimization import *

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


class FakeParser:
    def __init__(f, scope, structs, interfaces, allImports, lexed):
        f.scope = scope
        f.structs = structs

        print(interfaces)

        f.interfaces = interfaces
        f.allImports = allImports
        #f.lexed = lexed

def getCompilationFiles(target):
    try:
        proj = open("src/port.json", mode="r")
        proj.close()
    except:
        Error.error("missing port.json in src folder")

    file = {}

    def getCompFiles(start, dir):
        for root, dirs, files in os.walk(dir, topdown=False):
            package = root
            if package == start: continue
            package = package[package.find("src/")+len("src/"):]

            if package in file and not package == "main":
                Error.error("multiple packages named "+package)

            file[package] = []

            try:
                port = open(start+package+"/port.json", mode= "r")
            except:
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

            for f in files:
                file[package].append((root, f+".top"))

            if root[0].lower() != root[0]:
                Error.error("package name must be lowercase")
    try:
        (_, dirs, _) = next(os.walk("packages"))
    except StopIteration:
        dirs = {}

    (linkCSSWithFiles, linkWithFiles, clientLinkWithFiles, nodeLinkWithFiles) = [[],[],[],[]]

    for name in dirs:
        f = open("packages/"+name+"/src/port.json")
        jsonLoads = json.loads(f.read())

        (_linkCSSWithFiles, _linkWithFiles, _clientLinkWithFiles, _nodeLinkWithFiles) = handleOptions(jsonLoads,
            ["linkCSS", "linkWith", "linkWith-client", "linkWith-node"])

        (_linkCSSWithFiles, _linkWithFiles, _clientLinkWithFiles, _nodeLinkWithFiles) = [["packages/"+name+"/"+c for c in i] for i in (_linkCSSWithFiles, _linkWithFiles, _clientLinkWithFiles, _nodeLinkWithFiles)]

        linkCSSWithFiles += _linkCSSWithFiles
        linkWithFiles += _linkWithFiles
        clientLinkWithFiles += _clientLinkWithFiles
        nodeLinkWithFiles += _nodeLinkWithFiles

        getCompFiles("packages/"+name+"/src/", "packages/"+name+"/src/")

    getCompFiles("src/", "src/")

    return (linkCSSWithFiles, linkWithFiles, clientLinkWithFiles, nodeLinkWithFiles, file)

compiled = []

error = ""

filenames_sources = {}

def start(run= False, dev= False, doc= False, init= False, hotswap= False, cache= False):
    hotswap = dev and not run
    global outputFile
    global didCompile

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

        try:
            port = open("src/port.json")
            data = port.read()
            port.close()
        except:
            Error.error("Missing file port.json in folder src")

        try:
            jsonLoad = json.loads(data)
        except:
            Error.error("invalid json in port.json")

        try:
            target = jsonLoad["target"]
            if not target in ["client", "node", "full"]:
                Error.error("In global port.json file: unknown compile target, " + target)
        except KeyError:
            Error.error("must specify compilation target in port.json file")

        (linkCSSWithFiles, linkWithFiles, clientLinkWithFiles, nodeLinkWithFiles) = handleOptions(jsonLoad, ["linkCSS", "linkWith", "linkWith-client", "linkWith-node"])

        (_linkCSSWithFiles, _linkWithFiles, _clientLinkWithFiles, _nodeLinkWithFiles, files) = getCompilationFiles(target)

        linkCSSWithFiles += _linkCSSWithFiles
        linkWithFiles += _linkWithFiles
        clientLinkWithFiles += _clientLinkWithFiles
        nodeLinkWithFiles += _nodeLinkWithFiles

        global filenames_sources

        sources = {}
        filenames = {}

        for package in files:
            #if not hotswap or (hotswap and modified(files[c], c)):


            def iterate(i):
                try:
                    file = open(os.path.join(i[0], i[1]), mode="r")
                    r = file.read()

                    filenames_sources[package][i[1][:-4]] = r
                    sources[package].append(r)

                    if i[1][0].upper() == i[1][0]:
                        Error.error("File name must be lowercase")

                    filenames[package].append((i[0], i[1][:-4]))

                    file.close()
                except FileNotFoundError:
                    Error.error("File " + os.path.join(i[0], i[1]) + ", not found")

            sources[package] = []
            if not hotswap or (hotswap and modified(cache.files[package], package)):
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

        time1 = time()

        """
        import cProfile
        profile = cProfile.Profile()
        profile.enable()
        #"""

        globalTarget = target

        didCompile = False

        def compile(target, sources, filenames, former = None):
            lexed = Lexer.lex(sources, filenames, files, hotswap, cache.lexed if cache else {})

            declarations = Parser.Parser(lexed, filenames)
            declarations.hotswap = False
            declarations.shouldCompile = {}
            declarations.atoms = 0
            declarations.atomTyp = False
            declarations.outputFile = outputFile
            declarations.jsFiles = clientLinkWithFiles + linkWithFiles + linkCSSWithFiles + nodeLinkWithFiles

            if cache:
                declarations.scope = cache.scope
                declarations.interfaces = cache.interfaces
                declarations.structs = cache.structs
                declarations.hotswap = hotswap
                declarations.allImports = cache.allImports
                declarations.atomTyp = cache.atomTyp

            if former:
                #print("inserting", target)
                ResolveSymbols.insert(former, declarations, only= True, copy= True)
                #print(declarations.scope["_global"])

            declarations.files = files
            declarations.lexed = lexed
            declarations.filenames = filenames
            declarations.opt = opt
            declarations.compiled = {}
            declarations.externFuncs = {"main": []}
            declarations.filenames_sources = filenames_sources
            declarations.global_target = target
            declarations.didCompile = False

            ResolveSymbols.resolve(declarations)

            #print("declarations")

            #print(declarations.shouldCompile)

            if opt == 3 or doc or (dev and run) or ImportParser.shouldCompile(False, "main", declarations):
                parser = Parser.Parser(lexed["main"], filenames["main"])
                parser.package = "main"
                ResolveSymbols.insert(declarations, parser, only= True)

                parser.files = files
                parser.global_target = target
                parser.lexed = lexed
                parser.filenames = filenames
                parser.compiled = declarations.compiled
                parser.compiled["main"] = None
                parser.dev = dev

                parsed = parser.parse()

                parser.compiled["main"] = (True, (parsed, []))

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

                for i in parser.compiled:
                    if parser.compiled[i][0]:
                        CodeGen.CodeGen(i, parser.compiled[i][1][0], parser.compiled[i][1][1], target, opt).compile(opt=opt)

                #print(dill.detect.badobjects(parser.scope))

                print("\n======== recompiling =========")
                print("Compilation took : " + str(time() - time1))

                if target == "full":
                    _linkCSSWithFiles = linkCSSWithFiles
                    client_linkWithFiles = linkWithFiles + clientLinkWithFiles
                    node_linkWithFiles = linkWithFiles + nodeLinkWithFiles

                    a = CodeGen.link(parser.compiled, outputFile, hotswap= hotswap, run= False, opt= opt, dev= dev, linkWithCSS= _linkCSSWithFiles, linkWith= client_linkWithFiles, target="client")

                    if run:
                        import webbrowser
                        webbrowser.open("http://127.0.0.1:3000/")

                    l = CodeGen.link(parser.compiled, outputFile, hotswap= hotswap, run= run, opt= opt, dev=dev, linkWithCSS=_linkCSSWithFiles, linkWith= node_linkWithFiles, target = "node")
                else:
                    _linkCSSWithFiles = [] if target != "client" else linkCSSWithFiles
                    _linkWithFiles = linkWithFiles + nodeLinkWithFiles if target == "node" else linkWithFiles + clientLinkWithFiles if target == "client" else []

                    l = CodeGen.link(parser.compiled, outputFile,
                                     run=run, opt=opt, dev=dev, hotswap= hotswap,
                                     linkWithCSS=_linkCSSWithFiles, linkWith=_linkWithFiles, target=target)
                didCompile = True

                parser.didCompile = True

                return parser
            elif run:
                if target == "full":
                    import webbrowser
                    webbrowser.open("http://127.0.0.1:3000/")

                    CodeGen.execNode(outputFile, dev)
                else:
                    if target == "node":
                        CodeGen.execNode(outputFile, dev)
                    else:
                        CodeGen.exec(outputFile)

            return declarations


        fil = filenames
        sour = sources

        c = compile(target, sour, fil)
        return c

    except (EOFError, ArithmeticError) as e:
        if dev:
            Error.error(str(e))
        else:
            print(e, file= sys.stderr)

    if didCompile:
        print("Compilation took : " + str(time() - time1))

    #profile.print_stats("time")

def prepareForHotswap(arg):
    count = 0
    for i in arg:
        if type(i) in [Tree.FuncBody, Tree.FuncBraceOpen, Tree.FuncStart]:
            count += 1
            continue

        if type(i) is Tree.FuncCall and i.nodes[0].type.do:
            print("side effect function")
            return True

        if type(i) is Tree.Create and i.imutable:
            return True

        if not i.isEnd():
            if prepareForHotswap(i) and type(arg) is Tree.Root:
                del i.owner.nodes[count]
                return True
        count += 1

    return False

import datetime
def modified(files, outputfile, jsFiles=[]):
    #return True

    try:
        t = os.path.getmtime("lib/"+outputfile.replace("/", ".")+"-node.js")
        t = datetime.datetime.fromtimestamp(int(t))
    except:
        return True

    for i in jsFiles:
        file = os.path.getmtime(i)
        file = datetime.datetime.fromtimestamp(int(file))

        if file > t:
            return True

    import time
    o = compiled

    #return True #delete after testing

    for i in files:
        joined = os.path.join(i[0], i[1])
        file = os.path.getmtime(joined)
        file = datetime.datetime.fromtimestamp(int(file))

        if file > t:
            return True

    return False
