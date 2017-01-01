from .node import *

class Enum(Node):
    def __init__(self, const, parser):
        Node.__init__(self, parser)
        self.const = const
        self.package = parser.package

    def compileToJS(self, codegen):
        count = 0
        for name in self.const:
            codegen.append("function "+self.package+"_"+name+"(")
            args = self.const[name]
            names = [codegen.getName() for _ in args]
            codegen.append(",".join(names))
            count += 1

            codegen.append("){return ["+str(count)+","+",".join(names)+"]}")

    def validate(self, parser): pass