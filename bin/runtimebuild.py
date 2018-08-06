pasteInto = "/Users/luke/Desktop/games/TopCCompiler/TopCompiler/runtime/runtimeTop.c"
modules = ["array", "maybe", "memory"]

from TopCompiler import topc
topc.start(compileRuntime=True)

output = open("lib/_global.c", mode="r")

file = open(pasteInto, mode="w")
file.write(output.read())
file.close()
output.close()
