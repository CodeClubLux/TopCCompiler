from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import ExprParser
from TopCompiler import Scope
from TopCompiler import ElseExpr
from TopCompiler import Types
import copy
from TopCompiler import MethodParser
from TopCompiler import Struct
from TopCompiler import Enum

def infer(parser, tree):
    varTypes = {}
    sc = parser.sc
    def loop(n, o_iter):
        count = 0
        for i in n:
            if type(n) is Tree.Root:
                o_iter += 1

            if not sc and type(i) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
                count += 1
                continue

            if type(i) is Tree.FuncStart:
                if not type(n) is Tree.Root:
                    Scope.addVar(i, parser, i.name, Scope.Type(True, i.ftype))
                Scope.incrScope(parser)

            elif type(i) in [Tree.Block, Tree.While]:
                Scope.incrScope(parser)

            if not (i.isEnd() or type(i) is Tree.MatchCase or (type(i) is Tree.Block and type(i.owner) is Tree.Match)):
                if not type(i) is Tree.Lambda:
                    loop(i, o_iter)

            if type(i) is Tree.Match:
                typ = i.nodes[0].type
                first = False
                for c in range(1,len(i.nodes),2):
                    body = i.nodes[c+1]

                    Scope.incrScope(parser)
                    Enum.checkCase(parser, i.nodes[c].nodes[0], typ, True)
                    loop(body, o_iter)
                    body.type = body.nodes[-1].type if len(body.nodes) > 0 else Types.Null()
                    Scope.decrScope(parser)
                    if first:
                        if body.type != first:
                            (body.nodes[-1] if len(body.nodes) > 0 else body).error(
                                "type mismatch in arms of match, " + str(body.type) + " and " + str(first))
                    else:
                        if len(i.nodes[2].nodes) > 0:
                            first = i.nodes[2].nodes[-1].type
                        else:
                            first = Types.Null()
                        i.nodes[2].type = first

                Enum.missingPattern(typ, i)
                i.type = first if first else Types.Null()

            elif type(i) is Tree.CreateAssign:
                if i.nodes[0].varType is None and i.nodes[0].name != "_":
                    if i.extern:
                        i.error("expecting type declaration, for external variable declaration")
                    i.nodes[0].varType = i.nodes[1].nodes[0].type

                    if i.nodes[0].attachTyp:
                        MethodParser.addMethod(i, parser, i.nodes[0].attachTyp, i.nodes[0].name, i.nodes[1].nodes[0].type)
                        i.nodes[0].isGlobal = True
                    else:
                        Scope.addVar(i, parser, i.nodes[0].name, Scope.Type(i.nodes[0].imutable, i.nodes[1].nodes[0].type, i.global_target))
                        i.nodes[0].isGlobal = Scope.isGlobal(parser, i.nodes[0].package, i.nodes[0].name)
                if i.global_target != parser.global_target:
                    #print(i.nodes[0].name)
                    Scope.changeTarget(parser, i.nodes[0].name, i.global_target)
                    #print("this variable can only be used in a specific target", i.global_target)
            elif type(i) is Tree.FuncBody:
                Scope.decrScope(parser)
                def check(n, _i):
                    for c in n:
                        if type(c) is Tree.FuncCall:
                            if c.nodes[0].type.do and not _i.do and not c.partial and not c.curry:
                                c.nodes[0].error("cannot call function with side effects in a pure function")

                        if type(c) is Tree.FuncBody:
                            check(c, c)

                        elif not c.isEnd():
                            check(c, _i)
                check(i, i)
                if i.global_target != parser.global_target:
                    #print(i.name)
                    Scope.changeTarget(parser, i.name, i.global_target)
                    #print("this function can only be used in a specific target", i.global_target)

            elif type(i) is Tree.Create:
                if not i.varType is None:
                    Scope.addVar(i, parser, i.name, Scope.Type(i.imutable, i.varType, i.owner.global_target))
                    i.isGlobal = Scope.isGlobal(parser, i.package, i.name)

            elif type(i) is Tree.ReadVar:
                if i.name == "newAtom":
                    if not (type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i and not i.owner.curry and not i.owner.partial):
                        i.error("expecting function call, with no currying or partial application")

                    if parser.atoms > 0:
                        i.error("can only have one atom per application")

                if not (type(i.owner) is Tree.Assign and type(i.owner.owner) is Tree.InitStruct and i.owner.nodes[0] == i):
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

                    target = Scope.targetOfVar(i, parser, parser.package, self.name)

                    if target != parser.global_target:
                        root = tree.nodes[o_iter]

                        if type(root) is Tree.FuncBody:
                            tree.nodes[o_iter-1].global_target = target
                            tree.nodes[o_iter-2].global_target = target

                        root.global_target = target

                    elif tree.nodes[o_iter].global_target != target and target != "full":
                        realT = tree.nodes[o_iter].global_target
                        i.error("variable "+i.name+" is bound to target "+realT+" however, this variable is from target "+target)

            elif type(i) is Tree.Field:
                def bind():
                    if type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i: return
                    typ = type(i.type)

                    if typ is Types.FuncPointer:
                        if not type(i.nodes[0].type) in [Types.Struct]:
                            bind = Tree.ArrBind(i.field, self.nodes[0], self)
                            bind.type = i.type
                        else:
                            bind = Tree.Bind(r, self.nodes[0], self)
                            bind.type = Types.FuncPointer(self.type.args[1:], self.type.returnType, generic= self.type.generic, do= self.type.do)
                        self.owner.nodes[count] = bind
                        bind.owner = self.owner


                typ = i.nodes[0].type
                t = i.nodes[0]

                if type(typ) is Types.Package:
                    i.indexPackage = True
                    i.type = Scope.typeOfVar(i, parser, i.nodes[0].name, i.field)

                    target = Scope.targetOfVar(i, parser, i.nodes[0].name, i.field)

                    if target != parser.global_target:
                        root = tree.nodes[o_iter]

                        if type(root) is Tree.FuncBody:
                            tree.nodes[o_iter-1].global_target = target
                            tree.nodes[o_iter-2].global_target = target

                        root.global_target = target

                    i.nodes[0].package = i.nodes[0].name
                    i.nodes[0].name = ""
                else:
                    if type(typ) is Types.FuncPointer:
                        i.error("type "+str(typ) + " has no field " + i.field)

                    struct = typ

                    self = i
                    try:
                        i.type = struct.types[self.field]

                        if type(i.nodes[0].type) is Types.Array:
                            bind()
                    except KeyError:
                        method = struct.hasMethod(parser, self.field)

                        if not method:
                            self.error("type "+str(typ) + " has no field " + self.field)

                        self.type = method

                        r = Tree.ReadVar(typ.normalName + "_" + self.field, self.type, self)
                        r.type = self.type
                        r.package = typ.package if not typ.package == "_global" else ""
                        r.owner = self.owner

                        if type(i.owner) is Tree.FuncCall and i.owner.nodes[0] == i:
                            self.owner.nodes[0] = r
                            self.owner.nodes.insert(1, self.nodes[0])
                            count += 1
                        else: bind()

            elif type(i) is Tree.Operator:
                if i.kind == "|>" or i.kind == ">>":
                    self = i

                    if len(self.nodes) != 2:
                        self.error("chain operator cannot be curried")

                    a = self.nodes[0].type
                    b = self.nodes[1].type

                    if i.kind == ">>":
                        if not type(a) is Types.FuncPointer:
                            self.nodes[1].error("right argument must be a function")
                        a = a.returnType

                    if not type(b) is Types.FuncPointer:
                        self.nodes[1].error("left argument must be a function")

                    if len(b.args) != 1:
                        self.nodes[1].error("expecting one function argument that matches return type of piped function")

                    try:
                        b.args[0].duckType(parser, a, self.nodes[0], self.nodes[1], 1)
                    except EOFError as e:
                        if i.kind == ">>":
                            Error.beforeError(e, "Function combining with: ")
                        else:
                            Error.beforeError(e, "Function piping to: ")

                    if i.kind == ">>":
                        a = self.nodes[0].type
                        self.type = Types.FuncPointer(a.args, b.returnType, do= a.do or b.do, generic=a.generic)
                    else:
                        self.type = b.returnType
                elif i.kind == "<-":
                    if i.unary:
                        try:
                            meth = i.nodes[0].type.types["unary_read"]
                        except:
                            meth = i.nodes[0].type.hasMethod(parser, "unary_read")

                        if meth:
                            i.type = meth.returnType
                            i.opT = i.nodes[0].type
                    else:
                        try:
                            meth = i.nodes[0].type.types["unary_read"]
                        except:
                            meth = i.nodes[0].type.hasMethod(parser, "unary_read")

                elif i.kind == "concat":
                    stringable = Types.Interface(False, {"toString": Types.FuncPointer([], Types.String(0))})
                    for c in i:
                        stringable.duckType(parser,c.type,i,i,0)
                    i.type = Types.String(0)
                    i.partial = False
                    i.curry = False
                else:
                    if len(i.nodes) == 0:
                        import collections as coll
                        if i.kind in ["not", "or", "and"]:
                            T = Types.Bool()
                            gen = []
                        else:
                            T = Types.T("T", Types.All, "Operator")
                            gen = [("Operator.T", Types.All)]

                        returnT = T

                        if i.kind in ["==", "!=", "not", "and", "or", "<", ">", "<=", ">="]:
                            returnT = Types.Bool()

                        i.opT = T
                        i.type = Types.FuncPointer([T,T], returnT, coll.OrderedDict(gen))

                        if i.kind != "not":
                            i.unary = False
                    else:
                        partial = False
                        if type(i.nodes[0]) is Tree.Under:
                            partial = True
                            startType = False
                        else:
                            startType = i.nodes[0].type
                            if i.kind in ["not", "and", "or"]:
                                if startType != Types.Bool():
                                    i.nodes[0].error("logical operator "+i.kind+" only works on boolean")

                        for c in i.nodes[1:]:
                            if type(c) is Tree.Under:
                                partial = True
                            else:
                                if not partial and c.type != startType:
                                    c.error("Type mismatch "+str(startType)+" and "+str(c.type))
                                startType = c.type


                        i.partial = partial
                        typ = startType
                        if i.kind in ["==", "!=", "not", "and", "or", "<", ">", "<=", ">="]:
                            typ = Types.Bool()

                        if i.curry or i.partial:
                            normal = (1 if i.unary else 2) - len(i.nodes)
                            for c in i.nodes:
                                if type(c) is Tree.Under:
                                    normal += 1

                            if not startType:
                                import collections as coll
                                if i.kind in ["not", "or", "and"]:
                                    T = Types.Bool()
                                    gen = []
                                else:
                                    T = Types.T("t", Types.All, "Operator")
                                    gen = [("t", Types.All)]
                                typ = Types.FuncPointer([T,T], T, coll.OrderedDict(gen))

                                if normal == (1 if i.unary else 2):
                                    i.partial = False
                                    i.curry = True
                                    i.nodes = []
                            else:
                                typ = Types.FuncPointer([startType] * normal, typ)

                        i.type = typ
                        i.opT = startType



            elif type(i) is Tree.FuncCall:
                c = i
                if i.nodes[0].name == "newAtom":
                    i = i.nodes[0]
                    if parser.hotswap:
                        parser.atomTyp.duckType(parser, i.owner.nodes[1].type, i.owner.nodes[1], i, 0)

                        f = Tree.Field(0, i.owner.nodes[1].type, i)
                        f.field = "arg"
                        f.type = parser.atomTyp
                        r = Tree.ReadVar("previousState", True, i)
                        r.package = ""
                        f.addNode(r)

                        i.owner.nodes[1] = f
                        f.owner = i.owner

                    parser.atomTyp = i.owner.nodes[1].type
                    parser.atoms += 1

                i = c

                partial = False


                if not type(i.nodes[0].type) is Types.FuncPointer:
                    i.nodes[0].error("type "+str(i.nodes[0].type)+" is not callable")

                do = i.nodes[0].type.do
                returnType = i.nodes[0].type.returnType

                args = i.nodes[0].type.args
                newArgs = []

                if len(args) < len(i.nodes)-1:
                    c = str(len(i.nodes) - 1 - len(args))
                    i.error(("1 argument" if c == "1" else c+" arguments")+" too many, expecting "+str(len(args))+" arguments")

                generics = {}
                for iter in range(len(i.nodes[1:])):
                    if type(i.nodes[iter+1]) is Tree.Under:
                        partial = True
                        newArgs.append(iter)
                    else:
                        xnormalTyp = args[iter]
                        myNode = i.nodes[iter+1]
                        normalNode = i

                        if Types.isGeneric(xnormalTyp):
                            normalTyp = resolveGen(xnormalTyp, myNode.type, generics, parser)
                        else:
                            normalTyp = xnormalTyp

                        normalTyp.duckType(parser, myNode.type, i, myNode, iter + 1)

                        """
                        try:
                            normalTyp.duckType(parser, myNode.type, i, myNode, iter+1)
                        except EOFError as e:
                            normalTyp = resolveGen(xnormalTyp, myNode.type, {}, parser)
                            print(e)
                        """

                newArgs = [Types.replaceT(args[c], generics) for c in newArgs]

                if len(args) > len(i.nodes)-1:
                    i.curry = True
                    i.type = Types.FuncPointer([Types.replaceT(c, generics) for c in args[len(i.nodes)-1:]], Types.replaceT(i.nodes[0].type.returnType, generics), do= do)
                elif not partial:
                    i.type = Types.replaceT(i.nodes[0].type.returnType, generics)
                else:
                    i.partial = True
                    i.type = Types.FuncPointer(newArgs, Types.replaceT(i.nodes[0].type.returnType, generics), returnType, do= do)
            elif type(i) is Tree.If:
                ElseExpr.checkIf(parser, i)
            elif type(i) is Tree.Block:
                i.type = i.nodes[-1].type if len(i.nodes) > 0 else Types.Null()
            elif type(i) is Tree.Assign:
                if type(i.owner) is Tree.InitStruct:
                    pass
                elif not (type(i.owner) is Tree.CreateAssign and i.owner.nodes[0].varType is None):
                    if type(i.owner) is Tree.CreateAssign and i.owner.extern:
                        if not type(i.nodes[0].type) is Types.String:
                            i.error("expecting String")
                    else:
                        normalNode = i.owner.nodes[0] if i.init else i.nodes[1]
                        normalTyp = i.owner.nodes[0].varType if i.init else i.nodes[0].type
                        myNode = (i.nodes[0] if i.init else i.nodes[1])

                        normalTyp.duckType(parser, myNode.type, normalNode, myNode, (0 if i.init else 1))

            elif type(i) is Tree.Tuple:
                if len(i.nodes) == 0:
                    i.error("unexpected )")
                elif len(i.nodes) > 1:
                    i.type = Types.Tuple([c.type for c in i])
                else:
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

                        count = 0
                        for c in arr.nodes[1:]:
                            if typ != c.type:
                                try:
                                    typ.duckType(parser, c.type, i, c, count)
                                except EOFError as e:
                                    Error.beforeError(e, "Element type in array: ")

                            count += 1

                    arr.type = Types.Array(arr.mutable, typ)
            elif type(i) is Tree.InitPack:
                parser.imports.append(i.package)
            elif type(i) is Tree.InitStruct:
                unary = i.unary
                if not unary:
                    typ = i.constructor.type
                    i.typ = typ

                    assign = True
                    if type(typ) is Struct.Struct:
                        s = typ
                        assign = False
                        i.paramNames = Struct.offsetsToList(s.offsets)
                    elif type(typ) is Types.Struct:
                        assign = True
                        s = typ
                    else:
                        i.constructor.error("type "+str(typ)+" can not be used as a constructor")

                    i.s = s
                    name = s.name

                    if len(s.types) < len(i.nodes) - 1:
                        c = str(len(i.nodes) - 1 - len(s.types))
                        i.error(("1 argument" if c == "1" else c + " arguments") + " too many")
                    elif not assign and len(s.types) > len(i.nodes) - 1:
                        c = str(len(s.types) + 1 - len(i.nodes))
                        i.error(("1 argument" if c == "1" else c + " arguments") + " too few")
                else:
                    assign = True


                gen = {}
                randomOrder = False
                order = {}

                for iter in range(0 if unary else 1, len(i.nodes)):
                    if type(i.nodes[iter]) is Tree.Assign:
                        randomOrder = True
                    elif assign:
                        i.nodes[iter].error("expecting =")

                    if not randomOrder:
                        order[i.paramNames[iter-1]] = i.nodes[iter]
                        myNode = i.nodes[iter]
                        normalTyp = s.fieldType[iter-1]
                    else:
                        if not type(i.nodes[iter]) is Tree.Assign:
                            i.nodes[iter].error("positional argument follows keyword argument")
                        if i.nodes[iter].nodes[0].name in order:
                            i.nodes[iter].nodes[0].error("duplicate parameter")
                        order[i.nodes[iter].nodes[0].name] = i.nodes[iter]
                        myNode = i.nodes[iter].nodes[1]
                        xname = i.nodes[iter].nodes[0].name

                        if not unary:
                            try:
                                normalTyp = s.types[xname]
                            except KeyError:
                                i.nodes[iter].nodes[0].error("type "+str(s)+" does not have the field "+ xname)

                    normalNode = i

                    if not unary:
                        if Types.isGeneric(normalTyp):
                            normalTyp = resolveGen(normalTyp, myNode.type, gen, parser)

                        normalTyp.duckType(parser, myNode.type, i, myNode, iter)

                if not assign:
                    for c in order:
                        i.nodes[s.offsets[c]] = order[c]
                i.assign = assign

                if i.assign:
                    if unary:
                        types = {c: order[c].nodes[1].type for c in order}
                        i.type = Types.Interface(False, types)
                    else:
                        i.type = typ
                else:
                    i.type = Types.Struct(i.mutable, name, s.types, i.package, gen)

            elif type(i) is Tree.ArrRead:
                if not len(i.nodes) == 1:
                    if not type(i.nodes[0].type) is Types.Array:
                        i.nodes[0].error("Type "+str(i.nodes[0].type)+"is not indexable")
                    arrRead = i
                    if len(arrRead.nodes) != 2 or not arrRead.nodes[1].type == Types.I32():
                        i.nodes[1].error("expecting single integer index")

                    arrRead.type = arrRead.nodes[0].type.elemT
                else:
                    i.error("expecting integer expression")
            elif type(i) is Tree.Generic:
                if not Types.isGeneric(i.nodes[0].type):
                    i.nodes[0].error("expecting generic type")

                gen = i.nodes[0].type.generic

                if len(gen) > len(i.generic):
                    i.error("missing "+str(len(gen)-len(i.generic))+" generic parameters")
                elif len(gen) < len(i.generic):
                    i.error(str(len(i.generic)-len(gen))+" too many generic parameters")

                v = list(gen.keys())
                replace = {v[index]: c for index, c in enumerate(i.generic)}

                for index, c in enumerate(gen):
                    g = gen[c].type if type(gen[c]) is Types.T else gen[c]
                    g.duckType(parser, i.generic[index], i.nodes[0], i, 0)

                i.type = Types.replaceT(i.nodes[0].type, replace)

                #i.nodes[0].type.duckType(parser, i.type, i, i.nodes[0])
            elif type(i) is Tree.Lens:
                lensType = Types.Interface(False, {
                    "query": Types.FuncPointer([i.lensType], i.nodes[0].type),
                    "set": Types.FuncPointer([i.lensType, i.nodes[0].type], i.lensType),
                })

                i.type = lensType
            elif type(i) is Tree.Block:
                if len(i.nodes) > 0:
                    i.type = i.nodes[-1].type

            if type(i) in [Tree.Block, Tree.While]:
                Scope.decrScope(parser)

            count += 1
    loop(tree, -1)

def validate(parser, tree):
    for i in tree:
        if type(i) is Tree.Lambda:
            Scope.incrScope(parser)
        if not i.isEnd():
            validate(parser, i)
        i.validate(parser)

    if type(tree) is Tree.Root:
        tree.validate(parser)

def resolveGen(shouldBeTyp, normalTyp, generics, parser):
    if type(shouldBeTyp) is Types.T:
        if shouldBeTyp.normalName in generics:
            return generics[shouldBeTyp.normalName]
        else:
            generics[shouldBeTyp.normalName] = normalTyp
            return shouldBeTyp.type
    elif type(shouldBeTyp) is Types.Array:
        if type(normalTyp) != Types.Array:
            return shouldBeTyp

        t = Types.Array(False, resolveGen(shouldBeTyp.elemT, normalTyp.elemT, generics, parser))
        return t
    elif type(shouldBeTyp) is Types.FuncPointer:
        args = []
        if not type(normalTyp) is Types.FuncPointer:
            return shouldBeTyp

        if len(shouldBeTyp.args) != len(normalTyp.args):
            return shouldBeTyp

        for (should, nor) in zip(shouldBeTyp.args, normalTyp.args):
            args.append(resolveGen(should, nor, generics, parser))

        resolveGen(shouldBeTyp.returnType, normalTyp.returnType, generics, parser)

        return Types.replaceT(shouldBeTyp, generics)
    elif type(shouldBeTyp) in [Types.Struct, Types.Enum]:
        if not type(normalTyp) is Types.Struct:
            return shouldBeTyp
        self = shouldBeTyp
        other = normalTyp
        if self.package+"_"+self.normalName != other.package+"_"+other.normalName:
            return shouldBeTyp

        types = {}
        shouldGeneric = shouldBeTyp.remainingGen
        normalGeneric = normalTyp.gen

        for i in shouldGeneric:
            generics[i] = resolveGen(shouldGeneric[i], normalGeneric[i], generics, parser)

        if type(shouldBeTyp) is Types.Enum:
            return Types.Enum(self.package, self.normalName, self.const, generics)
        else:
            return Types.Struct(False, self.normalName, self.types, self.package, generics)

    elif type(shouldBeTyp) is Types.Assign:
        const = shouldBeTyp.const
        return Types.Assign(Types.replaceT(const, generics))
    elif type(shouldBeTyp) is Types.Interface:
        types = {}
        for i in shouldBeTyp.types:
            try:
                types[i] = resolveGen(shouldBeTyp.types[i], normalTyp.types[i], generics, parser)
            except KeyError:
                try:
                    meth = normalTyp.hasMethod(parser, i)
                    if type(meth) is Types.FuncPointer:
                        types[i] = resolveGen(shouldBeTyp.types[i], Types.FuncPointer(meth.args[1:], meth.returnType, generic= meth.generic, do= meth.do), generics, parser)
                    elif meth:
                        types[i] = meth
                    else:
                        types[i] = shouldBeTyp.types[i]
                except AttributeError:
                    types[i] = shouldBeTyp.types[i]
        return Types.Interface(False, types, generics)

    else:
        return shouldBeTyp