void _global_log_main_Point(struct main_Point _global_s, struct _global_Context* c);
struct _global_String main_Point_toString(struct main_Point* main_self, struct _global_Context* c){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(6,"Point("),_global_int_toStringByValue(((main_self)->x),c),c),_global_StringInit(2,", "),c),_global_int_toStringByValue(((main_self)->y),c),c),_global_StringInit(1,")"),c);
;}
static inline struct _global_String main_Point_toStringByValue(struct main_Point d,struct _global_Context* c){
return main_Point_toString(&d,c);
}void _global_log_main_Point(struct main_Point _global_s, struct _global_Context* c){;
_global_c_log(main_Point_toString(&(_global_s),c),c);
;}

void mainInit() { 

_global_log_main_Point(main_PointInit(10,20),(&_global_context));
;
};