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
        parser.structs[attachTyp.package][attachTyp.normalName].addMethod(parser, name,func)
    elif type(attachTyp) is Struct.Struct:
        if type(func) is Types.FuncPointer:
            if len(func.args) == 0:
                node.error("the function attached must have a first parameter with type "+attachTyp.package+"."+attachTyp.name)

            Types.Struct(False, attachTyp.name, attachTyp.types, attachTyp.package, attachTyp.generic).duckType(parser, func.args[0], node, otherNode, 0)

        attachTyp.addMethod(parser, name, func)
    else:
        node.error("Can't add method to "+str(attachTyp))
def checkIfOperator(parser, attachTyp, name, func):
    operators = {
        "add": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "sub": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "mul": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "div": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "eq": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
        "ne": Types.FuncPointer([attachTyp, attachTyp], Types.Bool()),
        "mod": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "pow": Types.FuncPointer([attachTyp, attachTyp], attachTyp),
        "getitem": Types.FuncPointer([attachTyp, Types.I32()], Types.I32() )
    }

    unary = {
        "add": Types.FuncPointer([attachTyp], attachTyp),
        "sub": Types.FuncPointer([attachTyp], attachTyp),
        "mul": Types.FuncPointer([attachTyp], attachTyp)
    }

    if name.startswith("operator_"):
        op = name[len("operator_"):]
        if not op in operators:
            Error.parseError(parser, "overload not found for operator_"+op)

        f = Types.FuncPointer(func.args, func.returnType)

        if f != operators[op]:
            Error.parseError(parser, "expecting function declaration "+str(operators[op])+", not "+str(f))
    elif name.startswith("unary_"):
        op = name[len("unary_"):]
        if not op in unary:
            Error.parseError(parser, "overload not found for unary_"+op)

        f = Types.FuncPointer(func.args, func.returnType)

        if f != unary[op]:
            Error.parseError(parser, "expecting function declaration "+str(unary[op])+", not "+str(f))