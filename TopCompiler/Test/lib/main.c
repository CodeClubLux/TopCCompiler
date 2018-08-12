struct _global_Maybe_Allocator_Some {
struct _global_Allocator field0;

};union _global_Maybe_Allocator_cases {
struct _global_Maybe_Allocator_Some Some;

};
struct _global_Maybe_Allocator {
 _Bool tag;
union _global_Maybe_Allocator_cases cases;

};
struct _global_Maybe_Allocator _global_Some_Allocator(struct _global_Allocator b,struct _global_Context* c){
struct _global_Maybe_Allocator d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_bb {
void* type; /* is always null, for now */ 
void* data;
};static inline struct _global_bb _global_bbFromStruct(void* data){ 
struct _global_bb c;
c.data = data;return c; 
}struct _global_Maybe_rmain_Point_Some {
struct main_Point* field0;

};union _global_Maybe_rmain_Point_cases {
struct _global_Maybe_rmain_Point_Some Some;

};
struct _global_Maybe_rmain_Point {
 _Bool tag;
union _global_Maybe_rmain_Point_cases cases;

};
struct _global_Maybe_rmain_Point _global_Some_rmain_Point(struct main_Point* b,struct _global_Context* c){
struct _global_Maybe_rmain_Point d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_Array_main_Point {
unsigned int length;
unsigned int capacity;
struct _global_Maybe_Allocator allocator;
struct _global_Maybe_rmain_Point data;
};
static inline struct _global_Array_main_Point _global_Array_main_PointInit(unsigned int length,unsigned int capacity,struct _global_Maybe_Allocator allocator,struct _global_Maybe_rmain_Point data){
struct _global_Array_main_Point b;
b.length=length;b.capacity=capacity;b.allocator=allocator;b.data=data;return b;
};
struct _global_Maybe_Maybe_T_Some {
struct _global_bb field0;

};union _global_Maybe_Maybe_T_cases {
struct _global_Maybe_Maybe_T_Some Some;

};
struct _global_Maybe_Maybe_T {
 _Bool tag;
union _global_Maybe_Maybe_T_cases cases;

};
struct _global_Maybe_Maybe_T _global_Some_Maybe_T(struct _global_bb b,struct _global_Context* c){
struct _global_Maybe_Maybe_T d;
d.cases.Some.field0 = b;d.tag = 0;
return d;}
struct _global_Maybe_Maybe_T _global_None;

struct _global_String main_Point_toString(struct main_Point* main_self, struct _global_Context* b);
static inline struct _global_String main_Point_toStringByValue(struct main_Point,struct _global_Context* b);struct _global_Allocator _global_Maybe_default_Allocator(struct _global_Maybe_Allocator* _global_self, struct _global_Allocator _global_value, struct _global_Context* c);
static inline struct _global_Allocator _global_Maybe_default_AllocatorByValue(struct _global_Maybe_Allocator,struct _global_Allocator,struct _global_Context* c);struct _global_bb* _global_alloc_rmain_Point(struct _global_Context* c);
struct main_Point _global_Array_op_get_main_Point(struct _global_Array_main_Point* _global_self, unsigned int _global_index, struct _global_Context* c);
static inline struct main_Point _global_Array_op_get_main_PointByValue(struct _global_Array_main_Point,unsigned int,struct _global_Context* c);struct _global_String _global_toString_main_Point(struct main_Point _global_s, struct _global_Context* c);
void _global_Array_reserve_main_Point(struct _global_Array_main_Point* _global_self, unsigned int _global_newSize, struct _global_Context* c);
static inline void _global_Array_reserve_main_PointByValue(struct _global_Array_main_Point,unsigned int,struct _global_Context* c);struct main_Point* _global_Maybe_unwrap_main_Point_rmain_Point(struct _global_Maybe_rmain_Point* _global_self, struct _global_Context* c);
static inline struct main_Point* _global_Maybe_unwrap_main_Point_rmain_PointByValue(struct _global_Maybe_rmain_Point,struct _global_Context* c);struct main_Point* _global_indexPtr_main_Point(struct main_Point* _global_pType, int _global_offset, struct _global_Context* c);
struct _global_String _global_Array_join_main_Point(struct _global_Array_main_Point* _global_self, struct _global_String _global_delimiter, struct _global_Context* c);
static inline struct _global_String _global_Array_join_main_PointByValue(struct _global_Array_main_Point,struct _global_String,struct _global_Context* c);struct _global_Array_main_Point _global_make_array_main_Point(struct _global_Context* c);
void _global_Array_append_main_Point(struct _global_Array_main_Point* _global_self, struct main_Point _global_value, struct _global_Context* c);
static inline void _global_Array_append_main_PointByValue(struct _global_Array_main_Point,struct main_Point,struct _global_Context* c);struct _global_String _global_Array_toString_main_Point(struct _global_Array_main_Point* _global_self, struct _global_Context* c);
static inline struct _global_String _global_Array_toString_main_PointByValue(struct _global_Array_main_Point,struct _global_Context* c);struct main_Point {
int x;
int y;
};
static inline struct main_Point main_PointInit(int x,int y){
struct main_Point c;
c.x=x;c.y=y;return c;
};
struct _global_String main_Point_toString(struct main_Point* main_self, struct _global_Context* c){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(6,"Point("),_global_int_toStringByValue(((main_self)->x),c),c),_global_StringInit(1,","),c),_global_int_toStringByValue(((main_self)->y),c),c),_global_StringInit(1,")"),c);}
static inline struct _global_String main_Point_toStringByValue(struct main_Point d,struct _global_Context* c){
return main_Point_toString(&d,c);
}struct _global_Array_main_Point main_array;static inline struct _global_Allocator funcb(struct _global_Maybe_Allocator** _global_self,struct _global_Allocator* _global_value, struct _global_Context* c) {
struct _global_Maybe_Allocator d =**_global_self;
if(d.tag==0){struct _global_Allocator _global_x = d.cases.Some.field0;
return _global_x;}if(d.tag==1){return *_global_value;}printf("oh oh!");
}
struct _global_Allocator _global_Maybe_default_Allocator(struct _global_Maybe_Allocator* _global_self, struct _global_Allocator _global_value, struct _global_Context* c){;
;
;return funcb(&_global_self,&_global_value, c);}
static inline struct _global_Allocator _global_Maybe_default_AllocatorByValue(struct _global_Maybe_Allocator f,struct _global_Allocator g,struct _global_Context* c){
return _global_Maybe_default_Allocator(&f,g,c);
}struct _global_bb* _global_alloc_rmain_Point(struct _global_Context* c){;return (struct _global_bb*)(_global_Allocator_allocByValue((c)->allocator,sizeof(struct _global_bb),c));}
struct main_Point _global_Array_op_get_main_Point(struct _global_Array_main_Point* _global_self, unsigned int _global_index, struct _global_Context* c){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),c);
;return *(_global_indexPtr_main_Point(_global_Maybe_unwrap_main_Point_rmain_PointByValue((_global_self)->data,c),(int)_global_index,c));}
static inline struct main_Point _global_Array_op_get_main_PointByValue(struct _global_Array_main_Point d,unsigned int f,struct _global_Context* c){
return _global_Array_op_get_main_Point(&d,f,c);
}struct _global_String _global_toString_main_Point(struct main_Point _global_s, struct _global_Context* c){;
;return main_Point_toStringByValue(_global_s,c);}
static inline struct _global_Maybe_rmain_Point funcc(struct _global_Array_main_Point** _global_self,unsigned int* _global_newSize,struct _global_Allocator* _global_allocator, struct _global_Context* c) {
struct _global_Maybe_rmain_Point d =(*_global_self)->data;
if(d.tag==0){struct main_Point* _global_data = d.cases.Some.field0;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),c);
struct main_Point* _global_newData;_global_newData = (struct main_Point*)(_global_Allocator_allocByValue(*_global_allocator,(*_global_self)->capacity*sizeof(struct main_Point),c));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(struct main_Point),c);
_global_Allocator_deallocByValue(*_global_allocator,(void*)_global_data,c);
return _global_Some_rmain_Point(_global_newData,c);}if(d.tag==1){return _global_Some_rmain_Point((struct main_Point*)(_global_Allocator_allocByValue(*_global_allocator,(*_global_self)->capacity*sizeof(struct main_Point),c)),c);}printf("oh oh!");
}
void _global_Array_reserve_main_Point(struct _global_Array_main_Point* _global_self, unsigned int _global_newSize, struct _global_Context* c){;
;
struct _global_Allocator _global_allocator;_global_allocator = _global_Maybe_default_AllocatorByValue((_global_self)->allocator,(c)->allocator,c);;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=funcc(&_global_self,&_global_newSize,&_global_allocator, c);;}
static inline void _global_Array_reserve_main_PointByValue(struct _global_Array_main_Point f,unsigned int g,struct _global_Context* c){
_global_Array_reserve_main_Point(&f,g,c);
}static inline struct main_Point* funcd(struct _global_Maybe_rmain_Point** _global_self, struct _global_Context* c) {
struct _global_Maybe_rmain_Point d =**_global_self;
if(d.tag==0){struct main_Point* _global_x = d.cases.Some.field0;
return _global_x;}if(d.tag==1){_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),c);
struct main_Point** _global_pToValue;_global_pToValue = _global_alloc_rmain_Point(c);;
return *_global_pToValue;}printf("oh oh!");
}
struct main_Point* _global_Maybe_unwrap_main_Point_rmain_Point(struct _global_Maybe_rmain_Point* _global_self, struct _global_Context* c){;
;return funcd(&_global_self, c);}
static inline struct main_Point* _global_Maybe_unwrap_main_Point_rmain_PointByValue(struct _global_Maybe_rmain_Point f,struct _global_Context* c){
return _global_Maybe_unwrap_main_Point_rmain_Point(&f,c);
}struct main_Point* _global_indexPtr_main_Point(struct main_Point* _global_pType, int _global_offset, struct _global_Context* c){;
;
;return (struct main_Point*)(_global_offsetPtr((void*)_global_pType,_global_offset*(int)sizeof(struct main_Point),c));}
static inline struct _global_String funcf(struct _global_Array_main_Point** _global_self,struct _global_String* _global_delimiter, struct _global_Context* c) {
unsigned int d =(*_global_self)->length;
if(d==0){return _global_StringInit(0,"");}if(d==1){return _global_toString_main_Point(_global_Array_op_get_main_Point(*_global_self,(unsigned int)0,c),c);}if(1){struct _global_String _global_s;_global_s = _global_StringInit(0,"");;
unsigned int _global_i;_global_i = 0;;
;while(_global_i<(*_global_self)->length-1){_global_s=_global_String_op_addByValue(_global_s,_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),main_Point_toStringByValue((_global_Array_op_get_main_Point(*_global_self,(unsigned int)_global_i,c)),c),c),_global_StringInit(0,""),c),(*_global_delimiter),c),_global_StringInit(0,""),c),c);;_global_i=_global_i+1;;};
return _global_String_op_addByValue(_global_s,_global_toString_main_Point(_global_Array_op_get_main_Point(*_global_self,(unsigned int)(*_global_self)->length-1,c),c),c);}printf("oh oh!");
}
struct _global_String _global_Array_join_main_Point(struct _global_Array_main_Point* _global_self, struct _global_String _global_delimiter, struct _global_Context* c){;
;
;return funcf(&_global_self,&_global_delimiter, c);}
static inline struct _global_String _global_Array_join_main_PointByValue(struct _global_Array_main_Point f,struct _global_String g,struct _global_Context* c){
return _global_Array_join_main_Point(&f,g,c);
}struct _global_Maybe_Allocator funcg(struct _global_Maybe_Maybe_T f) {
struct _global_Maybe_Allocator d;d.tag = f.tag;d.cases = *(union _global_Maybe_Allocator_cases*) &(f.cases);return d;
}
struct _global_Maybe_rmain_Point funch(struct _global_Maybe_Maybe_T h) {
struct _global_Maybe_rmain_Point g;g.tag = h.tag;g.cases = *(union _global_Maybe_rmain_Point_cases*) &(h.cases);return g;
}
struct _global_Array_main_Point _global_make_array_main_Point(struct _global_Context* c){;return _global_Array_main_PointInit(0,0,funcg(_global_None),funch(_global_None));}
void _global_Array_append_main_Point(struct _global_Array_main_Point* _global_self, struct main_Point _global_value, struct _global_Context* c){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){if((_global_self)->capacity==0){_global_Array_reserve_main_Point(_global_self,1,c);}
else{_global_Array_reserve_main_Point(_global_self,(_global_self)->capacity*2,c);};};
*(_global_indexPtr_main_Point(_global_Maybe_unwrap_main_Point_rmain_PointByValue((_global_self)->data,c),(int)(_global_self)->length,c))=_global_value;;
(_global_self)->length=_global_newLength;;}
static inline void _global_Array_append_main_PointByValue(struct _global_Array_main_Point d,struct main_Point f,struct _global_Context* c){
_global_Array_append_main_Point(&d,f,c);
}struct _global_String _global_Array_toString_main_Point(struct _global_Array_main_Point* _global_self, struct _global_Context* c){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[ "),(_global_Array_join_main_Point(_global_self,_global_StringInit(2,", "),c)),c),_global_StringInit(2," ]"),c);}
static inline struct _global_String _global_Array_toString_main_PointByValue(struct _global_Array_main_Point d,struct _global_Context* c){
return _global_Array_toString_main_Point(&d,c);
}
void mainInit() { 
_global_None.tag = 1;
;
main_array = _global_make_array_main_Point((&_global_context));;
_global_Array_append_main_Point(&main_array,main_PointInit((int)30,(int)50),(&_global_context));
_global_log(_global_Array_toString_main_Point(&main_array,(&_global_context)),(&_global_context));
;
};