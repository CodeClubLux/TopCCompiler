#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct _global_String {
    unsigned int length;
    unsigned int capacity;
    char* data;
};

struct _global_String _global_StringInit(unsigned int length, char* data) {
    struct _global_String s;
    s.data = data;
    s.length = length;
    s.capacity = 0;
    return s;
};

struct _global_String _global_String_op_add(struct _global_String a, struct _global_String b) {
    if (a.length == 0) {
        return b;
    } else if (b.length == 0) {
        return a;
    }

    struct _global_String newString;
    newString.length = a.length + b.length;
    newString.data = malloc(sizeof(char) * (newString.length+1));
    memcpy(newString.data, a.data, sizeof(char) * a.length);
    memcpy(newString.data + a.length, b.data, sizeof(char) * (b.length + 1));
    return newString;
};



struct _global_String _global_String_append(struct _global_String self, struct _global_String other) {
    if (other.length == 0) {
        return self;
    }

    struct _global_String newString;
    newString.length = self.length + other.length;
    if (self.capacity < newString.length) {
        if (self.capacity != 0) {
            free(newString.data);
        }

        newString.capacity = newString.length * 2; //double capacity
        newString.data = malloc(sizeof(char) * (newString.capacity+1));
        memcpy(newString.data, self.data, sizeof(char) * self.length);
    } else {
        newString.capacity = self.capacity;
        newString.data = self.data;
    }

    memcpy(newString.data + self.length, other.data, sizeof(char) * (other.length + 1));
    return newString;
};

void _reverse_string(struct _global_String * self) {
    unsigned int half_length = self->length / 2;
    for (unsigned int i = 0; i < half_length; i++) {
        char tmp = self->data[i];
        self->data[i] = self->data[self->length - 1 - i];
        self->data[self->length - 1 - i] = tmp;
    }
}

void _itoa(int value, char* str, int base) {
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

struct _global_String _global_Int_toString(int number) {
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

    struct _global_String newString = _global_StringInit(length, malloc(sizeof(char) * (length + 1)));
    newString.capacity = newString.length;

    _itoa(number, newString.data, 10);
    _reverse_string(&newString);

    return newString;
}

void _global_log(struct _global_String s) {
    printf("%s", s.data);
};

void main_logMessage_int(int main_value){;
_global_log(_global_String_op_add(_global_String_op_add(_global_StringInit(17,"printed message: "),_global_Int_toString((main_value))),_global_StringInit(0,"")));}
int main() { 
main_logMessage_int(10);
; return 0;};