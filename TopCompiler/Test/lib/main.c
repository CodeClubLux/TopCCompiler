typedef void(*_____none)() ;
struct main_Animal{
void* type; /* is always null, for now */void* data;_____none method_makeNoise;
};static inline struct main_Animal main_AnimalFromStruct(void* data, _____none b){ 
struct main_Animal c;
c.data = data;c.method_makeNoise = b;
return c; 
}static inline void main_Animal_makeNoise(struct main_Animal* c){
return c->method_makeNoise(c->data);
};static inline void main_Animal_makeNoiseByValue(struct main_Animal c){
return c.method_makeNoise(c.data);
};
struct main_Duck {struct _global_String name;};static inline struct main_Duck main_DuckInit(struct _global_String name){struct main_Duck b;b.name=name;return b;};void main_Duck_makeNoise(struct main_Duck* main_self){;
_global_log(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),((main_self)->name)),_global_StringInit(2,"\n")));}
static inline void main_Duck_makeNoiseByValue(struct main_Duck c){
main_Duck_makeNoise(&c);
}struct main_Duck main_d;struct main_Animal main_i;struct main_Nullable_Value {
int field0;

};struct main_Nullable {
 _Bool tag;
union {
struct main_Nullable_Value Value;

};};
struct main_Nullable main_Value(int c){
struct main_Nullable d;
d.Value.field0 = c;d.tag = 0;
return d;}
struct main_Nullable main_Null;
struct main_Nullable main_s;
void mainInit() { 
;
main_d = main_DuckInit(_global_StringInit(12,"hello world!"));;
main_i = main_AnimalFromStruct(&main_d, &main_Duck_makeNoise);;
main_Animal_makeNoiseByValue(main_i);
main_Null.tag = 1;
main_s = main_Value(10);;
struct main_Nullable c =main_s;if(c.tag==0){int main_x = c.Value.field0;
;
_global_log(_global_Int_toStringByValue(main_x));};
if(c.tag==1){;
_global_log(_global_StringInit(4,"null"));};
;
;
};