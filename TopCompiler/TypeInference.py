from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import Scope
from TopCompiler import ElseExpr
from TopCompiler import Types
import copy
from TopCompiler import MethodParser

def infer(parser, tree):
    varTypes = {}
    def loop(n):
        count = 0
        for i in n:
            if type(i) is Tree.FuncStart:
                Scope.incrScope(parser)
            elif type(i) in [Tree.If, Tree.While]:
                Scope.incrScope(parser)

            if not i.isEnd():
                loop(i)

            if type(i) is Tree.CreateAssign:
                if i.nodes[0].varType is None:
                    i.nodes[0].varType = i.nodes[1].nodes[0].type
                    if i.nodes[0].attachTyp:
                        MethodParser.addMethod(i, parser, i.nodes[0].attachTyp, i.nodes[0].name, i.nodes[1].nodes[0].type)
                        i.nodes[0].isGlobal = True
                    else:
                        Scope.addVar(i, parser, i.nodes[0].name, Scope.Type(i.nodes[0].imutable, i.nodes[1].nodes[0].type))
                        i.nodes[0].isGlobal = Scope.isGlobal(parser, i.nodes[0].package, i.nodes[0].name)
            elif type(i) is Tree.FuncBody:
                Scope.decrScope(parser)

            elif type(i) is Tree.Create:
                if not i.varType is None:
                    Scope.addVar(i, parser, i.name, Scope.Type(i.imutable, i.varType))
                    i.isGlobal = Scope.isGlobal(parser, i.package, i.name)

            elif type(i) is Tree.ReadVar:
                if i.name in parser.imports:
                    if not type(i.owner) is Tree.Field:
                        i.error("expecting .")
                elif type(i.type) is Tree.Type:
                    i.error("unexpected type "+str(i.type))

                i.type = Scope.typeOfVar(i, parser, i.package, i.name)
                self = i
                self.imutable = not Scope.isMutable(parser, self.package, self.name)
                self.isGlobal = Scope.isGlobal(parser, self.package, self.name)
                self.package = Scope.packageOfVar(parser, parser.package, self.name)
            elif type(i) is Tree.Field:
                typ = i.nodes[0].type
                t = i.nodes[0]

                if type(typ) is Types.Package:
                    i.indexPackage = True
                    i.type = Scope.typeOfVar(i, parser, i.nodes[0].name, i.field)

                    i.nodes[0].package = i.nodes[0].name
                    i.nodes[0].name = ""
                else:
                    struct = typ

                    self = i
                    try:
                        i.type = struct.types[self.field]
                    except KeyError:
                        try:
                            method = struct.hasMethod(parser, self.field)
                        except:
                            print("")

                        if not method:
                            self.error(typ.name + " has no field " + self.field)

                        self.type = method

                        r = Tree.ReadVar(typ.normalName+"_"+self.field, self.type, self)
                        r.type = self.type
                        r.package = typ.package if not typ.package == "_global" else ""
                        r.owner = self.owner

                        if type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i:
                            self.owner.nodes[0] = r
                            self.owner.nodes.insert(1, self.nodes[0])
                        elif type(i.type) is Types.FuncPointer:
                            bind = Tree.Bind(r, self.nodes[0], self)
                            self.owner.nodes[0] = bind
                            bind.owner = self.owner
                            bind.type = Types.FuncPointer(self.type.args[1:], self.type.returnType)

            elif type(i) is Tree.Operator:
                if i.kind == "|>":
                    self = i

                    a = self.nodes[0].type
                    b = self.nodes[1].type

                    if not type(a) is Types.FuncPointer:
                        self.nodes[0].error("function chain operator works on functions only")
                    if not type(b) is Types.FuncPointer:
                        self.nodes[1].error("function chain operator works on functions only")

                    if [a.returnType] != b.args:
                        self.nodes[1].error("function arguments don't match returnType of piped function, "+
                            str(a.returnType)+" and ("+", ".join([str(c) for c in b.args]))
                    self.type = Types.FuncPointer(a.args, b.returnType)
                elif i.kind == "concat":
                    stringable = Types.Interface(False, {"toString": Types.FuncPointer([], Types.String(0))})
                    for c in i:
                        stringable.duckType(parser,c.type,Tree.PlaceHolder(c),c,0)
                    i.type = Types.String(0)
                else:
                    if len(i.nodes) == 0:
                        import collections as coll
                        T = Types.T("t", Types.All)
                        i.type = Types.FuncPointer([T,T], T, coll.OrderedDict([("t", Types.All)]))
                        i.unary = False
                    else:
                        startType = i.nodes[0].type
                        for c in i.nodes[1:]:
                            if c.type != startType:
                                c.error("Type mismatch "+str(startType)+" and "+str(c.type))

                        i.type = startType
                        if i.kind in ["==", "!=", "not", "and", "or", "<", ">", "<=", ">="]:
                            i.type = Types.Bool()

                        if i.curry:
                            normal = 1 if i.unary else 2
                            i.type = Types.FuncPointer([startType] * (normal - len(i.nodes)), i.type)


            elif type(i) is Tree.FuncCall:
                partial = False

                if not type(i.nodes[0].type) is Types.FuncPointer:
                    i.nodes[0].error("type "+str(i.nodes[0].type)+" is not callable")

                args = i.nodes[0].type.args
                newArgs = []

                if len(args) < len(i.nodes)-1:
                    c = str(len(i.nodes) - 1 - len(args))
                    i.nodes[-1].error(("1 argument" if c == "1" else c+" arguments")+" too many")

                generics = {}
                for iter in range(len(i.nodes[1:])):
                    if type(i.nodes[iter+1]) is Tree.Under:
                        partial = True
                        newArgs.append(args[iter])
                    else:
                        normalTyp = args[iter]
                        myNode = i.nodes[iter+1]
                        normalNode = i

                        if Types.isGeneric(normalTyp):
                            normalTyp = resolveGen(normalTyp, myNode.type, generics)

                        normalTyp.duckType(parser, myNode.type, i, myNode, iter+1)

                if len(args) > len(i.nodes)-1:
                    i.curry = True
                    i.type = Types.FuncPointer(args[:len(args)-len(i.nodes)-1], i.nodes[0].type.returnType)
                elif not partial:
                    i.type = Types.replaceT(i.nodes[0].type.returnType, generics)
                else:
                    i.partial = True
                    i.type = Types.FuncPointer(newArgs, i.nodes[0].type.returnType)

            elif type(i) is Tree.If:
                ElseExpr.checkIf(parser, i)
            elif type(i) is Tree.Block:
                i.type = i.nodes[-1].type if len(i.nodes) > 0 else Types.Null()
            elif type(i) is Tree.Assign:
                if not (type(i.owner) is Tree.CreateAssign and i.owner.nodes[0].varType is None):
                    normalNode = i.owner.nodes[0] if i.init else i.nodes[1]
                    normalTyp = i.owner.nodes[0].varType if i.init else i.nodes[0].type
                    myNode = (i.nodes[0] if i.init else i.nodes[1])

                    normalTyp.duckType(parser, myNode.type, normalNode, myNode, (0 if i.init else 1))

            elif type(i) is Tree.Tuple:
                i.type = i.nodes[0].type
            elif type(i) is Tree.Array:
                arr = i

                if len(i.nodes) > 0:
                    if arr.init or arr.range:
                        if arr.nodes[0].type != Types.I32():
                            arr.nodes[0].error("expecting integer for range start, not "+str(arr.nodes[1].type))

                        if arr.range:
                            if arr.nodes[1].type != Types.I32():
                                arr.nodes[1].error("expecting integer for range end, not "+str(arr.nodes[1].type))
                            typ = Types.I32()
                        else:
                            typ = arr.nodes[1].type

                    else:
                        typ = arr.nodes[0].type
                        if typ == Types.Null():
                            arr.error("array elements must be non none")

                        for c in arr.nodes[1:]:
                            if typ != c.type:
                                c.error("type mismatch "+str(typ)+" and "+str(c.type))

                    arr.type = Types.Array(arr.mutable, typ)
            elif type(i) is Tree.InitPack:
                parser.imports.append(i.package)
            elif type(i) is Tree.InitStruct:
                s = i.s
                name = s.name
                args = s.fieldType

                if len(args) < len(i.nodes):
                    c = str(len(i.nodes) - 1 - len(args))
                    i.nodes[-1].error(("1 argument" if c == "1" else c+" arguments")+" too many")

                gen = {}
                for iter in range(len(i.nodes)):
                    normalTyp = args[iter]
                    myNode = i.nodes[iter]
                    normalNode = i

                    if Types.isGeneric(normalTyp):
                        normalTyp = resolveGen(normalTyp, myNode.type, gen)

                    normalTyp.duckType(parser, myNode.type, i, myNode, iter)

                i.type = Types.Struct(i.mutable, name, s.types, i.package, gen)

            elif type(i) is Tree.ArrRead:
                arrRead = i
                if len(arrRead.nodes) != 2 or not arrRead.nodes[1].type == Types.I32():
                    Error.parseError(parser, "expecting single integer index")

                arrRead.type = arrRead.nodes[0].type.elemT
            elif type(i) is Tree.Generic:
                if not Types.isGeneric(i.nodes[0].type):
                    i.nodes[0].error("expecting generic")

                gen = i.nodes[0].type.generic

                if len(gen) > len(i.generic):
                    i.error("missing "+str(len(gen)-len(i.generic))+" generic parameters")
                elif len(gen) < len(i.generic):
                    i.error(str(len(i.generic)-len(gen))+" too many generic parameters")

                v = list(gen.keys())
                replace = {v[index]: i for index, i in enumerate(i.generic)}

                i.type = Types.replaceT(i.nodes[0].type, replace)

            if type(i) in [Tree.If, Tree.While]:
                Scope.decrScope(parser)

            count += 1
    loop(tree)

def validate(parser, tree):
    for i in tree:
        if not i.isEnd():
            validate(parser, i)
        i.validate(parser)

def resolveGen(shouldBeTyp, normalTyp, generics):
    if type(shouldBeTyp) is Types.T:
        if shouldBeTyp.normalName in generics:
            return generics[shouldBeTyp.normalName]
        else:
            generics[shouldBeTyp.normalName] = normalTyp
            return shouldBeTyp
    elif type(shouldBeTyp) is Types.Array:
        t = Types.Array(shouldBeTyp.mutable, resolveGen(shouldBeTyp.elemT, normalTyp.elemT, generics))
        return t