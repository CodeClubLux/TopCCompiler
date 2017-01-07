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
        #print("compiling struct " + self.package + "." + self.name)
        names = [codegen.getName() for i in self.fields]
        codegen.out_parts.append("function "+self.package+"_"+self.normalName+"("+",".join(names)+"){")
        for i in range(len(self.fields)):
            codegen.out_parts.append("this."+self.fields[i]+"="+names[i]+";")
        codegen.out_parts.append("}")
        codegen.out_parts.append(self.package+"_"+self.normalName+".fields=newVector(")
        codegen.out_parts.append(",".join('"'+i+'"' for i in self.fields))
        codegen.out_parts.append(");")
    def validate(self, parser): pass

class Field(Node):
    def __init__(self, offset, sType, parser):
        super(Field, self).__init__(parser)

        self.offset = offset
        self.sType = sType
        self.indexPackage = False
        self.newValue = False
        self.number = False


    def __str__(self):
        return "."+self.field

    def compileToJS(self, codegen):
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