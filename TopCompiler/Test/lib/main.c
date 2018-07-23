
struct main_Nullable_Value {
int field0;

};struct main_Nullable {
 char tag;
union {
struct main_Nullable_Value Value;

};};
struct main_Nullable main_Value(int b){
struct main_Nullable c;
c.Value.field0 = b;c.tag = 0;
return c;}
struct main_Nullable main_Null;
struct main_Nullable main_s;
void mainInit() { 
main_Null.tag = 1;
main_s = main_Value(10);;
struct main_Nullable d =main_s;if(d.tag==0){int main_x = d.Value.field0;
;
_global_log(_global_Int_toString(main_x));};
if(d.tag==1){;
_global_log(_global_StringInit(4,"null"));};
;
;
};