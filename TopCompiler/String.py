__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Types
from TopCompiler import String
import AST as Tree


Parser.exprType["str"] = lambda parser, string: \
    parser.currentNode.addNode(Tree.String(string, parser))

Parser.exprType["char"] = lambda parser, string: \
    parser.currentNode.addNode(Tree.Char(string, parser))