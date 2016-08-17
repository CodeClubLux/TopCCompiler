import AST as Tree
from TopCompiler import Types

#optimize inlined functions for javascript
def optimizeInliningPass(tree):
    def loop(node):
        for iter in range(len(node.nodes)):
            i = node.nodes[iter]

            if not i.isEnd():
                loop(i)

            if type(i) is Tree.FuncCall and i.inline and i.type != Types.Null():
                if len(i.nodes) == 2:
                    node.nodes[iter] = i.nodes[1]
                    node.nodes[iter].owner = node

    loop(tree)