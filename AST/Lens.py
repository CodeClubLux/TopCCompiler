from .node import *

class Lens(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToJS(self, codegen):
        name = codegen.getName()
        old = codegen.getName()

        self.place.name = name

        def loop(n):
            for i in n:
                if type(i) is Tree.Field:
                    codegen.append('+"' + "."+i.field + '"')
                elif type(i) is Tree.ArrRead:
                    codegen.append('+"' + '["+')
                    i.nodes[1].compileToJS(codegen)
                    codegen.append('+"]"')
                if not i.isEnd():
                    loop(i)

        self.nodes[0].newValue = name
        codegen.append("newLens(function("+name+"){return ")
        self.nodes[0].compileToJS(codegen)
        codegen.append("}, function("+old+","+name+"){")
        self.place.owner.set(old, codegen)
        codegen.append("},''")
        loop(self)
        codegen.append(")")

    def validate(self, parser):
        pass

    def __str__(self):
        return "Lens"