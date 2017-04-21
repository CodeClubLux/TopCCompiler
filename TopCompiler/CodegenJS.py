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
    def __init__(self, filename, tree, externFunctions, target, opt, main=True):
        self.tree = tree
        self.filename = filename

        self.opt = opt

        self.out = ""

        self.out_parts = []
        self.main_parts = []

        self.global_target = target
        self.target = target

        self.client_out_parts = []
        self.client_main_parts = []

        self.node_out_parts = []
        self.node_main_parts = []

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

    def toJSHelp(self, tree=None, isGlobal=True):
        if tree is None:
            tree = self.tree
        out = ""

        tree.res = self.getName()
        tree._name = self.getName()
        tree._context = self.getName()

        # variable declarations
        self.inAFunction = True
        for i in tree.before:
            self.target = i.global_target
            i.compileToJS(self)
        self.inAFunction = False

        for i in tree:
            self.target = i.global_target
            i.compileToJS(self)
            if not type(i) in [Tree.FuncCall,Tree.If,Tree.Match,Tree.FuncBody,Tree.Create,Tree.Assign,Tree.CreateAssign,Tree.Tree.FuncBraceOpen,Tree.FuncStart] and i.type.name == "none":
                self.append(";")

    def toEvalHelp(self):
        tree = self.tree

        tree.res = self.getName()
        tree._name = self.getName()
        tree._context = self.getName()

        for i in tree.nodes[:-1]:
            i.compileToJS(self)

        from TopCompiler import Types
        import AST

        if AST.yields(tree.nodes[-1]):
            tree.nodes[-1].compileToJS(self)
            self.append(";reply(" + tree.res + ", '" + str(tree.nodes[-1].type) + "')")
            self.append(";return;")
        elif not type(tree.nodes[-1].type) is Types.Null:
            self.append(";reply(")
            tree.nodes[-1].compileToJS(self)
            self.append(", '" + str(tree.nodes[-1].type) + "')")
            self.append(";return")
        else:
            tree.nodes[-1].compileToJS(self)
            self.append("reply(undefined, 'none')")

    def getName(self):
        return next(self.gen)

    def createName(self, name):
        if self.opt == 0:
            self.names[-1][name] = name
            return name
        else:
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

    def toJS(self, _target):
        def _compile(out, main, target):
            return "function " + str(self.filename) + "_" + target + "Init(){var " + self.tree._context + "=0;" + \
                   "return function " + self.tree._name + "(" + self.tree.res + "){" + \
                   "while(1){switch (" + self.tree._context + "){case 0:" + main + ";return;}}}()}" + \
                   out

        if _target == "full":
            main = self.filename == "main"

            self.toJSHelp()

            self.node_out = "".join(self.node_out_parts)
            self.node_main = "".join(self.node_main_parts)

            self.client_out = "".join(self.client_out_parts)
            self.client_main = "".join(self.client_main_parts)

            return (
            _compile(self.node_out, self.node_main, "node"), _compile(self.client_out, self.client_main, "client"))
        else:
            main = self.filename == "main"

            self.toJSHelp()

            self.out = "".join(self.out_parts)
            self.main = "".join(self.main_parts)

            return _compile(self.out, self.main, self.global_target)

    def toEval(self):
        main = "main"

        self.toEvalHelp()

        self.out = "".join(self.out_parts)
        self.main = "".join(self.main_parts)

        out = self.out
        main = self.main

        result = out + "(function(){var " + self.tree._context + "=0;" + \
                 "return function " + self.tree._name + "(" + self.tree.res + "){" + \
                 "while(1){switch (" + self.tree._context + "){case 0:" + main + ";return;}}}()}" + \
                 ")();"

        return result

    def append(self, value):
        if value is None:
            raise Error.error("expecting type string and got none, internal error")

        if self.target == self.global_target:
            if self.global_target == "full":
                if self.inAFunction:
                    self.client_out_parts.append(value)
                    self.node_out_parts.append(value)
                else:
                    self.client_main_parts.append(value)
                    self.node_main_parts.append(value)
            else:
                if self.inAFunction:
                    self.out_parts.append(value)
                else:
                    self.main_parts.append(value)
        elif self.target == "client":
            if self.inAFunction:
                self.client_out_parts.append(value)
            else:
                self.client_main_parts.append(value)
        elif self.target == "node":
            if self.inAFunction:
                self.node_out_parts.append(value)
            else:
                self.node_main_parts.append(value)
        elif self.target == "full":
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

    def compile(self, opt=0):
        target = self.global_target

        if target == "full":
            (node, client) = self.toJS(target)

            try:
                f = open("lib/" + self.filename.replace("/", ".") + "-node.js", mode="w")
                f.write(node)
                f.close()
            except:
                Error.error("Compilation failed")

            try:
                f = open("lib/" + self.filename.replace("/", ".") + "-client.js", mode="w")
                f.write(client)
                f.close()
            except:
                Error.error("Compilation failed")
        else:
            js = self.toJS(target)

            try:
                f = open("lib/" + self.filename.replace("/", ".") + "-"+ target +".js", mode="w")
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


def link(filenames, output, run, opt, dev, linkWith, linkWithCSS, target, hotswap):
    needSocket = False

    if target == "client" and dev:
        terminal = open(__file__[0:__file__.rfind("/") + 1] + "terminal/bundle.html").read()

        needSocket = True
        linked = ""
        socket = ""
    else:
        linked = ""

    if opt == 3:
        linked = "(function(){"

    import sys

    runtime = "" if hotswap and target == "client" else getRuntime() if target == "client" else getRuntimeNode()

    linked += runtime

    if target == "client" and dev:
        linked += """log= function(d) {
            terminal.echo(d);
        };

        log_unop = function(data, next) {
            terminal.echo(data);
            next();
        };

        function newAtom(arg) {
            previousState = {
                unary_read: unary_read,
                op_set: op_set,
                arg: arg,
                watch: atom_watch,
                events: [],
                toString: function(){ return "" }
            }

            calledBy.push("init -> ");
            recordNewValue(arg, function(){});

            previousState.events.push(recordNewValue);

            return previousState
        }
        """

    array = []
    # print("====", target)
    for i in linkWith:
        try:
            f = open(i, mode="r")
        except:
            f.close()

            Error.error("cannot find file " + i + " to link")
        array.append(f.read())
        f.close()

    linked += ";".join(array)
    css = ""

    if target == "client":
        for i in linkWithCSS:
            try:
                f = open(i, mode="r")
            except:
                f.close()

                Error.error("cannot find file " + i + " to link")
            css += '<style id="' + i + '">' + f.read() + "</style>"
            f.close()

    linked += "\n"

    for i in filenames:
        f = open("lib/" + i.replace("/", ".") + "-" + target + ".js", mode="r")
        linked += f.read()
        f.close()

    fjs = open("bin/" + output + "-" + target + ".js", mode="w")

    preCall = linked
    linked += "main_" + target + "Init();"
    if opt == 3:
        linked += "})()"

    #import jsbeautifier
    #linked = jsbeautifier.beautify(linked)

    fjs.write(linked)
    fjs.close()

    if opt == 3 and target == "client":
        #args = ["uglifyjs", "--noerr", "--warn" "--compress", "unused,dead_code", "--output", output + ".min-" + target + ".js", "--mangle", "--",
        #      output + "-" + target + ".js"]

        args = ["closure-compiler", "--js", "EC-client.js", "--js_output_file", "EC.min-client.js", "--warning_level", "QUIET", "--compilation_level", "ADVANCED"]

        subprocess.check_call(args, shell=False, cwd="bin")
        output += ".min"
        linked = open("bin/" + output + "-" + target + ".js", "r").read()

    if target == "node":
        if run:
            execNode(output, dev)
        return

    if target == "full":
        return linked

    if opt == 3:
        output = output[:-len(".min")]

    f = open("bin/" + output + ".html", mode="w")

    html = """
<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML>
    <head>
        <meta charset="UTF-8">
        <TITLE>""" + output + """</TITLE>
        <link rel="icon" href="favicon.ico" type="image/x-icon" />
        """ + css + """
    </head>
    <body>
        """ + ('<div id="container" style="padding-top: 50px; margin-top: -10px; padding-bottom: 100px; color: white; margin-right: 10px; position: fixed; display: inline-block; float: left; height: 100%; background-color: black; width: 30%;"><button id="switchMode" style="position: fixed; color: black; z-index: 100000; top: 20; margin-left: 10px;so">Time Travel</button><div id="terminal" style="position: fixed; width: inherit; height: 90%;"></div></div><div id= "code" style= "float: right; width: 70%; position: relative;"></div>' if needSocket else '<div id= "code"></div>') + """
        """+('<script>' + socket + "</script>"+terminal if needSocket else '') + """
        <script>
        """ + linked + """
        </script>
    </body>
</HTML>"""

    f.write(html)

    f.close()
    fjs.close()

    if run: exec(output)


def exec(outputFile):
    args = ["open", "bin/" + outputFile + ".html"]
    subprocess.check_call(args, shell=False)

def execNode(outputFile, dev):
    if dev:
        args = ["node", outputFile + "-node.js"]

        subprocess.Popen(args, cwd="bin/")
    else:
        args = ["node", outputFile + "-node.js"]
        subprocess.call(args, cwd="bin/")

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
