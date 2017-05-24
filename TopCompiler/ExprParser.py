__author__ = 'antonellacalvia'

import AST as Tree
from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types


Parser.exprType["bool"] = lambda parser, token: parser.currentNode.addNode(Tree.Bool(token, parser))
Parser.exprType["i32"] = lambda parser, token: parser.currentNode.addNode(Tree.Int(token, parser))
Parser.exprType["f32"] = lambda parser, token: parser.currentNode.addNode(Tree.Float(token, parser))


def operatorPop(parser, op, takesIn, unary= False):
    kind = op.kind
    op.unary = unary
    parser.currentNode.addNode(op)

    count = 0
    min = -1 - takesIn

    #print(parser.currentNode.nodes[parser.nodeBookmark[-1]:])
    #print("=====")

    nb = parser.nodeBookmark[-1]

    if len(parser.bookmark) > 1 and len(parser.stack) > parser.bookmark[-2]+1:
        last = parser.stack[-2].pos
    else:
        last = 0

    use = last if nb < last else nb

    for i in parser.currentNode.nodes[use:][min:-1]:
        parser.currentNode.nodes[-1].addNode(i)
        count += 1

    if count < takesIn:
        op.curry = True

    parser.currentNode.nodes = parser.currentNode.nodes[:-1 - len(op.nodes)] + [op]
    #parser.nodeBookmark.pop()
    pass
   # checkOperator(parser, parser.currentNode.nodes[-1], unary)

operators = {}

Parser.exprType["operator"] = lambda parser, token: operators[token](parser)

def newOperator(kind, precidence, takesIn, func=None, unary= False, token=True):
    def f(parser):
        op = Tree.Operator(kind, parser)

        if len(parser.currentNode.nodes) != 0:
            if not unary and isUnary(parser, parser.lookBehind()):
                Error.parseError(parser, "unexpected "+kind)
            elif unary and not isUnary(parser, parser.lookBehind()):
                Error.parseError(parser, "unexpected "+kind)

        #parser.nodeBookmark.append(len(parser.currentNode.nodes)-1)
        Parser.Opcode(parser, kind, lambda: operatorPop(parser, op, takesIn, unary))

    if func == None: func = f
    Parser.precidences[kind] = precidence

    _f = lambda parser: Error.parseError(parser, "unexpected operator") if parser.lookBehind().type == "xoperator" else func(parser)

    if token:
        Parser.exprToken[kind] = _f
    else:
        operators[kind] = _f

def endExpr(parser, layer= -1):
    for i in reversed(parser.stack[parser.bookmark[layer]:]):
        i.func()
        parser.stack.pop()

    #parser.stack = parser.stack[:parser.bookmark[layer]]
    return

def isUnary(parser, lastToken):
    fact = (lastToken.type in ["operator", "keyword", "whiteOpenS", "bracketOpenS"] or lastToken.token in ["(", "{", "[", ",", "|", ":", "..", "=", "->", "then", "with", "else"] or (lastToken.token == "set" and lastToken.type == "operator") or Parser.selectStmt(parser, lastToken) != None) and\
        not lastToken.token in ["int", "float", "bool", "lens"]

    if fact: return True
    else:
        if parser.thisToken().type in ["operator", "dotS"] or parser.thisToken().token in ["."]:
            return len(parser.currentNode.nodes) == 0
        else:
            return lastToken.type == "indent" or lastToken.token == "\n"

def plus(parser):
    lastToken = parser.lookBehind()

    node = Tree.Operator("+", parser)
    if isUnary(parser, lastToken):  # unary+
        Parser.precidences["+"] = (100, True)

        Parser.Opcode(parser, "+", lambda: operatorPop(parser, node, 1, unary= True))

        Parser.precidences["+"] = (20, True)
        return

    Parser.Opcode(parser, "+", lambda: operatorPop(parser, node, 2))

def minus(parser):
    lastToken = parser.lookBehind()

    op = Tree.Operator("-", parser)
    if isUnary(parser, lastToken):  # unary-
        Parser.precidences["-"] = (100, True)  # give higher power

        Parser.Opcode(parser, "-", lambda:  operatorPop(parser, op, 1, unary= True))

        Parser.precidences["-"] = (20, True)

    else:
        Parser.Opcode(parser, "-", lambda: operatorPop(parser, op, 2))

def read(parser):
    op = Tree.Operator("<-", parser)
    Parser.Opcode(parser, "<-", lambda: operatorPop(parser, op, 1, unary=True))

def set(parser):
    op = Tree.Operator("<-", parser)
    Parser.Opcode(parser, "<-", lambda: operatorPop(parser, op, 2, unary=False))

def asOperator(parser):
    lastToken = parser.lookBehind()

    if not isUnary(parser, lastToken):
        op = Tree.Operator("as", parser)
        parser.nextToken()
        op.type = Types.parseType(parser)
        operatorPop(parser, op, 1)
    else:
        Error.parseError(parser, "unexpected as operator ")

newOperator("set", (2, True), 2, func=set, token=False)
newOperator("|>", (2, True), 2)
newOperator(">>", (2, True), 2)
newOperator("and", (3, True), 2)
newOperator("or", (4, True), 2)
newOperator("not", (6, False), 1, unary= True)
newOperator("<-", (100, False), 1, func = read)
newOperator("==", (8, True), 2)
newOperator("!=", (8, True), 2)
newOperator("<", (10, True), 2)
newOperator("<=", (10, True), 2)
newOperator(">=", (10, True), 2)
newOperator(">", (10, True), 2)
newOperator("concat", (20, True), 2)
newOperator("+", (20, True), 2, func=plus)  # becuase of unary, possiblity
newOperator("-", (20, True), 2, func=minus)  # becuase of unary, possiblity
newOperator("*", (40, True), 2)
newOperator("/", (40, True), 2)
newOperator("%", (40, True), 2)
newOperator("^", (60, False), 2)
newOperator('as', (70, True), 1, func= asOperator)

Parser.exprToken["\\"] = lambda parser: parser.nodeBookmark.append(len(parser.currentNode.owner.nodes))