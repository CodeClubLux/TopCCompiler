__author__ = 'antonellacalvia'

from .node import *
from TopCompiler import Types
class Int(Node):
    def __init__(self, number, parser):
        Node.__init__(self, parser)
        self.number = number

        self.type = Types.I32()

    def __str__(self):
        return "int " + self.number

    def compileToJS(self, codegen):
        codegen.append(self.number)

    def validate(self, parser): pass

class Bool(Node):
    def __init__(self, bool, parser):
        Node.__init__(self, parser)
        self.bool = bool

        self.type = Types.Bool()

    def __str__(self):
        return "bool " + self.bool

    def compileToJS(self, codegen):
        codegen.append(self.bool)

    def validate(self, parser): pass

class Float(Node):
    def __init__(self, number, parser):
        Node.__init__(self, parser)
        self.number = number

        self.type = Types.Float()

    def __str__(self):
        return "double " + self.number

    def validate(self, parser): pass
    def compileToJS(self, codegen):
        codegen.append(self.number)


class String(Node):
    def __init__(self, string, parser):
        super(String, self).__init__(parser)

        self.string = string
        self.type = Types.String(len(string))
        self.target = parser.global_target

    def __str__(self):
        return self.string

    def toString(self):
        if self.target == "node":
            return self.string.\
                replace("\\{", "{"). \
                replace("\\}", "}"). \
                replace("\n", "\\n")

        else:
            return self.string.replace("<", "&lt"). \
                replace(">", "&gt"). \
                replace("\\t", "&nbsp" * 4). \
                replace("\n", ""). \
                replace("\\{", "{"). \
                replace("\\}", "}")

    def compileToJS(self, codegen):
        codegen.append(self.toString())

    def validate(self, parser): pass

class ParseJson(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def validate(self, parser): pass

    def compileToJS(self, codegen):
        typ = self.shouldBeTyp

        if len(self.nodes) == 0:
            codegen.append("(function(")
            tmp = codegen.getName()
            codegen.append(tmp+"){")
            codegen.append("return core_parseJSON("+tmp)
        else:
            codegen.append("core_parseJSON(")
            self.nodes[0].compileToJS(codegen)

        codegen.append(",")

        def loop(typ):
            if type(typ) in [Types.I32, Types.Float, Types.Bool, Types.String]:
                codegen.append("core_json_"+typ.name)
            elif type(typ) in [Types.Struct, Types.Interface]:
                if type(typ) is Types.Struct:
                    codegen.append("core_json_struct("+typ.package+"_"+typ.normalName+",")
                elif type(typ) is Types.Interface:
                    codegen.append("core_json_interface(")

                codegen.append("[")
                for n in typ.types:
                    codegen.append("['"+n+"',")
                    loop(typ.types[n])
                    codegen.append("],")

                codegen.append("])")
            elif type(typ) is Types.Enum:
                codegen.append("core_json_enum[")
                const = list(typ.const)[0]
                for n in const:
                    loop(n)
                    codegen.append(",")
                codegen.append("])")
            elif type(typ) is Types.Array:
                codegen.append("core_json_vector(")
                loop(typ.elemT)
                codegen.append(")")
        loop(typ)
        codegen.append(")")
        if len(self.nodes) == 0:
            codegen.append("})")