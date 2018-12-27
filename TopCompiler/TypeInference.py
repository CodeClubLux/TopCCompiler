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
from collections import OrderedDict as ODict
from TopCompiler import ContextParser

from collections import OrderedDict

checkTyp = []

def infer(parser, tree):
    varTypes = {}
    sc = parser.sc

    parser.func = []

    def loop(n, o_iter):
        for (count, i) in enumerate(n):
            parser.on(i)

            if type(n) is type(tree):
                o_iter += 1

            if not sc and type(i) in [Tree.FuncStart, Tree.FuncBraceOpen, Tree.FuncBody]:
                continue

            if type(i.owner) is Tree.For and (count == 1 if len(i.owner.nodes) > 1 else count == 0):
                _for = i.owner

                condition = _for.nodes[0]
                it_should_be = None
                
                if type(condition) is Tree.CreateAssign:
                    _for.implicit = False
                    _for.implicit_index = False
                    if condition.nodes[0].varType.isType(Types.Array):
                        it_should_be = Types.I32(unsigned=True)
                        _for.implicit_index = True

                    _for.condition_type = condition.nodes[0].varType
                else:
                    _for.implicit = True
                    _for.implicit_index = False

                    if condition.type.isType(Types.Array):
                        it_should_be = condition.type.toRealType().elemT
                    elif condition.type.name == "Range":
                        it_should_be = Types.I32(unsigned=True)
                    else:
                        i.error("for loop only operators either on Range or array")

                    _for.condition_type = condition.type
                if it_should_be:
                    try:
                        Scope.addVar(_for, parser, "i", Scope.Type(True, it_should_be, _for.global_target))
                    except EOFError as e:
                        pass

            if type(i) is Tree.FuncStart:
                if not type(n) is Tree.Root:
                    Scope.addVar(i, parser, i.name, Scope.Type(True, i.ftype))
                Scope.incrScope(parser)

            elif type(i) in [Tree.Block, Tree.While, Tree.For, Tree.AddToContext]:
                Scope.incrScope(parser)

            if type(i) is Tree.Lambda:
                count = Types.state.count
                Scope.incrScope(parser)

            if not (i.isEnd() or type(i) in [Tree.MatchCase, Tree.Lens] or (type(i) is Tree.Block and type(i.owner) is Tree.Match)):
                if type(i) is Tree.FuncBody:
                    if i.method:
                        parser.func.append(parser.package+"."+i.name[:i.name.find("_")])
                    else:
                        parser.func.append(parser.package+"."+i.name)

                loop(i, o_iter)

                if type(i) is Tree.FuncBody and len(parser.func) > 0:
                    parser.func.pop()

            if type(i) is Tree.Match:
                typ = i.nodes[0].type
                first = False
                for c in range(1,len(i.nodes),2):
                    body = i.nodes[c+1]

                    if not i.guard:
                        Scope.incrScope(parser)
                    Enum.checkCase(parser, i.nodes[c].nodes[0], typ, True)

                    loop(body, o_iter)
                    body.type = body.nodes[-1].type if len(body.nodes) > 0 else Types.Null()

                    if not i.guard:
                        Scope.decrScope(parser)

                    if first:
                        try:
                            thisTyp = body.type
                            first.duckType(parser, thisTyp, body, i, 0)
                        except EOFError as e:
                            try:
                                thisTyp.duckType(parser, first, body, i, 0)
                                first = thisTyp
                            except EOFError:
                                Error.beforeError(e, "Type mismatch, this arm has a different type : ")

                        #if body.type != first:
                        #    (body.nodes[-1] if len(body.nodes) > 0 else body).error(
                        #        "type mismatch in arms of match, " + str(body.type) + " and " + str(first))
                    else:
                        if len(i.nodes[2].nodes) > 0:
                            first = i.nodes[2].nodes[-1].type
                        else:
                            first = Types.Null()
                        i.nodes[2].type = first

                for c in range(1, len(i.nodes), 2):
                    if len(i.nodes[c+1].nodes) > 0:
                        Tree.insertCast(i.nodes[c+1].nodes[-1], i.nodes[c+1].type, first, -1)

                Enum.missingPattern(typ, i)
                i.type = first if first else Types.Null()

            elif type(i) is Tree.PushContext:
                ContextParser.typecheckPushContext(parser, i)

            elif type(i) is Tree.Using:
                typ = i.varType
                i.extracted_fields = {}
                i.extracted_methods = {}

                for field in typ.types:
                    try:
                        Scope.addVar(i, parser, field, Scope.Type(i.imutable, typ.types[field]), False)
                        i.extracted_fields[field] = typ.types[field]
                    except:
                        pass
                        #i.error("Could not extract field " + field)

            elif type(i) is Tree.CreateAssign:
                if type(i.nodes[0].name) is Tree.PlaceHolder:
                    p = i.nodes[0].name.nodes[0]
                    node = i.nodes[1].nodes[0]

                    def recur(typ, pattern):
                        if type(pattern) is Tree.Tuple:
                            if len(pattern) > len(typ.list):
                                diff = len(pattern) - len(typ.list)
                                node.error(diff+" too few values to unpack")
                            elif len(pattern) < len(typ.list):
                                diff = len(typ.list) - len(pattern)
                                node.error(diff+" too many values to unpack")

                            for (index, p) in enumerate(pattern):
                                recur(typ.list[index],p)
                        elif type(pattern) is Tree.InitStruct:
                            for p in pattern:
                                if type(p) is Tree.Assign:
                                    name = p.nodes[0].name
                                    p = p.nodes[1]
                                else:
                                    name = p.name

                                if not name in typ.types:
                                    node.error("Object has no field "+name)
                                recur(typ.types[name],p)
                        else:
                            Scope.addVar(node, parser, pattern.name, Scope.Type(True, typ, i.global_target))
                            pattern.isGlobal = Scope.isGlobal(parser, parser.package, pattern.name)

                    recur(node.type, p)
                elif i.nodes[0].varType is None and i.nodes[0].name != "_":
                    if i.extern:
                        i.error("expecting type declaration, for external variable declaration")
                    i.nodes[0].varType = i.nodes[1].nodes[0].type

                    typ = i.nodes[1].nodes[0].type
                    
                    if type(i.owner) is Tree.For and count == 0:
                        if typ.isType(Types.Array):
                            typ = typ.elemT
                        elif typ.name == "Range":
                            typ = Types.I32(unsigned= True)
                            i.nodes[0].varType = typ
                        else:
                            i.error("for loop only operators either on Range or array")

                    Scope.addVar(i, parser, i.nodes[0].name, Scope.Type(i.nodes[0].imutable, typ, i.global_target))
                    i.nodes[0].isGlobal = Scope.isGlobal(parser, i.nodes[0].package, i.nodes[0].name)

            elif type(i) is Tree.FuncBody:
                Scope.decrScope(parser)
            elif type(i) is Tree.Create:
                if not i.varType is None:
                    if type(i.owner) is Tree.For and count == 0:
                        if i.varType.isType(Types.Array):
                            i.varType = i.varType.elemT
                        elif i.varType.name == "Range":
                            i.varType = Types.I32(unsigned= True)
                        else:
                            i.error("for loop only operators either on Range or array")

                    Scope.addVar(i, parser, i.name, Scope.Type(i.imutable, i.varType, i.owner.global_target))
                    i.isGlobal = Scope.isGlobal(parser, i.package, i.name)
                    if i.isGlobal and not i.imutable:
                        i.error("Global variables are bad")

            elif type(i) is Tree.ReadVar:
                if not (type(i.owner) is Tree.Assign and type(i.owner.owner) is Tree.InitStruct and i.owner.nodes[0] == i):
                    if i.name in parser.imports:
                        if not type(i.owner) is Tree.Field:
                            i.error("expecting ., cannot directly mention package name")
                    elif type(i.type) is Tree.Type:
                        i.error("unexpected type "+str(i.type))

                    i.type = Scope.typeOfVar(i, parser, i.package, i.name)
                    self = i
                    self.imutable = not Scope.isMutable(parser, self.package, self.name)
                    self.isGlobal = Scope.isGlobal(parser, self.package, self.name)
                    self.package = Scope.packageOfVar(parser, parser.package, self.name)

            elif type(i) is Tree.Field:
                #if i.unary:
                #    field = i.field

                #    T = Types.T("T", Types.All, "get"+i.field[0].upper()+i.field[1:])

                #    I = Types.Interface(False, {field: T})

                 #   i.type = Types.FuncPointer([I], T, generic=ODict([("T", T)]))
                  #  count += 1
                   # continue

                """ 
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
                """

                typ = i.nodes[0].type
                t = i.nodes[0]

                if type(typ) is Types.Package:
                    i.indexPackage = True
                    i.type = Scope.typeOfVar(i, parser, i.nodes[0].name, i.field)
                    i.nodes[0].package = i.nodes[0].name
                    i.nodes[0].name = ""
                else:
                    if type(typ) is Types.FuncPointer:
                        i.error("type "+str(typ) + " has no field " + i.field)

                    struct = typ

                    self = i
                    insertTakeRef = False

                    try:
                        i.type = struct.types[self.field]
                    except KeyError:
                        try:
                            if type(struct) is Types.Alias:
                                insertTakeRef = Tree.canTakeRef(self.nodes[0], struct)

                                method = struct.typ.hasMethod(parser, self.field, isP= insertTakeRef) #has method should check if t can be upcasted
                                if method:
                                    typ = struct.typ
                                else:
                                    method = struct.hasMethod(parser, self.field)
                            else:
                                insertTakeRef = Tree.canTakeRef(self.nodes[0], struct)

                                method = struct.hasMethod(parser, self.field, isP= insertTakeRef)
                        except EOFError as e:
                            Error.beforeError(e, str(struct)+"."+self.field+" only operates: ")

                        if not method:
                            self.error("type "+str(typ) + " has no field " + self.field)

                        newMethod = copy.copy(method)
                        newMethod.args = newMethod.args[1:]
                        self.type = newMethod
                        self.replaced = i.nodes[0].type.remainingGen

                        if not type(self.owner) is Tree.FuncCall:
                            self.error("Binding method function not supported")

                        if insertTakeRef:
                            Tree.insertCast(self.nodes[0], self.nodes[0].type, method.args[0], 0, onlyToP=True)
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

                        f = Tree.FuncCall(parser)
                        f.addNode(self.nodes[1])
                        f.addNode(self.nodes[0])
                        f.owner = self.owner
                        f.type = b.returnType

                        self.owner.nodes[count] = f
                elif i.kind == "as":
                    #does this create a cast node
                    i.type.duckType(parser, i.nodes[0].type, i, i.nodes[0], 0)

                elif i.kind == "..":
                    for c in i.nodes:
                        if not (type(c.type.toRealType()) is Types.I32 and c.type.toRealType().unsigned):
                            c.error("Expecting uint")

                    i.type = Parser.Range
                elif i.kind == "<-":
                    if i.unary:
                        try:
                            meth = i.nodes[0].type.types["unary_read"]
                        except KeyError:
                            meth = i.nodes[0].type.hasMethod(parser, "unary_read")

                        if meth:
                            i.type = meth.returnType
                            i.opT = i.nodes[0].type
                        else:
                            i.error("type "+str(i.nodes[0].type)+", missing method unary_read")
                    else:
                        try:
                            meth = i.nodes[0].type.types["op_set"]
                        except KeyError:
                            meth = i.nodes[0].type.hasMethod(parser, "op_set")

                        if meth:
                            meth.args[0].duckType(parser, i.nodes[1].type, i.nodes[1], i, 1)
                            Tree.insertCast(i.nodes[1], fromT= i.nodes[1].type, toT=meth.args[0])

                            i.opT = i.nodes[0].type
                        else:
                            i.error("type " + str(i.nodes[0].type) + ", missing method op_set")

                        #else:
                        #    i.nodes[0].error("Type " + str(i.nodes[0].type) + ", missing method op_set")

                elif i.kind == "concat":
                    stringable = Parser.Stringable #Types.Interface(False, {}, meth {"toString": Types.FuncPointer([], Types.String(0))})
                    for (it, c) in enumerate(i):
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
                                    i.nodes[0].error("logical operator "+i.kind+" only works on boolean, not " + str(startType))

                        for c in i.nodes[1:]:
                            if type(c) is Tree.Under:
                                partial = True
                            elif startType:
                                try:
                                    c.type.duckType(parser, startType, i, c, 0)
                                    startType = c.type
                                except EOFError:
                                    startType.duckType(parser, c.type, c, i, 0)
                            else:
                                startType = c.type

                        for (_iter, c) in enumerate(i.nodes):
                            Tree.insertCast(c, c.type, startType, _iter)

                        i.partial = partial
                        typ = startType
                        if i.kind in ["==", "!=", "not", "and", "or", "<", ">", "<=", ">="]:
                            typ = Types.Bool()
                        elif i.kind == "&":
                            typ = Types.Pointer(startType, True)

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

                        realT = typ #.toRealType()
                        if i.kind == "-" and type(realT) is Types.I32 and realT.unsigned:
                            i.type = Types.I32(size= realT.size, unsigned=True)
                        i.type = typ
                        i.opT = startType

                Tree.checkOperator(i, parser)

            elif type(i) is Tree.FuncCall:
                c = i

                partial = False

                if not i.nodes[0].type.isType(Types.FuncPointer):
                    i.nodes[0].error("type "+str(i.nodes[0].type)+" is not callable")

                i.nodes[0].type = i.nodes[0].type.toRealType()
                do = i.nodes[0].type.do
                returnType = i.nodes[0].type.returnType
                fType = i.nodes[0].type
                args = i.nodes[0].type.args
                newArgs = []

                realNumArgs = len(i.nodes)-1
                if len(args) != realNumArgs:
                    i.error("Expecting "+str(len(args))+ " amount of arguments but got "+str(realNumArgs))

                generics = {}
                for iter in range(len(i.nodes[1:])):
                    if type(i.nodes[iter+1]) is Tree.Under:
                        partial = True
                        newArgs.append(args[iter])
                    else:
                        xnormalTyp = args[iter]
                        myNode = i.nodes[iter+1]
                        myTyp = myNode.type
                        normalNode = i

                        isGen = Types.isGeneric(myTyp)

                        if Types.isGeneric(xnormalTyp) or isGen:
                            normalTyp = resolveGen(xnormalTyp, myNode.type, generics, parser, myNode, i)

                            if isGen:
                                myTyp = Types.replaceT(myTyp, generics)

                        else:
                            normalTyp = xnormalTyp

                        normalTyp.duckType(parser, myTyp, myNode, i, iter + 1)
                        Tree.insertCast(i.nodes[iter+1], myNode.type, normalTyp, iter+1)

                i = c
                i.replaced = {}

                #fromReadVar = []
                #if type(i.nodes[0]) is Tree.Field:
                #    fromReadVar =  i.nodes[0].replaced

                for key in fType.generic:
                    #if not key in generics and not key in fromReadVar:
                    #    i.error("Could not infer parameter " + key)
                    i.replaced[key] = fType.generic[key]

                for key in generics:
                    if key in fType.generic:
                        i.replaced[key] = generics[key]

                i.type = Types.replaceT(i.nodes[0].type.returnType, generics)
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
                        if not (i.init and type(i.nodes[0]) is Tree.Under):
                            normalNode = i.owner.nodes[0] if i.init else i.nodes[1]
                            normalTyp = i.owner.nodes[0].varType if i.init else i.nodes[0].type
                            myNode = (i.nodes[0] if i.init else i.nodes[1])

                            normalTyp.duckType(parser, myNode.type, normalNode, myNode, (0 if i.init else 1))
                            Tree.insertCast(myNode, myNode.type, normalTyp, (0 if i.init else 1))

            elif type(i) is Tree.Tuple:
                if len(i.nodes) == 0:
                    i.error("unexpected )")
                elif len(i.nodes) > 1:
                    i.type = Types.Tuple([c.type for c in i])
                else:
                    i.type = i.nodes[0].type

            elif type(i) is Tree.AddToContext:
                ContextParser.typecheckAddToContext(parser, i)

            elif type(i) is Tree.Array:
                arr = i
                lengthOfArray = 0

                if len(i.nodes) > 0:
                    static = False
                    if arr.init:
                        if arr.nodes[0].type != Types.I32(unsigned=True) and arr.nodes[0].type != Types.I32(unsigned=True, size=32):
                            arr.nodes[0].error("expecting unsigned integer for range start, not "+str(arr.nodes[0].type))
                        if len(arr.nodes) > 1:
                            typ = arr.nodes[1].type
                            static = type(arr.nodes[0]) is Tree.Int
                            if static:
                                lengthOfArray = int(arr.nodes[0].number)
                        else:
                            arr.nodes[0].error("expecting value after :")

                    else:
                        static = True
                        lengthOfArray = len(arr.nodes)
                        typ = arr.nodes[0].type
                        if typ == Types.Null():
                            arr.error("array elements must be non none")

                        count = 0
                        for c in arr.nodes[1:]:
                            err = False
                            if typ != c.type:
                                ctype = c.type
                                try:
                                    typ.duckType(parser, ctype, i, c, count)
                                except EOFError as e:
                                    try:
                                        ctype.duckType(parser, typ, c, i, count)
                                        typ = ctype
                                    except EOFError as e:
                                        err = e

                                if err:
                                    Error.beforeError(err, "Element type in array: ")

                            count += 1

                        for (index, c) in enumerate(arr.nodes[1:]):
                            Tree.insertCast(c, c.type, typ, index+1)

                    arr.type = Types.Array(typ, static= static, numElements=lengthOfArray, both=False)
                else:
                    arr.type = Types.Array(Types.Null(), empty=True, static=False,both=False)
            elif type(i) is Tree.InitPack:
                parser.imports.append(i.package)
            elif type(i) is Tree.InitStruct:
                unary = i.unary
                if not unary:
                    typ = i.constructor.type
                    i.typ = typ

                    assign = True
                    if typ.isType(Struct.Struct):
                        s = typ
                        assign = False
                        i.paramNames = Struct.offsetsToList(s.offsets)
                    elif typ.isType(Types.Interface) or typ.isType(Types.Struct):
                        assign = True
                        s = typ
                    else:
                        i.constructor.error("type "+str(typ)+" can not be used as a constructor")

                    i.s = s
                    name = s.name

                    types = normalTyp = s._types if type(s) is Struct.Struct else s.types

                    if len(types) < len(i.nodes) - 1:
                        c = str(len(i.nodes) - 1 - len(types))
                        i.error(("1 argument" if c == "1" else c + " arguments") + " too many")
                    elif not assign and len(types) > len(i.nodes) - 1:
                        c = str(len(types) + 1 - len(i.nodes))
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

                    realIter = iter

                    if not randomOrder:
                        nameInOrder = i.paramNames[iter-1]
                        order[nameInOrder] = i.nodes[iter]
                        myNode = i.nodes[iter]
                        normalTyp = s.fieldType[iter-1]
                    else:
                        if not type(i.nodes[iter]) is Tree.Assign:
                            i.nodes[iter].error("positional argument follows keyword argument")
                        if i.nodes[iter].nodes[0].name in order:
                            i.nodes[iter].nodes[0].error("duplicate parameter")
                        nameInOrder = i.nodes[iter].nodes[0].name
                        order[nameInOrder] = i.nodes[iter]
                        myNode = i.nodes[iter].nodes[1]
                        xname = i.nodes[iter].nodes[0].name

                        if not unary:
                            try:
                                normalTyp = types[xname]
                            except KeyError:
                                i.nodes[iter].nodes[0].error("type "+str(s)+" does not have the field "+ xname)

                        iter = 1

                    normalNode = i

                    if not unary:
                        xnormalTyp = normalTyp

                        isGen = Types.isGeneric(normalTyp)
                        myIsGen = Types.isGeneric(myNode.type)

                        myTyp = myNode.type

                        if isGen:
                            normalTyp = resolveGen(normalTyp, myNode.type, gen, parser, myNode, i)

                            if myIsGen:
                                myTyp = Types.replaceT(myNode.type, gen)

                        normalTyp.duckType(parser, myTyp, myNode, i, iter)

                        Tree.insertCast(myNode, myNode.type, normalTyp, iter)
                        order[nameInOrder] = i.nodes[realIter]

                        #resolveGen(xnormalTyp, myNode.type, gen, parser, myNode, i)
                if not assign:
                    del i.nodes[0]
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
                    package = parser.structs[i.package][name].package
                    newGen = OrderedDict()

                    for _name in s.generic:
                        if not _name in gen:
                            newGen[_name] = s.generic[_name]
                        else:
                            newGen[_name] = gen[_name]

                    i.type = Types.Struct(i.mutable, name, s._types, package, newGen)
                i.replaced = i.type.remainingGen
            elif type(i) is Tree.ArrRead:
                if len(i.nodes) == 2:
                    typ = i.nodes[0].type
                    insertTakeRef = False

                    try:
                        insertTakeRef = Tree.canTakeRef(i.nodes[0], i.nodes[0].type)
                        func = typ.hasMethod(parser, "op_get", isP=insertTakeRef)
                    except EOFError as e:
                        Error.beforeError(e, str(typ) + " only operates : ")

                    firstArg = None
                    if not func:
                        i.nodes[0].error("Type "+str(i.nodes[0].type)+" is not indexable, missing method op_get")
                    else:
                        firstArg = func.args[0]
                        func = Types.FuncPointer(func.args[1:], func.returnType, generic=func.generic, do=func.do)

                    if insertTakeRef:
                        Tree.insertCast(i.nodes[0], i.nodes[0].type, firstArg, 0)

                    arrRead = i
                    if len(arrRead.nodes) != 2:
                        i.nodes[1].error("expecting single index")


                    #if len(func.args) != 1: cant add a method that does not follow the proper type for operator overloading
                    #    i.nodes[0].error(str(typ) + " is not indexable, method get should take 1 parameter, not "+str(len(func.args)))

                    try:
                        func.args[0].duckType(parser, i.nodes[1].type, i.nodes[1], i, 0)
                        Tree.insertCast(i.nodes[1], i.nodes[0].type, func.args[0], 1)
                    except EOFError as e:
                        Error.beforeError(e, "Index : ")

                    if func.returnType.isType(Types.Pointer):
                        arrRead.type = func.returnType.pType
                    else:
                        arrRead.type = func.returnType
                else:
                    i.error("expecting single index")
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
            elif type(i) is Tree.Block:
                if len(i.nodes) > 0:
                    i.type = i.nodes[-1].type
            else:
                for c in checkTyp:
                    if checkTyp[c](i):
                        break

            if type(i) in [Tree.Block, Tree.While, Tree.For, Tree.AddToContext]:
                Scope.decrScope(parser)

    loop(tree, -1)

validate = Tree.validate

def resolveGen(shouldBeTyp, normalTyp, generics, parser, myNode, other):
    #shouldBeTyp = shouldBeTyp.toRealType()
    #normalTyp = normalTyp.toRealType()

    """
    if type(normalTyp) is Types.T and not (normalTyp.owner in parser.func) and normalTyp.name != shouldBeTyp.name:
        if normalTyp.normalName in generics:
            normalTyp = generics[normalTyp.normalName]
        else:
            newTyp = Types.replaceT(shouldBeTyp, generics)

            tmp = normalTyp

            generics[normalTyp.normalName] = newTyp
            normalTyp = newTyp
            normalTyp = resolveGen(tmp.type, newTyp, generics, parser, myNode, other)

            normalTyp.duckType(parser, newTyp, myNode, other, 0)
            normalTyp = newTyp
    """
    if type(shouldBeTyp) is Types.T and not (shouldBeTyp.owner in parser.func):
        if shouldBeTyp.normalName in generics:
            tmp = generics[shouldBeTyp.normalName]
            return tmp
        else:
            generics[shouldBeTyp.normalName] = normalTyp
            if normalTyp.name != shouldBeTyp.name:
                tmp = shouldBeTyp.type
                tmp = resolveGen(tmp, normalTyp, generics, parser, myNode, other)

                tmp.duckType(parser, normalTyp, myNode, other, 0)
            else:
                tmp = shouldBeTyp

        #if Types.isGeneric(tmp):
        #    resolveGen(tmp, normalTyp, generics, parser, myNode, other)
        #else:

        return normalTyp

    elif type(shouldBeTyp) is Types.Array:
        if type(normalTyp) != Types.Array:
            normalTyp = normalTyp.toRealType()
            if shouldBeTyp.both and normalTyp.isType(Types.Pointer) and normalTyp.pType.isType(Types.Array):
                normalTyp = normalTyp.pType.toRealType()
            else:
                return shouldBeTyp

        try:
            t = Types.Array(resolveGen(shouldBeTyp.elemT, normalTyp.elemT, generics, parser, myNode, other), both= shouldBeTyp.both, static= shouldBeTyp.static, numElements= shouldBeTyp.numElements)
        except EOFError as e:
            Error.beforeError(e, "Element type in array: ")

        return t
    elif type(shouldBeTyp) is Types.FuncPointer:
        args = []
        if not type(normalTyp) is Types.FuncPointer:
            return shouldBeTyp

        if len(shouldBeTyp.args) != len(normalTyp.args):
            return shouldBeTyp

        for (count, (should, nor)) in enumerate(zip(shouldBeTyp.args, normalTyp.args)):
            try:
                args.append(resolveGen(should, nor, generics, parser, myNode, other))
            except EOFError as e:
                Error.beforeError(e, "Function type argument "+str(count)+": ")

        try:
            returnTyp = resolveGen(shouldBeTyp.returnType, normalTyp.returnType, generics, parser, myNode, other)
        except EOFError as e:
            Error.beforeError(e, "Function type return type: ")

        return Types.FuncPointer(args, returnTyp, do=shouldBeTyp.do)

        #return Types.replaceT(shouldBeTyp, generics)
        #return Types.FuncPointer(args, returnTyp, Types.remainingT(returnTyp), do = shouldBeTyp.do)
    elif type(shouldBeTyp) is Types.Tuple:
        if not type(normalTyp) is Types.Tuple:
            return shouldBeTyp

        arr = []
        for (key, (should, nor)) in enumerate(zip(shouldBeTyp.list, normalTyp.list)):
            try:
                arr.append(resolveGen(should, nor, generics, parser, myNode, other))
            except EOFError as e:
                Error.beforeError(e, "Tuple element #" + str(key) + ": ")

        return Types.Tuple(arr)
    elif type(shouldBeTyp) is Types.Pointer:
        if not type(normalTyp) is Types.Pointer:
            return shouldBeTyp

        pType = resolveGen(shouldBeTyp.pType, normalTyp.pType, generics, parser, myNode, other)
        return Types.Pointer(pType)
    elif type(shouldBeTyp) in [Types.Struct, Types.Enum, Types.Alias]:
        gen = generics
        if not type(normalTyp) is type(shouldBeTyp):
            return shouldBeTyp
        self = shouldBeTyp
        other = normalTyp
        if self.package+"_"+self.normalName != other.package+"_"+other.normalName:
            return shouldBeTyp

        types = {}
        shouldGeneric = shouldBeTyp.remainingGen
        if type(shouldBeTyp) in [Types.Enum, Types.Alias]:
            normalGeneric = normalTyp.generic
        else:
            normalGeneric = normalTyp.gen

        for i in shouldGeneric:
            try:
                generics[i] = resolveGen(shouldGeneric[i], normalGeneric[i], generics, parser, myNode, other)
            except EOFError as e:
                Error.beforeError(e, "Field '" + i + "' in " + str(shouldBeTyp) + ": ")

        if type(shouldBeTyp) is Types.Enum:
            return Types.Enum(self.package, self.normalName, self.const, generics)
        elif type(shouldBeTyp) is Types.Alias:

            return Types.Alias(self.package, self.normalName, Types.replaceT(self.typ, generics), generics)
        else:
            return Types.Struct(False, self.normalName, self.types, self.package, generics)

    elif type(shouldBeTyp) is Types.Assign:
        const = shouldBeTyp.const
        return Types.Assign(Types.replaceT(const, generics))
    elif type(shouldBeTyp) is Types.Interface:
        types = {}
        methods = {}
        for i in shouldBeTyp.types:
            try:
                types[i] = resolveGen(shouldBeTyp.types[i], normalTyp.types[i], generics, parser, myNode, other)
            except EOFError as e:
                Error.beforeError(e, "Field '" + i + "' in " + str(shouldBeTyp) + ": ")
            except KeyError:
                types[i] = shouldBeTyp.types[i]

        for i in shouldBeTyp.methods:
            try:
                try:
                    meth = normalTyp.hasMethod(parser, i, isP=True)
                except EOFError as e:
                    Error.beforeError(e, "type " + str(normalTyp) + "." + i + ", to be upcasted to " + str(
                        shouldBeTyp) + ", only operates: ")

                if meth:
                    methods[i] = resolveGen(shouldBeTyp.methods[i], Types.FuncPointer(meth.args[1:], meth.returnType, generic= meth.generic, do= meth.do), generics, parser, myNode, other)
                else:
                    methods[i] = shouldBeTyp.methods[i]
            except EOFError as e:
                Error.beforeError(e, "Method '" + i + "' in " + str(shouldBeTyp) + ": ")

        gen = ODict()

        for key in shouldBeTyp.generic:
            gen[key] = Types.replaceT(shouldBeTyp.generic[key], generics)

        #gen = {i: generics[i] for i in generics if ".".join(i.split(".")[:-1]) == shouldBeTyp.normalName}
        r = Types.Interface(False, types, gen, shouldBeTyp.fullName, methods= methods)

        return r
    else:
        return shouldBeTyp