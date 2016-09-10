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
    "link": []
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

    file.write("""
{
    "name": \"""" + port["name"] + """\",
    "version": """+str(port["version"]) + """,
    "link": """+str(port["link"]+[name]) + """,
}
    """)

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

def getCompilationFiles():
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

            file[package] = []

            try:
                port = open("src/"+package+"/port.json", mode= "r")
            except:
                Error.error("missing file port.json in package "+package+"")

            try:
                j = json.loads(port.read())
                files = j["files"]
            except KeyError:
                Error.error("missing property files in file "+package+"port.json")

            for name in files:
                file[package].append((root, name+".top"))

            if root[0].lower() != root[0]:
                Error.error("package name must be lowercase")
        return file

    return getCompFiles("src/")

compiled = []

error = ""

def start(run= False, dev= False, init= False):
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

        files = getCompilationFiles()
        allfilenames = []
        allsources = []

        sources = {}
        filenames = {}

        for c in files:
            sources[c] = []
            filenames[c] = []
            for i in files[c]:
                try:
                    file = open(os.path.join(i[0], i[1]), mode="r")
                    r = file.read()
                    allsources.append(r)
                    sources[c].append(r)

                    if i[1][0].upper() == i[1][0]:
                        Error.error("file name must be lowercase")

                    filenames[c].append((c, i[1][:-4]))
                    allfilenames.append((c, i[1][:-4]))

                    file.close()
                except FileNotFoundError:
                    Error.error("file " + i[1] +", not found")

        if outputFile == "":
            port = open("src/port.json")

            data = port.read()
            outputFile = (json.loads(data)["name"])
            port.close()

        if filenames == []:
            Error.error("no input files")

        """
        import cProfile

        profile = cProfile.Profile()
        profile.enable()
        """

        time1 = time()

        # print ("============= Compiling ==============\n")

        """
        for i in lexed:
            print(i.token+"_"+i.type)
        """

        lexed = Lexer.lex(sources, filenames)
        #print("lexed")

        declarations = Parser.Parser(lexed, filenames)
        declarations.files = files
        declarations.lexed = lexed
        declarations.filenames = filenames
        declarations.opt = opt
        declarations.compiled = {}
        declarations.externFuncs = {"main": []}

        ResolveSymbols.resolve(declarations)

        #print("declarations")

        if ImportParser.shouldCompile(False, "main", declarations):
            parser = Parser.Parser(lexed["main"], filenames["main"])
            ResolveSymbols.insert(declarations, parser, only= True)

            parser.files = files
            parser.lexed = lexed
            parser.filenames = filenames
            parser.compiled = declarations.compiled
            parser.compiled["main"] = None

            parsed = parser.parse()

            parser.compiled["main"] = (True, (parsed, parser.externFuncs["main"]))

            import AST as Tree
            allCode = Tree.Root()

            if opt > 0:
                for d in parser.compiled:
                    allCode.addNode(parser.compiled[d][1][0])
                optimize(allCode, opt)

            #print("parsing")

            for i in parser.compiled:
                if parser.compiled[i][0]:
                    CodeGen.CodeGen(i, parser.compiled[i][1][0], parser.compiled[i][1][1]).compile(opt=opt)

            l = CodeGen.link(parser.compiled, outputFile, run=run, opt= opt, dev= dev)
            print("Compilation took : "+str(time() - time1))
            return (True, l)
        elif run:
            CodeGen.exec(outputFile)
        elif init:
            return (True, open("bin/"+outputFile+".js").read())
        elif dev:
            return (False, "")

        print("Compilation took : "+str(time() - time1))
    except EOFError as e:
        if dev:
            return (False, str(error))
        else:
            print(e, file= sys.stderr)

    #profile.print_stats("time")

import datetime
def modified(files, outputfile):
    import time
    o = compiled

    #return True #delete after testing

    try:
        t = os.path.getmtime("lib/"+outputfile.replace("/", ".")+".js")
        t = datetime.datetime.fromtimestamp(int(t))
    except:
        return True

    for i in files:
        file = os.path.getmtime(os.path.join(i[0], i[1]))
        file = datetime.datetime.fromtimestamp(int(file))

        if file > t:
            return True

    return False