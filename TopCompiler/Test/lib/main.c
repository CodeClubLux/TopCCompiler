struct _global_Array_int {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
int* data;
};
static inline struct _global_Array_int _global_Array_intInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,int* data){
struct _global_Array_int b;
b.length=length;b.capacity=capacity;b.allocator=allocator;b.data=data;return b;
};
struct _global_StaticArray_6_int {
unsigned int length;
int data[6];
};
struct _global_StaticArray_6_int _global_StaticArray_6_intFill_array(unsigned int length, int with){
struct _global_StaticArray_6_int tmp;
tmp.length = 6;
for (unsigned int i = 0; i < 6; i++) {
tmp.data[i] = with;
}; return tmp; }
struct _global_StaticArray_6_int _global_StaticArray_6_intInit(int b,int c,int d,int f,int g,int h){
struct _global_StaticArray_6_int tmp;
tmp.length = 6;tmp.data[0] = b;
tmp.data[1] = c;
tmp.data[2] = d;
tmp.data[3] = f;
tmp.data[4] = g;
tmp.data[5] = h;
return tmp; }

struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* b);

static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator**,struct _global_Allocator*,struct _global_Context* b);
void _global_Array_reserve_int(struct _global_Array_int* _global_self, unsigned int _global_newSize, struct _global_Context* c);
int* _global_Maybe_unwrap_int_rintByValue(int* _global_self, struct _global_Context* c);

static inline int* _global_Maybe_unwrap_int_rint(int**,struct _global_Context* c);
int* _global_indexPtr_int(int* _global_pType, int _global_offset, struct _global_Context* c);
void _global_Array_append_int(struct _global_Array_int* _global_self, int _global_value, struct _global_Context* c);
struct _global_StaticArray_6_int* _global_box__6_int(struct _global_StaticArray_6_int _global_value, struct _global_Context* c);
int* _global_StaticArray_op_get_6_int(struct _global_StaticArray_6_int* _global_self, unsigned int _global_index, struct _global_Context* c);
void _global_log_int(int _global_s, struct _global_Context* c);
struct _global_Array_int main_dynamic_array;struct _global_Array_int tmpmainb(struct _global_Array_Array_T c) {
return *((struct _global_Array_int*) &c);};
struct _global_StaticArray_6_int* main_static_array;unsigned int main_i;struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* c){;
;
;struct _global_Allocator* d =_global_self;
if(d != NULL){struct _global_Allocator* _global_x= d;
return _global_x;}if(d == NULL){return _global_value;};}
static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator** f,struct _global_Allocator* g,struct _global_Context* c){
return _global_Maybe_default_rAllocatorByValue(*f,g,c);
}static inline int* tmpmainc(struct _global_Array_int** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* c) {
int* d =(*_global_self)->data;
if(d != NULL){int* _global_data= d;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),c);
int* _global_newData;_global_newData = (int*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(int),c));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(int),c);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,c);
return _global_newData;}if(d == NULL){return (int*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(int),c));}
}
void _global_Array_reserve_int(struct _global_Array_int* _global_self, unsigned int _global_newSize, struct _global_Context* c){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(c)->allocator,c);;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainc(&_global_self,&_global_newSize,&_global_allocator, c);;}
int* _global_Maybe_unwrap_int_rintByValue(int* _global_self, struct _global_Context* c){;
;int* d =_global_self;
if(d != NULL){int* _global_x= d;
return _global_x;}if(d == NULL){_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),c);
return *((int**)(_global_alloc(0,c)));};}
static inline int* _global_Maybe_unwrap_int_rint(int** f,struct _global_Context* c){
return _global_Maybe_unwrap_int_rintByValue(*f,c);
}int* _global_indexPtr_int(int* _global_pType, int _global_offset, struct _global_Context* c){;
;
;return (int*)(_global_offsetPtr((void*)_global_pType,_global_offset*sizeof(int),c));}
void _global_Array_append_int(struct _global_Array_int* _global_self, int _global_value, struct _global_Context* c){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){if((_global_self)->capacity==0){_global_Array_reserve_int(_global_self,1,c);
;}
else{_global_Array_reserve_int(_global_self,(_global_self)->capacity*2,c);
;};
;};
*(_global_indexPtr_int(_global_Maybe_unwrap_int_rintByValue((_global_self)->data,c),(_global_self)->length,c))=_global_value;;
(_global_self)->length=_global_newLength;;}
struct _global_StaticArray_6_int* _global_box__6_int(struct _global_StaticArray_6_int _global_value, struct _global_Context* c){;
struct _global_StaticArray_6_int* _global_pointer;_global_pointer = (struct _global_StaticArray_6_int*)(_global_Allocator_alloc((c)->allocator,sizeof(struct _global_StaticArray_6_int),c));;
*_global_pointer=_global_value;;
;return _global_pointer;}
int* _global_StaticArray_op_get_6_int(struct _global_StaticArray_6_int* _global_self, unsigned int _global_index, struct _global_Context* c){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),c);
;return _global_indexPtr_int((_global_self)->data,_global_index,c);}
void _global_log_int(int _global_s, struct _global_Context* c){;
_global_c_log(_global_int_toString(&_global_s,c),c);}

void mainInit() { 

main_dynamic_array = tmpmainb(_global_empty_array((&_global_context)));;;
_global_Array_append_int(&main_dynamic_array,10,(&_global_context));
main_static_array = _global_box__6_int(_global_StaticArray_6_intInit(0,1,2,3,-4,5),(&_global_context));;
main_i = 0;;
;while(main_i<(main_static_array)->length){*_global_StaticArray_op_get_6_int(main_static_array,main_i,(&_global_context))=10;;_global_log_int(*_global_StaticArray_op_get_6_int(main_static_array,main_i,(&_global_context)),(&_global_context));main_i=main_i+1;;};
;
};