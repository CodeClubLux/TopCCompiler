struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* c);
struct gizmo_Gizmo* ecs_Store_get_active_gizmo_Gizmo_gizmo_Gizmo(struct ecs_Store_gizmo_Gizmo* ecs_self, struct _global_Context* c);
struct gizmo_Gizmo* _global_Maybe_unwrap_rgizmo_GizmoByValue(struct gizmo_Gizmo* _global_self, struct _global_Context* c);

static inline struct gizmo_Gizmo* _global_Maybe_unwrap_rgizmo_Gizmo(struct gizmo_Gizmo**,struct _global_Context* c);

struct gizmo_Gizmo* _global_Maybe_unwrap_rgizmo_GizmoByValue(struct gizmo_Gizmo*,struct _global_Context* c);
struct _global_StaticArray_4_materialSystem_Param main_substance_params(struct _global_String main_folder, struct _global_String main_name, struct _global_Context* c){;
;
;return _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(14,"_basecolor.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(13,"_metallic.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(14,"_roughness.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(0,""),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(11,"_normal.jpg"),c),c),c));
;}
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct model_Model* main_cube;struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmaincM(struct _global_StaticArray_4_materialSystem_Param* c) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(c->data, 4);};
struct ecs_Entity* main_cube_entity;struct model_ModelRenderer* main_mesh_renderer;struct fpsController_FPSController* main_floating_camera;struct gizmo_Gizmo* main_gizmo_component;struct ibl_Skybox* main_skybox;struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* c){;
struct _global_StaticArray_1_materialSystem_Material* _global_pointer;_global_pointer = (struct _global_StaticArray_1_materialSystem_Material*)(_global_Allocator_alloc((c)->allocator,sizeof(struct _global_StaticArray_1_materialSystem_Material),c));;
*(_global_pointer)=_global_value;;
;return _global_pointer;
;}
struct gizmo_Gizmo* ecs_Store_get_active_gizmo_Gizmo_gizmo_Gizmo(struct ecs_Store_gizmo_Gizmo* ecs_self, struct _global_Context* c){;
struct _global_StaticArray_StaticArray_S_ecs_Slot_gizmo_Gizmo_ d =(ecs_self)->components;
for (unsigned int f = 0;f < d.length; f++) {
struct ecs_Slot_gizmo_Gizmo ecs_slot;unsigned int ecs_i;ecs_slot = *_global_StaticArray_op_get_StaticArray_S_ecs_Slot_gizmo_Gizmo_(&d, f, c);
ecs_i = f;
struct gizmo_Gizmo* ecs_active_comp;;
struct gizmo_Gizmo* g =ecs_Store_index_active_gizmo_Gizmo(ecs_self,ecs_i,c);if(g != NULL){ecs_active_comp = g;

;}
else if(1){
 continue;;
;}
;
return ecs_active_comp;
;
}
;
;return NULL;
;}
struct gizmo_Gizmo* _global_Maybe_unwrap_rgizmo_GizmoByValue(struct gizmo_Gizmo* _global_self, struct _global_Context* c){;
struct gizmo_Gizmo* _global_x;;
struct gizmo_Gizmo* d =_global_self;if(d != NULL){_global_x = d;

;}
else if(1){
_global_panic(_global_StringInit(38,"Trying to unwrap maybe, which was None"),c);
;}
;
;return _global_x;
;}
static inline struct gizmo_Gizmo* _global_Maybe_unwrap_rgizmo_Gizmo(struct gizmo_Gizmo** f,struct _global_Context* c){
return _global_Maybe_unwrap_rgizmo_GizmoByValue(*f,c);
}
void mainInit() { 
_global_StaticArray_4_materialSystem_ParamType.size.tag = 0;
_global_StaticArray_4_materialSystem_ParamType.size.cases.Static.field0 = 4;
_global_StaticArray_4_materialSystem_ParamType.array_type = 
_global_TypeFromStruct(
materialSystem_Param_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
)
;
windowInit();;
;
bufferInit();;
shaderInit();;
textureInit();;
modelInit();;
;
fpsControllerInit();;
gizmoInit();;
main_wet_street_params = main_substance_params(_global_StringInit(6,"wood_2"),_global_StringInit(13,"Stylized_Wood"),(&_global_context));;
main_cube = model_load_model(_global_StringInit(13,"HOVERTANK.fbx"),tmpprimitivesM(_global_box__1_materialSystem_Material(_global_StaticArray_1_materialSystem_MaterialInit(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(16,"shaders/pbr.vert"),_global_StringInit(16,"shaders/pbr.frag"),(&_global_context)),tmpmaincM(&(main_wet_street_params)))),(&_global_context))),(&_global_context));;
main_cube_entity = ecs_make_Entity(ecs_make_ID((&_global_context)),(&_global_context));;
(main_cube_entity)->scale=math_Vec3Init(0.5,0.5,0.5);;
main_mesh_renderer = model_make_ModelRenderer((main_cube_entity)->id,(&_global_context));;
(main_mesh_renderer)->model=main_cube;;
main_floating_camera = fpsController_make_FPSController((camera_Camera_get_entity(camera_get_camera((&_global_context)),(&_global_context)))->id,(&_global_context));;
main_gizmo_component = _global_Maybe_unwrap_rgizmo_GizmoByValue(ecs_Store_get_active_gizmo_Gizmo_gizmo_Gizmo(gizmo_gizmo_system,(&_global_context)),(&_global_context));;
editor_Editor_select(&(editor_editor),(main_cube_entity)->id,(&_global_context));
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_skybox = ibl_make_Skybox(ecs_make_ID((&_global_context)),_global_StringInit(37,"LA_Downtown_Helipad_GoldenHour_3k.hdr"),(&_global_context));;
runner_init((&_global_context));
;
};