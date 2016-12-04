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

    def compileToJS(self, codegen):
        codegen.append("new "+self.type.package+"_"+self.type.normalName+"(")
        for i in range(len(self.nodes)):
            self.nodes[i].compileToJS(codegen)
            if i != len(self.nodes)-1:
                codegen.append(",")
        codegen.append(")")

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
        names = [codegen.getName() for i in self.fields]
        codegen.out_parts.append("function "+self.package+"_"+self.normalName+"("+",".join(names)+"){")
        for i in range(len(self.fields)):
            codegen.out_parts.append("this."+self.fields[i]+"="+names[i]+";")
        codegen.out_parts.append("}")

    def validate(self, parser): pass

class Field(Node):
    def __init__(self, offset, sType, parser):
        super(Field, self).__init__(parser)

        self.offset = offset
        self.sType = sType
        self.indexPackage = False
        self.newValue = False


    def __str__(self):
        return "."+self.field

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)
        codegen.append(("" if self.indexPackage else ".") +self.field)

    def set(self, old, codegen):
        if self.newValue:
            codegen.append("return Object.assign("+old+",{"+self.field+":"+self.newValue+"})")
        else:
            codegen.append("return Object.assign("+old+", {"+self.field+":"+"(function("+old+"){")
            self.owner.set(old, codegen)
            codegen.append("})("+old+"."+self.field+")})")

    def validate(self, parser): pass