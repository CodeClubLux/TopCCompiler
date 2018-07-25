pasteInto = "/Users/luke/Desktop/games/TopCCompiler/TopCompiler/runtime/runtimeTop.c"
modules = ["array", "maybe", "memory"]

combined = []
for mod in modules:
    f = open("src/"+mod+".top", mode="r")
    combined.append(f.read())
    f.close()

_global = open("src/_global.top", mode="w")
_global.write("\n".join(combined))

from TopCompiler import topc
topc.start()

output = open("bin/TopRuntime.c", mode="r")

file = open(pasteInto, mode="w")
file.write(output.read())
file.close()
output.close()
