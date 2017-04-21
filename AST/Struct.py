__author__ = 'antonellacalvia'


from .node import *
from .Func import *
from .Operator import *
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
                self.nodes[i].compileToJS(codegen)

                if i != len(self.nodes) - 1:
                    codegen.append(",")
            codegen.append("}")
        else:
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

    def compileToJS(self, codegen):
        if not self.assign:
            codegen.append("new "+self.type.package+"_"+self.type.normalName+"(")
            for i in range(len(self.nodes)):
                self.nodes[i].compileToJS(codegen)
                if i != len(self.nodes)-1:
                    codegen.append(",")
            codegen.append(")")
        else:
            self.compileAssign(codegen)

    def validate(self, parser): pass

class Type(Node):
    def __init__(self, package, name, parser):
        super(Type, self).__init__(parser)
        self.package = package
        self.name = name

    def __str__(self):
        return "type "+self.package+"."+self.name

    def compile(self, codegen):
        return ""

    def compileToJS(self, codegen):
        codegen.inFunction()
        #print("compiling struct " + self.package + "." + self.name)
        names = [codegen.getName() for i in self.fields]
        codegen.append("function "+self.package+"_"+self.normalName+"("+",".join(names)+"){")
        for i in range(len(self.fields)):
            codegen.append("this."+self.fields[i]+"="+names[i]+";")
        codegen.append("}")
        codegen.append(self.package+"_"+self.normalName+"._fields=[")
        codegen.append(",".join('"'+i+'"' for i in self.fields))
        codegen.append("];")
        codegen.outFunction()


    def validate(self, parser): pass

class Field(Node):
    def __init__(self, offset, sType, parser):
        super(Field, self).__init__(parser)

        self.offset = offset
        self.sType = sType
        self.indexPackage = False
        self.newValue = False
        self.number = False
        self.unary = False


    def __str__(self):
        return "."+self.field

    def compileToJS(self, codegen):
        if self.unary:
            tmp = codegen.getName()
            field = "get"+self.field[0].upper()+self.field[1:]
            codegen.append("(function get"+self.field+"("+tmp+"){return "+tmp+"."+self.field+"})")
            return

        if not self.indexPackage:
            codegen.append("(")
        self.nodes[0].compileToJS(codegen)

        if not self.number:
            codegen.append(("" if self.indexPackage else ").") +self.field)
        else:
            codegen.append(")["+self.field+"]")

    def set(self, old, codegen):
        if self.newValue:
            codegen.append("return Object.assign(new "+old+".constructor(), "+old+",{"+self.field+":"+self.newValue+"})")
        else:
            codegen.append("return Object.assign(new "+old+".constructor(), {"+self.field+":"+"(function("+old+"){")
            self.owner.set(old, codegen)
            codegen.append("})("+old+"."+self.field+")})")

    def validate(self, parser): pass