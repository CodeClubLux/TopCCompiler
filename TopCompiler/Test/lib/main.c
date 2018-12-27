struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* b);

static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator**,struct _global_Allocator*,struct _global_Context* b);

struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator*,struct _global_Allocator*,struct _global_Context* b);
void _global_Array_reserve_dict_HashBucket_int_(struct _global_Array_dict_HashBucket_int_* _global_self, unsigned int _global_newSize, struct _global_Context* c);
struct dict_HashBucket_int* _global_Maybe_unwrap_rdict_HashBucket_int_ByValue(struct dict_HashBucket_int* _global_self, struct _global_Context* c);

static inline struct dict_HashBucket_int* _global_Maybe_unwrap_rdict_HashBucket_int_(struct dict_HashBucket_int**,struct _global_Context* c);

struct dict_HashBucket_int* _global_Maybe_unwrap_rdict_HashBucket_int_ByValue(struct dict_HashBucket_int*,struct _global_Context* c);
void _global_Array_free_string(struct _global_Array_string* _global_self, struct _global_Context* c);
void _global_Array_free_int(struct _global_Array_int* _global_self, struct _global_Context* c);
void _global_Array_reserve_string(struct _global_Array_string* _global_self, unsigned int _global_newSize, struct _global_Context* c);
struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String* _global_self, struct _global_Context* c);

static inline struct _global_String* _global_Maybe_unwrap_rstring(struct _global_String**,struct _global_Context* c);

struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String*,struct _global_Context* c);
void _global_Array_reserve_int(struct _global_Array_int* _global_self, unsigned int _global_newSize, struct _global_Context* c);
int* _global_Maybe_unwrap_rintByValue(int* _global_self, struct _global_Context* c);

static inline int* _global_Maybe_unwrap_rint(int**,struct _global_Context* c);

int* _global_Maybe_unwrap_rintByValue(int*,struct _global_Context* c);
struct dict_HashBucket_int dict_make_HashBucket_int(struct _global_Context* c);
void _global_Array_append_dict_HashBucket_int_(struct _global_Array_dict_HashBucket_int_* _global_self, struct dict_HashBucket_int _global_value, struct _global_Context* c);
void dict_HashBucket_free_int(struct dict_HashBucket_int* dict_self, struct _global_Context* c);
struct dict_HashBucket_int* _global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(struct _global_StaticArray_StaticArray_S_dict_HashBucket_int_* _global_self, unsigned int _global_index, struct _global_Context* c);
void _global_Array_append_string(struct _global_Array_string* _global_self, struct _global_String _global_value, struct _global_Context* c);
void _global_Array_append_int(struct _global_Array_int* _global_self, int _global_value, struct _global_Context* c);
struct _global_String* _global_Array_op_get_string(struct _global_Array_string* _global_self, unsigned int _global_index, struct _global_Context* c);
int* _global_Array_op_get_int(struct _global_Array_int* _global_self, unsigned int _global_index, struct _global_Context* c);
struct dict_HashMap_int dict_make_HashMap_int(struct _global_Context* c);
void dict_HashMap_free_int(struct dict_HashMap_int* dict_self, struct _global_Context* c);
void dict_HashMap_insert_int(struct dict_HashMap_int* dict_self, struct _global_String dict_key, int dict_value, struct _global_Context* c);
struct _global_StaticArray_StaticArray_S_string dict_HashMap_keys_int(struct dict_HashMap_int* dict_self, struct _global_Context* c);
int* dict_HashMap_op_get_int(struct dict_HashMap_int* dict_self, struct _global_String dict_key, struct _global_Context* c);
struct _global_String* _global_StaticArray_op_get_StaticArray_S_string(struct _global_StaticArray_StaticArray_S_string* _global_self, unsigned int _global_index, struct _global_Context* c);
struct dict_HashMap_int main_hash_map;struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* g){;
;
;struct _global_Allocator* h =_global_self;
if(h != NULL){struct _global_Allocator* _global_x = h;
return _global_x;}else if(h == NULL){return _global_value;};
;}
static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator** j,struct _global_Allocator* k,struct _global_Context* g){
return _global_Maybe_default_rAllocatorByValue(*j,k,g);
}
static inline struct dict_HashBucket_int* tmpmainb(struct _global_Array_dict_HashBucket_int_** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
struct dict_HashBucket_int* h =(*_global_self)->data;
if(h != NULL){struct dict_HashBucket_int* _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
struct dict_HashBucket_int* _global_newData;_global_newData = (struct dict_HashBucket_int*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct dict_HashBucket_int),g));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(uint64_t)(*_global_self)->length*sizeof(struct dict_HashBucket_int),g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (struct dict_HashBucket_int*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct dict_HashBucket_int),g));}
}
void _global_Array_reserve_dict_HashBucket_int_(struct _global_Array_dict_HashBucket_int_* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainb(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
struct dict_HashBucket_int* _global_Maybe_unwrap_rdict_HashBucket_int_ByValue(struct dict_HashBucket_int* _global_self, struct _global_Context* g){;
struct dict_HashBucket_int* _global_x;;
struct dict_HashBucket_int* h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct dict_HashBucket_int* _global_Maybe_unwrap_rdict_HashBucket_int_(struct dict_HashBucket_int** j,struct _global_Context* g){
return _global_Maybe_unwrap_rdict_HashBucket_int_ByValue(*j,g);
}void _global_Array_free_string(struct _global_Array_string* _global_self, struct _global_Context* g){;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
struct _global_String* h =(_global_self)->data;if(h != NULL){struct _global_String* _global_data = h;

_global_free((void*)_global_data,g);
;}
else if(h == NULL){
;}
;
;}
void _global_Array_free_int(struct _global_Array_int* _global_self, struct _global_Context* g){;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
int* h =(_global_self)->data;if(h != NULL){int* _global_data = h;

_global_free((void*)_global_data,g);
;}
else if(h == NULL){
;}
;
;}

static inline struct _global_String* tmpmainc(struct _global_Array_string** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
struct _global_String* h =(*_global_self)->data;
if(h != NULL){struct _global_String* _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
struct _global_String* _global_newData;_global_newData = (struct _global_String*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct _global_String),g));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(uint64_t)(*_global_self)->length*sizeof(struct _global_String),g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (struct _global_String*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(struct _global_String),g));}
}
void _global_Array_reserve_string(struct _global_Array_string* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainc(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String* _global_self, struct _global_Context* g){;
struct _global_String* _global_x;;
struct _global_String* h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline struct _global_String* _global_Maybe_unwrap_rstring(struct _global_String** j,struct _global_Context* g){
return _global_Maybe_unwrap_rstringByValue(*j,g);
}
static inline int* tmpmaind(struct _global_Array_int** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* g) {
int* h =(*_global_self)->data;
if(h != NULL){int* _global_data = h;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),g);
int* _global_newData;_global_newData = (int*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(int),g));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(uint64_t)(*_global_self)->length*sizeof(int),g);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,g);
return _global_newData;}else if(h == NULL){return (int*)(_global_Allocator_alloc(*_global_allocator,(uint64_t)(*_global_self)->capacity*sizeof(int),g));}
}
void _global_Array_reserve_int(struct _global_Array_int* _global_self, unsigned int _global_newSize, struct _global_Context* g){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(g)->allocator,g);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmaind(&_global_self,&_global_newSize,&_global_allocator, g);;
;}
int* _global_Maybe_unwrap_rintByValue(int* _global_self, struct _global_Context* g){;
int* _global_x;;
int* h =_global_self;if(h != NULL){_global_x = h;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),g);
;}
;
;return _global_x;
;}
static inline int* _global_Maybe_unwrap_rint(int** j,struct _global_Context* g){
return _global_Maybe_unwrap_rintByValue(*j,g);
}struct dict_HashBucket_int dict_make_HashBucket_int(struct _global_Context* g){;return dict_HashBucket_intInit(_global_Array_stringInit(0, 0, NULL, NULL),_global_Array_intInit(0, 0, NULL, NULL));
;}
void _global_Array_append_dict_HashBucket_int_(struct _global_Array_dict_HashBucket_int_* _global_self, struct dict_HashBucket_int _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_dict_HashBucket_int_(_global_self,1,g);
;}
else{_global_Array_reserve_dict_HashBucket_int_(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_rdict_HashBucket_int_ByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
void dict_HashBucket_free_int(struct dict_HashBucket_int* dict_self, struct _global_Context* g){;
_global_Array_free_string(&((dict_self)->keys),g);
_global_Array_free_int(&((dict_self)->values),g);
;}
struct dict_HashBucket_int* _global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(struct _global_StaticArray_StaticArray_S_dict_HashBucket_int_* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + _global_index);
;}
void _global_Array_append_string(struct _global_Array_string* _global_self, struct _global_String _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_string(_global_self,1,g);
;}
else{_global_Array_reserve_string(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_rstringByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
void _global_Array_append_int(struct _global_Array_int* _global_self, int _global_value, struct _global_Context* g){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_int(_global_self,1,g);
;}
else{_global_Array_reserve_int(_global_self,(_global_self)->capacity*2,g);
;};
;};
*(((_global_Maybe_unwrap_rintByValue((_global_self)->data,g) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
struct _global_String* _global_Array_op_get_string(struct _global_Array_string* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return (_global_Maybe_unwrap_rstringByValue((_global_self)->data,g) + _global_index);
;}
int* _global_Array_op_get_int(struct _global_Array_int* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return (_global_Maybe_unwrap_rintByValue((_global_self)->data,g) + _global_index);
;}
struct dict_HashMap_int dict_make_HashMap_int(struct _global_Context* g){struct _global_Array_dict_HashBucket_int_ dict_buckets;dict_buckets = _global_Array_dict_HashBucket_int_Init(0, 0, NULL, NULL);;
struct _global_Range h =_global_RangeInit(0,dict_default_table_size);
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int dict_i;dict_i = j;
_global_Array_append_dict_HashBucket_int_(&(dict_buckets),dict_make_HashBucket_int(g),g);
}
;
;return dict_HashMap_intInit(_global_StaticArray_StaticArray_S_dict_HashBucket_int_Init(dict_buckets.data, dict_buckets.length));
;}
void dict_HashMap_free_int(struct dict_HashMap_int* dict_self, struct _global_Context* g){;
struct _global_StaticArray_StaticArray_S_dict_HashBucket_int_ h =(dict_self)->buckets;
for (unsigned int j = 0;j < h.length; j++) {
struct dict_HashBucket_int dict_bucket;unsigned int dict_i;dict_bucket = *_global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(&h, j, g);
dict_i = j;
dict_HashBucket_free_int(&(dict_bucket),g);
}
;
;}
void dict_HashMap_insert_int(struct dict_HashMap_int* dict_self, struct _global_String dict_key, int dict_value, struct _global_Context* g){;
;
;
unsigned int dict_hash;dict_hash = dict_hash_string(dict_key,dict_default_table_size,g);;
struct dict_HashBucket_int* dict_bucket;dict_bucket = &(*(_global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(&((dict_self)->buckets),dict_hash,g)));;
_global_Array_append_string(&((dict_bucket)->keys),dict_key,g);
_global_Array_append_int(&((dict_bucket)->values),dict_value,g);
;}
struct _global_StaticArray_StaticArray_S_string dict_HashMap_keys_int(struct dict_HashMap_int* dict_self, struct _global_Context* g){;
struct _global_Array_string dict_arr;dict_arr = _global_Array_stringInit(0, 0, NULL, NULL);;
struct _global_StaticArray_StaticArray_S_dict_HashBucket_int_ h =(dict_self)->buckets;
for (unsigned int j = 0;j < h.length; j++) {
struct dict_HashBucket_int dict_bucket;unsigned int dict_i;dict_bucket = *_global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(&h, j, g);
dict_i = j;
struct _global_Array_string k =(dict_bucket).keys;
for (unsigned int l = 0;l < k.length; l++) {
struct _global_String dict_key;unsigned int dict_i;dict_key = *_global_Array_op_get_string(&k, l, g);
dict_i = l;
_global_Array_append_string(&(dict_arr),dict_key,g);
}
;
}
;
;return _global_StaticArray_StaticArray_S_stringInit(dict_arr.data, dict_arr.length);
;}
int* dict_HashMap_op_get_int(struct dict_HashMap_int* dict_self, struct _global_String dict_key, struct _global_Context* g){;
;
unsigned int dict_hash;dict_hash = dict_hash_string(dict_key,dict_default_table_size,g);;
struct dict_HashBucket_int* dict_bucket;dict_bucket = &(*(_global_StaticArray_op_get_StaticArray_S_dict_HashBucket_int_(&((dict_self)->buckets),dict_hash,g)));;
struct _global_Array_string h =(dict_bucket)->keys;
for (unsigned int j = 0;j < h.length; j++) {
struct _global_String dict_b_key;unsigned int dict_i;dict_b_key = *_global_Array_op_get_string(&h, j, g);
dict_i = j;
if(_global_String_op_eqByValue(dict_b_key,dict_key,g)){;
return &(*(_global_Array_op_get_int(&((dict_bucket)->values),dict_i,g)));
;
;};
}
;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(3,"No "),(dict_key),g),_global_StringInit(12," in hash map"),g),g);
;return (int*)0;
;}
struct _global_String* _global_StaticArray_op_get_StaticArray_S_string(struct _global_StaticArray_StaticArray_S_string* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + _global_index);
;}

void mainInitTypes() { 
 dictInitTypes();
_global_Array_stringType.size.tag = 1;
_global_Array_stringType.array_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;_global_Maybe_rstringType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rstringType.package = _global_StringInit(7, "_global");
_global_Maybe_rstringType.name = _global_StringInit(13, "Maybe_rstring");_global_Array_intType.size.tag = 1;
_global_Array_intType.array_type = 
_global_TypeFromStruct(
_global_int_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_Maybe_rintType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rintType.package = _global_StringInit(7, "_global");
_global_Maybe_rintType.name = _global_StringInit(10, "Maybe_rint");dict_HashBucket_intType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
dict_HashBucket_intType.fields = _global_StaticArray_StaticArray_S_FieldInit(
dict_HashBucket_intType_fields
,2
);
dict_HashBucket_intType.package = _global_StringInit(4, "dict");
dict_HashBucket_intType.name = _global_StringInit(14, "HashBucket_int");
dict_HashBucket_intType.size = sizeof(struct dict_HashBucket_int);
dict_HashBucket_intType_fields[0].name = _global_StringInit(4, "keys");
dict_HashBucket_intType_fields[0].offset = offsetof(struct dict_HashBucket_int, keys);
dict_HashBucket_intType_fields[0].field_type = 
_global_TypeFromStruct(
_global_Array_string_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
dict_HashBucket_intType_fields[1].name = _global_StringInit(6, "values");
dict_HashBucket_intType_fields[1].offset = offsetof(struct dict_HashBucket_int, values);
dict_HashBucket_intType_fields[1].field_type = 
_global_TypeFromStruct(
_global_Array_int_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;_global_Maybe_rdict_HashBucket_int_Type.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rdict_HashBucket_int_Type.package = _global_StringInit(7, "_global");
_global_Maybe_rdict_HashBucket_int_Type.name = _global_StringInit(27, "Maybe_rdict_HashBucket_int_");_global_Array_dict_HashBucket_int_Type.size.tag = 1;
_global_Array_dict_HashBucket_int_Type.array_type = 
_global_TypeFromStruct(
dict_HashBucket_int_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;_global_StaticArray_StaticArray_S_dict_HashBucket_int_Type.size.tag = 2;
_global_StaticArray_StaticArray_S_dict_HashBucket_int_Type.array_type = 
_global_TypeFromStruct(
dict_HashBucket_int_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;dict_HashMap_intType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 1);
dict_HashMap_intType.fields = _global_StaticArray_StaticArray_S_FieldInit(
dict_HashMap_intType_fields
,1
);
dict_HashMap_intType.package = _global_StringInit(4, "dict");
dict_HashMap_intType.name = _global_StringInit(11, "HashMap_int");
dict_HashMap_intType.size = sizeof(struct dict_HashMap_int);
dict_HashMap_intType_fields[0].name = _global_StringInit(7, "buckets");
dict_HashMap_intType_fields[0].offset = offsetof(struct dict_HashMap_int, buckets);
dict_HashMap_intType_fields[0].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_dict_HashBucket_int__get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;_global_StaticArray_StaticArray_S_stringType.size.tag = 2;
_global_StaticArray_StaticArray_S_stringType.array_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;dict_Hash_Type.name = _global_StringInit(4, "Hash");
dict_Hash_Type.package = _global_StringInit(4, "dict");
dict_Hash_Type.real_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
; }
void mainInit() { 
dictInit();;
;
main_hash_map = dict_make_HashMap_int((&_global_context));;
struct dict_HashMap_int* c = &(main_hash_map);
;
dict_HashMap_insert_int(&(main_hash_map),_global_StringInit(5,"hello"),10,(&_global_context));
dict_HashMap_insert_int(&(main_hash_map),_global_StringInit(3,"bye"),20,(&_global_context));
struct _global_StaticArray_StaticArray_S_string d =dict_HashMap_keys_int(&(main_hash_map),(&_global_context));
for (unsigned int f = 0;f < d.length; f++) {
struct _global_String main_key;unsigned int main_i;main_key = *_global_StaticArray_op_get_StaticArray_S_string(&d, f, (&_global_context));
main_i = f;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(9,"hash_map["),(main_key),(&_global_context)),_global_StringInit(4,"] = "),(&_global_context)),_global_int_toStringByValue((*(dict_HashMap_op_get_int(&(main_hash_map),(struct _global_String)main_key,(&_global_context)))),(&_global_context)),(&_global_context)),_global_StringInit(0,""),(&_global_context)),(&_global_context));
}
;
;
};