void _global_memcpy_rmain_Ball(struct main_Ball** _global_target, struct main_Ball** _global_destination, unsigned int _global_length, struct _global_Context* g);
struct main_Ball** _global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue(struct main_Ball** _global_self, struct _global_Context* g);

static inline struct main_Ball** _global_Maybe_unwrap_rMaybe_rmain_Ball_(struct main_Ball***,struct _global_Context* g);

struct main_Ball** _global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue(struct main_Ball**,struct _global_Context* g);
void _global_Array_reserve_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, unsigned int _global_newSize, struct _global_Context* g);
struct main_Ball** _global_Maybe_unwrap_rrmain_BallByValue(struct main_Ball** _global_self, struct _global_Context* g);

static inline struct main_Ball** _global_Maybe_unwrap_rrmain_Ball(struct main_Ball***,struct _global_Context* g);

struct main_Ball** _global_Maybe_unwrap_rrmain_BallByValue(struct main_Ball**,struct _global_Context* g);
void _global_memcpy_Maybe_rmain_Ball_(struct main_Ball** _global_target, struct main_Ball** _global_destination, unsigned int _global_length, struct _global_Context* g);
void _global_memcpy_ecs_Slot_main_Ball_(struct ecs_Slot_main_Ball* _global_target, struct ecs_Slot_main_Ball* _global_destination, unsigned int _global_length, struct _global_Context* g);
struct ecs_Slot_main_Ball* _global_Maybe_unwrap_recs_Slot_main_Ball_ByValue(struct ecs_Slot_main_Ball* _global_self, struct _global_Context* g);

static inline struct ecs_Slot_main_Ball* _global_Maybe_unwrap_recs_Slot_main_Ball_(struct ecs_Slot_main_Ball**,struct _global_Context* g);

struct ecs_Slot_main_Ball* _global_Maybe_unwrap_recs_Slot_main_Ball_ByValue(struct ecs_Slot_main_Ball*,struct _global_Context* g);
struct main_Ball* ecs_Store_index_active_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_i, struct _global_Context* g);
struct main_Ball* ecs_Store_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g);
struct main_Ball** _global_Array_op_get_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g);
struct ecs_Slot_main_Ball* _global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(struct _global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g);
void _global_Array_append_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, struct main_Ball* _global_value, struct _global_Context* g);
struct main_Ball** _global_Array_op_get_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, unsigned int _global_index, struct _global_Context* g);
void _global_Array_reserve_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, unsigned int _global_newSize, struct _global_Context* g);
void _global_Array_append_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, struct main_Ball* _global_value, struct _global_Context* g);
void _global_Array_reserve_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, unsigned int _global_newSize, struct _global_Context* g);
void _global_Array_append_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, struct ecs_Slot_main_Ball _global_value, struct _global_Context* g);
struct ecs_Slot_main_Ball* _global_Array_op_get_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g);
struct ecs_Store_main_Ball* _global_box_ecs_Store_main_Ball_(struct ecs_Store_main_Ball _global_value, struct _global_Context* g);
void ecs_Store_deserialize_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g);
struct _global_Type ecs_Store_get_component_type_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g);
void ecs_Store_make_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g);
void ecs_Store_render_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_layer_mask, struct _global_Context* g);
void ecs_Store_update_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_layer_mask, struct _global_Context* g);
void ecs_Store_free_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g);
struct _global_Maybe_ecs_Component ecs_Store_get_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g);
void ecs_Store_serialize_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g);
struct main_Ball* ecs_Store_register_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct main_Ball* ecs_obj_ptr, struct _global_Context* g);
struct ecs_Store_main_Ball* ecs_make_Store_main_Ball(pecs_IDp___rmain_Ball ecs_make_component, unsigned int ecs_max_number, struct _global_Context* g);
struct transform_Transform* _global_Maybe_unwrap_rtransform_TransformByValue(struct transform_Transform* _global_self, struct _global_Context* g);

static inline struct transform_Transform* _global_Maybe_unwrap_rtransform_Transform(struct transform_Transform**,struct _global_Context* g);

struct transform_Transform* _global_Maybe_unwrap_rtransform_TransformByValue(struct transform_Transform*,struct _global_Context* g);
struct main_Ball* ecs_Store_add_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct main_Ball ecs_comp, struct _global_Context* g);
struct ecs_Entity* main_Ball_get_entity(struct main_Ball* main_self, struct _global_Context* g){;
;return transform_Transform_get_entity((main_self)->trans,g);
;}
void main_Ball_render(struct main_Ball* main_self, struct _global_Context* g){;
;}
void main_Ball_update(struct main_Ball* main_self, struct _global_Context* g){;
float main_vertical;main_vertical = input_get_vertical_axis(g);;
float main_horizontal;main_horizontal = input_get_horizontal_axis(g);;
(((main_self)->trans)->position).z=main_vertical*(main_self)->speed*time_get_delta_time(g);;
(((main_self)->trans)->position).x=main_horizontal*(main_self)->speed*time_get_delta_time(g);;
;}
struct ecs_Store_main_Ball* main_ball_system;struct main_Ball* main_make_Ball(unsigned int main_id, struct _global_Context* g){;
;return ecs_Store_add_component_main_Ball(main_ball_system,main_BallInit(_global_Maybe_unwrap_rtransform_TransformByValue((ecs_Store_component_by_id_transform_Transform(transform_transform_system,main_id,g)),g),10.0),g);
;}
void _global_memcpy_rmain_Ball(struct main_Ball** _global_target, struct main_Ball** _global_destination, unsigned int _global_length, struct _global_Context* g){;
;
;
_global_c_memcpy((void*)_global_target,(void*)_global_destination,(uint64_t)_global_length*sizeof(struct main_Ball*),g);
;}
struct main_Ball** _global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue(struct main_Ball** _global_self, struct _global_Context* g){;
struct main_Ball** _global_x;;
struct main_Ball** h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct main_Ball** _global_Maybe_unwrap_rMaybe_rmain_Ball_(struct main_Ball*** j,struct _global_Context* g){
return _global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue(*j,g);
}
static inline struct main_Ball** tmpmainb(struct _global_Array_rmain_Ball** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
struct main_Ball** h =(*_global_self)->data;
if(h != NULL){struct main_Ball** _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
struct main_Ball** _global_newData;_global_newData = (struct main_Ball**)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct main_Ball*),g));;
_global_memcpy_rmain_Ball(_global_newData,_global_data,(*_global_self)->length,g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (struct main_Ball**)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct main_Ball*),g));}
}
void _global_Array_reserve_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainb(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
struct main_Ball** _global_Maybe_unwrap_rrmain_BallByValue(struct main_Ball** _global_self, struct _global_Context* g){;
struct main_Ball** _global_x;;
struct main_Ball** h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct main_Ball** _global_Maybe_unwrap_rrmain_Ball(struct main_Ball*** j,struct _global_Context* g){
return _global_Maybe_unwrap_rrmain_BallByValue(*j,g);
}void _global_memcpy_Maybe_rmain_Ball_(struct main_Ball** _global_target, struct main_Ball** _global_destination, unsigned int _global_length, struct _global_Context* g){;
;
;
_global_c_memcpy((void*)_global_target,(void*)_global_destination,(uint64_t)_global_length*sizeof(struct main_Ball*),g);
;}
void _global_memcpy_ecs_Slot_main_Ball_(struct ecs_Slot_main_Ball* _global_target, struct ecs_Slot_main_Ball* _global_destination, unsigned int _global_length, struct _global_Context* g){;
;
;
_global_c_memcpy((void*)_global_target,(void*)_global_destination,(uint64_t)_global_length*sizeof(struct ecs_Slot_main_Ball),g);
;}
struct ecs_Slot_main_Ball* _global_Maybe_unwrap_recs_Slot_main_Ball_ByValue(struct ecs_Slot_main_Ball* _global_self, struct _global_Context* g){;
struct ecs_Slot_main_Ball* _global_x;;
struct ecs_Slot_main_Ball* h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct ecs_Slot_main_Ball* _global_Maybe_unwrap_recs_Slot_main_Ball_(struct ecs_Slot_main_Ball** j,struct _global_Context* g){
return _global_Maybe_unwrap_recs_Slot_main_Ball_ByValue(*j,g);
}struct main_Ball* ecs_Store_index_active_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_i, struct _global_Context* g){;
;
struct main_Ball ecs_hey;;
struct ecs_Slot_main_Ball h =*(_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&((ecs_self)->components),ecs_i,g));if(h.tag==1){ecs_hey = h.cases.Active.field0;

;}
else if(1){
return NULL;
;
;}
;
struct main_Ball* ecs_comp;ecs_comp = (struct main_Ball*)(&(*(_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&((ecs_self)->components),ecs_i,g))));;
if(!((main_Ball_get_entity(ecs_comp,g))->enabled)){;
return NULL;
;
;};
;return ecs_comp;
;}
struct main_Ball* ecs_Store_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g){;
;
if(ecs_id>=((ecs_self)->id_to_obj).length){;
return NULL;
;
;};
;return *(_global_Array_op_get_Maybe_rmain_Ball_(&((ecs_self)->id_to_obj),ecs_id,g));
;}
struct main_Ball** _global_Array_op_get_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return (_global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue((_global_self)->data,g) + _global_index);
;}
struct ecs_Slot_main_Ball* _global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(struct _global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + _global_index);
;}
void _global_Array_append_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, struct main_Ball* _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_rmain_Ball(_global_self,1,g);
;}
else{_global_Array_reserve_rmain_Ball(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_rrmain_BallByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
struct main_Ball** _global_Array_op_get_rmain_Ball(struct _global_Array_rmain_Ball* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return (_global_Maybe_unwrap_rrmain_BallByValue((_global_self)->data,g) + _global_index);
;}

static inline struct main_Ball** tmpmainc(struct _global_Array_Maybe_rmain_Ball_** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
struct main_Ball** h =(*_global_self)->data;
if(h != NULL){struct main_Ball** _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
struct main_Ball** _global_newData;_global_newData = (struct main_Ball**)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct main_Ball*),g));;
_global_memcpy_Maybe_rmain_Ball_(_global_newData,_global_data,(*_global_self)->length,g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (struct main_Ball**)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct main_Ball*),g));}
}
void _global_Array_reserve_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainc(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
void _global_Array_append_Maybe_rmain_Ball_(struct _global_Array_Maybe_rmain_Ball_* _global_self, struct main_Ball* _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_Maybe_rmain_Ball_(_global_self,1,g);
;}
else{_global_Array_reserve_Maybe_rmain_Ball_(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_rMaybe_rmain_Ball_ByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}

static inline struct ecs_Slot_main_Ball* tmpmaind(struct _global_Array_ecs_Slot_main_Ball_** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
struct ecs_Slot_main_Ball* h =(*_global_self)->data;
if(h != NULL){struct ecs_Slot_main_Ball* _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
struct ecs_Slot_main_Ball* _global_newData;_global_newData = (struct ecs_Slot_main_Ball*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct ecs_Slot_main_Ball),g));;
_global_memcpy_ecs_Slot_main_Ball_(_global_newData,_global_data,(*_global_self)->length,g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (struct ecs_Slot_main_Ball*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct ecs_Slot_main_Ball),g));}
}
void _global_Array_reserve_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmaind(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
void _global_Array_append_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, struct ecs_Slot_main_Ball _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_ecs_Slot_main_Ball_(_global_self,1,g);
;}
else{_global_Array_reserve_ecs_Slot_main_Ball_(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_recs_Slot_main_Ball_ByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
struct ecs_Slot_main_Ball* _global_Array_op_get_ecs_Slot_main_Ball_(struct _global_Array_ecs_Slot_main_Ball_* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return (_global_Maybe_unwrap_recs_Slot_main_Ball_ByValue((_global_self)->data,g) + _global_index);
;}
struct ecs_Store_main_Ball* _global_box_ecs_Store_main_Ball_(struct ecs_Store_main_Ball _global_value, struct _global_Context* g){;
struct ecs_Store_main_Ball* _global_pointer;_global_pointer = (struct ecs_Store_main_Ball*)(_global_Allocator_alloc((g)->allocator,(uint64_t)sizeof(struct ecs_Store_main_Ball),g));;
*(_global_pointer)=_global_value;;
;return _global_pointer;
;}
void ecs_Store_deserialize_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g){;
return ;
;
struct _global_Context ecs_new_context;ecs_new_context = *(g);;
(ecs_new_context).allocator=(ecs_new_context).longterm_storage;;
struct _global_File ecs_f;;
struct _global_Maybe_File h =_global_open(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"assets\\save_files\\"),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),&ecs_new_context),&ecs_new_context),_global_StringInit(4,".tsf"),&ecs_new_context),_global_ReadFile,&ecs_new_context);if(h.tag==0){ecs_f = h.cases.Some.field0;

;}
else if(1){
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(26,"Could not read save_files\\"),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),&ecs_new_context),&ecs_new_context),_global_StringInit(0,""),&ecs_new_context),&ecs_new_context);
;}
;
struct sBuffer_Buffer ecs_read_buffer;ecs_read_buffer = sBuffer_make_read_Buffer(_global_File_read(&(ecs_f),&ecs_new_context),&ecs_new_context);;
uint32_t ecs_num;ecs_num = sBuffer_Buffer_read_integer(&(ecs_read_buffer),&ecs_new_context);;
struct _global_Range j =_global_RangeInit(0,ecs_num);
for (unsigned int k = j.start; k < j.end; k++) {
unsigned int ecs_i;ecs_i = k;
struct main_Ball ecs_comp;;
sBuffer_Buffer_read_object(&(ecs_read_buffer),_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size),(void*)&(ecs_comp),&ecs_new_context);
ecs_Store_add_component_main_Ball(ecs_self,ecs_comp,&ecs_new_context);
}
;
_global_File_freeByValue(ecs_f,&ecs_new_context);
;
;}
struct _global_Type ecs_Store_get_component_type_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g){;
;return _global_TypeFromStruct(main_Ball_get_type(NULL,g),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size);
;}
void ecs_Store_make_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g){;
;
(ecs_self)->make_component_func(ecs_id,g);
;}
void ecs_Store_render_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_layer_mask, struct _global_Context* g){;
;
struct _global_Range h =_global_RangeInit(0,((ecs_self)->components).length);
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int ecs_i;ecs_i = j;
struct main_Ball* ecs_comp;;
struct main_Ball* k =ecs_Store_index_active_main_Ball(ecs_self,ecs_i,g);if(k != NULL){ecs_comp = k;

;}
else if(1){
 continue;;
;}
;
if(!(layermask_mask((main_Ball_get_entity(ecs_comp,g))->layermask,ecs_layer_mask,g))){;
main_Ball_render(ecs_comp,g);
;};
}
;
;}
void ecs_Store_update_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_layer_mask, struct _global_Context* g){;
;
struct _global_Range h =_global_RangeInit(0,((ecs_self)->components).length);
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int ecs_i;ecs_i = j;
struct main_Ball* ecs_comp;;
struct main_Ball* k =ecs_Store_index_active_main_Ball(ecs_self,ecs_i,g);if(k != NULL){ecs_comp = k;

;}
else if(1){
 continue;;
;}
;
if(!(layermask_mask((main_Ball_get_entity(ecs_comp,g))->layermask,ecs_layer_mask,g))){;
main_Ball_update(ecs_comp,g);
;};
}
;
;}
void ecs_Store_free_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g){;
;
struct main_Ball* h =ecs_Store_component_by_id_main_Ball(ecs_self,ecs_id,g);if(h != NULL){struct main_Ball* ecs_obj_ptr = h;

*(_global_Array_op_get_Maybe_rmain_Ball_(&((ecs_self)->id_to_obj),ecs_id,g))=NULL;;
struct ecs_Slot_main_Ball* ecs_slot;ecs_slot = (struct ecs_Slot_main_Ball*)ecs_obj_ptr;;
*(ecs_slot)=ecs_Free_main_Ball((ecs_self)->free_node,g);;
(ecs_self)->free_node=ecs_slot;;
;}
else if(h == NULL){
;}
;
;}
struct ecs_Component_VTABLE rmain_Ball_VTABLE_FOR_ecs_Component;static inline struct _global_Maybe_ecs_Component tmpmainf(struct _global_Maybe_Maybe_T k) {
struct _global_Maybe_ecs_Component j;j.tag = k.tag;j.cases = *(union _global_Maybe_ecs_Component_cases*) &(k.cases);return j;
}
struct _global_Maybe_ecs_Component ecs_Store_get_component_by_id_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct _global_Context* g){;
;
;struct main_Ball* h =ecs_Store_component_by_id_main_Ball(ecs_self,ecs_id,g);
if(h != NULL){struct main_Ball* ecs_ptr = h;
return _global_Some_ecs_Component(ecs_ComponentFromStruct(ecs_ptr,&rmain_Ball_VTABLE_FOR_ecs_Component,_global_TypeFromStruct(main_Ball_get_type(NULL,g),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &main_Ball_get_entity, &main_Ball_render, &main_Ball_update),g);}else if(h == NULL){return tmpmainf(_global_None);};
;}
void ecs_Store_serialize_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct _global_Context* g){;
struct _global_Context ecs_new_context;ecs_new_context = *(g);;
(ecs_new_context).allocator=(ecs_new_context).longterm_storage;;
struct _global_Allocator* h = (ecs_new_context).allocator;
uint64_t j = _global_Allocator_get_occupied((ecs_new_context).allocator,g);
;
struct _global_Array_rmain_Ball ecs_comps;ecs_comps = _global_Array_rmain_BallInit(0, 0, NULL, NULL);;
unsigned int ecs_serialize_layermask;ecs_serialize_layermask = layermask_make_Layermask(&ecs_new_context);;
ecs_serialize_layermask=layermask_enable(ecs_serialize_layermask,layermask_serialize_layer,&ecs_new_context);;
struct _global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_ k =(ecs_self)->components;
for (unsigned int l = 0;l < k.length; l++) {
struct ecs_Slot_main_Ball ecs_slot;unsigned int ecs_i;ecs_slot = *_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&k, l, &ecs_new_context);
ecs_i = l;
;
struct ecs_Slot_main_Ball m =*(_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&((ecs_self)->components),ecs_i,&ecs_new_context));if(m.tag==1&&1){
;}
else if(1){
 continue;;
;}
;
struct main_Ball* ecs_comp;ecs_comp = (struct main_Ball*)(&(*(_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&((ecs_self)->components),ecs_i,&ecs_new_context))));;
if(!(layermask_mask((main_Ball_get_entity(ecs_comp,&ecs_new_context))->layermask,ecs_serialize_layermask,&ecs_new_context))){;
_global_Array_append_rmain_Ball(&(ecs_comps),(struct main_Ball*)(&(*(_global_StaticArray_op_get_StaticArray_S_ecs_Slot_main_Ball_(&((ecs_self)->components),ecs_i,&ecs_new_context)))),&ecs_new_context);
;};
}
;
struct sBuffer_Buffer ecs_write_buffer;ecs_write_buffer = (sBuffer_make_write_Buffer(10000000,&ecs_new_context));;
sBuffer_Buffer_write_integer(&(ecs_write_buffer),(ecs_comps).length,&ecs_new_context);
if((ecs_comps).length>0){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(12,"serialized: "),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),&ecs_new_context),&ecs_new_context),_global_StringInit(0,""),&ecs_new_context),&ecs_new_context);
;}
else{_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(19,"did not serialize: "),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),&ecs_new_context),&ecs_new_context),_global_StringInit(0,""),&ecs_new_context),&ecs_new_context);
;};
struct _global_Array_rmain_Ball n =ecs_comps;
for (unsigned int p = 0;p < n.length; p++) {
struct main_Ball* ecs_comp;unsigned int ecs_i;ecs_comp = *_global_Array_op_get_rmain_Ball(&n, p, &ecs_new_context);
ecs_i = p;
_global_log_string(_global_StringInit(5,"====="),&ecs_new_context);
sBuffer_Buffer_write_object(&(ecs_write_buffer),_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size),(void*)ecs_comp,&ecs_new_context);
}
;
struct _global_File ecs_f;;
struct _global_Maybe_File q =_global_open(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"assets\\save_files\\"),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,&ecs_new_context),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),&ecs_new_context),&ecs_new_context),_global_StringInit(4,".tsf"),&ecs_new_context),_global_WriteFile,&ecs_new_context);if(q.tag==0){ecs_f = q.cases.Some.field0;

;}
else if(1){
_global_panic(_global_StringInit(29,"Could not write to save_files"),&ecs_new_context);
;}
;
_global_File_write(&(ecs_f),sBuffer_Buffer_string_buffer(&(ecs_write_buffer),&ecs_new_context),&ecs_new_context);
_global_File_freeByValue(ecs_f,&ecs_new_context);
;
_global_Allocator_reset_to(h,j,g);
;}
struct main_Ball* ecs_Store_register_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, unsigned int ecs_id, struct main_Ball* ecs_obj_ptr, struct _global_Context* g){;
;
;
if(ecs_id>=((ecs_self)->id_to_obj).length){;
_global_Array_reserve_Maybe_rmain_Ball_(&((ecs_self)->id_to_obj),ecs_id+1,g);
struct _global_Range h =_global_RangeInit(((ecs_self)->id_to_obj).length,(ecs_id+1));
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int ecs_i;ecs_i = j;
_global_Array_append_Maybe_rmain_Ball_(&((ecs_self)->id_to_obj),NULL,g);
}
;
;};
*(_global_Array_op_get_Maybe_rmain_Ball_(&((ecs_self)->id_to_obj),ecs_id,g))=ecs_obj_ptr;;
;return ecs_obj_ptr;
;}
static inline struct ecs_Slot_main_Ball tmpmaing(struct ecs_Slot_ecs_Slot_T l) {
struct ecs_Slot_main_Ball k;k.tag = l.tag;k.cases = *(union ecs_Slot_main_Ball_cases*) &(l.cases);return k;
}
struct ecs_System_VTABLE recs_Store_main_Ball__VTABLE_FOR_ecs_System;struct ecs_Store_main_Ball* ecs_make_Store_main_Ball(pecs_IDp___rmain_Ball ecs_make_component, unsigned int ecs_max_number, struct _global_Context* g){;
;
_global_assert(ecs_max_number>0,_global_StringInit(50,"Minimum number of elements has to be bigger than 0"),g);
struct _global_Array_Maybe_rmain_Ball_ ecs_id_to_key;ecs_id_to_key = _global_Array_Maybe_rmain_Ball_Init(0, 0, NULL, NULL);;
(ecs_id_to_key).allocator=(g)->longterm_storage;;
struct _global_Array_ecs_Slot_main_Ball_ ecs_slots;ecs_slots = _global_Array_ecs_Slot_main_Ball_Init(0, 0, NULL, NULL);;
_global_Array_reserve_ecs_Slot_main_Ball_(&(ecs_slots),ecs_max_number,g);
struct _global_Range h =_global_RangeInit(0,ecs_max_number);
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int ecs_i;ecs_i = j;
_global_Array_append_ecs_Slot_main_Ball_(&(ecs_slots),tmpmaing(ecs_Free_ecs_Slot_T(NULL,g)),g);
}
;
struct _global_Range m =_global_RangeInit(0,ecs_max_number-1);
for (unsigned int n = m.start; n < m.end; n++) {
unsigned int ecs_i;ecs_i = n;
*(_global_Array_op_get_ecs_Slot_main_Ball_(&(ecs_slots),ecs_i,g))=ecs_Free_main_Ball(&(*(_global_Array_op_get_ecs_Slot_main_Ball_(&(ecs_slots),ecs_i+1,g))),g);;
}
;
struct ecs_Store_main_Ball* ecs_self;ecs_self = _global_box_ecs_Store_main_Ball_(ecs_Store_main_BallInit(ecs_make_component,ecs_id_to_key,_global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_Init(ecs_slots.data, ecs_slots.length),&(*(_global_Array_op_get_ecs_Slot_main_Ball_(&(ecs_slots),0,g))),ecs_max_number,0),g);;
ecs_Store_deserialize_main_Ball(ecs_self,g);
_global_Array_append_ecs_System(&(ecs_component_types),ecs_SystemFromStruct(ecs_self,&recs_Store_main_Ball__VTABLE_FOR_ecs_System,_global_TypeFromStruct(ecs_Store_main_Ball_get_type(NULL,g),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &ecs_Store_get_component_type_main_Ball, &ecs_Store_make_component_main_Ball, &ecs_Store_render_main_Ball, &ecs_Store_update_main_Ball, &ecs_Store_free_component_by_id_main_Ball, &ecs_Store_get_component_by_id_main_Ball, &ecs_Store_serialize_main_Ball),g);
;return ecs_self;
;}
struct transform_Transform* _global_Maybe_unwrap_rtransform_TransformByValue(struct transform_Transform* _global_self, struct _global_Context* g){;
struct transform_Transform* _global_x;;
struct transform_Transform* h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct transform_Transform* _global_Maybe_unwrap_rtransform_Transform(struct transform_Transform** j,struct _global_Context* g){
return _global_Maybe_unwrap_rtransform_TransformByValue(*j,g);
}struct main_Ball* ecs_Store_add_component_main_Ball(struct ecs_Store_main_Ball* ecs_self, struct main_Ball ecs_comp, struct _global_Context* g){;
;
unsigned int ecs_id;ecs_id = ((main_Ball_get_entity(&(ecs_comp),g)))->id;;
struct ecs_Slot_main_Ball* ecs_free_node;;
struct ecs_Slot_main_Ball* h =(ecs_self)->free_node;if(h != NULL){ecs_free_node = h;

;}
else if(1){
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(26,"Out of memory for system: "),_global_Type_toStringByValue((_global_TypeFromStruct(main_Ball_get_type(NULL,g),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size)),g),g),_global_StringInit(0,""),g),g);
;}
;
struct ecs_Slot_main_Ball* ecs_next_free_node;;
struct ecs_Slot_main_Ball j =*(ecs_free_node);if(j.tag==0){ecs_next_free_node = j.cases.Free.field0;

;}
else if(1){
_global_panic(_global_StringInit(39,"Node that was said to be free is active"),g);
;}
;
(ecs_self)->free_node=ecs_next_free_node;;
*(ecs_free_node)=ecs_Active_main_Ball(ecs_comp,g);;
struct main_Ball* ecs_obj_ptr;ecs_obj_ptr = (struct main_Ball*)ecs_free_node;;
(ecs_self)->added=(ecs_self)->added+1;;
;return ecs_Store_register_component_main_Ball(ecs_self,ecs_id,ecs_obj_ptr,g);
;}

void mainInitTypes() { 
 runnerInitTypes();taskInitTypes();syncInitTypes();syncInitTypes();atomicInitTypes();atomicInitTypes();queueInitTypes();queueInitTypes();
main_BallType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
main_BallType.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_BallType_fields
,2
);
main_BallType.package = _global_StringInit(4, "main");
main_BallType.name = _global_StringInit(4, "Ball");
main_BallType.size = sizeof(struct main_Ball);
main_BallType_fields[0].name = _global_StringInit(5, "trans");
main_BallType_fields[0].offset = offsetof(struct main_Ball, trans);
main_BallType_fields[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
transform_Transform_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;
main_BallType_fields[1].name = _global_StringInit(5, "speed");
main_BallType_fields[1].offset = offsetof(struct main_Ball, speed);
main_BallType_fields[1].field_type = 
_global_TypeFromStruct(
_global_Float_get_type(NULL,(&_global_context))
,
&rFloatType_VTABLE_FOR_Type
,
rFloatType_VTABLE_FOR_Type.type
, &_global_FloatType_toString
, &_global_FloatType_get_size
)
;_global_Maybe_rmain_BallType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rmain_BallType.package = _global_StringInit(7, "_global");
_global_Maybe_rmain_BallType.name = _global_StringInit(16, "Maybe_rmain_Ball");_global_Maybe_rMaybe_rmain_Ball_Type.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rMaybe_rmain_Ball_Type.package = _global_StringInit(7, "_global");
_global_Maybe_rMaybe_rmain_Ball_Type.name = _global_StringInit(24, "Maybe_rMaybe_rmain_Ball_");_global_Maybe_rrmain_BallType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rrmain_BallType.package = _global_StringInit(7, "_global");
_global_Maybe_rrmain_BallType.name = _global_StringInit(17, "Maybe_rrmain_Ball");_global_Array_rmain_BallType.size.tag = 1;
_global_Array_rmain_BallType.array_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
main_Ball_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
, &_global_PointerType_get_size
)
;ecs_Slot_main_BallType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
ecs_Slot_main_BallType.package = _global_StringInit(3, "ecs");
ecs_Slot_main_BallType.name = _global_StringInit(14, "Slot_main_Ball");_global_Maybe_recs_Slot_main_Ball_Type.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_recs_Slot_main_Ball_Type.package = _global_StringInit(7, "_global");
_global_Maybe_recs_Slot_main_Ball_Type.name = _global_StringInit(26, "Maybe_recs_Slot_main_Ball_");_global_Array_Maybe_rmain_Ball_Type.size.tag = 1;
_global_Array_Maybe_rmain_Ball_Type.array_type = 
_global_TypeFromStruct(
_global_Maybe_rmain_Ball_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;_global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_Type.size.tag = 2;
_global_StaticArray_StaticArray_S_ecs_Slot_main_Ball_Type.array_type = 
_global_TypeFromStruct(
ecs_Slot_main_Ball_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;ecs_Store_main_BallType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 6);
ecs_Store_main_BallType.fields = _global_StaticArray_StaticArray_S_FieldInit(
ecs_Store_main_BallType_fields
,6
);
ecs_Store_main_BallType.package = _global_StringInit(3, "ecs");
ecs_Store_main_BallType.name = _global_StringInit(15, "Store_main_Ball");
ecs_Store_main_BallType.size = sizeof(struct ecs_Store_main_Ball);
ecs_Store_main_BallType_fields[0].name = _global_StringInit(19, "make_component_func");
ecs_Store_main_BallType_fields[0].offset = offsetof(struct ecs_Store_main_Ball, make_component_func);
ecs_Store_main_BallType_fields[0].field_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;
ecs_Store_main_BallType_fields[1].name = _global_StringInit(9, "id_to_obj");
ecs_Store_main_BallType_fields[1].offset = offsetof(struct ecs_Store_main_Ball, id_to_obj);
ecs_Store_main_BallType_fields[1].field_type = 
_global_TypeFromStruct(
_global_Array_Maybe_rmain_Ball__get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
ecs_Store_main_BallType_fields[2].name = _global_StringInit(10, "components");
ecs_Store_main_BallType_fields[2].offset = offsetof(struct ecs_Store_main_Ball, components);
ecs_Store_main_BallType_fields[2].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_ecs_Slot_main_Ball__get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
ecs_Store_main_BallType_fields[3].name = _global_StringInit(9, "free_node");
ecs_Store_main_BallType_fields[3].offset = offsetof(struct ecs_Store_main_Ball, free_node);
ecs_Store_main_BallType_fields[3].field_type = 
_global_TypeFromStruct(
_global_Maybe_recs_Slot_main_Ball__get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;
ecs_Store_main_BallType_fields[4].name = _global_StringInit(10, "max_number");
ecs_Store_main_BallType_fields[4].offset = offsetof(struct ecs_Store_main_Ball, max_number);
ecs_Store_main_BallType_fields[4].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;
ecs_Store_main_BallType_fields[5].name = _global_StringInit(5, "added");
ecs_Store_main_BallType_fields[5].offset = offsetof(struct ecs_Store_main_Ball, added);
ecs_Store_main_BallType_fields[5].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_Array_ecs_Slot_main_Ball_Type.size.tag = 1;
_global_Array_ecs_Slot_main_Ball_Type.array_type = 
_global_TypeFromStruct(
ecs_Slot_main_Ball_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
; }
void mainInit() { 
runnerInit();;
taskInit();;
syncInit();;
syncInit();;
atomicInit();;
atomicInit();;
queueInit();;
queueInit();;
;
main_ball_system = ecs_make_Store_main_Ball(main_make_Ball,10,(&_global_context));;
;
};