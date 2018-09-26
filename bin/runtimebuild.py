pasteInto = "../runtime/runtimeTop.c"
modules = ["array", "maybe", "memory"]

from TopCompiler import topc
topc.start(compileRuntime=True)

output = open("lib/_global.c", mode="r")
output_h = open("lib/_global.h", mode="r")

code = output_h.read() + output.read()

file = open(pasteInto, mode="w")
file.write(code)
file.close()
output.close()
output_h.close()
