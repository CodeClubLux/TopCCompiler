struct _global_Maybe_int main_val;static inline struct _global_Maybe_int tmpmainb(struct _global_Maybe_Maybe_T c) {
struct _global_Maybe_int b;b.tag = c.tag;b.cases = *(union _global_Maybe_int_cases*) &(c.cases);return b;
}
struct _global_Maybe_int main_val2;static inline struct _global_Maybe_int tmpmainc(struct _global_Maybe_Maybe_T f) {
struct _global_Maybe_int d;d.tag = f.tag;d.cases = *(union _global_Maybe_int_cases*) &(f.cases);return d;
}
struct _global_Maybe_int main_val3;static inline struct _global_Maybe_int tmpmaind(struct _global_Maybe_Maybe_T h) {
struct _global_Maybe_int g;g.tag = h.tag;g.cases = *(union _global_Maybe_int_cases*) &(h.cases);return g;
}

void mainInitTypes() { 
 
_global_Maybe_intType.fields = _global_StaticArray_StaticArray_S_FieldInit(NULL, 0);
_global_Maybe_intType.package = _global_StringInit(7, "_global");
_global_Maybe_intType.name = _global_StringInit(9, "Maybe_int"); }
void mainInit() { 
main_val = tmpmainb(_global_None);;
main_val2 = tmpmainc(_global_None);;
main_val3 = tmpmaind(_global_None);;
struct _global_Maybe_int j =main_val;if(j.tag==0){int main_i = j.cases.Some.field0;

_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(5,"some "),_global_int_toStringByValue((main_i),(&_global_context)),(&_global_context)),_global_StringInit(0,""),(&_global_context)),(&_global_context));
;}
else if(1){
struct _global_Maybe_int k =main_val2;if(k.tag==0){int main_i = k.cases.Some.field0;

_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"some 2 "),_global_int_toStringByValue((main_i),(&_global_context)),(&_global_context)),_global_StringInit(0,""),(&_global_context)),(&_global_context));
;}
else if(1){
struct _global_Maybe_int l =main_val3;if(l.tag==0){int main_i = l.cases.Some.field0;

_global_log_string(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(7,"some 3 "),_global_int_toStringByValue((main_i),(&_global_context)),(&_global_context)),_global_StringInit(0,""),(&_global_context)),(&_global_context));
;}
else if(1){
_global_log_string(_global_StringInit(4,"hey!"),(&_global_context));
;}
;
;}
;
;}
;
;
};