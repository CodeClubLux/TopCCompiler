__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import Scope
import copy
from TopCompiler import ExprParser
from TopCompiler import VarParser
from TopCompiler import Types
from TopCompiler import MethodParser
import collections as coll

def parserMethodGen(parser, gen, struct):
    sgen = struct.generic

    if len(gen) > len(sgen):
        Error.parseError(parser, str(len(gen)-len(sgen))+" generic arguments too many")
    elif len(gen) < len(sgen):
        Error.parseError(parser, str(len(gen) - len(sgen)) + " generic arguments too few")

    newGen = coll.OrderedDict()
    for a, b in zip(gen, sgen):
        typ = sgen[b]

        aStripped = a[a.rfind(".")+1:]

        if not a in sgen:
            Error.parseError(parser, "Unknown type parameter " + aStripped + " in "+str(struct))
        if gen[a].type != Types.All:
            typ = gen[b] #@cleanup check if interface is compatible with structs regular generics  Error.parseError(parser, "unexpected :")
        newGen[a] = typ
        Scope.changeType(parser, aStripped, typ)

    return newGen

def generics(parser, fname):
    generic = coll.OrderedDict()

    while parser.thisToken().token != "]":
        name = parser.nextToken().token

        typ = Types.T(name, Types.All, parser.package+"."+fname if parser.package != "_global" else fname)
        if parser.thisToken().type != "identifier":
            Error.parseError(parser, "type name must be an identifier")

        if not parser.nextToken().token in [":", ",", "]"]:
            Error.parseError(parser, "expecting ,")

        if parser.thisToken().token == ":":
            parser.nextToken()
            interface = Types.parseType(parser)

            if not type(interface) in [Types.Interface, Types.EnumT, Types.Assign]:
                Error.parseError(parser, "Type variable "+name+", must either be a interface or enumT, not "+str(interface))

            typ = Types.T(name, interface, parser.package+"."+fname if parser.package != "_global" else fname)

            if parser.lookInfront().token != "]":
                parser.nextToken()

        Scope.addVar(Tree.PlaceHolder(parser), parser, name, Scope.Type(False, typ))
        generic[typ.name] = typ

        if parser.lookInfront().token == "]":
            parser.nextToken()
            break

    parser.nextToken()
    return generic

def funcHead(parser, decl= False, dontAdd= False, method= False, attachTyp = False, interfaceMethod=False):
    Scope.incrScope(parser)

    if parser.tokens[parser.iter+2].token == ".":
        if interfaceMethod:
            Error.parseError(parser, "unexpected .")
        if attachTyp: Error.parseError(parser, "unexpected .")
        parser.nextToken()
        name = parser.thisToken().token
        parser.nextToken()

        try:
            attachTyp = Types.Struct(False, name, parser.structs[parser.package][name]._types, parser.package)
        except KeyError:
            try:
                attachTyp = parser.interfaces[parser.package][name]
                if not type(attachTyp) in [Types.Enum, Types.Alias]:
                    Error.parseError(parser, "no attachable data structure found, called "+name)

            except KeyError:
                Error.parseError(parser, "no attachable data structure found, called "+name)
        return funcHead(parser, decl, dontAdd, True, attachTyp)
    name = parser.nextToken()

    if name.type != "identifier":
        Error.parseError(parser, "function name must be of type identifier, not "+name.type)
    parser.nextToken()

    name = name.token

    g = {}
    if parser.thisToken().token != "(":
        if parser.thisToken().token == "[":
            if interfaceMethod:
                Error.parseError(parser, "interfaces can't have generic functions") #not sure about this one

            g = generics(parser, (attachTyp.normalName+"." if method else "")+name)
            if parser.thisToken().token == ".":
                if attachTyp: Error.parseError(parser, "unexpected .")
                if not Scope.varExists(parser, parser.package, name): Error.parseError(parser,
                     "cannot attach method to unknown type main."+name)

                try:
                    attachTyp = Types.Struct(False, name, parser.structs[parser.package][name]._types, parser.package,
                                         parserMethodGen(parser, g, parser.structs[parser.package][name]))
                except KeyError:
                    try:
                        tmp = parser.interfaces[parser.package][name]
                        if not type(tmp) in [Types.Enum, Types.Alias]:
                            raise KeyError

                        attachTyp = Types.replaceT(tmp, parserMethodGen(parser, g, tmp))
                    except KeyError:
                        Error.parseError(parser, "no attachable data structure found, called " + name)

                return funcHead(parser, decl, dontAdd, True, attachTyp)

        if parser.thisToken().token != "(":
            Error.parseError(parser, "expecting (")

    if method and not type(parser.currentNode) is Tree.Root and not decl:
        Error.parseError(parser, "method extension must be in out-most scope")

    header = Tree.FuncStart(name, Types.Null(), parser)
    header.package = parser.package
    parser.currentNode.addNode(header)

    brace = Tree.FuncBraceOpen(parser)
    brace.name = name
    brace.package = parser.package

    parser.currentNode.addNode(brace)

    parser.currentNode = brace

    if method:
        typ = attachTyp
        self = parser.nextToken()
        mut = False
        if not self.token == "&":
            Error.parseError(parser, "expecting & followed by binding name, not "+self.type)

        self = parser.nextToken()
        if not self.type == "identifier":
            Error.parseError(parser, "expecting binding name which is an identifier, not "+str(self.type))

        self = self.token

        pType = Types.Pointer(typ, mut)

        selfNode = Tree.Create(self, pType, parser)
        selfNode.package = parser.package

        selfNode.imutable = False

        parser.currentNode.addNode(selfNode)

        if not parser.lookInfront().token in [")", ","]:
            Error.parseError(parser, "expecting comma not "+parser.thisToken().token)


    if name[0].lower() != name[0]:
        Error.parseError(parser, "function name must be lower case")

    returnType = Types.Null()

    parser.paren += 1
    parser.nextToken()

    while parser.paren != parser.parenBookmark[-1] :
        b = parser.thisToken().token
        if b == ",":
            parser.nextToken()
            continue
        elif b == ")":
            parser.paren -= 1
            parser.nextToken()
            continue
        elif b == "(":
            Error.parseError(parser, "unexpected (")

        if interfaceMethod:
            typ = Types.parseType(parser, parser.package)
            parser.nextToken()
            c = Tree.Create("", typ, parser)
            parser.currentNode.addNode(c)
        else:
            Parser.declareOnly(parser)
            parser.nextToken()

    t = parser.thisToken()
    do = False

    if t.token != "=" or interfaceMethod:
        if not (t.token == "\n" and interfaceMethod):
            returnType = Types.parseType(parser)

        if not interfaceMethod:
            t = parser.nextToken()
            if t.token != "=" and t.token != "do":
                Error.parseError(parser, "expecting = or do")

    parser.currentNode = brace.owner

    names = [i.name for i in brace.nodes]
    types = [i.varType for i in brace.nodes]

    func = Types.FuncPointer(
        types,
        returnType,
        g,
        do
    )

    header.do = do
    header.ftype = func
    brace.ftype = func

    if method:
        Scope.decrScope(parser)

        header.method = True
        header.types = types[1:]
        header.attachTyp = attachTyp
        header.normalName = name
        header.name = attachTyp.normalName+"_"+header.normalName

        MethodParser.checkIfOperator(parser, attachTyp, name, func)

        if decl:
            MethodParser.addMethod(brace, parser, attachTyp, name, func)

        return attachTyp.normalName+"_"+name, names, types, brace, returnType, do

    #parser.func[parser.package][name] = func

    if decl:
        if not dontAdd:
            Scope.addFunc(header, parser, name, func)

    return name, names, types, brace, returnType, do

def funcBody(parser, name, names, types, brace, returnType, do):
    body = Tree.FuncBody(parser)
    body.name = name
    body.returnType = returnType
    body.package = parser.package
    body.do = do
    body.types = types

    brace.body = body

    parser.currentNode.addNode(body)
    parser.currentNode = body

    for i in range(len(names)):
        n = Tree.InitArg(names[i], body)
        n.package = parser.package
        n.varType = types[i]
        n.imutable = not Scope.isMutable(parser, parser.package, names[i])
        body.addNode(n)

    parser.nextToken()
    Parser.callToken(parser) #incase next case is newline

    while not Parser.isEnd(parser):
        parser.nextToken()
        t = parser.thisToken().token
        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = body.owner

    Scope.decrScope(parser)
    return body

def func(parser):
    (name, names, types, header, returnType, do) = funcHead(parser)
    body = funcBody(parser, name, names, types, header, returnType, do)
    body.method = parser.currentNode.nodes[-3].method

def funcCallBody(parser, paren):
    parser.nodeBookmark.append(1)

    def notParen():
        return not Parser.isEnd(parser)

    if paren :
        notEnd = lambda: parser.paren > parser.parenBookmark[-1]
    else:
        notEnd = notParen

    while notEnd():
        t = parser.nextToken()
        if t.token == "," :
            ExprParser.endExpr(parser)
            parser.nodeBookmark[-1] = len(parser.currentNode.nodes)
            continue

        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.nodeBookmark.pop()

def callFunc(parser,paren):
    if len(parser.currentNode.nodes) == 0:
        Error.parseError(parser, "Expecting identifier")
    tail = Tree.FuncCall(parser)

    tail.addNode(parser.currentNode.nodes[-1])

    tail.owner = parser.currentNode

    parser.currentNode.nodes[-1] = tail
    parser.currentNode = tail

    if not paren:
        Parser.selectExpr(parser, parser.thisToken())

    funcCallBody(parser, paren)

    parser.currentNode = tail.owner

def genericT(parser):
    parser.nextToken()
    if len(parser.currentNode.nodes) > 0:
        func = parser.currentNode.nodes.pop()
    else:
        Error.parseError(parser, "unexpected ::")

    generic = Tree.Generic(parser)
    parser.currentNode.addNode(generic)
    generic.addNode(func)

    generic.generic = []

    if parser.thisToken().token != "[":
        Error.parseError(parser, "expecting [")

    parser.nextToken()

    while parser.thisToken().token != "]":
        if parser.thisToken().token == ",":
            parser.nextToken()
            parser.nodeBookmark[-1] = len(parser.currentNode.nodes)
            continue

        generic.generic.append(Types.parseType(parser))
        t = parser.thisToken().token
        parser.nextToken()

def under(parser):
    parser.currentNode.addNode(Tree.Under(parser))

def comma(parser):
    parser.fired = True

def returnF(parser):
    previous = parser.currentNode

    if type(previous) is Tree.Root:
        Error.parseError(parser, "Can only return from function")

    returnAST = Tree.Return(parser)
    previous.addNode(returnAST)

    parser.currentNode = returnAST

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.callToken(parser)

    if len(returnAST.nodes) > 1:
        Error.parseError(parser, "Expecting single expression not "+str(len(returnAST.nodes)))

    parser.currentNode = previous

Parser.stmts["def"] = func
Parser.stmts["return"] = returnF
#Parser.exprToken["none"] = lambda parser: Error.parseError(parser, "unexpected type none")
Parser.exprToken[","] = comma
Parser.exprToken["_"] = under
Parser.exprToken["::"] = genericT
Parser.exprToken["!"] = lambda parser: 0