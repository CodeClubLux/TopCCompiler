import js2py

from TopCompiler import CodegenJS as CodeGen
from TopCompiler import Lexer
from TopCompiler import Parser
from TopCompiler import ResolveSymbols
from TopCompiler import PackageParser
from TopCompiler import topc
import AST as Tree

import sys

def main():
    tokens = [[]]
    parser = Parser.Parser(tokens, [("main", "anonymous")])
    parser.compiled = {}
    parser.global_target = "client"
    parser.opt = 0
    parser.externFuncs = {"main": []}
    parser.repl = True
    parser.hotswap = False
    parser._tokens = parser.tokens
    parser._filename = parser.filename
    PackageParser.packDec(parser, "main", pack=True)

    parenThing = 0

    js = js2py.EvalJs()
    js.eval(CodeGen.getRuntimeNode())

    text = ""
    indent = 0


    while True:
        if indent == 0:
            line = input("> ")
        else:
            line = input("." * indent + " ")

        text = line+"\n"
        topc.filenames_sources = {"main": {"anonymous": text}}
        try:
            t = Lexer.tokenize(line, "anonymous")
            if indent == 0:
                tokens[0] = t
            else:
                tokens[0] += t

            count = 0
            for i in t:
                if i.token in ["(", "{", "["]:
                    count += 1
                elif i.token in [")", "}", "]"]:
                    count -= 1

            parenThing += count

            if count > 0:
                indent += 4
            elif count < 0 and parenThing == 0:
                indent -= 4

            if len(t) > 2:
                c = t[-3]
                if c.type == "keyword" or c.token == "=":
                    indent += 4
            elif len(t) == 2:
                indent -= 4

            tokens[0][-1].token = str(indent)

            if indent == 0:
                #ResolveSymbols.insert(parser, parser, only= True)
                parser.package = "main"
                parser.opackage = "main"

                t = parser.tokens
                f = parser.filename

                for i in range(3):
                    ResolveSymbols._resolve(parser, tokens[0], "anonymous", i)

                parser.currentNode = Tree.Root()

                parser.tokens = t
                parser.filename = f

                parsed = parser.parse()

                compiled = (parsed, {"main": []})

                code = CodeGen.CodeGen("main", parsed, {"main": []}, "node", 0).toEval()
                    #print(code)

                js.eval(code)
                print("Of type: "+str(parsed.nodes[-1].type))
                tokens[0] = []
                parser.currentNode = Tree.Root()

        except EOFError as e:
            parser.tokens = parser._tokens
            parser.filename = parser._filename

            CRED = '\033[91m'
            CEND = '\033[0m'
            print(CRED+str(e)+CEND)

main()
