import pickle
import os

def save(parser):
    #return

    f = open("lib/parser.p", "wb")
    parser.rootAst = 0
    parser.currentNode = 0
    parser.compiled = 0
    parser.Stringable = 0
    parser.atomTyp = 0
    parser._tokens = 0
    parser.tokens = 0

    pickle.dump(parser, f)

def load():
    #return False

    try:
        f = open("lib/parser.p", "rb")
        if os.stat("lib/parser.p").st_size == 0:
            return False

        res = pickle.load(f)
        return res
    except FileNotFoundError:
        return False