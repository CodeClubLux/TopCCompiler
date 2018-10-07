struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct materialSystem_Material* main_wet_street;struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmainbH(struct _global_StaticArray_4_materialSystem_Param* b) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(b->data, 4);};
struct model_Model main_cube;struct ecs_Entity* main_cube_entity;struct model_ModelRenderer* main_mesh_renderer;struct fpsController_FPSController* main_floating_camera;struct ibl_Skybox* main_skybox;
void mainInit() { 

windowInit();;
;
bufferInit();;
shaderInit();;
imageLoaderInit();;
modelInit();;
;
fpsControllerInit();;
_global_log_string(_global_StringInit(20,"about to load images"),(&_global_context));
main_wet_street_params = _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_basecolor.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),imageLoader_load(_global_StringInit(48,"assets/wet_street/Pebble_Wet_street_metallic.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),imageLoader_load(_global_StringInit(49,"assets/wet_street/Pebble_Wet_street_roughness.jpg"),(&_global_context)),(&_global_context)),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),imageLoader_load(_global_StringInit(50,"assets/wet_street/Pebble_Wet_street_Normal_Map.jpg"),(&_global_context)),(&_global_context)));;
main_wet_street = _global_box_materialSystem_Material(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(23,"assets/shaders/pbr.vert"),_global_StringInit(23,"assets/shaders/pbr.frag"),(&_global_context)),tmpmainbH(&(main_wet_street_params))),(&_global_context));;
_global_Array_append_rmaterialSystem_Material(&(materialSystem_materials),main_wet_street,(&_global_context));
main_cube = model_load_model(_global_StringInit(15,"assets/cube.fbx"),(&_global_context));;
main_cube_entity = ecs_make_Entity((&_global_context));;
(main_cube_entity)->scale=math_Vec3Init(0.5,0.5,0.5);;
main_mesh_renderer = model_make_ModelRenderer(model_ModelRendererInit(main_cube_entity,&(main_cube)),(&_global_context));;
main_floating_camera = fpsController_make_FPSController(camera_get_camera((&_global_context)),(&_global_context));;
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_skybox = ibl_make_Skybox(_global_StringInit(28,"assets/Tropical_Beach_3k.hdr"),(&_global_context));;
runner_init((&_global_context));
;
};