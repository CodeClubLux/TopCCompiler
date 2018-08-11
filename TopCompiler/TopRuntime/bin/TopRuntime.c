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
struct _global_Allocator allocator;struct _global_Allocator longterm_storage;};
struct _global_Context _global_context;
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

#define Context struct _global_Context* context
#define alloc _global_Allocator_allocByValue

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

struct _global_String _global_Int_toStringByValue(int number, Context) {
    unsigned int length = 1;
    unsigned int divisor = 10;

    int absNumber = number;
    if (absNumber < 0) {
        absNumber *= -1;
    }

    while (number % divisor != absNumber) {
        length++;
        divisor *= 10;
    }

    if (number < 0) {
        length++;
    }

    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);

    struct _global_String newString = _global_StringInit(length, memory);

    itoa(number, newString.data, 10);
    _reverse_string(&newString);

    return newString;
}

struct _global_String _global_Uint_toStringByValue(unsigned int number, Context) {
    return _global_Int_toStringByValue(number, context);
}

struct _global_String _global_Int_toString(int* n, Context) {
    return _global_Int_toStringByValue(*n, context);
}

struct _global_String _global_Uint_toString(unsigned int* n, Context) {
    return _global_Int_toStringByValue(*n, context);
}

void _global_log(struct _global_String s, Context) {
    printf("%s\n", s.data);
};

static inline void* _global_offsetPtr(void* ptr, int offset, Context) {
    return ((char*)ptr) + offset;
}


struct _global_Context _global_context;

#include <string.h>
#define _global_memcpy(b,c,d,f) memcpy(b,c,d)

#define _global_c_alloc(g,h) malloc(g)

#define _global_c_free(j,k) free(j)
;
;
;
struct _global_TemporaryStorage {
unsigned int occupied;
unsigned int highest;
void* data;
unsigned int maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(unsigned int occupied,unsigned int highest,void* data,unsigned int maxSize){
struct _global_TemporaryStorage l;
l.occupied=occupied;l.highest=highest;l.data=data;l.maxSize=maxSize;return l;
};
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* c){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,c),_global_maxSize);}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
(_global_self)->occupied=_global_size;;
if((_global_self)->occupied>(_global_self)->highest){(_global_self)->highest=(_global_self)->occupied;;};
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"),c);};
;return _global_offsetPtr((_global_self)->data,(int)(_global_self)->occupied,c);}
static inline void* _global_TemporaryStorage_allocByValue(struct _global_TemporaryStorage d,unsigned int f,struct _global_Context* c){
return _global_TemporaryStorage_alloc(&d,f,c);
}void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* c){;
;}
static inline void _global_TemporaryStorage_deallocByValue(struct _global_TemporaryStorage d,void* f,struct _global_Context* c){
_global_TemporaryStorage_dealloc(&d,f,c);
}void _global_TemporaryStorage_resetTo(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* c){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"),c);};}
static inline void _global_TemporaryStorage_resetToByValue(struct _global_TemporaryStorage d,unsigned int f,struct _global_Context* c){
_global_TemporaryStorage_resetTo(&d,f,c);
}void _global_TemporaryStorage_clear(struct _global_TemporaryStorage* _global_self, struct _global_Context* c){;
_global_TemporaryStorage_resetTo(_global_self,0,c);}
static inline void _global_TemporaryStorage_clearByValue(struct _global_TemporaryStorage d,struct _global_Context* c){
_global_TemporaryStorage_clear(&d,c);
}struct _global_MallocWrapper {
};
static inline struct _global_MallocWrapper _global_MallocWrapperInit(){
struct _global_MallocWrapper c;
return c;
};
void* _global_MallocWrapper_alloc(struct _global_MallocWrapper* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
;return _global_c_alloc(_global_size,c);}
static inline void* _global_MallocWrapper_allocByValue(struct _global_MallocWrapper d,unsigned int f,struct _global_Context* c){
return _global_MallocWrapper_alloc(&d,f,c);
}void _global_MallocWrapper_dealloc(struct _global_MallocWrapper* _global_self, void* _global_pointer, struct _global_Context* c){;
;
_global_c_free(_global_pointer,c);}
static inline void _global_MallocWrapper_deallocByValue(struct _global_MallocWrapper d,void* f,struct _global_Context* c){
_global_MallocWrapper_dealloc(&d,f,c);
}void _global_MallocWrapper_clear(struct _global_MallocWrapper* _global_self, struct _global_Context* c){;}
static inline void _global_MallocWrapper_clearByValue(struct _global_MallocWrapper d,struct _global_Context* c){
_global_MallocWrapper_clear(&d,c);
}struct _global_TemporaryStorage _global_temporary_storage;struct _global_MallocWrapper _global_mallocWrapper;void _global_panic(struct _global_String _global_s, struct _global_Context* c){;
_global_log(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),c),_global_StringInit(0,""),c),c);}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c){;
;
if(!_global_b){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),c),_global_StringInit(0,""),c),c);};}

void _globalInit() { 

;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(16384,(&_global_context));;
_global_mallocWrapper = _global_MallocWrapperInit();;
(&_global_context)->allocator = _global_AllocatorFromStruct(&_global_temporary_storage, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_clear);
(&_global_context)->longterm_storage = _global_AllocatorFromStruct(&_global_mallocWrapper, &_global_MallocWrapper_alloc, &_global_MallocWrapper_dealloc, &_global_MallocWrapper_clear);
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
 mainInit(); return 0; };