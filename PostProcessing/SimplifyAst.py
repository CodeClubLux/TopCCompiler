import AST as Tree
from TopCompiler import Types

def callMethodCode(node, name, type, parser, unary):
    length = 1 if unary else 2
    if type.isType(Types.Interface):
        field = Tree.Field(node)
        field.type = Types.FuncPointer([node.type] * length, node.type)
        field.field = name
        field.addNode(node)
        return field
    else:

        package = "_global" if type.package == "" else type.package
        var = Tree.ReadVar(type.normalName + "_" + name, True, node)
        var.package = package
        var.type = Types.FuncPointer([node.type] * length, node.type)
        return var

def simplifyOperator(operator, iter, parser):
    def overloaded(methodName):
        func = Tree.FuncCall(operator)
        func.addNode(methodName)

        array = []

        for node in operator.nodes:
            func.addNode(node)
            array.append(node.type)

        func.type = operator.type
        operator.owner.nodes[iter] = func

    if operator.type.isType(Types.String):
        func = Tree.FuncCall(operator)

        if operator.kind == "concat":
            func.addNode(Tree.ReadVar("String_op_add", True, parser))
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
        elif operator.kind == "+":
            overloaded(callMethodCode(operator.nodes[0], "op_add", operator.type, parser, operator.unary))
    elif operator.overload:
        overloaded(callMethodCode(operator.nodes[0], operator.name[operator.name.find("_")+1:], operator.type, parser, operator.unary))

import copy

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

            return newAST

        funcStart = copy.copy(self.funcStart)
        funcBrace = loop(self.funcBrace)
        funcBody = loop(self.funcBody)

        n = self.identifier[self.identifier.find("_")+1:] #remove package as it will be added later

        funcStart.name = n
        funcBody.name = n
        if funcBody.method:
            funcBody.types = [Types.replaceT(i, self.replaced) for i in funcBody.types]

        owner = funcBody.owner
        p = Tree.PlaceHolder(funcBody)
        p.addNode(funcBody)

        package = self.identifier[0:self.identifier.find("_")]

        simplifyAst(parser, p, parser.specifications[package])

        funcBody.owner = owner

        return (funcStart, funcBrace, funcBody)


import re

#credit to mmj, https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string


def multiple_replace(rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    def replace(string):
        return pattern.sub(lambda x: rep_dict[x.group(0)], string)
    return replace

sanitize = multiple_replace({" ": "_", "[": "_", "]": "_", ".": "_"})

def stringify(typ):
    if type(typ) is Types.T:
        return typ.type.name
    else:
        return typ.name

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
        return id

    def addGenericFunc(self, package, name, funcStart, funcBrace, funcBody):
        self.genericFuncs[package+ "_" + name] = (funcStart, funcBrace, funcBody)

    def genAST(self, parser):
        for key in self.delayed:
            (package, funcName, replaced) = self.delayed[key]
            self.addSpecification(package, funcName, replaced, forceFound=True)

        _keys = list(self.funcsToBeProcessed.keys())
        for id in _keys:
            specification = self.funcsToBeProcessed[id]
            del self.funcsToBeProcessed[id]
            (funcStart, funcBrace, funcBody) = specification.replace(parser)
            self.root.addNode(funcStart)
            self.root.addNode(funcBrace)
            self.root.addNode(funcBody)

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

def simplifyAst(parser, ast, specifications=None):
    if not specifications:
        inImports = {}
        genericFuncs = {}
        specifications = parser.specifications[parser.package]

        for name in parser.compiled:
            spec = parser.specifications[name]
            for i in spec.genericFuncs:
                genericFuncs[i] = spec.genericFuncs[i]
            for i in spec.funcs:
                inImports[i] = spec.funcs[i]

        specifications.inImports = inImports
        specifications.genericFuncs = genericFuncs

    def simplify(ast, iter, upperDeleteQueue):
        deleteQueue = []
        if not (type(ast) is Tree.FuncBody and len(ast.owner.nodes) >= 3 and isGenericFunc(ast.owner.nodes[iter-2])):
            for (it, i) in enumerate(ast.nodes):
                simplify(i, it, deleteQueue)

        if type(ast) is Tree.Operator:
            simplifyOperator(ast, iter, parser)

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
                    readVar.name = newName[newName.find("_") + 1:] + "ByValue"  # remove package which will be added later
                else:
                    newName = specifications.addSpecification(readVar.package, readVar.name, {**readVar.replaced, **ast.replaced})
                    readVar.name = newName[newName.find("_")+1:] #remove package which will be added later
                    print(readVar.name)
            elif readVar.type.generic:
                newName = specifications.addSpecification(readVar.package, readVar.name, ast.replaced)
                readVar.name = newName[newName.find("_") + 1:]  # remove package which will be added later
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

                r = Tree.ReadVar(name, self.type, self)
                r.type = self.type
                r.package = package
                r.owner = self.owner

                if not type(self.nodes[0].type) is Types.Pointer:
                    r.name += "ByValue"

                if type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i:
                    self.owner.nodes[0] = r
                    self.owner.nodes.insert(1, self.nodes[0])
                    if type(typ) in [Types.Struct, Types.Alias, Types.Enum]:
                        r.replaced = self.nodes[0].type.gen

        for e in deleteQueue:
            ast.nodes.remove(e)

    simplify(ast, 0, [])
    specifications.genAST(parser)