__author__ = 'antonellacalvia'

from .node import *
from .Func import *
from .Struct import *
from TopCompiler import Scope
import AST as Tree

class Create(Node):
    def __init__(self, name, varType, parser):
        Node.__init__(self, parser)
        self.name = name
        self.names = []

        self.varType = varType
        self.isGlobal = False
        self.extern = False
        self.escapes = False
        self.attachTyp = False

    def __str__(self):
        return self.name + ": "+str(self.varType)

    def compileToC(self, codegen):
        if type(self.name) is Tree.PlaceHolder:
            for i in self.names:
                self.name = i
                self.compileToC(codegen)
            return

        if type(self.owner) is FuncBraceOpen:
            codegen.append(self.varType.toCType() + " " + codegen.createName(self.package+"_"+self.name))
            return

        inFunc = codegen.inAFunction

        if self.attachTyp:
            codegen.inAFunction = True

            codegen.append(self.varType.toCType() + " " + self.attachTyp.package + "_" + self.attachTyp.normalName + "_" + self.name + ";")
            codegen.inAFunction = inFunc
        elif not self.isGlobal:
            codegen.append(self.varType.toCType() + " " + codegen.createName(self.package + "_" + self.name) + ";")
        else:
            codegen.inAFunction = True
            if self.extern:
                codegen.append(f"\n#define {self.package}_{self.name} ")
            else:
                codegen.append(self.varType.toCType() + " " + self.package + "_" + self.name + ";")
            codegen.inAFunction = inFunc

    def validate(self, parser): pass

class CreateAssign(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.names = []
        self.extern = False

    def __str__(self):
        return "CreateAssign "

    def compileToC(self, codegen):
        create = self.nodes[0]

        self.nodes[0].extern = self.extern

        self.nodes[0].compileToC(codegen)
        self.nodes[1].compileToC(codegen)

        self = self.nodes[0]
        if self.attachTyp:
            attachTyp = self.attachTyp

    def validate(self, parser): pass

def canMutate(self, tryingToMutate):
    def getReadVar(node):
        for i in node:
            if type(i) is Tree.ReadVar:
                return i

            if not type(i) in [Tree.Field, Tree.ArrRead, Tree.ReadVar]:
                i.error("expecting variable")

            if len(i.nodes) > 0:
                return getReadVar(i)

    readVar = getReadVar(self)

    def checkIfImutable(node, createTyp):
        iter = 0
        for i in node:
            isMutable = not readVar.imutable
            if type(node.nodes[0].type) is Types.Pointer:
                createTyp = node.nodes[0].type
            elif tryingToMutate:
                if not isMutable:
                    self.nodes[0].error(
                        "Immutable variable " + readVar.name + ": cannot mutate an immutable variable")

            return
    checkIfImutable(self, readVar.type)

class Assign(Node):
    def __init__(self, name, parser):
        Node.__init__(self, parser)
        self.name = name
        self.isGlobal = None
        self.extern = False

    def __str__(self):
        return self.name + "="

    def compileToC(self, codegen):
        if type(self.owner) is Tree.InitStruct:
            self.nodes[1].compileToC(codegen)
            return
        elif self.init:
            if type(self.name) is Tree.PlaceHolder:
                name = codegen.getName()
            else:
                name = self.package+"_"+self.name if self.isGlobal else codegen.readName(self.package + "_" + self.name)

            if self.extern:
                func = codegen.inAFunction
                codegen.inAFunction = True
                tmp = self.nodes[0].string.replace("\{", "{").replace("\}", "}")
                codegen.append(tmp[1:-1])
                codegen.append("\n")

                codegen.inAFunction = func
            else:
                codegen.append(name + " = ")
                self.nodes[0].compileToC(codegen)
                codegen.append(";")

            if type(self.name) is Tree.PlaceHolder:
                pattern = self.name

                print("object destructuring isnt supported yet")
                def gen(tmp, p):
                    if type(p) is Tree.Tuple:
                        for (index, i) in enumerate(p):
                            gen(tmp + "[" + str(index) + "]", i)
                    elif type(p) is Tree.InitStruct:
                        for i in p:
                            if type(i) is Tree.Assign:
                                gen(tmp+"."+i.nodes[0].name, i.nodes[1])
                            else:
                                gen(tmp + "."+i.name, i)
                    elif type(p) is Tree.ReadVar:
                        if not p.isGlobal:
                            name = codegen.readName(self.package + "_" + p.name)
                        else:
                            name = self.package+"_"+p.name

                        codegen.append(name + "=" + tmp + ";")

                gen(name, pattern.nodes[0])
                return
        else:
            self.nodes[0].compileToC(codegen)
            codegen.append("=")
            self.nodes[1].compileToC(codegen)
            codegen.append(";")

    def validate(self, parser):
        node = self
        package = self.package

        if type(self.owner) is Tree.InitStruct:
            return

        if self.init:
            self.isGlobal = Scope.isGlobal(parser, self.package, self.name)
            createTyp = self.createTyp
        else:
            varNode = self.nodes[0]
            canMutate(self.nodes[0], True)

        if len(node.nodes) == 0:
           self.error( "expecting expression")
        if self.init:
            if len(node.nodes) > 1:
                self.error( "expecting single expression, not multiple")

            typ = node.nodes[0].type
        else:
            if len(node.nodes) > 2:
                self.error("expecting single expression, not multiple")
            typ = node.nodes[1].type

        if typ == Types.Null():
            self.nodes[0].error("cannot assign nothing")

class ReadVar(Node):
    def __init__(self, name, isGlobal, parser):
        Node.__init__(self, parser)
        self.name = name
        self.isGlobal = isGlobal
        self.replaced = {}

    def __str__(self):
        return "read " + self.name

    def compileToC(self, codegen):
        codegen.append(codegen.readName(
            self.package + "_" + self.name) if not self.isGlobal else
            (self.package+"_"+self.name if self.package != "" else "_global_" + self.name
        ))

    def validate(self, parser):
        pass