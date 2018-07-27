from .node import *

class Interface(Node):
    def __init__(self, iType, name):
        self.iType = iType
        self.name = name

    def compileToC(self, codegen):
        #interface as c struct
        codegen.append("struct " + self.name + "{\n")
        codegen.append("void* type; /* is always null, for now */") #@cleanup change to real type once type introspection is possible
        codegen.append("void* data;")

        iType = self.iType

        for field in iType.types:
            codegen.append(f"unsigned short field_{field};\n") #just store offset, should be long enough let's see
        for field in iType.methods:
            codegen.append(f"{iType.methods[field].toCType()} method_{field};\n")
        codegen.append("};")

        #helper function from struct to interface
        codegen.append(f"static inline struct {self.name} {self.name}FromStruct(void* data")
        names = []
        for field in iType.types:
            n = codegen.getName()
            codegen.append(f", short {n}")
            names.append(n)

        for field in iType.methods:
            n = codegen.getName()
            codegen.append(f", {iType.methods[field].toCType()} {n}")
            names.append(n)
        codegen.append("){ \n")

        tmp = codegen.getName()

        codegen.append(f"struct {self.name} {tmp};\n")
        codegen.append(f"{tmp}.data = data;")
        for (name, field) in zip(names, iType.types):
            codegen.append(f"{tmp}.field_{field} = {name};\n")
        for (name, field) in zip(names, iType.methods):
            codegen.append(f"{tmp}.method_{field} = {name};\n")
        codegen.append(f"return {tmp}; \n}}")

        #helper function to access fields
        for field in iType.types:
            typ = iType.types[field].toCType()
            codegen.append(f"static inline {typ}* {self.name}_{field}(struct {self.name} {tmp}){{\n")
            codegen.append(f"return ({typ}*)({tmp}.data + {tmp}.field_{field});")
            codegen.append("\n};")

        #helper function to call methods
        for field in iType.methods:
            typ = iType.methods[field]
            codegen.append(f"static inline {typ.returnType.toCType()} {self.name}_{field}(struct {self.name}* {tmp}")
            names = []
            for i in typ.args:
                n = codegen.getName()
                names.append(n)
                codegen.append(f",{i.toCType()} {n}")

            codegen.append(f"){{\n")
            codegen.append(f"return {tmp}->method_{field}({tmp}->data")
            for i in names:
                codegen.append(f",{n}")
            codegen.append(");")
            codegen.append("\n};")

            codegen.append(f"static inline {typ.returnType.toCType()} {self.name}_{field}ByValue(struct {self.name} {tmp}")
            for (iter, i) in enumerate(typ.args):
                codegen.append(f",{i.toCType()} {names[i]}")
            codegen.append(f"){{\n")
            data = codegen.getName()
            codegen.append(f"return {tmp}.method_{field}({tmp}.data")
            for i in names:
                codegen.append(f",{n}")
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