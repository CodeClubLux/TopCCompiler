from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree

from TopCompiler import Types
from TopCompiler import Scope
from TopCompiler import VarParser

def externVar(parser):
    VarParser.createAndAssignParser(parser)
    parser.currentNode.nodes[-1].extern = True

Parser.stmts["ext"] = externVar