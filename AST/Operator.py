__author__ = 'antonellacalvia'

from .node import *
import AST as Tree

class Operator(Node):
    def __init__(self, kind, parser):
        self.kind = kind
        Node.__init__(self, parser)

        self.overload = False
        self.unary = False
        self.curry = False
        self.interface = False
        self.name = False

    def __str__(self):
        return self.kind

    def compileToJS(self, codegen):
        if self.kind == "|>":
            names = [codegen.getName() for i in self.nodes[0].type.args]
            codegen.append("(function("+",".join(names)+"){return ")
            self.nodes[1].compileToJS(codegen)
            codegen.append("(")
            self.nodes[0].compileToJS(codegen)
            codegen.append("("+",".join(names)+"))})")
            return

        if self.overload or self.curry or self.partial:
            if self.interface:
                if len(self.nodes) == 0:
                    codegen.append(self.name)
                    return

                self.nodes[0].compileToJS(codegen)
                codegen.append("."+self.name+"(")
            elif self.curry or self.unary:
                name = self.package + "_" + self.name if self.package != "" else self.name
                codegen.append(name+(".bind(null,"if self.curry and len(self.nodes) > 0 else "("))

                self.nodes[0].compileToJS(codegen)
            else:
                #partial application
                name = self.package + "_" + self.name if self.package != "" else self.name
                names = [codegen.getName() for i in self.nodes]

                partial = []
                missing = []
                for i in range(len(names)):
                    if type(self.nodes[i]) is Tree.Under:
                        missing += names[i]
                    else:
                        partial += names[i]

                codegen.append("(function("+",".join(partial)+"){return function("+",".join(missing)+"){")
                codegen.append("return "+name)
                codegen.append("("+",".join(names)+");}})(")

                for iter in range(len(self.nodes)-1):
                    i = self.nodes[iter]
                    if not type(i) is Tree.Under:
                        i.compileToJS(codegen)
                        if not (iter+2 == len(self.nodes) and type(self.nodes[iter+1]) is Tree.Under):
                            codegen.append(",")

                if len(self.nodes) > 1 and not type(self.nodes[-1]) is Tree.Under:
                    self.nodes[-1].compileToJS(codegen)

                codegen.append(")")
                return

            if len(self.nodes) > 1:
                codegen.append(",") if not self.interface else 0
                self.nodes[0].compileToJS(codegen)

            codegen.append(")")
            return

        codegen.append("(")
        if self.kind == "concat":
            codegen.append("(")

        if self.type == Types.I32():
            codegen.append("(")
        if self.kind in ["+", "-", "*", "/", "<", ">", "<=", ">="]:
            op = self.kind
        else:
            translate = {
                "==": "===",
                "!=": "!==",
                "not": "!",
                "and": "&&",
                "or": "||",
                "%": "%",
                "concat": ").toString()+(",
            }

            op = translate[self.kind]

        if self.unary:
            codegen.append(op)
        self.nodes[0].compileToJS(codegen)

        if not self.unary:
            codegen.append(op)
            self.nodes[1].compileToJS(codegen)
            if self.kind == "concat":
                codegen.append(").toString()")

        codegen.append(")")

        if self.type == Types.I32():
            codegen.append("|0)")

    def validate(self, parser):
        unary = self.unary
        i = self

        if i.type == Types.Null():
            i.error("operator "+i.kind + " cannot operate on type "+str(i.type))

        operators = {
            "int": ["+", "-", "%", "*", "/", "^", "==", "<", ">", "!=", "<=", ">="],
            "float": ["+", "-", "*", "/", "^", "==", "<", ">", "!=", "<=", ">="],
            "string": ["+", "==", "!=", "<", ">"],
            "bool": ["==", "not", "and", "or", "!="]
        }

        boolean = [
            "==",
            "not",
            "and",
            "or",
            "!=",
            "<",
            ">",
            "<=",
            ">="
        ]

        if i.kind in ["|>", "concat"] : return

        if not i.type.name in operators or i.curry or i.partial:
            if unary:
               overloads = {
                    "+": "unary_add",
                    "-": "unary_sub",
                    "*": "unary_mul",
                    "/": "unary_div",
                    "^": "unary_pow",
                    "!=": "unary_ne",
                    "==": "unary_eq",
                    "not": "unary_not",
                }
            else:
                overloads = {
                    "+": "operator_add",
                    "-": "operator_sub",
                    "*": "operator_mul",
                    "/": "operator_div",
                    "^": "operator_pow",
                    "%": "operator_mod",
                    "!=": "operator_ne",
                    "==": "operator_eq",
                    "<": "operator_lt",
                    ">": "operator_gt",
                    "or": "operator_or"
                }

            if len(i.nodes) == 0:
                i.interface = True
                i.name = overloads[i.kind]
                return
            if type(i.opT) in [Types.Struct, Types.Interface, Types.T]:
                if type(i.opT) in [Types.Interface, Types.T]:
                    func = i.opT.hasMethod(parser, overloads[i.kind])
                    if not func:
                        i.error( "Operator " + i.kind + ", cannot operate on type " + str(i.opT))

                    i.interface = True
                    i.name = overloads[i.kind]
                else:
                    func = parser.structs[i.opT.package][i.opT.normalName].hasMethod(parser, overloads[i.kind])
                    if not func:
                        i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))

                    i.package = i.type.package
                    i.name = i.type.normalName + "_" + overloads[i.kind]

                i.overload = True

            else:
                if not i.kind in operators[i.opT.name]:
                    i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))
                i.package = ""
                i.name = overloads[i.kind]

        elif not i.kind in operators[i.nodes[0].type.name]:
            i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))