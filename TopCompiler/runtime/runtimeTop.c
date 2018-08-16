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
struct _global_bb {
void* type; /* is always null, for now */ 
void* data;
};static inline struct _global_bb _global_bbFromStruct(void* data){ 
struct _global_bb c;
c.data = data;return c; 
}struct _global_Maybe_Maybe_T_Some {
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
;return _global_TemporaryStorageInit(0,0,0,0);}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"),c);
;};
;return _global_offsetPtr((_global_self)->data,(int)_global_occupied,c);}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* c){;
;}
void _global_TemporaryStorage_resetTo(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* c){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"),c);
;};}
void _global_TemporaryStorage_clear(struct _global_TemporaryStorage* _global_self, struct _global_Context* c){;
_global_TemporaryStorage_resetTo(_global_self,0,c);}
struct _global_MallocWrapper {
};
static inline struct _global_MallocWrapper _global_MallocWrapperInit(){
struct _global_MallocWrapper c;
return c;
};
void* _global_MallocWrapper_alloc(struct _global_MallocWrapper* _global_self, unsigned int _global_size, struct _global_Context* c){;
;
;return _global_c_alloc(_global_size,c);}
void _global_MallocWrapper_dealloc(struct _global_MallocWrapper* _global_self, void* _global_pointer, struct _global_Context* c){;
;
_global_c_free(_global_pointer,c);}
void _global_MallocWrapper_clear(struct _global_MallocWrapper* _global_self, struct _global_Context* c){;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_MallocWrapper _global_mallocWrapper;void* _global_alloc(unsigned int _global_size, struct _global_Context* c){;
;return _global_Allocator_allocByValue((c)->allocator,_global_size,c);}
void _global_free(void* _global_p, struct _global_Context* c){;
_global_Allocator_deallocByValue((c)->allocator,_global_p,c);}
void _global_panic(struct _global_String _global_s, struct _global_Context* c){;
_global_log(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),c),_global_StringInit(0,""),c),c);}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c){;
;
if(!_global_b){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),c),_global_StringInit(0,""),c),c);
;};}
struct _global_Range {
unsigned int start;
struct _global_Maybe_uint end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,struct _global_Maybe_uint end){
struct _global_Range c;
c.start=start;c.end=end;return c;
};
struct _global_RangeIterator {
struct _global_Range range;
unsigned int i;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int i){
struct _global_RangeIterator c;
c.range=range;c.i=i;return c;
};
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* c){;
_global_RangeIteratorInit(_global_self,0);}
static inline void _global_Range_iterator(struct _global_Range* d,struct _global_Context* c){
_global_Range_iteratorByValue(*d,c);
}static inline struct _global_Maybe_uint funcb(struct _global_RangeIterator** _global_self,struct _global_Range** _global_range, struct _global_Context* c) {
if(_global_Bool_op_ltByValue((_global_Some_uint((*_global_range)->start,c)),(*_global_range)->end,c)){unsigned int _global_tmp;_global_tmp = (*_global_self)->i;;
(*_global_self)->i=(*_global_self)->i+1;;
return _global_Some_uint(_global_tmp,c);}
else{return struct _global_Maybe_uint funcc(struct _global_Maybe_Maybe_T f) {
struct _global_Maybe_uint d;d.tag = f.tag;d.cases = *(union _global_Maybe_uint_cases*) &(f.cases);return d;
}
funcc(_global_None);}
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* c){;
struct _global_Range* _global_range;_global_range = &((_global_self)->range);;
;return funcb(&_global_self,&_global_range, c);}
struct _global_Range _global_range;struct _global_Maybe_uint funcd(struct _global_Maybe_Maybe_T d) {
struct _global_Maybe_uint c;c.tag = d.tag;c.cases = *(union _global_Maybe_uint_cases*) &(d.cases);return c;
}

void _globalInit() { 
_global_None.tag = 1;
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
;
_global_range = _global_RangeInit(0,funcd(_global_None));;
;
};