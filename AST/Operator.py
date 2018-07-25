__author__ = 'antonellacalvia'

from .node import *
import AST as Tree
from AST import Vars
from AST import Cast

class Operator(Node):
    def __init__(self, kind, parser):
        self.kind = kind
        Node.__init__(self, parser)

        self.overload = False
        self.unary = False
        self.curry = False
        self.partial = False
        self.interface = False
        self.name = False
        self.opT = Types.Null()


    def __str__(self):
        return self.kind

    def compileToC(self, codegen):
        if self.kind == "|>":
            self.nodes[1].compileToC(codegen)
            codegen.append("(")
            self.nodes[0].compileToC(codegen)
            codegen.append(")")
            return
        elif self.kind == "as":
            return Cast.castFrom(self.nodes[0].type, self.type, self.nodes[0], codegen)
        elif self.kind == ">>":
            a = self.nodes[0].type
            b = self.nodes[1].type


            codegen.append("function(")
            names = ",".join([codegen.getName() for i in self.nodes[0].type.args])
            codegen.append(names)
            codegen.append("){return ")
            self.nodes[1].compileToJS(codegen)
            codegen.append("(")
            self.nodes[0].compileToJS(codegen)
            codegen.append("("+names+"))}")
            return

        if self.overload:
            if self.interface:
                if len(self.nodes) == 0:
                    codegen.append(self.name)
                    return
                self.nodes[0].compileToC(codegen)
                codegen.append("."+self.name+"(")
            elif self.overload:
                codegen.append(self.package+"_"+self.name)
                codegen.append("(")
                self.nodes[0].compileToC(codegen)

            if len(self.nodes) > 1:
                codegen.append(",") if not self.interface else 0
                self.nodes[1].compileToC(codegen)
            codegen.append(")")
            return

        if self.kind == "concat":
            codegen.append("_global_String_append_tmp")
        if self.kind == "+" and type(self.type ) is Types.String:
            codegen.append("_global_String_op_add")

        #codegen.append("(")


        if self.kind == "^":
            codegen.append("powf(")

        if self.kind in ["+", "-", "*", "/", "<", ">", "<=", ">=", "&"]:
            op = self.kind

        else:
            translate = {
                "==": "==",
                "!=": "!=",
                "not": "!",
                "and": "&&",
                "or": "||",
                "%": "%",
                "concat": ")+(",
                "^": ",",
                "&mut": "&"
            }

            op = translate[self.kind]

        if self.unary:
            codegen.append(op)
        self.nodes[0].compileToC(codegen)

        if not self.unary:
            if self.kind == "concat" or (self.kind == "+" and type(self.type) is Types.String):
                codegen.append(",")
            else:
                codegen.append(op)

            self.nodes[1].compileToC(codegen)
            if self.kind == "concat":
                pass
                #@cleanup implement toString later
                #codegen.append(").toString()")
            if self.kind == "^":
                codegen.append(")")

        #codegen.append(")")

def checkOperator(self, parser):
        i = self
        if type(i.opT) is Types.Alias:
            i.opT = i.opT.typ

        unary = self.unary


        if not (i.kind == "<-" and not unary) and i.type == Types.Null():
            i.error("op "+i.kind + " cannot operate on type "+str(i.type))

        ops = {
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

        if i.kind in ["|>", ">>", "concat", "as", ".."] : return

        if not i.opT.name in ops:
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
                   "<-": "unary_read",
                }
            else:
                overloads = {
                    "+": "op_add",
                    "-": "op_sub",
                    "*": "op_mul",
                    "/": "op_div",
                    "^": "op_pow",
                    "%": "op_mod",
                    "!=": "op_ne",
                    "==": "op_eq",
                    "<": "op_lt",
                    ">": "op_gt",
                    "or": "op_or",
                    "<-": "op_set",
                }

            if len(i.nodes) == 0:
                i.interface = True
                i.name = overloads[i.kind]
                return

            if i.kind == "&":
                Vars.canMutate(self, False)
            elif i.kind == "&mut":
                Vars.canMutate(self, True)
            elif type(i.opT) is Types.Pointer and i.kind == "*" and i.unary:
                i.type = i.opT.pType
            elif type(i.opT) in [Types.Struct, Types.Interface, Types.Enum, Types.T, Types.Array, Types.Pointer]:
                func = i.opT.hasMethod(parser, overloads[i.kind])
                if not func:
                    try:
                        i.opT.types[overloads[i.kind]]
                        i.interface = True
                        i.name = overloads[i.kind]

                    except KeyError:
                        i.error( "Operator " + i.kind + ", cannot operate on type " + str(i.opT))
                else:
                    i.name = i.opT.normalName + "_" + overloads[i.kind]
                    i.package = i.opT.package

                i.overload = True
            else:
                if not i.kind in ops[i.opT.name]:
                    i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))
                i.package = ""
                i.name = overloads[i.kind]

        elif not i.kind in ops[i.opT.name]:
            i.error("Operator " + i.kind + ", cannot operate on type " + str(i.nodes[0].type))