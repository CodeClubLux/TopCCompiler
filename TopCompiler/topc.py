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
        Error.error("directory has no source folder")

def getCompilationFiles(target):
    try:
        proj = open("src/port.json", mode="r")
        proj.close()
    except:
        Error.error("missing port.json in source folder")

    def getCompFiles(dir= ""):
        file = {}

        for root, dirs, files in os.walk(dir, topdown=False):
            package = root
            if package == "src/": continue
            package = package[len("src/"):]

            file[package] = {"client": [], "full": [], "node": []}

            try:
                port = open("src/"+package+"/port.json", mode= "r")
            except:
                Error.error("missing file port.json in package "+package+"")

            files = []
            try:
                j = json.loads(port.read())
                files.append((target, j["files"]))
            except KeyError:
                pass
            except json.decoder.JSONDecodeError as e:
                Error.error("In file port.json, in directory "+package+", "+str(e))


            if "client-files" in j and (target in ["full", "client"]):
                files.append(("client", j["client-files"]))
            if "node-files" in j and (target in ["full", "node"]):
                files.append(("node", j["node-files"]))

            if len(files) == 0:
                Error.error("no compilation files are specified in package "+ package + "/port.json")

            for f in files:
                for name in f[1]:
                    file[package][f[0]].append((root, name+".top"))

            if root[0].lower() != root[0]:
                Error.error("package name must be lowercase")
        return file

    return getCompFiles("src/")

compiled = []

error = ""



def start(run= False, dev= False, init= False, hotswap= False, cache= False):
    global outputFile

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

        port = open("src/port.json")
        data = port.read()
        jsonLoad = json.loads(data)

        port.close()

        def handleOptions(names):
            t = ()
            for i in names:
                t += (jsonLoad[i] if i in jsonLoad else [],)
            return t

        (linkCSSWithFiles, linkWithFiles, clientLinkWithFiles, nodeLinkWithFiles) = handleOptions(["linkCSS", "linkWith", "linkWith-client", "linkWith-node"])

        try:
            target = jsonLoad["target"]
            if not target in ["client", "node", "full"]:
                Error.error("In global port.json file: unknown compile target, " + target)
        except KeyError:
            Error.error("must specify compilation target in port.json file")

        files = getCompilationFiles(target)
        allfilenames = []
        allsources = []

        sources = {}
        filenames = {}

        filenames = {"client": {}, "full": {}, "node": {}}
        sources = {"client": {}, "full": {}, "node": {}}

        for c in files:
            for _i in files[c]:
                filenames[_i][c] = []
                sources[_i][c] = []

                def iterate(i):
                    try:
                        file = open(os.path.join(i[0], i[1] ), mode="r")
                        r = file.read()
                        allsources.append(r)

                        sources[_i][c].append(r)

                        if i[1][0].upper() == i[1][0]:
                            Error.error("file name must be lowercase")

                        filenames[_i][c].append((c, i[1][:-4]))
                        allfilenames.append((c, i[1][:-4]))

                        file.close()
                    except FileNotFoundError:
                        Error.error("file " + i[1] +", not found")

                for i in files[c][_i]:
                    iterate(i)

        if outputFile == "":
            outputFile = (jsonLoad["name"])

        global filenames_sources

        filenames_sources = {i: {} for i in sources["full"]}

        for _target in filenames:
            for package in filenames[_target]:
                for i, c in enumerate(filenames[_target][package]):
                    filenames_sources[package][c[1]] = sources[_target][package][i]

        if not "main" in filenames_sources:
            Error.error("Project must have a main package, from where to start the code for the client")

        time1 = time()

        """
        import cProfile
        profile = cProfile.Profile()
        profile.enable()
        #"""

        globalTarget = target

        class T:
            pass

        x = T()
        x.didCompile = False

        def compile(target, sources, filenames, former = None):
            lexed = Lexer.lex(sources, filenames)

            declarations = Parser.Parser(lexed, filenames)
            declarations.hotswap = False
            declarations.shouldCompile = {}
            declarations.atoms = 0
            declarations.atomTyp = False

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

            ResolveSymbols.resolve(declarations)

            #print("declarations")

            #print(declarations.shouldCompile)

            if (dev and run) or ImportParser.shouldCompile(False, "main", declarations):
                print("\n======== recompiling =========")
                parser = Parser.Parser(lexed["main"], filenames["main"])
                ResolveSymbols.insert(declarations, parser, only= True)

                parser.files = files
                parser.global_target = target
                parser.lexed = lexed
                parser.filenames = filenames
                parser.compiled = declarations.compiled
                parser.compiled["main"] = None

                parsed = parser.parse()

                parser.compiled["main"] = (True, (parsed, parser.externFuncs["main"]))

                import AST as Tree
                allCode = Tree.Root()

                """
                if opt > 0:
                    for d in parser.compiled:
                        allCode.addNode(parser.compiled[d][1][0])
                    optimize(allCode, opt)
                """

                #print("parsing")

                for i in parser.compiled:
                    if parser.compiled[i][0]:
                        CodeGen.CodeGen(i, parser.compiled[i][1][0], parser.compiled[i][1][1], target).compile(opt=opt)

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
                x.didCompile = True
                return parser
            elif run:
                if target == "full":
                    if run:
                        import webbrowser
                        webbrowser.open("http://127.0.0.1:3000/")

                    CodeGen.execNode(outputFile, dev)
                else:
                    CodeGen.exec(outputFile)


            return declarations


        fil = filenames[target]
        sour = sources[target]

        return compile(target, sour, fil)

    except EOFError as e:
        if dev:
            Error.error(str(e))
        else:
            print(e, file= sys.stderr)

    if x.didCompile:
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
def modified(files, outputfile):
    import time
    o = compiled

    #return True #delete after testing

    try:
        t = os.path.getmtime("lib/"+outputfile.replace("/", ".")+"-node.js")
        t = datetime.datetime.fromtimestamp(int(t))
    except:
        return True

    for i in files["full"]:
        file = os.path.getmtime(os.path.join(i[0], i[1]))
        file = datetime.datetime.fromtimestamp(int(file))

        if file > t:
            return True

    return False