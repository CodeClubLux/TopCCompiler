from .node import *

class Lens(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def compileToJS(self, codegen):
        name = codegen.getName()
        old = codegen.getName()

        self.nodes[0].newValue = name

        self.place.compileToJS = lambda codegen: codegen.append(name)
        codegen.append("newLens(function("+name+"){return ")
        self.nodes[0].compileToJS(codegen)
        codegen.append("}, function("+old+","+name+"){")
        self.place.owner.set(old, codegen)
        codegen.append("})")

    def validate(self, parser):
        pass

    def __str__(self):
        return "Lens"
