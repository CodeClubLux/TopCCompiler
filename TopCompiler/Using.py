from TopCompiler import Parser
import AST as Tree

def usingParser(parser):
    parser.nextToken()

    len_of_nodes = len(parser.currentNode.nodes)

    while not Parser.isEnd(parser):
        parser.nextToken()
        Parser.declareOnly(parser, noVar= True)

    if len_of_nodes + 1 != len(parser.currentNode.nodes):
        parser.error("Expecting single expression")

    u = Tree.Using(parser.currentNode.nodes[-1])
    parser.currentNode.nodes[-1] = u
    u.owner = parser.currentNode

Parser.exprToken["using"] = usingParser