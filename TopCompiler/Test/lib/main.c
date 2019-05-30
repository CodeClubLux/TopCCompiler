struct main_Token* _global_StaticArray_op_get_8_main_Token(struct _global_StaticArray_8_main_Token* _global_self, unsigned int _global_index, struct _global_Context* k);
void _global_log_int(int _global_s, struct _global_Context* k);

#define main_atoi(k,l) atoi(k)
struct _global_StaticArray_8_main_Token main_tokens;unsigned int main_i;struct main_Token main_peek(struct _global_Context* m){;return *(_global_StaticArray_op_get_8_main_Token(&(main_tokens),(unsigned int)main_i+1,m));
;}
struct main_Token main_next(struct _global_Context* m){main_i = main_i+1;;
;return *(_global_StaticArray_op_get_8_main_Token(&(main_tokens),(unsigned int)main_i,m));
;}
struct main_Token main_current(struct _global_Context* m){;return *(_global_StaticArray_op_get_8_main_Token(&(main_tokens),(unsigned int)main_i,m));
;}

static inline int tmpmainb(struct main_Token* main_token, struct _global_Context* m) {
if(_global_String_op_eqByValue((*main_token).value,_global_StringInit(1,"("),m)){;
int main_expr;main_expr = main_parse((int)0,m);;
main_advance(_global_StringInit(1,")"),m);
return main_expr;}
else{_global_panic(_global_StringInit(12,"Unexpected )"),m);
return (int)0;}
}
int main_Token_nudByValue(struct main_Token main_token, struct _global_Context* m){;
;struct main_TokenType n =(main_token).kind;
if(n.tag==1){_global_panic(_global_StringInit(12,"Unexpected +"),m);
return (int)0;}else if(n.tag==3){return tmpmainb(&main_token, m);}else if(n.tag==0){return main_atoi(_global_String_to_c_stringByValue((main_token).value,m),m);}else if(n.tag==2){_global_panic(_global_StringInit(3,"EOF"),m);
return (int)0;};
;}
static inline int main_Token_nud(struct main_Token* p,struct _global_Context* m){
return main_Token_nudByValue(*p,m);
}
static inline int tmpmainc(struct main_Token* main_token,int* main_left, struct _global_Context* m) {
struct _global_String p =(*main_token).value;
if(_global_String_op_eqByValue(p,_global_StringInit(1,"+"),NULL)){return *main_left+main_parse((int)10,m);}else if(_global_String_op_eqByValue(p,_global_StringInit(1,"*"),NULL)){return *main_left*main_parse((int)20,m);}else if(1){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(18,"Unknown operator: "),((*main_token).value),m),_global_StringInit(0,""),m),m);
return (int)0;}
}
int main_Token_ledByValue(struct main_Token main_token, int main_left, struct _global_Context* m){;
;
;struct main_TokenType n =(main_token).kind;
if(n.tag==1){return tmpmainc(&main_token,&main_left, m);}else if(n.tag==2){_global_panic(_global_StringInit(3,"EOF"),m);
return (int)0;}else if(n.tag==3){_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(11,"Unexpected "),((main_token).value),m),_global_StringInit(0,""),m),m);
return (int)0;}else if(n.tag==0){_global_panic(_global_StringInit(17,"Unexpected number"),m);
return (int)0;};
;}
static inline int main_Token_led(struct main_Token* q,int r,struct _global_Context* m){
return main_Token_ledByValue(*q,r,m);
}struct main_Token main_token;void main_advance(struct _global_String main_expect, struct _global_Context* m){;
if(_global_String_op_neByValue((main_token).value,main_expect,m)){;
_global_panic(_global_String_op_addByValue(_global_String_op_addByValue(_global_StringInit(10,"Expected: "),(main_expect),m),_global_StringInit(0,""),m),m);
;};
main_token = main_next(m);;
;}
int main_parse(int main_rbp, struct _global_Context* m){;
struct main_Token main_t;main_t = main_current(m);;
main_token = main_next(m);;
int main_left;main_left = main_Token_nudByValue(main_t,m);;
;while(main_rbp<(main_token).lbp){main_t = main_token;;main_token = main_next(m);;main_left = main_Token_ledByValue(main_t,main_left,m);;};
;return main_left;
;}
struct main_Token* _global_StaticArray_op_get_8_main_Token(struct _global_StaticArray_8_main_Token* _global_self, unsigned int _global_index, struct _global_Context* m){;
;
_global_assert(_global_index<8,_global_StringInit(13,"Out of bounds"),m);
;return ((_global_self)->data + (int64_t)_global_index);
;}
void _global_log_int(int _global_s, struct _global_Context* m){;
_global_c_log(_global_int_toString(&(_global_s),m),m);
;}

void mainInitTypes() { 
 
main_Int.tag = 0;
main_Operator.tag = 1;
main_End.tag = 2;
main_Paren.tag = 3;
struct _global_Case* c =
(struct _global_Case*) malloc(sizeof(struct _global_Case) * 4);
c[0].name = _global_StringInit(3, "Int");
c[0].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
c[1].name = _global_StringInit(8, "Operator");
c[1].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
c[2].name = _global_StringInit(3, "End");
c[2].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
c[3].name = _global_StringInit(5, "Paren");
c[3].args = _global_StaticArray_StaticArray_S_CaseArgInit(malloc(sizeof(struct _global_CaseArg) * 0), 0);
main_TokenTypeType.tag_field.name = _global_StringInit(3, "tag");

main_TokenTypeType.tag_field.offset = offsetof(struct main_TokenType, tag);
main_TokenTypeType.tag_field.field_type = 
_global_TypeFromStruct(
_global_u8_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;

main_TokenTypeType.size = sizeof(struct main_TokenType);

main_TokenTypeType.package = _global_StringInit(4, "main");
main_TokenTypeType.name = _global_StringInit(9, "TokenType");
main_TokenTypeType.cases.data = c;
main_TokenTypeType.cases.length = 4;
main_TokenType_fields = (struct _global_Field*) malloc(sizeof(struct _global_Field) * 3);
main_TokenType.fields = _global_StaticArray_StaticArray_S_FieldInit(
main_TokenType_fields
,3
);
main_TokenType.package = _global_StringInit(4, "main");
main_TokenType.name = _global_StringInit(5, "Token");
main_TokenType.size = sizeof(struct main_Token);
main_TokenType_fields[0].name = _global_StringInit(5, "value");
main_TokenType_fields[0].offset = offsetof(struct main_Token, value);
main_TokenType_fields[0].field_type = 
_global_TypeFromStruct(
_global_String_get_type(NULL,(&_global_context))
,
&rStringType_VTABLE_FOR_Type
,
rStringType_VTABLE_FOR_Type.type
, &_global_StringType_toString
, &_global_StringType_get_size
)
;
main_TokenType_fields[1].name = _global_StringInit(4, "kind");
main_TokenType_fields[1].offset = offsetof(struct main_Token, kind);
main_TokenType_fields[1].field_type = 
_global_TypeFromStruct(
main_TokenType_get_type(NULL,(&_global_context))
,
&rEnumType_VTABLE_FOR_Type
,
rEnumType_VTABLE_FOR_Type.type
, &_global_EnumType_toString
, &_global_EnumType_get_size
)
;
main_TokenType_fields[2].name = _global_StringInit(3, "lbp");
main_TokenType_fields[2].offset = offsetof(struct main_Token, lbp);
main_TokenType_fields[2].field_type = 
_global_TypeFromStruct(
_global_int_get_type(NULL,(&_global_context))
,
&rIntType_VTABLE_FOR_Type
,
rIntType_VTABLE_FOR_Type.type
, &_global_IntType_toString
, &_global_IntType_get_size
)
;_global_StaticArray_8_main_TokenType.size = malloc(sizeof(struct _global_ArraySize));
_global_StaticArray_8_main_TokenType.size->tag = 0;
_global_StaticArray_8_main_TokenType.size->cases.Static.field0 = 8;
_global_StaticArray_8_main_TokenType.array_type = 
_global_TypeFromStruct(
main_Token_get_type(NULL,(&_global_context))
,
&rStructType_VTABLE_FOR_Type
,
rStructType_VTABLE_FOR_Type.type
, &_global_StructType_toString
, &_global_StructType_get_size
)
; }
void mainInit() { 
;
main_tokens = _global_StaticArray_8_main_TokenInit(main_TokenInit(_global_StringInit(1,"("),main_Paren,(int)0),main_TokenInit(_global_StringInit(2,"10"),main_Int,(int)0),main_TokenInit(_global_StringInit(1,"+"),main_Operator,(int)10),main_TokenInit(_global_StringInit(1,"6"),main_Int,(int)0),main_TokenInit(_global_StringInit(1,")"),main_Paren,(int)0),main_TokenInit(_global_StringInit(1,"*"),main_Operator,(int)20),main_TokenInit(_global_StringInit(1,"5"),main_Int,(int)0),main_TokenInit(_global_StringInit(0,""),main_End,(int)0));;
main_i = 0;;
main_token = main_current((&_global_context));;
_global_log_int(main_parse((int)0,(&_global_context)),(&_global_context));
;
};