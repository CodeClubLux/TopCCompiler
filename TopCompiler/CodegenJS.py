__author__ = 'antonellacalvia'

import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import optimization
import os
import copy

class CodeGen:
    def __init__(self, filename, tree, externFunctions, main= True):
        self.tree = tree
        self.filename = filename

        self.out = ""

        self.out_parts = []
        self.main_parts = []

        self.main = ""

        self.externs =externFunctions

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

    def toJSHelp(self, tree= None, isGlobal= True):
        if tree is None:
            tree = self.tree
        out = ""

        tree.res = self.getName()
        tree._name = self.getName()
        tree._context = self.getName()

        #variable declarations
        self.inAFunction = True
        for i in tree.before:
            i.compileToJS(self)
        self.inAFunction = False

        for i in tree:
            i.compileToJS(self)

    def toEvalHelp(self):
        tree = self.tree

        for i in tree.nodes[:-1]:
            i.compileToJS(self)

        from TopCompiler import Types


        if not type(tree.nodes[-1].type) is Types.Null:
            self.append("(")
            tree.nodes[-1].compileToJS(self)
            self.append(").toString()")
        else:
            tree.nodes[-1].compileToJS(self)
            self.append(";")
            self.append("undefined")

    def getName(self):
        return next(self.gen)

    def createName(self, name):
        self.names[-1][name] = self.getName()
        return self.names[-1][name]

    def readName(self, name):
        for i in reversed(self.names):
            try:
                return i[name]
            except:
                pass

    def incrScope(self):
        self.names.append({})

    def decrScope(self):
        self.names.pop()

    def toJS(self, target):
        main = self.filename == "main"

        self.toJSHelp()

        self.out = "".join(self.out_parts)
        self.main = "".join(self.main_parts)

        out = "function "+self.filename+"_"+target+"Init(){var "+self.tree._context+"=0;"+\
            "return function "+self.tree._name+"("+self.tree.res+"){"+\
            "while(1){switch ("+self.tree._context+"){case 0:"+self.main+"return;}}}()}"+\
            self.out

        return out

    def toEval(self):
        main = "main"

        self.toEvalHelp()

        self.out = "".join(self.out_parts)
        self.main = "".join(self.main_parts)

        if self.out == "":
            return self.main
        return self.out + ";" + self.main


    def append(self, value):
        if value is None:
            raise Error.error("expecting type string and got none, internal error")
        if self.inAFunction:
            self.out_parts.append(value)
        else:
            self.main_parts.append(value)

    def inFunction(self):
        self.inAFunction = True
        self._level = copy.copy(self.info.array)
        self._pointer = self.info.pointer

        self.info.reset([0], 0)

    def outFunction(self):
        self.inAFunction = False
        self.info.reset(self._level, self._pointer)

    def compile(self, opt= 0, target="browser"):
        js = self.toJS(target)

        try:
            f = open("lib/"+self.filename.replace("/", ".") + "-" + target + ".js", mode="w")
            f.write(js)
            f.close()
        except:
            Error.error("Compilation failed")

def getRuntime():
    runtimeName = __file__[0:__file__.rfind("/") + 1] + "runtime.js"
    file = open(runtimeName, mode="r")
    return file.read()

def getRuntimeNode():
    runtimeName = __file__[0:__file__.rfind("/") + 1] + "runtime_node.js"
    file = open(runtimeName, mode="r")
    return file.read()

def link(filenames, output, run, opt, dev, linkWith, linkWithCSS, target):
    linked = '"use strict";'
    import sys
    runtime = getRuntime() if target == "browser" else getRuntimeNode()

    if target == "full":
        runtime = ""
    linked += runtime


    #print("====", target)
    for i in linkWith + (["bin/"+output+"-full.js"] if target != "full" else []):
        try:
            f = open(i, mode="r")
        except:
            f.close()

            Error.error("cannot find file "+i+" to link")
        linked += f.read()
        f.close()

    css = ""

    for i in linkWithCSS:
        try:
            f = open(i, mode="r")
        except:
            f.close()

            Error.error("cannot find file "+i+" to link")
        css += "<style>"+f.read()+"</style>"
        f.close()

    linked += "\n"

    for i in filenames:
        f = open("lib/"+i.replace("/", ".") +  "-" + target + ".js", mode="r")
        linked += f.read()
        f.close()

    fjs = open("bin/"+ output + "-" + target + ".js", mode="w")

    preCall = linked
    linked += "main_" + target + "Init();"

    if target == "node":
        fjs.write(linked)
        fjs.close()

        if dev:
            return preCall
        if run:
            execNode(output)
        return

    if target == "full":
        fjs.write(linked)
        fjs.close()
        return linked

    f = open("bin/" + output + ".html", mode="w")

    html = """<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN"><HTML><HEAD><meta charset="UTF-8"><TITLE>""" + output + """</TITLE></HEAD><script>""" + linked + """</script></HTML>"""

    if opt == 0:
        html = """
<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML>
    <HEAD>
        <meta charset="UTF-8">
        <TITLE>""" + output + """</TITLE>
        <link rel="shortcut icon" href="/Users/luke/Desktop/arrow.ico" />
        """+css+"""
    </HEAD>
    <body>
        <div id= "code"></div>
        <script>
        """ +linked + """
        </script>
    </body>


</HTML>"""

    f.write(html)
    fjs.write(preCall)

    f.close()
    fjs.close()

    if dev:
        return preCall

    if run: exec(output)

def exec(outputFile):
    args = ["open", "bin/"+outputFile+".html"]
    subprocess.check_call(args, shell=False)

def execNode(outputFile):
    args = ["node", outputFile + "-node.js"]
    subprocess.call(args, shell=False, cwd="bin/")

class Info:
    def __init__(self):
        self.pointer = 0
        self.array = [0]
        
    def reset(self, lastArr, pointer):
        self.array = lastArr
        self.pointer = pointer


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
                info.pointer = len(info.array)-1
            else:
                info.pointer -= 1
                info.array[info.pointer] += 1
        elif info.pointer != len(info.array)-1:

            yield ("".join((letters[i] for i in info.array)))
            info.pointer += 1
            info.array[info.pointer] += 1
        else:

            yield ("".join((letters[i] for i in info.array)))
            info.array[info.pointer] += 1