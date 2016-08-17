__author__ = 'antonellacalvia'

import AST as Tree


def removeUnusedFunc(tree):
    class Func():
        def __init__(self, iter, node):
            self.array = []
            self.marked = False
            self.iter = iter
            self.node = node

        def called(self, name):
            self.array.append(callGraph[name])

    f = Func(0, tree)
    f.marked = True

    callGraph = {"": f}
    def check(n):
        for c in n:
            for iter in range(len(c.nodes)):
                i = c.nodes[iter]
                if type(i) is Tree.FuncBody:
                    callGraph[i.package+"_"+i.name] = Func(iter, i)

    def loop(n, name= ""):
        for i in n:
            if type(i) is Tree.FuncBody:
                loop(i, i.package+"_"+i.name)
                continue
            elif type(i) is Tree.ReadVar and (i.package+"_"+i.name) in callGraph:
                callGraph[name].called(i.package+"_"+i.name)
            elif type(i) is Tree.Operator and i.overload:
                callGraph[name].called(i.name)

            if not i.isEnd():
                loop(i, name)

    check(tree)
    loop(tree)

    def mark(n):
        for i in n.array:
            if not i.marked:
                i.marked = True
                mark(i)

    mark(callGraph[""])

    def delete(callG):
        for i in callG:
            if not i.marked:
                i.node.owner.nodes[i.iter] = Tree.PlaceHolder(i.node)
                i.node.owner.nodes[i.iter-1] = Tree.PlaceHolder(i.node)
                i.node.owner.nodes[i.iter-2] = Tree.PlaceHolder(i.node)

    delete(callGraph.values())
