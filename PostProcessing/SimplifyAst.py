import AST as Tree
from TopCompiler import Types

"""
def print(s):
    return
    if s == "Array.T_toStringByValue":
        print("shouldn''")
    realPrint(s)
"""

def callMethodCode(node, name, typ, parser, unary):
    isMethod = False
    if type(typ) is Types.Pointer and type(typ.pType) is Types.Alias:
        method = typ.pType.typ.hasMethod(parser, name, isP=True)
        if method:
            typ = typ.pType.typ
            isMethod = True

    elif type(typ) is Types.Alias:
        method = typ.typ.hasMethod(parser, name, isP= isMethod)
        if method:
            typ = typ.typ

    if not node.type.isType(Types.Pointer):
        name += "ByValue"


    length = 1 if unary else 2

    if type(typ) is Types.Pointer:
        typ = typ.pType

    package = "_global" if typ.package == "" else typ.package

    var = Tree.ReadVar(typ.normalName + "_" + name, True, node)
    var.package = package
    var.type = Types.FuncPointer([node.type] * length, node.type)

    while True:
        if typ.isType(Types.Pointer):
            typ = typ.pType
        else:
            break

    #if type(typ) in [Types.Struct, Types.Alias, Types.Enum]:
    var.replaced = typ.remainingGen

    return var


def simplifyArrRead(operator, iter, parser):
    readMethodName = callMethodCode(operator.nodes[0], "op_get", operator.nodes[0].type, parser, False)
    readMethodName.type.args[1] = operator.nodes[1].type
    readMethodName.type.returnType = operator.type
    # if operator.nodes[0].type.isType(Types.Pointer):
    #    readMethodName.replaced = operator.nodes[0].type.pType.remainingGen
    # else:
    #    readMethodName.replaced = operator.nodes[0].type.remainingGen

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

        # array = []

        for node in operator.nodes:
            func.addNode(node)
            # array.append(node.type)

        func.type = operator.type
        operator.owner.nodes[iter] = func

        return func

    typ = operator.nodes[0].type

    if typ.isType(Types.Pointer) and type(typ.pType.toRealType()) in [Types.I32, Types.Float, Types.Bool, Types.Char] and not (operator.kind in ["*", "&"] and operator.unary):
        for (c, i) in enumerate(operator.nodes):
            deref = Tree.Operator("*", i)
            deref.unary = True
            deref.type = typ.pType
            deref.opT = typ
            deref.owner = operator

            deref.addNode(i)

            operator.nodes[c] = deref
        typ = typ.pType.toRealType()

    if typ.isType(Types.String):
        func = Tree.FuncCall(operator)
        if operator.kind == "concat":
            r = Tree.ReadVar("String_op_addByValue", True, parser)
            # r.type = Types.FuncPointer([Types.String(0), Types.String(0)], Types.String(0))

            func.addNode(r)
            func.nodes[0].type = Types.String(0).hasMethod(parser, "op_add", isP=True)
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
            return overloaded(callMethodCode(operator.nodes[0], "op_add", typ, parser, operator.unary))
        elif operator.kind == "==":
            return overloaded(callMethodCode(operator.nodes[0], "op_eq", typ, parser, operator.unary))
        elif operator.kind == "!=":
            return overloaded(callMethodCode(operator.nodes[0], "op_ne", typ, parser, operator.unary))
    elif operator.overload and not typ.isType(Types.I32) and not typ.isType(Types.Float) and not typ.isType(Types.Bool) and not typ.isType(Types.Char):
        operator.name = Tree.get_overloads(operator.unary)[operator.kind]
        return overloaded(
            callMethodCode(operator.nodes[0], operator.name, operator.opT, parser,
                           operator.unary))
    else:
        operator.overload = False
        return operator

import copy


def splitPackageAndName(identifier):
    if identifier.startswith("_global"):
        return ("_global", identifier[len("_global") + 1:])
    else:
        return (identifier[:identifier.find("_")], identifier[identifier.find("_") + 1:])

from TopCompiler import Parser

class FuncSpecification:
    def __init__(self, identifier, funcStart, funcBrace, funcBody, replaced):
        self.funcStart = funcStart
        self.funcBrace = funcBrace
        self.funcBody = funcBody
        self.replaced = replaced

        self.identifier = identifier

    def replace(self, parser):
        def loop(ast, iter, owner):  # loop will copy
            newAST = copy.copy(ast)
            newAST.nodes = []
            for inner_iter, i in enumerate(ast.nodes):
                newAST.addNode(loop(i, inner_iter, newAST))

            if Types.isGeneric(newAST.type):
                newAST.type = Types.replaceT(newAST.type, self.replaced)

            if type(newAST) is Tree.Create and Types.isGeneric(newAST.varType):
                newAST.varType = Types.replaceT(newAST.varType, self.replaced)

            elif type(newAST) is Tree.FuncStart and Types.isGeneric(newAST.ftype):
                newAST.ftype = Types.replaceT(newAST.ftype, self.replaced)
            elif type(newAST) in [Tree.Sizeof, Tree.Offsetof] and Types.isGeneric(newAST.typ):
                newAST.typ = Types.replaceT(newAST.typ, self.replaced)
            elif type(newAST) is Tree.Typeof and newAST.type == Parser.IType:
                #print("hey")
                typeof = Tree.Typeof(ast, Types.replaceT(newAST.typ, self.replaced))

                cast = Tree.Cast.Cast(typeof.type, newAST.type, ast)
                cast.addNode(typeof)
                newAST = cast
            elif type(newAST) is Tree.Cast.Cast:  # @cleanup add for cast which is an operator for some reason
                newAST.f = Types.replaceT(newAST.f, self.replaced)
                newAST.to = Types.replaceT(newAST.to, self.replaced)
                newAST.type = newAST.to
                newAST.realName = copy.copy(newAST.realName)
            elif type(newAST) is Tree.For:
                newAST.condition_type = Types.replaceT(ast.condition_type, self.replaced)
            elif type(newAST) is Tree.Match:
                if newAST.guard:
                    newAST.place = owner.nodes[iter-1]
            elif type(newAST) is Tree.FuncCall:
                newAST.replaced = {name: Types.replaceT(newAST.replaced[name], self.replaced) for name in
                                   newAST.replaced}
            elif type(newAST) is Tree.Operator and newAST.kind == "&" and newAST.insertedCast:
                opT = Types.replaceT(newAST.nodes[0].type, self.replaced)
                if opT.isType(Types.Pointer):
                    return newAST.nodes[0]
            elif type(newAST) is Tree.Operator:
                newAST.opT = Types.replaceT(newAST.opT, self.replaced)

            return newAST

        # if self.identifier == "ecs_Store_index_is_active_ecs_Entity":
        # print("gadeem")

        funcStart = copy.copy(self.funcStart)
        funcStart.ftype = Types.replaceT(funcStart.ftype, self.replaced)
        funcBrace = loop(self.funcBrace, 0, None)
        funcBody = loop(self.funcBody, 0, None)
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
        p.addNode(funcBrace)
        p.addNode(funcBody)

        # if n == "sort_array_int":
        #    print("hey")

        simplifyAst(parser, p, specifications=parser.specifications[parser.package], dontGen=True)

        funcBody.owner = owner

        return (funcStart, funcBrace, funcBody)


import re


# credit to mmj, https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string


def multiple_replace(rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]))

    def replace(string):
        return pattern.sub(lambda x: rep_dict[x.group(0)], string).replace(".", "_")

    return replace


sanitize = multiple_replace(
    {" ": "_", "[": "_", "]": "_", "|": "p", "->": "_", "&": "r", ",": "c", "{": "b", "}": "b", ".": "_", ":": "_", "(": "p", ")": "p"})


def stringify(typ):
    # return typ
    # if type(typ) is Types.T:
    #    return typ.type.name
    # else:
    return str(typ)  # .name


def toUniqueID(package, funcName, replaced):
    keys = sorted(replaced.keys())
    joinedKeys = "_".join(stringify(replaced[key]) for key in keys)
    if joinedKeys == "":
        return package + "_" + funcName
    else:
        return package + "_" + funcName + "_" + sanitize(joinedKeys)


class Specifications:
    def __init__(self, root, inImports, genericFuncsFromDifferentPackage):
        self.funcs = {}
        self.root = root
        self.inImports = inImports
        self.genericFuncs = genericFuncsFromDifferentPackage
        self.delayed = {}
        self.funcsToBeProcessed = {}
        self.packageGenericFuncs = {}

    def addSpecification(self, package, funcName, replaced, forceFound=False):
        if package == "":
            package = "_global"

        if package == "reflection" and funcName == "typeof":
            return toUniqueID(package, funcName, replaced)

        fullName = package + "_" + funcName
        id = toUniqueID(package, funcName, replaced)

        if not fullName in self.genericFuncs:
            if forceFound: pass
            # raise EOFError("Could not find generic function " + fullName)
            self.delayed[fullName] = (package, funcName, replaced)
            return id

        (funcStart, funcBrace, funcBody) = self.genericFuncs[fullName]

        if id in self.inImports:
            return id
        if not id in self.funcs:
            self.funcs[id] = FuncSpecification(id, funcStart, funcBrace, funcBody, replaced)
            self.funcsToBeProcessed[id] = self.funcs[id]
            # print("adding specification", id)
        return id

    def addGenericFunc(self, package, name, funcStart, funcBrace, funcBody):
        self.genericFuncs[package + "_" + name] = (funcStart, funcBrace, funcBody)

    def genAST(self, parser):
        groups = []

        # print("gen ast")

        while (len(self.funcsToBeProcessed) > 0 or len(self.delayed) > 0):
            groups.append([])

            for key in list(self.delayed.keys()):
                (package, funcName, replaced) = self.delayed[key]
                self.addSpecification(package, funcName, replaced, forceFound=True)
                del self.delayed[key]

            _keys = list(self.funcsToBeProcessed.keys())

            for id in _keys:
                # if not id in self.funcsToBeProcessed: #this can happen cause specification replace might handle this func
                #    continue
                specification = self.funcsToBeProcessed[id]
                del self.funcsToBeProcessed[id]
                groups[-1].append(specification.replace(parser))

        # print("outputting")
        for group in reversed(groups):
            for (funcStart, funcBrace, funcBody) in group:
                # print(funcStart.name)
                self.root.addNode(funcStart)
                self.root.addNode(funcBrace)
                self.root.addNode(funcBody)

        # print("ending")


def isGenericMethod(ast):
    if ast.method:
        t = ast.ftype.args[0]
        if type(t) is Types.Pointer:
            g = t.pType.remainingGen
            return g
        else:
            return t.remainingGen

    return False


def isGenericFunc(ast):
    return ast.ftype.generic or isGenericMethod(ast)  # pass by reference


def resolveGeneric(parser, root):
    specifications = Specifications(root, {}, {})  # @cleanup add support for modules
    parser.specifications[parser.package] = specifications

    for (iter, ast) in enumerate(root.nodes):
        if type(ast) is Tree.FuncStart and isGenericFunc(ast):
            funcStart = ast
            funcBrace = ast.owner.nodes[iter + 1]
            funcBody = ast.owner.nodes[iter + 2]
            specifications.addGenericFunc(funcStart.package, funcStart.name, funcStart, funcBrace, funcBody)


class Replacer():
    def __init__(self):
        self.scope = [[]]

    def replace(self, ast, it):
        for scope in self.scope:
            for replacement in scope:
                a = replacement(ast)
                if not a is None:
                    ast.owner.nodes[it] = a
                    return a

        return ast

    def incrScope(self):
        self.scope.append([])

    def decrScope(self):
        self.scope.pop()

    def add(self, replacement):
        self.scope[-1].append(replacement)


def simplifyAst(parser, ast, specifications=None, dontGen=False):
    replacer = Replacer()
    real_ast = ast

    if not specifications:
        inImports = {}
        genericFuncs = {}
        specifications = parser.specifications[parser.package]

        specifications.packageGenericFuncs = specifications.genericFuncs

        for name in ["_global"] + list(parser.compiled):
            spec = parser.specifications[name]
            for i in spec.packageGenericFuncs:
                genericFuncs[i] = spec.genericFuncs[i]
            for i in spec.funcs:
                inImports[i] = spec.funcs[i]

        specifications.inImports = inImports
        specifications.genericFuncs = genericFuncs

    def simplify(ast, iter, upperDeleteQueue):
        deleteQueue = []
        originalAST = ast

        if type(ast) in [Tree.FuncBraceOpen]:
            replacer.incrScope()

        if type(ast) in [Tree.ReadVar]:
            ast = replacer.replace(ast, iter)

        if not (type(ast) is Tree.FuncBody and len(ast.owner.nodes) >= 3 and isGenericFunc(ast.owner.nodes[iter - 2])):
            for (it, i) in enumerate(ast.nodes):
                simplify(i, it, deleteQueue)
        if type(ast) is Tree.Operator:
            ast = simplifyOperator(ast, iter, parser)
        elif type(ast) is Tree.ArrRead:
            ast = simplifyArrRead(ast, iter, parser)
            ast = ast.nodes[0]
            iter = 0

        elif type(ast) is Tree.Using:
            types = ast.extracted_fields
            methods = ast.extracted_methods

            wrapping = ast.nodes[0]
            varType = ast.nodes[0].varType

            def shouldReplace(a):
                if type(a) is Tree.ReadVar:
                    if a.name in types:
                        field = Tree.Field(a.name, varType, a)
                        field.field = a.name
                        field.type = types[a.name]
                        var = Tree.ReadVar(wrapping.name, False, a)
                        var.package = a.package
                        var.type = varType
                        field.addNode(var)
                        return field

                    if a.name in methods:
                        pass

            replacer.add(shouldReplace)

        elif type(ast) is Tree.Cast.Cast:
            if ast.to.isType(Types.Interface):
                toT = ast.to.toRealType()
                fromT = ast.f.toRealType()

                if type(fromT) is Types.Pointer:  # has to be but type checking this hasnt happened yet
                    fromT = fromT.pType

                    if fromT.remainingGen:
                        for name in toT.methods:
                            package = toT.package

                            newName = specifications.addSpecification(package, fromT.normalName + "_" + name,
                                                                      fromT.remainingGen)
                            ast.realName[name] = newName
                        # readVar.name = splitPackageAndName(newName)[1]

        elif type(ast) is Tree.For:
            condition = ast.condition_type
            ast.op_get = specifications.addSpecification(condition.package, condition.normalName + "_op_get",
                                                         condition.remainingGen)
        elif type(ast) is Tree.Array:
            ast = Tree.simplifyArray(parser, ast, iter)
        elif type(ast) is Tree.Match and ast.guard:
            for case in ast.nodes[1::2]:
                def loop(x):
                    if type(x) is Tree.ReadVar:
                        c = Tree.Create(x.name, x.type, parser)
                        c.package = x.package
                        ast.place.addNode(c)

                    nodes = x.nodes
                    if type(x) is Tree.FuncCall:
                        nodes = nodes[1:]

                    for i in nodes:
                        loop(i)

                loop(case)

        elif type(ast) is Tree.Field and ast.indexPackage:
            package = ast.nodes[0].package
            name = ast.field
            owner = ast.owner
            typ = ast.type

            ast = Tree.ReadVar(name, True, ast)
            ast.package = package
            ast.owner = owner
            ast.type = typ
            owner.nodes[iter] = ast

        if type(ast) is Tree.Generic:
            ast.owner.nodes[iter] = ast.nodes[0]
        elif type(ast) is Tree.FuncStart and isGenericFunc(ast):
            funcStart = ast
            funcBrace = ast.owner.nodes[iter + 1]
            funcBody = ast.owner.nodes[iter + 2]
            upperDeleteQueue.append(
                funcStart)  # remove funcStart, funcBrace, funcBody, since specialized version is useless
            upperDeleteQueue.append(funcBrace)
            upperDeleteQueue.append(funcBody)

        elif type(ast) is Tree.FuncCall and type(ast.nodes[0]) is Tree.ReadVar and not ast.nodes[0].name == "indexPtr" and ast.nodes[0].isGlobal:
            readVar = ast.nodes[0]
            if readVar.replaced:  # for method calls
                if readVar.name.endswith("ByValue"):
                    newName = specifications.addSpecification(readVar.package, readVar.name[:-7],
                                                              {**readVar.replaced, **ast.replaced})
                    readVar.name = splitPackageAndName(newName)[
                                       1] + "ByValue"  # remove package which will be added later
                else:
                    newName = specifications.addSpecification(readVar.package, readVar.name,
                                                              {**readVar.replaced, **ast.replaced})
                    readVar.name = splitPackageAndName(newName)[1]  # remove package which will be added later
            elif readVar.type.generic and Tree.funcIsCase(ast):
                newName = toUniqueID(readVar.package, readVar.name, ast.replaced)
                readVar.name = splitPackageAndName(newName)[1]
            elif readVar.type.generic:
                newName = specifications.addSpecification(readVar.package, readVar.name, ast.replaced)
                readVar.name = splitPackageAndName(newName)[1]  # remove package which will be added later
            # elif type(ast) is Tree.Cast and type(ast.nodes[0]) is Tree.InitStruct and ast.fromT in [Types.Enum, Types.Struct] and Tree.Cast.notSpecified(ast.fromT):  @cleanup add optimization
            #    print("happens")
            #    ast.nodes[0].constructor = ast.toT
            readVar.replaced = {}
            ast.replaced = {}
        elif type(ast) is Tree.Field and ast.method:
            typ = ast.nodes[0].type
            struct = typ
            self = ast
            i = ast

            isP = False
            if type(typ) is Types.Pointer:
                typ = typ.pType
                isP = True

            if type(typ) is Types.Alias:
                method = typ.typ.hasMethod(parser, self.field, isP=isP)
                if method:
                    typ = typ.typ
                else:
                    method = typ.hasMethod(parser, self.field, isP=isP)
            else:
                method = typ.hasMethod(parser, self.field, isP=isP)

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

                    if type(typ) in [Types.Struct, Types.Alias, Types.Enum, Types.Array]:
                        r.replaced = typ.remainingGen
            #else:
            #    if self.using:
            #        field = None
            #        for using_field in typ.using:
            #            if self.field in typ.types[using_field].types:
            #                f = Tree.Field(0, typ.types[using_field], self)
            #                f.field = using_field
            #                f.type = typ.types[using_field]
            #                f.addNode(self.nodes[0])
            #
            #                self.nodes[0] = f
            #                f.owner = self


        if type(ast) in [Tree.FuncBody]:
            replacer.decrScope()

        for e in deleteQueue:
            ast.nodes.remove(e)

    simplify(ast, 0, [])
    if not dontGen:
        specifications.genAST(parser)