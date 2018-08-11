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
            typ = self.varType.toCType()
            codegen.append(typ + " " + codegen.createName(self.package+"_"+self.name, typ))
            return


        inFunc = codegen.inAFunction

        if self.attachTyp:
            codegen.out_parts.append(self.varType.toCType() + " " + self.attachTyp.package + "_" + self.attachTyp.normalName + "_" + self.name + ";")
        elif not self.isGlobal:
            typ = self.varType.toCType()
            codegen.append(typ + " " + codegen.createName(self.package + "_" + self.name, typ) + ";")
        else:
            if self.extern:
                if self.varType.isType(Types.FuncPointer):
                    codegen.out_parts.append(f"\n#define {self.package}_{self.name}(")
                    names = [codegen.getName() for i in range(len(self.varType.args)+1)]
                    codegen.out_parts.append(",".join(names))
                    codegen.out_parts.append(") ")
                    self.names = names
                else:
                    codegen.out_parts.append(f"\n#define {self.package}_{self.name} ")
            else:
                codegen.out_parts.append(self.varType.toCType() + " " + self.package + "_" + self.name + ";")

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

        if self.extern and self.nodes[0].name == "_":
            tmp = self.nodes[1].nodes[0].string.replace("\{", "{").replace("\}", "}")
            tmp = tmp[1:-1]
            codegen.out_parts.append(tmp)
            return
        elif self.nodes[0].name == "_":
            self.nodes[1].nodes[0].compileToC(codegen)
            return

        self.nodes[0].compileToC(codegen)
        self.nodes[1].compileToC(codegen)

        self = self.nodes[0]
        if self.attachTyp:
            attachTyp = self.attachTyp

    def validate(self, parser): pass

def canMutate(self, tryingToMutate):
    def getReadVar(node):
        i = node
        if type(i) is Tree.FuncCall:
            return

        if not type(i) in [Tree.Field, Tree.ArrRead, Tree.ReadVar, Tree.Tuple] and not (type(i) is Tree.Operator and i.kind in ["*", "&"]):
            i.error("expecting variable")

        if type(node) is Tree.ReadVar:
            return node
        for i in node.nodes:
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

    if readVar:
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
                create = self.owner.nodes[0]
                tmp = self.nodes[0].string.replace("\{", "{").replace("\}", "}")
                tmp = tmp[1:-1]
                if create.varType.isType(Types.FuncPointer):
                    codegen.out_parts.append(tmp)
                    codegen.out_parts.append("(")
                    iter = 0
                    for i in create.names[:-1]:
                        iter += 1
                        codegen.out_parts.append(i)
                        if iter + 1 < len(create.names):
                            codegen.out_parts.append(",")
                    codegen.out_parts.append(")")
                else:
                    codegen.out_parts.append(tmp)
                codegen.out_parts.append("\n")
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

def getVar(self, codegen):
    return codegen.readName(
            self.package + "_" + self.name) if not self.isGlobal else \
            (self.package+"_"+self.name if self.package != "" else "_global_" + self.name
        )

class ReadVar(Node):
    def __init__(self, name, isGlobal, parser):
        Node.__init__(self, parser)
        self.name = name
        self.isGlobal = isGlobal
        self.replaced = {}

    def __str__(self):
        return "read " + self.name

    def compileToC(self, codegen):
        if type(self.type) is Types.Enum:
            self.type.toCType()

        if self.package == "": self.package = "_global"
        if self.name == "context" and self.package in ["_global"]:
            return codegen.append(codegen.getContext())
        codegen.append(getVar(self, codegen))

    def validate(self, parser):
        pass