void _global_log_uint(unsigned int _global_s, struct _global_Context* b);
struct puintcuintp* _global_StaticArray_op_get_1_puintcuintp(struct _global_StaticArray_1_puintcuintp* _global_self, unsigned int _global_index, struct _global_Context* c);
void _global_log_uint(unsigned int _global_s, struct _global_Context* g){;
_global_c_log(_global_uint_toString(&(_global_s),g),g);
;}
struct puintcuintp* _global_StaticArray_op_get_1_puintcuintp(struct _global_StaticArray_1_puintcuintp* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<1,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + (int64_t)_global_index);
;}

void mainInitTypes() { 
 
_global_StaticArray_1_puintcuintpType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_1_puintcuintpType.size->tag = 0;
_global_StaticArray_1_puintcuintpType.size->cases.Static.field0 = 1;
_global_StaticArray_1_puintcuintpType.array_type = 
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
void mainInit() { 
struct _global_StaticArray_1_puintcuintp c =_global_StaticArray_1_puintcuintpInit(puintcuintpInit(10,20));
for (unsigned int d = 0;d < 1; d++) {
unsigned int main_a;unsigned int main_b;struct puintcuintp f;f = *_global_StaticArray_op_get_1_puintcuintp(&c, d, (&_global_context));
;main_a=f.field0;main_b=f.field1;unsigned int main_i;main_i = d;
main_a=main_a+30;;
_global_log_uint(main_a,(&_global_context));
}
;
;
};