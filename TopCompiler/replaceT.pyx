from .Types import *

def replaceT(typ, gen, acc=False, unknown=False):  # with bool replaces all
    if typ is None: return

    if not acc:
        acc = {}

    isGen = isGeneric(typ, unknown)

    if typ in acc:
        return acc[typ]

    if not isGen:
        return typ

    if type(typ) is T:
        if typ.normalName in gen:
            r = gen[typ.normalName]
            acc[typ] = r
            return replaceT(r, gen, acc, unknown)
        else:
            # if type(typ.type) is Assign:
            return T(typ.realName, replaceT(typ.type, gen, acc, unknown), typ.owner)
            # return typ
    elif type(typ) is Struct:
        rem = {}  # gen
        types = typ._types
        for i in typ.remainingGen:
            if i in gen:
                rem[i] = gen[i]  # T(i[i.find(".")+1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)

        #types = {i: replaceT(types[i], gen, acc, unknown) for i in types}

        joined = {}
        for i in rem:
            joined[i] = rem[i]

        for i in gen:
            joined[i] = gen[i]
        return Struct(False, typ.normalName, typ.types, typ.package, joined)
    elif type(typ) is Alias:
        rem = {}
        for i in typ.generic:
            if i in gen:
                rem[i] = gen[i]  # T(i[i.find(".") + 1:], gen[i], i[:i.find(".")])
            else:
                rem[i] = replaceT(typ.remainingGen[i], gen, acc, unknown)
        return Alias(typ.package, typ.normalName, replaceT(typ.typ, gen, acc, unknown), rem)
    elif type(typ) is Assign:
        return Assign(replaceT(typ.const, gen, acc, unknown))
    elif type(typ) is Interface:
        types = typ.types

        c = Interface(False, {})

        if acc == {}:
            acc = {typ: c}
        else:
            acc[typ] = c

        types = {i: replaceT(types[i], gen, acc, unknown) for i in types}
        methods = {i: replaceT(typ.methods[i], gen, acc, unknown) for i in typ.methods}

        c.fromObj(Interface(False, types, gen, typ.fullName, methods=methods))
        return c
    elif type(typ) is Pointer:
        newP = Pointer(replaceT(typ.pType, gen, acc, unknown), typ.mutable)
        return newP
    elif type(typ) is Enum:
        const = coll.OrderedDict()
        g = {}

        c = Enum(typ.package, typ.normalName, const, g)

        # if acc == {}:
        #    acc = {typ: c}
        # else:
        acc[typ] = c

        for name in typ.const:
            const[name] = [replaceT(i, gen, acc, unknown) for i in typ.const[name]]

        for name in typ.remainingGen:
            g[name] = replaceT(typ.remainingGen[name], gen, acc, unknown)

        c.fromObj(Enum(typ.package, typ.normalName, const, g, findRemaining=False))
        return c

    elif type(typ) is Tuple:
        arr = []
        for i in typ.list:
            arr.append(replaceT(i, gen, acc, unknown))

        return Types.Tuple(arr)

    elif type(typ) is Array and isGen:
        return Array(replaceT(typ.elemT, gen, acc, unknown), both=typ.both, static=typ.static,
                     numElements=typ.numElements)
    elif type(typ) is FuncPointer:
        generics = typ.generic

        arr = []
        for i in typ.args:
            arr.append(replaceT(i, gen, acc, unknown))

        newTyp = replaceT(typ.returnType, gen, acc, unknown)
        r = FuncPointer(arr, newTyp, gen, do=typ.do)
        r.remainingGen = {}
        #for field in r.remainingGen:
        #    r.remainingGen[field] = replaceT(r.remainingGen[field], gen, acc, unknown)

        return r
    else:
        return typ

def isGeneric(t, unknown=False):
    #if unknown: return True
    if type(t) is FuncPointer: #return True
        if t.generic != {}: return True
        for i in t.args:
            if isGeneric(i): return True
        return isGeneric(t.returnType)
    elif type(t) is Array:
        return isGeneric(t.elemT)
    elif type(t) is T:
        return True
    elif type(t) is Pointer:
        return isGeneric(t.pType)
    elif type(t) in [Interface, Struct, Alias, Enum]:
        return len(t.remainingGen) > 0
    elif type(t) is Tuple: return True
        #for i in t.list:
        #    if isGeneric(i):
        #        return True

    return False