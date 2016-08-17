__author__ = 'antonellacalvia'

from .Escape import *
from .Inline import *
from .Constansts import *
from .Ternary import *
from .BranchRemoving import *
from .RemoveUnusedVar import *
from .OptimizeInlining import *
from .SingleRead import *
from .RemoveUnusedFunc import *

def optimize(tree, opt):
    if opt > 0:
        args = {}
        def findFunctions():
            for c in tree:
                for i in c:
                    if type(i) is Tree.FuncBraceOpen:
                        args[i.package + "." + i.name] = i

        findFunctions()
        ternaryPass(tree)
        constantsPass(tree, args)
        findFunctions()
        inlinePass(tree)
        constantsPass(tree, args)

        if opt > 1:
            branchRemovingPass(tree)
            constantsPass(tree, args)
            singleReadPass(tree)
            removeUnusedFunc(tree)
            removeUnusedPass(tree)

        optimizeInliningPass(tree)
    return None
