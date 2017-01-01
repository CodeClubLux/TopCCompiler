"use strict";function operator_add(x,y) {return x.operator_add(y)}
function operator_sub(x,y) {return x.operator_sub(y)}
function operator_mul(x,y) {return x.operator_mul(y)}
function operator_div(x,y) {return x.operator_div(y)}
function operator_mod(x,y) {return x.operator_mod(y)}
function operator_eq(x,y) {return x.operator_eq(y)}
function operator_pow(x,y) {return Math.pow(x,y)}
function operator_lt(x,y) {return x.operator_lt(y)}
function operator_gt(x,y) {return x.operator_gt(y)}
function operator_or(x,y) {return x || y}
function operator_not(x) {return !x}
function operator_and(x,y) { return x && y }


function unary_add(x) {return x}
function unary_sub(x) {return -x}

Number.prototype.operator_add = function (other) { return this + other }
Number.prototype.operator_div = function (other) { return this / other }
Number.prototype.operator_sub = function (other) { return this - other }
Number.prototype.operator_mul = function (other) { return this * other }
Number.prototype.operator_eq = function (other) { return this == other }
Number.prototype.operator_mod = function (other) { return this % other }
Number.prototype.operator_lt = function (other) { return this < other }
Number.prototype.operator_gt = function (other) { return this > other }
Number.prototype.toFloat = function () { return this }
Number.prototype.toInt = function () { return this | 0 }

String.prototype.operator_eq = function (other) { return this == other }
String.prototype.operator_add = function (other) { return this + other }
function toString(s) {
    return s.toString()
}

function log(s){
    console.log(s.toString())
}

function string_toString(s) {return s}
function int_toString(s) { return s.toString() }
function float_toString(s) { return s.toString() }
function array_toString(s) { return s.toString() }

function float_toInt(s) { return s | 0 }
function int_toInt(s) { return s }

String.prototype.toInt = function () { return Number(this) | 0 }
String.prototype.toFloat = function () { return Number(this) }

function float_toFloat(s) { return s }
function int_toFloat(s) { return s }

function isOdd(number) {
    return number % 2 != 0
}

function isEven(number) {
    return number % 2 == 0
}

function min(a,b) {
    return a < b ? a : b
}

function max(a,b) {
    return a > b ? a : b
}

function len(x) {
    return x.length
}

function toFloat(x) {
    return x.toFloat()
}

function toInt(x) {
    return x.toInt()
}

function toJS(arg) {
    if (arg instanceof Vector) {
        return arg.map(toJS).toArray()
    }

    if (arg instanceof Function) {
        return funcWrapper(arg);
    }

    return arg
}

function fromJS(arg) {
    if (arg instanceof Array) {
        return fromArray(arg.map(fromJS));
    }

    else if (arg instanceof Function) {
        return jsFuncWrapper(arg);
    }

    return arg
}

function funcWrapper(func) {
    return function () {
        var x = Array.prototype.slice.call(arguments);

        var args = [];
        for (var i = 0; i < x.length; i++) {
            args.push(fromJS(x[i]));
        }

        return toJS(func.apply(null, args))
    }
}

function jsFuncWrapper(func) {
    return function () {
        var x = Array.prototype.slice.call(arguments);

        var args = [];
        for (var i = 0; i < x.length; i++) {
            args.push(toJS(x[i]));
        }

        return fromJS(func.apply(null, args));
    }
}

function toAsync(func) {
    return function () {
        var x = Array.prototype.slice.call(arguments);

        var args = [];
        for (var i = 0; i < x.length-1; i++) {
            args.push(x[i]);
        }

        var next = x[x.length-1];

        return next(func.apply(null, args));
    }
}

var _empty_func = function() {}

function toSync(func) {
    return function () {
        var x = Array.prototype.slice.call(arguments);

        var args = [];
        for (var i = 0; i < x.length; i++) {
            args.push(x[i]);
        }

        args.push(_empty_func);

        return func.apply(null, args);
    }
}


function unary_read(next) {
    next(this.arg);
}

function operator_set(val, next) {
    this.arg = val;
    for (var i = 0; i < this.events.length; i++ ) {
        this.events[i](val, _empty_func);
    }
    next()
}

function atom_watch(func, next) {
    this.events.push(func)
    next();
}

function newAtom(arg) {
    return {
        unary_read: unary_read,
        operator_set: operator_set,
        arg: arg,
        watch: atom_watch,
        events: [],
    }
}

function newLens(reader, setter) {
    return {
        query: function(item) {
            return reader(item);
        },
        set: function(old, item) {
            return setter(old, item)
        },
    }
}

function defer(func) {
    return function (x) {
        return function (callback) { func(x, callback) }
    }
}

function sleep(time, callback) {
    setTimeout(callback, time);
}

function parallel(funcs, next) {
    var count = 0;

    var length = funcs.length;
    var array = funcs;

    for (var i = 0; i < funcs.length; i++) {
        var f = (function (i) {
            return function (res) {
                count++;
                array = array.set(i, res);

                if (count == funcs.length) {
                    next(array);
                }
            }
        })(i)

        funcs.get(i)(f);

    }
}

function serial(funcs, next) {
    var i = 0;
    var length = funcs.length;
    var array = EmptyVector;

    function loop() {
        if (i == funcs.length) {
            next(array);
        } else {
            funcs.get(i)(function (val) {
                array = array.append(val);
                i += 1
                loop()
            })

        }
    }
    loop()
}

function core_assign(construct, obj) {
    return Object.assign(new construct.constructor(), construct, obj);
}
//linked list
/*
function List(value, list) {
    this.head = value;
    this.tail = list;

    if (list === null) {
        if (value === null) {
            this.length = 0
        } else {
            this.length = 1;
        }
    } else {
        this.length = list.length+1
    }
}

var EmptyList = new List(null, null);

List.prototype.append = function (head) {
    return new List(head, this);
}

List.prototype.toArray = function () {
    var v = [];
    var curr = this;
    for (var i = 0; i < this.length; i++) {
        v.push(curr.head);
        curr = curr.tail
    }
    return v.reverse();
}

List.prototype.getProperIndex = function (index) {
    if (index < 0) {
        return (this.length + index);
    }
    return index;
}

List.prototype.getList = function (index) {
    index = this.getProperIndex(index)

    var getElement = (this.length-index)-1;
    var curr = this;

    for (var i = 0; i < getElement; i++) {
        curr = curr.tail;
    }
    return curr;
}

List.prototype.get = function (index) {
    return this.getList(index).head;
}

List.prototype.toString = function () {
    return "List("+this.join(", ")+")"
}

List.prototype.join = function(sep) {
    if (sep === null) sep = ",";

    var curr = this;

    if (this.length === 0) return "";

    var str = curr.head.toString();

    for (var i = 1; i< this.length; i++ ) {
        curr = curr.tail;
        str = (curr.head.toString() + sep.toString()) + str
    }
    return str;

}

List.prototype.insert = function (pos, val) {
    function insert(self, position, value) {
        if (position < 0) {
            throw new Exception();
        } else if (position === 0) {
            return self.append(value);
        } else {
            return insert(self.tail, position - 1, value).append(self.head);

        }
    }

    pos = this.getProperIndex(pos);
    return insert(this, this.length - pos, val)
}

List.prototype.del = function (pos) {
    function insert(self, position) {
        if (position < 0) {
           throw new Error("")
        } else if (position === 1) {
            var t = self.tail;
            if (t === null) {
                t = EmptyList;
            }
            return t;
        } else {
            return insert(self.tail, position - 1).append(self.head);

        }
    }

    pos = this.getProperIndex(pos);
    return insert(this, this.length - pos)
}

List.prototype.slice = function (index, indexEnd) {
    if (index == null ) { index = 0 }
    if (indexEnd == null ) { indexEnd = this.length }
    indexEnd = this.getProperIndex(indexEnd-1);
    index = this.getProperIndex(index);

    var l = this.getList(indexEnd)
    var e = new List(l.head, l.tail);

    e.length = indexEnd-index+1;

    return e;
}

List.prototype.reverse = function () {
    var v = EmptyList;
    var curr = this;
    for (var i = 0; i < this.length; i++) {
        v = v.append(curr.head);
        curr = curr.tail;
    }
    return v;
}

List.prototype.operator_eq = function (other) {
    if (this.length !== other.length) return false;
    if (self === other) return true;

    var self = this;

    for (var i = 0; i < this.length; i++) {
        if (!self.head.operator_eq(other.head)) {
            return false;
        }

        self = self.tail;
        other = other.tail;
    }
    return true;
}

List.prototype.operator_add = function (other) {
    function insert(self, position, s) {
        if (position < 0) {
            throw new Exception();
        } else if (position == 0) {
            return new List(s.head, s.tail);
        } else {
            return insert(self.tail, position - 1, s).append(self.head);

        }
    }

    return insert(other, other.length, this)
}

List.prototype.copy = function () {
    function insert(self, position) {
        if (position < 0) {
            throw new Exception();
        } else if (position == 0) {
            return self;
        } else {
            return insert(self.tail, position - 1).append(self.head);
        }
    }

    return insert(this, this.length)
}

List.prototype.set = function (pos, val) {
    function insert(self, position, value) {
        if (position < 0) {
            throw new Exception();
        } else if (position === 0) {
            return new List(value, self.tail)
        } else {
            return insert(self.tail, position - 1, value).append(self.head);

        }
    }

    pos = this.getProperIndex(pos);
    return insert(this, this.length - pos - 1, val)
}

function listFromArray(arr) {
    var len = arr.length;
    var curr = EmptyList;

    for (var i = 0; i < len; i++) {
        curr = curr.append(arr[i]);
    }
    return curr;
}

function newList() {
    return listFromArray(Array.prototype.slice.call(arguments));
}

function newListRange(start, end) {
    var arr = EmptyList;
    for (var i = start; i < end; i++) {
        arr = arr.append(i)
    }
    return arr;
}

function newListInit(repeat, elem) {
    var arr = EmptyList;
    for (var i = 0; i < repeat; i++) {
        arr = arr.append(i);
    }
    return arr;
}
*/
function Vector(root, len, depth) {
    this.shift = (depth - 1) * this.bits;
    this.root = root;
    this.length = len;
    this.depth = depth;
}

Vector.prototype.bits = 5;
Vector.prototype.width = 1 << Vector.prototype.bits;
Vector.prototype.mask = Vector.prototype.width - 1;

var EmptyVector = new Vector(Array(Vector.prototype.width), 0, 1)

Vector.prototype.get = function (key) {
    key = getProperIndex(this, key);
    if (key >= this.length || key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var node = this.root;

    var bits = this.bits;
    var mask = this.mask;

    for (var level = this.shift; level > 0; level -= bits) {
          node = node[(key >> level) & mask]
    }
    return node[key & mask]
}

Vector.prototype.append_m = function (value) {
    var width = Vector.prototype.width;

    if (Math.pow(width, this.depth) === this.length || this.length == 0) {
        return this.append(value);
    }

    var key = this.length;
    var node = this.root;

    var bits = this.bits;
    var mask = this.mask;

    for (var level = this.shift; level > 0; level -= bits) {
        var res = (key >> level) & mask
        var tmp = node[res]

        if (tmp === undefined) {

            tmp = Array(width);
            node[res] = tmp;
        }
        node = tmp;
    }


    node[key & mask] = value;

    this.length++;
    return this;
}

Vector.prototype.set_m = function (key, value) {
    key = getProperIndex(this, key);
    if (key >= this.length || key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var node = this.root;

    var bits = this.bits;
    var mask = this.mask;

    for (var level = this.shift; level > 0; level -= bits) {
        node = node[(key >> level) & mask]
    }

    node[key & mask] = value;
    return this;
}

Vector.prototype.append = function (value) {
    var bits = this.bits;
    var mask = this.mask;

    function update(node, level, key) {
        if (level > 0) {
            var pos = key >> level & mask;

            if (!node) {
                var newNode = Array(width);
            } else {
                var newNode = node.slice();
            }

            newNode[pos] = update(newNode[pos], level - bits, key);
            return newNode;
        } else {
            var pos = key & mask;

            if (node == null) {
                var newNode = Array(width);
            } else {
                var newNode = node.slice();
            }
            newNode[pos] = value;
            return newNode
        }
    }

    var width = Vector.prototype.width;

    if (Math.pow(width, this.depth) === this.length) {
        var n = Array(width)
        n[0] = this.root;
        n[1] = Array(width)

        var u = update(n, this.depth * this.bits, this.length);
        return new Vector(u, this.length+1, this.depth+1)
    } else {
        var u = update(this.root, this.shift, this.length);
        return new Vector(u, this.length+1, this.depth)
    }
}

Vector.prototype.set = function (key, value) {
    key = getProperIndex(this, key);
    if (key >= this.length || key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var bits = this.bits;
    var mask = this.mask;

    function update(node, level, key) {
        if (level > 0) {
            var pos = key >> level & mask;

            var newNode = node.slice();

            newNode[pos] = update(newNode[pos], level - bits, key);
            return newNode;
        } else {
            var pos = key & mask;

            var newNode = node.slice();
            newNode[pos] = value;
            return newNode
        }
    }

    var width = Vector.prototype.width;

    var u = update(this.root, this.shift, key);
    return new Vector(u, this.length, this.depth);
}

Vector.prototype.insert = function (key, val) {
    key = getProperIndex(this, key);
    if (key >= this.length || key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var bits = this.bits;
    var mask = this.mask;

    var self = this;

    function insert(node, level, key, value) {
        if (level > 0) {
            var pos = key >> level & mask;

            if (node) {
                var newNode = Array(width);
            } else {
                var newNode = node.slice();
            }

            var u = insert(newNode[pos], level - bits, key, value);
            newNode[pos] = u[0];
            var next = null;
            if (u[1]) {
                next = u[1];
                for (var i = pos+1; i < width; i++) {
                    var u = insert(newNode[i], level - bits, (i << level), next);
                    newNode[i] = u[0];
                    next = u[1];
                }
            }
            return [newNode, next];
        } else {
            var pos = key & mask;
            return arrayInsert(node, pos, value)
        }
    }

    function arrayInsert(arr, index, val) {
        var narr = [];
        for (var i = 0; i < width-1; i++) {
            if (index === i) {
                narr.push(val);
            }
            narr.push(arr[i]);
        }

        if (index === i) {
            narr.push(val);
        }

        return [narr, arr[width-1]]
    }

    var width = Vector.prototype.width;

    var u = insert(this.root, this.shift, key, val);
    if (u[1]) {
        return new Vector(u[0], this.length+1, this.depth).append(u[1])
    } else {
        return new Vector(u[0], this.length+1, this.depth)
    }
}

Vector.prototype.toArray = function () {
    var v = Array(this.length)
    for (var i = 0; i < this.length; i++) {
        v[i] = this.get(i);
    }
    return v;
}

Vector.prototype.toString = function () {
    return "["+this.toArray().join(",")+"]"
}

Vector.prototype.operator_eq = function (other) {
    if (this.length !== other.length) return false;
    if (this === other) return true;

    for (var i = 0; i < this.length; i++) {
        if (!(this.get(i).operator_eq(other.get(i)))) {
            return false;
        }
    }
    return true;
}

Vector.prototype.map = function (func) {
    var newArr = EmptyVector;
    var len = this.length;
    for (var i = 0; i < len; i++) {
        newArr = newArr.append_m(func(this.get(i), i));
    }
    return newArr;
}

Vector.prototype.filter = function (func) {
    var newArr = EmptyVector;
    var len = this.length;
    for (var i = 0; i < len; i++) {
        var el = this.get(i)
        if (func(el)) {
            newArr = newArr.append_m(el);
        }
    }
    return newArr;
}

Vector.prototype.reduce = function (func) {
    if (this.length == 1) {
        return this.get(0)
    } else if (this.length === 0) {
        throw Error("Cannot reduce empty vector")
    }

    var len = this.length;
    var curr = this.get(0)
    for (var i = 1; i < len; i++) {
        curr = func(curr, this.get(i));
    }
    return curr;
}

Vector.prototype.join = function (s) {
    if (s.length == 0) { return "" }
    var string = this.get(0);
    var len = this.length;
    for (var i = 1; i < len; i++) {
        string += s + this.get(i);
    }
    return string
}

function getProperIndex(self, index) {
    if (index < 0) {
        return (self.length + index);
    }
    return index;
}

Vector.prototype.has = function (s) {
    for (var i = 0; i < this.length; i++) {
        if (this.get(i).operator_eq(s)) {
            return true;
        }
    }
    return false;
}

Vector.prototype.operator_add = function (s) {
    var newArr = this;
    for (var i = 0; i < s.length; i++) {
        newArr = newArr.append(s.get(i));
    }
    return newArr;
}

Vector.prototype.shorten = function (number) {
    return new Vector(this.root, this.length-number, this.depth)
}

function newVector() {
    return fromArray(Array.prototype.slice.call(arguments))
}

function fromArray(arr) {
    var v = EmptyVector;
    for (var i = 0; i < arr.length; i++) {
        v = v.append_m(arr[i]);
    }
    return v;
}

function newVectorRange(start, end) {
    var arr = EmptyVector;
    for (var i = start; i < end; i++) {
        arr = arr.append_m(i);
    }
    return arr;
}

function newVectorInit(repeat, elem) {
    var arr = EmptyVector;
    for (var i = 0; i < repeat; i++) {
        arr = arr.append_m(elem);
    }
    return arr;
}"use strict";
function main_fullInit(){var d=0;return function c(b){while(1){switch (d){case 0:return;}}}()}function main_map(c, d){return (d).map(c);}function main_filter(c, d){return (d).filter(c);}function main_reduce(c, d){return (d).reduce(c);}function main_comp(c, d){return c((d));}function main_zip(c, d){var f;f = newVector();var g;g = 0;
while((g<(c).length)){f=(f).append((newVector(c.get(g),d.get(g))));g=((g+1)|0);}return f;}function main_append(c, d){return (d).append(c);}function main_first(c){return c.get(0);}function main_toEffect(c){function d(f,g){var k=0;return function j(h){while(1){switch(k){case 0:return g(c(f));}}}()}return d;}main_fullInit();
function main_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_nodeInit();function main_Some(g){return [1,g]}function main_None(){return [2,]}main_fs = require('fs');main_read = function(f,next){main_fs.readFile(f,'utf8',function(e,res){next(res)})};d=1;return main_read("bin/Simulation.html",c);case 1:main_htmlFile = b;main_port = process.env.PORT || 3000;main_server = http_server(main_requestHandler);d=3;return (main_server).listen(main_port,c);case 3:log((((("started web server on port ")+((main_port)).toString()))+("").toString()));return;}}}()}var main_fs;var main_read;var main_htmlFile;var main_port;var main_server;function main_fib(c){return (function(){if((c<2)){return c;}
else{return (((main_fib(((c-2)|0)))+(main_fib(((c-1)|0))))|0);}})();}function main_println(c,d){var h=0;return function g(f){while(1){switch(h){case 0:log(c);return d();}}}()}function main_FS(f){this.open=f;}main_FS.fields=newVector("open");function main_requestHandler(c, d,f){var j=0;return function h(g){while(1){switch(j){case 0:log(("server request, "+(c).url));j=2;return http_endResponse(d,(function(){if(((c).url==="/")){return main_htmlFile;}
else{return "";}})(),h);case 2:return f(g);}}}()}function http_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_httpNode = require('http');http_endResponse = function (res, value, next) { res.writeHead(200, {'Content-Type': 'html'}); next(res.end(value)); };http_server = function (func) { return http_httpNode.createServer(toSync(func)); };return;}}}()}var http_httpNode;var http_endResponse;var http_server;function http_Request(f){this.url=f;}http_Request.fields=newVector("url");function http_Response(){}http_Response.fields=newVector();function http_Server(g){this.listen=g;}http_Server.fields=newVector("listen");function http_NodeHTTP(h){this.createServer=h;}http_NodeHTTP.fields=newVector("createServer");main_nodeInit();