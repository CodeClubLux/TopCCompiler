import AST as Tree
from TopCompiler import Types

#turns if conditions to ternary when possible
def ternaryPass(tree):
    def loop(node):
        for i in node:
            if type(i) is Tree.If and i.type != Types.Null():
                for n in i.nodes[::2]:
                    if len(n.nodes) != 1: break
                else:
                    if not i.isEnd():
                        loop(i)
                    continue
                i.ternary = True
            if not i.isEnd():
                loop(i)

    loop(tree)