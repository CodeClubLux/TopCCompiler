# TopCompiler
Transpiler from the Top programming language to javascript, written in python3.5.

The Top programming language, also known as Toplang is a functional, staticly-typed and procedural programming language. The language depends on hindley milner type inference to infer most types. Top is aimed at enabling reactive, reusable, reliable web apps running in the browser and the server using the same language.

## Installing topc
1. Clone this repo
2. Cd into the downloaded clone
3. Call 'python3 setup.py install'

## Setting Up a New Project
1. Open up terminal or command prompt`
2. Cd into the directory you wish to create the project folder in.
3. Execute `topc new project HelloWorld`, this will create a new top project in the current directory
4. Execute `topdev 8080`, this will start a live reloading build server, that can be viewed at port 8080
5. Open up any web browser with the url `127.0.0.1:8080`, the result should be a blank page
6. Create a new file called `TopCompiler/main/main.top`

## Introduction
Like many functional programming languages, blocks in Top are delimited by whitespace. Indenting blocks are required to be with spaces and not tabs to facilitate platform independence. In addition, newlines end statements if the expression is not further indented and no unclosed parenthesis.

Function must called without parenthesis, the function call will then end following the normal statement ending rule
```scala
func 10, 5
```

## Compiling
Once the topdev server is running all you have to do recompile, is save the file. The web page you have open immediately update, however if the compiler catches a compile error a blue box with the error message will be shown below.

## Literals
### Integers
Integers are like long's in languages like java, however they may contain underscores to make them more readable.
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

However strings can also be interpolated with other values as long as they have a toString method.
```scala
"fib(20) = {6765}"
```

Their type signature is `string`


