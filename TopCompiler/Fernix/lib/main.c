struct _global_StaticArray_4_materialSystem_Param main_substance_params(struct _global_String main_folder, struct _global_String main_name, struct _global_Context* d){;
;
;return _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),d),_global_StringInit(1,"/"),d),(main_name),d),_global_StringInit(14,"_basecolor.jpg"),d),d),d),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),d),_global_StringInit(1,"/"),d),(main_name),d),_global_StringInit(13,"_metallic.jpg"),d),d),d),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),d),_global_StringInit(1,"/"),d),(main_name),d),_global_StringInit(14,"_roughness.jpg"),d),d),d),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),d),_global_StringInit(1,"/"),d),(main_name),d),_global_StringInit(11,"_normal.jpg"),d),d),d));
;}
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct _global_StaticArray_1_materialSystem_Material main_cube_materials;struct _global_StaticArray_StaticArray_S_materialSystem_Material tmpmaindy(struct _global_StaticArray_1_materialSystem_Material* f) {
return _global_StaticArray_StaticArray_S_materialSystem_MaterialInit(f->data, 1);};
void main_make_cube(struct _global_Context* d){struct model_Model* main_cube;main_cube = model_load_model(_global_StringInit(13,"HOVERTANK.fbx"),d);;
unsigned int main_id;main_id = ecs_make_ID(d);;
ecs_make_Entity(main_id,d);
struct transform_Transform* main_cube_transform;main_cube_transform = transform_make_Transform(main_id,d);;
(main_cube_transform)->scale=math_Vec3Init(0.5,0.5,0.5);;
struct model_ModelRenderer* main_mesh_renderer;main_mesh_renderer = model_make_ModelRenderer(main_id,d);;
(main_mesh_renderer)->model_id=_global_Some_ecs_ID(ecs_Store_id_of_model_Model(model_models,main_cube,d),d);;
model_ModelRenderer_set_materials(main_mesh_renderer,tmpmaindy(&(main_cube_materials)),d);
;}
struct fpsController_FPSController* main_floating_camera;struct ibl_Skybox* main_skybox;
void mainInitTypes() { 
 windowInitTypes();runnerInitTypes();fpsControllerInitTypes();
_global_StaticArray_1_materialSystem_MaterialType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_1_materialSystem_MaterialType.size->tag = 0;
_global_StaticArray_1_materialSystem_MaterialType.size->cases.Static.field0 = 1;
_global_StaticArray_1_materialSystem_MaterialType.array_type = 
_global_TypeFromStruct(
materialSystem_Material_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
; }
void mainInit() { 
windowInit();;
runnerInit();;
;
;
fpsControllerInit();;
;
main_wet_street_params = main_substance_params(_global_StringInit(6,"wood_2"),_global_StringInit(13,"Stylized_Wood"),(&_global_context));;
main_cube_materials = _global_StaticArray_1_materialSystem_MaterialInit(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(16,"shaders/pbr.vert"),_global_StringInit(16,"shaders/pbr.frag"),(&_global_context)),tmpmodelSettingscy(&(main_wet_street_params)),&(draw_default_state)));;
main_floating_camera = fpsController_make_FPSController(ecs_Store_id_of_camera_Camera(camera_cameras,camera_get_camera((&_global_context)),(&_global_context)),(&_global_context));;
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_skybox = ibl_make_Skybox(ecs_make_ID((&_global_context)),_global_StringInit(21,"Tropical_Beach_3k.hdr"),(&_global_context));;
runner_init((&_global_context));
;
};