from .node import *

from TopCompiler import Parser

class Interface(Node):
    def __init__(self, iType, name):
        self.iType = iType
        self.name = name

    def compileToC(self, codegen):
        codegen.inFunction()

        iType = self.iType
        context = codegen.getName()
        methods = {}

        pNone = Types.Pointer(Types.Null(), True)

        for methName in iType.methods:
            meth = iType.methods[methName]
            f = Types.FuncPointer([pNone] + meth.args, meth.returnType, meth.generic, meth.do)
            methods[methName] = f

        #interface as c struct
        vtable_name = self.name + "_VTABLE"

        codegen.append("struct " + self.name + " {\n")
        codegen.append(f"struct {vtable_name}* vtable;\n")
        codegen.append("void* data;\n")
        codegen.append("};")

        type_interface = "struct _global_Type"

        codegen.append(f"struct {vtable_name} {{")
        codegen.append(f"{type_interface} type;")
        for field in methods:
            codegen.append(f"{methods[field].toCType()} method_{field};\n")
        codegen.append("};")

        type_interface = Parser.IType.toCType()


        #for field in iType.types:
        #    codegen.append(f"unsigned short field_{field};\n") #just store offset, should be long enough let's see

        #helper function from struct to interface
        codegen.append(f"static inline struct {self.name} {self.name}FromStruct(void* data, struct {vtable_name}* vtable, {type_interface} typ")
        method_names = []

        for field in methods:
            n = codegen.getName()
            codegen.append(f", {methods[field].toCType()} {n}")
            method_names.append(n)

        codegen.append("){ \n")

        tmp = codegen.getName()

        codegen.append(f"struct {self.name} {tmp};\n")

        codegen.append(f"{tmp}.data = data;")
        codegen.append(f"{tmp}.vtable = vtable;")
        for (name, field) in zip(method_names, methods):
            codegen.append(f"{tmp}.vtable->method_{field} = {name};\n")
        codegen.append(f"{tmp}.vtable->type = typ;\n")
        codegen.append(f"return {tmp}; \n}}")

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
            codegen.append(f"return {tmp}->vtable->method_{field}({tmp}->data")
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
            codegen.append(f"return {tmp}.vtable->method_{field}({tmp}.data")
            for i in names:
                codegen.append(f",{n}")
            codegen.append(f",{context}")
            codegen.append(");")
            codegen.append("\n};")

        codegen.append(f"{type_interface} {self.name}_get_type(struct {self.name}* {tmp}, struct _global_Context* context)")
        codegen.append("{ return " + tmp + "->vtable->type; }")

        codegen.append(f"{type_interface} {self.name}_get_typeByValue(struct {self.name} {tmp}, struct _global_Context* context)")
        codegen.append("{ return " + tmp + ".vtable->type; }\n")

        interface_type = Parser.InterfaceType.toCType()

        typ_name = f"{self.name}_Type"
        codegen.append(f"{interface_type} {typ_name};")

        codegen.outFunction()


        def as_string(s):
            return f'_global_StringInit({len(s)}, "{s}")'

        codegen.append(f"{typ_name}.name = " + as_string(iType.normalName))
        codegen.append(f";{typ_name}.package = " + as_string(iType.package) + ";")


        """
        struct Animal Animal_FromString(void* data, size_t offset)
            struct Animal a;
            a.data = data;
            a.type = type;
            a.offset = offset;
        };
        
        
        """