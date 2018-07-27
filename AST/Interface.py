from .node import *

class Interface(Node):
    def __init__(self, iType, name):
        self.iType = iType
        self.name = name

    def compileToC(self, codegen):
        iType = self.iType
        context = codegen.getName()
        methods = {}

        pNone = Types.Pointer(Types.Null(), True)

        for methName in iType.methods:
            meth = iType.methods[methName]
            f = Types.FuncPointer([pNone] + meth.args, meth.returnType, meth.generic, meth.do)
            methods[methName] = f

        #interface as c struct
        codegen.append("struct " + self.name + "{\n")
        codegen.append("void* type; /* is always null, for now */ \n") #@cleanup change to real type once type introspection is possible
        codegen.append("void* data;\n")

        for field in iType.types:
            codegen.append(f"unsigned short field_{field};\n") #just store offset, should be long enough let's see
        for field in methods:
            codegen.append(f"{methods[field].toCType()} method_{field};\n")
        codegen.append("};")

        #helper function from struct to interface
        codegen.append(f"static inline struct {self.name} {self.name}FromStruct(void* data")
        names = []
        for field in iType.types:
            n = codegen.getName()
            codegen.append(f", short {n}")
            names.append(n)

        for field in methods:
            n = codegen.getName()
            codegen.append(f", {methods[field].toCType()} {n}")
            names.append(n)

        codegen.append("){ \n")

        tmp = codegen.getName()

        codegen.append(f"struct {self.name} {tmp};\n")

        codegen.append(f"{tmp}.data = data;")
        for (name, field) in zip(names, iType.types):
            codegen.append(f"{tmp}.field_{field} = {name};\n")
        for (name, field) in zip(names, methods):
            codegen.append(f"{tmp}.method_{field} = {name};\n")
        codegen.append(f"return {tmp}; \n}}")

        #helper function to access fields
        for field in iType.types:
            typ = iType.types[field].toCType()
            codegen.append(f"static inline {typ}* {self.name}_{field}(struct {self.name} {tmp}, struct _global_Context* {context}){{\n")
            codegen.append(f"return ({typ}*)({tmp}.data + {tmp}.field_{field});")
            codegen.append("\n};")

        #helper function to call methods
        for field in methods:
            typ = methods[field]
            codegen.append(f"static inline {typ.returnType.toCType()} {self.name}_{field}(struct {self.name}* {tmp}")
            names = []
            for i in typ.args[1:]:
                n = codegen.getName()
                names.append(n)
                codegen.append(f",{i.toCType()} {n}")
            codegen.append(f",struct _global_Context* {context}")

            codegen.append(f"){{\n")
            codegen.append(f"return {tmp}->method_{field}({tmp}->data")
            for i in names:
                codegen.append(f",{n}")
            codegen.append(f",{context}")
            codegen.append(");")
            codegen.append("\n};")

            codegen.append(f"static inline {typ.returnType.toCType()} {self.name}_{field}ByValue(struct {self.name} {tmp}")
            for (iter, i) in enumerate(typ.args[1:]):
                codegen.append(f",{i.toCType()} {names[iter]}")
            codegen.append(f",struct _global_Context* {context}")
            codegen.append(f"){{\n")

            data = codegen.getName()
            codegen.append(f"return {tmp}.method_{field}({tmp}.data")
            for i in names:
                codegen.append(f",{n}")
            codegen.append(f",{context}")
            codegen.append(");")
            codegen.append("\n};")


        """
        struct Animal Animal_FromString(void* data, size_t offset)
            struct Animal a;
            a.data = data;
            a.type = type;
            a.offset = offset;
        };
        
        
        """