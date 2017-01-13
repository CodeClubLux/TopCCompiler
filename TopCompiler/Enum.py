from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import Struct
from TopCompiler import FuncParser
from TopCompiler import ExprParser
import AST as Tree
import collections as coll

def enumParser(parser, name, decl, generic):
    const = coll.OrderedDict()
    enum = Types.Enum(parser.package, name, const, generic)

    if decl:
        del parser.structs[parser.package][name]# = Struct.Struct(name, args, fields, coll.OrderedDict())
        parser.interfaces[parser.package][name] = enum

    """if parser.lookInfront().token == "\n":
        parser.nextToken()
        Parser.callToken(parser)
        parser.nextToken()"" \
    """

    while not Parser.isEnd(parser):
        t = parser.nextToken()

        if t.token == "\n" or t.type == "indent":
            Parser.callToken(parser)
            continue


        if t.type != "identifier":
            Error.parseError(parser, "expecting identifier")

        varName = t.token

        if varName[0].upper() != varName[0]:
            Error.parseError(parser, "constructor type must be capitalized")

        args = []
        nextT = parser.nextToken()
        #print(varName)
        #print(nextT)
        if nextT.token == "(":
            args = Types.parseType(parser).list

        const[varName] = args

        if decl:
            Scope.addVar(Tree.PlaceHolder(parser), parser, varName, Scope.Type(True,
                Types.FuncPointer(args, enum, generic = generic) if len(args) > 0 else enum
            ), _global=True)

        t = parser.thisToken()
        if t.token == "\n" or t.type == "indent":
            Parser.callToken(parser)

    parser.currentNode.addNode(Tree.Enum(const, parser))

    Scope.decrScope(parser)

from TopCompiler import ElseExpr

def checkCase(parser, case, typ, first=False):
    if type(case) is Tree.FuncCall:
        if not (type(typ) is Types.Enum or case.nodes[0].name in typ.const):
            case.nodes[0].error("unknown pattern")

        if not case.nodes[0].name in typ.const:
            case.nodes[0].error("no such variable "+case.nodes[0].name)
        pattern = typ.const[case.nodes[0].name]

        for iter in range(1, len(case.nodes)):
            checkCase(parser, case.nodes[iter], pattern[iter-1])
        case.nodes[0].type = Types.FuncPointer([], Types.Null(), do=False)
        case.type = typ
    elif type(case) is Tree.ReadVar and not first:
        Scope.addVar(case, parser, case.name, Scope.Type(True, typ))
    elif type(case) is Tree.ReadVar and first:
        if not (type(typ) is Types.Enum or case.nodes[0].name in typ.const):
            case.nodes[0].error("unknown pattern")
        case.type = typ
    elif type(case) is Tree.Operator and case.kind == "or" and not case.curry and not case.partial:
        typT = case.nodes[0].type
        if typT != case.nodes[1].type:
            case.nodes[1].error("expecting type to be "+str(typ)+" and not "+str(case.nodes[1]))

        if typT != typ:
            case.error("expecting result of or, to be of type "+str(typ))
    elif type(case) in [Tree.String, Tree.Int, Tree.Float]:
        if case.type != typ:
            case.error("expecting type "+str(case.type)+", not "+str(typ))
    elif not type(case) is Tree.Under:
        case.error("unknown pattern")

def match(parser):
    t = parser.thisToken()
    self = Tree.Match(parser)
    parser.currentNode.addNode(self)
    parser.currentNode = self
    while t.token != "with":
        t = parser.nextToken()
        if t.token == "with":
            break
        Parser.callToken(parser)
        t = parser.thisToken()

    parser.nextToken()
    Parser.callToken(parser)

    while not Parser.isEnd(parser):
        t = parser.nextToken()
        if t.token == "->":
            ExprParser.endExpr(parser)

            #print("entered ->")
            if len(self.nodes) == 0:
                Error.parseError(parser, "unexpected ->")
            previos = self.nodes[-1]
            if type(previos) is [Tree.MatchCase, Tree.Block]:
                Error.parseError(parser, "unexpected ->")

            case = Tree.MatchCase(parser)
            case.addNode(previos)

            self.nodes[-1] = case
            case.owner = self

            body = Tree.Block(parser)
            self.addNode(body)

            parser.currentNode = body

            Parser.addBookmark(parser)

            parser.nextToken()
            Parser.callToken(parser)

            while not Parser.isEnd(parser):
                parser.nextToken()
                """if Parser.isEnd(parser):
                    parser.callToken(parser)
                    #print("break", parser.thisToken())
                break
                """
                Parser.callToken(parser)
            #print("break", parser.thisToken())
            Parser.returnBookmark(parser)
            parser.currentNode = body.owner



            continue

        Parser.callToken(parser)

        if parser.thisToken().token == "->":
            parser.iter -= 1

    parser.currentNode = self.owner

Parser.exprToken["match"] = match
Parser.exprToken["with"] = lambda parser: \
    Error.parseError(parser, "unexpected with keyword") if type(parser.currentNode) == Tree.Root else ""

Parser.exprToken["->"] = lambda parser: \
    Error.parseError(parser, "unexpected with keyword") if type(parser.currentNode) == Tree.Root else ""
