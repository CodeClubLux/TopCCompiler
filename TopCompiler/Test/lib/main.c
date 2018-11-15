struct main_Recursive main_r;struct _global_Array_main_Recursive tmpmainb(struct _global_Array_Array_T b) {
return *((struct _global_Array_main_Recursive*) &b);};

void mainInit() { 
_global_Array_main_RecursiveType.size.tag = 1;
_global_Array_main_RecursiveType.array_type = 
_global_TypeFromStruct(
main_Recursive_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
)
;main_RecursiveType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 1);
main_RecursiveType.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_RecursiveType_fields
,1
);
main_RecursiveType.package = _global_StringInit(4, "main");
main_RecursiveType.name = _global_StringInit(9, "Recursive");
main_RecursiveType_fields[0].name = _global_StringInit(3, "has");
main_RecursiveType_fields[0].offset = offsetof(struct main_Recursive, has);
main_RecursiveType_fields[0].field_type = 
_global_TypeFromStruct(
_global_Array_main_Recursive_get_type(NULL,(&_global_context))
,
&rArrayType_VTABLE_FOR_Type
,
rArrayType_VTABLE_FOR_Type.type
, &_global_ArrayType_toString
)
;_global_Maybe_rmain_RecursiveType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_rmain_RecursiveType.package = _global_StringInit(7, "_global");
_global_Maybe_rmain_RecursiveType.name = _global_StringInit(21, "Maybe_rmain_Recursive");
main_r = main_RecursiveInit(tmpmainb(_global_empty_array((&_global_context))));;
;
};