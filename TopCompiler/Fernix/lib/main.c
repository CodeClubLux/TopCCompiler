atomic_uint main_counter;void main_Task1_run(struct main_Task1* main_self, struct _global_Context* c){;
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(17,"got assigned id: "),_global_uint_toStringByValue((((c)->thread_info)->id),c),c),_global_StringInit(0,""),c),c);
struct _global_Range d =_global_RangeInit(0,10000);
for (unsigned int f = d.start; f < d.end; f++) {
unsigned int main_i;main_i = f;
atomic_atomic_uint_incr(&(main_counter),1,c);
}
;
;}
struct sync_WaitGroup main_wg;struct main_Task1 main_task1;struct task_Task_VTABLE rmain_Task1_VTABLE_FOR_task_Task;
void mainInitTypes() { 
 runnerInitTypes();windowInitTypes();windowInitTypes();keyInitTypes();keyInitTypes();mathInitTypes();mathInitTypes();shaderInitTypes();shaderInitTypes();textureInitTypes();textureInitTypes();ecsInitTypes();ecsInitTypes();layermaskInitTypes();layermaskInitTypes();sBufferInitTypes();sBufferInitTypes();cameraInitTypes();cameraInitTypes();transformInitTypes();transformInitTypes();lightsInitTypes();lightsInitTypes();inputInitTypes();inputInitTypes();timeInitTypes();timeInitTypes();taskInitTypes();
main_Task1Type_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 0);
main_Task1Type.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_Task1Type_fields
,0
);
main_Task1Type.package = _global_StringInit(4, "main");
main_Task1Type.name = _global_StringInit(5, "Task1");
main_Task1Type.size = sizeof(struct main_Task1); }
void mainInit() { 
runnerInit();;
windowInit();;
windowInit();;
keyInit();;
keyInit();;
mathInit();;
mathInit();;
shaderInit();;
shaderInit();;
textureInit();;
textureInit();;
ecsInit();;
ecsInit();;
layermaskInit();;
layermaskInit();;
sBufferInit();;
sBufferInit();;
cameraInit();;
cameraInit();;
transformInit();;
transformInit();;
lightsInit();;
lightsInit();;
inputInit();;
inputInit();;
timeInit();;
timeInit();;
taskInit();;
task_create_worker_threads(7,(&_global_context));
main_counter = atomic_make_atomic_uint(0,(&_global_context));;
main_wg = sync_make_WaitGroup((&_global_context));;
main_task1 = main_Task1Init();;
struct _global_Range c =_global_RangeInit(0,100);
for (unsigned int d = c.start; d < c.end; d++) {
unsigned int main_i;main_i = d;
sync_WaitGroup_wait_on(&(main_wg),task_HighPriority,task_TaskFromStruct(&(main_task1),&rmain_Task1_VTABLE_FOR_task_Task,_global_TypeFromStruct(main_Task1_get_type(NULL,(&_global_context)),&rStructType_VTABLE_FOR_Type,rStructType_VTABLE_FOR_Type.type, &_global_StructType_toString, &_global_StructType_get_size), &main_Task1_run),(&_global_context));
}
;
sync_WaitGroup_wait(&(main_wg),(&_global_context));
_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(9,"counter: "),_global_uint_toStringByValue((atomic_atomic_uint_load(&(main_counter),(&_global_context))),(&_global_context)),(&_global_context)),_global_StringInit(0,""),(&_global_context)),(&_global_context));
;
};