import AST as Tree
from TopCompiler import Types

realPrint = print

"""
def print(s):
    return
    if s == "Array.T_toStringByValue":
        print("shouldn''")
    realPrint(s)
"""

def callMethodCode(node, name, typ, parser, unary):
    if not node.type.isType(Types.Pointer):
        name += "ByValue"

    if type(typ) is Types.Alias:
        method = typ.typ.hasMethod(parser, name)
        if method:
            typ = typ.typ

    length = 1 if unary else 2

    package = "_global" if typ.package == "" else typ.package
    var = Tree.ReadVar(typ.normalName + "_" + name, True, node)
    var.package = package
    var.type = Types.FuncPointer([node.type] * length, node.type)

    while True:
        if typ.isType(Types.Pointer):
            typ = typ.pType
        else:
            break

    if type(typ) in [Types.Struct, Types.Alias, Types.Enum]:
        var.replaced = typ.remainingGen

    return var

def simplifyArrRead(operator, iter, parser):
    readMethodName = callMethodCode(operator.nodes[0], "op_get", operator.nodes[0].type, parser, False)
    readMethodName.type.args[1] = operator.nodes[1].type
    readMethodName.type.returnType = operator.type
    if operator.nodes[0].type.isType(Types.Pointer):
        readMethodName.replaced = operator.nodes[0].type.pType.remainingGen
    else:
        readMethodName.replaced = operator.nodes[0].type.remainingGen

    deref = Tree.Operator("*", operator)
    deref.unary = True
    deref.type = operator.type
    deref.owner = operator.owner

    func = Tree.FuncCall(operator)
    func.type = Types.Pointer(operator.type)
    func.addNode(readMethodName)

    func.addNode(operator.nodes[0])
    func.addNode(operator.nodes[1])


    deref.addNode(func)

    operator.owner.nodes[iter] = deref

    return deref

def simplifyOperator(operator, iter, parser):
    def overloaded(methodName):
        func = Tree.FuncCall(operator)
        func.addNode(methodName)

        #array = []

        for node in operator.nodes:
            func.addNode(node)
            #array.append(node.type)

        func.type = operator.type
        operator.owner.nodes[iter] = func

        return func

    typ = operator.nodes[0].type

    if operator.type.isType(Types.String):
        func = Tree.FuncCall(operator)

        if operator.kind == "concat":
            func.addNode(Tree.ReadVar("String_op_addByValue", True, parser))
            func.nodes[0].type = Types.String(0).getMethod(parser, "op_add")
            func.nodes[0].package = "_global"

            for node in operator.nodes:
                if not node.type.isType(Types.String):
                    f = Tree.FuncCall(node)
                    f.type = Types.String(0)
                    f.addNode(callMethodCode(node, "toString", node.type, parser, operator.unary))
                    f.addNode(node)
                    func.addNode(f)
                else:
                    func.addNode(node)

            func.type = operator.type
            operator.owner.nodes[iter] = func
            return func
        elif operator.kind == "+":
            return overloaded(callMethodCode(operator.nodes[0], "op_add", operator.type, parser, operator.unary))
    elif operator.overload and not typ.isType(Types.I32) and not typ.isType(Types.Float):
        return overloaded(callMethodCode(operator.nodes[0], operator.name[operator.name.find("_")+1:], operator.opT, parser, operator.unary))

import copy

def splitPackageAndName(identifier):
    if identifier.startswith("_global"):
        return ("_global",  identifier[len("_global") + 1:])
    else:
        return (identifier[:identifier.find("_")], identifier[identifier.find("_")+1:])

class FuncSpecification:
    def __init__(self, identifier, funcStart, funcBrace, funcBody, replaced):
        self.funcStart = funcStart
        self.funcBrace = funcBrace
        self.funcBody = funcBody
        self.replaced = replaced

        self.identifier = identifier

    def replace(self, parser):
        def loop(ast): #loop will copy
            newAST = copy.copy(ast)
            newAST.nodes = []
            for i in ast.nodes:
                newAST.addNode(loop(i))

            if Types.isGeneric(newAST.type):
                newAST.type = Types.replaceT(newAST.type, self.replaced)

            if type(newAST) is Tree.Create and Types.isGeneric(newAST.varType):
                newAST.varType = Types.replaceT(newAST.varType, self.replaced)

            elif type(newAST) is Tree.FuncStart and Types.isGeneric(newAST.ftype):
                newAST.ftype = Types.replaceT(newAST.ftype, self.replaced)
            elif type(newAST) is Tree.Sizeof and Types.isGeneric(newAST.typ):
                newAST.typ = Types.replaceT(newAST.typ, self.replaced)
            elif type(newAST) is Tree.Cast.Cast: #@cleanup add for cast which is an operator for some reason
                newAST.f = Types.replaceT(newAST.f, self.replaced)
                newAST.to =  Types.replaceT(newAST.to, self.replaced)
                newAST.type = newAST.to
            elif type(newAST) is Tree.FuncCall:
                newAST.replaced = {name: Types.replaceT(newAST.replaced[name], self.replaced) for name in newAST.replaced}

            return newAST

        funcStart = copy.copy(self.funcStart)
        funcStart.ftype = Types.replaceT(funcStart.ftype, self.replaced)
        funcBrace = loop(self.funcBrace)
        funcBody = loop(self.funcBody)
        funcBody.returnType = funcStart.ftype.returnType


        inGlobal = False

        (package, n) = splitPackageAndName(self.identifier)

        funcStart.name = n
        funcStart.generated = True
        funcBody.name = n
        if funcBody.method:
            funcBody.types = [Types.replaceT(i, self.replaced) for i in funcBody.types]

        owner = funcBody.owner
        p = Tree.PlaceHolder(funcBody)
        p.addNode(funcBody)

        simplifyAst(parser, p, specifications= parser.specifications[parser.package], dontGen=True)

        funcBody.owner = owner

        return (funcStart, funcBrace, funcBody)


import re

#credit to mmj, https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string


def multiple_replace(rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]))
    def replace(string):
        return pattern.sub(lambda x: rep_dict[x.group(0)], string).replace(".", "_")

    return replace

sanitize = multiple_replace({" ": "_", "[": "_", "]": "_", "|": "p", "->": "_", "&": "r", ",": "c", "{": "b", "}": "b", ".": "_", ":": "_"})

def stringify(typ):
    #return typ
    #if type(typ) is Types.T:
    #    return typ.type.name
    #else:
    return str(typ) #.name

def toUniqueID(package, funcName, replaced):
    keys = sorted(replaced.keys())
    joinedKeys = "_".join(stringify(replaced[key]) for key in keys)
    return package + "_" + funcName + "_" + sanitize(joinedKeys)

class Specifications:
    def __init__(self, root, inImports, genericFuncsFromDifferentPackage):
        self.funcs = {}
        self.root = root
        self.inImports = inImports
        self.genericFuncs = genericFuncsFromDifferentPackage
        self.delayed = {}
        self.funcsToBeProcessed = {}

    def addSpecification(self, package, funcName, replaced, forceFound= False):
        if package == "":
            package = "_global"

        fullName = package+"_"+funcName
        id = toUniqueID(package, funcName, replaced)

        if not fullName in self.genericFuncs:
            if forceFound:
                raise EOFError("Could not find generic function " + fullName)
            self.delayed[fullName] = (package, funcName, replaced)
            return id

        (funcStart, funcBrace, funcBody) = self.genericFuncs[fullName]

        if id in self.inImports:
            return id
        if not id in self.funcs:
            self.funcs[id] = FuncSpecification(id, funcStart, funcBrace, funcBody, replaced)
            self.funcsToBeProcessed[id] = self.funcs[id]
            #print("adding specification", id)
        return id

    def addGenericFunc(self, package, name, funcStart, funcBrace, funcBody):
        self.genericFuncs[package+ "_" + name] = (funcStart, funcBrace, funcBody)

    def genAST(self, parser):
        groups = []

        #print("gen ast")

        while (len(self.funcsToBeProcessed) > 0 or len(self.delayed) > 0):
            groups.append([])

            for key in self.delayed:
                (package, funcName, replaced) = self.delayed[key]
                self.addSpecification(package, funcName, replaced, forceFound=True)
                del self.delayed[key]

            _keys = list(self.funcsToBeProcessed.keys())

            for id in _keys:
                #if not id in self.funcsToBeProcessed: #this can happen cause specification replace might handle this func
                #    continue
                specification = self.funcsToBeProcessed[id]
                del self.funcsToBeProcessed[id]
                groups[-1].append(specification.replace(parser))

        #print("outputting")
        for group in reversed(groups):
            for (funcStart, funcBrace, funcBody) in group:
                #print(funcStart.name)
                self.root.addNode(funcStart)
                self.root.addNode(funcBrace)
                self.root.addNode(funcBody)

        #print("ending")


def isGenericMethod(ast):
    if ast.method:
        t = ast.ftype.args[0]
        if type(t) is Types.Pointer:
            return t.pType.gen
        else:
            return t.gen

    return False


def isGenericFunc(ast):
    return ast.ftype.generic or isGenericMethod(ast) #pass by reference

def resolveGeneric(parser, root):
    specifications = Specifications(root, {}, {}) #@cleanup add support for modules
    parser.specifications[parser.package] = specifications

    for (iter, ast) in enumerate(root.nodes):
        if type(ast) is Tree.FuncStart and isGenericFunc(ast):
            funcStart = ast
            funcBrace = ast.owner.nodes[iter + 1]
            funcBody = ast.owner.nodes[iter + 2]
            specifications.addGenericFunc(funcStart.package, funcStart.name, funcStart, funcBrace, funcBody)

def simplifyAst(parser, ast, specifications=None, dontGen=False):
    if not specifications:
        inImports = {}
        genericFuncs = {}
        specifications = parser.specifications[parser.package]

        for name in ["_global"] + list(parser.compiled):
            spec = parser.specifications[name]
            for i in spec.genericFuncs:
                genericFuncs[i] = spec.genericFuncs[i]
            for i in spec.funcs:
                inImports[i] = spec.funcs[i]

        specifications.inImports = inImports
        specifications.genericFuncs = genericFuncs

    def simplify(ast, iter, upperDeleteQueue):
        deleteQueue = []
        originalAST = ast

        if not (type(ast) is Tree.FuncBody and len(ast.owner.nodes) >= 3 and isGenericFunc(ast.owner.nodes[iter-2])):
            for (it, i) in enumerate(ast.nodes):
                simplify(i, it, deleteQueue)
        if type(ast) is Tree.Operator:
            ast = simplifyOperator(ast, iter, parser)
        elif type(ast) is Tree.ArrRead:
            ast = simplifyArrRead(ast, iter, parser)
            ast = ast.nodes[0]
            iter = 0
        elif type(ast) is Tree.Array:
            ast = Tree.simplifyArray(parser, ast, iter)
        if type(ast) is Tree.Generic:
            ast.owner.nodes[iter] = ast.nodes[0]
        elif type(ast) is Tree.FuncStart and isGenericFunc(ast):
            funcStart = ast
            funcBrace = ast.owner.nodes[iter+1]
            funcBody = ast.owner.nodes[iter+2]
            upperDeleteQueue.append(funcStart) #remove funcStart, funcBrace, funcBody, since specialized version is useless
            upperDeleteQueue.append(funcBrace)
            upperDeleteQueue.append(funcBody)
        elif type(ast) is Tree.FuncCall and type(ast.nodes[0]) is Tree.ReadVar:
            readVar = ast.nodes[0]

            if readVar.replaced: #for method calls
                if readVar.name.endswith("ByValue"):
                    newName = specifications.addSpecification(readVar.package, readVar.name[:-7], {**readVar.replaced, **ast.replaced})
                    readVar.name = splitPackageAndName(newName)[1] + "ByValue"  # remove package which will be added later
                else:
                    newName = specifications.addSpecification(readVar.package, readVar.name, {**readVar.replaced, **ast.replaced})
                    readVar.name = splitPackageAndName(newName)[1] #remove package which will be added later
            elif readVar.type.generic and Tree.funcIsCase(ast):
                newName = toUniqueID(readVar.package, readVar.name, ast.replaced)
                readVar.name = splitPackageAndName(newName)[1]
            elif readVar.type.generic:
                newName = specifications.addSpecification(readVar.package, readVar.name, ast.replaced)
                readVar.name = splitPackageAndName(newName)[1]  # remove package which will be added later
        #elif type(ast) is Tree.Cast and type(ast.nodes[0]) is Tree.InitStruct and ast.fromT in [Types.Enum, Types.Struct] and Tree.Cast.notSpecified(ast.fromT):  @cleanup add optimization
        #    print("happens")
        #    ast.nodes[0].constructor = ast.toT

        elif type(ast) is Tree.Field:
            typ = ast.nodes[0].type
            struct = typ
            self = ast
            i = ast

            if type(typ) is Types.Alias:
                method = struct.typ.hasMethod(parser, self.field)
                if method:
                    typ = struct.typ

                else:
                    method = struct.hasMethod(parser, self.field)
            else:
                method = struct.hasMethod(parser, self.field)

            if method:
                self.type = method
                name = typ.normalName + "_" + self.field
                package = typ.package if not typ.package == "_global" else ""

                if type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i:
                    r = Tree.ReadVar(name, self.type, self)
                    if not type(self.nodes[0].type) is Types.Pointer:
                        r.name += "ByValue"

                    r.type = self.type
                    r.package = package
                    r.owner = self.owner

                    self.owner.nodes[0] = r
                    self.owner.nodes.insert(1, self.nodes[0])
                    while True:
                        if typ.isType(Types.Pointer):
                            typ = typ.pType
                        else:
                            break

                    if type(typ) in [Types.Struct, Types.Alias, Types.Enum]:
                        r.replaced = typ.remainingGen

        for e in deleteQueue:
            ast.nodes.remove(e)

    simplify(ast, 0, [])
    if not dontGen:
        specifications.genAST(parser)