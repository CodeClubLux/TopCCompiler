__author__ = 'antonellacalvia'


from .node import *
from .Func import *
from .Operator import *
from PostProcessing import SimplifyAst

class InitStruct(Node):
    def __init__(self, parser):
        super(InitStruct, self).__init__(parser)
        self.alloca = None

        self.escapes = False

    def __str__(self):
        return "Struct Init"

    def compileAssign(self, codegen):
        if self.unary:
            codegen.append("{")
            for i in range(len(self.nodes)):
                codegen.append(self.nodes[i].nodes[0].name)
                codegen.append(":")
                self.nodes[i].compileToC(codegen)

                if i != len(self.nodes) - 1:
                    codegen.append(",")
            codegen.append("}")
        else:
            if type(self.nodes[0]) is Tree.ReadVar or (type(self.nodes[0]) is Tree.Field and self.nodes[0].indexPackage):
                from TopCompiler import topc
                structT = topc.global_parser.structs[self.type.package][self.type.normalName]


                if self.replaced:
                    codegen.append(
                        f"{SimplifyAst.toUniqueID(self.type.package, self.type.normalName, self.type.remainingGen)}Init(")
                else:
                    codegen.append(self.typ.package + "_" + self.typ.normalName + "Init(")

                myFields = {}
                for c in self.nodes[1:]:
                    myFields[c.nodes[0].name] = c.nodes[1]

                iter = 0
                for field in structT.actualfields:
                    field = field.name
                    if field in myFields:
                        myFields[field].compileToC(codegen)
                    else:
                        f = Field(0, structT, self)
                        f.field = field
                        f.addNode(self.nodes[0])
                        f.compileToC(codegen)

                    iter += 1
                    if iter != len(structT.actualfields):
                        codegen.append(",")
                codegen.append(")")
                return

            self.error("not implemented")
            codegen.append("core_assign(")
            self.nodes[0].compileToJS(codegen)
            codegen.append(",{")
            for i in range(1, len(self.nodes)):
                codegen.append(self.nodes[i].nodes[0].name)
                codegen.append(":")
                self.nodes[i].compileToJS(codegen)

                if i != len(self.nodes) - 1:
                    codegen.append(",")
            codegen.append("})")

    def compileToC(self, codegen):
        if not self.assign:
            cType = self.type.toCType()
            if self.replaced:
                codegen.append(f"{SimplifyAst.toUniqueID(self.typ.package, self.typ.normalName, self.type.remainingGen)}Init(")
            else:
                codegen.append(self.typ.package + "_" + self.typ.normalName + "Init(")
            for i in range(len(self.nodes)):
                self.nodes[i].compileToC(codegen)
                if i != len(self.nodes)-1:
                    codegen.append(",")
            codegen.append(")")
        else:
            self.compileAssign(codegen)

    def validate(self, parser): pass

from TopCompiler import Types

class Type(Node):
    def __init__(self, package, name, parser):
        super(Type, self).__init__(parser)
        self.package = package
        self.name = name
        self.args = []
        self.fields = []
        self.generics = {}
        self.remainingGen = {}
        self.externalStruct = False
        self.replaced = False

    def __str__(self):
        return "type "+self.package+"."+self.name

    def compile(self, codegen):
        return ""

    def replaceT(self, structT, newName):
        self.package = structT.package
        self.normalName = newName

        self.args = list(structT.types.values())
        #Types.replaceT(i, structT.gen) for i in structT.types.values()]
        self.fields =list(structT.types.keys())
        self.remainingGen = structT.remainingGen
        self.replaced = True

    def compileToC(self, codegen):
        if not self.replaced and not self.externalStruct:
            return
        if self.package and self.normalName.startswith("StaticArray") and type(self.remainingGen["StaticArray.S"]) is int:
            staticArrDataType = Tree.ArrDataType(self.package, self.normalName, self)

            staticArrDataType.replaceT(self, self.normalName)
            staticArrDataType.compileToC(codegen)

            return

        codegen.inFunction()
        #print("compiling struct " + self.package + "." + self.name)
        names = self.fields

        if not self.externalStruct:
            cType = "struct " + self.package + "_" + self.normalName
        else:
            cType = self.package + "_" + self.normalName

        codegen.append("struct "+self.package+"_"+self.normalName+" {\n")
        for i in range(len(self.fields)):
            typ = self.args[i].toCType()
            codegen.append(typ + " " + self.fields[i]+";\n")
        codegen.append("};\n")

        codegen.append("static inline " + cType +" " + self.package+"_"+self.normalName + "Init(")

        for i in range(len(self.fields)):
            codegen.append(self.args[i].toCType() + " " + names[i])
            if i < len(self.fields) - 1:
                codegen.append(",")

        codegen.append("){\n")
        name = codegen.getName()
        codegen.append(cType + " " + name + ";\n")

        for i in range(len(self.fields)):
            codegen.append(name + "." + self.fields[i] + "=" + names[i])
            codegen.append(";")

        codegen.append("return "+name)
        codegen.append(";\n};\n")


        #@cleanup Add Serialization for types
        #codegen.append(self.package+"_"+self.normalName+"._fields=[")
        #codegen.append(",".join('"'+i+'"' for i in self.fields))
        #codegen.append("];")
        codegen.outFunction()


    def validate(self, parser): pass

from PostProcessing import SimplifyAst

class Field(Node):
    def __init__(self, offset, sType, parser):
        super(Field, self).__init__(parser)

        self.offset = offset
        self.sType = sType
        self.indexPackage = False
        self.newValue = False
        self.number = False
        self.unary = False
        self.replaced = {}


    def __str__(self):
        return "."+self.field

    def compileToC(self, codegen):
        if self.unary:
            raise Exception("Un implemented")
            tmp = codegen.getName()
            field = "get"+self.field[0].upper()+self.field[1:]
            codegen.append("(function get"+self.field+"("+tmp+"){return "+tmp+"."+self.field+"})")
            return

        if self.field == "length":
            typ = self.nodes[0].type.toRealType()
            if typ.isType(Types.Pointer):
                typ = typ.pType.toRealType()
            try:
                if type(typ.remainingGen["StaticArray.S"]) is int:
                    codegen.append(str(typ.remainingGen["StaticArray.S"]))
                    return
            except KeyError:
                pass

        if not self.indexPackage:
            def getFieldOfInterface(iType, pointer=False):
                n = SimplifyAst.sanitize(iType.name)
                codegen.append(f"*{n}_{self.field}")
                if pointer:
                    codegen.append("(")
                else:
                    codegen.append("ByValue(")
                self.nodes[0].compileToC(codegen)
                if pointer:
                    codegen.append(")")
                codegen.append(")")

            typ = self.nodes[0].type
            if typ.isType(Types.Pointer) and typ.pType.isType(Types.Interface):
                getFieldOfInterface(typ.pType, True)
                return
            elif typ.isType(Types.Interface):
                getFieldOfInterface(typ, False)
                return

        if not self.indexPackage:
            if self.number:
                raise Exception("not implemented yet")
                codegen.append("array_op_index")
            codegen.append("(")

        self.nodes[0].compileToC(codegen)

        if not self.number:
            if self.nodes[0].type.isType(Types.Pointer):
                codegen.append(("" if self.indexPackage else ")->") + self.field)
            else:
                codegen.append(("" if self.indexPackage else ").") +self.field)
        else:
            codegen.append(".field_" + self.field + ")")

    def set(self, old, codegen):
        if self.newValue:
            codegen.append("return Object.assign(new "+old+".constructor(), "+old+",{"+self.field+":"+self.newValue+"})")
        else:
            codegen.append("return Object.assign(new "+old+".constructor(), {"+self.field+":"+"(function("+old+"){")
            self.owner.set(old, codegen)
            codegen.append("})("+old+"."+self.field+")})")

    def validate(self, parser): pass