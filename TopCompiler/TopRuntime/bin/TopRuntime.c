#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>
#include <math.h>
#include <stdint.h>

struct _global_String {
    unsigned int length;
    char* data;
};
typedef struct _global_String(*prnonep___string)(void*,struct _global_Context*) ;
struct _global_Type {
struct _global_Type_VTABLE* vtable;
void* data;
};struct _global_Type_VTABLE {struct _global_Type type;prnonep___string method_toString;
};static inline struct _global_Type _global_TypeFromStruct(void* data, struct _global_Type_VTABLE* vtable, struct _global_Type typ, prnonep___string c){ 
struct _global_Type d;
d.data = data;d.vtable = vtable;d.vtable->method_toString = c;
d.vtable->type = typ;
return d; 
}static inline struct _global_String _global_Type_toString(struct _global_Type* d,struct _global_Context* b){
return d->vtable->method_toString(d->data,b);
};static inline struct _global_String _global_Type_toStringByValue(struct _global_Type d,struct _global_Context* b){
return d.vtable->method_toString(d.data,b);
};struct _global_Type _global_Type_get_type(struct _global_Type* d, struct _global_Context* context){ return d->vtable->type; }struct _global_Type _global_Type_get_typeByValue(struct _global_Type d, struct _global_Context* context){ return d.vtable->type; }
struct _global_InterfaceType _global_Type_Type;struct _global_StaticArray_StaticArray_S_Field {
struct _global_Field* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Field _global_StaticArray_StaticArray_S_FieldInit(struct _global_Field* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Field C;
C.data=data;C.length=length;return C;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_FieldType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Field_get_type(struct _global_StaticArray_StaticArray_S_Field* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Field_get_typeByValue(struct _global_StaticArray_StaticArray_S_Field self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_FieldType;struct _global_StructType {
struct _global_String name;
struct _global_String package;
struct _global_Type real_type;
struct _global_StaticArray_StaticArray_S_Field fields;
};
static inline struct _global_StructType _global_StructTypeInit(struct _global_String name,struct _global_String package,struct _global_Type real_type,struct _global_StaticArray_StaticArray_S_Field fields){
struct _global_StructType j;
j.name=name;j.package=package;j.real_type=real_type;j.fields=fields;return j;
};
struct _global_StructType _global_StructTypeType;struct _global_StructType* _global_StructType_get_type(struct _global_StructType* self, struct _global_Context* c){return &_global_StructTypeType;}
struct _global_StructType* _global_StructType_get_typeByValue(struct _global_StructType self, struct _global_Context* c){return &_global_StructTypeType;}
struct _global_Type_VTABLE rStringType_VTABLE_FOR_Type;struct _global_Type_VTABLE rStructType_VTABLE_FOR_Type;struct _global_Type_VTABLE rInterfaceType_VTABLE_FOR_Type;struct _global_Type_VTABLE rArrayType_VTABLE_FOR_Type;struct _global_InterfaceType {
struct _global_String name;
struct _global_String package;
struct _global_StaticArray_StaticArray_S_Field fields;
struct _global_StaticArray_StaticArray_S_Method* methods;
};
static inline struct _global_InterfaceType _global_InterfaceTypeInit(struct _global_String name,struct _global_String package,struct _global_StaticArray_StaticArray_S_Field fields,struct _global_StaticArray_StaticArray_S_Method* methods){
struct _global_InterfaceType D;
D.name=name;D.package=package;D.fields=fields;D.methods=methods;return D;
};
struct _global_StructType _global_InterfaceTypeType;struct _global_StructType* _global_InterfaceType_get_type(struct _global_InterfaceType* self, struct _global_Context* c){return &_global_InterfaceTypeType;}
struct _global_StructType* _global_InterfaceType_get_typeByValue(struct _global_InterfaceType self, struct _global_Context* c){return &_global_InterfaceTypeType;}
struct _global_ArraySize_Static {
unsigned int field0;

};union _global_ArraySize_cases {
struct _global_ArraySize_Static Static;

};
struct _global_ArraySize {
 char tag;
union _global_ArraySize_cases cases;

};
struct _global_ArraySize _global_Static(unsigned int l,struct _global_Context* m){
struct _global_ArraySize n;
n.cases.Static.field0 = l;n.tag = 0;
return n;}
struct _global_ArraySize _global_Dynamic;
struct _global_ArraySize _global_Both;
struct _global_StructType _global_ArraySizeType;struct _global_StructType* _global_ArraySize_get_type(struct _global_ArraySize* self, struct _global_Context* c){return &_global_ArraySizeType;}
struct _global_StructType* _global_ArraySize_get_typeByValue(struct _global_ArraySize self, struct _global_Context* c){return &_global_ArraySizeType;}
struct _global_ArrayType {
struct _global_ArraySize size;
struct _global_Type array_type;
};
static inline struct _global_ArrayType _global_ArrayTypeInit(struct _global_ArraySize size,struct _global_Type array_type){
struct _global_ArrayType p;
p.size=size;p.array_type=array_type;return p;
};
struct _global_StructType _global_ArrayTypeType;struct _global_StructType* _global_ArrayType_get_type(struct _global_ArrayType* self, struct _global_Context* c){return &_global_ArrayTypeType;}
struct _global_StructType* _global_ArrayType_get_typeByValue(struct _global_ArrayType self, struct _global_Context* c){return &_global_ArrayTypeType;}
struct _global_Type_VTABLE rEnumType_VTABLE_FOR_Type;struct _global_StaticArray_StaticArray_S_Type {
struct _global_Type* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Type _global_StaticArray_StaticArray_S_TypeInit(struct _global_Type* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Type r;
r.data=data;r.length=length;return r;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_TypeType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Type_get_type(struct _global_StaticArray_StaticArray_S_Type* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_TypeType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Type_get_typeByValue(struct _global_StaticArray_StaticArray_S_Type self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_TypeType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_TypeType;struct _global_Cases {
struct _global_String name;
struct _global_StaticArray_StaticArray_S_Type args;
};
static inline struct _global_Cases _global_CasesInit(struct _global_String name,struct _global_StaticArray_StaticArray_S_Type args){
struct _global_Cases s;
s.name=name;s.args=args;return s;
};
struct _global_StructType _global_CasesType;struct _global_StructType* _global_Cases_get_type(struct _global_Cases* self, struct _global_Context* c){return &_global_CasesType;}
struct _global_StructType* _global_Cases_get_typeByValue(struct _global_Cases self, struct _global_Context* c){return &_global_CasesType;}
struct _global_StaticArray_StaticArray_S_Cases {
struct _global_Cases* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Cases _global_StaticArray_StaticArray_S_CasesInit(struct _global_Cases* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Cases v;
v.data=data;v.length=length;return v;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_CasesType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Cases_get_type(struct _global_StaticArray_StaticArray_S_Cases* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CasesType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Cases_get_typeByValue(struct _global_StaticArray_StaticArray_S_Cases self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CasesType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_CasesType;struct _global_PointerType {
struct _global_Type p_type;
};
static inline struct _global_PointerType _global_PointerTypeInit(struct _global_Type p_type){
struct _global_PointerType G;
G.p_type=p_type;return G;
};
struct _global_StructType _global_PointerTypeType;struct _global_StructType* _global_PointerType_get_type(struct _global_PointerType* self, struct _global_Context* c){return &_global_PointerTypeType;}
struct _global_StructType* _global_PointerType_get_typeByValue(struct _global_PointerType self, struct _global_Context* c){return &_global_PointerTypeType;}
struct _global_Method {
struct _global_String name;
void* pointer_to_method;
};
static inline struct _global_Method _global_MethodInit(struct _global_String name,void* pointer_to_method){
struct _global_Method w;
w.name=name;w.pointer_to_method=pointer_to_method;return w;
};
struct _global_StructType _global_MethodType;struct _global_StructType* _global_Method_get_type(struct _global_Method* self, struct _global_Context* c){return &_global_MethodType;}
struct _global_StructType* _global_Method_get_typeByValue(struct _global_Method self, struct _global_Context* c){return &_global_MethodType;}
struct _global_Type_VTABLE rPointerType_VTABLE_FOR_Type;struct _global_Type_VTABLE rNoneType_VTABLE_FOR_Type;struct _global_StaticArray_StaticArray_S_Method {
struct _global_Method* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Method _global_StaticArray_StaticArray_S_MethodInit(struct _global_Method* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Method y;
y.data=data;y.length=length;return y;
};
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Method_get_type(struct _global_StaticArray_StaticArray_S_Method* self, struct _global_Context* c){return NULL;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Method_get_typeByValue(struct _global_StaticArray_StaticArray_S_Method self, struct _global_Context* c){return NULL;}
struct _global_EnumType {
struct _global_String name;
struct _global_String package;
struct _global_StaticArray_StaticArray_S_Cases cases;
struct _global_StaticArray_StaticArray_S_Method methods;
};
static inline struct _global_EnumType _global_EnumTypeInit(struct _global_String name,struct _global_String package,struct _global_StaticArray_StaticArray_S_Cases cases,struct _global_StaticArray_StaticArray_S_Method methods){
struct _global_EnumType z;
z.name=name;z.package=package;z.cases=cases;z.methods=methods;return z;
};
struct _global_StructType _global_EnumTypeType;struct _global_StructType* _global_EnumType_get_type(struct _global_EnumType* self, struct _global_Context* c){return &_global_EnumTypeType;}
struct _global_StructType* _global_EnumType_get_typeByValue(struct _global_EnumType self, struct _global_Context* c){return &_global_EnumTypeType;}
struct _global_Field {
struct _global_String name;
unsigned int offset;
struct _global_Type field_type;
};
static inline struct _global_Field _global_FieldInit(struct _global_String name,unsigned int offset,struct _global_Type field_type){
struct _global_Field g;
g.name=name;g.offset=offset;g.field_type=field_type;return g;
};
struct _global_StructType _global_FieldType;struct _global_StructType* _global_Field_get_type(struct _global_Field* self, struct _global_Context* c){return &_global_FieldType;}
struct _global_StructType* _global_Field_get_typeByValue(struct _global_Field self, struct _global_Context* c){return &_global_FieldType;}
struct _global_Type_VTABLE rIntType_VTABLE_FOR_Type;typedef unsigned int(*prnonep___uint)(void*,struct _global_Context*) ;
struct _global_AliasType {
struct _global_String name;
struct _global_String package;
struct _global_Type real_type;
};
static inline struct _global_AliasType _global_AliasTypeInit(struct _global_String name,struct _global_String package,struct _global_Type real_type){
struct _global_AliasType K;
K.name=name;K.package=package;K.real_type=real_type;return K;
};
struct _global_StructType _global_AliasTypeType;struct _global_StructType* _global_AliasType_get_type(struct _global_AliasType* self, struct _global_Context* c){return &_global_AliasTypeType;}
struct _global_StructType* _global_AliasType_get_typeByValue(struct _global_AliasType self, struct _global_Context* c){return &_global_AliasTypeType;}
struct _global_AliasType _global_SizeT_Type;struct _global_Type_VTABLE rAliasType_VTABLE_FOR_Type;typedef void*(*prnonec_SizeTp___rnone)(void*,unsigned int,struct _global_Context*) ;
typedef void(*prnonec_rnonep___none)(void*,void*,struct _global_Context*) ;
typedef void(*prnonec_uintp___none)(void*,unsigned int,struct _global_Context*) ;
struct _global_Allocator {
struct _global_Allocator_VTABLE* vtable;
void* data;
};struct _global_Allocator_VTABLE {struct _global_Type type;prnonep___uint method_get_occupied;
prnonec_SizeTp___rnone method_alloc;
prnonec_rnonep___none method_dealloc;
prnonec_uintp___none method_reset_to;
};static inline struct _global_Allocator _global_AllocatorFromStruct(void* data, struct _global_Allocator_VTABLE* vtable, struct _global_Type typ, prnonep___uint M, prnonec_SizeTp___rnone N, prnonec_rnonep___none P, prnonec_uintp___none Q){ 
struct _global_Allocator R;
R.data = data;R.vtable = vtable;R.vtable->method_get_occupied = M;
R.vtable->method_alloc = N;
R.vtable->method_dealloc = P;
R.vtable->method_reset_to = Q;
R.vtable->type = typ;
return R; 
}static inline unsigned int _global_Allocator_get_occupied(struct _global_Allocator* R,struct _global_Context* J){
return R->vtable->method_get_occupied(R->data,J);
};static inline unsigned int _global_Allocator_get_occupiedByValue(struct _global_Allocator R,struct _global_Context* J){
return R.vtable->method_get_occupied(R.data,J);
};static inline void* _global_Allocator_alloc(struct _global_Allocator* R,unsigned int T,struct _global_Context* J){
return R->vtable->method_alloc(R->data,T,J);
};static inline void* _global_Allocator_allocByValue(struct _global_Allocator R,unsigned int T,struct _global_Context* J){
return R.vtable->method_alloc(R.data,T,J);
};static inline void _global_Allocator_dealloc(struct _global_Allocator* R,void* W,struct _global_Context* J){
return R->vtable->method_dealloc(R->data,W,J);
};static inline void _global_Allocator_deallocByValue(struct _global_Allocator R,void* W,struct _global_Context* J){
return R.vtable->method_dealloc(R.data,W,J);
};static inline void _global_Allocator_reset_to(struct _global_Allocator* R,unsigned int Y,struct _global_Context* J){
return R->vtable->method_reset_to(R->data,Y,J);
};static inline void _global_Allocator_reset_toByValue(struct _global_Allocator R,unsigned int Y,struct _global_Context* J){
return R.vtable->method_reset_to(R.data,Y,J);
};struct _global_Type _global_Allocator_get_type(struct _global_Allocator* R, struct _global_Context* context){ return R->vtable->type; }struct _global_Type _global_Allocator_get_typeByValue(struct _global_Allocator R, struct _global_Context* context){ return R.vtable->type; }
struct _global_InterfaceType _global_Allocator_Type;struct _global_Context {
struct _global_Allocator* allocator;struct _global_Allocator* longterm_storage;};
struct _global_Context _global_context;
#define __Context struct _global_Context* context
#define alloc _global_Allocator_alloc

struct _global_String _global_StringInit(unsigned int length, char* data) {
    struct _global_String s;
    s.data = data;
    s.length = length;
    return s;
};
struct _global_String _global_String_toStringByValue(struct _global_String s,__Context) {
    return s;
}

struct _global_String _global_String_toString(struct _global_String* s,__Context) {
    return *s;
}

struct _global_String _global_Bool_toStringByValue(_Bool b, __Context) {
    if (b) {
        return _global_StringInit(4, "true");
    } else {
        return _global_StringInit(5, "false");
    }
}

struct BoolType {};

struct BoolType _global_Bool_typ;

struct BoolType* _global_Bool_get_typeByValue(_Bool b, __Context) {
    return &_global_Bool_typ;
}

struct BoolType* _global_Bool_get_type(_Bool* b, __Context) {
    return &_global_Bool_typ;
}



struct _global_String _global_Bool_toString(_Bool* b, __Context) {
    return _global_Bool_toStringByValue(*b, context);
}

_Bool _global_String_op_eqByValue(struct _global_String self, struct _global_String other, __Context) {
    if (self.length != other.length) {
        return 0;
    }

    for (unsigned int i =0; i < self.length; i++) {
        if (self.data[i] != other.data[i]) {
            return 0;
        }
    }
    return 1;
}

struct _global_String _global_String_op_eq(struct _global_String* s, struct _global_String* other, __Context) {
    _global_String_op_eqByValue(*s, *other, context);
}

void _global_log(struct _global_String,__Context);

struct _global_String _global_String_op_addByValue(struct _global_String a, struct _global_String b,__Context) {
    if (a.length == 0) {
        return b;
    } else if (b.length == 0) {
        return a;
    }

    struct _global_String newString;
    newString.length = a.length + b.length;
    newString.data = alloc(context->allocator, sizeof(char) * (newString.length+1), context);

    memcpy(newString.data, a.data, sizeof(char) * a.length);
    memcpy(newString.data + a.length, b.data, sizeof(char) * (b.length + 1));
    return newString;
};

struct _global_String _global_String_op_add(struct _global_String* a, struct _global_String b,__Context) {
    return _global_String_op_addByValue(*a, b, context);
}

struct FloatType {
    unsigned int size;
};

struct _global_String _global_Float_toStringByValue(float x,__Context) {
    int len = snprintf(NULL, 0, "%f", x);
    char *result = (char *)alloc(context->allocator, len + 1, context);
    snprintf(result, len + 1, "%f", x);
    return _global_StringInit(len,result);
}

struct _global_String _global_Float_toString(float* x,__Context) {
    return _global_Float_toStringByValue(*x, context);
}

struct FloatType _global_FloatType;

struct FloatType* _global_Float_get_type(float* x, __Context) {
    return &_global_FloatType;
}

struct FloatType* _global_Float_get_typeByValue(float x, __Context) {
    return &_global_FloatType;
}

void _reverse_string(struct _global_String * self) {
    unsigned int half_length = self->length / 2;

    for (unsigned int i = 0; i < half_length; i++) {
        char tmp = self->data[i];
        self->data[i] = self->data[self->length - 1 - i];
        self->data[self->length - 1 - i] = tmp;
    }
}


struct NoneType {};

struct NoneType _global_NoneTypeInit() {
    struct NoneType s;
    return s;
}

struct NoneType None_Type;

/*
void itoa(int value, char* str, int base) {
	static char num[] = "0123456789abcdefghijklmnopqrstuvwxyz";
	char* wstr=str;

	int sign;
	// Validate base
	if (base<2 || base>35){ *wstr='\0'; return; }
	// Take care of sign

	if ((sign=value) < 0) value = -value;
	// Conversion. Number is reversed.

	do *wstr++ = num[value%base]; while(value/=base);

	if(sign<0) *wstr++='-';

	*wstr='\0';
	// Reverse string
}
*/

struct _global_String _global_int_toStringByValue(int number,__Context) {
    unsigned int length = 1;
    unsigned int divisor = 10;

    int absNumber = number;
    if (absNumber < 0) {
        absNumber = -absNumber;
    }

    while (absNumber % divisor != absNumber) {
        length++;
        divisor *= 10;
    }

    if (number < 0) {
        length++;
    }

    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);

    struct _global_String newString = _global_StringInit(length, memory);
    snprintf(newString.data, 10, "%d", number);

    return newString;
}

struct _global_String _global_int_toString(int* number,__Context) {
    return _global_int_toStringByValue(*number, context);
}

char* _global_String_to_c_string(struct _global_String* s, __Context) {
    return s->data;
}

char* _global_String_to_c_stringByValue(struct _global_String s, __Context) {
    return s.data;
}

struct IntType {
    _Bool sign;
    unsigned int size;
};

struct IntType _global_IntType;

#define gen_integer(name, typ, sign_of_int) struct _global_String _global_##name##_toString(typ* number,__Context) {\
return _global_int_toStringByValue(*number, context); \
} \
struct _global_String _global_##name##_toStringByValue(typ number,__Context) {\
return _global_int_toStringByValue(number, context); \
} \
\
struct IntType _global_##name##Type;\
void _global_##name##TypeInit() { \
    _global_##name##Type.sign = sign_of_int; \
    _global_##name##Type.size = sizeof(typ); \
} \
struct IntType* _global_##name##_get_typeByValue(typ number, __Context) { \
    return &_global_##name##Type; \
} \
\
struct IntType* _global_##name##_get_type(typ* number, __Context) { \
    return &_global_##name##Type; \
}

struct IntType* _global_int_get_typeByValue(int number, __Context) {
    return &_global_IntType;
}

struct IntType* _global_int_get_type(int* number, __Context) {
    return &_global_IntType;
}


gen_integer(uint, unsigned int, 0)
gen_integer(u8, uint8_t, 0)
gen_integer(u16, uint16_t, 0)
gen_integer(u32, uint32_t, 0)
gen_integer(u64, uint64_t, 0)

gen_integer(i8, int8_t, 1)
gen_integer(i16, int16_t, 1)
gen_integer(i32, int32_t, 1)
gen_integer(i64, int64_t, 1)

void _global_c_log(struct _global_String s) {
    printf("%s\n", s.data);
    fflush(stdout);
};

static inline void* _global_offsetPtr(void* ptr, int offset, __Context) {
    return ((char*)ptr) + offset;
};



struct _global_String _global_console_input(struct _global_String text, __Context) {
    char string[40];
    fputs(text.data, stdout);
    fflush(stdout);
    fgets(string, sizeof(string), stdin);
    fflush(stdin);



    unsigned int length = strlen(string);
    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);
    memcpy(memory, string, length + 1);
    return _global_StringInit(length, memory);
}



FILE* _runtime_c_open_file(struct _global_String filename, struct _global_String acess) {
    char * buffer = 0;
    int length;
    FILE* f;
    #ifdef __APPLE__
        f = fopen(filename.data, acess.data);
    #else
        errno_t errors = fopen_s(&f, filename.data, acess.data);

        if (errors) { return NULL; }
    #endif

    return f;
}

struct _global_String _runtime_read_file(FILE* f, __Context) {
    fseek (f, 0, SEEK_END);
    int length = ftell (f);
    fseek (f, 0, SEEK_SET);
    char* buffer = alloc(context->allocator, length + 1, context);

    length = fread(buffer, sizeof(char), length, f);
    buffer[length] = '\0';

    return _global_StringInit(length, buffer);
}

void _runtime_c_close_file(FILE* file) {
    fclose (file);
}

struct _global_String _runtime_char_buffer_toString(char* buffer) {
    return _global_StringInit(strlen(buffer), buffer);
}

//char

struct _global_String _global_char_toStringByValue(char self, __Context) {
    char* buffer = alloc(context->allocator, 2, context);
    buffer[0] = self;
    buffer[1] = '\0';
    return _global_StringInit(1, buffer);
}

struct _global_String _global_char_toString(char* self, __Context) {
    return _global_char_toStringByValue(*self, context);
}

uint8_t _global_char_toU8ByValue(char self, __Context) {
    return (uint8_t) self;
}

uint8_t _global_char_toU8(char* self, __Context) {
    return (uint8_t) *self;
}








#define _global_indexPtr(value, by, c) value + by
#define _global_c_set_bit_to(number, n, x) (number & ~(1U << n) | (x << n))
#define _global_c_is_bit_set(number, n) ((number >> n) & 1U)

/*
void printI(int i) {
    printf("%i\n", i);
};
*/

struct StringType {
};

struct StringType _global_StringType;

struct StringType* _global_String_get_type(struct _global_String* s, __Context) {
    return &_global_StringType;
}

struct StringType* _global_String_get_typeByValue(struct _global_String s, __Context) {
    return &_global_StringType;
}

struct _global_PointerType pointerTypes[100];
unsigned int pointerTypeCounter;

struct _global_PointerType* _global_boxPointerType(struct _global_PointerType p, __Context) {
    if (pointerTypeCounter > 99) {
        printf("More pointer types than available");
    }

    pointerTypes[pointerTypeCounter++] = p;
    return &pointerTypes[pointerTypeCounter - 1];
}

void _global_init_c_runtime() {
    printf("Initialized types\n");

    pointerTypeCounter = 0;
    _global_FloatType.size = sizeof(float);
    _global_IntType.sign = 1;
    _global_IntType.size = sizeof(int);

    _global_u8TypeInit();
    _global_u16TypeInit();
    _global_u32TypeInit();
    _global_u64TypeInit();
    _global_uintTypeInit();

    _global_i8TypeInit();
    _global_i16TypeInit();
    _global_i32TypeInit();
    _global_i64TypeInit();

    /*
    _global_##name##TypeInit()
    gen_integer(uint, unsigned int, 0)
gen_integer(u8, uint8_t, 0)
gen_integer(u16, uint16_t, 0)
gen_integer(u32, uint32_t, 0)
gen_integer(u64, uint64_t, 0)

gen_integer(i8, int8_t, 1)
gen_integer(i16, int16_t, 1)
gen_integer(i32, int32_t, 1)
gen_integer(i64, int64_t, 1) */
}

struct _global_Context _global_context;
#include <string.h>

struct _global_TemporaryStorage {
unsigned int occupied;
unsigned int highest;
void* data;
unsigned int maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(unsigned int occupied,unsigned int highest,void* data,unsigned int maxSize){
struct _global_TemporaryStorage c;
c.occupied=occupied;c.highest=highest;c.data=data;c.maxSize=maxSize;return c;
};
struct _global_StructType _global_TemporaryStorageType;struct _global_StructType* _global_TemporaryStorage_get_type(struct _global_TemporaryStorage* self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_StructType* _global_TemporaryStorage_get_typeByValue(struct _global_TemporaryStorage self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc f;
return f;
};
struct _global_StructType _global_MallocType;struct _global_StructType* _global_Malloc_get_type(struct _global_Malloc* self, struct _global_Context* c){return &_global_MallocType;}
struct _global_StructType* _global_Malloc_get_typeByValue(struct _global_Malloc self, struct _global_Context* c){return &_global_MallocType;}
struct _global_All {
struct _global_All_VTABLE* vtable;
void* data;
};struct _global_All_VTABLE {struct _global_Type type;};static inline struct _global_All _global_AllFromStruct(void* data, struct _global_All_VTABLE* vtable, struct _global_Type typ){ 
struct _global_All j;
j.data = data;j.vtable = vtable;j.vtable->type = typ;
return j; 
}struct _global_Type _global_All_get_type(struct _global_All* j, struct _global_Context* context){ return j->vtable->type; }struct _global_Type _global_All_get_typeByValue(struct _global_All j, struct _global_Context* context){ return j.vtable->type; }
struct _global_InterfaceType _global_All_Type;struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
struct _global_All* data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,struct _global_All* data){
struct _global_Array_Array_T k;
k.length=length;k.capacity=capacity;k.allocator=allocator;k.data=data;return k;
};
struct _global_ArrayType _global_Array_Array_TType;struct _global_ArrayType* _global_Array_Array_T_get_type(struct _global_Array_Array_T* self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType* _global_Array_Array_T_get_typeByValue(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType _global_Array_Array_TType;struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range l;
l.start=start;l.end=end;return l;
};
struct _global_StructType _global_RangeType;struct _global_StructType* _global_Range_get_type(struct _global_Range* self, struct _global_Context* c){return &_global_RangeType;}
struct _global_StructType* _global_Range_get_typeByValue(struct _global_Range self, struct _global_Context* c){return &_global_RangeType;}
struct _global_Maybe_uint_Some {
unsigned int field0;

};union _global_Maybe_uint_cases {
struct _global_Maybe_uint_Some Some;

};
struct _global_Maybe_uint {
 _Bool tag;
union _global_Maybe_uint_cases cases;

};
struct _global_Maybe_uint _global_Some_uint(unsigned int n,struct _global_Context* p){
struct _global_Maybe_uint q;
q.cases.Some.field0 = n;q.tag = 0;
return q;}
struct _global_StructType _global_Maybe_uintType;struct _global_StructType* _global_Maybe_uint_get_type(struct _global_Maybe_uint* self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_StructType* _global_Maybe_uint_get_typeByValue(struct _global_Maybe_uint self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator r;
r.range=range;r.it=it;return r;
};
struct _global_StructType _global_RangeIteratorType;struct _global_StructType* _global_RangeIterator_get_type(struct _global_RangeIterator* self, struct _global_Context* c){return &_global_RangeIteratorType;}
struct _global_StructType* _global_RangeIterator_get_typeByValue(struct _global_RangeIterator self, struct _global_Context* c){return &_global_RangeIteratorType;}
union _global_FileAcess_cases {

};
struct _global_FileAcess {
 _Bool tag;
union _global_FileAcess_cases cases;

};
struct _global_FileAcess _global_ReadFile;
struct _global_FileAcess _global_WriteFile;
struct _global_StructType _global_FileAcessType;struct _global_StructType* _global_FileAcess_get_type(struct _global_FileAcess* self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_StructType* _global_FileAcess_get_typeByValue(struct _global_FileAcess self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_File {
struct FILE* c_file;
struct _global_FileAcess acess;
};
static inline struct _global_File _global_FileInit(struct FILE* c_file,struct _global_FileAcess acess){
struct _global_File t;
t.c_file=c_file;t.acess=acess;return t;
};
struct _global_StructType _global_FileType;struct _global_StructType* _global_File_get_type(struct _global_File* self, struct _global_Context* c){return &_global_FileType;}
struct _global_StructType* _global_File_get_typeByValue(struct _global_File self, struct _global_Context* c){return &_global_FileType;}
struct _global_Maybe_File_Some {
struct _global_File field0;

};union _global_Maybe_File_cases {
struct _global_Maybe_File_Some Some;

};
struct _global_Maybe_File {
 _Bool tag;
union _global_Maybe_File_cases cases;

};
struct _global_Maybe_File _global_Some_File(struct _global_File w,struct _global_Context* x){
struct _global_Maybe_File y;
y.cases.Some.field0 = w;y.tag = 0;
return y;}
struct _global_StructType _global_Maybe_FileType;struct _global_StructType* _global_Maybe_File_get_type(struct _global_Maybe_File* self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_StructType* _global_Maybe_File_get_typeByValue(struct _global_Maybe_File self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_Maybe_Maybe_T_Some {
struct _global_All field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct _global_All z,struct _global_Context* B){
struct _global_Maybe_Maybe_T C;
C.cases.Some.field0 = z;C.tag = 0;
return C;}
struct _global_Maybe_Maybe_T _global_None;
struct _global_StructType _global_Maybe_Maybe_TType;struct _global_StructType* _global_Maybe_Maybe_T_get_type(struct _global_Maybe_Maybe_T* self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_StructType* _global_Maybe_Maybe_T_get_typeByValue(struct _global_Maybe_Maybe_T self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}

void _global_panic(struct _global_String _global_s, struct _global_Context* b);
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c);
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* d);
unsigned int _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* f);
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* g);
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* h);
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* j);
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* k);
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* l);
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* m);
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, unsigned int _global_to, struct _global_Context* n);
void* _global_alloc(unsigned int _global_size, struct _global_Context* p);
void _global_free(void* _global_p, struct _global_Context* q);
struct _global_Array_Array_T _global_empty_array(struct _global_Context* r);
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* s);

static inline void _global_Range_iterator(struct _global_Range*,struct _global_Context* s);

void _global_Range_iteratorByValue(struct _global_Range,struct _global_Context* s);
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* t);
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* v);

static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess*,struct _global_Context* v);

struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess,struct _global_Context* v);
struct _global_String _global_File_readByValue(struct _global_File _global_self, struct _global_Context* w);

static inline struct _global_String _global_File_read(struct _global_File*,struct _global_Context* w);

struct _global_String _global_File_readByValue(struct _global_File,struct _global_Context* w);
void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* x);

static inline void _global_File_free(struct _global_File*,struct _global_Context* x);

void _global_File_freeByValue(struct _global_File,struct _global_Context* x);
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* y);
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* z);

struct _global_String _global_IntType_toString(struct IntType*,struct _global_Context* z);
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* B);

struct _global_String _global_FloatType_toString(struct FloatType*,struct _global_Context* B);
struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* C);

struct _global_String _global_BoolType_toString(struct BoolType*,struct _global_Context* C);
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* D);

struct _global_String _global_StringType_toString(struct StringType*,struct _global_Context* D);
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* F);

struct _global_String _global_AliasType_toString(struct _global_AliasType*,struct _global_Context* F);
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* G);

struct _global_String _global_PointerType_toString(struct _global_PointerType*,struct _global_Context* G);
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* H);

struct _global_String _global_StructType_toString(struct _global_StructType*,struct _global_Context* H);
struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* J);

struct _global_String _global_EnumType_toString(struct _global_EnumType*,struct _global_Context* J);
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* K);

struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType*,struct _global_Context* K);
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* L);

struct _global_String _global_ArrayType_toString(struct _global_ArrayType*,struct _global_Context* L);
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* M);

struct _global_String _global_NoneType_toString(struct NoneType*,struct _global_Context* M);




void _global_log_string(struct _global_String _global_s, struct _global_Context* N);

#define _global_exit(N,P) exit(N)
void _global_panic(struct _global_String _global_s, struct _global_Context* Q){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),Q),_global_StringInit(0,""),Q),Q);
_global_exit(1,Q);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* Q){;
;
if(!(_global_b)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),Q),_global_StringInit(0,""),Q),Q);
;};
;}

#define _global_c_log(Q,R) _global_c_log(Q)

#define _global_memcpy(S,T,V,W) memcpy(S,T,V)

#define _global_c_alloc(X,Y) malloc(X)

#define _global_c_free(Z,bb) free(Z)
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* bc){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,bc),_global_maxSize);
;}
unsigned int _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* bc){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* bc){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){;
(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_log_string(_global_StringInit(48,"panic: used more temporary memory than available"),bc);
_global_exit(1,bc);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,bc);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* bc){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* bc){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_panic(_global_StringInit(41,"used more temporary memory than available"),bc);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* bc){;
;
;return _global_c_alloc(_global_size,bc);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* bc){;
;
_global_c_free(_global_pointer,bc);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* bc){;
;return 0;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, unsigned int _global_to, struct _global_Context* bc){;
;
;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator_VTABLE rTemporaryStorage_VTABLE_FOR_Allocator;struct _global_Allocator _global_malloc_as_allocator;struct _global_Allocator_VTABLE rMalloc_VTABLE_FOR_Allocator;void* _global_alloc(unsigned int _global_size, struct _global_Context* bc){;
;return _global_Allocator_alloc((bc)->allocator,_global_size,bc);
;}
void _global_free(void* _global_p, struct _global_Context* bc){;
_global_Allocator_dealloc((bc)->allocator,_global_p,bc);
;}

#define _global_char_buffer_toString(bc,bd) _runtime_char_buffer_toString(bc)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* bf){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* bf){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* bg,struct _global_Context* bf){
_global_Range_iteratorByValue(*bg,bf);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T bh) {
struct _global_Maybe_uint bg;bg.tag = bh.tag;bg.cases = *(union _global_Maybe_uint_cases*) &(bh.cases);return bg;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* bf){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){;
unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,bf);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* bf){;
;struct _global_FileAcess bg =_global_self;
if(bg.tag==0){return _global_StringInit(1,"r");}if(bg.tag==1){return _global_StringInit(1,"w");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* bh,struct _global_Context* bf){
return _global_FileAcess_toStringByValue(*bh,bf);
}
#define _global_c_open_file(bf,bg,bh) _runtime_c_open_file(bf,bg)

#define _global_c_close_file(bj,bk) _runtime_c_close_file(bj)

#define _global_c_read_file(bl,bm,bn) _runtime_read_file(bl,bm)
struct _global_String _global_File_readByValue(struct _global_File _global_self, struct _global_Context* bp){;
;struct _global_FileAcess bq =(_global_self).acess;
if(bq.tag==0){return _global_c_read_file((_global_self).c_file,bp,bp);}if(1){_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bp);
return _global_StringInit(0,"");};
;}
static inline struct _global_String _global_File_read(struct _global_File* br,struct _global_Context* bp){
return _global_File_readByValue(*br,bp);
}void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bp){;
_global_c_close_file((_global_self).c_file,bp);
;}
static inline void _global_File_free(struct _global_File* bq,struct _global_Context* bp){
_global_File_freeByValue(*bq,bp);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bs) {
struct _global_Maybe_File br;br.tag = bs.tag;br.cases = *(union _global_Maybe_File_cases*) &(bs.cases);return br;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bp){;
;
struct FILE* _global_c_file;_global_c_file = _global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bp),bp);;
;struct FILE* bq =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bp),bp);
if(bq != NULL){struct FILE* _global_file= bq;
return _global_Some_File(_global_FileInit(_global_file,_global_acess),bp);}if(bq == NULL){return tmp_globalc(_global_None);};
;}

#define _global_set_bit_to(bp,bq,br,bs) _global_c_set_bit_to(bp,bq,br)

#define _global_is_bit_set(bt,bv,bw) _global_c_is_bit_set(bt,bv)
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* bx){;
;return ((_global_self)->sign ? _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"i"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx):(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"u"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx)));
;}
static inline struct _global_String _global_IntType_toStringByValue(struct IntType by,struct _global_Context* bx){
return _global_IntType_toString(&by,bx);
}struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"f"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_FloatType_toStringByValue(struct FloatType by,struct _global_Context* bx){
return _global_FloatType_toString(&by,bx);
}struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(4,"bool");
;}
static inline struct _global_String _global_BoolType_toStringByValue(struct BoolType by,struct _global_Context* bx){
return _global_BoolType_toString(&by,bx);
}struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(6,"string");
;}
static inline struct _global_String _global_StringType_toStringByValue(struct StringType by,struct _global_Context* bx){
return _global_StringType_toString(&by,bx);
}struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_AliasType_toStringByValue(struct _global_AliasType by,struct _global_Context* bx){
return _global_AliasType_toString(&by,bx);
}struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"&"),_global_Type_toStringByValue(((_global_self)->p_type),bx),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_PointerType_toStringByValue(struct _global_PointerType by,struct _global_Context* bx){
return _global_PointerType_toString(&by,bx);
}struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* bx){;
;return (_global_String_op_eqByValue((_global_self)->package,_global_StringInit(7,"_global"),bx) ? (_global_self)->name:(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx)));
;}
static inline struct _global_String _global_StructType_toStringByValue(struct _global_StructType by,struct _global_Context* bx){
return _global_StructType_toString(&by,bx);
}struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_EnumType_toStringByValue(struct _global_EnumType by,struct _global_Context* bx){
return _global_EnumType_toString(&by,bx);
}struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_InterfaceType_toStringByValue(struct _global_InterfaceType by,struct _global_Context* bx){
return _global_InterfaceType_toString(&by,bx);
}struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* bx){;
;struct _global_ArraySize by =(_global_self)->size;
if(by.tag==0){unsigned int _global_length = by.cases.Static.field0;
return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"["),_global_uint_toStringByValue((_global_length),bx),bx),_global_StringInit(1,"]"),bx),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);}if(by.tag==1){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(4,"[..]"),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);}if(by.tag==2){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[]"),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);};
;}
static inline struct _global_String _global_ArrayType_toStringByValue(struct _global_ArrayType bz,struct _global_Context* bx){
return _global_ArrayType_toString(&bz,bx);
}struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(4,"none");
;}
static inline struct _global_String _global_NoneType_toStringByValue(struct NoneType by,struct _global_Context* bx){
return _global_NoneType_toString(&by,bx);
}void _global_log_string(struct _global_String _global_s, struct _global_Context* bx){;
_global_c_log(_global_String_toString(&(_global_s),bx),bx);
;}

void _globalInit() { 
struct _global_Field d[4];
_global_TemporaryStorageType.fields = _global_StaticArray_StaticArray_S_FieldInit(
d
,4
);
_global_TemporaryStorageType.package = _global_StringInit(7, "_global");
_global_TemporaryStorageType.name = _global_StringInit(16, "TemporaryStorage");
d[0].name = _global_StringInit(8, "occupied");
d[0].offset = offsetof(struct _global_TemporaryStorage, occupied);
d[0].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;
d[1].name = _global_StringInit(7, "highest");
d[1].offset = offsetof(struct _global_TemporaryStorage, highest);
d[1].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;
d[2].name = _global_StringInit(4, "data");
d[2].offset = offsetof(struct _global_TemporaryStorage, data);
d[2].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
)
;
d[3].name = _global_StringInit(7, "maxSize");
d[3].offset = offsetof(struct _global_TemporaryStorage, maxSize);
d[3].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;struct _global_Field g[0];
_global_MallocType.fields = _global_StaticArray_StaticArray_S_FieldInit(
g
,0
);
_global_MallocType.package = _global_StringInit(7, "_global");
_global_MallocType.name = _global_StringInit(6, "Malloc");_global_All_Type.name = _global_StringInit(3, "All")
;_global_All_Type.package = _global_StringInit(7, "_global");_global_Array_Array_TType.size.tag = 1;
_global_Array_Array_TType.array_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
)
;struct _global_Field m[2];
_global_RangeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
m
,2
);
_global_RangeType.package = _global_StringInit(7, "_global");
_global_RangeType.name = _global_StringInit(5, "Range");
m[0].name = _global_StringInit(5, "start");
m[0].offset = offsetof(struct _global_Range, start);
m[0].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;
m[1].name = _global_StringInit(3, "end");
m[1].offset = offsetof(struct _global_Range, end);
m[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;_global_Maybe_uintType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_uintType.package = _global_StringInit(7, "_global");
_global_Maybe_uintType.name = _global_StringInit(10, "Maybe_uint");struct _global_Field s[2];
_global_RangeIteratorType.fields = _global_StaticArray_StaticArray_S_FieldInit(
s
,2
);
_global_RangeIteratorType.package = _global_StringInit(7, "_global");
_global_RangeIteratorType.name = _global_StringInit(13, "RangeIterator");
s[0].name = _global_StringInit(5, "range");
s[0].offset = offsetof(struct _global_RangeIterator, range);
s[0].field_type = 
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
;
s[1].name = _global_StringInit(2, "it");
s[1].offset = offsetof(struct _global_RangeIterator, it);
s[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;
_global_FileAcessType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_FileAcessType.package = _global_StringInit(7, "_global");
_global_FileAcessType.name = _global_StringInit(9, "FileAcess");struct _global_Field v[2];
_global_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(
v
,2
);
_global_FileType.package = _global_StringInit(7, "_global");
_global_FileType.name = _global_StringInit(4, "File");
v[0].name = _global_StringInit(6, "c_file");
v[0].offset = offsetof(struct _global_File, c_file);
v[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
)
;
v[1].name = _global_StringInit(5, "acess");
v[1].offset = offsetof(struct _global_File, acess);
v[1].field_type = 
_global_TypeFromStruct(
NULL
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
)
;_global_Maybe_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_FileType.package = _global_StringInit(7, "_global");
_global_Maybe_FileType.name = _global_StringInit(10, "Maybe_File");_global_None.tag = 1;
_global_Maybe_Maybe_TType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_Maybe_TType.package = _global_StringInit(7, "_global");
_global_Maybe_Maybe_TType.name = _global_StringInit(13, "Maybe_Maybe_T");
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(100000,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&(_global_temporary_storage),&rTemporaryStorage_VTABLE_FOR_Allocator,_global_TypeFromStruct(NULL,&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString), &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&(_global_malloc),&rMalloc_VTABLE_FOR_Allocator,_global_TypeFromStruct(NULL,&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString), &_global_Malloc_get_occupied, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_reset_to);;
(&_global_context)->allocator = &(_global_temporary_storage_as_allocator);
(&_global_context)->longterm_storage = &(_global_malloc_as_allocator);
;
;
;
;
;
;
;
};

void mainInit() { 

_globalInit();;
;
};
int main() { 
_globalInit(); _global_init_c_runtime(); 
 _global_Type_Type.name = _global_StringInit(4, "Type")
;_global_Type_Type.package = _global_StringInit(7, "_global");_global_StaticArray_StaticArray_S_FieldType.size.tag = 2;
_global_StaticArray_StaticArray_S_FieldType.array_type = 
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
;struct _global_Field k[4];
_global_StructTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
k
,4
);
_global_StructTypeType.package = _global_StringInit(7, "_global");
_global_StructTypeType.name = _global_StringInit(10, "StructType");
k[0].name = _global_StringInit(4, "name");
k[0].offset = offsetof(struct _global_StructType, name);
k[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_StructType_toString
)
, &_global_StringType_toString
)
;
k[1].name = _global_StringInit(7, "package");
k[1].offset = offsetof(struct _global_StructType, package);
k[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
k[2].name = _global_StringInit(9, "real_type");
k[2].offset = offsetof(struct _global_StructType, real_type);
k[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_InterfaceType_toString
)
;
k[3].name = _global_StringInit(6, "fields");
k[3].offset = offsetof(struct _global_StructType, fields);
k[3].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Field_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_ArrayType_toString
)
;struct _global_Field F[4];
_global_InterfaceTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
F
,4
);
_global_InterfaceTypeType.package = _global_StringInit(7, "_global");
_global_InterfaceTypeType.name = _global_StringInit(13, "InterfaceType");
F[0].name = _global_StringInit(4, "name");
F[0].offset = offsetof(struct _global_InterfaceType, name);
F[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
F[1].name = _global_StringInit(7, "package");
F[1].offset = offsetof(struct _global_InterfaceType, package);
F[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
F[2].name = _global_StringInit(6, "fields");
F[2].offset = offsetof(struct _global_InterfaceType, fields);
F[2].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Field_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;
F[3].name = _global_StringInit(7, "methods");
F[3].offset = offsetof(struct _global_InterfaceType, methods);
F[3].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Method_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
)
;_global_Dynamic.tag = 1;
_global_Both.tag = 2;
_global_ArraySizeType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_ArraySizeType.package = _global_StringInit(7, "_global");
_global_ArraySizeType.name = _global_StringInit(9, "ArraySize");struct _global_Field q[2];
_global_ArrayTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
q
,2
);
_global_ArrayTypeType.package = _global_StringInit(7, "_global");
_global_ArrayTypeType.name = _global_StringInit(9, "ArrayType");
q[0].name = _global_StringInit(4, "size");
q[0].offset = offsetof(struct _global_ArrayType, size);
q[0].field_type = 
_global_TypeFromStruct(
NULL
,
&rEnumType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_EnumType_toString
)
;
q[1].name = _global_StringInit(10, "array_type");
q[1].offset = offsetof(struct _global_ArrayType, array_type);
q[1].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
)
;_global_StaticArray_StaticArray_S_TypeType.size.tag = 2;
_global_StaticArray_StaticArray_S_TypeType.array_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
)
;struct _global_Field t[2];
_global_CasesType.fields = _global_StaticArray_StaticArray_S_FieldInit(
t
,2
);
_global_CasesType.package = _global_StringInit(7, "_global");
_global_CasesType.name = _global_StringInit(5, "Cases");
t[0].name = _global_StringInit(4, "name");
t[0].offset = offsetof(struct _global_Cases, name);
t[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
t[1].name = _global_StringInit(4, "args");
t[1].offset = offsetof(struct _global_Cases, args);
t[1].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Type_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;_global_StaticArray_StaticArray_S_CasesType.size.tag = 2;
_global_StaticArray_StaticArray_S_CasesType.array_type = 
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
;struct _global_Field H[1];
_global_PointerTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
H
,1
);
_global_PointerTypeType.package = _global_StringInit(7, "_global");
_global_PointerTypeType.name = _global_StringInit(11, "PointerType");
H[0].name = _global_StringInit(6, "p_type");
H[0].offset = offsetof(struct _global_PointerType, p_type);
H[0].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
)
;struct _global_Field x[2];
_global_MethodType.fields = _global_StaticArray_StaticArray_S_FieldInit(
x
,2
);
_global_MethodType.package = _global_StringInit(7, "_global");
_global_MethodType.name = _global_StringInit(6, "Method");
x[0].name = _global_StringInit(4, "name");
x[0].offset = offsetof(struct _global_Method, name);
x[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
x[1].name = _global_StringInit(17, "pointer_to_method");
x[1].offset = offsetof(struct _global_Method, pointer_to_method);
x[1].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_NoneType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_PointerType_toString
)
;struct _global_Field B[4];
_global_EnumTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
B
,4
);
_global_EnumTypeType.package = _global_StringInit(7, "_global");
_global_EnumTypeType.name = _global_StringInit(8, "EnumType");
B[0].name = _global_StringInit(4, "name");
B[0].offset = offsetof(struct _global_EnumType, name);
B[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
B[1].name = _global_StringInit(7, "package");
B[1].offset = offsetof(struct _global_EnumType, package);
B[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
B[2].name = _global_StringInit(5, "cases");
B[2].offset = offsetof(struct _global_EnumType, cases);
B[2].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Cases_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;
B[3].name = _global_StringInit(7, "methods");
B[3].offset = offsetof(struct _global_EnumType, methods);
B[3].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Method_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;struct _global_Field h[3];
_global_FieldType.fields = _global_StaticArray_StaticArray_S_FieldInit(
h
,3
);
_global_FieldType.package = _global_StringInit(7, "_global");
_global_FieldType.name = _global_StringInit(5, "Field");
h[0].name = _global_StringInit(4, "name");
h[0].offset = offsetof(struct _global_Field, name);
h[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
h[1].name = _global_StringInit(6, "offset");
h[1].offset = offsetof(struct _global_Field, offset);
h[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_IntType_toString
)
;
h[2].name = _global_StringInit(10, "field_type");
h[2].offset = offsetof(struct _global_Field, field_type);
h[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
)
;struct _global_Field L[3];
_global_AliasTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
L
,3
);
_global_AliasTypeType.package = _global_StringInit(7, "_global");
_global_AliasTypeType.name = _global_StringInit(9, "AliasType");
L[0].name = _global_StringInit(4, "name");
L[0].offset = offsetof(struct _global_AliasType, name);
L[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
L[1].name = _global_StringInit(7, "package");
L[1].offset = offsetof(struct _global_AliasType, package);
L[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
)
;
L[2].name = _global_StringInit(9, "real_type");
L[2].offset = offsetof(struct _global_AliasType, real_type);
L[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
)
;_global_SizeT_Type.name = _global_StringInit(5, "SizeT");
_global_SizeT_Type.package = _global_StringInit(7, "_global");
_global_SizeT_Type.real_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
, &_global_AliasType_toString
)
;_global_Allocator_Type.name = _global_StringInit(9, "Allocator")
;_global_Allocator_Type.package = _global_StringInit(7, "_global");; 
 mainInit(); return 0; };