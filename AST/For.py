from .node import *

class For(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.implicit = False
        self.implicit_index = False
        self.op_get = None
        self.condition_type = None

    def compileToC(self, codegen):
        obj = codegen.getName()

        if not self.implicit:
            typ = self.nodes[0].nodes[1].nodes[0].type
        else:
            typ = self.nodes[0].type
        typ = typ.toRealType()
        isRange = typ.name == "Range"

        codegen.append(f"{typ.toCType()} {obj} =")
        if not self.implicit:
            self.nodes[0].nodes[1].nodes[0].compileToC(codegen)
        else:
            self.nodes[0].compileToC(codegen)
        codegen.addSemicolon(self.nodes[0])

        countTyp = Types.I32(unsigned=True)

        if isRange:
            iterationTyp = Types.I32(unsigned=True)
        else:
            iterationTyp = typ.toRealType().elemT

        iteration = codegen.getName()

        codegen.append(f"for ({iterationTyp.toCType()} {iteration} = ")
        if isRange:
            codegen.append(f"{obj}.start; {iteration} < {obj}.end; {iteration}++) {{\n")
        else:
            if typ.static:
                codegen.append(f"0;{iteration} < {typ.numElements}; {iteration}++) {{\n")
            else:
                codegen.append(f"0;{iteration} < {obj}.length; {iteration}++) {{\n")

        codegen.incrDeferred()
        codegen.incrScope()

        if not self.implicit:
            tmp = self.nodes[0].nodes[0].varType
            self.nodes[0].nodes[0].varType = iterationTyp

            name = self.nodes[0].nodes[0].compileToC(codegen)
            self.nodes[0].nodes[0].varType = tmp

            if self.implicit_index:
                c = Tree.Create("i", iterationTyp, self)
                c.package = codegen.filename
                c.varType = countTyp
                i = c.compileToC(codegen)
        else:
            c = Tree.Create("i", iterationTyp, self)
            c.package = codegen.filename
            c.varType = iterationTyp
            name = c.compileToC(codegen)
        if isRange:
            codegen.append(f"{name} = {iteration};\n")
        else:
            codegen.append(f"{name} = *{self.op_get}(&{obj}, {iteration}, {codegen.getContext()});\n")

            if self.implicit_index:
                codegen.append(f"{i} = {iteration};\n")

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        codegen.decrScope()
        codegen.decrDeferred()

        codegen.append("}\n")

