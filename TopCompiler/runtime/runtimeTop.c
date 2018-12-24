struct _global_TemporaryStorage {
uint64_t occupied;
uint64_t highest;
void* data;
uint64_t maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(uint64_t occupied,uint64_t highest,void* data,uint64_t maxSize){
struct _global_TemporaryStorage c;
c.occupied=occupied;c.highest=highest;c.data=data;c.maxSize=maxSize;return c;
};
struct _global_StructType _global_TemporaryStorageType;struct _global_StructType* _global_TemporaryStorage_get_type(struct _global_TemporaryStorage* self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_Field* _global_TemporaryStorageType_fields;
struct _global_Type_VTABLE rAliasType_VTABLE_FOR_Type;struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc d;
return d;
};
struct _global_StructType _global_MallocType;struct _global_StructType* _global_Malloc_get_type(struct _global_Malloc* self, struct _global_Context* c){return &_global_MallocType;}
struct _global_Field* _global_MallocType_fields;
struct _global_StructType _global_Maybe_rAllocatorType;struct _global_StructType* _global_Maybe_rAllocator_get_type(struct _global_Allocator*** self, struct _global_Context* c){return &_global_Maybe_rAllocatorType;}
struct _global_StructType* _global_Maybe_rAllocator_get_typeByValue(struct _global_Allocator** self, struct _global_Context* c){return &_global_Maybe_rAllocatorType;}
struct _global_StructType _global_Maybe_rArray_TType;struct _global_StructType* _global_Maybe_rArray_T_get_type(void**** self, struct _global_Context* c){return &_global_Maybe_rArray_TType;}
struct _global_StructType* _global_Maybe_rArray_T_get_typeByValue(void*** self, struct _global_Context* c){return &_global_Maybe_rArray_TType;}
struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
void** data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,void** data){
struct _global_Array_Array_T f;
f.length=length;f.capacity=capacity;f.allocator=allocator;f.data=data;return f;
};
struct _global_ArrayType _global_Array_Array_TType;struct _global_ArrayType* _global_Array_Array_T_get_type(struct _global_Array_Array_T* self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType* _global_Array_Array_T_get_typeByValue(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType _global_Array_Array_TType;struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range g;
g.start=start;g.end=end;return g;
};
struct _global_StructType _global_RangeType;struct _global_StructType* _global_Range_get_type(struct _global_Range* self, struct _global_Context* c){return &_global_RangeType;}
struct _global_Field* _global_RangeType_fields;
struct _global_Maybe_uint_Some {
unsigned int field0;

};union _global_Maybe_uint_cases {
struct _global_Maybe_uint_Some Some;

};
struct _global_Maybe_uint {
union _global_Maybe_uint_cases cases;
_Bool tag;
};
struct _global_Maybe_uint _global_Some_uint(unsigned int h,struct _global_Context* j){
struct _global_Maybe_uint k;
k.cases.Some.field0 = h;k.tag = 0;
return k;}
struct _global_StructType _global_Maybe_uintType;struct _global_StructType* _global_Maybe_uint_get_type(struct _global_Maybe_uint* self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_StructType* _global_Maybe_uint_get_typeByValue(struct _global_Maybe_uint self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator l;
l.range=range;l.it=it;return l;
};
struct _global_StructType _global_RangeIteratorType;struct _global_StructType* _global_RangeIterator_get_type(struct _global_RangeIterator* self, struct _global_Context* c){return &_global_RangeIteratorType;}
struct _global_Field* _global_RangeIteratorType_fields;
union _global_FileAcess_cases {

};
struct _global_FileAcess {
union _global_FileAcess_cases cases;
_Bool tag;
};
struct _global_FileAcess _global_ReadFile;
struct _global_FileAcess _global_WriteFile;
struct _global_StructType _global_FileAcessType;struct _global_StructType* _global_FileAcess_get_type(struct _global_FileAcess* self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_StructType* _global_FileAcess_get_typeByValue(struct _global_FileAcess self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_StructType _global_FILEType;struct _global_StructType* _global_FILE_get_type(struct FILE* self, struct _global_Context* c){return &_global_FILEType;}
struct _global_Field* _global_FILEType_fields;
struct _global_File {
struct FILE* c_file;
struct _global_FileAcess acess;
};
static inline struct _global_File _global_FileInit(struct FILE* c_file,struct _global_FileAcess acess){
struct _global_File m;
m.c_file=c_file;m.acess=acess;return m;
};
struct _global_StructType _global_FileType;struct _global_StructType* _global_File_get_type(struct _global_File* self, struct _global_Context* c){return &_global_FileType;}
struct _global_Field* _global_FileType_fields;
struct _global_Maybe_File_Some {
struct _global_File field0;

};union _global_Maybe_File_cases {
struct _global_Maybe_File_Some Some;

};
struct _global_Maybe_File {
union _global_Maybe_File_cases cases;
_Bool tag;
};
struct _global_Maybe_File _global_Some_File(struct _global_File n,struct _global_Context* p){
struct _global_Maybe_File q;
q.cases.Some.field0 = n;q.tag = 0;
return q;}
struct _global_StructType _global_Maybe_FileType;struct _global_StructType* _global_Maybe_File_get_type(struct _global_Maybe_File* self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_StructType* _global_Maybe_File_get_typeByValue(struct _global_Maybe_File self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_StructType _global_FloatTypeType;struct _global_StructType* _global_FloatType_get_type(struct FloatType* self, struct _global_Context* c){return &_global_FloatTypeType;}
struct _global_Field* _global_FloatTypeType_fields;
struct _global_StructType _global_BoolTypeType;struct _global_StructType* _global_BoolType_get_type(struct BoolType* self, struct _global_Context* c){return &_global_BoolTypeType;}
struct _global_Field* _global_BoolTypeType_fields;
struct _global_FuncType {
struct _global_StaticArray_StaticArray_S_Type args;
struct _global_Type return_type;
};
static inline struct _global_FuncType _global_FuncTypeInit(struct _global_StaticArray_StaticArray_S_Type args,struct _global_Type return_type){
struct _global_FuncType r;
r.args=args;r.return_type=return_type;return r;
};
struct _global_StructType _global_FuncTypeType;struct _global_StructType* _global_FuncType_get_type(struct _global_FuncType* self, struct _global_Context* c){return &_global_FuncTypeType;}
struct _global_Field* _global_FuncTypeType_fields;
struct _global_CharType {
};
static inline struct _global_CharType _global_CharTypeInit(){
struct _global_CharType s;
return s;
};
struct _global_StructType _global_CharTypeType;struct _global_StructType* _global_CharType_get_type(struct _global_CharType* self, struct _global_Context* c){return &_global_CharTypeType;}
struct _global_Field* _global_CharTypeType_fields;
struct _global_Maybe_Maybe_T_Some {
void* field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
union _global_Maybe_Maybe_T_cases cases;
_Bool tag;
};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(void* t,struct _global_Context* v){
struct _global_Maybe_Maybe_T w;
w.cases.Some.field0 = t;w.tag = 0;
return w;}
struct _global_Maybe_Maybe_T _global_None;
struct _global_StructType _global_Maybe_Maybe_TType;struct _global_StructType* _global_Maybe_Maybe_T_get_type(struct _global_Maybe_Maybe_T* self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_StructType* _global_Maybe_Maybe_T_get_typeByValue(struct _global_Maybe_Maybe_T self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_StructType _global_Maybe_rFILEType;struct _global_StructType* _global_Maybe_rFILE_get_type(struct FILE*** self, struct _global_Context* c){return &_global_Maybe_rFILEType;}
struct _global_StructType* _global_Maybe_rFILE_get_typeByValue(struct FILE** self, struct _global_Context* c){return &_global_Maybe_rFILEType;}
typedef void(*pp___none)(struct _global_Context*) ;
struct bb {
struct bb_VTABLE* vtable;
void* data;
};struct bb_VTABLE {struct _global_Type type;};static inline struct bb bbFromStruct(void* data, struct bb_VTABLE* vtable, struct _global_Type typ){ 
struct bb y;
y.data = data;y.vtable = vtable;y.vtable->type = typ;
return y; 
}void* bb_get_pointer_to_data(struct bb* self, struct _global_Context* context) { return self->data; }struct _global_Type bb_get_type(struct bb* y, struct _global_Context* context){ return y->vtable->type; }struct _global_Type bb_get_typeByValue(struct bb y, struct _global_Context* context){ return y.vtable->type; }
struct _global_InterfaceType bb_Type;struct _global_Array_none {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
void* data;
};
static inline struct _global_Array_none _global_Array_noneInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,void* data){
struct _global_Array_none z;
z.length=length;z.capacity=capacity;z.allocator=allocator;z.data=data;return z;
};
struct _global_ArrayType _global_Array_noneType;struct _global_ArrayType* _global_Array_none_get_type(struct _global_Array_none* self, struct _global_Context* c){return &_global_Array_noneType;}
struct _global_ArrayType* _global_Array_none_get_typeByValue(struct _global_Array_none self, struct _global_Context* c){return &_global_Array_noneType;}
struct _global_ArrayType _global_Array_noneType;struct _global_StructType _global_Maybe_rnoneType;struct _global_StructType* _global_Maybe_rnone_get_type(void*** self, struct _global_Context* c){return &_global_Maybe_rnoneType;}
struct _global_StructType* _global_Maybe_rnone_get_typeByValue(void** self, struct _global_Context* c){return &_global_Maybe_rnoneType;}
struct _global_StaticArray_StaticArray_S_none {
void* data;
unsigned int length;
};
static inline struct _global_StaticArray_StaticArray_S_none _global_StaticArray_StaticArray_S_noneInit(void* data,unsigned int length){
struct _global_StaticArray_StaticArray_S_none B;
B.data=data;B.length=length;return B;
};
struct _global_ArrayType _global_StaticArray_StaticArray_S_noneType;struct _global_ArrayType* _global_StaticArray_StaticArray_S_none_get_type(struct _global_StaticArray_StaticArray_S_none* self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_noneType;}
struct _global_ArrayType* _global_StaticArray_StaticArray_S_none_get_typeByValue(struct _global_StaticArray_StaticArray_S_none self, struct _global_Context* c){return &_global_StaticArray_StaticArray_S_noneType;}
struct _global_ArrayType _global_StaticArray_StaticArray_S_noneType;
void _global_panic(struct _global_String _global_s, struct _global_Context* b);
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* c);
struct _global_TemporaryStorage _global_new_TemporaryStorage(uint64_t _global_maxSize, struct _global_Context* d);
uint64_t _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* f);
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, uint64_t _global_size, struct _global_Context* g);
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* h);
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, uint64_t _global_occupied, struct _global_Context* j);
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, uint64_t _global_size, struct _global_Context* k);
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* l);
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* m);
void _global_Malloc_free_allocator(struct _global_Malloc* _global_self, struct _global_Context* n);
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, uint64_t _global_to, struct _global_Context* p);
void _global_free(void* _global_p, struct _global_Context* q);
void _global_TemporaryStorage_free_allocator(struct _global_TemporaryStorage* _global_self, struct _global_Context* r);
struct _global_Array_Array_T _global_empty_array(struct _global_Context* s);
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* t);

static inline void _global_Range_iterator(struct _global_Range*,struct _global_Context* t);

void _global_Range_iteratorByValue(struct _global_Range,struct _global_Context* t);
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* v);
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* w);

static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess*,struct _global_Context* w);

struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess,struct _global_Context* w);
struct _global_String _global_File_read(struct _global_File* _global_self, struct _global_Context* x);
void _global_File_write(struct _global_File* _global_self, struct _global_String _global_s, struct _global_Context* y);
void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* z);

static inline void _global_File_free(struct _global_File*,struct _global_Context* z);

void _global_File_freeByValue(struct _global_File,struct _global_Context* z);
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* B);
uint64_t _global_IntType_get_size(struct IntType* _global_self, struct _global_Context* C);
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* D);

struct _global_String _global_IntType_toString(struct IntType*,struct _global_Context* D);
uint64_t _global_FloatType_get_size(struct FloatType* _global_self, struct _global_Context* F);
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* G);

struct _global_String _global_FloatType_toString(struct FloatType*,struct _global_Context* G);
struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* H);

struct _global_String _global_BoolType_toString(struct BoolType*,struct _global_Context* H);
uint64_t _global_BoolType_get_size(struct BoolType* _global_self, struct _global_Context* J);
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* K);

struct _global_String _global_StringType_toString(struct StringType*,struct _global_Context* K);
uint64_t _global_StringType_get_size(struct StringType* _global_self, struct _global_Context* L);
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* M);

struct _global_String _global_AliasType_toString(struct _global_AliasType*,struct _global_Context* M);
uint64_t _global_AliasType_get_size(struct _global_AliasType* _global_self, struct _global_Context* N);
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* P);

struct _global_String _global_PointerType_toString(struct _global_PointerType*,struct _global_Context* P);
uint64_t _global_PointerType_get_size(struct _global_PointerType* _global_self, struct _global_Context* Q);
uint64_t _global_StructType_get_size(struct _global_StructType* _global_self, struct _global_Context* R);
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* S);

struct _global_String _global_StructType_toString(struct _global_StructType*,struct _global_Context* S);
struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* T);

struct _global_String _global_EnumType_toString(struct _global_EnumType*,struct _global_Context* T);
uint64_t _global_EnumType_get_size(struct _global_EnumType* _global_self, struct _global_Context* V);
uint64_t _global_FuncType_get_size(struct _global_FuncType* _global_self, struct _global_Context* W);
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* X);

struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType*,struct _global_Context* X);
uint64_t _global_InterfaceType_get_size(struct _global_InterfaceType* _global_self, struct _global_Context* Y);
uint64_t _global_ArrayType_get_size(struct _global_ArrayType* _global_self, struct _global_Context* Z);
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* bb);

struct _global_String _global_ArrayType_toString(struct _global_ArrayType*,struct _global_Context* bb);
uint64_t _global_CharType_get_size(struct _global_CharType* _global_self, struct _global_Context* bc);
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* bd);

struct _global_String _global_NoneType_toString(struct NoneType*,struct _global_Context* bd);
uint64_t _global_NoneType_get_size(struct NoneType* _global_self, struct _global_Context* bf);
void _global_log_string(struct _global_String _global_s, struct _global_Context* bg);

#define _global_exit(bg,bh) exit(bg)

#define _global_c_log(bj,bk) _global_c_log(bj)
void _global_panic(struct _global_String _global_s, struct _global_Context* bl){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),bl),_global_StringInit(0,""),bl),bl);
_global_exit(1,bl);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* bl){;
;
if(!(_global_b)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),bl),_global_StringInit(0,""),bl),bl);
;};
;}

#define _global_memcpy(bl,bm,bn,bp) memcpy(bl,bm,bn)

#define _global_c_alloc(bq,br) malloc(bq)

#define _global_c_free(bs,bt) free(bs)
struct _global_TemporaryStorage _global_temporary_storage;struct _global_TemporaryStorage _global_longterm_storage_allocator;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator_VTABLE rTemporaryStorage_VTABLE_FOR_Allocator;struct _global_Allocator _global_malloc_as_allocator;struct _global_Allocator_VTABLE rMalloc_VTABLE_FOR_Allocator;struct _global_Allocator _global_longterm_storage_as_allocator;struct _global_TemporaryStorage _global_new_TemporaryStorage(uint64_t _global_maxSize, struct _global_Context* bv){;
;return _global_TemporaryStorageInit((uint64_t)0,(uint64_t)0,_global_c_alloc(_global_maxSize,bv),_global_maxSize);
;}
uint64_t _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* bv){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, uint64_t _global_size, struct _global_Context* bv){;
;
uint64_t _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){;
(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){;
(bv)->allocator=&(_global_malloc_as_allocator);;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(48,"ERROR: used more tempory memory than available: "),_global_u64_toStringByValue(((_global_self)->maxSize),bv),bv),_global_StringInit(0,""),bv),bv);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,bv);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* bv){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, uint64_t _global_occupied, struct _global_Context* bv){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){;
(bv)->allocator=&(_global_malloc_as_allocator);;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(48,"ERROR: used more tempory memory than available: "),_global_u64_toStringByValue(((_global_self)->occupied),bv),bv),_global_StringInit(0,""),bv),bv);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, uint64_t _global_size, struct _global_Context* bv){;
;
;return _global_c_alloc(_global_size,bv);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* bv){;
;
_global_c_free(_global_pointer,bv);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* bv){;
;return 0;
;}
void _global_Malloc_free_allocator(struct _global_Malloc* _global_self, struct _global_Context* bv){;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, uint64_t _global_to, struct _global_Context* bv){;
;
;}
void _global_free(void* _global_p, struct _global_Context* bv){;
_global_Allocator_dealloc((bv)->allocator,_global_p,bv);
;}
void _global_TemporaryStorage_free_allocator(struct _global_TemporaryStorage* _global_self, struct _global_Context* bv){;
_global_Allocator_dealloc((bv)->longterm_storage,(_global_self)->data,bv);
;}

#define _global_char_buffer_toString(bv,bw) _runtime_char_buffer_toString(bv)

#define _global_null_terminated '\0'

#define _global_make_String(bx,by,bz) _global_StringInit(bx,by)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* bB){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* bB){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* bC,struct _global_Context* bB){
_global_Range_iteratorByValue(*bC,bB);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T bD) {
struct _global_Maybe_uint bC;bC.tag = bD.tag;bC.cases = *(union _global_Maybe_uint_cases*) &(bD.cases);return bC;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* bB){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){;
unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,bB);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* bB){;
;struct _global_FileAcess bC =_global_self;
if(bC.tag==0){return _global_StringInit(1,"r");}else if(bC.tag==1){return _global_StringInit(1,"w");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* bD,struct _global_Context* bB){
return _global_FileAcess_toStringByValue(*bD,bB);
}
#define _global_c_open_file(bB,bC,bD) _runtime_c_open_file(bB,bC)

#define _global_c_close_file(bF,bG) _runtime_c_close_file(bF)

#define _global_c_read_file(bH,bJ,bK) _runtime_read_file(bH,bJ)

#define _global_c_write_file(bL,bM,bN,bP) _runtime_write_file(bL,bM,bN)
struct _global_String _global_File_read(struct _global_File* _global_self, struct _global_Context* bQ){;
struct _global_FileAcess bR =(_global_self)->acess;if(bR.tag==0){
;}
else if(1){
_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bQ);
;}
;
;return _global_c_read_file((_global_self)->c_file,bQ,bQ);
;}
void _global_File_write(struct _global_File* _global_self, struct _global_String _global_s, struct _global_Context* bQ){;
;
struct _global_FileAcess bR =(_global_self)->acess;if(bR.tag==1){
;}
else if(1){
_global_panic(_global_StringInit(39,"Trying to write to file not set to read"),bQ);
;}
;
_global_c_write_file((_global_self)->c_file,_global_s,bQ,bQ);
;}
void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bQ){;
_global_c_close_file((_global_self).c_file,bQ);
;}
static inline void _global_File_free(struct _global_File* bR,struct _global_Context* bQ){
_global_File_freeByValue(*bR,bQ);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bT) {
struct _global_Maybe_File bS;bS.tag = bT.tag;bS.cases = *(union _global_Maybe_File_cases*) &(bT.cases);return bS;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bQ){;
;
;struct FILE* bR =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bQ),bQ);
if(bR != NULL){struct FILE* _global_file = bR;
return _global_Some_File(_global_FileInit(_global_file,_global_acess),bQ);}else if(bR == NULL){return tmp_globalc(_global_None);};
;}

#define _global_set_bit_to(bQ,bR,bS,bT) _global_c_set_bit_to(bQ,bR,bS)

#define _global_is_bit_set(bV,bW,bX) _global_c_is_bit_set(bV,bW)

#define _global_bit_and(bY,bZ,cb) _global_c_bit_and(bY,bZ)

#define _global_null_char '\0'
uint64_t _global_IntType_get_size(struct IntType* _global_self, struct _global_Context* cc){;
;return (_global_self)->size;
;}
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* db){;
;return ((_global_self)->sign ? _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"i"),_global_uint_toStringByValue(((_global_self)->size*8),db),db),_global_StringInit(0,""),db):(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"u"),_global_uint_toStringByValue(((_global_self)->size*8),db),db),_global_StringInit(0,""),db)));
;}
static inline struct _global_String _global_IntType_toStringByValue(struct IntType dc,struct _global_Context* db){
return _global_IntType_toString(&dc,db);
}uint64_t _global_FloatType_get_size(struct FloatType* _global_self, struct _global_Context* db){;
;return (_global_self)->size;
;}
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* cc){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"f"),_global_uint_toStringByValue(((_global_self)->size*8),cc),cc),_global_StringInit(0,""),cc);
;}
static inline struct _global_String _global_FloatType_toStringByValue(struct FloatType cd,struct _global_Context* cc){
return _global_FloatType_toString(&cd,cc);
}struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* db){;
;return _global_StringInit(4,"bool");
;}
static inline struct _global_String _global_BoolType_toStringByValue(struct BoolType dc,struct _global_Context* db){
return _global_BoolType_toString(&dc,db);
}uint64_t _global_BoolType_get_size(struct BoolType* _global_self, struct _global_Context* db){;
;return sizeof(_Bool);
;}
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* cc){;
;return _global_StringInit(6,"string");
;}
static inline struct _global_String _global_StringType_toStringByValue(struct StringType cd,struct _global_Context* cc){
return _global_StringType_toString(&cd,cc);
}uint64_t _global_StringType_get_size(struct StringType* _global_self, struct _global_Context* db){;
;return sizeof(struct _global_String);
;}
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* cc){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),cc),_global_StringInit(1,"."),cc),((_global_self)->name),cc),_global_StringInit(0,""),cc);
;}
static inline struct _global_String _global_AliasType_toStringByValue(struct _global_AliasType cd,struct _global_Context* cc){
return _global_AliasType_toString(&cd,cc);
}uint64_t _global_AliasType_get_size(struct _global_AliasType* _global_self, struct _global_Context* db){;
;return _global_Type_get_size(&((_global_self)->real_type),db);
;}
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* cc){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"&"),_global_Type_toStringByValue(((_global_self)->p_type),cc),cc),_global_StringInit(0,""),cc);
;}
static inline struct _global_String _global_PointerType_toStringByValue(struct _global_PointerType cd,struct _global_Context* cc){
return _global_PointerType_toString(&cd,cc);
}uint64_t _global_PointerType_get_size(struct _global_PointerType* _global_self, struct _global_Context* db){;
;return sizeof(void*);
;}
uint64_t _global_StructType_get_size(struct _global_StructType* _global_self, struct _global_Context* cc){;
;return (_global_self)->size;
;}
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* db){;
;return (_global_String_op_eqByValue((_global_self)->package,_global_StringInit(7,"_global"),db) ? (_global_self)->name:(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),db),_global_StringInit(1,"."),db),((_global_self)->name),db),_global_StringInit(0,""),db)));
;}
static inline struct _global_String _global_StructType_toStringByValue(struct _global_StructType dc,struct _global_Context* db){
return _global_StructType_toString(&dc,db);
}struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* db){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),db),_global_StringInit(1,"."),db),((_global_self)->name),db),_global_StringInit(0,""),db);
;}
static inline struct _global_String _global_EnumType_toStringByValue(struct _global_EnumType dc,struct _global_Context* db){
return _global_EnumType_toString(&dc,db);
}uint64_t _global_EnumType_get_size(struct _global_EnumType* _global_self, struct _global_Context* db){;
;return (_global_self)->size;
;}
uint64_t _global_FuncType_get_size(struct _global_FuncType* _global_self, struct _global_Context* cc){;
;return sizeof(pp___none);
;}
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* db){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),db),_global_StringInit(1,"."),db),((_global_self)->name),db),_global_StringInit(0,""),db);
;}
static inline struct _global_String _global_InterfaceType_toStringByValue(struct _global_InterfaceType dc,struct _global_Context* db){
return _global_InterfaceType_toString(&dc,db);
}uint64_t _global_InterfaceType_get_size(struct _global_InterfaceType* _global_self, struct _global_Context* db){;
;return sizeof(struct bb);
;}
uint64_t _global_ArrayType_get_size(struct _global_ArrayType* _global_self, struct _global_Context* cc){;
;struct _global_ArraySize cd =(_global_self)->size;
if(cd.tag==0){unsigned int _global_length = cd.cases.Static.field0;
return _global_length*_global_Type_get_size(&((_global_self)->array_type),cc);}else if(cd.tag==1){return sizeof(struct _global_Array_none);}else if(cd.tag==2){return sizeof(struct _global_StaticArray_StaticArray_S_none);};
;}
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* db){;
;struct _global_ArraySize dc =(_global_self)->size;
if(dc.tag==0){unsigned int _global_length = dc.cases.Static.field0;
return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"["),_global_uint_toStringByValue((_global_length),db),db),_global_StringInit(1,"]"),db),_global_Type_toStringByValue(((_global_self)->array_type),db),db),_global_StringInit(0,""),db);}else if(dc.tag==1){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(4,"[..]"),_global_Type_toStringByValue(((_global_self)->array_type),db),db),_global_StringInit(0,""),db);}else if(dc.tag==2){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[]"),_global_Type_toStringByValue(((_global_self)->array_type),db),db),_global_StringInit(0,""),db);};
;}
static inline struct _global_String _global_ArrayType_toStringByValue(struct _global_ArrayType dd,struct _global_Context* db){
return _global_ArrayType_toString(&dd,db);
}uint64_t _global_CharType_get_size(struct _global_CharType* _global_self, struct _global_Context* db){;
;return sizeof(char);
;}
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* cc){;
;return _global_StringInit(4,"none");
;}
static inline struct _global_String _global_NoneType_toStringByValue(struct NoneType cd,struct _global_Context* cc){
return _global_NoneType_toString(&cd,cc);
}uint64_t _global_NoneType_get_size(struct NoneType* _global_self, struct _global_Context* db){;
;return sizeof(char);
;}
void _global_log_string(struct _global_String _global_s, struct _global_Context* cc){;
_global_c_log(_global_String_toString(&(_global_s),cc),cc);
;}

void _globalInitTypes() { 
 
_global_TemporaryStorageType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 4);
_global_TemporaryStorageType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_TemporaryStorageType_fields
,4
);
_global_TemporaryStorageType.package = _global_StringInit(7, "_global");
_global_TemporaryStorageType.name = _global_StringInit(16, "TemporaryStorage");
_global_TemporaryStorageType.size = sizeof(struct _global_TemporaryStorage);
_global_TemporaryStorageType_fields[0].name = _global_StringInit(8, "occupied");
_global_TemporaryStorageType_fields[0].offset = offsetof(struct _global_TemporaryStorage, occupied);
_global_TemporaryStorageType_fields[0].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
_global_TypeFromStruct(
_global_AliasType_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;
_global_TemporaryStorageType_fields[1].name = _global_StringInit(7, "highest");
_global_TemporaryStorageType_fields[1].offset = offsetof(struct _global_TemporaryStorage, highest);
_global_TemporaryStorageType_fields[1].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;
_global_TemporaryStorageType_fields[2].name = _global_StringInit(4, "data");
_global_TemporaryStorageType_fields[2].offset = offsetof(struct _global_TemporaryStorage, data);
_global_TemporaryStorageType_fields[2].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
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
_global_TemporaryStorageType_fields[3].name = _global_StringInit(7, "maxSize");
_global_TemporaryStorageType_fields[3].offset = offsetof(struct _global_TemporaryStorage, maxSize);
_global_TemporaryStorageType_fields[3].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
, &_global_AliasType_get_size
)
;_global_MallocType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_MallocType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_MallocType_fields
,0
);
_global_MallocType.package = _global_StringInit(7, "_global");
_global_MallocType.name = _global_StringInit(6, "Malloc");
_global_MallocType.size = sizeof(struct _global_Malloc);_global_Maybe_rAllocatorType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rAllocatorType.package = _global_StringInit(7, "_global");
_global_Maybe_rAllocatorType.name = _global_StringInit(16, "Maybe_rAllocator");_global_Maybe_rArray_TType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rArray_TType.package = _global_StringInit(7, "_global");
_global_Maybe_rArray_TType.name = _global_StringInit(14, "Maybe_rArray_T");_global_Array_Array_TType.size.tag = 1;
_global_Array_Array_TType.array_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;_global_RangeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_RangeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_RangeType_fields
,2
);
_global_RangeType.package = _global_StringInit(7, "_global");
_global_RangeType.name = _global_StringInit(5, "Range");
_global_RangeType.size = sizeof(struct _global_Range);
_global_RangeType_fields[0].name = _global_StringInit(5, "start");
_global_RangeType_fields[0].offset = offsetof(struct _global_Range, start);
_global_RangeType_fields[0].field_type = 
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
_global_RangeType_fields[1].name = _global_StringInit(3, "end");
_global_RangeType_fields[1].offset = offsetof(struct _global_Range, end);
_global_RangeType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_Maybe_uintType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_uintType.package = _global_StringInit(7, "_global");
_global_Maybe_uintType.name = _global_StringInit(10, "Maybe_uint");_global_RangeIteratorType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_RangeIteratorType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_RangeIteratorType_fields
,2
);
_global_RangeIteratorType.package = _global_StringInit(7, "_global");
_global_RangeIteratorType.name = _global_StringInit(13, "RangeIterator");
_global_RangeIteratorType.size = sizeof(struct _global_RangeIterator);
_global_RangeIteratorType_fields[0].name = _global_StringInit(5, "range");
_global_RangeIteratorType_fields[0].offset = offsetof(struct _global_RangeIterator, range);
_global_RangeIteratorType_fields[0].field_type = 
_global_TypeFromStruct(
_global_Range_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
;
_global_RangeIteratorType_fields[1].name = _global_StringInit(2, "it");
_global_RangeIteratorType_fields[1].offset = offsetof(struct _global_RangeIterator, it);
_global_RangeIteratorType_fields[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;
_global_FileAcessType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_FileAcessType.package = _global_StringInit(7, "_global");
_global_FileAcessType.name = _global_StringInit(9, "FileAcess");_global_FILEType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_FILEType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FILEType_fields
,0
);
_global_FILEType.package = _global_StringInit(7, "_global");
_global_FILEType.name = _global_StringInit(4, "FILE");_global_FileType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FileType_fields
,2
);
_global_FileType.package = _global_StringInit(7, "_global");
_global_FileType.name = _global_StringInit(4, "File");
_global_FileType.size = sizeof(struct _global_File);
_global_FileType_fields[0].name = _global_StringInit(6, "c_file");
_global_FileType_fields[0].offset = offsetof(struct _global_File, c_file);
_global_FileType_fields[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
_global_FILE_get_type(NULL,(&_global_context))
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
_global_FileType_fields[1].name = _global_StringInit(5, "acess");
_global_FileType_fields[1].offset = offsetof(struct _global_File, acess);
_global_FileType_fields[1].field_type = 
_global_TypeFromStruct(
_global_FileAcess_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;_global_Maybe_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_FileType.package = _global_StringInit(7, "_global");
_global_Maybe_FileType.name = _global_StringInit(10, "Maybe_File");_global_FloatTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_FloatTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FloatTypeType_fields
,0
);
_global_FloatTypeType.package = _global_StringInit(7, "_global");
_global_FloatTypeType.name = _global_StringInit(9, "FloatType");_global_BoolTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_BoolTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_BoolTypeType_fields
,0
);
_global_BoolTypeType.package = _global_StringInit(7, "_global");
_global_BoolTypeType.name = _global_StringInit(8, "BoolType");_global_FuncTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 2);
_global_FuncTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_FuncTypeType_fields
,2
);
_global_FuncTypeType.package = _global_StringInit(7, "_global");
_global_FuncTypeType.name = _global_StringInit(8, "FuncType");
_global_FuncTypeType.size = sizeof(struct _global_FuncType);
_global_FuncTypeType_fields[0].name = _global_StringInit(4, "args");
_global_FuncTypeType_fields[0].offset = offsetof(struct _global_FuncType, args);
_global_FuncTypeType_fields[0].field_type = 
_global_TypeFromStruct(
_global_StaticArray_StaticArray_S_Type_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
, &_global_ArrayType_get_size
)
;
_global_FuncTypeType_fields[1].name = _global_StringInit(11, "return_type");
_global_FuncTypeType_fields[1].offset = offsetof(struct _global_FuncType, return_type);
_global_FuncTypeType_fields[1].field_type = 
_global_TypeFromStruct(
&_global_Type_Type
,
&rInterfaceType_VTABLE_FOR_Type
,
rInterfaceType_VTABLE_FOR_Type.type
, &_global_InterfaceType_toString
, &_global_InterfaceType_get_size
)
;_global_CharTypeType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
_global_CharTypeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
_global_CharTypeType_fields
,0
);
_global_CharTypeType.package = _global_StringInit(7, "_global");
_global_CharTypeType.name = _global_StringInit(8, "CharType");
_global_CharTypeType.size = sizeof(struct _global_CharType);_global_None.tag = 1;
_global_Maybe_Maybe_TType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_Maybe_TType.package = _global_StringInit(7, "_global");
_global_Maybe_Maybe_TType.name = _global_StringInit(13, "Maybe_Maybe_T");_global_Maybe_rFILEType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rFILEType.package = _global_StringInit(7, "_global");
_global_Maybe_rFILEType.name = _global_StringInit(11, "Maybe_rFILE");bb_Type.name = _global_StringInit(0, "")
;bb_Type.package = _global_StringInit(0, "");_global_Array_noneType.size.tag = 1;
_global_Array_noneType.array_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
;_global_Maybe_rnoneType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rnoneType.package = _global_StringInit(7, "_global");
_global_Maybe_rnoneType.name = _global_StringInit(11, "Maybe_rnone");_global_StaticArray_StaticArray_S_noneType.size.tag = 2;
_global_StaticArray_StaticArray_S_noneType.array_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
, &_global_NoneType_get_size
)
; }
void _globalInit() { 
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage((uint64_t)10000000,(&_global_context));;
_global_longterm_storage_allocator = _global_new_TemporaryStorage((uint64_t)100000000,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&(_global_temporary_storage),&rTemporaryStorage_VTABLE_FOR_Allocator,_global_TypeFromStruct(_global_TemporaryStorage_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to, &_global_TemporaryStorage_free_allocator);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&(_global_malloc),&rMalloc_VTABLE_FOR_Allocator,_global_TypeFromStruct(_global_Malloc_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &_global_Malloc_get_occupied, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_reset_to, &_global_Malloc_free_allocator);;
_global_longterm_storage_as_allocator = _global_AllocatorFromStruct(&(_global_longterm_storage_allocator),&rTemporaryStorage_VTABLE_FOR_Allocator,rTemporaryStorage_VTABLE_FOR_Allocator.type, &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to, &_global_TemporaryStorage_free_allocator);;
(&_global_context)->allocator = &(_global_temporary_storage_as_allocator);
(&_global_context)->longterm_storage = &(_global_longterm_storage_as_allocator);
;
;
;
;
;
;
;
;
;
;
;
;
};