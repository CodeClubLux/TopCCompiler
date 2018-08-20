__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import FuncParser
from TopCompiler import Struct

def addMethod(node, parser, attachTyp, name, func, otherNode= False):
    if type(attachTyp) is Types.Struct:
        parser.structs[attachTyp.package][attachTyp.normalName].addMethod(node, parser, name,func)
    elif type(attachTyp) is Struct.Struct:
        if type(func) is Types.FuncPointer:
            if len(func.args) == 0:
                node.error("the function attached must have a first parameter with type "+attachTyp.package+"."+attachTyp.name)

            Types.Struct(False, attachTyp.name, attachTyp.types, attachTyp.package, attachTyp.generic).duckType(parser, func.args[0], node, otherNode, 0)

        attachTyp.addMethod(parser, name, func)
    elif type(attachTyp) in [Types.Enum, Types.Alias]:
        parser.interfaces[attachTyp.package][attachTyp.normalName].addMethod(node, parser, name, func)
    else:
        node.error("Can't add method to "+str(attachTyp))
def checkIfOperator(parser, attachTyp, name, func):
    attachTyp = func.args[0]

    if name.startswith("op_"):
        try:
            operators = {
                "add": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "sub": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "mul": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "div": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "eq": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
                "ne": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
                "mod": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "pow": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
                "gt": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
                "lt": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
                "set": Types.FuncPointer([attachTyp, func.args[1]], Types.Null()),
                "get": Types.FuncPointer([attachTyp, func.args[1]], func.returnType)
            }
        except IndexError:
            Error.parseError(parser, "Operator overload: Function has to have two arguments")

        op = name[len("op_"):]

        if not op in operators:
            Error.parseError(parser, "overload not found for op_"+op)

        try:
            operators[op].duckType(parser, func, Tree.PlaceHolder(parser), Tree.PlaceHolder(parser), 0)
        except EOFError as e:
            Error.beforeError(e, "Operator overload: ")


        if op == "get" and not func.returnType.isType(Types.Pointer):
            Error.parseError(parser, "Return type of operator overload op_get: Must be of type pointer, not " + str(func.returnType))
    elif name.startswith("unary_"):
        unary = {
            "add": Types.FuncPointer([Types.All], attachTyp),
            "sub": Types.FuncPointer([Types.All], attachTyp),
            "read": Types.FuncPointer([Types.All], Types.All, do=True),
        }

        op = name[len("unary_"):]
        if not op in unary:
            Error.parseError(parser, "overload not found for unary_"+op)

        try:
            unary[op].duckType(parser, func, Tree.PlaceHolder(parser), Tree.PlaceHolder(parser), 0)
        except EOFError as e:
            Error.beforeError(e, "Unary overload: ")