__author__ = 'antonellacalvia'

import collections

from TopCompiler import Error


class Token:
    def __init__(self,token,type,line,column):
        self.token = str(token)
        self.type = type
        self.line = line
        self.column = column + (len(str(token)) // 2)


    def __repr__(self):
        return str((self.token,self.type, self.line, self.column ))

def lex(stream, filename):
    lexed = {}
    for c in stream:
        lexed[c] = []
        for i in range(len(stream[c])):
            lexed[c].append(tokenize(stream[c][i], filename[c][i]))
    return lexed

import re

def tokenize(s, filename, spos= 0, sline= 0, slinePos= 0):
    keywords = [
        'import',
        'def',
        'then', 'do', 'if', 'elif', 'else', 'while',
        'int', 'float', 'none', 'bool', 'string',
        'break', 'continue',
        'true', 'false',
        'let',
        'ext',
        'type',
        'string',
        'var',
        "not", "or", "and",
    ]

    special = ["arrow", "doublecolon", "line", "underscore", "assign", "assignPlus", "assignSub", "assignMul", "assignDiv", 'colon', 'dot', 'openC', 'openB', 'closeC', 'closeB', 'comma', 'closeS', 'openS', 'doubleDot', 'semi']

    token_specification = [
        ("comment", r"/\*.*\*/"),
        ("indent", r'\n[ ]*'),
        ('commentLine', r'//.*'),
        ('newline', r'\n'),
        ('openB', '{'),
        ('closeB', '}'),
        ('openC', '\('),
        ('closeC', '\)'),
        ('f32', r'\d+\.\d+'),
        ('i32', r'\d+'),
        ('arrow', r'->'),
        ('equal',  r'=='),
        ('doublecolon', r'::'),
        ("colon", r":"),
        ("semi", r";"),
        ('ne', r'!='),
        ('assign',  r'='),
        ('openS', r'\['),
        ('closeS', r'\]'),
        ('assignPlus', r'\+='),
        ('assignSub', r'\-='),
        ('assignMul', r'\*='),
        ('assignDiv', r'\/='),
        ('operator',  r'[+*\/\-&><]|(\|>)'),
        ('line', r'\|'),
        ('identifier', r'[A-Za-z0-9_]+'),
        ('underscore', '_'),
        ('skip', r'[ \t]'),
        ("str", r'"(?:\\.|({.*})|[^"\\])*"'),
        ('doubleDot', '\.\.'),
        ('dot', '\.'),
        ('tab', '\t'),
        ('comma', ','),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line = 1

    pos = spos
    mo = get_token(s)
    lastIndent = 0
    lastTyp = None
    linePos = slinePos

    line = sline

    array = []

    while mo is not None:
        typ = mo.lastgroup

        next = get_token(s, mo.end())

        if typ == "indent" or typ == "newline":
            val = mo.group(typ)
            array.append(Token("\n", "symbol", line, pos))
            line += 1

            linePos = mo.end()

            if next == None:
                array.append(Token(0,"indent", line, pos))
                break
            if next.lastgroup == "indent":
                array.append(Token(lastIndent, "indent", line, pos ))
            else:
                array.append(Token(len(val)-1, "indent", line, pos))
                lastIndent = len(val)-1
        elif typ in ["str"]:
            val = mo.group(typ)
            if typ == "str":
                def notBack(iter):
                    if iter == 0: return True
                    if val[iter-1] != "\\": return True
                    return notBack(iter-1)

                start = 0
                inBrace = False
                tokens = []
                val = val[1:-1]
                bcount = 0
                shouldBe = 0
                for iter in range(len(val)):
                    i = val[iter]
                    if notBack(iter) and i == "{" and not inBrace:
                        tokens.append(Token('"'+val[start: iter]+'"', "str", line, pos))
                        inBrace = True
                        start = iter+1
                        shouldBe = bcount

                    if i == "{":
                        bcount += 1
                    elif notBack(iter) and i == "}":
                        bcount -= 1
                        if bcount == shouldBe and inBrace:
                            tokens.append(Token("concat", "operator", line, pos))
                            tokens.append(Token("(", "symbol", line, pos))

                            tokens += tokenize(val[start: iter], filename, pos, line, linePos)
                            tokens.append(Token(")", "symbol", line, pos))
                            tokens.append(Token("concat", "operator", line, pos))
                            start = iter + 1
                            inBrace = False

                tokens.append(Token('"'+val[start:]+'"', "str", line, pos))
                array += tokens

        elif typ != 'skip':
            val = mo.group(typ)
            if typ == 'identifier' and val in keywords:
                if val in ["true", "false"]:
                    typ = "bool"
                elif val in ["_"]:
                    typ = "symbol"
                else:
                    typ = "keyword"

            elif typ in special:
                typ = "symbol"
            elif typ == "equal" or typ == "mut" or typ == "ne":
                typ = "operator"

            if val != " ": array.append(Token(val, typ, line, pos))
            elif val == "\t":
                Error.compileError(filename[1], line, "tabs are not allowed")

        lastTyp = typ

        pos = mo.end() - linePos
        mo = next

    if spos == 0 and sline == 0:
        array.append(Token("\n", "symbol", line-1, pos))
        array.append(Token(0, "indent", line, pos))

    return array





