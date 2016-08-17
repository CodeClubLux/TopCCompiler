__author__ = 'antonellacalvia'

import AST as Tree
import pprint
import copy
from TopCompiler import Types

def inlinePass(tree):
    sizes = {"": 100000}
    functions = {}
    def findFunctions():
        for c in tree:
            for i in c:
                if type(i) is Tree.FuncBody:
                    sizes[i.package+"."+i.name] = sizeof(i)
                    functions[i.package+"."+i.name] = i

    def sizeof(node):
        count = 0
        for i in node:
            if not i.isEnd():
                count += sizeof(i)

            count += 1
        return count

    findFunctions()

    inlineMax = 50

    def decideToInline(name):
        return sizes[name] < inlineMax

    def whatToInline(node, self= False):

        for i in node:
            if not i.isEnd():
                whatToInline(i, i if type(i) is Tree.FuncBody else self)

            if (type(i) is Tree.FuncCall and (i.nodes[0].package+"."+i.nodes[0].name) in sizes):
                name = i.nodes[0].package+ "." + i.nodes[0].name

                if (self and self.package + "." + self.name == name) or i.partial or i.curry:
                    continue

                if decideToInline(name):
                    inline(i, functions[name])
                    if self:
                        sizes[self] = sizeof(self)

    def inline(funcCall, func):
        funcCall.inline = True

        f = copy.deepcopy(func)

        for it in range(len(f.nodes)):
            i = f.nodes[it]
            if type(i) is Tree.InitArg:
                f.nodes[it] = Tree.InitInline(i.name, i.varType, i)
                f.nodes[it].addNode(funcCall.nodes[it+1])
                f.nodes[it].package = i.package
                f.nodes[it].imutable = i.imutable
                f.nodes[it].owner = funcCall
            i.owner = funcCall

        t = Tree.InlineStart(f)
        t.owner = funcCall
        f.nodes.insert(0, t)

        funcCall.nodes = f.nodes

    whatToInline(tree)
    return



