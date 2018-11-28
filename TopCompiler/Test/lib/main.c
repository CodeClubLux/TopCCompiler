struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* b);

static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator**,struct _global_Allocator*,struct _global_Context* b);

struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator*,struct _global_Allocator*,struct _global_Context* b);
struct main_Slot_int* _global_Maybe_unwrap_rmain_Slot_int_ByValue(struct main_Slot_int* _global_self, struct _global_Context* c);

static inline struct main_Slot_int* _global_Maybe_unwrap_rmain_Slot_int_(struct main_Slot_int**,struct _global_Context* c);

struct main_Slot_int* _global_Maybe_unwrap_rmain_Slot_int_ByValue(struct main_Slot_int*,struct _global_Context* c);
void _global_Array_reserve_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, unsigned int _global_newSize, struct _global_Context* c);
void _global_Array_append_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, struct main_Slot_int _global_value, struct _global_Context* c);
struct main_Slot_int* _global_Array_op_get_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, unsigned int _global_index, struct _global_Context* c);
void _global_log_int(int _global_s, struct _global_Context* c);
struct main_BlockAllocator_int main_make_BlockAllocator_int_int(unsigned int main_num, struct _global_Context* c);
int* main_BlockAllocator_alloc_int(struct main_BlockAllocator_int* main_self, int main_obj, struct _global_Context* c);
void main_BlockAllocator_log_int(struct main_BlockAllocator_int* main_self, struct _global_Context* c);
void main_BlockAllocator_dealloc_int(struct main_BlockAllocator_int* main_self, int* main_obj, struct _global_Context* c);
struct main_BlockAllocator_int main_allocator;int* main_c;struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* c){;
;
;struct _global_Allocator* d =_global_self;
if(d != NULL){struct _global_Allocator* _global_x = d;
return _global_x;}else if(d == NULL){return _global_value;};
;}
static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator** f,struct _global_Allocator* g,struct _global_Context* c){
return _global_Maybe_default_rAllocatorByValue(*f,g,c);
}struct main_Slot_int* _global_Maybe_unwrap_rmain_Slot_int_ByValue(struct main_Slot_int* _global_self, struct _global_Context* c){;
struct main_Slot_int* _global_x;;
struct main_Slot_int* d =_global_self;if(d != NULL){_global_x = d;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),c);
;}
;
;return _global_x;
;}
static inline struct main_Slot_int* _global_Maybe_unwrap_rmain_Slot_int_(struct main_Slot_int** f,struct _global_Context* c){
return _global_Maybe_unwrap_rmain_Slot_int_ByValue(*f,c);
}
static inline struct main_Slot_int* tmpmainb(struct _global_Array_main_Slot_int_** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* c) {
struct main_Slot_int* d =(*_global_self)->data;
if(d != NULL){struct main_Slot_int* _global_data = d;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),c);
struct main_Slot_int* _global_newData;_global_newData = (struct main_Slot_int*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct main_Slot_int),c));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(struct main_Slot_int),c);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,c);
return _global_newData;}else if(d == NULL){return (struct main_Slot_int*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct main_Slot_int),c));}
}
void _global_Array_reserve_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, unsigned int _global_newSize, struct _global_Context* c){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(c)->allocator,c);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainb(&_global_self,&_global_newSize,&_global_allocator, c);;
;}
void _global_Array_append_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, struct main_Slot_int _global_value, struct _global_Context* c){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_main_Slot_int_(_global_self,1,c);
;}
else{_global_Array_reserve_main_Slot_int_(_global_self,(_global_self)->capacity*2,c);
;};
;};
*(((_global_Maybe_unwrap_rmain_Slot_int_ByValue((_global_self)->data,c) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
struct main_Slot_int* _global_Array_op_get_main_Slot_int_(struct _global_Array_main_Slot_int_* _global_self, unsigned int _global_index, struct _global_Context* c){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),c);
;return (_global_Maybe_unwrap_rmain_Slot_int_ByValue((_global_self)->data,c) + _global_index);
;}
void _global_log_int(int _global_s, struct _global_Context* c){;
_global_c_log(_global_int_toString(&(_global_s),c),c);
;}
struct _global_Array_main_Slot_int_ tmpmainc(struct _global_Array_Array_T d) {
return *((struct _global_Array_main_Slot_int_*) &d);};
static inline struct main_Slot_int tmpmaind(struct main_Slot_main_Slot_T j) {
struct main_Slot_int h;h.tag = j.tag;h.cases = *(union main_Slot_int_cases*) &(j.cases);return h;
}
struct main_BlockAllocator_int main_make_BlockAllocator_int_int(unsigned int main_num, struct _global_Context* c){;
_global_assert(main_num>0,_global_StringInit(50,"Minimum number of elements has to be bigger than 0"),c);
struct _global_Array_main_Slot_int_ main_slots;main_slots = tmpmainc(_global_empty_array(c));;
_global_Array_reserve_main_Slot_int_(&(main_slots),main_num,c);
struct _global_Range f =_global_RangeInit(0,main_num);
for (unsigned int g = f.start; g < f.end; g++) {
unsigned int main_i;main_i = g;
_global_Array_append_main_Slot_int_(&(main_slots),tmpmaind(main_Free_main_Slot_T(NULL,c)),c);
}
;
struct main_BlockAllocator_int main_allocator;main_allocator = main_BlockAllocator_intInit(main_slots,&(*(_global_Array_op_get_main_Slot_int_(&(main_slots),0,c))));;
struct _global_Range k =_global_RangeInit(0,(main_num-1));
for (unsigned int l = k.start; l < k.end; l++) {
unsigned int main_i;main_i = l;
*(_global_Array_op_get_main_Slot_int_(&(main_slots),main_i,c))=main_Free_int(&(*(_global_Array_op_get_main_Slot_int_(&(main_slots),main_i+1,c))),c);;
}
;
;return main_allocator;
;}
int* main_BlockAllocator_alloc_int(struct main_BlockAllocator_int* main_self, int main_obj, struct _global_Context* c){;
;
struct main_Slot_int* main_free_node;;
struct main_Slot_int* d =(main_self)->free_node;if(d != NULL){main_free_node = d;

;}
else if(1){
_global_panic(_global_StringInit(13,"Out of memory"),c);
;}
;
struct main_Slot_int* main_next_free_node;;
struct main_Slot_int f =*(main_free_node);if(f.tag==0){main_next_free_node = f.cases.Free.field0;

;}
else if(1){
_global_panic(_global_StringInit(39,"Node that was said to be free is active"),c);
;}
;
(main_self)->free_node=main_next_free_node;;
*(main_free_node)=main_Active_int(main_obj,c);;
;return (int*)main_free_node;
;}
void main_BlockAllocator_log_int(struct main_BlockAllocator_int* main_self, struct _global_Context* c){;
struct _global_Array_main_Slot_int_ d =(main_self)->slots;
for (unsigned int f = 0;f < d.length; f++) {
struct main_Slot_int main_slot;unsigned int main_i;main_slot = *_global_Array_op_get_main_Slot_int_(&d, f, c);
main_i = f;
int main_object;;
struct main_Slot_int g =main_slot;if(g.tag==1){main_object = g.cases.Active.field0;

;}
else if(1){
 continue;;
;}
;
_global_log_int(main_object,c);
}
;
;}
void main_BlockAllocator_dealloc_int(struct main_BlockAllocator_int* main_self, int* main_obj, struct _global_Context* c){;
;
struct main_Slot_int* main_slot;main_slot = (struct main_Slot_int*)main_obj;;
*(main_slot)=main_Free_int((main_self)->free_node,c);;
(main_self)->free_node=main_slot;;
;}

void mainInit() { printf("main\n");
main_Slot_intType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
main_Slot_intType.package = _global_StringInit(4, "main");
main_Slot_intType.name = _global_StringInit(8, "Slot_int");_global_Maybe_rmain_Slot_int_Type.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rmain_Slot_int_Type.package = _global_StringInit(7, "_global");
_global_Maybe_rmain_Slot_int_Type.name = _global_StringInit(21, "Maybe_rmain_Slot_int_");_global_Array_main_Slot_int_Type.size.tag = 1;
_global_Array_main_Slot_int_Type.array_type = 
_global_TypeFromStruct(
main_Slot_int_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
)
;main_BlockAllocator_intType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
main_BlockAllocator_intType.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_BlockAllocator_intType_fields
,2
);
main_BlockAllocator_intType.package = _global_StringInit(4, "main");
main_BlockAllocator_intType.name = _global_StringInit(18, "BlockAllocator_int");
main_BlockAllocator_intType_fields[0].name = _global_StringInit(5, "slots");
main_BlockAllocator_intType_fields[0].offset = offsetof(struct main_BlockAllocator_int, slots);
main_BlockAllocator_intType_fields[0].field_type = 
_global_TypeFromStruct(
_global_Array_main_Slot_int__get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;
main_BlockAllocator_intType_fields[1].name = _global_StringInit(9, "free_node");
main_BlockAllocator_intType_fields[1].offset = offsetof(struct main_BlockAllocator_int, free_node);
main_BlockAllocator_intType_fields[1].field_type = 
_global_TypeFromStruct(
_global_Maybe_rmain_Slot_int__get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
)
;main_Slot_main_Slot_TType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
main_Slot_main_Slot_TType.package = _global_StringInit(4, "main");
main_Slot_main_Slot_TType.name = _global_StringInit(16, "Slot_main_Slot_T");_global_Maybe_rmain_Slot_main_Slot_T_Type.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rmain_Slot_main_Slot_T_Type.package = _global_StringInit(7, "_global");
_global_Maybe_rmain_Slot_main_Slot_T_Type.name = _global_StringInit(29, "Maybe_rmain_Slot_main_Slot_T_");
main_allocator = main_make_BlockAllocator_int_int(10,(&_global_context));;
main_c = main_BlockAllocator_alloc_int(&(main_allocator),20,(&_global_context));;
main_BlockAllocator_log_int(&(main_allocator),(&_global_context));
main_BlockAllocator_dealloc_int(&(main_allocator),main_c,(&_global_context));
;
};