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

from TopCompiler import topc

def lex(stream, filename, modifiers, hotswap, lexed):
    for c in stream:
        if not hotswap or (hotswap and topc.modified(modifiers[c], c)):
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
        'int', 'float', 'none', 'bool', 'string', 'as',
        'break', 'continue',
        'true', 'false',
        'let',
        'ext',
        'type',
        'string',
        'var',
        "not", "or", "and",
        "lens",
        "match",
        "with",
        "from",
        "decoder",
    ]

    special = ["dollar", "bang", "arrow", "doublecolon", "line", "underscore", "assign", "assignPlus", "assignSub", "assignMul", "assignDiv", 'colon', 'dot', 'openC', 'openB', 'closeC', 'closeB', 'comma', 'closeS', 'openS', 'doubleDot', 'semi']

    token_specification = [
        ("comment", r"/\*([\s\S]*?)\*/"),
        ("indent", r'\n[ ]*'),
        ('commentLine', r'//.*'),
        ('newline', r'\n'),
        ('openB', '{'),
        ('closeB', '}'),
        ('openC', '\('),
        ('closeC', '\)'),
        ('hex', r'0[xX][0-9a-fA-F]+'),
        ('f32', r'\d*[\d_]*\d+(\.\d*[\d_]*(\d+)|f)'),
        ('i32', r'\d*[\d_]*(\d+)'),
        ('arrow', r'->'),
        ('equal',  r'=='),
        ('doublecolon', r'::'),
        ("colon", r":"),
        ("semi", r";"),
        ('ne', r'!='),
        ('assign',  r'='),
        ('whiteOpenS', r' +\['),
        ('openS', r'\['),
        ('closeS', r'\]'),
        ('assignPlus', r'\+='),
        ('assignSub', r'\-='),
        ('assignMul', r'\*='),
        ('assignDiv', r'\/='),
        ('operator',  r'(\|>|>>|<-)|[+*\/\-%><^\\]'),
        ('line', r'\|'),
        ('identifier', r'[^\d\W](\w|(-[^\d\W]))*'),  #[A-Za-z0-9_$]*([A-Za-z0-9_$]*-[A-Za-z_$]+)*
        ('underscore', '_'),
        ('skip', r'[ \t]'),
        ("str", r'"(?:\\.|({.*})|[^"\\])*"'),
        ('doubleDot', '\.\.'),
        ('dot', '\.'),
        ('tab', '\t'),
        ('comma', ','),
        ('bang', '!'),
        ('dollar', '\$'),
        ('set', '=>'),
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
        elif typ == "comment":
            val = mo.group(typ)
            c = mo.end()
            r = val.rfind("\n")
            linePos = c + r
            line += len(val) - len(val.replace("\n", ""))
            array.append(Token(val, "comment", line, pos ))
        elif typ in ["str"]:
            val = mo.group(typ)
            def notBack(iter):
                if iter == 0: return True
                if val[iter-1] != "\\": return True
                return not notBack(iter-1)

            start = 0
            inBrace = False
            tokens = []
            val = val[1:-1]
            bcount = 0
            shouldBe = 0
            v = list(val)
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
                        tokens.append(Token("concat", "operator", line, pos+start))
                        tokens.append(Token("(", "symbol", line, pos+start))

                        tokens += tokenize(val[start: iter], filename, pos+start, line, linePos)
                        tokens.append(Token(")", "symbol", line, pos+iter))
                        tokens.append(Token("concat", "operator", line, pos+iter))
                        start = iter + 1
                        inBrace = False
                elif i == "\n":
                    line += 1

            tokens.append(Token('"'+val[start:]+'"', "str", line, pos))
            array += tokens

        elif typ != 'skip' and not typ in ["comment", "commentLine"]:
            val = mo.group(typ)
            if typ == "identifier":
                def my_replace(match):
                    match = match.group()
                    return match[1].upper()

                val = re.sub(r'\-[A-Za-z]', my_replace, val)

            if typ == 'identifier' and val in keywords:
                if val in ["true", "false"]:
                    typ = "bool"
                elif val in ["_"]:
                    typ = "symbol"
                else:
                    typ = "keyword"
            elif typ == "f32":
                val = val[:-1]+".0" if val[-1] == "f" else val
            elif typ == "hex":
                typ = "i32"

            if typ == "i32" or typ == "f32":
                val = val.replace("_", "")

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





