# Top Compiler <img src="https://github.com/CodeClubLux/TopCompiler/blob/master/arrow.png" width="40" height="40"> 

Compiler for the Top programming language to C, written in python3.6.

The Top programming language, also known as Toplang is a imperative programming language with functional features such as pattern matching and ADT. It is designed to be low level while having clean syntax and being aimed at rapid development. They key being able to hotswap the code just by saving the file. It implements performant features without increasing friction such as context based allocation, allowing code not caring about allocations to easily switch to efficient allocators. The default allocator being a linear allocator that just deletes all data at the end of the frame, which means most of the time freeing memory is necessary. In addition, it will have the ability to easily switch between AOS and SOA as well as have relative pointers and lightweight fibers and go like concurrency.  

## Installing Top-Lang
1. If not already downloaded, download python3.
2. Then type into your terminal 'pip install TopCompiler'

## For the latest copy
1. Clone this repo
2. Cd into the downloaded clone
3. Call 'python3 setup.py install'

## Setting Up a New Project
1. Open up terminal or command prompt`
2. Cd into the directory you wish to create the project folder in.
3. Execute `topc new project HelloWorld`, this will create a new top project in the current directory
4. Execute `cd HelloWorld`, this will go into the project directory
5. Execute `topc new package main`, this will create a new main package inside the src directory, which will contain a port.json file for configurations, the main package and it the entry point to your application
7. Execute `topc run`, to build and run your program.
## Introduction

Blocks in Top are delimited by whitespace. Indenting blocks are required to be with spaces and not tabs to facilitate platform independence. In addition, newlines end statements if the expression is not further indented and there are no unclosed parenthesis.

Function must called without parenthesis, the function call will then end following the normal statement ending rule
```scala
func 10, 5
```

While in c, this is perfectly normal
```c
func(10,5) + 89
```
In top you should write this instead, because otherwise you would be passing the tuple (10,5) plus 89 to func
```scala
(func 10, 5) + 80
```

## Compiling
Just re-enter and execute the `topc run`. In the future there will be hotswapping and re-compilation on file save.
## Literals
### Integers
Integers are the same as in c, however they may contain underscores to make them more readable.
```scala
1_000_000
```

Their type signature is written as `int`, although there are also `i8`, `i16`, `i32`, `i64` which are each of their respective size.
To make an int unsigned either use `uint`, or use `u` in stead of `i` for the other sized ints.

### Floats
Floats can have underscores as Integers and must have a dot in the middle or end with an `f`.
```scala
3.51296
9f
```

Float's type signature is `float`.

### Boolean
Boolean can only have two values: `true` or `false`. Their type signature is `bool`.

### Strings
Strings look the same as c strings but various utility methods and have a length. For compatibility with c, they are zero terminated so their buffers are actually one character longer than their length. 
```scala
"hello toplang"
```

However strings can also be interpolated with an expression inside the braces as long as the value has a toString method.
```scala
"fib(20) = {6765}"
```

Their type signature is `string`

### Chars

Chars are the same as in c, sharing the same type signature, however they will not be implicitly converted to ints. 
```
'a'
```

### None
The `none` type is a type which represents the absence of a value like void in c.

## Functions

### Defining named functions

The syntax for defining functions is the `def` keyword followed by the function name and opening parenthesis then list the arguments followed by a colon and the argument type seperated by `,`, followed by a closing parenthesis and a return type, if no return type is specified the return type of the function is `none`, the function beings with an `=`. 

```scala
def add(a: int, b: int) int =
  a + b
```

### Conditionals and Loops

## If, Elif, Else

The if statement in top is both an expression and a statement, it expects a boolean as a condition and will return the last expression in the body.
The else statement does what you would expect and elif is the same as if else in c.

```scala
x := 10

log 
    if x == 10 then 10
    elif x > 20 then 30
    else 30
```

## While Loop
```scala
x := 0
while x < 10 do
    log "x is {x}
    x++
``` 

## break, continue, return

Break will exit the current loop, continue will skipping the rest of the body of a loop and will return will skip the rest of the body of a function 

### Pointers

Pointers are the adresses to some data. There is no concept of null in top so there can't be any null pointer dereferences. 
However this does not mean that acessing a pointer is always safe as the data could have been freed. This is the problem with automatic memory management but it is necessary for games. 
Passing an object by reference means you don't make a copy which can be slow and you can modify the original data when passed to a function or struct.
The size of a pointer is around 32bit-64bit depending on the platform.


```scala
def func() &int =
    ì := 10
    
    pointerToI := &i //takes the references
    *pointerToI = 20
    
    log i //will print 20
    
    i //don't do this!!!!! The variable i will no longer exist once this function returns so the pointer is pointing to garbage which will cause problems.

//do this instead

def funcWhichAllocates() &int =
    pointerToInt := alloc::[int]! /*
        ! just means calling a function which doesn't take any arguments
        ::[..] sets the generic parameters of the function. Generics will be explained below
    */
    *pointerToInt = 20
    
    log i //will print 20
    i //this is ok, just remember to free, otherwise this might cause a memory leak  
    // in most cases you won't have to free because the default allocator in top is just a linear buffer and can be freed in one go
    // setting what allocator will be described later as well 
```

### Structs

```scala
type Point =
    x: int
    y: int
    
type Point2 =
    x: int
    y: int
    
p := Point{ 10, 20 } //this will create a new point, x = 10, y = 20
p2 := Point{ x = 10, y = 20 } //this will also create a new point
```

This will create a struct called point with the fields x and y. Although `Point` and `Point2` are structurally the same the type system will complain as the type equality is based on name. 

### Interfaces

```scala
type Point2 with
    x: int
    y: int
    
p : Point2 = Point{ 10, 20 } //note this will use dynamic dispatch which is slower as the compiler doesn't know the exact type.

p2 : { x: int, y: int } = Point{ 10, 20 } //the other way of defining interfaces, using the syntax {..}
    
type Stringer with
    def toString() string =  //this means to convert a type to a Stringer it must have the method toString
```

### Alias
```scala
type P is Point //used to create a name equivalent to another type 

p : P = Point{ 10, 20 }
```

### Enum or ADT
```scala
type List =
    
    
``

### Methods
Methods are functions which are attached to a particular data type. 
You can attach methods to Structs, Enums and Aliases (only if the alias does not already have that method)

scala
``` 
def Point.toString(&self) string = //this will add the method to Point, self is of type `&Point`
    "Point({self.x}, {self.y})"
    
def Point.incr(&self) =
    self.x += 10
    
i := Point{ 0, 0 }
i.incr! 
log i /*
    this will not print Point(10, 0), but Point(0,0)
    this is because it will create a copy of the point which will be passed to Point.toIncr
    meaning i is never modified.
    Now you may ask why self in methods is always a reference and you can't choose which one is to allow dynamic dispatch
    Dynamic dispatch requires the data to be the same size which is only possible if it is a pointer
*/

&i.incr!

log i /* this will print Point(10, 0)

```

### #addToContext

In top there is an extra parameter passed to every function implicitly. This is the context variable of type `&Context`.
To change this 



### Features coming soon

Defer will be added and will behave the same as in go but end at the end of a scope and not of the function.
Hotswapping
using statement which allows variables to become namespaces, usefull for struct composition and shorting stuff such as `self.transform.position.x` into `position.x`
For loop which will iterate through an interator simmilar to python
Lightweight fibers and a job system