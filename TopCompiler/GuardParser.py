from TopCompiler import Parser
from TopCompiler import ExprParser
from TopCompiler import Error
from TopCompiler import ElseExpr
from TopCompiler import IfExpr

import AST as Tree

def guardExpr(parser):
    ExprParser.endExpr(parser, -1)

    parser.nodeBookmark.append(0)

    place = Tree.PlaceHolder(parser)
    parser.currentNode.addNode(place)

    m = Tree.Match(parser)
    m.guard = True
    m.place = place
    parser.currentNode.addNode(m)
    parser.currentNode = m

    assign = False

    while True:
        parser.nextToken()
        if parser.thisToken().token == ":=":
            assign = True
            ExprParser.endExpr(parser, -1)
        else:

            Parser.callToken(parser)
        b = parser.thisToken()
        if b.token == ":=":
            assign = True

        isEnd = Parser.maybeEnd(parser)

        next = parser.lookInfront()
        if (next.token in ["else", "elif"]) and isEnd:
            break

    if len(m.nodes) != 2:
        Error.parseError(parser, "Expecting singular expression, not " + str(len(m.nodes)-1))
    if not assign:
        Error.parseError(parser, "Expecting :=")

    #parser.currentNode.addNode(m)

    ExprParser.endExpr(parser)
    parser.nodeBookmark.pop()

    create = m.nodes[0]
    assign = m.nodes[1]

    m.nodes[0] = assign
    m.nodes[0].owner = m
    del m.nodes[1]

    case = Tree.MatchCase(parser)

    m.addNode(case)
    case.addNode(create)
    m.addNode(Tree.Block(parser))

    case2 = Tree.MatchCase(parser)
    m.addNode(case2)

    if not parser.nextToken().token in ["else", "elif"]:
        Error.parseError(parser, "Expecting else")
    if parser.thisToken().token == "else":
        case2.addNode(Tree.Under(parser))
        m.addNode(Tree.Block(parser))

        ElseExpr.elseExpr(parser, canHaveElse= True)

        m.nodes[4].nodes = m.nodes[4].nodes[1].nodes
        else_block = m.nodes[4]
    else:
        IfExpr.elifExpr(parser, canHaveElse= True)
        conditions = case2.nodes[0].nodes
        block = case2.nodes[1]

        case2.nodes = conditions
        m.addNode(block)

        else_block = block

    if len(else_block) == 0:
        Error.parseError(parser, "Guard block requires exit statement")

    exit_condition = else_block.nodes[-1]
    if not (type(exit_condition) in [Tree.Continue, Tree.Return, Tree.Break] or (type(exit_condition) is Tree.FuncCall and exit_condition.nodes[0].name == "panic")):
        Error.parseError(parser, "Guard block requires exit statement")

    parser.currentNode = m.owner


Parser.exprToken["guard"] = guardExpr

