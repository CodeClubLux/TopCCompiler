#include <string.h>

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

struct BoolType {};
struct StringType {};
struct NoneType {};
struct CharType {};

struct IntType {
    _Bool sign;
    unsigned int size;
};

struct FloatType {
    unsigned int size;
};
struct _global_Type {
struct _global_Type_VTABLE* vtable;
void* data;
};struct _global_Type_VTABLE {struct _global_Type type;struct _global_String(*method_toString)(void*,struct _global_Context*);
uint64_t(*method_get_size)(void*,struct _global_Context*);
};static inline struct _global_Type _global_TypeFromStruct(void* data, struct _global_Type_VTABLE* vtable, struct _global_Type typ, struct _global_String(*c)(void*,struct _global_Context*), uint64_t(*d)(void*,struct _global_Context*)){ 
struct _global_Type f;
f.data = data;f.vtable = vtable;f.vtable->method_toString = c;
f.vtable->method_get_size = d;
f.vtable->type = typ;
return f; 
}void* _global_Type_get_pointer_to_data(struct _global_Type* self, struct _global_Context* context) { return self->data; }static inline struct _global_String _global_Type_toString(struct _global_Type* f,struct _global_Context* b){
return f->vtable->method_toString(f->data,b);
};static inline struct _global_String _global_Type_toStringByValue(struct _global_Type f,struct _global_Context* b){
return f.vtable->method_toString(f.data,b);
};static inline uint64_t _global_Type_get_size(struct _global_Type* f,struct _global_Context* b){
return f->vtable->method_get_size(f->data,b);
};static inline uint64_t _global_Type_get_sizeByValue(struct _global_Type f,struct _global_Context* b){
return f.vtable->method_get_size(f.data,b);
};struct _global_Type _global_Type_get_type(struct _global_Type* f, struct _global_Context* context){ return f->vtable->type; }struct _global_Type _global_Type_get_typeByValue(struct _global_Type f, struct _global_Context* context){ return f.vtable->type; }
struct _global_InterfaceType _global_Type_Type;struct _global_StaticArray_StaticArray_S_Field {
struct _global_Field* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Field _global_StaticArray_StaticArray_S_FieldInit(struct _global_Field* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Field B;
B.data=data;B.length=length;return B;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_FieldType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Field_get_type(struct _global_StaticArray_StaticArray_S_Field* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Field_get_typeByValue(struct _global_StaticArray_StaticArray_S_Field self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_FieldType;struct _global_StructType {
struct _global_String name;
struct _global_String package;
struct _global_Type real_type;
struct _global_StaticArray_StaticArray_S_Field fields;
uint64_t size;
};
static inline struct _global_StructType _global_StructTypeInit(struct _global_String name,struct _global_String package,struct _global_Type real_type,struct _global_StaticArray_StaticArray_S_Field fields,uint64_t size){
struct _global_StructType k;
k.name=name;k.package=package;k.real_type=real_type;k.fields=fields;k.size=size;return k;
};
struct _global_StructType _global_StructTypeType;struct _global_StructType* _global_StructType_get_type(struct _global_StructType* self, struct _global_Context* c){return &_global_StructTypeType;}
struct _global_Field* _global_StructTypeType_fields;
struct _global_Type_VTABLE rStringType_VTABLE_FOR_Type;struct _global_Type_VTABLE rStructType_VTABLE_FOR_Type;struct _global_Type_VTABLE rInterfaceType_VTABLE_FOR_Type;struct _global_Type_VTABLE rArrayType_VTABLE_FOR_Type;struct _global_StructType _global_StringTypeType;struct _global_StructType* _global_StringType_get_type(struct StringType* self, struct _global_Context* c){return &_global_StringTypeType;}
struct _global_Field* _global_StringTypeType_fields;
struct _global_InterfaceType {
struct _global_String name;
struct _global_String package;
struct _global_StaticArray_StaticArray_S_Field fields;
struct _global_StaticArray_StaticArray_S_Method* methods;
};
static inline struct _global_InterfaceType _global_InterfaceTypeInit(struct _global_String name,struct _global_String package,struct _global_StaticArray_StaticArray_S_Field fields,struct _global_StaticArray_StaticArray_S_Method* methods){
struct _global_InterfaceType C;
C.name=name;C.package=package;C.fields=fields;C.methods=methods;return C;
};
struct _global_StructType _global_InterfaceTypeType;struct _global_StructType* _global_InterfaceType_get_type(struct _global_InterfaceType* self, struct _global_Context* c){return &_global_InterfaceTypeType;}
struct _global_Field* _global_InterfaceTypeType_fields;
struct _global_StaticArray_StaticArray_S_Case {
struct _global_Case* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Case _global_StaticArray_StaticArray_S_CaseInit(struct _global_Case* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Case p;
p.data=data;p.length=length;return p;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_CaseType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Case_get_type(struct _global_StaticArray_StaticArray_S_Case* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CaseType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Case_get_typeByValue(struct _global_StaticArray_StaticArray_S_Case self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CaseType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_CaseType;struct _global_StaticArray_StaticArray_S_CaseArg {
struct _global_CaseArg* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_CaseArg _global_StaticArray_StaticArray_S_CaseArgInit(struct _global_CaseArg* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_CaseArg m;
m.data=data;m.length=length;return m;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_CaseArgType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_CaseArg_get_type(struct _global_StaticArray_StaticArray_S_CaseArg* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CaseArgType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_CaseArg_get_typeByValue(struct _global_StaticArray_StaticArray_S_CaseArg self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_CaseArgType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_CaseArgType;struct _global_StructType _global_IntTypeType;struct _global_StructType* _global_IntType_get_type(struct IntType* self, struct _global_Context* c){return &_global_IntTypeType;}
struct _global_Field* _global_IntTypeType_fields;
struct _global_CaseArg {
struct _global_Type arg_type;
unsigned int offset;
};
static inline struct _global_CaseArg _global_CaseArgInit(struct _global_Type arg_type,unsigned int offset){
struct _global_CaseArg l;
l.arg_type=arg_type;l.offset=offset;return l;
};
struct _global_StructType _global_CaseArgType;struct _global_StructType* _global_CaseArg_get_type(struct _global_CaseArg* self, struct _global_Context* c){return &_global_CaseArgType;}
struct _global_Field* _global_CaseArgType_fields;
struct _global_Type_VTABLE rIntType_VTABLE_FOR_Type;struct _global_ArrayType {
struct _global_ArraySize* size;
struct _global_Type array_type;
};
static inline struct _global_ArrayType _global_ArrayTypeInit(struct _global_ArraySize* size,struct _global_Type array_type){
struct _global_ArrayType z;
z.size=size;z.array_type=array_type;return z;
};
struct _global_StructType _global_ArrayTypeType;struct _global_StructType* _global_ArrayType_get_type(struct _global_ArrayType* self, struct _global_Context* c){return &_global_ArrayTypeType;}
struct _global_Field* _global_ArrayTypeType_fields;
struct _global_Type_VTABLE rEnumType_VTABLE_FOR_Type;struct _global_Case {
struct _global_String name;
struct _global_StaticArray_StaticArray_S_CaseArg args;
};
static inline struct _global_Case _global_CaseInit(struct _global_String name,struct _global_StaticArray_StaticArray_S_CaseArg args){
struct _global_Case n;
n.name=name;n.args=args;return n;
};
struct _global_StructType _global_CaseType;struct _global_StructType* _global_Case_get_type(struct _global_Case* self, struct _global_Context* c){return &_global_CaseType;}
struct _global_Field* _global_CaseType_fields;
struct _global_StaticArray_StaticArray_S_Method {
struct _global_Method* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Method _global_StaticArray_StaticArray_S_MethodInit(struct _global_Method* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Method r;
r.data=data;r.length=length;return r;
};
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Method_get_type(struct _global_StaticArray_StaticArray_S_Method* self, struct _global_Context* c){return NULL;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Method_get_typeByValue(struct _global_StaticArray_StaticArray_S_Method self, struct _global_Context* c){return NULL;}
struct _global_StructType _global_NoneTypeType;struct _global_StructType* _global_NoneType_get_type(struct NoneType* self, struct _global_Context* c){return &_global_NoneTypeType;}
struct _global_Field* _global_NoneTypeType_fields;
struct _global_PointerType {
struct _global_Type p_type;
_Bool nullable;
};
static inline struct _global_PointerType _global_PointerTypeInit(struct _global_Type p_type,_Bool nullable){
struct _global_PointerType D;
D.p_type=p_type;D.nullable=nullable;return D;
};
struct _global_StructType _global_PointerTypeType;struct _global_StructType* _global_PointerType_get_type(struct _global_PointerType* self, struct _global_Context* c){return &_global_PointerTypeType;}
struct _global_Field* _global_PointerTypeType_fields;
struct _global_Type_VTABLE rBoolType_VTABLE_FOR_Type;struct _global_Method {
struct _global_String name;
void* pointer_to_method;
};
static inline struct _global_Method _global_MethodInit(struct _global_String name,void* pointer_to_method){
struct _global_Method q;
q.name=name;q.pointer_to_method=pointer_to_method;return q;
};
struct _global_StructType _global_MethodType;struct _global_StructType* _global_Method_get_type(struct _global_Method* self, struct _global_Context* c){return &_global_MethodType;}
struct _global_Field* _global_MethodType_fields;
struct _global_Type_VTABLE rPointerType_VTABLE_FOR_Type;struct _global_Type_VTABLE rNoneType_VTABLE_FOR_Type;struct _global_Field {
struct _global_String name;
unsigned int offset;
struct _global_Type field_type;
};
static inline struct _global_Field _global_FieldInit(struct _global_String name,unsigned int offset,struct _global_Type field_type){
struct _global_Field j;
j.name=name;j.offset=offset;j.field_type=field_type;return j;
};
struct _global_StructType _global_FieldType;struct _global_StructType* _global_Field_get_type(struct _global_Field* self, struct _global_Context* c){return &_global_FieldType;}
struct _global_Field* _global_FieldType_fields;
struct _global_EnumType {
struct _global_String name;
struct _global_String package;
struct _global_StaticArray_StaticArray_S_Case cases;
struct _global_StaticArray_StaticArray_S_Method methods;
struct _global_Field tag_field;
uint64_t size;
};
static inline struct _global_EnumType _global_EnumTypeInit(struct _global_String name,struct _global_String package,struct _global_StaticArray_StaticArray_S_Case cases,struct _global_StaticArray_StaticArray_S_Method methods,struct _global_Field tag_field,uint64_t size){
struct _global_EnumType s;
s.name=name;s.package=package;s.cases=cases;s.methods=methods;s.tag_field=tag_field;s.size=size;return s;
};
struct _global_StructType _global_EnumTypeType;struct _global_StructType* _global_EnumType_get_type(struct _global_EnumType* self, struct _global_Context* c){return &_global_EnumTypeType;}
struct _global_Field* _global_EnumTypeType_fields;
struct _global_ArraySize_Static {
unsigned int field0;

};union _global_ArraySize_cases {
struct _global_ArraySize_Static Static;

};
struct _global_ArraySize {
union _global_ArraySize_cases cases;
unsigned char tag;
};
struct _global_ArraySize _global_Static(unsigned int t,struct _global_Context* v){
struct _global_ArraySize w;
w.cases.Static.field0 = t;w.tag = 0;
return w;}
struct _global_ArraySize _global_Dynamic;
struct _global_ArraySize _global_Both;
struct _global_EnumType _global_ArraySizeType;struct _global_EnumType* _global_ArraySize_get_type(struct _global_ArraySize* self, struct _global_Context* c){return &_global_ArraySizeType;}
struct _global_EnumType* _global_ArraySize_get_typeByValue(struct _global_ArraySize self, struct _global_Context* c){return &_global_ArraySizeType;}
struct _global_StructType _global_BoolTypeType;struct _global_StructType* _global_BoolType_get_type(struct BoolType* self, struct _global_Context* c){return &_global_BoolTypeType;}
struct _global_Field* _global_BoolTypeType_fields;
struct _global_AliasType {
struct _global_String name;
struct _global_String package;
struct _global_Type real_type;
};
static inline struct _global_AliasType _global_AliasTypeInit(struct _global_String name,struct _global_String package,struct _global_Type real_type){
struct _global_AliasType G;
G.name=name;G.package=package;G.real_type=real_type;return G;
};
struct _global_StructType _global_AliasTypeType;struct _global_StructType* _global_AliasType_get_type(struct _global_AliasType* self, struct _global_Context* c){return &_global_AliasTypeType;}
struct _global_Field* _global_AliasTypeType_fields;
struct _global_AliasType _global_SizeT_Type;struct _global_Allocator {
struct _global_Allocator_VTABLE* vtable;
void* data;
};struct _global_Allocator_VTABLE {struct _global_Type type;uint64_t(*method_get_occupied)(void*,struct _global_Context*);
void*(*method_alloc)(void*,uint64_t,struct _global_Context*);
void(*method_dealloc)(void*,void*,struct _global_Context*);
void(*method_reset_to)(void*,uint64_t,struct _global_Context*);
void(*method_free_allocator)(void*,struct _global_Context*);
};static inline struct _global_Allocator _global_AllocatorFromStruct(void* data, struct _global_Allocator_VTABLE* vtable, struct _global_Type typ, uint64_t(*H)(void*,struct _global_Context*), void*(*J)(void*,uint64_t,struct _global_Context*), void(*K)(void*,void*,struct _global_Context*), void(*L)(void*,uint64_t,struct _global_Context*), void(*M)(void*,struct _global_Context*)){ 
struct _global_Allocator N;
N.data = data;N.vtable = vtable;N.vtable->method_get_occupied = H;
N.vtable->method_alloc = J;
N.vtable->method_dealloc = K;
N.vtable->method_reset_to = L;
N.vtable->method_free_allocator = M;
N.vtable->type = typ;
return N; 
}void* _global_Allocator_get_pointer_to_data(struct _global_Allocator* self, struct _global_Context* context) { return self->data; }static inline uint64_t _global_Allocator_get_occupied(struct _global_Allocator* N,struct _global_Context* F){
return N->vtable->method_get_occupied(N->data,F);
};static inline uint64_t _global_Allocator_get_occupiedByValue(struct _global_Allocator N,struct _global_Context* F){
return N.vtable->method_get_occupied(N.data,F);
};static inline void* _global_Allocator_alloc(struct _global_Allocator* N,uint64_t Q,struct _global_Context* F){
return N->vtable->method_alloc(N->data,Q,F);
};static inline void* _global_Allocator_allocByValue(struct _global_Allocator N,uint64_t Q,struct _global_Context* F){
return N.vtable->method_alloc(N.data,Q,F);
};static inline void _global_Allocator_dealloc(struct _global_Allocator* N,void* S,struct _global_Context* F){
return N->vtable->method_dealloc(N->data,S,F);
};static inline void _global_Allocator_deallocByValue(struct _global_Allocator N,void* S,struct _global_Context* F){
return N.vtable->method_dealloc(N.data,S,F);
};static inline void _global_Allocator_reset_to(struct _global_Allocator* N,uint64_t V,struct _global_Context* F){
return N->vtable->method_reset_to(N->data,V,F);
};static inline void _global_Allocator_reset_toByValue(struct _global_Allocator N,uint64_t V,struct _global_Context* F){
return N.vtable->method_reset_to(N.data,V,F);
};static inline void _global_Allocator_free_allocator(struct _global_Allocator* N,struct _global_Context* F){
return N->vtable->method_free_allocator(N->data,F);
};static inline void _global_Allocator_free_allocatorByValue(struct _global_Allocator N,struct _global_Context* F){
return N.vtable->method_free_allocator(N.data,F);
};struct _global_Type _global_Allocator_get_type(struct _global_Allocator* N, struct _global_Context* context){ return N->vtable->type; }struct _global_Type _global_Allocator_get_typeByValue(struct _global_Allocator N, struct _global_Context* context){ return N.vtable->type; }
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



#include <stdatomic.h>

void c_runtime_incr_atomic_uint(volatile atomic_uint* a, unsigned int value) {
    *a += value;
}

atomic_flag c_runtime_ATOMIC_FLAG_INIT = ATOMIC_FLAG_INIT;




struct BoolType _global_Bool_typ;

struct BoolType* _global_Bool_get_typeByValue(_Bool b, __Context) {
    return &_global_Bool_typ;
}

struct BoolType* _global_Bool_get_type(_Bool* b, __Context) {
    return &_global_Bool_typ;
}

struct CharType _global_Char_typ;

struct CharType* _global_char_get_typeByValue(char b, __Context) {
    return &_global_Char_typ;
}

struct CharType* _global_char_get_type(char* b, __Context) {
    return &_global_Char_typ;
}

struct _global_String _global_CharType_toString(struct CharType* self, __Context) {
    return _global_StringInit(4, "char");
}

struct _global_String _global_Bool_toString(_Bool* b, __Context) {
    return _global_Bool_toStringByValue(*b, context);
}


struct _global_String _global_String_sliceByValue(struct _global_String s, unsigned int from, unsigned int end, __Context) {
    int length = end - from;
    char* buffer = alloc(context->allocator, sizeof(char) * length + 1, context);
    memcpy(buffer, s.data + from, length);
    buffer[length] = '\0';
    return _global_StringInit(length, buffer);
}

char* _global_String_op_getByValue(struct _global_String s, unsigned int i, __Context) {
    if (i >= s.length) {
        printf("String acess out of bounds: %i", i);
        exit(1);
    }
    return &s.data[i];
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

_Bool _global_String_op_eq(struct _global_String* s, struct _global_String* other, __Context) {
    return _global_String_op_eqByValue(*s, *other, context);
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

    unsigned int length = strlen(string) - 1;
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

        if (f == NULL && errors) {
            printf("%s\n", filename.data);
            printf("%i\n", (int)f);
            printf("error %i\n", errors);
            return NULL;
        }
    #endif

    return f;
}

#include <sys/stat.h>

struct _global_String _runtime_read_file(FILE* f, struct _global_String filename, __Context) {
    struct stat info[1];

    stat (filename.data, info);
    int length = info->st_size;
    char* buffer = alloc(context->allocator, length + 1, context);

    length = fread(buffer, sizeof(char), sizeof(char) * length, f);
    buffer[length] = '\0';

    return _global_StringInit(length, buffer);
}

void _runtime_write_file(FILE* f, struct _global_String s, __Context) {
    fwrite(s.data, sizeof(char), sizeof(char) * s.length, f);
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

_Bool _global_String_starts_withByValue(struct _global_String str, struct _global_String pre, __Context) {
    if (str.length < pre.length) { return 0; }
    return strncmp(pre.data, str.data, pre.length) == 0;
}

_Bool _global_String_ends_withByValue(struct _global_String str, struct _global_String pre, __Context) {
    if (str.length < pre.length) { return 0; }
    return strncmp(pre.data, str.data + (str.length - pre.length), pre.length) == 0;
}


#define _global_indexPtr(value, by, c) value + by
#define _global_c_set_bit_to(number, n, x) (number & ~(1U << n) | (x << n))
#define _global_c_is_bit_set(number, n) ((number >> n) & 1U)
#define _global_c_bit_and(x,y) x & y

/*
void printI(int i) {
    printf("%i\n", i);
};
*/


struct StringType _global_StringType;

struct StringType* _global_String_get_type(struct _global_String* s, __Context) {
    return &_global_StringType;
}

struct StringType* _global_String_get_typeByValue(struct _global_String s, __Context) {
    return &_global_StringType;
}

struct _global_PointerType pointerTypes[200];
unsigned int pointerTypeCounter;

struct _global_PointerType* _global_boxPointerType(struct _global_PointerType p, __Context) {
    if (pointerTypeCounter > 199) {
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
struct _global_TemporaryStorage {
uint64_t occupied;
uint64_t highest;
void* data;
uint64_t maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(uint64_t occupied,uint64_t highest,void* data,uint64_t maxSize){
struct _global_TemporaryStorage c;
c.occupied=occupied;c.highest=highest;c.data=data;c.maxSize=maxSize;return c;
};
struct _global_StructType _global_TemporaryStorageType;struct _global_StructType* _global_TemporaryStorage_get_type(struct _global_TemporaryStorage* self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_Field* _global_TemporaryStorageType_fields;
struct _global_Type_VTABLE rAliasType_VTABLE_FOR_Type;struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc d;
return d;
};
struct _global_StructType _global_MallocType;struct _global_StructType* _global_Malloc_get_type(struct _global_Malloc* self, struct _global_Context* c){return &_global_MallocType;}
struct _global_Field* _global_MallocType_fields;
struct _global_PointerType _global_Maybe_rAllocatorType;struct _global_PointerType* _global_Maybe_rAllocator_get_type(struct _global_Allocator*** self, struct _global_Context* c){return &_global_Maybe_rAllocatorType;}
struct _global_PointerType* _global_Maybe_rAllocator_get_typeByValue(struct _global_Allocator** self, struct _global_Context* c){return &_global_Maybe_rAllocatorType;}
struct _global_PointerType _global_Maybe_rArray_TType;struct _global_PointerType* _global_Maybe_rArray_T_get_type(void**** self, struct _global_Context* c){return &_global_Maybe_rArray_TType;}
struct _global_PointerType* _global_Maybe_rArray_T_get_typeByValue(void*** self, struct _global_Context* c){return &_global_Maybe_rArray_TType;}
struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
void** data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,void** data){
struct _global_Array_Array_T f;
f.length=length;f.capacity=capacity;f.allocator=allocator;f.data=data;return f;
};
struct _global_ArrayType _global_Array_Array_TType;struct _global_ArrayType* _global_Array_Array_T_get_type(struct _global_Array_Array_T* self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType* _global_Array_Array_T_get_typeByValue(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType _global_Array_Array_TType;struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range g;
g.start=start;g.end=end;return g;
};
struct _global_StructType _global_RangeType;struct _global_StructType* _global_Range_get_type(struct _global_Range* self, struct _global_Context* c){return &_global_RangeType;}
struct _global_Field* _global_RangeType_fields;
struct _global_Maybe_uint_Some {
unsigned int field0;

};union _global_Maybe_uint_cases {
struct _global_Maybe_uint_Some Some;

};
struct _global_Maybe_uint {
union _global_Maybe_uint_cases cases;
unsigned char tag;
};
struct _global_Maybe_uint _global_Some_uint(unsigned int h,struct _global_Context* j){
struct _global_Maybe_uint k;
k.cases.Some.field0 = h;k.tag = 0;
return k;}
struct _global_EnumType _global_Maybe_uintType;struct _global_EnumType* _global_Maybe_uint_get_type(struct _global_Maybe_uint* self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_EnumType* _global_Maybe_uint_get_typeByValue(struct _global_Maybe_uint self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator n;
n.range=range;n.it=it;return n;
};
struct _global_StructType _global_RangeIteratorType;struct _global_StructType* _global_RangeIterator_get_type(struct _global_RangeIterator* self, struct _global_Context* c){return &_global_RangeIteratorType;}
struct _global_Field* _global_RangeIteratorType_fields;
union _global_FileAcess_cases {

};
struct _global_FileAcess {
union _global_FileAcess_cases cases;
unsigned char tag;
};
struct _global_FileAcess _global_ReadFile;
struct _global_FileAcess _global_WriteFile;
struct _global_FileAcess _global_ReadBFile;
struct _global_FileAcess _global_WriteBFile;
struct _global_EnumType _global_FileAcessType;struct _global_EnumType* _global_FileAcess_get_type(struct _global_FileAcess* self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_EnumType* _global_FileAcess_get_typeByValue(struct _global_FileAcess self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_StructType _global_FILEType;struct _global_StructType* _global_FILE_get_type(struct FILE* self, struct _global_Context* c){return &_global_FILEType;}
struct _global_Field* _global_FILEType_fields;
struct _global_File {
struct FILE* c_file;
struct _global_FileAcess acess;
struct _global_String filename;
};
static inline struct _global_File _global_FileInit(struct FILE* c_file,struct _global_FileAcess acess,struct _global_String filename){
struct _global_File r;
r.c_file=c_file;r.acess=acess;r.filename=filename;return r;
};
struct _global_StructType _global_FileType;struct _global_StructType* _global_File_get_type(struct _global_File* self, struct _global_Context* c){return &_global_FileType;}
struct _global_Field* _global_FileType_fields;
struct _global_Maybe_File_Some {
struct _global_File field0;

};union _global_Maybe_File_cases {
struct _global_Maybe_File_Some Some;

};
struct _global_Maybe_File {
union _global_Maybe_File_cases cases;
unsigned char tag;
};
struct _global_Maybe_File _global_Some_File(struct _global_File s,struct _global_Context* t){
struct _global_Maybe_File v;
v.cases.Some.field0 = s;v.tag = 0;
return v;}
struct _global_EnumType _global_Maybe_FileType;struct _global_EnumType* _global_Maybe_File_get_type(struct _global_Maybe_File* self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_EnumType* _global_Maybe_File_get_typeByValue(struct _global_Maybe_File self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_StructType _global_FloatTypeType;struct _global_StructType* _global_FloatType_get_type(struct FloatType* self, struct _global_Context* c){return &_global_FloatTypeType;}
struct _global_Field* _global_FloatTypeType_fields;
struct _global_StaticArray_StaticArray_S_Type {
struct _global_Type* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Type _global_StaticArray_StaticArray_S_TypeInit(struct _global_Type* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Type y;
y.data=data;y.length=length;return y;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_TypeType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_Type_get_type(struct _global_StaticArray_StaticArray_S_Type* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_TypeType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_Type_get_typeByValue(struct _global_StaticArray_StaticArray_S_Type self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_TypeType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_TypeType;struct _global_FuncType {
struct _global_StaticArray_StaticArray_S_Type args;
struct _global_Type return_type;
};
static inline struct _global_FuncType _global_FuncTypeInit(struct _global_StaticArray_StaticArray_S_Type args,struct _global_Type return_type){
struct _global_FuncType z;
z.args=args;z.return_type=return_type;return z;
};
struct _global_StructType _global_FuncTypeType;struct _global_StructType* _global_FuncType_get_type(struct _global_FuncType* self, struct _global_Context* c){return &_global_FuncTypeType;}
struct _global_Field* _global_FuncTypeType_fields;
struct _global_CharType {
};
static inline struct _global_CharType _global_CharTypeInit(){
struct _global_CharType B;
return B;
};
struct _global_StructType _global_CharTypeType;struct _global_StructType* _global_CharType_get_type(struct _global_CharType* self, struct _global_Context* c){return &_global_CharTypeType;}
struct _global_Field* _global_CharTypeType_fields;
struct _global_Maybe_Maybe_T_Some {
void* field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
union _global_Maybe_Maybe_T_cases cases;
unsigned char tag;
};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(void* C,struct _global_Context* D){
struct _global_Maybe_Maybe_T F;
F.cases.Some.field0 = C;F.tag = 0;
return F;}
struct _global_Maybe_Maybe_T _global_None;
struct _global_EnumType _global_Maybe_Maybe_TType;struct _global_EnumType* _global_Maybe_Maybe_T_get_type(struct _global_Maybe_Maybe_T* self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_EnumType* _global_Maybe_Maybe_T_get_typeByValue(struct _global_Maybe_Maybe_T self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_PointerType _global_Maybe_rFILEType;struct _global_PointerType* _global_Maybe_rFILE_get_type(struct FILE*** self, struct _global_Context* c){return &_global_Maybe_rFILEType;}
struct _global_PointerType* _global_Maybe_rFILE_get_typeByValue(struct FILE** self, struct _global_Context* c){return &_global_Maybe_rFILEType;}
typedef void(*pp___none)(struct _global_Context*) ;
struct bb {
struct bb_VTABLE* vtable;
void* data;
};struct bb_VTABLE {struct _global_Type type;};static inline struct bb bbFromStruct(void* data, struct bb_VTABLE* vtable, struct _global_Type typ){ 
struct bb K;
K.data = data;K.vtable = vtable;K.vtable->type = typ;
return K; 
}void* bb_get_pointer_to_data(struct bb* self, struct _global_Context* context) { return self->data; }struct _global_Type bb_get_type(struct bb* K, struct _global_Context* context){ return K->vtable->type; }struct _global_Type bb_get_typeByValue(struct bb K, struct _global_Context* context){ return K.vtable->type; }
struct _global_InterfaceType bb_Type;struct _global_Array_none {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
void* data;
};
static inline struct _global_Array_none _global_Array_noneInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,void* data){
struct _global_Array_none L;
L.length=length;L.capacity=capacity;L.allocator=allocator;L.data=data;return L;
};
struct _global_ArrayType _global_Array_noneType;struct _global_ArrayType* _global_Array_none_get_type(struct _global_Array_none* self, struct _global_Context* c){return &_global_Array_noneType;}
struct _global_ArrayType* _global_Array_none_get_typeByValue(struct _global_Array_none self, struct _global_Context* c){return &_global_Array_noneType;}
struct _global_ArrayType _global_Array_noneType;struct _global_PointerType _global_Maybe_rnoneType;struct _global_PointerType* _global_Maybe_rnone_get_type(void*** self, struct _global_Context* c){return &_global_Maybe_rnoneType;}
struct _global_PointerType* _global_Maybe_rnone_get_typeByValue(void** self, struct _global_Context* c){return &_global_Maybe_rnoneType;}
struct _global_StaticArray_StaticArray_S_none {
void* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_none _global_StaticArray_StaticArray_S_noneInit(void* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_none M;
M.data=data;M.length=length;return M;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_noneType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_none_get_type(struct _global_StaticArray_StaticArray_S_none* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_noneType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_none_get_typeByValue(struct _global_StaticArray_StaticArray_S_none self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_noneType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_noneType;
void _global_panic(struct _global_String _global_s, struct _global_Context* b);
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c);
struct _global_TemporaryStorage _global_new_TemporaryStorage(uint64_t _global_maxSize, struct _global_Context* d);
uint64_t _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* f);
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, uint64_t _global_size, struct _global_Context* g);
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* h);
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, uint64_t _global_occupied, struct _global_Context* j);
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, uint64_t _global_size, struct _global_Context* k);
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* l);
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* m);
void _global_Malloc_free_allocator(struct _global_Malloc* _global_self, struct _global_Context* n);
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, uint64_t _global_to, struct _global_Context* p);
void _global_free(void* _global_p, struct _global_Context* q);
void _global_free_longterm(void* _global_p, struct _global_Context* r);
void _global_TemporaryStorage_free_allocator(struct _global_TemporaryStorage* _global_self, struct _global_Context* s);
struct _global_Array_Array_T _global_empty_array(struct _global_Context* t);
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* v);

static inline void _global_Range_iterator(struct _global_Range*,struct _global_Context* v);

void _global_Range_iteratorByValue(struct _global_Range,struct _global_Context* v);
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* w);
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* x);

static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess*,struct _global_Context* x);

struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess,struct _global_Context* x);
struct _global_String _global_File_read(struct _global_File* _global_self, struct _global_Context* y);
void _global_File_write(struct _global_File* _global_self, struct _global_String _global_s, struct _global_Context* z);
void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* B);

static inline void _global_File_free(struct _global_File*,struct _global_Context* B);

void _global_File_freeByValue(struct _global_File,struct _global_Context* B);
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* C);
uint64_t _global_IntType_get_size(struct IntType* _global_self, struct _global_Context* D);
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* F);

struct _global_String _global_IntType_toString(struct IntType*,struct _global_Context* F);
uint64_t _global_FloatType_get_size(struct FloatType* _global_self, struct _global_Context* G);
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* H);

struct _global_String _global_FloatType_toString(struct FloatType*,struct _global_Context* H);
struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* J);

struct _global_String _global_BoolType_toString(struct BoolType*,struct _global_Context* J);
uint64_t _global_BoolType_get_size(struct BoolType* _global_self, struct _global_Context* K);
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* L);

struct _global_String _global_StringType_toString(struct StringType*,struct _global_Context* L);
uint64_t _global_StringType_get_size(struct StringType* _global_self, struct _global_Context* M);
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* N);

struct _global_String _global_AliasType_toString(struct _global_AliasType*,struct _global_Context* N);
uint64_t _global_AliasType_get_size(struct _global_AliasType* _global_self, struct _global_Context* P);
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* Q);

struct _global_String _global_PointerType_toString(struct _global_PointerType*,struct _global_Context* Q);
uint64_t _global_PointerType_get_size(struct _global_PointerType* _global_self, struct _global_Context* R);
uint64_t _global_StructType_get_size(struct _global_StructType* _global_self, struct _global_Context* S);
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* T);

struct _global_String _global_StructType_toString(struct _global_StructType*,struct _global_Context* T);
unsigned char _global_EnumType_get_tag(struct _global_EnumType* _global_self, void* _global_ptr, struct _global_Context* V);
struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* W);

struct _global_String _global_EnumType_toString(struct _global_EnumType*,struct _global_Context* W);
uint64_t _global_EnumType_get_size(struct _global_EnumType* _global_self, struct _global_Context* X);
uint64_t _global_FuncType_get_size(struct _global_FuncType* _global_self, struct _global_Context* Y);
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* Z);

struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType*,struct _global_Context* Z);
uint64_t _global_InterfaceType_get_size(struct _global_InterfaceType* _global_self, struct _global_Context* bb);
uint64_t _global_ArrayType_get_size(struct _global_ArrayType* _global_self, struct _global_Context* bc);
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* bd);

struct _global_String _global_ArrayType_toString(struct _global_ArrayType*,struct _global_Context* bd);
uint64_t _global_CharType_get_size(struct _global_CharType* _global_self, struct _global_Context* bf);
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* bg);

struct _global_String _global_NoneType_toString(struct NoneType*,struct _global_Context* bg);
uint64_t _global_NoneType_get_size(struct NoneType* _global_self, struct _global_Context* bh);



void _global_log_string(struct _global_String _global_s, struct _global_Context* bj);

#define _global_exit(bj,bk) exit(bj)

#define _global_c_log(bl,bm) _global_c_log(bl)
void _global_panic(struct _global_String _global_s, struct _global_Context* bn){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),bn),_global_StringInit(0,""),bn),bn);
_global_exit(1,bn);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* bn){;
;
if(!(_global_b)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),bn),_global_StringInit(0,""),bn),bn);
;};
;}

#define _global_c_memcpy(bn,bp,bq,br) memcpy(bn,bp,bq)

#define _global_c_alloc(bs,bt) malloc(bs)

#define _global_c_free(bv,bw) free(bv)
struct _global_TemporaryStorage _global_temporary_storage;struct _global_TemporaryStorage _global_longterm_storage_allocator;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator_VTABLE rTemporaryStorage_VTABLE_FOR_Allocator;struct _global_Allocator _global_malloc_as_allocator;struct _global_Allocator_VTABLE rMalloc_VTABLE_FOR_Allocator;struct _global_Allocator _global_longterm_storage_as_allocator;struct _global_TemporaryStorage _global_new_TemporaryStorage(uint64_t _global_maxSize, struct _global_Context* bx){;
;return _global_TemporaryStorageInit((uint64_t)0,(uint64_t)0,_global_c_alloc(_global_maxSize,bx),_global_maxSize);
;}
uint64_t _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* bx){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, uint64_t _global_size, struct _global_Context* bx){;
;
uint64_t _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){;
(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){;
(bx)->allocator=&(_global_malloc_as_allocator);;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(48,"ERROR: used more tempory memory than available: "),_global_u64_toStringByValue(((_global_self)->maxSize),bx),bx),_global_StringInit(0,""),bx),bx);
;};
;return _global_offsetPtr((_global_self)->data,(int64_t)_global_occupied,bx);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* bx){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, uint64_t _global_occupied, struct _global_Context* bx){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){;
(bx)->allocator=&(_global_malloc_as_allocator);;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(48,"ERROR: used more tempory memory than available: "),_global_u64_toStringByValue(((_global_self)->occupied),bx),bx),_global_StringInit(0,""),bx),bx);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, uint64_t _global_size, struct _global_Context* bx){;
;
;return _global_c_alloc(_global_size,bx);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* bx){;
;
_global_c_free(_global_pointer,bx);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* bx){;
;return 0;
;}
void _global_Malloc_free_allocator(struct _global_Malloc* _global_self, struct _global_Context* bx){;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, uint64_t _global_to, struct _global_Context* bx){;
;
;}
void _global_free(void* _global_p, struct _global_Context* bx){;
_global_Allocator_dealloc((bx)->allocator,_global_p,bx);
;}
void _global_free_longterm(void* _global_p, struct _global_Context* bx){;
_global_Allocator_dealloc((bx)->longterm_storage,_global_p,bx);
;}
void _global_TemporaryStorage_free_allocator(struct _global_TemporaryStorage* _global_self, struct _global_Context* bx){;
_global_c_free((_global_self)->data,bx);
;}

#define _global_char_buffer_toString(bx,by) _runtime_char_buffer_toString(bx)

#define _global_null_terminated '\0'

#define _global_make_String(bz,bB,bC) _global_StringInit(bz,bB)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* bD){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* bD){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* bF,struct _global_Context* bD){
_global_Range_iteratorByValue(*bF,bD);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T bG) {
struct _global_Maybe_uint bF;bF.tag = bG.tag;bF.cases = *(union _global_Maybe_uint_cases*) &(bG.cases);return bF;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* bD){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){;
unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,bD);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* bD){;
;struct _global_FileAcess bF =_global_self;
if(bF.tag==0){return _global_StringInit(1,"r");}else if(bF.tag==1){return _global_StringInit(1,"w");}else if(bF.tag==2){return _global_StringInit(2,"rb");}else if(bF.tag==3){return _global_StringInit(2,"wb");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* bG,struct _global_Context* bD){
return _global_FileAcess_toStringByValue(*bG,bD);
}
#define _global_c_open_file(bD,bF,bG) _runtime_c_open_file(bD,bF)

#define _global_c_close_file(bH,bJ) _runtime_c_close_file(bH)

#define _global_c_read_file(bK,bL,bM,bN) _runtime_read_file(bK,bL,bM)

#define _global_c_write_file(bP,bQ,bR,bS) _runtime_write_file(bP,bQ,bR)
struct _global_String _global_File_read(struct _global_File* _global_self, struct _global_Context* bT){;
struct _global_FileAcess bV =(_global_self)->acess;if(bV.tag==0){
;}
else if(bV.tag==2){
;}
else if(1){
_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bT);
;}
;
;return _global_c_read_file((_global_self)->c_file,(_global_self)->filename,bT,bT);
;}
void _global_File_write(struct _global_File* _global_self, struct _global_String _global_s, struct _global_Context* bT){;
;
struct _global_FileAcess bV =(_global_self)->acess;if(bV.tag==1){
;}
else if(bV.tag==3){
;}
else if(1){
_global_panic(_global_StringInit(40,"Trying to write to file not set to write"),bT);
;}
;
_global_c_write_file((_global_self)->c_file,_global_s,bT,bT);
;}
void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bT){;
_global_c_close_file((_global_self).c_file,bT);
;}
static inline void _global_File_free(struct _global_File* bV,struct _global_Context* bT){
_global_File_freeByValue(*bV,bT);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bX) {
struct _global_Maybe_File bW;bW.tag = bX.tag;bW.cases = *(union _global_Maybe_File_cases*) &(bX.cases);return bW;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bT){;
;
;struct FILE* bV =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bT),bT);
if(bV != NULL){struct FILE* _global_file = bV;
return _global_Some_File(_global_FileInit(_global_file,_global_acess,_global_filename),bT);}else if(bV == NULL){return tmp_globalc(_global_None);};
;}

#define _global_set_bit_to(bT,bV,bW,bX) _global_c_set_bit_to(bT,bV,bW)

#define _global_is_bit_set(bY,bZ,cb) _global_c_is_bit_set(bY,bZ)

#define _global_bit_and(db,fb,gb) _global_c_bit_and(db,fb)

#define _global_null_char '\0'
uint64_t _global_IntType_get_size(struct IntType* _global_self, struct _global_Context* hb){;
;return (uint64_t)(_global_self)->size;
;}
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* hb){;
;return ((_global_self)->sign ? _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"i"),_global_uint_toStringByValue(((_global_self)->size*8),hb),hb),_global_StringInit(0,""),hb):(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"u"),_global_uint_toStringByValue(((_global_self)->size*8),hb),hb),_global_StringInit(0,""),hb)));
;}
static inline struct _global_String _global_IntType_toStringByValue(struct IntType jb,struct _global_Context* hb){
return _global_IntType_toString(&jb,hb);
}uint64_t _global_FloatType_get_size(struct FloatType* _global_self, struct _global_Context* hb){;
;return (uint64_t)(_global_self)->size;
;}
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* hb){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"f"),_global_uint_toStringByValue(((_global_self)->size*8),hb),hb),_global_StringInit(0,""),hb);
;}
static inline struct _global_String _global_FloatType_toStringByValue(struct FloatType jb,struct _global_Context* hb){
return _global_FloatType_toString(&jb,hb);
}struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* hb){;
;return _global_StringInit(4,"bool");
;}
static inline struct _global_String _global_BoolType_toStringByValue(struct BoolType jb,struct _global_Context* hb){
return _global_BoolType_toString(&jb,hb);
}uint64_t _global_BoolType_get_size(struct BoolType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(_Bool);
;}
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* hb){;
;return _global_StringInit(6,"string");
;}
static inline struct _global_String _global_StringType_toStringByValue(struct StringType jb,struct _global_Context* hb){
return _global_StringType_toString(&jb,hb);
}uint64_t _global_StringType_get_size(struct StringType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(struct _global_String);
;}
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* hb){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),hb),_global_StringInit(1,"."),hb),((_global_self)->name),hb),_global_StringInit(0,""),hb);
;}
static inline struct _global_String _global_AliasType_toStringByValue(struct _global_AliasType jb,struct _global_Context* hb){
return _global_AliasType_toString(&jb,hb);
}uint64_t _global_AliasType_get_size(struct _global_AliasType* _global_self, struct _global_Context* hb){;
;return _global_Type_get_size(&((_global_self)->real_type),hb);
;}
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* hb){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"&"),_global_Type_toStringByValue(((_global_self)->p_type),hb),hb),_global_StringInit(0,""),hb);
;}
static inline struct _global_String _global_PointerType_toStringByValue(struct _global_PointerType jb,struct _global_Context* hb){
return _global_PointerType_toString(&jb,hb);
}uint64_t _global_PointerType_get_size(struct _global_PointerType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(void*);
;}
uint64_t _global_StructType_get_size(struct _global_StructType* _global_self, struct _global_Context* hb){;
;return (_global_self)->size;
;}
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* hb){;
;return (_global_String_op_eqByValue((_global_self)->package,_global_StringInit(7,"_global"),hb) ? (_global_self)->name:(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),hb),_global_StringInit(1,"."),hb),((_global_self)->name),hb),_global_StringInit(0,""),hb)));
;}
static inline struct _global_String _global_StructType_toStringByValue(struct _global_StructType jb,struct _global_Context* hb){
return _global_StructType_toString(&jb,hb);
}unsigned char _global_EnumType_get_tag(struct _global_EnumType* _global_self, void* _global_ptr, struct _global_Context* hb){;
;
;return *((unsigned char*)(_global_offsetPtr(_global_ptr,(int64_t)((_global_self)->tag_field).offset,hb)));
;}
struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* hb){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),hb),_global_StringInit(1,"."),hb),((_global_self)->name),hb),_global_StringInit(0,""),hb);
;}
static inline struct _global_String _global_EnumType_toStringByValue(struct _global_EnumType jb,struct _global_Context* hb){
return _global_EnumType_toString(&jb,hb);
}uint64_t _global_EnumType_get_size(struct _global_EnumType* _global_self, struct _global_Context* hb){;
;return (_global_self)->size;
;}
uint64_t _global_FuncType_get_size(struct _global_FuncType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(pp___none);
;}
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* hb){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),hb),_global_StringInit(1,"."),hb),((_global_self)->name),hb),_global_StringInit(0,""),hb);
;}
static inline struct _global_String _global_InterfaceType_toStringByValue(struct _global_InterfaceType jb,struct _global_Context* hb){
return _global_InterfaceType_toString(&jb,hb);
}uint64_t _global_InterfaceType_get_size(struct _global_InterfaceType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(struct bb);
;}
uint64_t _global_ArrayType_get_size(struct _global_ArrayType* _global_self, struct _global_Context* hb){;
;struct _global_ArraySize jb =*((_global_self)->size);
if(jb.tag==0){unsigned int _global_length = jb.cases.Static.field0;
return (uint64_t)_global_length*_global_Type_get_size(&((_global_self)->array_type),hb);}else if(jb.tag==1){return (uint64_t)sizeof(struct _global_Array_none);}else if(jb.tag==2){return (uint64_t)sizeof(struct _global_StaticArray_StaticArray_S_none);};
;}
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* hb){;
;struct _global_ArraySize jb =*((_global_self)->size);
if(jb.tag==0){unsigned int _global_length = jb.cases.Static.field0;
return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"["),_global_uint_toStringByValue((_global_length),hb),hb),_global_StringInit(1,"]"),hb),_global_Type_toStringByValue(((_global_self)->array_type),hb),hb),_global_StringInit(0,""),hb);}else if(jb.tag==1){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(4,"[..]"),_global_Type_toStringByValue(((_global_self)->array_type),hb),hb),_global_StringInit(0,""),hb);}else if(jb.tag==2){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[]"),_global_Type_toStringByValue(((_global_self)->array_type),hb),hb),_global_StringInit(0,""),hb);};
;}
static inline struct _global_String _global_ArrayType_toStringByValue(struct _global_ArrayType kb,struct _global_Context* hb){
return _global_ArrayType_toString(&kb,hb);
}uint64_t _global_CharType_get_size(struct _global_CharType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(char);
;}
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* hb){;
;return _global_StringInit(4,"none");
;}
static inline struct _global_String _global_NoneType_toStringByValue(struct NoneType jb,struct _global_Context* hb){
return _global_NoneType_toString(&jb,hb);
}uint64_t _global_NoneType_get_size(struct NoneType* _global_self, struct _global_Context* hb){;
;return (uint64_t)sizeof(char);
;}
void _global_log_string(struct _global_String _global_s, struct _global_Context* hb){;
_global_c_log(_global_String_toString(&(_global_s),hb),hb);
;}

void _globalInitTypes() { 
 
_global_TemporaryStorageType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 4);
_global_TemporaryStorageType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_TemporaryStorageType_fields
,4
);
_global_TemporaryStorageType.package = _global_StringInit(7, "_global");
_global_TemporaryStorageType.name = _global_StringInit(16, "TemporaryStorage");
_global_TemporaryStorageType.size = sizeof(struct _global_TemporaryStorage);
_global_TemporaryStorageType_fields[0].name = _global_StringInit(8, "occupied");
_global_TemporaryStorageType_fields[0].offset = offsetof(struct _global_TemporaryStorage, occupied);
_global_TemporaryStorageType_fields[0].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_AliasType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;
_global_TemporaryStorageType_fields[1].name = _global_StringInit(7, "highest");
_global_TemporaryStorageType_fields[1].offset = offsetof(struct _global_TemporaryStorage, highest);
_global_TemporaryStorageType_fields[1].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;
_global_TemporaryStorageType_fields[2].name = _global_StringInit(4, "data");
_global_TemporaryStorageType_fields[2].offset = offsetof(struct _global_TemporaryStorage, data);
_global_TemporaryStorageType_fields[2].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
,0),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;
_global_TemporaryStorageType_fields[3].name = _global_StringInit(7, "maxSize");
_global_TemporaryStorageType_fields[3].offset = offsetof(struct _global_TemporaryStorage, maxSize);
_global_TemporaryStorageType_fields[3].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;_global_MallocType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_MallocType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_MallocType_fields
,0
);
_global_MallocType.package = _global_StringInit(7, "_global");
_global_MallocType.name = _global_StringInit(6, "Malloc");
_global_MallocType.size = sizeof(struct _global_Malloc);_global_Maybe_rAllocatorType.p_type =
_global_TypeFromStruct(
&_global_Allocator_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;
_global_Maybe_rAllocatorType.nullable = 1;_global_Maybe_rArray_TType.p_type =
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;
_global_Maybe_rArray_TType.nullable = 1;_global_Array_Array_TType.size = malloc(sizeof(struct _global_ArraySize));
_global_Array_Array_TType.size->tag = 1;
_global_Array_Array_TType.array_type=
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;_global_RangeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_RangeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_RangeType_fields
,2
);
_global_RangeType.package = _global_StringInit(7, "_global");
_global_RangeType.name = _global_StringInit(5, "Range");
_global_RangeType.size = sizeof(struct _global_Range);
_global_RangeType_fields[0].name = _global_StringInit(5, "start");
_global_RangeType_fields[0].offset = offsetof(struct _global_Range, start);
_global_RangeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;
_global_RangeType_fields[1].name = _global_StringInit(3, "end");
_global_RangeType_fields[1].offset = offsetof(struct _global_Range, end);
_global_RangeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;struct _global_Case* l =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 2);
l[0].name = _global_StringInit(4, "Some");
l[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 1), 1);
l[0].args.data[0].arg_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
; l[0].args.data[0].offset = offsetof(struct _global_Maybe_uint_Some, field0);
l[1].name = _global_StringInit(4, "None");
l[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
_global_Maybe_uintType.tag_field.name = _global_StringInit(3, "tag");

_global_Maybe_uintType.tag_field.offset = offsetof(struct _global_Maybe_uint, tag);
_global_Maybe_uintType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

_global_Maybe_uintType.size = sizeof(struct _global_Maybe_uint);

_global_Maybe_uintType.package = _global_StringInit(7, "_global");
_global_Maybe_uintType.name = _global_StringInit(10, "Maybe_uint");
_global_Maybe_uintType.cases.data = l;
_global_Maybe_uintType.cases.length = 2;
_global_RangeIteratorType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_RangeIteratorType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_RangeIteratorType_fields
,2
);
_global_RangeIteratorType.package = _global_StringInit(7, "_global");
_global_RangeIteratorType.name = _global_StringInit(13, "RangeIterator");
_global_RangeIteratorType.size = sizeof(struct _global_RangeIterator);
_global_RangeIteratorType_fields[0].name = _global_StringInit(5, "range");
_global_RangeIteratorType_fields[0].offset = offsetof(struct _global_RangeIterator, range);
_global_RangeIteratorType_fields[0].field_type = 
_global_TypeFromStruct(
_global_Range_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;
_global_RangeIteratorType_fields[1].name = _global_StringInit(2, "it");
_global_RangeIteratorType_fields[1].offset = offsetof(struct _global_RangeIterator, it);
_global_RangeIteratorType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;
_global_ReadBFile.tag = 2;
_global_WriteBFile.tag = 3;
struct _global_Case* p =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 4);
p[0].name = _global_StringInit(8, "ReadFile");
p[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
p[1].name = _global_StringInit(9, "WriteFile");
p[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
p[2].name = _global_StringInit(9, "ReadBFile");
p[2].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
p[3].name = _global_StringInit(10, "WriteBFile");
p[3].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
_global_FileAcessType.tag_field.name = _global_StringInit(3, "tag");

_global_FileAcessType.tag_field.offset = offsetof(struct _global_FileAcess, tag);
_global_FileAcessType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

_global_FileAcessType.size = sizeof(struct _global_FileAcess);

_global_FileAcessType.package = _global_StringInit(7, "_global");
_global_FileAcessType.name = _global_StringInit(9, "FileAcess");
_global_FileAcessType.cases.data = p;
_global_FileAcessType.cases.length = 4;
_global_FILEType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_FILEType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FILEType_fields
,0
);
_global_FILEType.package = _global_StringInit(7, "_global");
_global_FILEType.name = _global_StringInit(4, "FILE");_global_FileType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 3);
_global_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FileType_fields
,3
);
_global_FileType.package = _global_StringInit(7, "_global");
_global_FileType.name = _global_StringInit(4, "File");
_global_FileType.size = sizeof(struct _global_File);
_global_FileType_fields[0].name = _global_StringInit(6, "c_file");
_global_FileType_fields[0].offset = offsetof(struct _global_File, c_file);
_global_FileType_fields[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
_global_FILE_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
,0),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;
_global_FileType_fields[1].name = _global_StringInit(5, "acess");
_global_FileType_fields[1].offset = offsetof(struct _global_File, acess);
_global_FileType_fields[1].field_type = 
_global_TypeFromStruct(
_global_FileAcess_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;
_global_FileType_fields[2].name = _global_StringInit(8, "filename");
_global_FileType_fields[2].offset = offsetof(struct _global_File, filename);
_global_FileType_fields[2].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;struct _global_Case* w =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 2);
w[0].name = _global_StringInit(4, "Some");
w[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 1), 1);
w[0].args.data[0].arg_type = 
_global_TypeFromStruct(
_global_File_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
; w[0].args.data[0].offset = offsetof(struct _global_Maybe_File_Some, field0);
w[1].name = _global_StringInit(4, "None");
w[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
_global_Maybe_FileType.tag_field.name = _global_StringInit(3, "tag");

_global_Maybe_FileType.tag_field.offset = offsetof(struct _global_Maybe_File, tag);
_global_Maybe_FileType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

_global_Maybe_FileType.size = sizeof(struct _global_Maybe_File);

_global_Maybe_FileType.package = _global_StringInit(7, "_global");
_global_Maybe_FileType.name = _global_StringInit(10, "Maybe_File");
_global_Maybe_FileType.cases.data = w;
_global_Maybe_FileType.cases.length = 2;
_global_FloatTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_FloatTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FloatTypeType_fields
,0
);
_global_FloatTypeType.package = _global_StringInit(7, "_global");
_global_FloatTypeType.name = _global_StringInit(9, "FloatType");_global_StaticArray_StaticArray_S_TypeType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_StaticArray_S_TypeType.size->tag = 2;
_global_StaticArray_StaticArray_S_TypeType.array_type=
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_FuncTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_FuncTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FuncTypeType_fields
,2
);
_global_FuncTypeType.package = _global_StringInit(7, "_global");
_global_FuncTypeType.name = _global_StringInit(8, "FuncType");
_global_FuncTypeType.size = sizeof(struct _global_FuncType);
_global_FuncTypeType_fields[0].name = _global_StringInit(4, "args");
_global_FuncTypeType_fields[0].offset = offsetof(struct _global_FuncType, args);
_global_FuncTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Type_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_FuncTypeType_fields[1].name = _global_StringInit(11, "return_type");
_global_FuncTypeType_fields[1].offset = offsetof(struct _global_FuncType, return_type);
_global_FuncTypeType_fields[1].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_CharTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_CharTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_CharTypeType_fields
,0
);
_global_CharTypeType.package = _global_StringInit(7, "_global");
_global_CharTypeType.name = _global_StringInit(8, "CharType");
_global_CharTypeType.size = sizeof(struct _global_CharType);_global_None.tag = 1;
struct _global_Case* G =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 2);
G[0].name = _global_StringInit(4, "Some");
G[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 1), 1);
G[0].args.data[0].arg_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
; G[0].args.data[0].offset = offsetof(struct _global_Maybe_Maybe_T_Some, field0);
G[1].name = _global_StringInit(4, "None");
G[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
_global_Maybe_Maybe_TType.tag_field.name = _global_StringInit(3, "tag");

_global_Maybe_Maybe_TType.tag_field.offset = offsetof(struct _global_Maybe_Maybe_T, tag);
_global_Maybe_Maybe_TType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

_global_Maybe_Maybe_TType.size = sizeof(struct _global_Maybe_Maybe_T);

_global_Maybe_Maybe_TType.package = _global_StringInit(7, "_global");
_global_Maybe_Maybe_TType.name = _global_StringInit(13, "Maybe_Maybe_T");
_global_Maybe_Maybe_TType.cases.data = G;
_global_Maybe_Maybe_TType.cases.length = 2;
_global_Maybe_rFILEType.p_type =
_global_TypeFromStruct(
_global_FILE_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;
_global_Maybe_rFILEType.nullable = 1;bb_Type.name = _global_StringInit(0, "")
;bb_Type.package = _global_StringInit(0, "");_global_Array_noneType.size = malloc(sizeof(struct _global_ArraySize));
_global_Array_noneType.size->tag = 1;
_global_Array_noneType.array_type=
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;_global_Maybe_rnoneType.p_type =
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;
_global_Maybe_rnoneType.nullable = 1;_global_StaticArray_StaticArray_S_noneType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_StaticArray_S_noneType.size->tag = 2;
_global_StaticArray_StaticArray_S_noneType.array_type=
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
; }
void _globalInit() { 
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage((uint64_t)10000000,(&_global_context));;
_global_longterm_storage_allocator = _global_new_TemporaryStorage((uint64_t)100000000,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&(_global_temporary_storage),&rTemporaryStorage_VTABLE_FOR_Allocator,_global_TypeFromStruct(_global_TemporaryStorage_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to, &_global_TemporaryStorage_free_allocator);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&(_global_malloc),&rMalloc_VTABLE_FOR_Allocator,_global_TypeFromStruct(_global_Malloc_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &_global_Malloc_get_occupied, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_reset_to, &_global_Malloc_free_allocator);;
_global_longterm_storage_as_allocator = _global_AllocatorFromStruct(&(_global_longterm_storage_allocator),&rTemporaryStorage_VTABLE_FOR_Allocator,rTemporaryStorage_VTABLE_FOR_Allocator.type, &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to, &_global_TemporaryStorage_free_allocator);;
(&_global_context)->allocator = &(_global_temporary_storage_as_allocator);
(&_global_context)->longterm_storage = &(_global_longterm_storage_as_allocator);
;
;
;
;
;
;
;
;
;
;
;
;
};

void mainInitTypes() { 
 _globalInitTypes();
 }
void mainInit() { 
_globalInit();;
;
};
int main() { 
_globalInitTypes(); _globalInit(); _global_init_c_runtime(); 
 _global_Type_Type.name = _global_StringInit(4, "Type")
;_global_Type_Type.package = _global_StringInit(7, "_global");_global_StaticArray_StaticArray_S_FieldType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_StaticArray_S_FieldType.size->tag = 2;
_global_StaticArray_StaticArray_S_FieldType.array_type=
_global_TypeFromStruct(
_global_Field_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;_global_StructTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 5);
_global_StructTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_StructTypeType_fields
,5
);
_global_StructTypeType.package = _global_StringInit(7, "_global");
_global_StructTypeType.name = _global_StringInit(10, "StructType");
_global_StructTypeType.size = sizeof(struct _global_StructType);
_global_StructTypeType_fields[0].name = _global_StringInit(4, "name");
_global_StructTypeType_fields[0].offset = offsetof(struct _global_StructType, name);
_global_StructTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_StringType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_StructType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_StructTypeType_fields[1].name = _global_StringInit(7, "package");
_global_StructTypeType_fields[1].offset = offsetof(struct _global_StructType, package);
_global_StructTypeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_StructTypeType_fields[2].name = _global_StringInit(9, "real_type");
_global_StructTypeType_fields[2].offset = offsetof(struct _global_StructType, real_type);
_global_StructTypeType_fields[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_InterfaceType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;
_global_StructTypeType_fields[3].name = _global_StringInit(6, "fields");
_global_StructTypeType_fields[3].offset = offsetof(struct _global_StructType, fields);
_global_StructTypeType_fields[3].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Field_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_ArrayType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_StructTypeType_fields[4].name = _global_StringInit(4, "size");
_global_StructTypeType_fields[4].offset = offsetof(struct _global_StructType, size);
_global_StructTypeType_fields[4].field_type = 
_global_TypeFromStruct(
_global_u64_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_StringTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_StringTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_StringTypeType_fields
,0
);
_global_StringTypeType.package = _global_StringInit(7, "_global");
_global_StringTypeType.name = _global_StringInit(10, "StringType");_global_InterfaceTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 4);
_global_InterfaceTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_InterfaceTypeType_fields
,4
);
_global_InterfaceTypeType.package = _global_StringInit(7, "_global");
_global_InterfaceTypeType.name = _global_StringInit(13, "InterfaceType");
_global_InterfaceTypeType.size = sizeof(struct _global_InterfaceType);
_global_InterfaceTypeType_fields[0].name = _global_StringInit(4, "name");
_global_InterfaceTypeType_fields[0].offset = offsetof(struct _global_InterfaceType, name);
_global_InterfaceTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_InterfaceTypeType_fields[1].name = _global_StringInit(7, "package");
_global_InterfaceTypeType_fields[1].offset = offsetof(struct _global_InterfaceType, package);
_global_InterfaceTypeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_InterfaceTypeType_fields[2].name = _global_StringInit(6, "fields");
_global_InterfaceTypeType_fields[2].offset = offsetof(struct _global_InterfaceType, fields);
_global_InterfaceTypeType_fields[2].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Field_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_InterfaceTypeType_fields[3].name = _global_StringInit(7, "methods");
_global_InterfaceTypeType_fields[3].offset = offsetof(struct _global_InterfaceType, methods);
_global_InterfaceTypeType_fields[3].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Method_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
,0),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;_global_StaticArray_StaticArray_S_CaseType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_StaticArray_S_CaseType.size->tag = 2;
_global_StaticArray_StaticArray_S_CaseType.array_type=
_global_TypeFromStruct(
_global_Case_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;_global_StaticArray_StaticArray_S_CaseArgType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_StaticArray_S_CaseArgType.size->tag = 2;
_global_StaticArray_StaticArray_S_CaseArgType.array_type=
_global_TypeFromStruct(
_global_CaseArg_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;_global_IntTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_IntTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_IntTypeType_fields
,0
);
_global_IntTypeType.package = _global_StringInit(7, "_global");
_global_IntTypeType.name = _global_StringInit(7, "IntType");_global_CaseArgType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_CaseArgType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_CaseArgType_fields
,2
);
_global_CaseArgType.package = _global_StringInit(7, "_global");
_global_CaseArgType.name = _global_StringInit(7, "CaseArg");
_global_CaseArgType.size = sizeof(struct _global_CaseArg);
_global_CaseArgType_fields[0].name = _global_StringInit(8, "arg_type");
_global_CaseArgType_fields[0].offset = offsetof(struct _global_CaseArg, arg_type);
_global_CaseArgType_fields[0].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;
_global_CaseArgType_fields[1].name = _global_StringInit(6, "offset");
_global_CaseArgType_fields[1].offset = offsetof(struct _global_CaseArg, offset);
_global_CaseArgType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_IntType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_ArrayTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_ArrayTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_ArrayTypeType_fields
,2
);
_global_ArrayTypeType.package = _global_StringInit(7, "_global");
_global_ArrayTypeType.name = _global_StringInit(9, "ArrayType");
_global_ArrayTypeType.size = sizeof(struct _global_ArrayType);
_global_ArrayTypeType_fields[0].name = _global_StringInit(4, "size");
_global_ArrayTypeType_fields[0].offset = offsetof(struct _global_ArrayType, size);
_global_ArrayTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
_global_ArraySize_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_EnumType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
,0),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;
_global_ArrayTypeType_fields[1].name = _global_StringInit(10, "array_type");
_global_ArrayTypeType_fields[1].offset = offsetof(struct _global_ArrayType, array_type);
_global_ArrayTypeType_fields[1].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_CaseType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_CaseType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_CaseType_fields
,2
);
_global_CaseType.package = _global_StringInit(7, "_global");
_global_CaseType.name = _global_StringInit(4, "Case");
_global_CaseType.size = sizeof(struct _global_Case);
_global_CaseType_fields[0].name = _global_StringInit(4, "name");
_global_CaseType_fields[0].offset = offsetof(struct _global_Case, name);
_global_CaseType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_CaseType_fields[1].name = _global_StringInit(4, "args");
_global_CaseType_fields[1].offset = offsetof(struct _global_Case, args);
_global_CaseType_fields[1].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_CaseArg_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;_global_NoneTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_NoneTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_NoneTypeType_fields
,0
);
_global_NoneTypeType.package = _global_StringInit(7, "_global");
_global_NoneTypeType.name = _global_StringInit(8, "NoneType");_global_PointerTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_PointerTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_PointerTypeType_fields
,2
);
_global_PointerTypeType.package = _global_StringInit(7, "_global");
_global_PointerTypeType.name = _global_StringInit(11, "PointerType");
_global_PointerTypeType.size = sizeof(struct _global_PointerType);
_global_PointerTypeType_fields[0].name = _global_StringInit(6, "p_type");
_global_PointerTypeType_fields[0].offset = offsetof(struct _global_PointerType, p_type);
_global_PointerTypeType_fields[0].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;
_global_PointerTypeType_fields[1].name = _global_StringInit(8, "nullable");
_global_PointerTypeType_fields[1].offset = offsetof(struct _global_PointerType, nullable);
_global_PointerTypeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_Bool_get_type(NULL,(&_global_context))
,
&rBoolType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_BoolType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_BoolType_toString
, &_global_BoolType_get_size
)
;_global_MethodType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_MethodType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_MethodType_fields
,2
);
_global_MethodType.package = _global_StringInit(7, "_global");
_global_MethodType.name = _global_StringInit(6, "Method");
_global_MethodType.size = sizeof(struct _global_Method);
_global_MethodType_fields[0].name = _global_StringInit(4, "name");
_global_MethodType_fields[0].offset = offsetof(struct _global_Method, name);
_global_MethodType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_MethodType_fields[1].name = _global_StringInit(17, "pointer_to_method");
_global_MethodType_fields[1].offset = offsetof(struct _global_Method, pointer_to_method);
_global_MethodType_fields[1].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_NoneType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
,0),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_PointerType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;_global_FieldType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 3);
_global_FieldType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FieldType_fields
,3
);
_global_FieldType.package = _global_StringInit(7, "_global");
_global_FieldType.name = _global_StringInit(5, "Field");
_global_FieldType.size = sizeof(struct _global_Field);
_global_FieldType_fields[0].name = _global_StringInit(4, "name");
_global_FieldType_fields[0].offset = offsetof(struct _global_Field, name);
_global_FieldType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_FieldType_fields[1].name = _global_StringInit(6, "offset");
_global_FieldType_fields[1].offset = offsetof(struct _global_Field, offset);
_global_FieldType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;
_global_FieldType_fields[2].name = _global_StringInit(10, "field_type");
_global_FieldType_fields[2].offset = offsetof(struct _global_Field, field_type);
_global_FieldType_fields[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_EnumTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 6);
_global_EnumTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_EnumTypeType_fields
,6
);
_global_EnumTypeType.package = _global_StringInit(7, "_global");
_global_EnumTypeType.name = _global_StringInit(8, "EnumType");
_global_EnumTypeType.size = sizeof(struct _global_EnumType);
_global_EnumTypeType_fields[0].name = _global_StringInit(4, "name");
_global_EnumTypeType_fields[0].offset = offsetof(struct _global_EnumType, name);
_global_EnumTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_EnumTypeType_fields[1].name = _global_StringInit(7, "package");
_global_EnumTypeType_fields[1].offset = offsetof(struct _global_EnumType, package);
_global_EnumTypeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_EnumTypeType_fields[2].name = _global_StringInit(5, "cases");
_global_EnumTypeType_fields[2].offset = offsetof(struct _global_EnumType, cases);
_global_EnumTypeType_fields[2].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Case_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_EnumTypeType_fields[3].name = _global_StringInit(7, "methods");
_global_EnumTypeType_fields[3].offset = offsetof(struct _global_EnumType, methods);
_global_EnumTypeType_fields[3].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Method_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_EnumTypeType_fields[4].name = _global_StringInit(9, "tag_field");
_global_EnumTypeType_fields[4].offset = offsetof(struct _global_EnumType, tag_field);
_global_EnumTypeType_fields[4].field_type = 
_global_TypeFromStruct(
_global_Field_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;
_global_EnumTypeType_fields[5].name = _global_StringInit(4, "size");
_global_EnumTypeType_fields[5].offset = offsetof(struct _global_EnumType, size);
_global_EnumTypeType_fields[5].field_type = 
_global_TypeFromStruct(
_global_u64_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_Dynamic.tag = 1;
_global_Both.tag = 2;
struct _global_Case* x =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 3);
x[0].name = _global_StringInit(6, "Static");
x[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 1), 1);
x[0].args.data[0].arg_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
; x[0].args.data[0].offset = offsetof(struct _global_ArraySize_Static, field0);
x[1].name = _global_StringInit(7, "Dynamic");
x[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
x[2].name = _global_StringInit(4, "Both");
x[2].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
_global_ArraySizeType.tag_field.name = _global_StringInit(3, "tag");

_global_ArraySizeType.tag_field.offset = offsetof(struct _global_ArraySize, tag);
_global_ArraySizeType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

_global_ArraySizeType.size = sizeof(struct _global_ArraySize);

_global_ArraySizeType.package = _global_StringInit(7, "_global");
_global_ArraySizeType.name = _global_StringInit(9, "ArraySize");
_global_ArraySizeType.cases.data = x;
_global_ArraySizeType.cases.length = 3;
_global_BoolTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_BoolTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_BoolTypeType_fields
,0
);
_global_BoolTypeType.package = _global_StringInit(7, "_global");
_global_BoolTypeType.name = _global_StringInit(8, "BoolType");_global_AliasTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 3);
_global_AliasTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_AliasTypeType_fields
,3
);
_global_AliasTypeType.package = _global_StringInit(7, "_global");
_global_AliasTypeType.name = _global_StringInit(9, "AliasType");
_global_AliasTypeType.size = sizeof(struct _global_AliasType);
_global_AliasTypeType_fields[0].name = _global_StringInit(4, "name");
_global_AliasTypeType_fields[0].offset = offsetof(struct _global_AliasType, name);
_global_AliasTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_AliasTypeType_fields[1].name = _global_StringInit(7, "package");
_global_AliasTypeType_fields[1].offset = offsetof(struct _global_AliasType, package);
_global_AliasTypeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
_global_AliasTypeType_fields[2].name = _global_StringInit(9, "real_type");
_global_AliasTypeType_fields[2].offset = offsetof(struct _global_AliasType, real_type);
_global_AliasTypeType_fields[2].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_SizeT_Type.name = _global_StringInit(5, "SizeT");
_global_SizeT_Type.package = _global_StringInit(7, "_global");
_global_SizeT_Type.real_type = 
_global_TypeFromStruct(
_global_u64_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_Allocator_Type.name = _global_StringInit(9, "Allocator")
;_global_Allocator_Type.package = _global_StringInit(7, "_global");; 
 mainInitTypes(); mainInit(); return 0;  };