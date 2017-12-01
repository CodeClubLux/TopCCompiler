# Top Compiler <img src="https://github.com/CodeClubLux/TopCompiler/blob/master/arrow.png" width="40" height="40"> 

Transpiler from the Top programming language to javascript, written in python3.5.

The Top programming language, also known as Toplang is a functional, staticly-typed and procedural programming language. The language depends on hindley milner type inference to infer most types. Top is aimed at enabling reactive, reusable, reliable web apps running in the browser and the server using the same language.

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
4. Execute `topdev 8080`, this will start a live reloading build server, that can be viewed at port 8080
6. Open up any web browser with the url `127.0.0.1:8080`, the result should be a blank page
7. Create a new file called `TopCompiler/main/main.top`, then add the filename `main` to the port.json file in the package directory under the `files` property, the `files` property lists in which order the package files should be compiled in.

## Introduction
Like many functional programming languages, blocks in Top are delimited by whitespace. Indenting blocks are required to be with spaces and not tabs to facilitate platform independence. In addition, newlines end statements if the expression is not further indented and no unclosed parenthesis.

Function must called without parenthesis, the function call will then end following the normal statement ending rule
```scala
func 10, 5
```

While in javascript, this is perfectly normal
```js
func(10,5) + 89
```
In top you should instead write, because otherwise you would be passing the tuple (10,5) plus 89 to func
```scala
(func 10, 5) + 80
```

## Compiling
Once the topdev server is running all you have to do recompile, is save the file. The web page you have open immediately update, however if the compiler catches a compile error a blue box with the error message will be shown below.

## Literals
### Integers
Integers are the same as in javascript, however they may contain underscores to make them more readable.
```scala
1_000_000
```

Their type signature is written as `int`.

### Floats
Floats can have underscores as Integers and must have a dot in the middle or end with an `f`.
```scala
3.51296
9f
```

Float's type signature is `float`.

### Boolean
Boolean can only have two values: `true` or `false`.

### Strings
Strings look the same as javascript strings and have the same methods.
```scala
"hello toplang"
```

However strings can also be interpolated with an expression inside the braces as long as they have a toString method.
```scala
"fib(20) = {6765}"
```

Their type signature is `string`

### None
The `none` type is a type and a value `none`, it represents the absence of a value like void in java.

## Functions

### Defining named functions

The syntax for defining functions is the `def` keyword followed by the function name and opening paranthesis then list the arguments followed by a colon and the argument type seperated by a comma, followed by a closing paranthesis the return type, if no return type is specified the return type of the function is `none` and then = or do. 

Functions defined with `=` must be pure and cannot perform any side effects.

```scala
def add(a: int, b: int) int =
  a + b
```

Functions defined with `do` can perform side effects and are compiled into state machines, which won't block on async operations simmilar to async in C#. This means it is unneccesarry to use callback style for asynchronous operations. 
```scala
import "http"

def getFile(name: string) string do
  http.get name //won't block main thread
```


# Known Bugs
Two side effect function calls after each other
Which target each scope is compiled to, is lost when not recompiling from scratch
Function chain operator doesn't work on do functions
