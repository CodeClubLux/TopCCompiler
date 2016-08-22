__author__ = 'antonellacalvia'


from .Parser import *
from .Error import *
from .Types import *

class Type :
    def __init__(self, imutable, type):
        self.imutable = imutable
        self.type = type

def incrScope(parser):
    parser.scope[parser.package].append({})

def addVar(node, parser, name, type):

    if varExists(parser, parser.package, name):
        node.error( "variable "+name+" already exists")

    parser.scope[parser.package][-1][name] = type

def addFunc(node, parser, name, typ, imutable= True):
    if varExists(parser, parser.package, name):
        node.error("function "+name+" already exists")

    parser.scope[parser.package][-2][name] = Type(type= typ, imutable= imutable)
    return

def decrScope(parser):
    parser.scope[parser.package].pop()

def varExists(parser, package, name):
    if package == parser.package:
        for i in parser.scope["_global"]:
            if name in i:
                return True

    for i in parser.scope[package]:
        if name in i:
            return True
    return False

def changeType(parser, name, newType):
    for i in parser.scope[parser.package]:
        try:
            i[name].type = newType
        except: pass

def isMutable(parser, package, name):
    if name in parser.imports: return False
    if package == parser.package:
        for i in parser.scope["_global"]:
            if name in i:
                return i[name].imutable

    for i in parser.scope[package]:
        try:
            return not i[name].imutable
        except KeyError: pass

def typeOfVar(node, parser, package, name):
    if name in parser.imports: return Types.Package()
    if package == parser.package:
        for i in parser.scope["_global"]:
            if name in i:
                return i[name].type

    for i in parser.scope[package]:
        try:
            return i[name].type
        except: pass
    node.error("variable "+name+" does not exist")

def packageOfVar(parser, package, name):
    if name in parser.imports: return ""
    if package == parser.package:
        for i in parser.scope["_global"]:
            if name in i:
                return ""

    return package

def isGlobal(parser, package, name):
    if name in parser.imports: return True
    if package == parser.package:
        if name in parser.scope["_global"][0]: return True
    return name in parser.scope[package][0]

def addPackage(parser, name):
    parser.scope[name] = [{}]
    parser.func[name] = {}
    parser.structs[name] = {}
    parser.interfaces[name] = {}




