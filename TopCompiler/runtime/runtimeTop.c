
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
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){(_global_self)->highest=(_global_self)->occupied;;};
if((_global_self)->occupied>=(_global_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"),c);};
;return _global_offsetPtr((_global_self)->data,(int)_global_occupied,c);}
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