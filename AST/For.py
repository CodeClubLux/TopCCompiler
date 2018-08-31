from .node import *

class For(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToC(self, codegen):
        obj = codegen.getName()
        typ = self.nodes[0].nodes[1].nodes[0].type
        isRange = typ.name == "Range"

        codegen.append(f"{typ.toCType()} {obj} =")
        self.nodes[0].nodes[1].nodes[0].compileToC(codegen)
        codegen.addSemicolon(self.nodes[0])

        iterationTyp = Types.I32(unsigned=True)
        iteration = codegen.getName()

        codegen.append(f"for ({iterationTyp.toCType()} {iteration} = ")
        if isRange:
            codegen.append(f"{obj}.start; {iteration} < {obj}.end; {iteration}++) {{\n")
        else:
            codegen.append("0;{iteration} < {obj}.length; {iteration}++) {{\n")

        codegen.incrDeferred()
        codegen.incrScope()

        name = self.nodes[0].nodes[0].compileToC(codegen)
        if isRange:
            codegen.append(f"{name} = {iteration};")
        else:
            self.func(codegen, obj)

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        codegen.decrScope()
        codegen.decrDeferred()

        codegen.append("}\n")

