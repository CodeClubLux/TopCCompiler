# Top Compiler <img src="https://github.com/CodeClubLux/TopCompiler/blob/master/arrow.png" width="40" height="40"> 

Compiler for the Top programming language, written in python3.6. The language compiles to C and then calls clang to convert it to machine code.

The Top programming language, also known as Toplang is a imperative programming language with functional features such as pattern matching, conditionals that return values and ADTs. It is designed to be low level while having clean syntax and powerfull but simple features. One example of this is context based allocation, allowing code to not care about allocations and then when needed fine tune the allocator strategy. The default allocator being a linear allocator that just deletes all data at the end of the frame. This means most of the time freeing memory is unnecessary. The next important features is interfaces which allows decoupling of code while still being performant when using generics that must fullfill an interface. In addition, lightweight fibers have been implemented with a couple synchronization primitives, such as atomic counters, locks and a thread safe queue (see TopCompiler/Fernix/concurrency). Furthermore, top supports full runtime introspection, radically simplifying serialization and editors.

Features that are hopefully coming soon, are the ability to switch between AOS and SOA, hot swapping and runtime type reflection. 

## Installing Top-Lang
1. If not already downloaded, download python3 and clang.
2. Then download this repo and cd into it from the command line
5. Run the command python3 setup.py install, to install the compiler in the path

## Setting Up a New Project
1. Open up terminal or command prompt`
2. Cd into the directory you wish to create the project folder in.
3. Execute `topc new project HelloWorld`, this will create a new top project in the current directory
4. Execute `cd HelloWorld`, this will go into the project directory
5. Execute `topc new package main`, this will create a new main package inside the src directory, which will contain a port.json file for configurations, the main package which is the entry point to your application
7. Execute `topc run`, to build and run your program.
8. Execute `topc debug`, to build your program with debug symbols (to add #line defintions, uncomment a line in codegen.py), note this is temporary and I will add a flag). 

## Introduction

## File structure

/
  /src - Put all your source files in here
      port.json - Sets the project settings
      *.top - Single file module
      */*.top - This is also a single file module as long as there is no port.json in this directory
      */
        port.json - Json files that has all the options for the module
        *.top
      
  /lib - The c output from the compiler
  /bin - The compiled binaries
  

  
## Example Project
Take a look inside of TopCompiler/Fernix for the beginings of a game engine written in Top. Also, check TopCompiler/TopRuntime which is the runtime, also written in top.

## Small Guide to Top

Blocks in Top are delimited by whitespace. Indenting blocks are required to be with spaces and not tabs to facilitate platform independence. In addition, newlines end statements if the expression is not further indented and there are no unclosed parenthesis.

Function must be called without parenthesis, the function call will then end following the normal statement ending rule
```scala
func 10, 5
```

While in c, this is perfectly normal
```c
func(10,5) + 89
```
In top you should write this instead, because otherwise you would be passing the tuple (10,5) plus 89 to func, note tuple's don't currently compile
```scala
(func 10, 5) + 80
```

## Compiling
Just re-enter and execute the `topc run` inside of your project. In the future there will be hotswapping and re-compilation on file save.
## Literals
### Integers
Integers are the same as in c, however they may contain underscores to make them more readable.
```scala
1_000_000
```

Their type signature is written as `int`, although there are also `i8`, `i16`, `i32`, `i64` which are each of their respective size.
To make an int unsigned either use `uint`, or use `u` instead of `i` for the other sized ints.

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
Strings look the same as c strings but have various utility methods and have a length. For compatibility with c, they are zero terminated so their buffers are actually one character longer than their length. Strings have a length field, which is an `uint` and a data field which is a pointer to the `Char` buffer. 

```scala
"hello toplang"
```

However strings can also be interpolated with an expression inside the braces as long as the value has a toString method.
```scala
"fib(20) = {6765}"
```

Their type signature is `string`

### Chars

Currently chars do not exist in top, however their is an Alias called `Char` which aliases i8.

### None
The `none` type is a type which represents the absence of a value like void in c.

## Functions

### Defining named functions

The syntax for defining functions is the `def` keyword followed by the function name and opening parenthesis then list the arguments followed by a colon and the argument type seperated by `,`, followed by a closing parenthesis and a return type, if no return type is specified the return type of the function is `none`, the body of the function begings with an `=`. Different to other languages the last statement acts as the return statement, so this function returns `a + b`.

```scala
def add(a: int, b: int) int =
  a + b
```

### Conditionals and Loops

## If, Elif, Else

The if statement in top is both an expression and a statement, it expects a boolean as a condition and will return the last expression in the body.
The else statement does what you would expect and elif is the same as if else in c.

```scala
x := 10 //creates a new variable with the type inferred to be an int

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

## For Loop
```
Currently, for loops only work on ranges however in the future there will also be support for iterators.

for x := 0..10 do //0..10 denotes a range from 0 to 10, so x will be 0, 1, 2, .., 9, but not 10
  log "x is {x}"
```

## break, continue, return

`break` will exit the current loop, `continue` will skip the rest of the body of a loop and `return` is the same as in other languages.

### Pointers

Pointers are the adresses to some data. There is no concept of null in top so there can't be any null pointer dereferences. 
However this does not mean that acessing a pointer is always safe as the data could have been freed. This is the problem with automatic memory management but it does allow for better performance.
Passing an object by reference means you don't make a copy which can be slow and you can modify the original data when passed to a function or struct. Pointers in top are a mix bitween reference in c++ and pointers. Unlike in c++ you can get a field from a pointer using ., as well as call methods on pointers and use them for operator overloading. 

```scala
def func() &int =
    ì := 10
    
    pointerToI := &i //takes the references
    *pointerToI = 20
    
    log i //will print 20 to the console, note, log takes anything that has a toString method which returns a string
    
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
    
def funcWhichAllocates() &int =
  box 20 //box takes a value, allocates enough memory for it and then sets that memory to the value
```

### Sizeof and Offsetof

```scala
log sizeof int //prints the sizeof an integer
log offsetof string.length //prints the byte offset of the field length in the type string
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
p2 := Point2{ x = 10, y = 20 } //this will also create a new point
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
type Maybe[T] = //the Maybe ADT in top is used instead of null, the [T] syntax means the type takes a generic type parameter T
    Some(T)
    None
    
def Maybe[T].default(&self, value: T) T =
    match *self with //pattern matching with match 
        Some x -> x //if self is Some then the result will be x
        None -> value //if self is None then the result will be value

def Maybe[T: Stringer].toString(&self) string =
    match *self with
      Some x -> "Some({x})
      None x -> "None"      
  
//You don't have to define this type as if is part of the global namespace, to see it's actual definition read through TopCompiler/TopRuntime 
    
type Person =
    name: Maybe[string]
    age: Maybe[int]
    
def Person.toString(&self) string =
    name := self.name.default "Anonymous"
    age := self.age.default "ageless"
    
    "{name} is {age}
 
person := Person{
    name = Some "Bob"
    age = None
}

person2 := Person2{
    name = None
    age = Some 30
}

copy_of_person := person{
  age = Some 26
} //copy of person with age set to Some 13

log toString person //will print: Bob is ageless
log toString person2 //will print: Anonymous is 14
log toString copy_of_person //will print: Luke is 26
``` 

### Methods
Methods are functions which are attached to a particular data type. 
You can attach methods to Structs, Enums and Aliases (only if the alias does not already have that method)

```scala
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

&i.incr! //correct way

log i /* this will print Point(10, 0)

```

### Operator overloading

```scala

def Point.op_add(self, other: Point) Point = //unary operator overloads use unary_name_of_operator
    Point{
        self.x + other.x
        other.y + other.y
    }

log (Point{10,20} + Point{30,20}).x
```


### #addToContext

In top there is an extra parameter passed to every function implicitly. This is the context variable of type `&Context`.
To change this use #addContext to a field to this variable.

```
#addToContext x := 10

log context.x //will print 10
```

### #pushContext

Push context pushes a new context meaning context, and the context passed into each function will be the new context.

```scala
new_context := *context
new_context.allocator = &Malloc_as_allocator //allocator is the field for context which set's the allocator to use, by default it is a linear allocator that you can free all memory up to a certain point, or at the end of a frame

#pushContext new_context do
  log "hello {name}" //the string addition will now use malloc as an allocator, meaning you now caused a memory leak as this will never be freed
```

### Defer
Defer calls a function at the end of the block with the parameters evaluated where the defer is.  Which is usefull for managing resources.
```scala
defer context.allocator.reset_to context.allocator.get_occupied! //will free all of the memory that has been allocated after this statement if you are using the default linear allocator

x := box 10


//will call defer at the end of the block no matter what (unless you segfault)
```
