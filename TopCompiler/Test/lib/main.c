struct _global_String main_Point_toString(struct main_Point* main_self, struct _global_Context* c){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),_global_int_toStringByValue(((main_self)->x),c),c),_global_StringInit(2,", "),c),_global_int_toStringByValue(((main_self)->y),c),c),_global_StringInit(0,""),c);
;}
static inline struct _global_String main_Point_toStringByValue(struct main_Point d,struct _global_Context* c){
return main_Point_toString(&d,c);
}unsigned int main_i;unsigned int* main_c;
void mainInit() { 

main_i = 10;;
main_c = &(main_i);;
;
};