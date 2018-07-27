
typedef void*(*prmut_nonec_main_SizeTp___rnone)(void*,unsigned int) ;
typedef void(*prmut_nonec_rnonep___none)(void*,void*) ;
typedef void(*prmut_nonep___none)(void*) ;
struct main_Allocator{
void* type; /* is always null, for now */ 
void* data;
prmut_nonec_main_SizeTp___rnone method_alloc;
prmut_nonec_rnonep___none method_dealloc;
prmut_nonep___none method_clear;
};static inline struct main_Allocator main_AllocatorFromStruct(void* data, prmut_nonec_main_SizeTp___rnone b, prmut_nonec_rnonep___none c, prmut_nonep___none d){ 
struct main_Allocator f;
f.data = data;f.method_alloc = b;
f.method_dealloc = c;
f.method_clear = d;
return f; 
}static inline void* main_Allocator_alloc(struct main_Allocator* f,unsigned int g){
return f->method_alloc(f->data,g);
};static inline void* main_Allocator_allocByValue(struct main_Allocator f,unsigned int g){
return f.method_alloc(f.data,g);
};static inline void main_Allocator_dealloc(struct main_Allocator* f,void* j){
return f->method_dealloc(f->data,j);
};static inline void main_Allocator_deallocByValue(struct main_Allocator f,void* j){
return f.method_dealloc(f.data,j);
};static inline void main_Allocator_clear(struct main_Allocator* f){
return f->method_clear(f->data);
};static inline void main_Allocator_clearByValue(struct main_Allocator f){
return f.method_clear(f.data);
};
#define main_c_alloc malloc

#define main_c_free free
struct main_TemporaryStorage {unsigned int occupied;void* data;unsigned int maxSize;};static inline struct main_TemporaryStorage main_TemporaryStorageInit(unsigned int occupied,void* data,unsigned int maxSize){struct main_TemporaryStorage c;c.occupied=occupied;c.data=data;c.maxSize=maxSize;return c;};struct main_TemporaryStorage main_new_TemporaryStorage(unsigned int main_maxSize){;
;return main_TemporaryStorageInit(0,main_c_alloc(main_maxSize),main_maxSize);}
void* main_TemporaryStorage_alloc(struct main_TemporaryStorage* main_self, unsigned int main_size){;
;
(main_self)->data=_global_offsetPtr((main_self)->data,main_size);;
(main_self)->occupied=(main_self)->occupied+main_size;;
if((main_self)->occupied<=(main_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"));};
;return (main_self)->data;}
static inline void* main_TemporaryStorage_allocByValue(struct main_TemporaryStorage c,unsigned int d){
return main_TemporaryStorage_alloc(&c,d);
}void main_TemporaryStorage_dealloc(struct main_TemporaryStorage* main_self, void* main_p){;
;}
static inline void main_TemporaryStorage_deallocByValue(struct main_TemporaryStorage c,void* d){
main_TemporaryStorage_dealloc(&c,d);
}void main_TemporaryStorage_resetTo(struct main_TemporaryStorage* main_self, unsigned int main_occupied){;
;
(main_self)->data=_global_offsetPtr((main_self)->data,main_occupied-(main_self)->occupied);;
(main_self)->occupied=main_occupied;;
if((main_self)->occupied<=(main_self)->maxSize){_global_log(_global_StringInit(41,"used more temporary memory than available"));};}
static inline void main_TemporaryStorage_resetToByValue(struct main_TemporaryStorage c,unsigned int d){
main_TemporaryStorage_resetTo(&c,d);
}void main_TemporaryStorage_clear(struct main_TemporaryStorage* main_self){;
main_TemporaryStorage_resetTo(main_self,0);}
static inline void main_TemporaryStorage_clearByValue(struct main_TemporaryStorage c){
main_TemporaryStorage_clear(&c);
}struct main_MallocWrapper {};static inline struct main_MallocWrapper main_MallocWrapperInit(){struct main_MallocWrapper c;return c;};void* main_MallocWrapper_alloc(struct main_MallocWrapper* main_self, unsigned int main_size){;
;
;return main_c_alloc(main_size);}
static inline void* main_MallocWrapper_allocByValue(struct main_MallocWrapper c,unsigned int d){
return main_MallocWrapper_alloc(&c,d);
}void main_MallocWrapper_dealloc(struct main_MallocWrapper* main_self, void* main_pointer){;
;
main_c_free(main_pointer);}
static inline void main_MallocWrapper_deallocByValue(struct main_MallocWrapper c,void* d){
main_MallocWrapper_dealloc(&c,d);
}void main_MallocWrapper_clear(struct main_MallocWrapper* main_self){;}
static inline void main_MallocWrapper_clearByValue(struct main_MallocWrapper c){
main_MallocWrapper_clear(&c);
}struct main_TemporaryStorage main_temporary_storage;struct main_MallocWrapper main_mallocWrapper;
void mainInit() { 
struct global_Context {
struct main_Allocator allocator;struct main_Allocator longterm_storage;};struct global_Context b;;
;
;
;
main_temporary_storage = main_new_TemporaryStorage(16384);;
main_mallocWrapper = main_MallocWrapperInit();;
(&b)->allocator = main_AllocatorFromStruct(&main_temporary_storage, &main_TemporaryStorage_alloc, &main_TemporaryStorage_dealloc, &main_TemporaryStorage_clear);
(&b)->longterm_storage = main_AllocatorFromStruct(&main_mallocWrapper, &main_MallocWrapper_alloc, &main_MallocWrapper_dealloc, &main_MallocWrapper_clear);
_global_log(_global_StringInit(12,"hello world!"));
;
};