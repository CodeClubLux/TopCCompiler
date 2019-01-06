void _global_log_uint(unsigned int _global_s, struct _global_Context* b);
struct puintcuintp* _global_StaticArray_op_get_2_puintcuintp(struct _global_StaticArray_2_puintcuintp* _global_self, unsigned int _global_index, struct _global_Context* c);
struct _global_StaticArray_2_puintcuintp main_arr;unsigned int main_a;unsigned int main_b;unsigned int main_i;void _global_log_uint(unsigned int _global_s, struct _global_Context* g){;
_global_c_log(_global_uint_toString(&(_global_s),g),g);
;}
struct puintcuintp* _global_StaticArray_op_get_2_puintcuintp(struct _global_StaticArray_2_puintcuintp* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<2,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + _global_index);
;}

void mainInitTypes() { 
 
_global_StaticArray_2_puintcuintpType.size.tag = 0;
_global_StaticArray_2_puintcuintpType.size.cases.Static.field0 = 2;
_global_StaticArray_2_puintcuintpType.array_type = 
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
main_arr = _global_StaticArray_2_puintcuintpInit(puintcuintpInit(10,20),puintcuintpInit(30,50));;
struct _global_StaticArray_2_puintcuintp c =main_arr;
for (unsigned int d = 0;d < 2; d++) {
struct puintcuintp f;f = *_global_StaticArray_op_get_2_puintcuintp(&c, d, (&_global_context));
;main_a=f.field0;main_b=f.field1;main_i = d;
_global_log_uint(main_i,(&_global_context));
_global_log_uint(main_a,(&_global_context));
_global_log_uint(main_b,(&_global_context));
}
;
;
};