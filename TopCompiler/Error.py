from __future__ import print_function

__author__ = 'antonellacalvia'

import sys
import os

def compileError(filename, line, message):
    print("File \""+os.path.abspath(filename+".top")+"\", line "+str(line)+"\n\t"+message, file=sys.stderr)
    sys.exit()

def parseError(parser, message):
    filename = parser.filename
    package = parser.package

    token = parser.tokens[parser.iter]

    errorAst(message,  package, filename, token)

style = """"font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace, serif;
background-color: lightblue;
position: fixed; bottom: 0; margin: 0; width: 100%;
padding-top: 10px; padding-left: 30px;
" """


def errorAst(message, package, filename, token):
    html = '<div name=\"error\", style='+style+'>'

    err = ("File \"" + os.path.abspath("TopCompiler/" + package + "/" + filename + ".top") + "\", line " + str(
        token.line + 1) + "\n\t" + message[0].capitalize() + message[1:])+"\n"

    html += "<p>"+("File \"" + os.path.abspath("TopCompiler/" + package + "/" + filename + ".top") + "\", line " + str(
        token.line + 1) + "</p><p style=\"text-indent: 50px;\">"+message[0].capitalize() + message[1:])+"\n"+"</p><br>"

    f = open(os.path.abspath("src/"+ package + "/" + filename + ".top"))  # change to use already read version
    s = f.read()
    f.close()

    divided = s.split("\n")
    line = ("\n\t" + divided[token.line])
    err += line+"\n"
    html += "<p style=\"text-indent: 50px;\">"+line+"</p>"

    err += "\t"+((" " * token.column) + "^")+"\n"
    html += "<p style=\"text-indent: 50px;\">"+(("&nbsp" * token.column) + "^")+"</p></div>"

    from TopCompiler import topc
    topc.error = html.replace("\n", "").replace("\"", "\\\"")

    raise EOFError(err)

def error(message):
    print(message, file=sys.stderr)
    sys.exit()

    topc.error = '<div name=\"error\", style='+style+'><p style="text-indent: 50px;">' +message[1:] +'</p><div>'+topc.error

    raise EOFError(message)

def beforeError(prev, mesg):
    splited = str(prev).split("\n")

    header = splited[0]
    header += "\n\t"+mesg+ splited[1].replace("\t", "")
    header += "\n" + "\n".join(splited[2:])

    error(header)

def afterError(prev, mesg):
    splited = str(prev).split("\n")

    header = splited[0]
    header += "\n"+splited[1].replace("\t", "")+mesg
    header += "\n" + "\n".join(splited[2:])

    error(header)

def typeError(parser, type1, type2, mesg):
    parseError(parser, "type {0}, {1} and {2}".format(mesg, str(type1), str(type2)))