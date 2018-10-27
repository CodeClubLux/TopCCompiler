struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* n);

static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator**,struct _global_Allocator*,struct _global_Context* n);

struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator*,struct _global_Allocator*,struct _global_Context* n);
void _global_Array_reserve_string(struct _global_Array_string* _global_self, unsigned int _global_newSize, struct _global_Context* n);
struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String* _global_self, struct _global_Context* n);

static inline struct _global_String* _global_Maybe_unwrap_rstring(struct _global_String**,struct _global_Context* n);

struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String*,struct _global_Context* n);
struct _global_String* _global_Array_op_get_string(struct _global_Array_string* _global_self, unsigned int _global_index, struct _global_Context* n);
struct _global_String _global_toString_string(struct _global_String _global_s, struct _global_Context* n);
void _global_Array_append_string(struct _global_Array_string* _global_self, struct _global_String _global_value, struct _global_Context* n);
struct _global_String _global_Array_join_string(struct _global_Array_string* _global_self, struct _global_String _global_delimiter, struct _global_Context* n);
struct main_StringValue* _global_box_main_StringValue(struct main_StringValue _global_value, struct _global_Context* n);
struct _global_String main_Vec3_toString(struct main_Vec3* main_self, struct _global_Context* n){;
;return _global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(5,"Vec3("),_global_Float_toStringByValue(((main_self)->x),n),n),_global_StringInit(2,", "),n),_global_Float_toStringByValue(((main_self)->y),n),n),_global_StringInit(2,", "),n),_global_Float_toStringByValue(((main_self)->z),n),n),_global_StringInit(1,")"),n);
;}
static inline struct _global_String main_Vec3_toStringByValue(struct main_Vec3 p,struct _global_Context* n){
return main_Vec3_toString(&p,n);
}void main_Vec3_compile_vec3(struct main_Vec3* main_self, struct main_ShaderCompiler* main_codegen, struct _global_Context* n){;
;
main_ShaderCompiler_append(main_codegen,main_Vec3_toString(main_self,n),n);
;}
void main_StringValue_compile_string(struct main_StringValue* main_self, struct main_ShaderCompiler* main_codegen, struct _global_Context* n){;
;
main_ShaderCompiler_append(main_codegen,(main_self)->value,n);
;}
void main_ShaderCompiler_append(struct main_ShaderCompiler* main_self, struct _global_String main_s, struct _global_Context* n){;
;
_global_Array_append_string(&((main_self)->compiled),main_s,n);
;}
struct _global_String main_ShaderCompiler_toString(struct main_ShaderCompiler* main_self, struct _global_Context* n){;
;return _global_Array_join_string(&((main_self)->compiled),_global_StringInit(0,""),n);
;}
static inline struct _global_String main_ShaderCompiler_toStringByValue(struct main_ShaderCompiler p,struct _global_Context* n){
return main_ShaderCompiler_toString(&p,n);
}void main_ImageTexture_compile_vec3(struct main_ImageTexture* main_self, struct main_ShaderCompiler* main_codegen, struct _global_Context* n){;
;
main_ShaderCompiler_append(main_codegen,_global_StringInit(8,"Texture{"),n);
main_NodeString_compile_string(&((main_self)->file),main_codegen,n);
main_ShaderCompiler_append(main_codegen,_global_StringInit(1,"}"),n);
;}
void main_PbrBSDF_compile_vec3(struct main_PbrBSDF* main_self, struct main_ShaderCompiler* main_codegen, struct _global_Context* n){;
;
main_ShaderCompiler_append(main_codegen,_global_StringInit(4,"Pbr{"),n);
main_NodeVec3_compile_vec3(&((main_self)->color),main_codegen,n);
main_ShaderCompiler_append(main_codegen,_global_StringInit(1,"}"),n);
;}
void main_Output_compile_vec3(struct main_Output* main_self, struct main_ShaderCompiler* main_codegen, struct _global_Context* n){;
;
main_NodeVec3_compile_vec3(&((main_self)->frag),main_codegen,n);
;}
struct main_ImageTexture main_imageTexture;struct _global_Array_string tmpmainb(struct _global_Array_Array_T p) {
return *((struct _global_Array_string*) &p);};
struct _global_String main_compile_shader(struct main_Output main_shader_output, struct _global_Context* n){;
struct main_ShaderCompiler main_shader_compiler;main_shader_compiler = main_ShaderCompilerInit(tmpmainb(_global_empty_array(n)));;
main_Output_compile_vec3(&(main_shader_output),&(main_shader_compiler),n);
;return _global_Array_join_string(&((main_shader_compiler).compiled),_global_StringInit(0,""),n);
;}
struct _global_String main_make_simple_shader(struct _global_Context* n){struct main_StringValue main_source;main_source = main_StringValueInit(_global_StringInit(7,"assets/"));;
struct main_ImageTexture main_diffuse_color;main_diffuse_color = main_ImageTextureInit(main_NodeStringFromStruct(&(main_source), &main_StringValue_compile_string));;
struct main_PbrBSDF main_pbr_bsdf;main_pbr_bsdf = main_PbrBSDFInit(main_NodeVec3FromStruct(&(main_diffuse_color), &main_ImageTexture_compile_vec3));;
;return main_compile_shader(main_OutputInit(main_NodeVec3FromStruct(&(main_pbr_bsdf), &main_PbrBSDF_compile_vec3)),n);
;}
struct _global_Allocator* _global_Maybe_default_rAllocatorByValue(struct _global_Allocator* _global_self, struct _global_Allocator* _global_value, struct _global_Context* n){;
;
;struct _global_Allocator* p =_global_self;
if(p != NULL){struct _global_Allocator* _global_x= p;
return _global_x;}if(p == NULL){return _global_value;};
;}
static inline struct _global_Allocator* _global_Maybe_default_rAllocator(struct _global_Allocator** q,struct _global_Allocator* r,struct _global_Context* n){
return _global_Maybe_default_rAllocatorByValue(*q,r,n);
}
static inline struct _global_String* tmpmainc(struct _global_Array_string** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* n) {
struct _global_String* p =(*_global_self)->data;
if(p != NULL){struct _global_String* _global_data= p;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),n);
struct _global_String* _global_newData;_global_newData = (struct _global_String*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct _global_String),n));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(struct _global_String),n);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,n);
return _global_newData;}if(p == NULL){return (struct _global_String*)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct _global_String),n));}
}
void _global_Array_reserve_string(struct _global_Array_string* _global_self, unsigned int _global_newSize, struct _global_Context* n){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(n)->allocator,n);;
(_global_self)->allocator=_global_allocator;;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainc(&_global_self,&_global_newSize,&_global_allocator, n);;
;}
struct _global_String* _global_Maybe_unwrap_rstringByValue(struct _global_String* _global_self, struct _global_Context* n){;
;struct _global_String* p =_global_self;
if(p != NULL){struct _global_String* _global_x= p;
return _global_x;}if(p == NULL){_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),n);
return *(((struct _global_String**)(_global_alloc(0,n))));};
;}
static inline struct _global_String* _global_Maybe_unwrap_rstring(struct _global_String** q,struct _global_Context* n){
return _global_Maybe_unwrap_rstringByValue(*q,n);
}struct _global_String* _global_Array_op_get_string(struct _global_Array_string* _global_self, unsigned int _global_index, struct _global_Context* n){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),n);
;return (_global_Maybe_unwrap_rstringByValue((_global_self)->data,n) + _global_index);
;}
struct _global_String _global_toString_string(struct _global_String _global_s, struct _global_Context* n){;
;return _global_String_toString(&(_global_s),n);
;}
void _global_Array_append_string(struct _global_Array_string* _global_self, struct _global_String _global_value, struct _global_Context* n){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){;
if((_global_self)->capacity==0){;
_global_Array_reserve_string(_global_self,1,n);
;}
else{_global_Array_reserve_string(_global_self,(_global_self)->capacity*2,n);
;};
;};
*(((_global_Maybe_unwrap_rstringByValue((_global_self)->data,n) + (_global_self)->length)))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
struct _global_String _global_Array_join_string(struct _global_Array_string* _global_self, struct _global_String _global_delimiter, struct _global_Context* n){;
;
;unsigned int p =(_global_self)->length;
if(p==0){return _global_StringInit(0,"");}if(p==1){return _global_toString_string(*(_global_Array_op_get_string(_global_self,0,n)),n);}if(1){struct _global_String _global_s;_global_s = _global_StringInit(0,"");;
unsigned int _global_i;_global_i = 0;;
;while(_global_i<(_global_self)->length-1){_global_s=_global_String_op_addByValue(_global_s,_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(*(_global_Array_op_get_string(_global_self,_global_i,n))),n),_global_StringInit(0,""),n),(_global_delimiter),n),_global_StringInit(0,""),n),n);;_global_i=_global_i+1;;};
return _global_String_op_addByValue(_global_s,_global_toString_string(*(_global_Array_op_get_string(_global_self,(_global_self)->length-1,n)),n),n);};
;}
struct main_StringValue* _global_box_main_StringValue(struct main_StringValue _global_value, struct _global_Context* n){;
struct main_StringValue* _global_pointer;_global_pointer = (struct main_StringValue*)(_global_Allocator_alloc((n)->allocator,sizeof(struct main_StringValue),n));;
*(_global_pointer)=_global_value;;
;return _global_pointer;
;}

void mainInit() { 

main_imageTexture = main_ImageTextureInit(main_NodeStringFromStruct(_global_box_main_StringValue(main_StringValueInit(_global_StringInit(0,"")),(&_global_context)), &main_StringValue_compile_string));;
_global_log_string(main_make_simple_shader((&_global_context)),(&_global_context));
;
};