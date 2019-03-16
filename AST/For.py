from .node import *

class For(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.package = parser.package
        self.implicit = False
        self.implicit_index = False
        self.op_get = None
        self.condition_type = None

    def compileToC(self, codegen):
        obj = codegen.getName()
        codegen.incrDeferred()
        codegen.incrScope()

        if not self.implicit:
            typ = self.nodes[0].nodes[1].nodes[0].type
        else:
            typ = self.nodes[0].type
        typ = typ.toRealType()
        isRange = typ.name == "Range"

        countTyp = Types.I32(unsigned=True)

        codegen.append(f"{typ.toCType()} {obj} =")
        if not self.implicit:
            self.nodes[0].nodes[1].nodes[0].compileToC(codegen)
        else:
            self.nodes[0].compileToC(codegen)
        codegen.addSemicolon(self.nodes[0])

        if isRange:
            iterationTyp = Types.I32(unsigned=True)
        else:
            iterationTyp = typ.toRealType().elemT

        iteration = codegen.getName()

        codegen.append(f"for ({countTyp.toCType()} {iteration} = ")
        if isRange:
            codegen.append(f"{obj}.start; {iteration} < {obj}.end; {iteration}++) {{\n")
        else:
            if typ.static:
                codegen.append(f"0;{iteration} < {typ.numElements}; {iteration}++) {{\n")
            else:
                codegen.append(f"0;{iteration} < {obj}.length; {iteration}++) {{\n")


        class Tmp:
            def __init__(self, typ):
                self.type = typ

            def compileToC(s, codegen):
                if isRange:
                    codegen.append(f"{iteration};\n")
                else:
                    codegen.append(f"*{self.op_get}(&{obj}, {iteration}, {codegen.getContext()});\n")

        if not self.implicit:
            tmp = self.nodes[0].nodes[0].varType
            self.nodes[0].nodes[0].varType = iterationTyp

            ass = self.nodes[0].nodes[1].nodes[0]
            self.nodes[0].nodes[1].nodes[0] = Tmp(iterationTyp) #.compileToC(codegen)
            #self.nodes[0].nodes[0].varType = tmp
            self.nodes[0].compileToC(codegen)
            self.nodes[0].nodes[1].nodes[0] = ass

            if self.implicit_index:
                c = Tree.Create("i", iterationTyp, self)
                c.package = self.package
                c.varType = countTyp
                c.compileToC(codegen)
                i = codegen.readName(c.package + "_" + c.name)
        else:
            c = Tree.Create("i", iterationTyp, self)
            c.package = codegen.filename
            c.varType = iterationTyp
            name = c.compileToC(codegen)




        if self.implicit_index:
            codegen.append(f"{i} = {iteration};\n")

        for i in self.nodes[1:]:
            i.compileToC(codegen)
            codegen.addSemicolon(i)

        codegen.decrScope()
        codegen.decrDeferred()

        codegen.append("}\n")

