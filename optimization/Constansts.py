__author__ = 'antonellacalvia'

import AST as Tree

def constantsPass(tree, funcs):
    vars = {}
    def run(n, pos= 0, name= ""):
        for iter in range(len(n.nodes)):
            i = n.nodes[iter]
            if not n.isEnd():
                run(i, iter, i.name if type(i) in [Tree.FuncBraceOpen, Tree.FuncBody] or (type(i) is Tree.FuncCall and i.inline) else name)

            if type(i) in [Tree.Assign, Tree.InitInline]:
                if (type(i.owner) is Tree.CreateAssign and i.owner.nodes[0].imutable) or (type(i) is Tree.InitInline and i.imutable):
                    inner = i.nodes[0]
                    if type(inner) is Tree.ReadVar:
                        if inner.package + "_" + inner.name in funcs:
                            vars[name + "_" + i.package + "_" + i.name] = inner

                    elif type(inner) is Tree.FuncCall and inner.partial:
                        for c in inner.nodes[1:]:
                            if not type(c) is Tree.Under:
                                if not isConstant(c):
                                    break
                        else:
                            optimizeFunc(i, pos)

                    if isConstant(i.nodes[0]):
                        vars[name+"_"+i.package+"_"+i.name] = turnToNode(evaluate(i.nodes[0]), i)

            elif type(i) is Tree.ReadVar:
                varname = name+"_"+i.package+"_"+i.name
                if varname in vars:
                    node = vars[varname]
                    node.owner = n
                    n.nodes[iter] = node

            elif type(i) is Tree.Field and i.indexPackage:
                r = Tree.ReadVar(i.field, True,i)
                r.package = i.nodes[0].package
                i.owner.nodes[iter] = r
                r.owner = i.owner
                r.type = i.type
            elif type(i) is Tree.Array:
                if i.range or i.init:
                    if i.range:
                        if isConstant(i.nodes[0]) and isConstant(i.nodes[1]):
                            arr = Tree.Array()
                            for c in range(evaluate(i.nodes[0]), evaluate(i.nodes[1])):
                                arr.addNode(turnToNode(c))
                    elif i.init:
                        if isConstant(i.nodes[0]):
                            arr = Tree.Array()
                            for c in range(evaluate(i.nodes[0])):
                                arr.addNode(i.nodes[1])
                    arr.owner = n
                    arr.type = i.type
                    n.nodes[iter] = arr

            elif isConstant(i):
                result = evaluate(i)
                node = turnToNode(result, i)
                node.owner = n
                n.nodes[iter] = node
            elif type(i) is Tree.Operator and i.overload and not i.curry:
                f = Tree.FuncCall(i)

                f.type = i.type
                r = Tree.ReadVar(i.name, True, i)
                r.package = i.package
                r.imutable = True

                r.type = Types.FuncPointer([c.type for c in i], i.type)
                f.addNode(r)
                for c in i: f.addNode(c)
                f.owner = i.owner

                i.owner.nodes[iter] = f


    def turnToNode(number, pos):
        if type(number) is int:
            return Tree.Int(str(number), pos)
        elif type(number) is float:
            return Tree.Float(str(number), pos)
        elif type(number) is bool:
            return Tree.Bool("true" if number else "false", pos)
        elif type(number) is str:
            return Tree.String(number, pos)
        raise Exception("cannot turn to constant node, "+number)

    def removeBlock():
        for root in tree:
            added = 0
            for iter in range(len(root.nodes)):
                iter += added
                i = root.nodes[iter]
                if type(i) is Tree.Block:
                    del root.nodes[iter]
                    for d in i:
                        d.owner = root
                        root.nodes.insert(iter, d)
                        iter += 1
                    added += len(i.nodes)-1

    run(tree)
    removeBlock()


def isConstant(n):
    if not type(n) in [Tree.Operator, Tree.Int, Tree.Float, Tree.Bool, Tree.String] or n.curry == True:
        return False

    for i in n:
        if not type(i) in [Tree.Int, Tree.Float, Tree.Bool, Tree.String, Tree.Under] and not (
                    type(i) is Tree.FuncCall and i.inline and isConstant(i.nodes[-1])):
            return False
    return True

def evaluate(i):
    if type(i) is Tree.Int:
        return int(i.number)
    elif type(i) is Tree.String:
        return str(i.string)
    elif type(i) is Tree.FuncCall:
        return evaluate(i.nodes[-1])
    elif type(i) is Tree.Float:
        return float(i.number)
    elif type(i) is Tree.Bool:
        return (True if i.bool == "true" else False)
    elif type(i) is Tree.Operator:
        if i.kind == "+":
            return evaluate(i.nodes[0]) + evaluate(i.nodes[1])
        elif i.kind == "-":
            return evaluate(i.nodes[0]) - evaluate(i.nodes[1])
        elif i.kind == "*":
            return evaluate(i.nodes[0]) * evaluate(i.nodes[1])
        elif i.kind == "/":
            if type(i.type) is Tree.Int:
                return evaluate(i.nodes[0]) // evaluate(i.nodes[1])
            return evaluate(i.nodes[0]) / evaluate(i.nodes[1])
        elif i.kind == "and":
            return evaluate(i.nodes[0]) and evaluate(i.nodes[1])
        elif i.kind == "or":
            return evaluate(i.nodes[0]) or evaluate(i.nodes[1])
        elif i.kind == "not":
            return not evaluate(i.nodes[0])
        elif i.kind == "==":
            return evaluate(i.nodes[0]) == evaluate(i.nodes[1])
        elif i.kind == "!=":
            return evaluate(i.nodes[0]) != evaluate(i.nodes[1])
        elif i.kind == "<":
            return evaluate(i.nodes[0]) < evaluate(i.nodes[1])
        elif i.kind == ">":
            return evaluate(i.nodes[0]) > evaluate(i.nodes[1])
        elif i.kind == ">=":
            return evaluate(i.nodes[0]) >= evaluate(i.nodes[1])
        elif i.kind == "<=":
            return evaluate(i.nodes[0]) <= evaluate(i.nodes[1])

from TopCompiler import Types
def optimizeFunc(i, pos):
    block = Tree.Block(i)
    block.noBrackets = True
    block.type = Types.Null()

    start = Tree.FuncStart(i.name, i.nodes[0].type, i)
    braces = Tree.FuncBraceOpen(i)
    body = Tree.FuncBody(i)

    start.package = i.package

    braces.package = i.package
    braces.name = i.name

    body.package = i.package
    body.name = i.name

    body.returnType = i.nodes[0].type

    i.owner.owner.nodes[pos] = block
    block.owner = i.owner.owner

    block.addNode(start)
    block.addNode(braces)
    block.addNode(body)

    call = i.nodes[0]
    newCall = Tree.FuncCall(i)
    newCall.type = call.type

    r = call.nodes[0]

    newCall.addNode(r)

    count = 0
    index = 0
    for c in call.nodes[1:]:
        if type(c) is Tree.Under:
            create = Tree.Create(str(count), call.nodes[0].type.args[index], i)
            create.package = i.package

            braces.addNode(create)

            t = Tree.InitArg(str(count), i)
            t.package = i.package
            t.imutable = True
            t.type = call.nodes[0].type.args[index]

            body.addNode(t)

            r = Tree.ReadVar(str(count), False, i)
            r.package = i.package
            r.varType = call.nodes[0].type.args[index]
            r.imutable = True
            newCall.addNode(r)
            count += 1
        else:
            newCall.addNode(c)
        index += 1

    body.addNode(newCall)

