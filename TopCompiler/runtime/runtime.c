#define __Context struct _global_Context* context
#define alloc _global_Allocator_alloc

struct _global_String _global_StringInit(unsigned int length, char* data) {
    struct _global_String s;
    s.data = data;
    s.length = length;
    return s;
};
struct _global_String _global_String_toStringByValue(struct _global_String s,__Context) {
    return s;
}

struct _global_String _global_String_toString(struct _global_String* s,__Context) {
    return *s;
}

struct _global_String _global_Bool_toStringByValue(_Bool b, __Context) {
    if (b) {
        return _global_StringInit(4, "true");
    } else {
        return _global_StringInit(5, "false");
    }
}

#include <stdatomic.h>

void c_runtime_incr_atomic_uint(volatile atomic_uint* a, unsigned int value) {
    *a += value;
}

atomic_flag c_runtime_ATOMIC_FLAG_INIT = ATOMIC_FLAG_INIT;




struct BoolType _global_Bool_typ;

struct BoolType* _global_Bool_get_typeByValue(_Bool b, __Context) {
    return &_global_Bool_typ;
}

struct BoolType* _global_Bool_get_type(_Bool* b, __Context) {
    return &_global_Bool_typ;
}

struct CharType _global_Char_typ;

struct CharType* _global_char_get_typeByValue(char b, __Context) {
    return &_global_Char_typ;
}

struct CharType* _global_char_get_type(char* b, __Context) {
    return &_global_Char_typ;
}

struct _global_String _global_CharType_toString(struct CharType* self, __Context) {
    return _global_StringInit(4, "char");
}

struct _global_String _global_Bool_toString(_Bool* b, __Context) {
    return _global_Bool_toStringByValue(*b, context);
}


struct _global_String _global_String_sliceByValue(struct _global_String s, unsigned int from, unsigned int end, __Context) {
    int length = end - from;
    char* buffer = alloc(context->allocator, sizeof(char) * length + 1, context);
    memcpy(buffer, s.data + from, length);
    buffer[length] = '\0';
    return _global_StringInit(length, buffer);
}

char* _global_String_op_getByValue(struct _global_String s, unsigned int i, __Context) {
    if (i >= s.length) {
        printf("String acess out of bounds: %i", i);
        exit(1);
    }
    return &s.data[i];
}

_Bool _global_String_op_eqByValue(struct _global_String self, struct _global_String other, __Context) {
    if (self.length != other.length) {
        return 0;
    }

    for (unsigned int i =0; i < self.length; i++) {
        if (self.data[i] != other.data[i]) {
            return 0;
        }
    }
    return 1;
}

_Bool _global_String_op_eq(struct _global_String* s, struct _global_String* other, __Context) {
    return _global_String_op_eqByValue(*s, *other, context);
}

_Bool _global_String_op_neByValue(struct _global_String s, struct _global_String o, __Context) {
    return !_global_String_op_eqByValue(s,o,context);
}

void _global_log(struct _global_String,__Context);

struct _global_String _global_String_op_addByValue(struct _global_String a, struct _global_String b,__Context) {
    if (a.length == 0) {
        return b;
    } else if (b.length == 0) {
        return a;
    }

    struct _global_String newString;
    newString.length = a.length + b.length;
    newString.data = alloc(context->allocator, sizeof(char) * (newString.length+1), context);

    memcpy(newString.data, a.data, sizeof(char) * a.length);
    memcpy(newString.data + a.length, b.data, sizeof(char) * (b.length + 1));
    return newString;
};

struct _global_String _global_String_op_add(struct _global_String* a, struct _global_String b,__Context) {
    return _global_String_op_addByValue(*a, b, context);
}

struct _global_String _global_Float_toStringByValue(float x,__Context) {
    int len = snprintf(NULL, 0, "%f", x);
    char *result = (char *)alloc(context->allocator, len + 1, context);
    snprintf(result, len + 1, "%f", x);
    return _global_StringInit(len,result);
}

struct _global_String _global_Float_toString(float* x,__Context) {
    return _global_Float_toStringByValue(*x, context);
}

struct FloatType _global_FloatType;

struct FloatType* _global_Float_get_type(float* x, __Context) {
    return &_global_FloatType;
}

struct FloatType* _global_Float_get_typeByValue(float x, __Context) {
    return &_global_FloatType;
}

void _reverse_string(struct _global_String * self) {
    unsigned int half_length = self->length / 2;

    for (unsigned int i = 0; i < half_length; i++) {
        char tmp = self->data[i];
        self->data[i] = self->data[self->length - 1 - i];
        self->data[self->length - 1 - i] = tmp;
    }
}

struct NoneType _global_NoneTypeInit() {
    struct NoneType s;
    return s;
}

struct NoneType None_Type;

/*
void itoa(int value, char* str, int base) {
	static char num[] = "0123456789abcdefghijklmnopqrstuvwxyz";
	char* wstr=str;

	int sign;
	// Validate base
	if (base<2 || base>35){ *wstr='\0'; return; }
	// Take care of sign

	if ((sign=value) < 0) value = -value;
	// Conversion. Number is reversed.

	do *wstr++ = num[value%base]; while(value/=base);

	if(sign<0) *wstr++='-';

	*wstr='\0';
	// Reverse string
}
*/

struct _global_String _global_int_toStringByValue(int number,__Context) {
    unsigned int length = 1;
    unsigned int divisor = 10;

    int absNumber = number;
    if (absNumber < 0) {
        absNumber = -absNumber;
    }

    while (absNumber % divisor != absNumber) {
        length++;
        divisor *= 10;
    }

    if (number < 0) {
        length++;
    }

    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);

    struct _global_String newString = _global_StringInit(length, memory);
    snprintf(newString.data, 10, "%d", number);

    return newString;
}

struct _global_String _global_int_toString(int* number,__Context) {
    return _global_int_toStringByValue(*number, context);
}

char* _global_String_to_c_string(struct _global_String* s, __Context) {
    return s->data;
}

char* _global_String_to_c_stringByValue(struct _global_String s, __Context) {
    return s.data;
}

struct IntType _global_IntType;

#define gen_integer(name, typ, sign_of_int) struct _global_String _global_##name##_toString(typ* number,__Context) {\
return _global_int_toStringByValue(*number, context); \
} \
struct _global_String _global_##name##_toStringByValue(typ number,__Context) {\
return _global_int_toStringByValue(number, context); \
} \
\
struct IntType _global_##name##Type;\
void _global_##name##TypeInit() { \
    _global_##name##Type.sign = sign_of_int; \
    _global_##name##Type.size = sizeof(typ); \
} \
struct IntType* _global_##name##_get_typeByValue(typ number, __Context) { \
    return &_global_##name##Type; \
} \
\
struct IntType* _global_##name##_get_type(typ* number, __Context) { \
    return &_global_##name##Type; \
}

struct IntType* _global_int_get_typeByValue(int number, __Context) {
    return &_global_IntType;
}

struct IntType* _global_int_get_type(int* number, __Context) {
    return &_global_IntType;
}


gen_integer(uint, unsigned int, 0)
gen_integer(u8, uint8_t, 0)
gen_integer(u16, uint16_t, 0)
gen_integer(u32, uint32_t, 0)
gen_integer(u64, uint64_t, 0)

gen_integer(i8, int8_t, 1)
gen_integer(i16, int16_t, 1)
gen_integer(i32, int32_t, 1)
gen_integer(i64, int64_t, 1)

void _global_c_log(struct _global_String s) {
    printf("%s\n", s.data);
    fflush(stdout);
};

static inline void* _global_offsetPtr(void* ptr, int offset, __Context) {
    return ((char*)ptr) + offset;
};

struct _global_String _global_console_input(struct _global_String text, __Context) {
    char string[40];
    fputs(text.data, stdout);
    fflush(stdout);
    fgets(string, sizeof(string), stdin);
    fflush(stdin);

    unsigned int length = strlen(string) - 1;
    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);
    memcpy(memory, string, length + 1);
    return _global_StringInit(length, memory);
}



FILE* _runtime_c_open_file(struct _global_String filename, struct _global_String acess) {
    char * buffer = 0;
    int length;
    FILE* f;
    #ifdef __APPLE__
        f = fopen(filename.data, acess.data);
    #else
        errno_t errors = fopen_s(&f, filename.data, acess.data);

        if (f == NULL && errors) {
            printf("%s\n", filename.data);
            printf("%i\n", (int)f);
            printf("error %i\n", errors);
            return NULL;
        }
    #endif

    return f;
}

#include <sys/stat.h>

struct _global_String _runtime_read_file(FILE* f, struct _global_String filename, __Context) {
    struct stat info[1];

    stat (filename.data, info);
    int length = info->st_size;
    char* buffer = alloc(context->allocator, length + 1, context);

    length = fread(buffer, sizeof(char), sizeof(char) * length, f);
    buffer[length] = '\0';

    return _global_StringInit(length, buffer);
}

void _runtime_write_file(FILE* f, struct _global_String s, __Context) {
    fwrite(s.data, sizeof(char), sizeof(char) * s.length, f);
}

void _runtime_c_close_file(FILE* file) {
    fclose (file);
}

struct _global_String _runtime_char_buffer_toString(char* buffer) {
    return _global_StringInit(strlen(buffer), buffer);
}

//char

struct _global_String _global_char_toStringByValue(char self, __Context) {
    char* buffer = alloc(context->allocator, 2, context);
    buffer[0] = self;
    buffer[1] = '\0';
    return _global_StringInit(1, buffer);
}

struct _global_String _global_char_toString(char* self, __Context) {
    return _global_char_toStringByValue(*self, context);
}

uint8_t _global_char_toU8ByValue(char self, __Context) {
    return (uint8_t) self;
}

uint8_t _global_char_toU8(char* self, __Context) {
    return (uint8_t) *self;
}

_Bool _global_String_starts_withByValue(struct _global_String str, struct _global_String pre, __Context) {
    if (str.length < pre.length) { return 0; }
    return strncmp(pre.data, str.data, pre.length) == 0;
}

_Bool _global_String_ends_withByValue(struct _global_String str, struct _global_String pre, __Context) {
    if (str.length < pre.length) { return 0; }
    return strncmp(pre.data, str.data + (str.length - pre.length), pre.length) == 0;
}


#define _global_indexPtr(value, by, c) value + by
#define _global_c_set_bit_to(number, n, x) (number & ~(1U << n) | (x << n))
#define _global_c_is_bit_set(number, n) ((number >> n) & 1U)
#define _global_c_bit_and(x,y) x & y

/*
void printI(int i) {
    printf("%i\n", i);
};
*/


struct StringType _global_StringType;

struct StringType* _global_String_get_type(struct _global_String* s, __Context) {
    return &_global_StringType;
}

struct StringType* _global_String_get_typeByValue(struct _global_String s, __Context) {
    return &_global_StringType;
}

struct _global_PointerType pointerTypes[200];
unsigned int pointerTypeCounter;

struct _global_PointerType* _global_boxPointerType(struct _global_PointerType p, __Context) {
    if (pointerTypeCounter > 199) {
        printf("More pointer types than available");
    }

    pointerTypes[pointerTypeCounter++] = p;
    return &pointerTypes[pointerTypeCounter - 1];
}


void _global_init_c_runtime() {
    printf("Initialized types\n");

    pointerTypeCounter = 0;
    _global_FloatType.size = sizeof(float);
    _global_IntType.sign = 1;
    _global_IntType.size = sizeof(int);

    _global_u8TypeInit();
    _global_u16TypeInit();
    _global_u32TypeInit();
    _global_u64TypeInit();
    _global_uintTypeInit();

    _global_i8TypeInit();
    _global_i16TypeInit();
    _global_i32TypeInit();
    _global_i64TypeInit();

    /*
    _global_##name##TypeInit()
    gen_integer(uint, unsigned int, 0)
gen_integer(u8, uint8_t, 0)
gen_integer(u16, uint16_t, 0)
gen_integer(u32, uint32_t, 0)
gen_integer(u64, uint64_t, 0)

gen_integer(i8, int8_t, 1)
gen_integer(i16, int16_t, 1)
gen_integer(i32, int32_t, 1)
gen_integer(i64, int64_t, 1) */
}