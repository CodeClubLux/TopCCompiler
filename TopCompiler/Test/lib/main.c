typedef void*(*prnonec_SizeTp___rnone)(void*,unsigned int,struct _global_Context*) ;
typedef void(*prnonec_rnonep___none)(void*,void*,struct _global_Context*) ;
typedef void(*prnonep___none)(void*,struct _global_Context*) ;
struct _global_Allocator {
void* type; /* is always null, for now */ 
void* data;
prnonec_SizeTp___rnone method_alloc;
prnonec_rnonep___none method_dealloc;
prnonep___none method_clear;
};static inline struct _global_Allocator _global_AllocatorFromStruct(void* data, prnonec_SizeTp___rnone c, prnonec_rnonep___none d, prnonep___none f){ 
struct _global_Allocator g;
g.data = data;g.method_alloc = c;
g.method_dealloc = d;
g.method_clear = f;
return g; 
}static inline void* _global_Allocator_alloc(struct _global_Allocator* g,unsigned int h,struct _global_Context* b){
return g->method_alloc(g->data,h,b);
};static inline void* _global_Allocator_allocByValue(struct _global_Allocator g,unsigned int h,struct _global_Context* b){
return g.method_alloc(g.data,h,b);
};static inline void _global_Allocator_dealloc(struct _global_Allocator* g,void* k,struct _global_Context* b){
return g->method_dealloc(g->data,k,b);
};static inline void _global_Allocator_deallocByValue(struct _global_Allocator g,void* k,struct _global_Context* b){
return g.method_dealloc(g.data,k,b);
};static inline void _global_Allocator_clear(struct _global_Allocator* g,struct _global_Context* b){
return g->method_clear(g->data,b);
};static inline void _global_Allocator_clearByValue(struct _global_Allocator g,struct _global_Context* b){
return g.method_clear(g.data,b);
};typedef struct _global_String(*prnonep___string)(void*,struct _global_Context*) ;
struct _global_Maybe_rint_Some {
int* field0;

};union _global_Maybe_rint_cases {
struct _global_Maybe_rint_Some Some;

};
struct _global_Maybe_rint {
 _Bool tag;
union _global_Maybe_rint_cases cases;

};
struct _global_Maybe_rint _global_Some_rint(int* s){
struct _global_Maybe_rint t;
t.cases.Some.field0 = s;t.tag = 0;
return t;}
struct _global_Maybe_Maybe_T_Some {
struct _global_bb field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct _global_bb q){
struct _global_Maybe_Maybe_T r;
r.cases.Some.field0 = q;r.tag = 0;
return r;}
struct _global_Maybe_Maybe_T _global_None;
struct _global_Stringer {
void* type; /* is always null, for now */ 
void* data;
prnonep___string method_toString;
};static inline struct _global_Stringer _global_StringerFromStruct(void* data, prnonep___string m){ 
struct _global_Stringer n;
n.data = data;n.method_toString = m;
return n; 
}static inline struct _global_String _global_Stringer_toString(struct _global_Stringer* n,struct _global_Context* l){
return n->method_toString(n->data,l);
};static inline struct _global_String _global_Stringer_toStringByValue(struct _global_Stringer n,struct _global_Context* l){
return n.method_toString(n.data,l);
};struct _global_Maybe_rArray_T_Some {
struct _global_bb* field0;

};union _global_Maybe_rArray_T_cases {
struct _global_Maybe_rArray_T_Some Some;

};
struct _global_Maybe_rArray_T {
 _Bool tag;
union _global_Maybe_rArray_T_cases cases;

};
struct _global_Maybe_rArray_T _global_Some_rArray_T(struct _global_bb* j){
struct _global_Maybe_rArray_T k;
k.cases.Some.field0 = j;k.tag = 0;
return k;}
struct _global_Array_Array_T {
unsigned int length;
unsigned int capacity;
struct _global_Maybe_Allocator allocator;
struct _global_Maybe_rArray_T data;
};
static inline struct _global_Array_Array_T _global_Array_Array_TInit(unsigned int length,unsigned int capacity,struct _global_Maybe_Allocator allocator,struct _global_Maybe_rArray_T data){
struct _global_Array_Array_T h;
h.length=length;h.capacity=capacity;h.allocator=allocator;h.data=data;return h;
};
struct _global_bb {
void* type; /* is always null, for now */ 
void* data;
};static inline struct _global_bb _global_bbFromStruct(void* data){ 
struct _global_bb g;
g.data = data;return g; 
}struct _global_Maybe_Allocator_Some {
struct _global_Allocator field0;

};union _global_Maybe_Allocator_cases {
struct _global_Maybe_Allocator_Some Some;

};
struct _global_Maybe_Allocator {
 _Bool tag;
union _global_Maybe_Allocator_cases cases;

};
struct _global_Maybe_Allocator _global_Some_Allocator(struct _global_Allocator c){
struct _global_Maybe_Allocator d;
d.cases.Some.field0 = c;d.tag = 0;
return d;}
struct _global_Array_int {
unsigned int length;
unsigned int capacity;
struct _global_Maybe_Allocator allocator;
struct _global_Maybe_rint data;
};
static inline struct _global_Array_int _global_Array_intInit(unsigned int length,unsigned int capacity,struct _global_Maybe_Allocator allocator,struct _global_Maybe_rint data){
struct _global_Array_int b;
b.length=length;b.capacity=capacity;b.allocator=allocator;b.data=data;return b;
};

struct _global_Array_int main_array;static inline struct _global_Allocator d(struct _global_Maybe_Allocator** _global_self,struct _global_Allocator* _global_value, struct _global_Context* b) {
struct _global_Maybe_Allocator c =**_global_self;
if(c.tag==0){struct _global_Allocator _global_x = c.cases.Some.field0;
return _global_x;}if(c.tag==1){return *_global_value;}
}
struct _global_Allocator _global_Maybe_default_Allocator(struct _global_Maybe_Allocator* _global_self, struct _global_Allocator _global_value, struct _global_Context* b){;
;
;return d(&_global_self,&_global_value, b);}
static inline struct _global_Allocator _global_Maybe_default_AllocatorByValue(struct _global_Maybe_Allocator f,struct _global_Allocator g,struct _global_Context* b){
return _global_Maybe_default_Allocator(&f,g,b);
}struct _global_bb* _global_alloc_Maybe_T(struct _global_Context* c){;return (struct _global_bb*)(_global_Allocator_allocByValue((c)->allocator,sizeof(struct _global_bb),c));}
static inline struct _global_Maybe_rArray_T f(struct _global_Array_Array_T** _global_self,unsigned int* _global_newSize,struct _global_Allocator* _global_allocator, struct _global_Context* c) {
struct _global_Maybe_rArray_T d =(*_global_self)->data;
if(d.tag==0){struct _global_bb* _global_data = d.cases.Some.field0;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),c);
struct _global_bb* _global_newData;_global_newData = (struct _global_bb*)(_global_Allocator_allocByValue(*_global_allocator,(*_global_self)->capacity*sizeof(struct _global_bb),c));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(struct _global_bb),c);
_global_Allocator_deallocByValue(*_global_allocator,(void*)_global_data,c);
return _global_Some(_global_newData,c);}if(d.tag==1){return _global_Some((struct _global_bb*)(_global_Allocator_allocByValue(*_global_allocator,sizeof(struct _global_bb),c)),c);}
}
void _global_Array_reserve_Array_T(struct _global_Array_Array_T* _global_self, unsigned int _global_newSize, struct _global_Context* c){;
;
struct _global_Allocator _global_allocator;_global_allocator = _global_Maybe_default_AllocatorByValue((_global_self)->allocator,(c)->allocator,c);;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=f(&_global_self,&_global_newSize,&_global_allocator, c);;}
static inline void _global_Array_reserve_Array_TByValue(struct _global_Array_Array_T g,unsigned int h,struct _global_Context* c){
_global_Array_reserve_Array_T(&g,h,c);
}static inline struct _global_bb* f(struct _global_Maybe_rArray_T** _global_self, struct _global_Context* c) {
struct _global_Maybe_rArray_T d =**_global_self;
if(d.tag==0){struct _global_bb* _global_x = d.cases.Some.field0;
return _global_x;}if(d.tag==1){_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),c);
struct _global_bb** _global_pToValue;_global_pToValue = _global_alloc_Maybe_T(c);;
return *_global_pToValue;}
}
struct _global_bb* _global_Maybe_unwrap_Array_T_rArray_T(struct _global_Maybe_rArray_T* _global_self, struct _global_Context* c){;
;return f(&_global_self, c);}
static inline struct _global_bb* _global_Maybe_unwrap_Array_T_rArray_TByValue(struct _global_Maybe_rArray_T g,struct _global_Context* c){
return _global_Maybe_unwrap_Array_T_rArray_T(&g,c);
}struct _global_bb* _global_indexPtr_Array_T(struct _global_bb* _global_pType, int _global_offset, struct _global_Context* c){;
;
;return (struct _global_bb*)(_global_offsetPtr((void*)_global_pType,_global_offset*(int)sizeof(struct _global_bb),c));}
struct _global_String _global_toString_Array_T(struct _global_Stringer _global_s, struct _global_Context* c){;
;return _global_Array.T_toStringByValue(_global_s,c);}
struct _global_Maybe_Allocator d(struct _global_Maybe_Maybe_T g) {
struct _global_Maybe_Allocator f;f.tag = g.tag;f.cases = *(union _global_Maybe_Allocator_cases*) &(g.cases);return f;
}
struct _global_Maybe_rint h(struct _global_Maybe_Maybe_T k) {
struct _global_Maybe_rint j;j.tag = k.tag;j.cases = *(union _global_Maybe_rint_cases*) &(k.cases);return j;
}
struct _global_Array_int _global_make_array_int(struct _global_Context* c){;return _global_Array_intInit(0,0,d(_global_None),h(_global_None));}
void _global_Array_append_int(struct _global_Array_int* _global_self, int _global_value, struct _global_Context* c){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){_global_Array_reserve_Array_T(_global_self,(_global_self)->capacity*2,c);};
*(_global_indexPtr_Array_T(_global_Maybe_unwrap_Array_T_rArray_TByValue((_global_self)->data,c),(int)(_global_self)->length,c))=_global_value;;
(_global_self)->length=_global_newLength;;}
static inline void _global_Array_append_intByValue(struct _global_Array_int d,int f,struct _global_Context* c){
_global_Array_append_int(&d,f,c);
}static inline struct _global_String f(struct _global_Array_int** _global_self,struct _global_String* _global_delimiter, struct _global_Context* c) {
unsigned int d =(*_global_self)->length;
if(d.op_eq(0)){return _global_StringInit(0,"");}if(d.op_eq(1)){return _global_toString_Array_T(_global_Uint_op_add(*_global_self,(unsigned int)0,c),c);}if(1){struct _global_String _global_s;_global_s = _global_StringInit(0,"");;
unsigned int _global_i;_global_i = 0;;
;while(_global_i<(*_global_self)->length-1){_global_s=_global_String_op_addByValue(_global_s,_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),_global_Int_toStringByValue((_global_Uint_op_add(*_global_self,(unsigned int)_global_i,c)),c),c),_global_StringInit(0,""),c),(*_global_delimiter),c),_global_StringInit(0,""),c),c);;++_global_i;};
return _global_String_op_addByValue(_global_s,_global_toString_Array_T(_global_Uint_op_add(*_global_self,(unsigned int)-1,c),c),c);}
}
struct _global_String _global_Array_join_int(struct _global_Array_int* _global_self, struct _global_String _global_delimiter, struct _global_Context* c){;
;
;return f(&_global_self,&_global_delimiter, c);}
static inline struct _global_String _global_Array_join_intByValue(struct _global_Array_int g,struct _global_String h,struct _global_Context* c){
return _global_Array_join_int(&g,h,c);
}
void mainInit() { 
_global_None.tag = 1;
main_array = _global_make_array_int((&_global_context));;
&_global_Array_append_intByValue(main_array,(int)10,(&_global_context));
_global_Array_append_intByValue(main_array,(int)20,(&_global_context));
&_global_log(_global_Array_join_intByValue(main_array,_global_StringInit(1,","),(&_global_context)),(&_global_context));
;
};