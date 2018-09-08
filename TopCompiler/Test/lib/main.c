
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

struct scene_Game* _global_box_scene_Game(struct scene_Game _global_value, struct _global_Context* b);
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct _global_Array_Array_T main_sky_box_params;struct materialSystem_Material* main_wet_street;struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmainz(struct _global_StaticArray_4_materialSystem_Param* c) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(c->data, 4);};
struct modelLoading_Model main_model;struct shader_Shader main_my_shader;struct _global_StaticArray_16_float main_identity;struct ibl_Skybox main_skybox;void main_ExampleScene_render(struct main_ExampleScene* main_self, struct _global_Context* c){;
ibl_Skybox_render(&main_skybox,c);
modelLoading_Model_renderByValue(main_model,c);
;}
void main_ExampleScene_set_scene_params_for(struct main_ExampleScene* main_self, struct shader_Shader main__shader, struct _global_Context* c){;
;
ibl_Skybox_set_ibl_params_for(&main_skybox,main__shader,c);
;}
void main_ExampleScene_update(struct main_ExampleScene* main_self, struct _global_Context* c){;
;}
struct main_ExampleScene main_example_scene;struct scene_Game* _global_box_scene_Game(struct scene_Game _global_value, struct _global_Context* c){;
struct scene_Game* _global_pointer;_global_pointer = (struct scene_Game*)(_global_Allocator_alloc((c)->allocator,sizeof(struct scene_Game),c));;
*_global_pointer=_global_value;;
;return _global_pointer;
;}

void mainInit() { 

windowInit();;
;
bufferInit();;
shaderInit();;
imageLoaderInit();;
modelLoadingInit();;
;
iblInit();;
main_wet_street_params = _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_basecolor.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),imageLoader_load(_global_StringInit(48,"assets/wet_street/Pebble_Wet_street_metallic.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_roughness.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),imageLoader_load(_global_StringInit(50,"assets/wet_street/Pebble_Wet_street_Normal_Map.jpg"),(&_global_context)),(&_global_context)));;
main_sky_box_params = _global_empty_array((&_global_context));;
main_wet_street = _global_box_materialSystem_Material(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(23,"assets/shaders/pbr.vert"),_global_StringInit(23,"assets/shaders/pbr.frag"),(&_global_context)),tmpmainz(&main_wet_street_params)),(&_global_context));;
_global_Array_append_rmaterialSystem_Material(&materialSystem_materials,main_wet_street,(&_global_context));
main_model = modelLoading_load_model(_global_StringInit(15,"assets/cube.fbx"),(&_global_context));;
main_my_shader = shader_make(_global_StringInit(18,"assets/vertex.vert"),_global_StringInit(20,"assets/fragment.frag"),(&_global_context));;
main_identity = math_identity_mat((&_global_context));;
main_skybox = ibl_make_Skybox((&_global_context));;
main_example_scene = main_ExampleSceneInit();;
scene_Scene_init(((&_global_context))->scene,_global_box_scene_Game(scene_GameFromStruct(&main_example_scene, &main_ExampleScene_update, &main_ExampleScene_render, &main_ExampleScene_set_scene_params_for),(&_global_context)),(&_global_context));
;
};