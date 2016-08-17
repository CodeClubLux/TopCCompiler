import AST as Tree
from TopCompiler import Types

def singleReadPass(tree):
    unusedLocals = [{}]
    funcs = [tree]

    def loop(node):
        deleted = 0
        for iter in range(len(node.nodes)):
            iter -= deleted
            i = node.nodes[iter]
            if type(i) is Tree.Create:
                if type(i.owner) != Tree.FuncBraceOpen and i.imutable:
                    unusedLocals[-1][i.name] = [False, False]
            elif type(i) is Tree.InitInline:
                unusedLocals[-1][i.name] = [False, i.nodes[0]]
            elif type(i) is Tree.ReadVar:
                if i.name in unusedLocals[-1]:
                    if not unusedLocals[-1][i.name][0]:
                        unusedLocals[-1][i.name][0] = True
                    else:
                        del unusedLocals[-1][i.name]
            elif type(i) is Tree.Assign:
                if i.name in unusedLocals[-1]:
                    unusedLocals[-1][i.name][1] = i.nodes[0]

            elif (type(i) is Tree.FuncCall and i.inline) or type(i) is Tree.FuncStart:
                unusedLocals.append({})
                if type(i) is Tree.FuncCall:
                    funcs.append(i)
            elif type(i) is Tree.FuncBody:
                funcs.append(i)
            if not i.isEnd():
                loop(i)

            if (type(i) is Tree.FuncCall and i.inline) or type(i) is Tree.FuncBody:
                popped = unusedLocals.pop()

                replace(funcs.pop(), popped)

                    
    def replace(node, names):
        for iter in range(len(node.nodes)):
            i = node.nodes[iter]
            if type(i) is Tree.ReadVar and i.name in names and (names[i.name][1] != False and canBeReplaced(names[i.name][1].owner)):
                print("replaced ", i.name)
                i.owner.nodes[iter] = names[i.name][1]

            if not i.isEnd() and not type(i) in [Tree.FuncBraceOpen, Tree.FuncBody, Tree.FuncStart] and not i.inline:
                replace(i, names)

    def canBeReplaced(value):
        for i in value:
            if type(i) is Tree.ReadVar and not i.imutable:
                return False
            if not i.isEnd():
                if not canBeReplaced(i):
                    return False
        return True
    loop(tree)
    popped = unusedLocals.pop()

    replace(funcs.pop(), popped)