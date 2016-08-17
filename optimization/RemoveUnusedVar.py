import AST as Tree
from TopCompiler import Types

#removes unused local variables
def removeUnusedPass(tree):
    unusedLocals = [{}]
    funcs = [tree]

    def loop(node):
        deleted = 0
        for iter in range(len(node.nodes)):
            iter -= deleted
            i = node.nodes[iter]
            if type(i) is Tree.Create :
                if type(i.owner) != Tree.FuncBraceOpen:
                    unusedLocals[-1][i.package+"_"+i.name] = (i, iter)
            elif type(i) is Tree.InitInline:
                unusedLocals[-1][i.package+"_"+i.name] = (i, iter)
            elif type(i) is Tree.ReadVar:
                if i.package+"_"+i.name in unusedLocals[-1]:
                    del unusedLocals[-1][i.package+"_"+i.name]
            elif (type(i) is Tree.FuncCall and i.inline) or type(i) is Tree.FuncStart:
                unusedLocals.append({})
                if type(i) is Tree.FuncCall:
                    funcs.append(i)
            elif type(i) is Tree.FuncBody:
                funcs.append(i)

            if not i.isEnd():
                loop(i)

            if (type(i) is Tree.FuncCall and i.inline) or type(i) is Tree.FuncBody:
                remove(funcs.pop(), unusedLocals.pop())

    def remove(node, names):
        deleted = 0
        for iter in range(len(node.nodes)):
            iter -= deleted
            i = node.nodes[iter]
            if type(i) is Tree.Assign and i.name in names:
                del i.owner.nodes[iter]
                deleted += 1
            elif type(i) is Tree.CreateAssign and i.nodes[0].name in names:
                del i.owner.nodes[iter]
                deleted += 1
                continue
            elif type(i) in [Tree.Create, Tree.InitInline] and i.name in names:
                del i.owner.nodes[iter]
                deleted += 1
                continue

            if not i.isEnd() and not type(i) in [Tree.FuncBraceOpen, Tree.FuncBody, Tree.FuncStart] and not i.inline:
                remove(i, names)
    loop(tree)
    remove(funcs.pop(), unusedLocals.pop())