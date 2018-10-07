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
struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc b;
return b;
};
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
struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range b;
b.start=start;b.end=end;return b;
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
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator b;
b.range=range;b.it=it;return b;
};
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
void _global_log_string(struct _global_String _global_s, struct _global_Context* z);

#define _global_exit(z,B) exit(z)
void _global_panic(struct _global_String _global_s, struct _global_Context* C){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),C),_global_StringInit(0,""),C),C);
_global_exit(1,C);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* C){;
;
if(!(_global_b)){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),C),_global_StringInit(0,""),C),C);
;};
;}

#define _global_c_log(C,D) _global_c_log(C)

#define _global_memcpy(F,G,H,J) memcpy(F,G,H)

#define _global_c_alloc(K,L) malloc(K)

#define _global_c_free(M,N) free(M)
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* P){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,P),_global_maxSize);
;}
unsigned int _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* P){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* P){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log_string(_global_StringInit(48,"panic: used more temporary memory than available"),P);
_global_exit(1,P);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,P);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* P){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* P){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){_global_panic(_global_StringInit(41,"used more temporary memory than available"),P);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* P){;
;
;return _global_c_alloc(_global_size,P);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* P){;
;
_global_c_free(_global_pointer,P);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* P){;
;return 0;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, unsigned int _global_to, struct _global_Context* P){;
;
;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator _global_malloc_as_allocator;void* _global_alloc(unsigned int _global_size, struct _global_Context* P){;
;return _global_Allocator_alloc((P)->allocator,_global_size,P);
;}
void _global_free(void* _global_p, struct _global_Context* P){;
_global_Allocator_dealloc((P)->allocator,_global_p,P);
;}

#define _global_char_buffer_toString(P,Q) _runtime_char_buffer_toString(P)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* R){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* R){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* S,struct _global_Context* R){
_global_Range_iteratorByValue(*S,R);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T T) {
struct _global_Maybe_uint S;S.tag = T.tag;S.cases = *(union _global_Maybe_uint_cases*) &(T.cases);return S;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* R){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,R);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* R){;
;struct _global_FileAcess S =_global_self;
if(S.tag==0){return _global_StringInit(1,"r");}if(S.tag==1){return _global_StringInit(1,"w");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* T,struct _global_Context* R){
return _global_FileAcess_toStringByValue(*T,R);
}
#define _global_c_open_file(R,S,T) _runtime_c_open_file(R,S)

#define _global_c_close_file(V,W) _runtime_c_close_file(V)

#define _global_c_read_file(X,Y,Z) _runtime_read_file(X,Y)
struct _global_String _global_File_readByValue(struct _global_File _global_self, struct _global_Context* bb){;
;struct _global_FileAcess bc =(_global_self).acess;
if(bc.tag==0){return _global_c_read_file((_global_self).c_file,bb,bb);}if(1){_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bb);
return _global_StringInit(0,"");};
;}
static inline struct _global_String _global_File_read(struct _global_File* bd,struct _global_Context* bb){
return _global_File_readByValue(*bd,bb);
}void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bb){;
_global_c_close_file((_global_self).c_file,bb);
;}
static inline void _global_File_free(struct _global_File* bc,struct _global_Context* bb){
_global_File_freeByValue(*bc,bb);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bf) {
struct _global_Maybe_File bd;bd.tag = bf.tag;bd.cases = *(union _global_Maybe_File_cases*) &(bf.cases);return bd;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bb){;
;
struct FILE* _global_c_file;_global_c_file = _global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bb),bb);;
;struct FILE* bc =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bb),bb);
if(bc != NULL){struct FILE* _global_file= bc;
return _global_Some_File(_global_FileInit(_global_file,_global_acess),bb);}if(bc == NULL){return tmp_globalc(_global_None);};
;}
void _global_log_string(struct _global_String _global_s, struct _global_Context* bb){;
_global_c_log(_global_String_toString(&(_global_s),bb),bb);
;}

void _globalInit() { 
_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;_global_None.tag = 1;
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(30000,(&_global_context));;
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
};