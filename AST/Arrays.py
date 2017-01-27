__author__ = 'antonellacalvia'

from .node import *
from .Struct import *

class Array(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

        self.range = False
        self.init = False

    def __str__(self):
        return "[]"

    def compileToJS(self, codegen):
        if len(self.nodes) == 0:
            codegen.append("EmptyVector");
            return
        if self.range:
            codegen.append("newVectorRange(")
            self.nodes[0].compileToJS(codegen)
            codegen.append(",")
            self.nodes[1].compileToJS(codegen)
            codegen.append(")")
        elif self.init:
            codegen.append("newVectorInit(")
            self.nodes[0].compileToJS(codegen)
            codegen.append(",")
            self.nodes[1].compileToJS(codegen)
            codegen.append(")")
        else:
            codegen.append("newVector(")
            for i in self.nodes[:-1]:
                i.compileToJS(codegen)
                codegen.append(",")

            if len(self.nodes) > 0 :
                self.nodes[-1].compileToJS(codegen)
            codegen.append(")")

    def validate(self, parser):
        arr = self
        mutable = self.mutable
        if self.range:
            arr.type = Types.Array(mutable, Types.I32())
            if len(arr.nodes) != 2 or arr.nodes[1].type != Types.I32():
                Error.parseError(parser, "expecting integer range")
            return
        elif self.init:
            arr.type = Types.Array(mutable, arr.nodes[1].type)
            if len(arr.nodes) != 2 or arr.nodes[1].type == Types.Null():
                Error.parseError(parser, "expecting single non-null expression")
            return

        if not len(arr.nodes) < 1:
            typ = self.type.elemT
            if typ == Types.Null():
                Error.parseError(parser, "array elements must non none")

class ArrRead(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.pointer = False
        self.newValue = False

    def __str__(self):
        return ".[]"

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)
        codegen.append(".get(")
        self.nodes[1].compileToJS(codegen)
        codegen.append(")")

    def set(self, old, codegen):
        if self.newValue:
            codegen.append("return "+old+".set(")
            self.nodes[1].compileToJS(codegen)
            codegen.append(","+self.newValue+")")
        else:
            idx = codegen.getName()

            codegen.append("var "+idx+"=")
            self.nodes[1].compileToJS(codegen)
            codegen.append(";return "+old+".set("+idx+",")
            codegen.append("(function("+old+"){")
            self.owner.set(old, codegen)
            codegen.append("})("+old+".get("+idx+")))")

    def validate(self, parser): pass


