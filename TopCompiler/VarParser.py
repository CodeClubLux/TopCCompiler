__author__ = 'antonellacalvia'

from TopCompiler import Parser
import AST as Tree
from TopCompiler import Error
from TopCompiler import ExprParser
from TopCompiler import Scope
from TopCompiler import FuncParser
from TopCompiler import ExprParser
from TopCompiler import Types
from TopCompiler import Struct
from TopCompiler import Lexer


def pattern(name, names, parser, getName):
    if type(name) in [Tree.Tuple, Tree.PlaceHolder]:
        node = name.nodes[0]
        if type(node) is Tree.Tuple:
            for i in node:
                pattern(i, names, parser, getName)
        elif type(node) is Tree.InitStruct:
            for i in node:
                if type(i) is Tree.Assign:
                    if not type(i.nodes[0]) is Tree.ReadVar:
                        i.error("Expecting variable name")
                    pattern(i.nodes[1], names, parser, getName)
                elif type(i) is Tree.ReadVar:
                    pattern(i, names, parser, getName)
                else:
                    i.error("Expecting variable name")
        return name
    elif type(name) is Tree.ReadVar:
        names.append(name.name)
        return getName(name.token)
    elif type(name) is Tree.Under:
        names.append(name.name)
    elif type(name) is Lexer.Token and name.type == "identifier":
        return getName(name)
    else:
        if type(name) is Lexer.Token:
            if name.type == "indent":
                Error.parseError(parser, "Expecting identifier")
            else:
                Error.parseError(parser, "Unexpected token "+name.token)
        else:
            name.error("Unexpected token")

def createParser(parser, name= "", typ= None, check= True, imutable= False, attachTyp= False): # : creation
    if name == "":
        name = parser.lookBehind()

    names = []

    def getName(name):
        if name.type != "identifier":
            Error.parseError(parser, "variable name must be of type identifier, not " + parser.lookBehind().type)

        name = name.token

        if name[0].lower() != name[0]:
            Error.parseError(parser, "variable name must be lower case")

        return name

    name = pattern(name, names, parser, getName)

    node = Tree.Create(name, Types.Null(), parser)
    node.package = parser.package
    node.imutable = imutable
    node.names = names

    if attachTyp:
        node.attachTyp = attachTyp

    parser.currentNode.addNode(node)

    node.varType = typ
    if check and typ is None:
        parser.nextToken()
        typ = Types.parseType(parser)

        node.varType = typ

def assignParser(parser, name= "", init= False, package = ""):
    if not init:
        ExprParser.endExpr(parser, -2)
        i = parser.currentNode.nodes[-1]
        del parser.currentNode.nodes[-1]

    if package == "": package = parser.package

    if name == "":
        node = Tree.Assign("", parser=parser)
        node.addNode(i)
    else:
        node = Tree.Assign(name, parser=parser)

    parser.nodeBookmark.append(0)

    node.package = package
    node.init = init

    parser.currentNode.addNode(node)
    parser.currentNode = node

    curr = parser.thisToken()

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = node.owner
    parser.nodeBookmark.pop()

    self = node

    if self.init:
        if len(node.nodes) > 1 or len(node.nodes) == 0:
            self.error("expecting single expression, not "+str(len(node.nodes)))
    else:
        if len(node.nodes) > 2 or len(node.nodes) == 1:
            self.error("expecting single expression, not "+str(len(node.nodes)-1))

def createAndAssignParser(parser, imutable= True): # let i assignment
    node = parser.currentNode



    checkIt = False
    attachTyp = False

    """if parser.lookInfront().token == ".":
        attachTyp = Types.parseType(parser, _attachTyp= True)
        parser.nextToken()
        if not imutable or not type(node) is Tree.Root:
            Error.parseError(parser, "expecting =, not .")
        parser.nextToken()
    """

    isPattern = False
    pattern = False
    if imutable:
        name = parser.nextToken()
    else:
        r = parser.currentNode.nodes[-1]
        del parser.currentNode.nodes[-1]
        name = r
        parser.iter -= 1
        isPattern = True
        pattern = True

    typ = None
    create = False

    t = parser.thisToken()

    if parser.nextToken().token == ":":
        checkIt = True

        parser.nextToken()
        typ = Types.parseType(parser)

        parser.nextToken()

        if parser.thisToken().token != "=":
            create = True
    elif imutable and parser.thisToken().token != "=":
        Error.parseError(parser, "expecting =, not "+parser.thisToken().token)

    if not create:
        n = Tree.CreateAssign(parser)
        parser.currentNode.addNode(n)
        parser.currentNode = n

        createParser(parser, name=name, typ=typ, check=checkIt, imutable=imutable, attachTyp=attachTyp)

        if attachTyp:
            assignParser(parser, name=parser.package+"_"+attachTyp.normalName+"_"+name.token, package= attachTyp.package, init=True)
            n.nodes[1].attachName = parser.package+"_"+attachTyp.normalName
            n.nodes[1].varName = name.token
        else:
            if type(name) is Tree.ReadVar:
                name = name.token
            c = name if not type(name) is Lexer.Token else name.token
            assignParser(parser, name= c, init= True)

        n.nodes[1].isGlobal = n.nodes[0].isGlobal
        n.nodes[1].createTyp = n.nodes[0].varType


        parser.currentNode = node
    else:
        createParser(parser, name=name, typ=typ, check=checkIt, imutable=imutable, attachTyp=attachTyp)

Parser.stmts["let"] = createAndAssignParser
Parser.stmts[":="] = lambda parser: createAndAssignParser(parser, imutable= False)
Parser.stmts["="] = assignParser
Parser.stmts[":"] = createParser

Parser.exprToken["i32"] = lambda parser: Error.parseError(parser, "unexpected type int")
Parser.exprToken["|"] = lambda parser: Error.parseError(parser, "unexpected function declaration")
Parser.exprToken["int"] = lambda parser: Error.parseError(parser, "unexpected type int")
Parser.exprToken["float"] = lambda parser: Error.parseError(parser, "unexpected type float")
Parser.exprToken["bool"] = lambda parser: Error.parseError(parser, "unexpected type bool")

def read(parser, name, package= ""):
    if package == "": package = parser.package

    node = Tree.ReadVar(name,  False, parser)
    node.package = package

    parser.currentNode.addNode(node)

def equalAnd(parser, operator, package= ""):
    if package == "": package = parser.package
    assignParser(parser, "", init= False, package= package)

    readVar =  parser.currentNode.nodes[-1].nodes[0]
    name = readVar.name

    node = parser.currentNode.nodes[-1]

    add = Tree.Operator(operator, parser)
    add.isUnary = False
    add.addNode(readVar)
    add.addNode(node.nodes[1])

    add.owner = node

    node.nodes[1] = add

Parser.exprType["identifier"] = read

Parser.stmts["+="] = lambda parser: equalAnd(parser, "+")
Parser.stmts["-="] = lambda parser: equalAnd(parser, "-")
Parser.stmts["*="] = lambda parser: equalAnd(parser,  "*")
Parser.stmts["/="] = lambda parser: equalAnd(parser,  "/")
Parser.stmts["%="] = lambda parser: equalAnd(parser,  "%")
Parser.stmts["^="] = lambda parser: equalAnd(parser,  "^")