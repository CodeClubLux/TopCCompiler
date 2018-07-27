
struct main_TemporaryStorage {int occupied;int size;};static inline struct main_TemporaryStorage main_TemporaryStorageInit(int occupied,int size){struct main_TemporaryStorage b;b.occupied=occupied;b.size=size;return b;};
#define main_c_alloc malloc

#define main_c_free free
struct main_MallocWrapper {};static inline struct main_MallocWrapper main_MallocWrapperInit(){struct main_MallocWrapper c;return c;};void* main_MallocWrapper_alloc(struct main_MallocWrapper* main_self, int main_size){;
;
;return main_c_alloc(main_size);}
static inline void* main_MallocWrapper_allocByValue(struct main_MallocWrapper c,int d){
return main_MallocWrapper_alloc(&c,d);
}void main_MallocWrapper_dealloc(struct main_MallocWrapper* main_self, void* main_pointer){;
;
main_c_free(main_pointer);}
static inline void main_MallocWrapper_deallocByValue(struct main_MallocWrapper c,void* d){
main_MallocWrapper_dealloc(&c,d);
}void main_MallocWrapper_clear(struct main_MallocWrapper* main_self){;}
static inline void main_MallocWrapper_clearByValue(struct main_MallocWrapper c){
main_MallocWrapper_clear(&c);
}
void mainInit() { 
;
;
;
;
;
;
_global_log(_global_StringInit(12,"hello world!"));
;
};