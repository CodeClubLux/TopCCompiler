__author__ = 'antonellacalvia'

from .node import *
from AST import Enum
from TopCompiler import IfExpr

class If(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

        self.returnTo = ""
        self.next = ""
        self.returnVar = ""
        self.var = ""
        self.ternary = False
        self.yielding = False

    def __str__(self):
        return "IF"

    def compileToC(self, codegen):
        if self.ternary:
            codegen.append("(")
            for i in self.nodes:
                i.compileToC(codegen)
            codegen.append(")")
        elif self.type != Types.Null():
            def compileInner():
                for i in self.nodes:
                    i.compileToC(codegen)


            Enum.genFunction(compileInner, codegen, self.type, self.owner, self)
        else:
            count = 0
            _l = len(self.nodes)
            while count < _l:
                self.nodes[count].compileToC(codegen)
                self.nodes[count+1].compileToC(codegen)

                count += 2

    def validate(self, parser):
        if self.type != Types.Null():
            if len(self.nodes) <= 2:
                self.nodes[-1].nodes[-1].error("expecting else")

            couldBeTernary = True
            for i in range(0, len(self.nodes), 2):
                if len(self.nodes[i + 1].nodes) > 1:
                    couldBeTernary = False
                    break

            self.ternary = couldBeTernary

class IfCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False

    def __str__(self):
        return "ifCondition"

    def compileToC(self, codegen):
        if self.owner.ternary:
            if self.owner.nodes[0] != self:
                codegen.append(" : (")
            self.nodes[0].compileToC(codegen)
            if self.owner.nodes[0] != self:
                codegen.append(")")
            codegen.append(" ? ")
        else:
            s = "else " if self.owner.nodes[0] != self else ""

            codegen.append(f"{s}if(")
            self.nodes[0].compileToC(codegen)
            codegen.append("){")
            codegen.addSemicolon(self)

    def validate(self, parser):
        if len(self.nodes) != 1:
            self.error( "expecting single boolean expression")

        if self.nodes[0].type != Types.Bool():
            self.nodes[0].error("expecting boolean expression not " + str(self.nodes[0].type))

class Else(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False
        self.yielding = False

    def __str__(self):
        return "else"

    def compileToC(self, codegen):
        if self.owner.ternary:
            codegen.append(":(")
        else:
            codegen.append("\nelse{")

    def validate(self, parser): pass

class While(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "While"

    def compileToC(self, codegen):
        for i in self.nodes:
            i.compileToC(codegen)

    def validate(self, parser): pass

class WhilePreCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "WhilePreCondition"

    def compileToC(self, codegen):
        codegen.append(";while(")

    def validate(self, parser): pass

class Break(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return " break"

    def compileToC(self, codegen):
        codegen.append("break;")

    def validate(self, parser): pass

class Continue(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "continue"

    def compileToC(self, codegen):
        codegen.append(" continue;")

    def validate(self, parser): pass

class WhileCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "WhileCondition"

    def compileToC(self, codegen):
        self.nodes[0].compileToC(codegen)
        codegen.append("){")

    def validate(self, parser):
        cond = self
        IfExpr.isBoolCondition(parser, cond)

class WhileBlock(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "block"

    def compileToC(self, codegen):
        codegen.incrDeferred()
        for i in self.nodes:
            i.compileToC(codegen)
            if not type(i) in [Tree.FuncBraceOpen, Tree.FuncBody, Tree.FuncStart]:
                codegen.append(";")

        codegen.decrDeferred()
        codegen.append("}")

    def validate(self, parser):
        checkUseless(self)

import AST

def actuallyYields(node):
    for i in node:
        if AST.yields(i):
            return True
    return False

class Block(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.noBrackets = False
        self.yielding = False
        self.first = True

    def __str__(self):
        return "block"

    def compileToC(self, codegen):
        codegen.incrDeferred()
        if not self.noBrackets and self.owner.ternary:
            self.nodes[0].compileToC(codegen)
            if self == self.owner.nodes[-1]:
                codegen.append(")")
        elif self.type != Types.Null():
            for i in self.nodes[:-1]:
                i.compileToC(codegen)
                codegen.addSemicolon(i)

            codegen.append("return ")
            self.nodes[-1].compileToC(codegen)
            codegen.append(";}")
        else:
            for i in self.nodes:
                i.compileToC(codegen)
                codegen.addSemicolon(i)

            if not self.noBrackets: codegen.append(";}")

        codegen.decrDeferred()

    def validate(self, parser):
        checkUseless(self)