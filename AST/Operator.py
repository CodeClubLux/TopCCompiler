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

        if self.overload or self.curry:
            if self.interface:
                if len(self.nodes) == 0:
                    codegen.append(self.name)
                    return

                self.nodes[0].compileToJS(codegen)
                codegen.append("."+self.name+"(")
            else:
                name = self.package + "_" + self.name if self.package != "" else self.name
                codegen.append(name+(".bind(undefined,"if self.curry and len(self.nodes) > 0 else "("))

                self.nodes[0].compileToJS(codegen)

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

        if not i.type.name in operators or i.curry:
            if unary:
               overloads = {
                    "+": "unary_add",
                    "-": "unary_sub",
                    "*": "unary_mul",
                    "/": "unary_div",
                    "^": "unary_pow",
                    "%": "unary_mod",
                    "!=": "unary_ne",
                    "==": "unary_eq",
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
                }

            if len(i.nodes) == 0:
                i.interface = True
                i.name = overloads[i.kind]
                return
            if type(i.type) in [Types.Struct, Types.Interface, Types.T]:
                if type(i.type) in [Types.Interface, Types.T]:
                    func = i.type.hasMethod(parser, overloads[i.kind])
                    if not func:
                        i.error( "Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))

                    i.interface = True
                    i.name = overloads[i.kind]
                else:
                    func = parser.structs[i.type.package][i.type.normalName].hasMethod(parser, overloads[i.kind])
                    if not func:
                        i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))

                    i.package = i.type.package
                    i.name = i.type.normalName + "_" + overloads[i.kind]

                i.overload = True

            else:
                if not i.kind in operators[i.nodes[0].type.name]:
                    i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))
                i.package = ""
                i.name = overloads[i.kind]

        elif not i.kind in operators[i.nodes[0].type.name]:
            i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))