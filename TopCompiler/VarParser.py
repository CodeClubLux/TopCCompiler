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

def createParser(parser, name= "", typ= None, check= True, imutable= True, attachTyp= False): # : creation
    if name == "":
        name = parser.lookBehind()

    if name.type != "identifier":
        Error.parseError(parser, "variable name must be of type identifier, not "+parser.lookBehind().type)

    name = name.token

    if name[0].lower() != name[0]:
        Error.parseError(parser, "variable name must be lower case")

    node = Tree.Create(name, Types.Null(), parser)
    node.package = parser.package
    node.imutable = imutable

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
        i = parser.currentNode.nodes[-1]
        del parser.currentNode.nodes[-1]

    if package == "": package = parser.package

    if name == "":
        node = Tree.Assign("",  parser= parser)
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


    if name == "_random":
        print()
    ExprParser.endExpr(parser)

    parser.currentNode = node.owner
    parser.nodeBookmark.pop()

    self = node

    if self.init:
        if len(node.nodes) > 1 or len(node.nodes) == 0:
            self.error("expecting single expression")
    else:
        if len(node.nodes) > 2 or len(node.nodes) == 1:
            self.error("expecting single expression")

def createAndAssignParser(parser, imutable= True): # let i assignment
    node = parser.currentNode

    parser.nextToken() #get current token to position of =

    checkIt = False
    attachTyp = False

    if parser.lookInfront().token == ".":

        attachTyp = Types.parseType(parser, attachTyp= True)
        parser.nextToken()
        if not imutable or not type(node) is Tree.Root:
            Error.parseError(parser, "expecting =, not .")
        parser.nextToken()


    name = parser.thisToken()

    typ = None

    if parser.nextToken().token == ":":
        checkIt = True

        parser.nextToken()
        typ = Types.parseType(parser)

        parser.nextToken()
    elif parser.thisToken().token != "=":
        Error.parseError(parser, "expecting =, not"+parser.thisToken().token)

    n = Tree.CreateAssign(parser)

    parser.currentNode.addNode(n)
    parser.currentNode = n



    createParser(parser, name= name, typ= typ, check= checkIt, imutable= imutable, attachTyp= attachTyp)

    if attachTyp:
        assignParser(parser, name=attachTyp.name+"_"+name.token, package= attachTyp.package, init=True)
    else:
        assignParser(parser, name= name.token, init= True)

    n.nodes[1].isGlobal = n.nodes[0].isGlobal
    n.nodes[1].createTyp = n.nodes[0].varType

    parser.currentNode = node

Parser.stmts["let"] = createAndAssignParser
Parser.stmts["var"] = lambda parser: createAndAssignParser(parser, imutable= False)
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

    name = parser.currentNode.nodes[-1].nodes[0].name

    node = parser.currentNode.nodes[-1]

    add = Tree.Operator(operator, parser)
    add.addNode(node.nodes[1])

    r = Tree.ReadVar(name, False, parser)
    r.package = node.package
    r.type = node.nodes[0].type
    add.nodes.insert(0, r)
    r.owner = add

    add.owner = node

    node.nodes[1] = add

Parser.exprType["identifier"] = read

Parser.stmts["+="] = lambda parser: equalAnd(parser, "+")
Parser.stmts["-="] = lambda parser: equalAnd(parser, "-")
Parser.stmts["*="] = lambda parser: equalAnd(parser,  "*")
Parser.stmts["/="] = lambda parser: equalAnd(parser,  "/")
Parser.stmts["%="] = lambda parser: equalAnd(parser,  "%")
Parser.stmts["^="] = lambda parser: equalAnd(parser,  "^")