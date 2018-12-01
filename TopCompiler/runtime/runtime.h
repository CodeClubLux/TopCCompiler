#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>
#include <math.h>
#include <stdint.h>

struct _global_String {
    unsigned int length;
    char* data;
};

struct BoolType {};
struct StringType {};
struct NoneType {};
struct CharType {};

struct IntType {
    _Bool sign;
    unsigned int size;
};

struct FloatType {
    unsigned int size;
};