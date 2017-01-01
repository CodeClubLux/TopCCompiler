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

    def __str__(self):
        return self.string

    def toString(self):
        return self.string.replace("<", "&lt"). \
            replace(">", "&gt"). \
            replace("\\t", "&nbsp" * 4). \
            replace("\n", ""). \
            replace("\\{", "{"). \
            replace("\\}", "}")

    def compileToJS(self, codegen):
        codegen.append(self.toString())

    def validate(self, parser): pass