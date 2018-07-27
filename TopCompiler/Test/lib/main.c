typedef void*(*prmut_nonec_main_SizeTp___rnone)(void*,unsigned int,struct _global_Context*) ;
typedef void(*prmut_nonec_rnonep___none)(void*,void*,struct _global_Context*) ;
typedef void(*prmut_nonep___none)(void*,struct _global_Context*) ;
struct main_Allocator{
void* type; /* is always null, for now */ 
void* data;
prmut_nonec_main_SizeTp___rnone method_alloc;
prmut_nonec_rnonep___none method_dealloc;
prmut_nonep___none method_clear;
};static inline struct main_Allocator main_AllocatorFromStruct(void* data, prmut_nonec_main_SizeTp___rnone c, prmut_nonec_rnonep___none d, prmut_nonep___none f){ 
struct main_Allocator g;
g.data = data;g.method_alloc = c;
g.method_dealloc = d;
g.method_clear = f;
return g; 
}static inline void* main_Allocator_alloc(struct main_Allocator* g,unsigned int h,struct _global_Context* b){
return g->method_alloc(g->data,h,b);
};static inline void* main_Allocator_allocByValue(struct main_Allocator g,unsigned int h,struct _global_Context* b){
return g.method_alloc(g.data,h,b);
};static inline void main_Allocator_dealloc(struct main_Allocator* g,void* k,struct _global_Context* b){
return g->method_dealloc(g->data,k,b);
};static inline void main_Allocator_deallocByValue(struct main_Allocator g,void* k,struct _global_Context* b){
return g.method_dealloc(g.data,k,b);
};static inline void main_Allocator_clear(struct main_Allocator* g,struct _global_Context* b){
return g->method_clear(g->data,b);
};static inline void main_Allocator_clearByValue(struct main_Allocator g,struct _global_Context* b){
return g.method_clear(g.data,b);
};struct _global_Context {
struct main_Allocator allocator;struct main_Allocator longterm_storage;};
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

#define Context struct _global_Context* context
#define alloc main_Allocator_allocByValue

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

    printf("%p\n", memory);

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
    printf("%s", s.data);
};

static inline void* _global_offsetPtr(void* ptr, unsigned int offset, Context) {
    return ((char*)ptr) + offset;
}


#define main_c_alloc(c,d) malloc(c)

#define main_c_free(f,g) free(f)
struct main_TemporaryStorage {unsigned int occupied;void* data;unsigned int maxSize;};static inline struct main_TemporaryStorage main_TemporaryStorageInit(unsigned int occupied,void* data,unsigned int maxSize){struct main_TemporaryStorage h;h.occupied=occupied;h.data=data;h.maxSize=maxSize;return h;};struct main_TemporaryStorage main_new_TemporaryStorage(unsigned int main_maxSize, struct global_Context* c){;
_global_log(_global_StringInit(31,"calling new temporary storage\n"),c);
;return main_TemporaryStorageInit(0,main_c_alloc(main_maxSize,c),main_maxSize);}
void* main_TemporaryStorage_alloc(struct main_TemporaryStorage* main_self, unsigned int main_size, struct global_Context* c){;
;
_global_log(_global_StringInit(19,"calling allocator\n"),c);
(main_self)->data=_global_offsetPtr((main_self)->data,main_size,c);;
(main_self)->occupied=(main_self)->occupied+main_size;;
if((main_self)->occupied>=(main_self)->maxSize){_global_log(_global_StringInit(43,"used more temporary memory than available\n"),c);};
;return (main_self)->data;}
static inline void* main_TemporaryStorage_allocByValue(struct main_TemporaryStorage d,unsigned int f,struct _global_Context* c){
return main_TemporaryStorage_alloc(&d,f,c);
}void main_TemporaryStorage_dealloc(struct main_TemporaryStorage* main_self, void* main_p, struct global_Context* c){;
;}
static inline void main_TemporaryStorage_deallocByValue(struct main_TemporaryStorage d,void* f,struct _global_Context* c){
main_TemporaryStorage_dealloc(&d,f,c);
}void main_TemporaryStorage_resetTo(struct main_TemporaryStorage* main_self, unsigned int main_occupied, struct global_Context* c){;
;
(main_self)->data=_global_offsetPtr((main_self)->data,main_occupied-(main_self)->occupied,c);;
(main_self)->occupied=main_occupied;;
if((main_self)->occupied>=(main_self)->maxSize){_global_log(_global_StringInit(43,"used more temporary memory than available\n"),c);};}
static inline void main_TemporaryStorage_resetToByValue(struct main_TemporaryStorage d,unsigned int f,struct _global_Context* c){
main_TemporaryStorage_resetTo(&d,f,c);
}void main_TemporaryStorage_clear(struct main_TemporaryStorage* main_self, struct global_Context* c){;
main_TemporaryStorage_resetTo(main_self,0,c);}
static inline void main_TemporaryStorage_clearByValue(struct main_TemporaryStorage d,struct _global_Context* c){
main_TemporaryStorage_clear(&d,c);
}struct main_MallocWrapper {};static inline struct main_MallocWrapper main_MallocWrapperInit(){struct main_MallocWrapper c;return c;};void* main_MallocWrapper_alloc(struct main_MallocWrapper* main_self, unsigned int main_size, struct global_Context* c){;
;
;return main_c_alloc(main_size,c);}
static inline void* main_MallocWrapper_allocByValue(struct main_MallocWrapper d,unsigned int f,struct _global_Context* c){
return main_MallocWrapper_alloc(&d,f,c);
}void main_MallocWrapper_dealloc(struct main_MallocWrapper* main_self, void* main_pointer, struct global_Context* c){;
;
main_c_free(main_pointer,c);}
static inline void main_MallocWrapper_deallocByValue(struct main_MallocWrapper d,void* f,struct _global_Context* c){
main_MallocWrapper_dealloc(&d,f,c);
}void main_MallocWrapper_clear(struct main_MallocWrapper* main_self, struct global_Context* c){;}
static inline void main_MallocWrapper_clearByValue(struct main_MallocWrapper d,struct _global_Context* c){
main_MallocWrapper_clear(&d,c);
}struct main_TemporaryStorage main_temporary_storage;struct main_MallocWrapper main_mallocWrapper;
void mainInit() { 
struct _global_Context b;;
;
;
;
main_temporary_storage = main_new_TemporaryStorage(16384,(&b));;
main_mallocWrapper = main_MallocWrapperInit();;
(&b)->allocator = main_AllocatorFromStruct(&main_temporary_storage, &main_TemporaryStorage_alloc, &main_TemporaryStorage_dealloc, &main_TemporaryStorage_clear);
(&b)->longterm_storage = main_AllocatorFromStruct(&main_mallocWrapper, &main_MallocWrapper_alloc, &main_MallocWrapper_dealloc, &main_MallocWrapper_clear);
_global_log(_global_Uint_toStringByValue(10,(&b)),(&b));
;
};