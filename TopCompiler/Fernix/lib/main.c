struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* b);
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct model_Model main_cube;struct _global_StaticArray_StaticArray_S_materialSystem_Material tmpmainbV(struct _global_StaticArray_1_materialSystem_Material* c) {
return _global_StaticArray_StaticArray_S_materialSystem_MaterialInit(c->data, 1);};
struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmainbW(struct _global_StaticArray_4_materialSystem_Param* c) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(c->data, 4);};
struct ecs_Entity* main_cube_entity;struct model_ModelRenderer* main_mesh_renderer;struct fpsController_FPSController* main_floating_camera;struct ibl_Skybox* main_skybox;struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* c){;
struct _global_StaticArray_1_materialSystem_Material* _global_pointer;_global_pointer = (struct _global_StaticArray_1_materialSystem_Material*)(_global_Allocator_alloc((c)->allocator,sizeof(struct _global_StaticArray_1_materialSystem_Material),c));;
*(_global_pointer)=_global_value;;
;return _global_pointer;
;}

void mainInit() { 

windowInit();;
;
bufferInit();;
shaderInit();;
textureInit();;
modelInit();;
;
fpsControllerInit();;
gizmoInit();;
main_wet_street_params = _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),texture_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_basecolor.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),texture_load(_global_StringInit(48,"assets/wet_street/Pebble_Wet_street_metallic.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),texture_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_roughness.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),texture_load(_global_StringInit(50,"assets/wet_street/Pebble_Wet_street_Normal_Map.jpg"),(&_global_context)),(&_global_context)));;
main_cube = model_load_model(_global_StringInit(20,"assets/HOVERTANK.fbx"),tmpmainbV(_global_box__1_materialSystem_Material(_global_StaticArray_1_materialSystem_MaterialInit(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(23,"assets/shaders/pbr.vert"),_global_StringInit(23,"assets/shaders/pbr.frag"),(&_global_context)),tmpmainbW(&(main_wet_street_params)))),(&_global_context))),(&_global_context));;
main_cube_entity = ecs_make_Entity((&_global_context));;
main_mesh_renderer = model_make_ModelRenderer(model_ModelRendererInit(main_cube_entity,&(main_cube)),(&_global_context));;
main_floating_camera = fpsController_make_FPSController(camera_get_camera((&_global_context)),(&_global_context));;
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_skybox = ibl_make_Skybox(_global_StringInit(28,"assets/Tropical_Beach_3k.hdr"),(&_global_context));;
runner_init((&_global_context));
;
};