#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

#define Context struct _global_Context* context
#define alloc _global_Allocator_allocByValue

struct _global_String {
    unsigned int length;
    char* data;
};

struct _global_String _global_StringInit(unsigned int length, char* data) {
    struct _global_String s;
    s.data = data;
    s.length = length;
    return s;
};
struct _global_String _global_String_toStringByValue(struct _global_String s, Context) {
    return s;
}

struct _global_String _global_String_toString(struct _global_String* s, Context) {
    return *s;
}

void _global_log(struct _global_String, Context);

struct _global_String _global_String_op_addByValue(struct _global_String a, struct _global_String b, Context) {
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

struct _global_String _global_String_op_add(struct _global_String* a, struct _global_String b, Context) {
    return _global_String_op_addByValue(*a, b, context);
}

void _reverse_string(struct _global_String * self) {
    unsigned int half_length = self->length / 2;

    for (unsigned int i = 0; i < half_length; i++) {
        char tmp = self->data[i];
        self->data[i] = self->data[self->length - 1 - i];
        self->data[self->length - 1 - i] = tmp;
    }
}

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

struct _global_String _global_int_toStringByValue(int number, Context) {
    unsigned int length = 1;
    unsigned int divisor = 10;

    int absNumber = number;
    if (absNumber < 0) {
        absNumber *= -1;
    }

    while (number % divisor != absNumber) {
        length++;
        divisor *= 10;
    }

    if (number < 0) {
        length++;
    }


    char* memory = alloc(context->allocator, sizeof(char) * (length + 1), context);

    struct _global_String newString = _global_StringInit(length, memory);

    itoa(number, newString.data, 10);
    _reverse_string(&newString);

    return newString;
}

struct _global_String _global_uint_toStringByValue(unsigned int number, Context) {
    return _global_int_toStringByValue(number, context);
}

struct _global_String _global_int_toString(int* n, Context) {
    return _global_int_toStringByValue(*n, context);
}

struct _global_String _global_uint_toString(unsigned int* n, Context) {
    return _global_int_toStringByValue(*n, context);
}

void _global_log(struct _global_String s, Context) {
    printf("%s\n", s.data);
};

static inline void* _global_offsetPtr(void* ptr, int offset, Context) {
    return ((char*)ptr) + offset;
};

/*
void printI(int i) {
    printf("%i\n", i);
};
*/
