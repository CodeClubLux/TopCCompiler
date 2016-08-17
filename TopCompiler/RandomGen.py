file = open("test/TopCompiler/"+input("filename: "), mode= "w")
sizeOfFunc = input("size of func: ")
lines = input("lines of code: ")

out = []
for i in range(int(int(lines) / int(sizeOfFunc)+2)):
    out.append("def func"+str(i)+"() =\n")
    for c in range(int(sizeOfFunc)):
        out.append('    println "hello world" \n')

file.write("".join(out))
file.close()