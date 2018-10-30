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
typedef unsigned int(*prnonep___uint)(void*,struct _global_Context*) ;
typedef void*(*prnonec_SizeTp___rnone)(void*,unsigned int,struct _global_Context*) ;
typedef void(*prnonec_rnonep___none)(void*,void*,struct _global_Context*) ;
typedef void(*prnonec_uintp___none)(void*,unsigned int,struct _global_Context*) ;
struct _global_Allocator {
void* type; /* is always null, for now */ 
void* data;
prnonep___uint method_get_occupied;
prnonec_SizeTp___rnone method_alloc;
prnonec_rnonep___none method_dealloc;
prnonec_uintp___none method_reset_to;
};static inline struct _global_Allocator _global_AllocatorFromStruct(void* data, prnonep___uint c, prnonec_SizeTp___rnone d, prnonec_rnonep___none f, prnonec_uintp___none g){ 
struct _global_Allocator h;
h.data = data;h.method_get_occupied = c;
h.method_alloc = d;
h.method_dealloc = f;
h.method_reset_to = g;
return h; 
}static inline unsigned int _global_Allocator_get_occupied(struct _global_Allocator* h,struct _global_Context* b){
return h->method_get_occupied(h->data,b);
};static inline unsigned int _global_Allocator_get_occupiedByValue(struct _global_Allocator h,struct _global_Context* b){
return h.method_get_occupied(h.data,b);
};static inline void* _global_Allocator_alloc(struct _global_Allocator* h,unsigned int k,struct _global_Context* b){
return h->method_alloc(h->data,k,b);
};static inline void* _global_Allocator_allocByValue(struct _global_Allocator h,unsigned int k,struct _global_Context* b){
return h.method_alloc(h.data,k,b);
};static inline void _global_Allocator_dealloc(struct _global_Allocator* h,void* m,struct _global_Context* b){
return h->method_dealloc(h->data,m,b);
};static inline void _global_Allocator_deallocByValue(struct _global_Allocator h,void* m,struct _global_Context* b){
return h.method_dealloc(h.data,m,b);
};static inline void _global_Allocator_reset_to(struct _global_Allocator* h,unsigned int p,struct _global_Context* b){
return h->method_reset_to(h->data,p,b);
};static inline void _global_Allocator_reset_toByValue(struct _global_Allocator h,unsigned int p,struct _global_Context* b){
return h.method_reset_to(h.data,p,b);
};struct _global_Context {
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
    return _global_##name##_get_typeByValue(*number, context); \
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

static inline void* _global_offsetPtr(void* ptr, int offset,__Context) {
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

void _global_init_c_runtime() {
    printf("Initialized types\n");
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
struct _global_TemporaryStorage b;
b.occupied=occupied;b.highest=highest;b.data=data;b.maxSize=maxSize;return b;
};
struct _global_StructType _global_TemporaryStorageType;struct _global_StructType* _global_TemporaryStorage_get_type(struct _global_TemporaryStorage self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_StructType* _global_TemporaryStorage_get_typeByValue(struct _global_TemporaryStorage self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc b;
return b;
};
struct _global_StructType _global_MallocType;struct _global_StructType* _global_Malloc_get_type(struct _global_Malloc self, struct _global_Context* c){return &_global_MallocType;}
struct _global_StructType* _global_Malloc_get_typeByValue(struct _global_Malloc self, struct _global_Context* c){return &_global_MallocType;}
struct bb {
void* type; /* is always null, for now */ 
void* data;
};static inline struct bb bbFromStruct(void* data){ 
struct bb c;
c.data = data;return c; 
}struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
struct bb* data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,struct bb* data){
struct _global_Array_Array_T b;
b.length=length;b.capacity=capacity;b.allocator=allocator;b.data=data;return b;
};
struct _global_StructType _global_Array_Array_TType;struct _global_StructType* _global_Array_Array_T_get_type(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_StructType* _global_Array_Array_T_get_typeByValue(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range b;
b.start=start;b.end=end;return b;
};
struct _global_StructType _global_RangeType;struct _global_StructType* _global_Range_get_type(struct _global_Range self, struct _global_Context* c){return &_global_RangeType;}
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
struct _global_Maybe_uint _global_Some_uint(unsigned int b,struct _global_Context* c){
struct _global_Maybe_uint d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator b;
b.range=range;b.it=it;return b;
};
struct _global_StructType _global_RangeIteratorType;struct _global_StructType* _global_RangeIterator_get_type(struct _global_RangeIterator self, struct _global_Context* c){return &_global_RangeIteratorType;}
struct _global_StructType* _global_RangeIterator_get_typeByValue(struct _global_RangeIterator self, struct _global_Context* c){return &_global_RangeIteratorType;}
union _global_FileAcess_cases {

};
struct _global_FileAcess {
 _Bool tag;
union _global_FileAcess_cases cases;

};
struct _global_FileAcess _global_ReadFile;
struct _global_FileAcess _global_WriteFile;
struct _global_File {
struct FILE* c_file;
struct _global_FileAcess acess;
};
static inline struct _global_File _global_FileInit(struct FILE* c_file,struct _global_FileAcess acess){
struct _global_File b;
b.c_file=c_file;b.acess=acess;return b;
};
struct _global_StructType _global_FileType;struct _global_StructType* _global_File_get_type(struct _global_File self, struct _global_Context* c){return &_global_FileType;}
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
struct _global_Maybe_File _global_Some_File(struct _global_File b,struct _global_Context* c){
struct _global_Maybe_File d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_Field {
struct _global_String name;
unsigned int offset;
struct bb field_type;
};
static inline struct _global_Field _global_FieldInit(struct _global_String name,unsigned int offset,struct bb field_type){
struct _global_Field b;
b.name=name;b.offset=offset;b.field_type=field_type;return b;
};
struct _global_StructType _global_FieldType;struct _global_StructType* _global_Field_get_type(struct _global_Field self, struct _global_Context* c){return &_global_FieldType;}
struct _global_StructType* _global_Field_get_typeByValue(struct _global_Field self, struct _global_Context* c){return &_global_FieldType;}
struct _global_StaticArray_StaticArray_S_Field {
struct _global_Field* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_Field _global_StaticArray_StaticArray_S_FieldInit(struct _global_Field* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_Field b;
b.data=data;b.length=length;return b;
};
struct _global_StructType _global_StaticArray_StaticArray_S_FieldType;struct _global_StructType* _global_StaticArray_StaticArray_S_Field_get_type(struct _global_StaticArray_StaticArray_S_Field self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_StructType* _global_StaticArray_StaticArray_S_Field_get_typeByValue(struct _global_StaticArray_StaticArray_S_Field self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_FieldType;}
struct _global_StructType {
struct _global_String name;
struct _global_String package;
struct bb real_type;
struct _global_StaticArray_StaticArray_S_Field fields;
};
static inline struct _global_StructType _global_StructTypeInit(struct _global_String name,struct _global_String package,struct bb real_type,struct _global_StaticArray_StaticArray_S_Field fields){
struct _global_StructType b;
b.name=name;b.package=package;b.real_type=real_type;b.fields=fields;return b;
};
struct _global_StructType _global_StructTypeType;struct _global_StructType* _global_StructType_get_type(struct _global_StructType self, struct _global_Context* c){return &_global_StructTypeType;}
struct _global_StructType* _global_StructType_get_typeByValue(struct _global_StructType self, struct _global_Context* c){return &_global_StructTypeType;}
struct _global_Maybe_Maybe_T_Some {
struct bb field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct bb b,struct _global_Context* c){
struct _global_Maybe_Maybe_T d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_Maybe_Maybe_T _global_None;

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
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* F);

struct _global_String _global_StructType_toString(struct _global_StructType*,struct _global_Context* F);




void _global_log_string(struct _global_String _global_s, struct _global_Context* G);

#define _global_exit(G,H) exit(G)
void _global_panic(struct _global_String _global_s, struct _global_Context* J){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),J),_global_StringInit(0,""),J),J);
_global_exit(1,J);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* J){;
;
if(!(_global_b)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),J),_global_StringInit(0,""),J),J);
;};
;}

#define _global_c_log(J,K) _global_c_log(J)

#define _global_memcpy(L,M,N,P) memcpy(L,M,N)

#define _global_c_alloc(Q,R) malloc(Q)

#define _global_c_free(S,T) free(S)
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* V){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,V),_global_maxSize);
;}
unsigned int _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* V){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* V){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){;
(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_log_string(_global_StringInit(48,"panic: used more temporary memory than available"),V);
_global_exit(1,V);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,V);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* V){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* V){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_panic(_global_StringInit(41,"used more temporary memory than available"),V);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* V){;
;
;return _global_c_alloc(_global_size,V);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* V){;
;
_global_c_free(_global_pointer,V);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* V){;
;return 0;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, unsigned int _global_to, struct _global_Context* V){;
;
;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator _global_malloc_as_allocator;void* _global_alloc(unsigned int _global_size, struct _global_Context* V){;
;return _global_Allocator_alloc((V)->allocator,_global_size,V);
;}
void _global_free(void* _global_p, struct _global_Context* V){;
_global_Allocator_dealloc((V)->allocator,_global_p,V);
;}

#define _global_char_buffer_toString(V,W) _runtime_char_buffer_toString(V)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* X){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* X){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* Y,struct _global_Context* X){
_global_Range_iteratorByValue(*Y,X);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T Z) {
struct _global_Maybe_uint Y;Y.tag = Z.tag;Y.cases = *(union _global_Maybe_uint_cases*) &(Z.cases);return Y;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* X){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){;
unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,X);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* X){;
;struct _global_FileAcess Y =_global_self;
if(Y.tag==0){return _global_StringInit(1,"r");}if(Y.tag==1){return _global_StringInit(1,"w");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* Z,struct _global_Context* X){
return _global_FileAcess_toStringByValue(*Z,X);
}
#define _global_c_open_file(X,Y,Z) _runtime_c_open_file(X,Y)

#define _global_c_close_file(bb,bc) _runtime_c_close_file(bb)

#define _global_c_read_file(bd,bf,bg) _runtime_read_file(bd,bf)
struct _global_String _global_File_readByValue(struct _global_File _global_self, struct _global_Context* bh){;
;struct _global_FileAcess bj =(_global_self).acess;
if(bj.tag==0){return _global_c_read_file((_global_self).c_file,bh,bh);}if(1){_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bh);
return _global_StringInit(0,"");};
;}
static inline struct _global_String _global_File_read(struct _global_File* bk,struct _global_Context* bh){
return _global_File_readByValue(*bk,bh);
}void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bh){;
_global_c_close_file((_global_self).c_file,bh);
;}
static inline void _global_File_free(struct _global_File* bj,struct _global_Context* bh){
_global_File_freeByValue(*bj,bh);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bl) {
struct _global_Maybe_File bk;bk.tag = bl.tag;bk.cases = *(union _global_Maybe_File_cases*) &(bl.cases);return bk;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bh){;
;
struct FILE* _global_c_file;_global_c_file = _global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bh),bh);;
;struct FILE* bj =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bh),bh);
if(bj != NULL){struct FILE* _global_file= bj;
return _global_Some_File(_global_FileInit(_global_file,_global_acess),bh);}if(bj == NULL){return tmp_globalc(_global_None);};
;}

#define _global_set_bit_to(bh,bj,bk,bl) _global_c_set_bit_to(bh,bj,bk)

#define _global_is_bit_set(bm,bn,bp) _global_c_is_bit_set(bm,bn)
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* bq){;
;return ((_global_self)->sign ? _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"i"),_global_uint_toStringByValue(((_global_self)->size*8),bq),bq),_global_StringInit(0,""),bq):(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"u"),_global_uint_toStringByValue(((_global_self)->size*8),bq),bq),_global_StringInit(0,""),bq)));
;}
static inline struct _global_String _global_IntType_toStringByValue(struct IntType br,struct _global_Context* bq){
return _global_IntType_toString(&br,bq);
}struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* bq){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"f"),_global_uint_toStringByValue(((_global_self)->size*8),bq),bq),_global_StringInit(0,""),bq);
;}
static inline struct _global_String _global_FloatType_toStringByValue(struct FloatType br,struct _global_Context* bq){
return _global_FloatType_toString(&br,bq);
}struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* bq){;
;return _global_StringInit(4,"bool");
;}
static inline struct _global_String _global_BoolType_toStringByValue(struct BoolType br,struct _global_Context* bq){
return _global_BoolType_toString(&br,bq);
}struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* bq){;
;return _global_StringInit(6,"string");
;}
static inline struct _global_String _global_StringType_toStringByValue(struct StringType br,struct _global_Context* bq){
return _global_StringType_toString(&br,bq);
}struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* bq){;
;return (_global_String_op_eqByValue((_global_self)->package,_global_StringInit(7,"_global"),bq) ? (_global_self)->name:(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bq),_global_StringInit(1,"."),bq),((_global_self)->name),bq),_global_StringInit(0,""),bq)));
;}
static inline struct _global_String _global_StructType_toStringByValue(struct _global_StructType br,struct _global_Context* bq){
return _global_StructType_toString(&br,bq);
}void _global_log_string(struct _global_String _global_s, struct _global_Context* bq){;
_global_c_log(_global_String_toString(&(_global_s),bq),bq);
;}

void _globalInit() { 
_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;_global_None.tag = 1;
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(100000,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&(_global_temporary_storage), &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&(_global_malloc), &_global_Malloc_get_occupied, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_reset_to);;
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

_global_init_c_runtime();
_globalInit();;
;
};
int main() { 
 ; 
_globalInit(); 
 mainInit(); return 0; };