import AST as Tree
from TopCompiler import Types
from .Constansts import *

def branchRemovingPass(tree):
    def loop(node, pos= 0):
        deleted = 0
        for iter in range(len(node.nodes)):

            iter -= deleted
            i = node.nodes[iter]

            if not i.isEnd():
                loop(i, iter)

            if type(i) is Tree.Else and len(i.owner.nodes) == 2:
                if i.owner.ternary:
                    i.owner.owner.nodes[pos] = i.owner.nodes[1].nodes[0]
                else:
                    i.owner.owner.nodes[pos] = i.owner.nodes[1]
                    i.owner.owner.nodes[pos].noBrackets = True

                i.owner.owner.nodes[pos].owner = i.owner.owner


            if type(i) is Tree.IfCondition:
                if isConstant(i.nodes[0]):
                    t = evaluate(i.nodes[0])
                    if (i.owner.ternary or i.owner.type == Types.Null()):
                        if t:
                            if i.owner.ternary:
                                i.owner.owner.nodes[pos] = i.owner.nodes[1].nodes[0]
                            else:
                                i.owner.owner.nodes[pos] = i.owner.nodes[1]
                                i.owner.owner.nodes[pos].noBrackets = True

                            i.owner.owner.nodes[pos].owner = i.owner.owner
                        else:
                            del i.owner.nodes[0]
                            del i.owner.nodes[0]
                            deleted += 2

    loop(tree)