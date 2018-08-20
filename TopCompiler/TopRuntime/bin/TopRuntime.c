typedef void*(*prnonec_SizeTp___rnone)(void*,unsigned int,struct _global_Context*) ;
typedef void(*prnonec_rnonep___none)(void*,void*,struct _global_Context*) ;
typedef void(*prnonep___none)(void*,struct _global_Context*) ;
struct _global_Allocator {
void* type; /* is always null, for now */ 
void* data;
prnonec_SizeTp___rnone method_alloc;
prnonec_rnonep___none method_dealloc;
prnonep___none method_clear;
};static inline struct _global_Allocator _global_AllocatorFromStruct(void* data, prnonec_SizeTp___rnone c, prnonec_rnonep___none d, prnonep___none f){ 
struct _global_Allocator g;
g.data = data;g.method_alloc = c;
g.method_dealloc = d;
g.method_clear = f;
return g; 
}static inline void* _global_Allocator_alloc(struct _global_Allocator* g,unsigned int h,struct _global_Context* b){
return g->method_alloc(g->data,h,b);
};static inline void* _global_Allocator_allocByValue(struct _global_Allocator g,unsigned int h,struct _global_Context* b){
return g.method_alloc(g.data,h,b);
};static inline void _global_Allocator_dealloc(struct _global_Allocator* g,void* k,struct _global_Context* b){
return g->method_dealloc(g->data,k,b);
};static inline void _global_Allocator_deallocByValue(struct _global_Allocator g,void* k,struct _global_Context* b){
return g.method_dealloc(g.data,k,b);
};static inline void _global_Allocator_clear(struct _global_Allocator* g,struct _global_Context* b){
return g->method_clear(g->data,b);
};static inline void _global_Allocator_clearByValue(struct _global_Allocator g,struct _global_Context* b){
return g.method_clear(g.data,b);
};struct _global_Context {
struct _global_Allocator* allocator;struct _global_Allocator* longterm_storage;};
struct _global_Context _global_context;
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>

#define Context struct _global_Context* context
#define alloc _global_Allocator_alloc


struct _global_String {
    unsigned int length;
    char* data;
};

struct _global_String _global_StringInit(unsigned int length, char* data) {
    struct _global_String s;
    s.data = data;
    s.length = length;
    return s;
};
struct _global_String _global_String_toStringByValue(struct _global_String s, Context) {
    return s;
}

struct _global_String _global_String_toString(struct _global_String* s, Context) {
    return *s;
}

void _global_log(struct _global_String, Context);

struct _global_String _global_String_op_addByValue(struct _global_String a, struct _global_String b, Context) {
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

struct _global_String _global_String_op_add(struct _global_String* a, struct _global_String b, Context) {
    return _global_String_op_addByValue(*a, b, context);
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

struct _global_String _global_int_toStringByValue(int number, Context) {
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

struct _global_String _global_int_toString(int* number, Context) {
    return _global_int_toStringByValue(*number, context);
}

#define gen_integer(name, typ) struct _global_String _global_##name##_toString(typ* number, Context) {\
return _global_int_toStringByValue(*number, context); \
} \
struct _global_String _global_##name##_toStringByValue(typ number, Context) {\
return _global_int_toStringByValue(number, context); \
} \

gen_integer(uint, unsigned int)
gen_integer(u8, uint8_t)
gen_integer(u16, uint16_t)
gen_integer(u32, uint32_t)
gen_integer(u64, uint64_t)

gen_integer(i8, int8_t)
gen_integer(i16, int16_t)
gen_integer(i32, int32_t)
gen_integer(i64, int64_t)

void _global_c_log(struct _global_String s) {
    printf("%s\n", s.data);
};

static inline void* _global_offsetPtr(void* ptr, int offset, Context) {
    return ((char*)ptr) + offset;
};

/*
void printI(int i) {
    printf("%i\n", i);
};
*/


struct _global_Context _global_context;
struct _global_bb {
void* type; /* is always null, for now */ 
void* data;
};static inline struct _global_bb _global_bbFromStruct(void* data){ 
struct _global_bb c;
c.data = data;return c; 
}struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator** allocator;
struct _global_bb** data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator** allocator,struct _global_bb** data){
struct _global_Array_Array_T b;
b.length=length;b.capacity=capacity;b.allocator=allocator;b.data=data;return b;
};
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
struct _global_Maybe_Maybe_T_Some {
struct _global_bb field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct _global_bb b,struct _global_Context* c){
struct _global_Maybe_Maybe_T d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_Maybe_Maybe_T _global_None;

void _global_log_string(struct _global_String _global_s, struct _global_Context* b);
#include <string.h>
#define _global_memcpy(c,d,f,g) memcpy(c,d,f)

#define _global_c_alloc(h,j) malloc(h)

#define _global_c_free(k,l) free(k)
struct _global_TemporaryStorage {
unsigned int occupied;
unsigned int highest;
void* data;
unsigned int maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(unsigned int occupied,unsigned int highest,void* data,unsigned int maxSize){
struct _global_TemporaryStorage m;
m.occupied=occupied;m.highest=highest;m.data=data;m.maxSize=maxSize;return m;
};
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* c){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,c),_global_maxSize);}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log_string(_global_StringInit(41,"used more temporary memory than available"),c);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,c);}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* c){;
;}
void _global_TemporaryStorage_resetTo(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* c){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log_string(_global_StringInit(41,"used more temporary memory than available"),c);
;};}
void _global_TemporaryStorage_clear(struct _global_TemporaryStorage* _global_self, struct _global_Context* c){;
_global_TemporaryStorage_resetTo(_global_self,0,c);}
struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc c;
return c;
};
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
;return _global_c_alloc(_global_size,c);}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* c){;
;
_global_c_free(_global_pointer,c);}
void _global_Malloc_clear(struct _global_Malloc* _global_self, struct _global_Context* c){;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator _global_malloc_as_allocator;void* _global_alloc(unsigned int _global_size, struct _global_Context* c){;
;return _global_Allocator_alloc((c)->allocator,_global_size,c);}
void _global_free(void* _global_p, struct _global_Context* c){;
_global_Allocator_dealloc((c)->allocator,_global_p,c);}
void _global_panic(struct _global_String _global_s, struct _global_Context* c){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),c),_global_StringInit(0,""),c),c);}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c){;
;
if(!_global_b){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),c),_global_StringInit(0,""),c),c);
;};}

#define _global_c_log(c,d) _global_c_log(c)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* f){;return _global_Array_Array_TInit(0,0,NULL,NULL);}
struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range c;
c.start=start;c.end=end;return c;
};
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator c;
c.range=range;c.it=it;return c;
};
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* c){;
_global_RangeIteratorInit(_global_self,0);}
static inline void _global_Range_iterator(struct _global_Range* d,struct _global_Context* c){
_global_Range_iteratorByValue(*d,c);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T f) {
struct _global_Maybe_uint d;d.tag = f.tag;d.cases = *(union _global_Maybe_uint_cases*) &(f.cases);return d;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* c){;
struct _global_Range* _global_range;_global_range = &((_global_self)->range);;
;if((_global_self)->it<(_global_range)->end){unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,c);}
else{return tmp_globalb(_global_None);};}
void _global_log_string(struct _global_String _global_s, struct _global_Context* c){;
_global_c_log(_global_String_toString(&_global_s,c),c);}

void _globalInit() { 
_global_None.tag = 1;
;
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(32384,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&_global_temporary_storage, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_clear);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&_global_malloc, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_clear);;
(&_global_context)->allocator = &_global_temporary_storage_as_allocator;
(&_global_context)->longterm_storage = &_global_malloc_as_allocator;
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


void mainInit() { 

_globalInit();;
;
};
int main() { 
 ; 
_globalInit(); 
 mainInit(); return 0; };