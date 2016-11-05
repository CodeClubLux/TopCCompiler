__author__ = 'antonellacalvia'

import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import optimization
import os

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
        self.gen = genNames()

        self.indent = 0

    def toJSHelp(self, tree= None, isGlobal= True):
        if tree is None:
            tree = self.tree
        out = ""

        for i in tree:
            i.compileToJS(self)

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

    def toJS(self):
        main = self.filename == "main"

        self.toJSHelp()

        self.out = "".join(self.out_parts)
        self.main = "".join(self.main_parts)

        out = "function "+self.filename+"_Init(){"""+''+self.main+"""}"""+self.out

        return out

    def append(self, value):
        if self.inAFunction:
            self.out_parts.append(value)
        else:
            self.main_parts.append(value)

    def inFunction(self):
        self.inAFunction = True

    def outFunction(self):
        self.inAFunction = False

    def compile(self, opt= 0):
        js = self.toJS()

        try:

            f = open("lib/"+self.filename.replace("/", ".") + ".js", mode="w")
            f.write(js)
            f.close()
        except:
            Error.error("Compilation failed")

def link(filenames, output, run, opt, dev, linkWith):
    linked = '"use strict";'
    for i in linkWith:
        f = open(i, mode="r")
        linked += f.read()
        f.close()

    linked += "\n"

    for i in filenames:
        f = open("lib/"+i.replace("/", ".")+ ".js", mode="r")
        linked += f.read()
        f.close()

    import sys
    runtimeName = __file__[0:__file__.rfind("/")+1] + "runtime.js"
    file = open(runtimeName, mode= "r")
    runtime = file.read()

    linked += runtime

    fjs = open("bin/"+ output + ".js", mode="w")

    preCall = linked
    linked += "main_Init();"

    if opt == 0: pass

    f = open("bin/" + output + ".html", mode="w")

    html = """<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN"><HTML><HEAD><meta charset="UTF-8"><TITLE>""" + output + """</TITLE></HEAD><script>""" + linked + """</script></HTML>"""

    if opt == 0:
        file.close()

        html = """
<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML>
    <HEAD>
        <meta charset="UTF-8">
        <TITLE>""" + output + """</TITLE>
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

def genNames():
    import string

    def overflow(id):
        return len(letters) <= array[id]

    letters = [i for i in string.ascii_letters if not i.lower() in ('a', 'e', 'i', 'o', 'u')]
    array = [0]
    pointer = 0
    skip = False

    while True:
        if overflow(pointer):
            array[pointer] = 0
            if pointer == 0:
                array = [0] * (len(array) + 1)
                pointer = len(array)-1
            else:
                pointer -= 1
                array[pointer] += 1
        elif pointer != len(array)-1:

            yield ("".join((letters[i] for i in array)))
            pointer += 1
            array[pointer] += 1
        else:

            yield ("".join((letters[i] for i in array)))
            array[pointer] += 1