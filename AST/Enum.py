from .node import *
from TopCompiler import Types
from PostProcessing import SimplifyAst
from TopCompiler import Scope
from TopCompiler import CodeGen

class Enum(Node):
    def __init__(self, const, normalName, parser, generic={}):
        Node.__init__(self, parser)
        self.const = const
        self.package = parser.package
        self.normalName = normalName
        self.generic = generic
        self.onlyGenericName = ""
        self.replaced = False

    def replaceT(self, structT, newName):
        self.package = structT.package
        self.normalName = newName
        self.const = structT.const
        self.onlyGenericName = SimplifyAst.toUniqueID("", "", structT.remainingGen)[1:]
        self.generic = structT.remainingGen
        self.replaced = True
        self.realNormalName = structT.normalName
        self.type = structT

        #Types.replaceT(i, structT.gen) for i in structT.types.values()]

    def compileToC(self, codegen):
        isMaybe = Types.isMaybe(self.type)

        if not self.replaced:
            return

        count = 0
        codegen.inFunction()

        """ 
        struct Maybe_int_Some {
            int value;
        };
        
        union Maybe_int_cases {
            struct Maybe_int_Some some;
        };
        
        struct Maybe_int {
            unsigned short tag;
            union Maybe_int_cases cases;
        };
        """

        if not isMaybe:
            cType = f"struct {self.package}_{self.normalName}"

            for name in self.const:
                args = self.const[name]

                if len(args) > 0:
                    codegen.append(f"struct {self.package}_{self.normalName}_{name} {{\n")
                    names = ["field" + str(iter) for iter in range(len(args))]

                    for i in range(len(args)):
                        if args[i].name == "ui.InputOptions":
                            print("hwat")

                        codegen.append(f"{args[i].toCType()} field{i};\n")
                    codegen.append("\n};")

            numCases = len(self.const)

            tag = ""
            if numCases <= 2:
                tag = "_Bool"
            else:
                sizes = ["char", "short", "int", "long"]
                for (iter, size) in enumerate(sizes):
                    if numCases < 2 ^ ((iter+1) * 8):
                        tag = size
                        break

            tag += " tag;"

            codegen.append(f"union {self.package}_{self.normalName}_cases {{\n")
            for name in self.const:
                if len(self.const[name]) > 0:
                    codegen.append(f"struct {self.package}_{self.normalName}_{name} {name};\n")
            codegen.append("\n};\n")

            codegen.append(f"struct {self.package}_{self.normalName} {{\n")
            codegen.append(f"union {self.package}_{self.normalName}_cases cases;\n{tag}")
            codegen.append("\n};\n")

            index = 0

            for (iter, name) in enumerate(self.const):
                args = self.const[name]
                if len(args) > 0:

                    codegen.append(f"{cType} {self.package}_{name}{self.onlyGenericName}(")
                    vars = [codegen.getName() for i in args + [0]]
                    types = [i.toCType() for i in args]
                    types.append("struct _global_Context*")

                    codegen.append(",".join(a + " " + b for (a,b) in zip(types, vars)))
                    codegen.append("){\n")

                    tmp = codegen.getName()
                    codegen.append(f"{cType} {tmp};\n")

                    for (c, i) in enumerate(vars[:-1]):
                        codegen.append(tmp + ".cases." + name + ".field" + str(c) + " = " + i + ";")
                    codegen.append(f"{tmp}.tag = {iter};\n")
                    codegen.append("return " + tmp + ";}\n")
                    index += 1
                else:
                    noGenericsDefined = True
                    for cName in self.generic:
                        c = self.generic[cName]
                        if not (type(c) is Types.T and (c.owner == self.package+"."+self.normalName if self.package != "_global" else c.owner == self.realNormalName)):
                            noGenericsDefined = False
                            break

                    if not self.generic or noGenericsDefined:
                        codegen.append(f"{cType} {self.package}_{name};\n")

                        codegen.outFunction()
                        alreadyOut = True

                        codegen.append(f"{self.package}_{name}.tag = {iter};")
                        codegen.inFunction()
        else:
            cType = self.type.remainingGen["Maybe.T"].toCType() + "*"

        # Type Introspection
        nameOfI = f"{self.package}_{self.normalName}Type"

        codegen.append("struct _global_StructType " + nameOfI + ";")

        codegen.append(
                    f"struct _global_StructType* {self.package}_{self.normalName}_get_type({cType}* self, struct _global_Context* c)" + "{")
        codegen.append(f"return &{self.package}_{self.normalName}Type;")
        codegen.append("}\n")

        codegen.append(
                    f"struct _global_StructType* {self.package}_{self.normalName}_get_typeByValue({cType} self, struct _global_Context* c)" + "{")
        codegen.append(f"return &{self.package}_{self.normalName}Type;")
        codegen.append("}\n")
        codegen.outFunction()

        fieldTypeInArray = "Field"  # SimplifyAst.sanitize(structType)

        def as_string(s):
            return f'_global_StringInit({len(s)}, "{s}")'


        codegen.append(f"{nameOfI}.fields = _global_StaticArray_StaticArray_S_" + fieldTypeInArray + "Init(NULL, 0);")
        codegen.append(f"{nameOfI}.package = " + as_string(self.package) + ";")
        codegen.append(f"{nameOfI}.name = " + as_string(self.normalName) + ";")

    def validate(self, parser):
        pass

def genFunction(compileNodes, codegen, returnType, owner, self):
    if type(owner) is Tree.FuncBody and owner.nodes[-1] == self:
        compileNodes()
        return

    funcName = CodeGen.genGlobalTmp(codegen.filename)
    inAFunc = codegen.inAFunction
    codegen.inGenerateFunction()

    vars = []
    varNames = []

    for scope in codegen.names[1:]:
        for varName in scope:
            (typ, var) = scope[varName]

            if inAFunc == 1 or (not var.startswith("*")):
                vars.append(f"{typ}* {var},")
                varNames.append("&" + var)
                scope[varName] = (typ, "*" + var)
            else:
                vars.append(f"{typ} {var},")
                varNames.append(var[1:])

    vars = "".join(vars)
    varNames = ",".join(varNames)

    codegen.append(
        f"\nstatic inline {returnType.toCType()} {funcName}({vars} struct _global_Context* {codegen.getContext()}) {{\n")

    codegen.incrScope()
    compileNodes()
    codegen.decrScope()

    if inAFunc == 1:
        for scope in codegen.names[1:]:
            for varName in scope:
                (typ, var) = scope[varName]
                scope[varName] = (typ, var[1:])

    codegen.append("\n}\n")
    codegen.outFunction()

    codegen.append(f"{funcName}({varNames}, {codegen.getContext()})")

class Match(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False
        self.next = ""
        self.ending = ""
        self.guard = False

    def compileToC(self, codegen):
        tmp = codegen.getName()
        self.tmp = tmp
        self.nodes[1].first = True

        codegen.incrScope()

        if not type(self.type) is Types.Null:
            def genNodes():
                codegen.append(f"{self.nodes[0].type.toCType()} {tmp} =")
                self.nodes[0].compileToC(codegen)
                codegen.append(";\n")

                for iter in range(1, len(self.nodes)):
                    self.nodes[iter].compileToC(codegen)

            genFunction(genNodes, codegen, self.type, self.owner, self)
        else:
            codegen.append(f"{self.nodes[0].type.toCType()} {tmp} =")
            self.nodes[0].compileToC(codegen)
            codegen.append(";")
            for iter in range(1, len(self.nodes)):
                self.nodes[iter].compileToC(codegen)
                codegen.addSemicolon(self.nodes[iter], no_semicolon=True)

        codegen.decrScope()

    def validate(self, parser):
        pass

    def __str__(self):
        return "match"

class Fake:
    def __init__(self, codegen, first):
        self.checking = True
        self.check = []
        self.body = []
        self.codegen = codegen
        self.first = first
        self.guard = False

    def getContext(self):
        return self.codegen.getContext()

    def createName(self, a, typ):
        if self.guard:
            return self.codegen.readName(a)
        else:
            return self.codegen.createName(a, typ)

        #return self.codegen.createName(a, typ)

    def getName(self):
        return self.codegen.getName()

    def readName(self, a):
        return self.codegen.createName(a)

    def append(self, string):
        if self.checking:
            self.check.append(string)
        else:
            self.body.append(string)

    def appendToCodegen(self):
        if self.first:
            tmp = "if"
        else:
            tmp = "else if"
        tmp += "("+"".join(self.check)+"){"+"".join(self.body)
        self.codegen.append(tmp)

class MatchCase(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.yielding = False
        self.first = False
        self.incrScope = True

    def compileToC(self, _codegen):
        codegen = Fake(_codegen, self.first)
        codegen.guard = bool(self.owner.guard)

        def loop(node,tmp):
            codegen.checking = True

            if type(node) is Tree.Operator and node.kind == "concat":
                arr = codegen.getName()
                codegen.append(arr+" = new RegExp('")
                names = []

                def iterate(n):
                    if type(n) is Tree.String:
                        codegen.append(n.toString()[1:-1])
                    elif type(n) is Tree.Tuple:
                        codegen.append("(.*)")
                        names.append(n.nodes[0])
                    elif type(n) is Tree.Operator and n.kind == "concat":
                        iterate(n.nodes[0])
                        iterate(n.nodes[1])

                iterate(node)
                codegen.append("').exec(" + tmp + ")")

                codegen.checking = False

                for (index, i) in enumerate(names):
                    if not self.yielding:
                        name = codegen.createName(i.package + "_" + i.name)
                        codegen.append("var ")
                    else:
                        name = codegen.readName(i.package + "_" + i.name)
                    codegen.append(name + "=" + arr + "[" + str(index + 1) + "];")

            elif type(node) is Tree.FuncCall:
                count = list(node.type.const.keys()).index(node.nodes[0].name)
                nameOfCase = node.nodes[0].name

                maybeOptimization = Types.isMaybe(node.type)

                if maybeOptimization:
                    codegen.append(tmp + " != NULL")
                else:
                    codegen.append(tmp + ".tag==" + str(count))

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) != Tree.ReadVar:
                        codegen.append("&&")
                        if maybeOptimization:
                            loop(i, tmp)
                        else:
                            loop(i, f"{tmp}.cases.{nameOfCase}.field{index}")

                codegen.checking = False

                for (index, i) in enumerate(node.nodes[1:]):
                    if type(i) is Tree.ReadVar:
                        typ = node.type.const[nameOfCase][index]
                        name = codegen.createName(i.package + "_" + i.name, typ.toCType())
                        if not self.owner.guard:
                            codegen.append(f"{typ.toCType()} ")

                        codegen.append(f"{name} = ")
                        if maybeOptimization:
                            codegen.append(f"{tmp};\n")
                        else:
                            codegen.append(f"{tmp}.cases.{nameOfCase}.field{index};\n")
            elif type(node) is Tree.Tuple:
                if len(node.nodes) == 1:
                    loop(node.nodes[0], tmp)
                else:
                    codegen.append("(")
                    codegen.checking = True
                    iter = 0
                    for (index, i) in enumerate(node):
                        if not (type(i) is Tree.ReadVar and i.name[0].islower()):
                            if iter > 0:
                                codegen.check.append("&&")
                            loop(i, tmp + "[" + str(index) + "]")
                            iter += 1

                    codegen.check.append(")")
                    codegen.checking = False

                    for (index, i) in enumerate(node):
                        if type(i) is Tree.ReadVar and i.name[0].islower():
                            if not self.yielding:
                                name = codegen.createName(i.package + "_" + i.name)
                                codegen.append("var ")
                            else:
                                name = codegen.readName(i.package + "_" + i.name)
                            codegen.append(name + "=" + tmp + "[" + str(index) + "];")
            elif type(node) is Tree.Array:
                iter = 0
                end = node.nodes[-1] if len(node.nodes) > 0 else False

                ending = False
                if type(end) is Tree.Operator and end.kind == "..":
                    ending = True
                    codegen.append(tmp+".length>"+str(len(node.nodes)-2))
                else:
                    codegen.append(tmp+".length=="+str(len(node.nodes)))

                for (index, i) in enumerate(node):
                    if not (ending and index == len(node.nodes) - 1) and type(i) != Tree.ReadVar:
                        codegen.append("&&")
                        loop(i, tmp + ".get(" + str(index) + ")")
                        iter += 1

                codegen.checking = False

                for (index, i) in enumerate(node):
                    if type(i) is Tree.ReadVar or (type(i) is Tree.Operator and i.kind == ".."):
                        if type(i) is Tree.Operator:
                            i = i.nodes[0]
                        if not self.yielding:
                            name = codegen.createName(i.package + "_" + i.name)
                            codegen.append("var ")
                        else:
                            name = codegen.readName(i.package + "_" + i.name)
                        if ending and index == len(node) - 1:
                            codegen.append(name+"="+tmp + ".slice(" + str(index) + "," + tmp + ".length);")
                        else:
                            codegen.append(name + "=" + tmp + ".get(" + str(index) + ");")

            elif type(node) is Tree.ReadVar:
                count = list(node.type.const.keys()).index(node.name)

                maybeOptimization = Types.isMaybe(node.type)
                if maybeOptimization:
                    codegen.append(tmp + " == NULL")
                else:
                    codegen.append(tmp + ".tag==" + str(count))

                codegen.checking = False
            elif type(node) is Tree.Under:
                codegen.append("1")
            elif type(node) is Tree.Operator and node.kind == "as":
                codegen.checking = True
                codegen.append(tmp + ".vtable->type.data == ")
                Tree.Typeof(node, node.type.pType).compileToC(codegen)
                i = node.nodes[0]
                if not type(i) is Tree.ReadVar:
                    codegen.append(" && ")
                    loop(node.nodes[0], tmp + ".data")

                codegen.checking = False

                if type(i) is Tree.ReadVar:
                    name = codegen.createName(i.package + "_" + i.name, node.type)
                    node_typ = node.type.toCType()
                    codegen.append(f"{node_typ} {name} = ({node_typ}){tmp}.data;")

            elif type(node) is Tree.Operator and node.kind == "or":
                codegen.append(tmp + "==")
                node.nodes[0].compileToC(codegen)
                codegen.append("||")
                codegen.append(tmp + "==")
                node.nodes[1].compileToC(codegen)
                codegen.checking = False
            else:
                if type(node.type) in [Types.I32,Types.Float,Types.String,Types.Bool]:
                    codegen.append(tmp+"==")
                    node.compileToC(codegen)
                else:
                    raise Exception("not handled yet")

                    codegen.append(tmp+".op_eq(")
                    node.compileToC(codegen)
                    codegen.append(")")
                codegen.checking = False

        codegen.checking = True
        tmp = self.owner.tmp
        loop(self.nodes[0], self.owner.tmp)
        codegen.appendToCodegen()

    def __str__(self):
        return "MatchCase"

    def validate(self, parser):
        pass

def funcIsCase(funcCall):
    readVar = funcCall.nodes[0]
    typ = funcCall.type

    return type(typ) is Types.Enum and readVar.name in typ.const