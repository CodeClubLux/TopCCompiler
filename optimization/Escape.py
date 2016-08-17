__author__ = 'antonellacalvia'

import AST as Tree
from TopCompiler import Types


class Connection:
    def __init__(self, node, escape=0):
        self.node = node
        self.connections = []
        self.fields = {}
        self.color = escape

        self.node.escapes = escape

    def connect(self, conn):
        self.connections.append(conn)

    def connectField(self, field, conn):
        if field in self.fields:
            self.fields[field].connect(conn)
        else:
            self.fields[field] = Connection(None, False)
            self.fields[field].connect(conn)

    def __iter__(self):
        return self._iter()

    def _iter(self):
        for i in self.connections:
            yield i

        for i in self.fields:
            for c in self.fields[i]:
                yield c

    def __str__(self):
        colors = ["white ", "grey", "black"]
        return colors[self.color]+" "+str(self.node)

    def setColor(self, color):
        self.node.escapes = color
        self.color = color

    def isEnd(self):
        return len(self.connections) == 0 and len(self.fields) == 0


def visual(conn, indent=""):
    if conn.isEnd():
        print(indent + str(conn))
    else:
        print(indent + str(conn))
        indent += "\t"
        for iter in conn:
            visual(iter, indent)
        indent = indent[:-1]


def escapePass(tree):
    connectionGraph = Connection(tree)

    vars = {}
    funcReturns = {}

    def isPointer(node):
        return type(node.type if not type(node) is Tree.Create else node.varType) in [Types.Pointer, Types.MutPointer]

    def resolveEnd(conn, node, funcName):
        if type(node) is Tree.Operator and node.kind == "&":
            b = Connection(node, False)
            for i in node:
                resolveEnd(b, i, funcName)
            conn.connect(b)
        elif type(node) is Tree.If:
            for i in node.nodes:
                if type(i) is Tree.Block:
                    resolveEnd(conn, i.nodes[-1])
        elif type(node) is Tree.ReadVar:
            if node.isGlobal:
                conn.connect(vars[node.package+".."+node.name])
            else:
                conn.connect(vars[node.package + "." + funcName + "."+ node.name])
        elif type(node) is Tree.FuncCall:
            if node.inline:
                for i in node:
                    resolveEnd(conn, i, node.name)
                return

            for i in range(len(node.nodes)):
                resolveEnd(funcs[node.name][i], node.nodes[i], funcName)

            c = Connection(node)
            c.connections = funcReturns[node.package+"."+node.name].connections
            conn.connect(c)
        elif type(node) is Tree.Field:
            resolveEnd(conn, node.nodes[0])

            if isPointer(node):
                vars[node.nodes[0].package + "." + funcName + "." + node.nodes[0].name].connectField(node.field, Connection(node))
                pass
        elif type(node) is Tree.FieldWrite:
            resolveEnd(conn, node.nodes[1], funcName)
        elif type(node) in [Tree.Assign]:
            resolveEnd(conn, node.nodes[0], funcName)
        elif type(node) is Tree.InitStruct:
            b = Connection(node)
            for i in range(len(node.nodes)):
                n = b.node.paramNames[i]

                b.fields[n] = Connection(b)
                resolveEnd(b.fields[b.node.paramNames[i]], node.nodes[i], funcName)
            conn.connect(b)

    def findEndpoints(node, conn=connectionGraph, name= ""):
        for i in node:

            if not i.isEnd() and not type(i) is Tree.FuncBraceOpen:
                if type(i) is Tree.FuncCall:
                    if i.inline:
                        findEndpoints(i, conn, i.name )
                    else:
                        findEndpoints(i, conn, name )
                else:
                    findEndpoints(i, conn, name )

            if type(i) is Tree.FuncStart:
                conn = Connection(i, True)
                connectionGraph.connect(conn)
                name = i.name

            elif type(i) is Tree.FuncBody:
                c = funcReturns[i.package+"."+i.name]

                if not type(i.returnType) is Types.Null:
                    resolveEnd(c, i.nodes[-1], name)
                conn.connect(c)
                conn = connectionGraph

                name = ""

            elif type(i) is Tree.Assign:
                resolveEnd(vars[i.package + "." + name + "." + i.name], i, name)

            elif type(i) is Tree.FieldWrite:
                if type(i.nodes[0]) is Tree.ReadVar:
                    v = vars[i.nodes[0].package + "." + name+"."+ i.nodes[0].name]
                else:
                    v = Connection(i)
                    resolveEnd(v, i.nodes[0], name)
                    conn.connect(v)
                    v = conn


                if i.field in v.fields:
                    v.fields[i.field] = Connection(None)
                resolveEnd(v, i, name)






            elif type(i) is Tree.Create:
                v = Connection(i, 2 if i.isGlobal else 0)

                vars[i.package + "." + name+ "." + i.name] = v

                if i.isGlobal:
                    conn.connect(v)

    funcs = {}

    def findFunctions(tree):
        for c in tree:
            for i in c:
                if type(i) is Tree.FuncBraceOpen:
                    funcs[i.package+"."+i.name] = []
                    for c in i:
                        v = Connection(c, False)
                        vars[c.package + "." + i.name+"."+c.name] = v
                        funcs[i.package+"."+i.name].append(v)
                elif type(i) is Tree.FuncBody:
                    funcReturns[i.package+"."+i.name] = Connection(i)

    def findEscaping(conn, color= 0):
        for i in conn:
            conn.setColor(i.color)

            if not i.isEnd():
                findEscaping(i, 2 if i.color == 2 else color )

            if (type(conn.node) is Tree.Operator and conn.node.kind == "&") or (isPointer(i.node) and not type(i.node) is Tree.FuncCall):
                i.setColor( 2 if i.color == 2 else color if color > 0 else 1)

    findFunctions(tree)
    findEndpoints(tree)

    findEscaping(connectionGraph)

    #visual(connectionGraph)
