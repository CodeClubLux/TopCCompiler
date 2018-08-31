__author__ = 'antonellacalvia'


from TopCompiler import Parser
from TopCompiler import Error
from TopCompiler import Types

class Type :
    def __init__(self, imutable, type, target= "full"):
        self.imutable = imutable
        self.type = type

    def __repr__(self):
        return str(self.type)

class Alias:
    def __init__(self, newPackage, realPackage, name, parser):
        self.newPackage = newPackage
        self.package = realPackage
        self.name = name
        self.parser = parser

    @property
    def imutable(self):
        return not isMutable(self.parser, self.package, self.name)

    @property
    def type(self):
        return typeOfVar(self.parser, self.parser, self.package, self.name)

    @type.setter
    def type(self, newTyp):
        changeType(self.parser, self.name, newTyp)

def addAlias(place, newPackage, realPackage, realName, name, parser):
    a = Alias(newPackage, realPackage, realName, parser)
    addVar(place, parser, name, a)

def incrScope(parser):
    parser.scope[parser.package].append({})

def addVar(node, parser, name, type, _global=False):
    if not parser.repl and varExists(parser, parser.package, name):
        node.error( "variable "+name+" already exists")

    if _global:
        parser.scope[parser.package][0][name] = type
    else:
        if len(parser.scope[parser.package]) == 0:
            print("error")
        else:
            parser.scope[parser.package][-1][name] = type

def addFunc(node, parser, name, typ, imutable= True):
    if not parser.repl and varExists(parser, parser.package, name):
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

    if name in parser.imports:
        return True

    for i in parser.scope[package]:
        if name in i:
            return True

    return False

def changeType(parser, name, newType):
    for i in parser.scope[parser.package]:
        try:
            i[name].type = newType
            return
        except: pass

def isMutable(parser, package, name):
    if name in parser.imports: return False
    if package == parser.package:
        for i in parser.scope["_global"]:
            if name in i:
                return i[name].imutable

    if package == "": package = "_global"

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

    if package == "": package = "_global"

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

    for i in parser.scope[package]:
        try:
            if type(i[name]) is Alias:
                return i[name].package
            return package
        except: pass

    return package

def isGlobal(parser, package, name):
    if name in parser.imports: return True
    if package == parser.package:
        if name in parser.scope["_global"][0]: return True

    if package == "": package = "_global"
    return name in parser.scope[package][0]

def addPackage(parser, name):
    if not name in parser.scope:
        parser.scope[name] = [{}]
        parser.func[name] = {}
        parser.structs[name] = {}
        parser.interfaces[name] = {}
        parser.contextFields[name] = {}






