_Bool _global_Maybe_is_none_rlister_NameByValue(struct lister_Name* _global_self, struct _global_Context* f);

static inline _Bool _global_Maybe_is_none_rlister_Name(struct lister_Name**,struct _global_Context* f);

_Bool _global_Maybe_is_none_rlister_NameByValue(struct lister_Name*,struct _global_Context* f);
struct _global_StaticArray_5_materialSystem_Param main_wet_street_params;struct _global_StaticArray_1_materialSystem_Material main_cube_materials;void main_make_cube(struct _global_Context* f){struct model_Model* main_cube;main_cube = model_load_model(_global_StringInit(10,"sphere.fbx"),f);;
unsigned int main_id;main_id = ecs_make_ID(f);;
ecs_make_Entity(main_id,f);
struct transform_Transform* main_cube_transform;main_cube_transform = transform_make_Transform(main_id,f);;
(main_cube_transform)->position=math_Vec3Init((float)0,(float)5,(float)-(1));;
(main_cube_transform)->scale=math_Vec3Init(0.5,0.5,0.5);;
struct model_ModelRenderer* main_mesh_renderer;main_mesh_renderer = model_make_ModelRenderer(main_id,f);;
(main_mesh_renderer)->model_id=_global_Some_ecs_ID(ecs_Store_id_of_model_Model(model_models,main_cube,f),f);;
model_ModelRenderer_set_materials(main_mesh_renderer,tmpcameraSb(&(main_cube_materials)),f);
struct physics_RigidBody* main_rb;main_rb = ecs_Store_make_physics_RigidBody(physics_rigid_bodies,main_id,f);;
(main_rb)->shape=physics_Sphere(0.5,f);;
(main_rb)->mass=(float)1;;
(main_rb)->continous=1;;
;}
void main_make_floor_collider(struct _global_Context* f){unsigned int main_id;main_id = ecs_make_ID(f);;
ecs_make_Entity(main_id,f);
struct transform_Transform* main_floor_transform;main_floor_transform = transform_make_Transform(main_id,f);;
(main_floor_transform)->position=math_Vec3Init((float)0,(float)0,(float)0);;
struct physics_RigidBody* main_rb;main_rb = ecs_Store_make_physics_RigidBody(physics_rigid_bodies,main_id,f);;
(main_rb)->shape=physics_Plane(math_Vec3Init((float)0,(float)1,(float)0),f);;
(main_rb)->mass=(float)0;;
;}
void main_make_floor(struct _global_Context* f){unsigned int main_id;main_id = ecs_make_ID(f);;
ecs_make_Entity(main_id,f);
struct transform_Transform* main_floor_transform;main_floor_transform = transform_make_Transform(main_id,f);;
(main_floor_transform)->position=math_Vec3Init((float)0,(float)0,(float)0);;
(main_floor_transform)->scale=math_Vec3Init((float)100,(float)1,(float)100);;
(main_floor_transform)->rotation=math_make_quat((math_radians((float)90,f)),math_Vec3Init((float)1,(float)0,(float)0),f);;
struct model_Model* main_plane;main_plane = model_load_model(_global_StringInit(9,"plane.fbx"),f);;
struct model_ModelRenderer* main_model_renderer;main_model_renderer = model_make_ModelRenderer(main_id,f);;
(main_model_renderer)->model_id=_global_Some_ecs_ID(ecs_Store_id_of_model_Model(model_models,main_plane,f),f);;
model_ModelRenderer_set_materials(main_model_renderer,tmpcameraSb(&(main_cube_materials)),f);
;}
struct lights_DirLight* main_main_light;struct ibl_Skybox* main_skybox;_Bool _global_Maybe_is_none_rlister_NameByValue(struct lister_Name* _global_self, struct _global_Context* f){;
;struct lister_Name* g =_global_self;
if(g != NULL&&1){return 0;}else if(g == NULL){return 1;};
;}
static inline _Bool _global_Maybe_is_none_rlister_Name(struct lister_Name** h,struct _global_Context* f){
return _global_Maybe_is_none_rlister_NameByValue(*h,f);
}
void mainInitTypes() { 
 windowInitTypes();runnerInitTypes();fpsControllerInitTypes();bowWeaponInitTypes();
 }
void mainInit() { 
windowInit();;
runnerInit();;
;
;
;
fpsControllerInit();;
bowWeaponInit();;
modelSettings_make_default_prefabs((&_global_context));
modelSettings_make_default_terrain_prefabs((&_global_context));
main_wet_street_params = materialSystem_substance_params(_global_StringInit(10,"wet_street"),_global_StringInit(17,"Pebble_Wet_street"),(&_global_context));;
main_cube_materials = _global_StaticArray_1_materialSystem_MaterialInit(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_Shader_get_id(materialSystem_pbr_shader,(&_global_context)),tmpmaterialSystembn(&(main_wet_street_params)),&(draw_default_state)));;
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_main_light = lights_get_dir_light((&_global_context));;
if(_global_Maybe_is_none_rlister_NameByValue((ecs_Store_by_id_lister_Name(lister_named,ecs_Store_id_of_lights_DirLight(lights_dir_lights,main_main_light,(&_global_context)),(&_global_context))),(&_global_context))){;
struct lister_Name* main_name;main_name = ecs_Store_make_lister_Name(lister_named,ecs_Store_id_of_lights_DirLight(lights_dir_lights,main_main_light,(&_global_context)),(&_global_context));;
(main_name)->name=_global_StringInit(8,"dirLight");;
;};
model_load_in_place(model_load_model(_global_StringInit(9,"plane.fbx"),(&_global_context)),(&_global_context));
main_skybox = ibl_make_Skybox(ecs_make_ID((&_global_context)),_global_StringInit(37,"LA_Downtown_Helipad_GoldenHour_3k.hdr"),(&_global_context));;
runner_init((&_global_context));
;
};