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

        funcStart.name = self.identifier[self.identifier.find("_")+1:] #remove package as it will be added later
        simplifyAst(parser, funcBody)

        return (funcStart, funcBrace, funcBody)

def sanitize(str):
    return str.replace(" ", "_").replace("[", "_").replace("]", "_")

def toUniqueID(package, funcName, replaced):
    keys = sorted(replaced.keys())
    joinedKeys = "_".join(replaced[key].name for key in keys)
    return package + "_" + funcName + "_" + sanitize(joinedKeys)

class Specifications:
    def __init__(self, root, inImports, genericFuncsFromDifferentPackage):
        self.funcs = {}
        self.root = root
        self.inImports = inImports
        self.genericFuncs = genericFuncsFromDifferentPackage
        self.delayed = {}

    def addSpecification(self, package, funcName, replaced, forceFound= False):
        fullName = package+"_"+funcName
        id = toUniqueID(package, funcName, replaced)

        if not fullName in self.genericFuncs:
            if forceFound:
                raise EOFError("Could not find generic function" + fullName)
            self.delayed[fullName] = (package, funcName, replaced)
            return id

        (funcStart, funcBrace, funcBody) = self.genericFuncs[fullName]

        if id in self.inImports:
            return id
        if not id in self.funcs:
            self.funcs[funcName] = FuncSpecification(id, funcStart, funcBrace, funcBody, replaced)
        return id

    def addGenericFunc(self, package, name, funcStart, funcBrace, funcBody):
        self.genericFuncs[package+ "_" + name] = (funcStart, funcBrace, funcBody)

    def genAST(self, parser):
        for (package, funcName, replaced) in self.delayed:
            self.addSpecification(package, funcName, replaced, forceFound=True)

        for id in self.funcs:
            specification = self.funcs[id]
            (funcStart, funcBrace, funcBody) = specification.replace(parser)
            self.root.addNode(funcStart)
            self.root.addNode(funcBrace)
            self.root.addNode(funcBody)


def simplifyAst(parser, ast):
    specifications = Specifications(ast, {}, {}) #@cleanup add support for modules

    def simplify(ast, iter, upperDeleteQueue):
        deleteQueue = []
        if not (type(ast) is Tree.FuncBody and len(ast.owner.nodes) >= 3 and ast.owner.nodes[iter-2].ftype.generic):
            for (it, i) in enumerate(ast.nodes):
                simplify(i, it, deleteQueue)

        if type(ast) is Tree.Operator:
            simplifyOperator(ast, iter, parser)

        elif type(ast) is Tree.FuncStart and ast.ftype.generic:
            funcStart = ast
            funcBrace = ast.owner.nodes[iter+1]
            funcBody = ast.owner.nodes[iter+2]
            specifications.addGenericFunc(funcStart.package, funcStart.name, funcStart, funcBrace, funcBody)

            upperDeleteQueue.append(funcStart) #remove funcStart, funcBrace, funcBody, since specialized version is useless
            upperDeleteQueue.append(funcBrace)
            upperDeleteQueue.append(funcBody)
        elif type(ast) is Tree.FuncCall and type(ast.nodes[0]) is Tree.ReadVar and ast.nodes[0].type.generic:
            readVar = ast.nodes[0]

            newName = specifications.addSpecification(readVar.package, ast.nodes[0].name, ast.replaced)
            readVar.name = newName[newName.find("_")+1:] #remove package which will be added later

        for e in deleteQueue:
            ast.nodes.remove(e)

    simplify(ast, 0, [])
    specifications.genAST(parser)