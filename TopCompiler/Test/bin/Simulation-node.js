function operator_add(x,y) {return x.operator_add(y)}
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
function operator_ne(x,y) { return x.operator_ne(y) }

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
Number.prototype.operator_ne = function (other) { return this != other }

Number.prototype.toFloat = function () { return this }
Number.prototype.toInt = function () { return this | 0 }

String.prototype.operator_eq = function (other) { return this == other }
String.prototype.operator_ne = function (other) { return this != other }
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

function log_unop(v, next) {
    console.log(v);
    return next()
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

function Some(x) {
    return [0, x];
}

function None() {
    return [0];
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

function core_json_int(obj) {
    return obj | 0;
}

function core_json_float(obj) {
    return Number(obj);
}

function core_json_bool(obj) {
    return !!obj;
}

function core_json_string(obj) {
    return ""+obj;
}

function core_json_struct(constr, array) {
    return function(realObj) {
        var len = array.length;
        var obj = new constr();
        for (var i = 0; i < len; i++) {
            var arr = array[i];
            obj[arr[0]] = arr[1](realObj[arr[0]]);
        }
        return obj;
    }
}

function core_json_interface(array) {
    return function (realObj) {
        var obj = {};
        for (var i = 0; i < len; i++) {
            var arr = array[i];
            obj[arr[0]] = arr[1](realObj[arr[0]]);
        }
        return obj;
    }
}

function core_json_vector(decoder) {
    return function (realObj) {
        return fromArray(realObj.map(decoder));
    }
}

function core_parseJSON(str, decoder) {
    var obj = JSON.parse(str);
    return decoder(obj);
}

function jsonStringify(i) {
    return JSON.stringify(i);
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

Vector.prototype.toJSON = function() {
    return this.toArray();
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
}var main_fs = require("fs");
var http = require("http");

function server_readFile(f,next) {
    main_fs.readFile(f,function(e,res){
        if(e){
            next([1])
        } else {
            next([0,res])
        }
    })
}

function _http_get(url, next) {
    http.get({path: url}, next);
}

function server_createServer(func) {
    return http.createServer(function (req, res) {
        func(req, function (_res) {
            res.writeHead(_res.status, {'Content-Type': _res.contentType});
            res.end(_res.body, _res.encoding);
        })
    })
}

function server_handleQuery(url, func, next) {
        var req = url.slice(url.indexOf("/", 2)+1);
        req = JSON.parse(req);
        req[req.length-1] = function (res) {
            return {
                body: JSON.stringify(res),
                status: 200,
                contentType: "text",
            }
        };

        func(req, next);
}

function server_isQuery(url) {
    return url.slice(1, url.indexOf("/", 2)) === "query"
}
function main_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_nodeInit();main_headers = newVector("HOME","EXAMPLES","DOCS","COMMUNITY","BLOG");main_footer_text = "All code for this site is written in Top, including the server - Lucas Goetz";main__read = server_readFile;main_quit = process.exit;d=2;return main_read("Simulation.html",c);case 2:main_htmlFile = b;d=3;return main_read("images/variation.png",c);case 3:main_logo = b;d=4;return main_read("images/async.png",c);case 4:main_async = b;d=5;return main_read("images/tools.png",c);case 5:main_tools = b;d=6;return main_read("images/arrow.ico",c);case 6:main_favicon = b;d=7;return main_read("images/error.png",c);case 7:main_error = b;main_port = process.env.PORT || 3000;main_server = http_server(main_requestHandler);d=11;return (main_server).listen(main_port,c);case 11:log((((("started web server on port ")+((main_port)).toString()))+("").toString()));html_nodeInit();main_gitbook = "https://lucasgoetz.gitbooks.io/top-lang/content/";main_logoUrl = "arrow.png";return;}}}()}function main_Feature(c,d,f,g){this.id=c;this.name=d;this.description=f;this.image=g;}main_Feature.fields=["id","name","description","image"];main_Feature.prototype.toString=(function(){return main_Feature_toString(this)});function main_Feature_toString(c){return (((((((((((("Feature(")+(((c).id)).toString()))+(",").toString()))+(((c).name)).toString()))+(",").toString()))+(((c).image)).toString()))+(")").toString());}function main_PageHome(f){return [0,f]}function main_PageDocs(g){return [1,g]}var main_PageNotFound=[2,];var main_PageGetStarted=[3,];function main_Home(c,d,f){this.features=c;this.headers=d;this.footer=f;}main_Home.fields=["features","headers","footer"];function main_Docs(c,d,f,g,h){this.overview=c;this.learn=d;this.packages=f;this.headers=g;this.footer=h;}main_Docs.fields=["overview","learn","packages","headers","footer"];function main_QueryDocs(h){return [0,h]}function main_map(c, d){return (d).map(c);}function main_filter(c, d){return (d).filter(c);}function main_reduce(c, d){return (d).reduce(c);}function main_comp(c, d){return c(d);}function main_zip(c, d){var f;f = newVector();var g;g = 0;
while((g<(c).length)){f=(f).append((newVector(c.get(g),d.get(g))));g=((g+1)|0);}return f;}function main_append(c, d){return (d).append(c);}function main_first(c){return c.get(0);}function main_toEffect(c){function d(f,g){var k=0;return function j(h){while(1){switch(k){case 0:return g(c(f));}}}()}return d;}function main_read(c,d){var h=0;return function g(f){while(1){switch(h){case 0:h=1;return main__read(c,g);case 1:return d(function(){var j=f; if (j[0]==0){var k=j[1];return k;} if (j[0]==1){log(("cannot find file, "+c));return main_quit(1);}}());}}}()}function main_query(c,d){var h=0;return function g(f){while(1){switch(h){case 0:return d(function(){var j=c; if (j[0]==0){var k=j[1];return k(new main_Docs(newVector("Get Started","Examples","How to structure your program"),newVector("An Introduction to Top","FAQ","Syntax","Style Guide","The Zen of Top","Writing Documentation"),newVector("All Packages","Core","HTML"),main_headers,main_footer_text,main_footer_text));}}());}}}()}function main_requestHandler(c,d){var h=0;return function g(f){while(1){switch(h){case 0:log(("request, "+(c).url));if((http_isQuery((c).url))){h=9;return http_handleQuery((c).url,main_query,g);}h=10;break;case 9:;h=8;/*block*/break;/*if*/case 10:/*notif*/if(((c).url==="/")){f=core_assign(http_response,{body:main_htmlFile,contentType:"text/html"});h=8;/*block*/break;}/*if*/case 10:/*notif*/if(((c).url==="/arrow.png")){f=core_assign(http_response,{body:main_logo,contentType:"image/png"});h=8;/*block*/break;}/*if*/case 10:/*notif*/if(((c).url==="/async.png")){f=core_assign(http_response,{body:main_async,contentType:"image/png"});h=8;/*block*/break;}/*if*/case 10:/*notif*/if(((c).url==="/tools.png")){f=core_assign(http_response,{body:main_tools,contentType:"image/png"});h=8;/*block*/break;}/*if*/case 10:/*notif*/if(((c).url==="/favicon.ico")){f=core_assign(http_response,{body:main_favicon,contentType:"image/x-icon"});h=8;/*block*/break;}/*if*/case 10:/*notif*/if(((c).url==="/error.png")){f=core_assign(http_response,{body:main_error,contentType:"image/png"});h=8;/*block*/break;}/*if*/case 10:/*notif*/{f=core_assign(http_response,{status:404,body:"404 Page not found"});h=8;/*block*/break;}case 8:return d(f);}}}()}function main_App(c,d,f){this.headers=c;this.page=d;this.footer=f;}main_App.fields=["headers","page","footer"];function http_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_response = new http_Response(200,"text/plain","","");http_server = server_createServer;http_handleQuery = server_handleQuery;http_isQuery = server_isQuery;return;}}}()}function http_Server(c){this.listen=c;}http_Server.fields=["listen"];function http_NodeHTTP(c){this.createServer=c;}http_NodeHTTP.fields=["createServer"];function http_Request(c){this.url=c;}http_Request.fields=["url"];function http_Response(c,d,f){this.status=c;this.contentType=d;this.body=f;}http_Response.fields=["status","contentType","body"];function http_endResponse(c){return core_assign(http_response,{body:jsonStringify(c)});}function http_toUrl(c){return ("query/"+jsonStringify(c(http_endResponse)));}function html_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:html_style = html_newAttrib.bind(null,"style");html_placeHolder = html_newAttrib.bind(null,"placeholder");html_position = html_newAttrib.bind(null,"position");html__type = html_newAttrib.bind(null,"type");html_height = html_newAttrib.bind(null,"height");html_width = html_newAttrib.bind(null,"width");html_id = html_newAttrib.bind(null,"id");html_min = html_newAttrib.bind(null,"min");html_max = html_newAttrib.bind(null,"max");html_step = html_newAttrib.bind(null,"step");html_value = html_newAttrib.bind(null,"value");html_href = html_newAttrib.bind(null,"href");html_src = html_newAttrib.bind(null,"src");html__float = html_newAttrib.bind(null,"float");html_class = html_newAttrib.bind(null,"className");html_onClick = html_onEvent.bind(null,"onclick");html_onInput = html_onEvent.bind(null,"oninput");html_onChange = html_onEvent.bind(null,"onchange");html_noAttrib = newVector();return;}}}()}function html_PosAtom(c,d){this.a=c;this.pos=d;}html_PosAtom.fields=["a","pos"];html_PosAtom.prototype.unary_read=(function(c){return html_PosAtom_unary_read(this,c)});function html_PosAtom_unary_read(d,f){var j=0;return function h(g){while(1){switch(j){case 0:j=1;return (d).a.unary_read(h);case 1:;return f(((d).pos).query(g));}}}()}html_PosAtom.prototype.operator_set=(function(c,d){return html_PosAtom_operator_set(this,c,d)});function html_PosAtom_operator_set(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=2;return (f).a.unary_read(k);case 2:;l=3;return ((f).a).operator_set(((f).pos).set(j,g),k);case 3:return h(j);}}}()}html_PosAtom.prototype.watch=(function(c,d){return html_PosAtom_watch(this,c,d)});function html_PosAtom_watch(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:function m(n,p){var s=0;return function r(q){while(1){switch(s){case 0:s=4;return (f).a.unary_read(r);case 4:;s=5;return g(((f).pos).query(q),r);case 5:return p(q);}}}()}l=6;return ((f).a).watch(m,k);case 6:return h(j);}}}()}function html_Event(c){this.target=c;}html_Event.fields=["target"];function html_Attribute(c,d){this.name=c;this.value=d;}html_Attribute.fields=["name","value"];function html_newAttrib(c, d){return new html_Attribute(c,d,d);}function html_onEvent(c, d, f){function g(h,j){var m=0;return function l(k){while(1){switch(m){case 0:m=7;return f.unary_read(l);case 7:;m=8;return d(k,h,l);case 8:m=9;return (f).operator_set(k,l);case 9:return j(k);}}}()}return new html_Attribute(c,g,g);}function html_async(c, d){function f(g){var k=0;return function j(h){while(1){switch(k){case 0:k=14;return d.unary_read(j);case 14:;k=15;return c(h,j);case 15:k=16;return (d).operator_set(h,j);case 16:return g(h);}}}()}return f;}function html_ignoreAct(c){function d(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=17;return c(f,k);case 17:return h(j);}}}()}return d;}function html_withId(c){function d(f, g, h,j){var n;var m=0;return function l(k){while(1){switch(m){case 0:m=18;return c(g.get(f),h,l);case 18:n = (k);return j((g).set(f,n));}}}()}return d;}function html_mapWithId(c, d, f){function g(h){return c(d.get(h),h,f);}return (newVectorRange(0,(d).length)).map(g);}function html_mapView(c, d, f){function g(h){var j;j = d.get(h);var k;k = newLens(function(l){return l.get(h)}, function(m,l){return m.set(h,l)});var n;n = new html_PosAtom(f,k,k);return c(j,n);}return (newVectorRange(0,(d).length)).map(g);}function html_viewFromLens(c, d, f, g){return c(((f).query(d)),new html_PosAtom(g,f,f));}function html_get(c){var g=0;return function f(d){while(1){switch(g){case 0:return c();}}}()}main_nodeInit();