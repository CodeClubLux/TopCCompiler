struct main_NoToString* _global_StaticArray_op_get_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, unsigned int _global_index, struct _global_Context* b);
struct _global_String _global_toString_main_NoToString(struct main_NoToString _global_s, struct _global_Context* c);
struct _global_String _global_StaticArray_join_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, struct _global_String _global_delimiter, struct _global_Context* c);
struct _global_String _global_StaticArray_toString_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, struct _global_Context* c);
struct _global_StaticArray_1_main_NoToString main_i;struct main_NoToString* _global_StaticArray_op_get_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, unsigned int _global_index, struct _global_Context* c){;
;
_global_assert(_global_index<1,_global_StringInit(13,"Out of bounds"),c);
;return ((_global_self)->data + (int64_t)_global_index);
;}
struct _global_String _global_toString_main_NoToString(struct main_NoToString _global_s, struct _global_Context* c){;
;return (&(_global_s))->toString(c);
;}
struct _global_String _global_StaticArray_join_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, struct _global_String _global_delimiter, struct _global_Context* c){;
;
;unsigned int d =1;
if(d==0){return _global_StringInit(0,"");}else if(d==1){return _global_toString_main_NoToString(*(_global_StaticArray_op_get_1_main_NoToString(_global_self,(unsigned int)0,c)),c);}else if(1){struct _global_String _global_s;_global_s = _global_StringInit(0,"");;
unsigned int _global_i;_global_i = 0;;
;while(_global_i<1-1){_global_s=_global_String_op_addByValue(_global_s,_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),main_NoToString_toStringByValue((*(_global_StaticArray_op_get_1_main_NoToString(_global_self,(unsigned int)_global_i,c))),c),c),_global_StringInit(0,""),c),(_global_delimiter),c),_global_StringInit(0,""),c),c);;_global_i=_global_i+1;;};
return _global_String_op_addByValue(_global_s,_global_toString_main_NoToString(*(_global_StaticArray_op_get_1_main_NoToString(_global_self,(unsigned int)1-1,c)),c),c);};
;}
struct _global_String _global_StaticArray_toString_1_main_NoToString(struct _global_StaticArray_1_main_NoToString* _global_self, struct _global_Context* c){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(2,"[ "),(_global_StaticArray_join_1_main_NoToString(_global_self,_global_StringInit(2,", "),c)),c),_global_StringInit(2," ]"),c);
;}

void mainInitTypes() { 
 
main_NoToStringType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
main_NoToStringType.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_NoToStringType_fields
,0
);
main_NoToStringType.package = _global_StringInit(4, "main");
main_NoToStringType.name = _global_StringInit(10, "NoToString");
main_NoToStringType.size = sizeof(struct main_NoToString);_global_StaticArray_1_main_NoToStringType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_1_main_NoToStringType.size->tag = 0;
_global_StaticArray_1_main_NoToStringType.size->cases.Static.field0 = 1;
_global_StaticArray_1_main_NoToStringType.array_type = 
_global_TypeFromStruct(
main_NoToString_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
; }
void mainInit() { 
main_i = _global_StaticArray_1_main_NoToStringInit(main_NoToStringInit());;
_global_log_string(_global_StaticArray_toString_1_main_NoToString(&(main_i),(&_global_context)),(&_global_context));
;
};