import subprocess
import os
import AST as Tree
from time import *
from TopCompiler import Error

import PostProcessing
import os
import copy

from AST import Func

import subprocess
import collections as coll

runtimeFile = open(os.path.dirname(__file__) + "/runtime/runtime.c", "r")
cRuntimeCode = runtimeFile.read()
runtimeFile.close()

hRuntimeFile = open(os.path.dirname(__file__) + "/runtime/runtime.h", "r")
hRuntimeCode = hRuntimeFile.read()
hRuntimeFile.close()

from TopCompiler import Types

class CodeGen:
    def __init__(self, parser, order_of_modules, filename, tree, externFunctions, target, opt, debug, main=True):
        self.tree = tree
        self.filename = filename
        self.parser = parser

        self.contextType = parser.contextType

        self.opt = opt

        self.out = ""
        self.order_of_modules = order_of_modules

        self.target = target

        self.header_parts = []
        self.out_parts = []
        self.main_parts = []
        self.func_parts = []
        self.func_count = 0
        self.init_types = []

        self.header_parts = []

        self.debug = debug

        self.main = ""

        self.externs = externFunctions

        self.inAFunction = 0
        self.names = [{}]
        self.contexts = []
        self.nameCount = 0

        self.info = Info()
        self.gen = genNames(self.info)

        self.indent = 0

        self.out_scopes = []
        self.count = 0
        self.deferred = []
        self.previousArray = []
        self.previousPointer = []

    def inFunction(self):
        if self.inAFunction == 0:
            self.previousPointer = self.info.pointer
            self.previousArray = list(self.info.array)
        self.inAFunction += 1
        self.func_parts.append([])

    def inHeader(self):
        tmp = self.inAFunction
        self.inAFunction = -1

        return tmp

    def outFunction(self):
        self.inAFunction -= 1
        if self.inAFunction == 0:
            for i in reversed(self.func_parts):
                self.out_parts.extend(i)
            self.func_parts = []
            self.info.array = self.previousArray
            self.info.pointer = self.previousPointer

    def inGenerateFunction(self):
        self.inFunction()

    """ 
    def setInAFunction(self, new):
        raise Exception()
        
        if new > 0:
            self.inAFunction = new + 1
            if self.inAFunction == 0:
                for i in reversed(self.func_parts):
                    self.out_parts.extend(i)
                self.func_parts = []

        else:
            self.outFunction()
    """

    def incrScope(self):
        self.names.append({})

    def getDeferred(self):
        return self.deferred[-1]

    def outputDeferred(self):
        for i in self.getDeferred():
            i()

    def incrDeferred(self):
        self.deferred.append([])

    def decrDeferred(self):
        self.outputDeferred()
        self.deferred.pop()

    def decrScope(self):
        self.names.pop()


    def readName(self, name):
        #return name

        for i in reversed(self.names):
            try:
                return i[name][1]
            except:
                pass

        raise Exception("could not find variable " + name)

    def getParts(self):
        if self.inAFunction > 0:
            return self.func_parts[self.inAFunction - 1]
        elif self.inAFunction == -1:
            return self.header_parts
        else:
            return self.main_parts

    def addSemicolon(self, ast, no_semicolon=False):
        if not type(ast) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
            if no_semicolon:
                self.append("\n")
            else:
                self.append(";\n")
            if self.debug:
                filename = ast.fullFilePath().replace("\\", "\\\\")
                self.append(f'#line {ast.token.line+1} "{filename}.top"\n')

    def createName(self, name, typ):
        self.names[-1][name] = (typ, name)

        return name

    def append(self, value):
        if value is None:
            print("")
        self.getParts().append(value)

    def toCHelp(self, tree=None, isGlobal=True):
        if tree is None:
            tree = self.tree

        self.incrDeferred()

        includes = Types.TmpCodegen()

        for (iter, i) in enumerate(tree):
            if type(i) is Tree.CreateAssign and i.extern and i.nodes[0].name == "_":
                i.compileToC(includes)

        for (iter, i) in enumerate(tree):
            if type(i) is Tree.FuncStart:
                funcStart = i
                funcBrace = i.owner.nodes[iter+1]
                funcBody = i.owner.nodes[iter+2]
                Func.forwardRef(funcStart, funcBrace, funcBody, self)

        for i in tree:
            if type(i) in [Tree.Type, Tree.Enum] or (type(i) is Tree.CreateAssign and i.extern and i.nodes[0].name == "_"): continue
            i.compileToC(self)
            self.addSemicolon(i)

        self.decrDeferred()

        return "".join(includes.out_parts)

    def getName(self):
        return next(self.gen)

    def getContext(self):
        return self.contexts[-1]

    def compile(self, opt):
        self.contexts = ["(&_global_context)"]

        self.parser.package = self.filename
        self.parser.imports = self.parser.allImports[self.filename]
        PostProcessing.simplifyAst(self.parser, self.tree)

        includes = self.toCHelp()

        mainCode = ""


        mainCode += ("".join(self.main_parts))
        outerCode = "".join(self.out_parts)
        forward_ref = "".join(self.header_parts)

        (generatedTypes, mainC) = Types.getGeneratedDataTypes(self.filename)
        Types.compiledTypes = coll.OrderedDict()
        Types.dataTypes = []

        mainC = "".join(self.init_types) + "\n" + mainC

        headerCode = f"{generatedTypes}\n{forward_ref}"
        print_code = "printf(" + '"' + self.filename + '\\n");'
        cCode = f"{outerCode}\nvoid {self.filename}InitTypes() {{ \n {mainC} }}\nvoid {self.filename}Init() {{ \n{mainCode};\n}};"

        #print("To C took :", time() - t)

        f = open("lib/" + self.filename + ".c", mode="w")
        f.write(cCode)
        f.close()

        f = open("lib/" + self.filename + ".h", mode="w")
        f.write(headerCode)
        f.close()

        return includes

class Info:
    def __init__(self):
        self.pointer = 0
        self.array = [0]

    def reset(self, lastArr, pointer):
        self.array = lastArr
        self.pointer = pointer

def buildContext(parser):
    from TopCompiler import Parser

    contextType = parser.contextType
    # build context data type
    context = "_global_context"
    typesGeneratedByContext = ""

    from TopCompiler import Parser
    from TopCompiler import topc

    if type(Parser.IType) is Parser.TmpType:
        topc.global_parser.setTypeIntrospection()

    Parser.PointerType.toCType()

    types = {}
    for field in contextType:
        t = contextType[field]
        if t.package in parser.structs:
            types[field] = t.toCType()

    string = []
    (typesGen, mainC) = Types.getGeneratedDataTypes("_context")

    parser.typesInContext = list(Types.genericTypes.keys())

    Types.compiledTypes = coll.OrderedDict()
    Types.dataTypes = []

    string.append(typesGen)

    string.append("struct _global_Context {\n")
    for field in contextType:
        string.append(f"{types[field]} {field};")
    string.append("};\n")

    string.append(f"struct _global_Context {context};")

    return ("".join(string), mainC)

import os



def link(compiled, outputFile, includes, opt, hotswap, debug, linkWith, headerIncludePath, target, dev, context, runtimeBuild, to_obj): #Add Option to change compiler
    print(compiled)
    topRuntime = ""
    (context, mainC) = context
    if not runtimeBuild:
        topRuntime = open(os.path.dirname(__file__) + "/runtime/runtimeTop.c")

        topRuntime = topRuntime.read()

    includes = "".join(includes)

    linkedCode = [includes, hRuntimeCode,  context, cRuntimeCode, topRuntime, "struct _global_Context _global_context;"]

    for c in compiled:
        f = open("lib/" + c + ".h", mode="r")
        linkedCode.append(f.read())
        f.close()

    for c in compiled:
        f = open("lib/" + c + ".c", mode="r")
        linkedCode.append(f.read())
        f.close()

    print_size = 'printf("offset of cases %llu, %llu", sizeof(struct ecs_Slot_model_ModelRenderer), sizeof(struct model_ModelRenderer)); return 0;'
    linkedCode.append(f"int main() {{ \n_globalInitTypes(); _globalInit(); _global_init_c_runtime(); \n {mainC}; \n mainInitTypes(); mainInit(); return 0;  }};")

    f = open("bin/" + outputFile + ".c", mode="w")
    f.write("\n".join(linkedCode))
    f.close()

    clang_commands = ["clang",  "bin/" + outputFile + ".c"]

    #linkWith.append("C:\\Program Files (x86)\Windows Kits\\10\Lib\\10.0.17134.0\\um\\x64\\.lib")

    for i in linkWith:
        clang_commands.append(i)

    for i in headerIncludePath:
        clang_commands.append("-iwithprefix")
        clang_commands.append(i)

    """
    glfw3.lib;
    opengl32.lib;
    kernel32.lib;
    user32.lib; 
    gdi32.lib;
    winspool.lib;
    shell32.lib;
    ole32.lib;
    oleaut32.lib;
    uuid.lib;
    comdlg32.lib;
    advapi32.lib;
    glfw3.lib
    """

    if debug:
        debug = ["-g", "-gcodeview", "-O" + str(opt)]
    else:
        debug = ["-O" + str(opt)] #["-g",  "-gcodeview"]

    if to_obj:
        clang_commands += [ "-c", "-o", "bin/" + outputFile + ".o"] + debug + ["-Wno-incompatible-pointer-types", "-Wno-visibility",  "-Wno-return-type", "-Wno-unused-value"]
    else:
        clang_commands += [ "-o", "bin/" + outputFile + ".exe"] + debug + ["-Wno-incompatible-pointer-types", "-Wno-visibility",  "-Wno-return-type", "-Wno-unused-value"]

    print(" ".join(clang_commands),"\n")
    try:
        subprocess.check_call(clang_commands)
    except:
        Error.error("\nC code failed to compile")

def exec(outputFile):
    try:
        subprocess.check_call(["./bin/"+outputFile + ".exe"])
    except subprocess.CalledProcessError as e:
        Error.error(e)

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
            #info.pointer += 1
            info.array[info.pointer] += 1
        else:

            yield ("".join((letters[i] for i in info.array)))
            info.array[info.pointer] += 1

global_info = Info()
global_gen = genNames(global_info)

def genGlobalTmp(package):
    tmp = global_gen.__next__()

    return "tmp"+package + tmp

