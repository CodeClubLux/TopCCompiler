struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* c);
struct gizmo_Gizmo* ecs_Store_get_active_gizmo_Gizmo(struct ecs_Store_gizmo_Gizmo* ecs_self, struct _global_Context* c);
struct _global_Field* _global_StaticArray_op_get_StaticArray_S_Field(struct _global_StaticArray_StaticArray_S_Field* _global_self, unsigned int _global_index, struct _global_Context* c);
struct _global_StaticArray_4_materialSystem_Param main_substance_params(struct _global_String main_folder, struct _global_String main_name, struct _global_Context* c){;
;
;return _global_StaticArray_4_materialSystem_ParamInit(materialSystem_Param_Image(_global_StringInit(16,"material.diffuse"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"assets/"),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(14,"_basecolor.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(17,"material.metallic"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"assets/"),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(13,"_metallic.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(18,"material.roughness"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"assets/"),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(14,"_roughness.jpg"),c),c),c),materialSystem_Param_Image(_global_StringInit(15,"material.normal"),texture_load(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"assets/"),(main_folder),c),_global_StringInit(1,"/"),c),(main_name),c),_global_StringInit(11,"_normal.jpg"),c),c),c));
;}
struct _global_StaticArray_4_materialSystem_Param main_wet_street_params;struct model_Model main_cube;struct _global_StaticArray_StaticArray_S_materialSystem_Param tmpmainbL(struct _global_StaticArray_4_materialSystem_Param* c) {
return _global_StaticArray_StaticArray_S_materialSystem_ParamInit(c->data, 4);};
struct ecs_Entity* main_cube_entity;struct model_ModelRenderer* main_mesh_renderer;struct fpsController_FPSController* main_floating_camera;struct gizmo_Gizmo* main_gizmo_component;struct ibl_Skybox* main_skybox;struct main_Point main_s;struct _global_All main_wrapping_s;struct _global_All_VTABLE rmain_Point_VTABLE_FOR_All;struct _global_Type main_typ_of_s;struct _global_StaticArray_1_materialSystem_Material* _global_box__1_materialSystem_Material(struct _global_StaticArray_1_materialSystem_Material _global_value, struct _global_Context* g){;
struct _global_StaticArray_1_materialSystem_Material* _global_pointer;_global_pointer = (struct _global_StaticArray_1_materialSystem_Material*)(_global_Allocator_alloc((g)->allocator,sizeof(struct _global_StaticArray_1_materialSystem_Material),g));;
*(_global_pointer)=_global_value;;
;return _global_pointer;
;}
struct gizmo_Gizmo* ecs_Store_get_active_gizmo_Gizmo(struct ecs_Store_gizmo_Gizmo* ecs_self, struct _global_Context* g){;
struct _global_Range h =_global_RangeInit(0,((ecs_self)->components).length);
for (unsigned int j = h.start; j < h.end; j++) {
unsigned int ecs_i;ecs_i = j;
if(*(_global_Array_op_get_bool(&((ecs_self)->components_alive),ecs_i,g))){;
struct gizmo_Gizmo* ecs_comp;ecs_comp = &(*(_global_Array_op_get_gizmo_Gizmo(&((ecs_self)->components),ecs_i,g)));;
struct ecs_Entity* ecs_entity;ecs_entity = gizmo_Gizmo_get_entity(ecs_comp,g);;
if((ecs_entity)->enabled){;
return ecs_comp;
;
;};
;};
}
;
;return NULL;
;}
struct _global_Field* _global_StaticArray_op_get_StaticArray_S_Field(struct _global_StaticArray_StaticArray_S_Field* _global_self, unsigned int _global_index, struct _global_Context* g){;
;
_global_assert(_global_index<(_global_self)->length,_global_StringInit(13,"Out of bounds"),g);
;return ((_global_self)->data + _global_index);
;}

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
;struct _global_Field j[2];
main_PointType.fields = _global_StaticArray_StaticArray_S_FieldInit(
j
,2
);
main_PointType.package = _global_StringInit(4, "main");
main_PointType.name = _global_StringInit(5, "Point");
j[0].name = _global_StringInit(1, "x");
j[0].offset = offsetof(struct main_Point, x);
j[0].field_type = 
_global_TypeFromStruct(
_global_Float_get_type(NULL,(&_global_context))
,
&rFloatType_VTABLE_FOR_Type
,
rFloatType_VTABLE_FOR_Type.type
, &_global_FloatType_toString
)
;
j[1].name = _global_StringInit(1, "y");
j[1].offset = offsetof(struct main_Point, y);
j[1].field_type = 
_global_TypeFromStruct(
_global_Float_get_type(NULL,(&_global_context))
,
&rFloatType_VTABLE_FOR_Type
,
rFloatType_VTABLE_FOR_Type.type
, &_global_FloatType_toString
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
main_cube = model_load_model(_global_StringInit(15,"assets/cube.fbx"),tmpprimitivesF(_global_box__1_materialSystem_Material(_global_StaticArray_1_materialSystem_MaterialInit(materialSystem_MaterialInit(_global_StringInit(15,"DefaultMaterial"),shader_make(_global_StringInit(23,"assets/shaders/pbr.vert"),_global_StringInit(23,"assets/shaders/pbr.frag"),(&_global_context)),tmpmainbL(&(main_wet_street_params)))),(&_global_context))),(&_global_context));;
main_cube_entity = ecs_make_Entity((&_global_context));;
(main_cube_entity)->scale=math_Vec3Init(0.5,0.5,0.5);;
main_mesh_renderer = model_make_ModelRenderer(main_cube_entity,&(main_cube),(&_global_context));;
main_floating_camera = fpsController_make_FPSController(camera_get_camera((&_global_context)),(&_global_context));;
main_gizmo_component = _global_Maybe_unwrap_rgizmo_GizmoByValue(ecs_Store_get_active_gizmo_Gizmo(gizmo_gizmo_system,(&_global_context)),(&_global_context));;
gizmo_Gizmo_set_target(main_gizmo_component,(main_cube_entity)->id,(&_global_context));
_global_log_string(_global_StringInit(7,"running"),(&_global_context));
main_skybox = ibl_make_Skybox(_global_StringInit(44,"assets/LA_Downtown_Helipad_GoldenHour_3k.hdr"),(&_global_context));;
main_s = main_PointInit((float)10,(float)20);;
main_wrapping_s = _global_AllFromStruct(&(main_s),&rmain_Point_VTABLE_FOR_All,_global_TypeFromStruct(main_Point_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString));;
main_typ_of_s = _global_All_get_typeByValue(main_wrapping_s,(&_global_context));;
struct _global_Type c =main_typ_of_s;if(c.vtable->type.data == NULL){struct _global_StructType* main_x = (struct _global_StructType*)c.data;
struct _global_StaticArray_StaticArray_S_Field d =(main_x)->fields;
for (unsigned int f = 0;f < d.length; f++) {
struct _global_Field main_field;unsigned int main_i;main_field = *_global_StaticArray_op_get_StaticArray_S_Field(&d, f, (&_global_context));
main_i = f;
_global_log_string((main_field).name,(&_global_context));
}
;
;}
else if(1){
_global_log_string(_global_StringInit(21,"I dont know what s is"),(&_global_context));
;}
;
runner_init((&_global_context));
;
};