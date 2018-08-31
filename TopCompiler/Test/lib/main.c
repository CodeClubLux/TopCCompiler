
struct _global_StaticArray_4_materialSystem_Param {
struct materialSystem_Param data[4];
};
struct _global_StaticArray_4_materialSystem_Param _global_StaticArray_4_materialSystem_ParamFill_array(struct materialSystem_Param with){
struct _global_StaticArray_4_materialSystem_Param tmp;
for (unsigned int i = 0; i < 4; i++) {
tmp.data[i] = with;
}; return tmp; }
struct _global_StaticArray_4_materialSystem_Param _global_StaticArray_4_materialSystem_ParamInit(struct materialSystem_Param b,struct materialSystem_Param c,struct materialSystem_Param d,struct materialSystem_Param f){
struct _global_StaticArray_4_materialSystem_Param tmp;
tmp.data[0] = b;
tmp.data[1] = c;
tmp.data[2] = d;
tmp.data[3] = f;
return tmp; }
struct main_ExampleScene {
};
static inline struct main_ExampleScene main_ExampleSceneInit(){
struct main_ExampleScene b;
return b;
};

void _global_Array_reserve_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, unsigned int _global_newSize, struct _global_Context* b);
struct materialSystem_Material* _global_box_materialSystem_Material(struct materialSystem_Material _global_value, struct _global_Context* c);
void _global_Array_append_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, struct materialSystem_Material* _global_value, struct _global_Context* c);
void _global_Array_shorten_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, unsigned int _global_num, struct _global_Context* c);
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct _global_Array_Array_T main_sky_box_params;struct materialSystem_Material* main_wet_street;struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmainv(struct _global_StaticArray_4_materialSystem_Param* c) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(c->data, 4);};
struct materialSystem_Material* main_sky_box;struct modelLoading_Model main_skybox_cube;struct modelLoading_Model main_model;struct shader_Shader main_my_shader;struct _global_StaticArray_16_float main_identity;void main_ExampleScene_render(struct main_ExampleScene* main_self, struct _global_Context* c){;
opengl_depthFunc(opengl_lequal,c);
modelLoading_Model_renderByValue(main_skybox_cube,c);
opengl_depthFunc(opengl_less,c);
modelLoading_Model_renderByValue(main_model,c);
;}
void main_ExampleScene_update(struct main_ExampleScene* main_self, struct _global_Context* c){;
;}
struct main_ExampleScene main_example_scene;
static inline struct materialSystem_Material** tmpmainw(struct _global_Array_rmaterialSystem_Material** _global_self,unsigned int* _global_newSize,struct _global_Allocator** _global_allocator, struct _global_Context* c) {
struct materialSystem_Material** d =(*_global_self)->data;
if(d != NULL){struct materialSystem_Material** _global_data= d;
_global_assert(*_global_newSize>=(*_global_self)->length,_global_StringInit(16,"Truncating array"),c);
struct materialSystem_Material** _global_newData;_global_newData = (struct materialSystem_Material**)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct materialSystem_Material*),c));;
_global_memcpy((void*)_global_newData,(void*)_global_data,(*_global_self)->length*sizeof(struct materialSystem_Material*),c);
_global_Allocator_dealloc(*_global_allocator,(void*)_global_data,c);
return _global_newData;}if(d == NULL){return (struct materialSystem_Material**)(_global_Allocator_alloc(*_global_allocator,(*_global_self)->capacity*sizeof(struct materialSystem_Material*),c));}
}
void _global_Array_reserve_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, unsigned int _global_newSize, struct _global_Context* c){;
;
struct _global_Allocator* _global_allocator;_global_allocator = _global_Maybe_default_rAllocatorByValue((_global_self)->allocator,(c)->allocator,c);;
(_global_self)->capacity=_global_newSize;;
(_global_self)->data=tmpmainw(&_global_self,&_global_newSize,&_global_allocator, c);;
;}
struct materialSystem_Material* _global_box_materialSystem_Material(struct materialSystem_Material _global_value, struct _global_Context* c){;
struct materialSystem_Material* _global_pointer;_global_pointer = (struct materialSystem_Material*)(_global_Allocator_alloc((c)->allocator,sizeof(struct materialSystem_Material),c));;
*_global_pointer=_global_value;;
;return _global_pointer;
;}
void _global_Array_append_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, struct materialSystem_Material* _global_value, struct _global_Context* c){;
;
unsigned int _global_newLength;_global_newLength = (_global_self)->length+1;;
if(_global_newLength>(_global_self)->capacity){if((_global_self)->capacity==0){_global_Array_reserve_rmaterialSystem_Material(_global_self,1,c);
;}
else{_global_Array_reserve_rmaterialSystem_Material(_global_self,(_global_self)->capacity*2,c);
;};
;};
*((_global_Maybe_unwrap_rmaterialSystem_Material_rrmaterialSystem_MaterialByValue((_global_self)->data,c) + (_global_self)->length))=_global_value;;
(_global_self)->length=_global_newLength;;
;}
void _global_Array_shorten_rmaterialSystem_Material(struct _global_Array_rmaterialSystem_Material* _global_self, unsigned int _global_num, struct _global_Context* c){;
;
(_global_self)->length=(_global_self)->length-_global_num;;
if((_global_self)->length<0){_global_panic(_global_StringInit(21,"shorten out of bounds"),c);
;};
;}

void mainInit() { 

windowInit();;
;
bufferInit();;
shaderInit();;
imageLoaderInit();;
modelLoadingInit();;
;
main_wet_street_params = _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_basecolor.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),imageLoader_load(_global_StringInit(48,"assets/wet_street/Pebble_Wet_street_metallic.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_roughness.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),imageLoader_load(_global_StringInit(50,"assets/wet_street/Pebble_Wet_street_Normal_Map.jpg"),(&_global_context)),(&_global_context)));;
main_sky_box_params = _global_empty_array((&_global_context));;
main_wet_street = _global_box_materialSystem_Material(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(23,"assets/shaders/pbr.vert"),_global_StringInit(23,"assets/shaders/pbr.frag"),(&_global_context)),tmpmainv(&main_wet_street_params)),(&_global_context));;
main_sky_box = _global_box_materialSystem_Material(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(26,"assets/shaders/skybox.vert"),_global_StringInit(26,"assets/shaders/skybox.frag"),(&_global_context)),_global_StaticArray_StaticArray_S_materialSystem_ParamInit(main_sky_box_params.data, main_sky_box_params.length)),(&_global_context));;
_global_Array_append_rmaterialSystem_Material(&materialSystem_materials,main_sky_box,(&_global_context));
main_skybox_cube = modelLoading_load_model(_global_StringInit(15,"assets/cube.fbx"),(&_global_context));;
_global_Array_shorten_rmaterialSystem_Material(&materialSystem_materials,1,(&_global_context));
_global_Array_append_rmaterialSystem_Material(&materialSystem_materials,main_wet_street,(&_global_context));
main_model = modelLoading_load_model(_global_StringInit(15,"assets/cube.fbx"),(&_global_context));;
main_my_shader = shader_make(_global_StringInit(18,"assets/vertex.vert"),_global_StringInit(20,"assets/fragment.frag"),(&_global_context));;
main_identity = math_identity_mat((&_global_context));;
main_example_scene = main_ExampleSceneInit();;
scene_Scene_init(((&_global_context))->scene,scene_GameFromStruct(&main_example_scene, &main_ExampleScene_update, &main_ExampleScene_render),(&_global_context));
;
};