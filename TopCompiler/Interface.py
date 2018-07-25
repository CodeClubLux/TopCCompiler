from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import Struct
from TopCompiler import FuncParser
import collections as coll
from AST import PlaceHolder

def traitParser(parser, name, decl, generic):
    meth = {}
    while not Parser.isEnd(parser):
        parser.nextToken()

        t = parser.thisToken()

        if t.token == "def":
            currentNode = parser.currentNode
            p = PlaceHolder(parser)
            parser.currentNode = p

            ( methodName, names, types, brace, returnType, do) = FuncParser.funcHead(parser, decl, dontAdd=True, interfaceMethod=True)
            Scope.decrScope(parser)
            if methodName in meth:
                Error.parseError(parser, "Method " + methodName + ", already defined")
            meth[methodName] = brace.ftype
            parser.currentNode = currentNode
        else:
            Parser.declareOnly(parser, noVar=True)

    names = {i.name: i.varType for i in parser.currentNode}
    #args = [i.varType for i in parser.currentNode]
    #fields = parser.currentNode.nodes

    if decl:
        del parser.structs[parser.package][name]# = Struct.Struct(name, args, fields, coll.OrderedDict())

        i = Types.Interface(False, names, generic, parser.package+"."+name, methods= meth)
        parser.interfaces[parser.package][name] = i

    Scope.decrScope(parser)