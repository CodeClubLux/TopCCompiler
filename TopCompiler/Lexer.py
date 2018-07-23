import collections
from TopCompiler import Error

class Token:
    def __init__(self,token,type,line,column):
        self.token = str(token)
        self.type = type
        self.line = line
        self.column = column

    def error(self, msg):
        Error.parseError(topc.global_parser, msg)

    def __repr__(self):
        return str((self.token,self.type, self.line, self.column ))

from TopCompiler import topc

def lex(target, stream, filename, modifiers, hotswap, lexed, transforms):
    for c in stream: #@cleanup might not need to reparse if isn't modified
        if not hotswap or (hotswap and topc.modified(target, modifiers[c], c)):
            lexed[c] = []
            for i in range(len(stream[c])):
                lexed[c].append(tokenize(stream[c][i], filename[c][i]))

    return lexed

import re

keywords = [
        'import',
        'def',
        'then', 'do', 'if', 'elif', 'else', 'while',
        'int', 'float', 'bool', 'string', 'as',
        'break', 'continue',
        'true', 'false',
        'let',
        'ext',
        'type',
        'string',
        'var',
        "not", "or", "and",
        "match",
        "with",
        "from",
        "decoder",
        "is",
        "either"
    ]

def fastacess(value):
    dictionary = {}
    for i in value:
        dictionary[i] = 0

    return dictionary

slSymbols = fastacess([
    "=",
    "[","]",
    "{", "}",
    "(", ")",
    ":", ";",
    "$",
    "!",
    "_",
    ".",
    ","
]) #Single length delimeters

mLSymbols = [
    "::",
    ":=",
    "..",
    "=>", "+=", "-=", "*=", "/=",
]

slOperator = fastacess(["+", "*", "/", "%", "|", "&", "^"])
mlOperators = ["<<", ">>", "<-", "->", "==", "!=", "<", ">", "-"]

tokenSpecification = [ #cleanup use loop instead of regex to find it out
        ('identifier', r'[^\d\W](\w|(-[^\d\W]))*'),  # [A-Za-z0-9_$]*([A-Za-z0-9_$]*-[A-Za-z_$]+)*
        ('i32', r'\d*[\d_]*(\d+)'),
        ('f32', r'\d*[\d_]*\d+(\.\d*[\d_]*(\d+)|f)'),
        ('hex', r'0[xX][0-9a-fA-F]+'),
    ]

compiledSpecifications = [re.compile(regex) for (group, regex) in tokenSpecification]

import time

def timeit(func):
    def inner(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        print(f"Lexing took: {time.time() - t}")
        return res

    return inner

class LexerState:
    def __init__(self, s):
        self.tok = ""
        self.tokens = []
        self.iter = 0
        self.column = 0
        self.line = 0
        self.s = s
        self.numberOfSInRow = 0
        self.inComment = False
        self.inCommentLine = False
        self.inString = False
        self.inChar = False

    def pushTok(self):
        if self.tok == "": return
        if self.tok in keywords:
            self.append(Token(self.tok, "keyword", self.line, self.column))
        else:
            t = time.time()
            typ = ""
            for (it, (group, regex)) in enumerate(tokenSpecification):
                regex = compiledSpecifications[it]
                if regex.match(self.tok):
                    typ = group
                    break

            if typ == "":
                print("could not match", self.tok)

            self.append(Token(self.tok, typ, self.line, self.column))

        self.tok = ""

    def append(self, value):
        if not type(value) is Token:
            print("what???")
        self.tokens.append(value)

    def followedByNumSpace(self):
        lenOfS = len(self.s)
        num = 0
        while self.iter+1 < lenOfS and self.s[self.iter+1] == " ":
            num += 1
            self.iter += 1

        return num

@timeit
def tokenize(s, filename, spos= 0, sline= 0, scolumn= 0):
    def notBack(iter):
        if state.iter == 0: return True
        if state.s[state.iter - 1] != "\\": return True
        return not notBack(state.iter - 1)

    state = LexerState(s)
    state.iter = spos
    state.line = sline
    state.column = scolumn

    state.inBrace = 0

    lenOfS = len(s)
    while state.iter < lenOfS:
        t = state.s[state.iter]
        completed = True
        if t == '"' and notBack(state.iter) and not (state.inComment or state.inChar or state.inCommentLine):
            state.inString = not state.inString
            if state.inString:
                state.pushTok()
                state.tok = '"'
            else:
                state.tok += '"'
                state.append(Token(state.tok, "str", state.line, state.column))
                state.tok = ""
        elif t == " " and not (state.inString or state.inComment or state.inChar or state.inCommentLine):
            state.pushTok()
        elif t == "{" and notBack(state.iter) and state.inString:
            state.inBrace += 1
            state.tok += '"'
            state.append(Token(state.tok, "str", state.line, state.column))
            state.append(Token("concat", "operator", state.line, state.column))
            state.append(Token("(", "symbol", state.line, state.column))

            state.inString = False
            state.tok = ""
        elif t == "}" and state.inBrace:
            state.inBrace -= 1
            state.inString = True
            state.pushTok()
            state.append(Token(")", "symbol", state.line, state.column))
            state.append(Token("concat", "operator", state.line, state.column))
            state.tok = '"'

        elif t == "'" and not (state.inString or state.inComment or state.inCommentLine):
            state.inChar = not state.inChar
            if state.inChar:
                state.pushTok()
                state.tok = "'"
            else:
                state.tok += "'"
                state.pushTok()
        elif t == "/" and state.iter+1 < lenOfS and state.s[state.iter + 1] == "*" \
        and not (state.inString or state.inComment or state.inChar or state.inCommentLine):
            state.inComment = True
            state.pushTok()
            state.iter += 1
            state.column += 1
        elif t == "*" and state.iter + 1 < lenOfS and state.s[state.iter + 1] == "/" \
        and not (state.inString or state.inChar or state.inCommentLine):
            state.iter += 1
            state.column += 1
            state.inComment = False
            state.append(Token(state.tok, "comment", state.line, state.column))
            state.tok = ""
        elif t == "/" and state.iter + 1 < lenOfS and state.s[state.iter + 1] == "/" \
        and not (state.inString or state.inComment or state.inChar or state.inCommentLine):
            state.pushTok()
            state.iter += 1
            state.column += 1
            state.inCommentLine = True
        elif t == "\n":
            if not (state.inString or state.inComment or state.inChar or state.inCommentLine):
                state.pushTok()
            if state.inCommentLine:
                state.tok = ""
            state.append(Token("\n", "symbol", state.line, state.column))
            state.append(Token(state.followedByNumSpace(), "indent", state.line, state.column))
            state.column = -1
            state.inCommentLine = False
            state.line += 1
        else:
            if not (state.inString or state.inComment or state.inChar or state.inCommentLine):
                if t in slSymbols:
                    state.pushTok()
                    state.append(Token(t, "symbol", state.line, state.column))
                elif t in slOperator:
                    state.pushTok()
                    if state.followedByNumSpace() > 0:
                        state.append(Token(t, "operator", state.line, state.column))
                    else:
                        state.append(Token(t, "unary_operator", state.line, state.column))
                else:
                    completed = False
                    lastLength = 0

                    tok = ""
                    for operators in mlOperators:
                        sameLength = False
                        lenOfOp = len(operators)
                        if len(state.tok) == operators:
                            tok = state.tok
                            sameLength = True

                        elif lastLength == lenOfOp:
                            pass #use existing tok
                        else:
                            if state.iter + lenOfOp - 1 < lenOfS:
                                tok = state.s[state.iter: state.iter+lenOfOp]

                        lastLength = lenOfOp

                        if tok.endswith(operators):
                            state.tok = tok
                            if not sameLength:
                                state.iter += lenOfOp - 1
                            iter = state.iter
                            state.iter -= lenOfOp
                            state.tok = state.tok[:-len(operators)]
                            state.pushTok()
                            state.iter = iter

                            if state.followedByNumSpace() > 0:
                                state.append(Token(operators, "operator", state.line, state.column))
                            else:
                                state.append(Token(operators, "unary_operator", state.line, state.column))
                            completed = True
                            break

                    if not completed:
                        for symbols in mLSymbols:
                            if state.tok.endswith(symbols):
                                iter = state.iter
                                state.tok = state.tok[:-len(operators)]
                                state.pushTok()
                                state.append(Token(symbols, "symbol", state.line, state.column))
                                state.iter = iter
                                completed = True
                                break
            else:
                completed = False

        if not completed:
            state.tok += t

        state.iter += 1
        state.column += 1

        #print("'" + state.tok + "'", state.inString, state.inCommentLine, state.inComment, state.inChar)

    state.pushTok()
    state.append(Token("\n", "symbol", state.line-1, state.column))
    state.append(Token(0, "indent", state.line, state.column))

    #print(state.tokens)

    return state.tokens
