void _global_log_uint(unsigned int _global_s, struct _global_Context* b);
unsigned int* _global_StaticArray_op_get_10_uint(struct _global_StaticArray_10_uint* _global_self, unsigned int _global_index, struct _global_Context* c);
void _global_log_uint(unsigned int _global_s, struct _global_Context* f){;
_global_c_log(_global_uint_toString(&(_global_s),f),f);
;}
unsigned int* _global_StaticArray_op_get_10_uint(struct _global_StaticArray_10_uint* _global_self, unsigned int _global_index, struct _global_Context* f){;
;
_global_assert(_global_index<10,_global_StringInit(13,"Out of bounds"),f);
;return ((_global_self)->data + _global_index);
;}

void mainInit() { 

struct _global_StaticArray_10_uint c =_global_StaticArray_10_uintFill_array(5);
for (unsigned int d = 0;d < 10; d++) {
unsigned int main_i;main_i = *_global_StaticArray_op_get_10_uint(&c, d, (&_global_context));
_global_log_uint(main_i,(&_global_context));
}
;
;
};