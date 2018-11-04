#include <string.h>

struct _global_TemporaryStorage {
unsigned int occupied;
unsigned int highest;
void* data;
unsigned int maxSize;
};
static inline struct _global_TemporaryStorage _global_TemporaryStorageInit(unsigned int occupied,unsigned int highest,void* data,unsigned int maxSize){
struct _global_TemporaryStorage c;
c.occupied=occupied;c.highest=highest;c.data=data;c.maxSize=maxSize;return c;
};
struct _global_StructType _global_TemporaryStorageType;struct _global_StructType* _global_TemporaryStorage_get_type(struct _global_TemporaryStorage* self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_StructType* _global_TemporaryStorage_get_typeByValue(struct _global_TemporaryStorage self, struct _global_Context* c){return &_global_TemporaryStorageType;}
struct _global_Malloc {
};
static inline struct _global_Malloc _global_MallocInit(){
struct _global_Malloc f;
return f;
};
struct _global_StructType _global_MallocType;struct _global_StructType* _global_Malloc_get_type(struct _global_Malloc* self, struct _global_Context* c){return &_global_MallocType;}
struct _global_StructType* _global_Malloc_get_typeByValue(struct _global_Malloc self, struct _global_Context* c){return &_global_MallocType;}
struct _global_All {
struct _global_All_VTABLE* vtable;
void* data;
};struct _global_All_VTABLE {struct _global_Type type;};static inline struct _global_All _global_AllFromStruct(void* data, struct _global_All_VTABLE* vtable, struct _global_Type typ){ 
struct _global_All j;
j.data = data;j.vtable = vtable;j.vtable->type = typ;
return j; 
}struct _global_Type _global_All_get_type(struct _global_All* j, struct _global_Context* context){ return j->vtable->type; }struct _global_Type _global_All_get_typeByValue(struct _global_All j, struct _global_Context* context){ return j.vtable->type; }
struct _global_InterfaceType _global_All_Type;struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Allocator* allocator;
struct _global_All* data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Allocator* allocator,struct _global_All* data){
struct _global_Array_Array_T k;
k.length=length;k.capacity=capacity;k.allocator=allocator;k.data=data;return k;
};
struct _global_ArrayType _global_Array_Array_TType;struct _global_ArrayType* _global_Array_Array_T_get_type(struct _global_Array_Array_T* self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType* _global_Array_Array_T_get_typeByValue(struct _global_Array_Array_T self, struct _global_Context* c){return &_global_Array_Array_TType;}
struct _global_ArrayType _global_Array_Array_TType;struct _global_Range {
unsigned int start;
unsigned int end;
};
static inline struct _global_Range _global_RangeInit(unsigned int start,unsigned int end){
struct _global_Range l;
l.start=start;l.end=end;return l;
};
struct _global_StructType _global_RangeType;struct _global_StructType* _global_Range_get_type(struct _global_Range* self, struct _global_Context* c){return &_global_RangeType;}
struct _global_StructType* _global_Range_get_typeByValue(struct _global_Range self, struct _global_Context* c){return &_global_RangeType;}
struct _global_Maybe_uint_Some {
unsigned int field0;

};union _global_Maybe_uint_cases {
struct _global_Maybe_uint_Some Some;

};
struct _global_Maybe_uint {
 _Bool tag;
union _global_Maybe_uint_cases cases;

};
struct _global_Maybe_uint _global_Some_uint(unsigned int n,struct _global_Context* p){
struct _global_Maybe_uint q;
q.cases.Some.field0 = n;q.tag = 0;
return q;}
struct _global_StructType _global_Maybe_uintType;struct _global_StructType* _global_Maybe_uint_get_type(struct _global_Maybe_uint* self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_StructType* _global_Maybe_uint_get_typeByValue(struct _global_Maybe_uint self, struct _global_Context* c){return &_global_Maybe_uintType;}
struct _global_RangeIterator {
struct _global_Range range;
unsigned int it;
};
static inline struct _global_RangeIterator _global_RangeIteratorInit(struct _global_Range range,unsigned int it){
struct _global_RangeIterator r;
r.range=range;r.it=it;return r;
};
struct _global_StructType _global_RangeIteratorType;struct _global_StructType* _global_RangeIterator_get_type(struct _global_RangeIterator* self, struct _global_Context* c){return &_global_RangeIteratorType;}
struct _global_StructType* _global_RangeIterator_get_typeByValue(struct _global_RangeIterator self, struct _global_Context* c){return &_global_RangeIteratorType;}
union _global_FileAcess_cases {

};
struct _global_FileAcess {
 _Bool tag;
union _global_FileAcess_cases cases;

};
struct _global_FileAcess _global_ReadFile;
struct _global_FileAcess _global_WriteFile;
struct _global_StructType _global_FileAcessType;struct _global_StructType* _global_FileAcess_get_type(struct _global_FileAcess* self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_StructType* _global_FileAcess_get_typeByValue(struct _global_FileAcess self, struct _global_Context* c){return &_global_FileAcessType;}
struct _global_File {
struct FILE* c_file;
struct _global_FileAcess acess;
};
static inline struct _global_File _global_FileInit(struct FILE* c_file,struct _global_FileAcess acess){
struct _global_File t;
t.c_file=c_file;t.acess=acess;return t;
};
struct _global_StructType _global_FileType;struct _global_StructType* _global_File_get_type(struct _global_File* self, struct _global_Context* c){return &_global_FileType;}
struct _global_StructType* _global_File_get_typeByValue(struct _global_File self, struct _global_Context* c){return &_global_FileType;}
struct _global_Maybe_File_Some {
struct _global_File field0;

};union _global_Maybe_File_cases {
struct _global_Maybe_File_Some Some;

};
struct _global_Maybe_File {
 _Bool tag;
union _global_Maybe_File_cases cases;

};
struct _global_Maybe_File _global_Some_File(struct _global_File w,struct _global_Context* x){
struct _global_Maybe_File y;
y.cases.Some.field0 = w;y.tag = 0;
return y;}
struct _global_StructType _global_Maybe_FileType;struct _global_StructType* _global_Maybe_File_get_type(struct _global_Maybe_File* self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_StructType* _global_Maybe_File_get_typeByValue(struct _global_Maybe_File self, struct _global_Context* c){return &_global_Maybe_FileType;}
struct _global_Maybe_Maybe_T_Some {
struct _global_All field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct _global_All z,struct _global_Context* B){
struct _global_Maybe_Maybe_T C;
C.cases.Some.field0 = z;C.tag = 0;
return C;}
struct _global_Maybe_Maybe_T _global_None;
struct _global_StructType _global_Maybe_Maybe_TType;struct _global_StructType* _global_Maybe_Maybe_T_get_type(struct _global_Maybe_Maybe_T* self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}
struct _global_StructType* _global_Maybe_Maybe_T_get_typeByValue(struct _global_Maybe_Maybe_T self, struct _global_Context* c){return &_global_Maybe_Maybe_TType;}

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
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* z);

struct _global_String _global_IntType_toString(struct IntType*,struct _global_Context* z);
struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* B);

struct _global_String _global_FloatType_toString(struct FloatType*,struct _global_Context* B);
struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* C);

struct _global_String _global_BoolType_toString(struct BoolType*,struct _global_Context* C);
struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* D);

struct _global_String _global_StringType_toString(struct StringType*,struct _global_Context* D);
struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* F);

struct _global_String _global_AliasType_toString(struct _global_AliasType*,struct _global_Context* F);
struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* G);

struct _global_String _global_PointerType_toString(struct _global_PointerType*,struct _global_Context* G);
struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* H);

struct _global_String _global_StructType_toString(struct _global_StructType*,struct _global_Context* H);
struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* J);

struct _global_String _global_EnumType_toString(struct _global_EnumType*,struct _global_Context* J);
struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* K);

struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType*,struct _global_Context* K);
struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* L);

struct _global_String _global_ArrayType_toString(struct _global_ArrayType*,struct _global_Context* L);
struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* M);

struct _global_String _global_NoneType_toString(struct NoneType*,struct _global_Context* M);
void _global_log_string(struct _global_String _global_s, struct _global_Context* N);

#define _global_exit(N,P) exit(N)
void _global_panic(struct _global_String _global_s, struct _global_Context* Q){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"panic: "),(_global_s),Q),_global_StringInit(0,""),Q),Q);
_global_exit(1,Q);
;}
void _global_assert(_Bool _global_b, struct _global_String _global_message, struct _global_Context* Q){;
;
if(!(_global_b)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Assertion failed: "),(_global_message),Q),_global_StringInit(0,""),Q),Q);
;};
;}

#define _global_c_log(Q,R) _global_c_log(Q)

#define _global_memcpy(S,T,V,W) memcpy(S,T,V)

#define _global_c_alloc(X,Y) malloc(X)

#define _global_c_free(Z,bb) free(Z)
struct _global_TemporaryStorage _global_new_TemporaryStorage(unsigned int _global_maxSize, struct _global_Context* bc){;
;return _global_TemporaryStorageInit(0,0,_global_c_alloc(_global_maxSize,bc),_global_maxSize);
;}
unsigned int _global_TemporaryStorage_get_occupied(struct _global_TemporaryStorage* _global_self, struct _global_Context* bc){;
;return (_global_self)->occupied;
;}
void* _global_TemporaryStorage_alloc(struct _global_TemporaryStorage* _global_self, unsigned int _global_size, struct _global_Context* bc){;
;
unsigned int _global_occupied;_global_occupied = (_global_self)->occupied;;
(_global_self)->occupied=(_global_self)->occupied+_global_size;;
if((_global_self)->occupied>(_global_self)->highest){;
(_global_self)->highest=(_global_self)->occupied;;
;};
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_log_string(_global_StringInit(48,"panic: used more temporary memory than available"),bc);
_global_exit(1,bc);
;};
;return _global_offsetPtr((_global_self)->data,_global_occupied,bc);
;}
void _global_TemporaryStorage_dealloc(struct _global_TemporaryStorage* _global_self, void* _global_p, struct _global_Context* bc){;
;
;}
void _global_TemporaryStorage_reset_to(struct _global_TemporaryStorage* _global_self, unsigned int _global_occupied, struct _global_Context* bc){;
;
(_global_self)->occupied=_global_occupied;;
if((_global_self)->occupied>=(_global_self)->maxSize){;
_global_panic(_global_StringInit(41,"used more temporary memory than available"),bc);
;};
;}
void* _global_Malloc_alloc(struct _global_Malloc* _global_self, unsigned int _global_size, struct _global_Context* bc){;
;
;return _global_c_alloc(_global_size,bc);
;}
void _global_Malloc_dealloc(struct _global_Malloc* _global_self, void* _global_pointer, struct _global_Context* bc){;
;
_global_c_free(_global_pointer,bc);
;}
unsigned int _global_Malloc_get_occupied(struct _global_Malloc* _global_self, struct _global_Context* bc){;
;return 0;
;}
void _global_Malloc_reset_to(struct _global_Malloc* _global_self, unsigned int _global_to, struct _global_Context* bc){;
;
;}
struct _global_TemporaryStorage _global_temporary_storage;struct _global_Malloc _global_malloc;struct _global_Allocator _global_temporary_storage_as_allocator;struct _global_Allocator_VTABLE rTemporaryStorage_VTABLE_FOR_Allocator;struct _global_Allocator _global_malloc_as_allocator;struct _global_Allocator_VTABLE rMalloc_VTABLE_FOR_Allocator;void* _global_alloc(unsigned int _global_size, struct _global_Context* bc){;
;return _global_Allocator_alloc((bc)->allocator,_global_size,bc);
;}
void _global_free(void* _global_p, struct _global_Context* bc){;
_global_Allocator_dealloc((bc)->allocator,_global_p,bc);
;}

#define _global_char_buffer_toString(bc,bd) _runtime_char_buffer_toString(bc)
struct _global_Array_Array_T _global_empty_array(struct _global_Context* bf){;return _global_Array_Array_TInit(0,0,NULL,NULL);
;}
void _global_Range_iteratorByValue(struct _global_Range _global_self, struct _global_Context* bf){;
_global_RangeIteratorInit(_global_self,0);
;}
static inline void _global_Range_iterator(struct _global_Range* bg,struct _global_Context* bf){
_global_Range_iteratorByValue(*bg,bf);
}static inline struct _global_Maybe_uint tmp_globalb(struct _global_Maybe_Maybe_T bh) {
struct _global_Maybe_uint bg;bg.tag = bh.tag;bg.cases = *(union _global_Maybe_uint_cases*) &(bh.cases);return bg;
}
struct _global_Maybe_uint _global_RangeIterator_next(struct _global_RangeIterator* _global_self, struct _global_Context* bf){;
struct _global_Range* _global_range;_global_range = &(((_global_self)->range));;
;if((_global_self)->it<(_global_range)->end){;
unsigned int _global_tmp;_global_tmp = (_global_self)->it;;
(_global_self)->it=(_global_self)->it+1;;
return _global_Some_uint(_global_tmp,bf);}
else{return tmp_globalb(_global_None);};
;}
struct _global_String _global_FileAcess_toStringByValue(struct _global_FileAcess _global_self, struct _global_Context* bf){;
;struct _global_FileAcess bg =_global_self;
if(bg.tag==0){return _global_StringInit(1,"r");}else if(bg.tag==1){return _global_StringInit(1,"w");};
;}
static inline struct _global_String _global_FileAcess_toString(struct _global_FileAcess* bh,struct _global_Context* bf){
return _global_FileAcess_toStringByValue(*bh,bf);
}
#define _global_c_open_file(bf,bg,bh) _runtime_c_open_file(bf,bg)

#define _global_c_close_file(bj,bk) _runtime_c_close_file(bj)

#define _global_c_read_file(bl,bm,bn) _runtime_read_file(bl,bm)
struct _global_String _global_File_readByValue(struct _global_File _global_self, struct _global_Context* bp){;
;struct _global_FileAcess bq =(_global_self).acess;
if(bq.tag==0){return _global_c_read_file((_global_self).c_file,bp,bp);}else if(1){_global_panic(_global_StringInit(40,"Trying to read from file not set to read"),bp);
return _global_StringInit(0,"");};
;}
static inline struct _global_String _global_File_read(struct _global_File* br,struct _global_Context* bp){
return _global_File_readByValue(*br,bp);
}void _global_File_freeByValue(struct _global_File _global_self, struct _global_Context* bp){;
_global_c_close_file((_global_self).c_file,bp);
;}
static inline void _global_File_free(struct _global_File* bq,struct _global_Context* bp){
_global_File_freeByValue(*bq,bp);
}static inline struct _global_Maybe_File tmp_globalc(struct _global_Maybe_Maybe_T bs) {
struct _global_Maybe_File br;br.tag = bs.tag;br.cases = *(union _global_Maybe_File_cases*) &(bs.cases);return br;
}
struct _global_Maybe_File _global_open(struct _global_String _global_filename, struct _global_FileAcess _global_acess, struct _global_Context* bp){;
;
struct FILE* _global_c_file;_global_c_file = _global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bp),bp);;
;struct FILE* bq =_global_c_open_file(_global_filename,_global_FileAcess_toStringByValue(_global_acess,bp),bp);
if(bq != NULL){struct FILE* _global_file= bq;
return _global_Some_File(_global_FileInit(_global_file,_global_acess),bp);}else if(bq == NULL){return tmp_globalc(_global_None);};
;}

#define _global_set_bit_to(bp,bq,br,bs) _global_c_set_bit_to(bp,bq,br)

#define _global_is_bit_set(bt,bv,bw) _global_c_is_bit_set(bt,bv)
struct _global_String _global_IntType_toString(struct IntType* _global_self, struct _global_Context* bx){;
;return ((_global_self)->sign ? _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"i"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx):(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"u"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx)));
;}
static inline struct _global_String _global_IntType_toStringByValue(struct IntType by,struct _global_Context* bx){
return _global_IntType_toString(&by,bx);
}struct _global_String _global_FloatType_toString(struct FloatType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"f"),_global_uint_toStringByValue(((_global_self)->size*8),bx),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_FloatType_toStringByValue(struct FloatType by,struct _global_Context* bx){
return _global_FloatType_toString(&by,bx);
}struct _global_String _global_BoolType_toString(struct BoolType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(4,"bool");
;}
static inline struct _global_String _global_BoolType_toStringByValue(struct BoolType by,struct _global_Context* bx){
return _global_BoolType_toString(&by,bx);
}struct _global_String _global_StringType_toString(struct StringType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(6,"string");
;}
static inline struct _global_String _global_StringType_toStringByValue(struct StringType by,struct _global_Context* bx){
return _global_StringType_toString(&by,bx);
}struct _global_String _global_AliasType_toString(struct _global_AliasType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_AliasType_toStringByValue(struct _global_AliasType by,struct _global_Context* bx){
return _global_AliasType_toString(&by,bx);
}struct _global_String _global_PointerType_toString(struct _global_PointerType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"&"),_global_Type_toStringByValue(((_global_self)->p_type),bx),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_PointerType_toStringByValue(struct _global_PointerType by,struct _global_Context* bx){
return _global_PointerType_toString(&by,bx);
}struct _global_String _global_StructType_toString(struct _global_StructType* _global_self, struct _global_Context* bx){;
;return (_global_String_op_eqByValue((_global_self)->package,_global_StringInit(7,"_global"),bx) ? (_global_self)->name:(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx)));
;}
static inline struct _global_String _global_StructType_toStringByValue(struct _global_StructType by,struct _global_Context* bx){
return _global_StructType_toString(&by,bx);
}struct _global_String _global_EnumType_toString(struct _global_EnumType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_EnumType_toStringByValue(struct _global_EnumType by,struct _global_Context* bx){
return _global_EnumType_toString(&by,bx);
}struct _global_String _global_InterfaceType_toString(struct _global_InterfaceType* _global_self, struct _global_Context* bx){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((_global_self)->package),bx),_global_StringInit(1,"."),bx),((_global_self)->name),bx),_global_StringInit(0,""),bx);
;}
static inline struct _global_String _global_InterfaceType_toStringByValue(struct _global_InterfaceType by,struct _global_Context* bx){
return _global_InterfaceType_toString(&by,bx);
}struct _global_String _global_ArrayType_toString(struct _global_ArrayType* _global_self, struct _global_Context* bx){;
;struct _global_ArraySize by =(_global_self)->size;
if(by.tag==0){unsigned int _global_length = by.cases.Static.field0;
return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(1,"["),_global_uint_toStringByValue((_global_length),bx),bx),_global_StringInit(1,"]"),bx),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);}else if(by.tag==1){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(4,"[..]"),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);}else if(by.tag==2){return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[]"),_global_Type_toStringByValue(((_global_self)->array_type),bx),bx),_global_StringInit(0,""),bx);};
;}
static inline struct _global_String _global_ArrayType_toStringByValue(struct _global_ArrayType bz,struct _global_Context* bx){
return _global_ArrayType_toString(&bz,bx);
}struct _global_String _global_NoneType_toString(struct NoneType* _global_self, struct _global_Context* bx){;
;return _global_StringInit(4,"none");
;}
static inline struct _global_String _global_NoneType_toStringByValue(struct NoneType by,struct _global_Context* bx){
return _global_NoneType_toString(&by,bx);
}void _global_log_string(struct _global_String _global_s, struct _global_Context* bx){;
_global_c_log(_global_String_toString(&(_global_s),bx),bx);
;}

void _globalInit() { 
struct _global_Field d[4];
_global_TemporaryStorageType.fields = _global_StaticArray_StaticArray_S_FieldInit(
d
,4
);
_global_TemporaryStorageType.package = _global_StringInit(7, "_global");
_global_TemporaryStorageType.name = _global_StringInit(16, "TemporaryStorage");
d[0].name = _global_StringInit(8, "occupied");
d[0].offset = offsetof(struct _global_TemporaryStorage, occupied);
d[0].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;
d[1].name = _global_StringInit(7, "highest");
d[1].offset = offsetof(struct _global_TemporaryStorage, highest);
d[1].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;
d[2].name = _global_StringInit(4, "data");
d[2].offset = offsetof(struct _global_TemporaryStorage, data);
d[2].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
)
;
d[3].name = _global_StringInit(7, "maxSize");
d[3].offset = offsetof(struct _global_TemporaryStorage, maxSize);
d[3].field_type = 
_global_TypeFromStruct(
&_global_SizeT_Type
,
&rAliasType_VTABLE_FOR_Type
,
rAliasType_VTABLE_FOR_Type.type
, &_global_AliasType_toString
)
;struct _global_Field g[0];
_global_MallocType.fields = _global_StaticArray_StaticArray_S_FieldInit(
g
,0
);
_global_MallocType.package = _global_StringInit(7, "_global");
_global_MallocType.name = _global_StringInit(6, "Malloc");_global_All_Type.name = _global_StringInit(3, "All")
;_global_All_Type.package = _global_StringInit(7, "_global");_global_Array_Array_TType.size.tag = 1;
_global_Array_Array_TType.array_type = 
_global_TypeFromStruct(
&None_Type
,
&rNoneType_VTABLE_FOR_Type
,
rNoneType_VTABLE_FOR_Type.type
, &_global_NoneType_toString
)
;struct _global_Field m[2];
_global_RangeType.fields = _global_StaticArray_StaticArray_S_FieldInit(
m
,2
);
_global_RangeType.package = _global_StringInit(7, "_global");
_global_RangeType.name = _global_StringInit(5, "Range");
m[0].name = _global_StringInit(5, "start");
m[0].offset = offsetof(struct _global_Range, start);
m[0].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;
m[1].name = _global_StringInit(3, "end");
m[1].offset = offsetof(struct _global_Range, end);
m[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;_global_Maybe_uintType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_uintType.package = _global_StringInit(7, "_global");
_global_Maybe_uintType.name = _global_StringInit(10, "Maybe_uint");struct _global_Field s[2];
_global_RangeIteratorType.fields = _global_StaticArray_StaticArray_S_FieldInit(
s
,2
);
_global_RangeIteratorType.package = _global_StringInit(7, "_global");
_global_RangeIteratorType.name = _global_StringInit(13, "RangeIterator");
s[0].name = _global_StringInit(5, "range");
s[0].offset = offsetof(struct _global_RangeIterator, range);
s[0].field_type = 
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
;
s[1].name = _global_StringInit(2, "it");
s[1].offset = offsetof(struct _global_RangeIterator, it);
s[1].field_type = 
_global_TypeFromStruct(
_global_uint_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
)
;_global_ReadFile.tag = 0;
_global_WriteFile.tag = 1;
_global_FileAcessType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_FileAcessType.package = _global_StringInit(7, "_global");
_global_FileAcessType.name = _global_StringInit(9, "FileAcess");struct _global_Field v[2];
_global_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(
v
,2
);
_global_FileType.package = _global_StringInit(7, "_global");
_global_FileType.name = _global_StringInit(4, "File");
v[0].name = _global_StringInit(6, "c_file");
v[0].offset = offsetof(struct _global_File, c_file);
v[0].field_type = 
_global_TypeFromStruct(
_global_boxPointerType(_global_PointerTypeInit(
_global_TypeFromStruct(
NULL
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
),(&_global_context))
,
&rPointerType_VTABLE_FOR_Type
,
rPointerType_VTABLE_FOR_Type.type
, &_global_PointerType_toString
)
;
v[1].name = _global_StringInit(5, "acess");
v[1].offset = offsetof(struct _global_File, acess);
v[1].field_type = 
_global_TypeFromStruct(
NULL
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
)
;_global_Maybe_FileType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_FileType.package = _global_StringInit(7, "_global");
_global_Maybe_FileType.name = _global_StringInit(10, "Maybe_File");_global_None.tag = 1;
_global_Maybe_Maybe_TType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_Maybe_TType.package = _global_StringInit(7, "_global");
_global_Maybe_Maybe_TType.name = _global_StringInit(13, "Maybe_Maybe_T");
;
;
;
;
;
_global_temporary_storage = _global_new_TemporaryStorage(100000,(&_global_context));;
_global_malloc = _global_MallocInit();;
_global_temporary_storage_as_allocator = _global_AllocatorFromStruct(&(_global_temporary_storage),&rTemporaryStorage_VTABLE_FOR_Allocator,_global_TypeFromStruct(NULL,&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString), &_global_TemporaryStorage_get_occupied, &_global_TemporaryStorage_alloc, &_global_TemporaryStorage_dealloc, &_global_TemporaryStorage_reset_to);;
_global_malloc_as_allocator = _global_AllocatorFromStruct(&(_global_malloc),&rMalloc_VTABLE_FOR_Allocator,_global_TypeFromStruct(NULL,&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString), &_global_Malloc_get_occupied, &_global_Malloc_alloc, &_global_Malloc_dealloc, &_global_Malloc_reset_to);;
(&_global_context)->allocator = &(_global_temporary_storage_as_allocator);
(&_global_context)->longterm_storage = &(_global_malloc_as_allocator);
;
;
;
;
;
;
;
};