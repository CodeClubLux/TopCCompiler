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

function assign(obj, other) {
    if (obj instanceof Array) {
        var arr = [];
        for (var i = 0; i < other.length; i++) {
            var c = other[i];
            if (c) {
                arr.push(c);
            } else {
                arr.push(obj[i]);
            }
        }
        for (var i = other.length; i < obj.length; i++) {
            arr.push(obj[i]);
        }
        return arr;
    }
    else if (typeof obj == "object") {
        return Object.assign(new obj.constructor(), obj, other);
    } else {
        return other
    }
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

function parseJson(decoder, str) {
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
function Vector(root, len, depth, start) {
    this.shift = (depth - 1) * this.bits;
    this.root = root;
    this.length = len;
    this.depth = depth;
    this.start= start || 0;
}

Vector.prototype.bits = 5;
Vector.prototype.width = 1 << Vector.prototype.bits;
Vector.prototype.mask = Vector.prototype.width - 1;

var EmptyVector = new Vector(Array(Vector.prototype.width), 0, 1)

Vector.prototype.get = function (key) {
    key = getProperIndex(this, key);
    if (key >= this.length+this.start || key < 0) {
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
    if (key >= this.length+this.start || key < 0) {
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
    if (key >= this.length+this.start || key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var bits = this.bits;
    var mask = this.mask;

    var self = this;

    function insert(node, level, key, value) {
        if (level > 0) {
            var pos = key >> level & mask;

            if (node) {
                var newNode = [];
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
    var v = [];
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

Vector.prototype.slice = function (start,end) {
    start = getProperIndex(this, start);
    if (!end) {
        end = this.length;
    } else {
        end = getProperIndex(this, end);
    }

    return new Vector(this.root, end-start, this.depth, start);
}

function getProperIndex(self, index) {
    index += self.start;
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
    return new Vector(this.root, this.length-number, this.depth);
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
        req.url = decodeURI(req.url);

        func(req, function (_res) {
            res.writeHead(_res.status, {'Content-Type': _res.contentType});
            res.end(_res.body, _res.encoding);
        })
    })
}

var _monk_connect = require("monk");

function _monk_get(db, name, decoder) {
    var tmp = db.get(name);
    tmp.decoder = decoder;
    return tmp;
}

function _monk_find(coll, query, next) {
    console.log("finding");
    coll.find(query).catch(function() { console.log("can not connect to database"); })
    .then(function(i) {
        next(fromArray(i.map(coll.decoder)));
    })
}

function _monk_search(coll, query, search, next) {
    var q = {$text: {$search: search}}
    query = Object.assign({}, query, q);
    console.log("searching");
    coll.find(query).catch(function() { console.log("can not connect to database"); })
    .then(function(i) {
        next(fromArray(i.map(coll.decoder).reverse()));
    });
}

function _monk_insert(coll, obj, next) {
    coll.insert(obj);
    next()
}

function server_handleQuery(url, func, next) {
        var req = url.slice(url.indexOf("/", 2)+1);
        req = decodeURI(req);
        req = JSON.parse(req);
        req[req.length-1] = function something(res) {
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
function http_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_response = new http_Response(200,"text/plain","","");http_server = server_createServer;http_handleQuery = server_handleQuery;http_isQuery = server_isQuery;return;}}}()}function http_Server(c){this.listen=c;}http_Server.fields=["listen"];function http_NodeHTTP(c){this.createServer=c;}http_NodeHTTP.fields=["createServer"];function http_Request(c){this.url=c;}http_Request.fields=["url"];function http_Response(c,d,f){this.status=c;this.contentType=d;this.body=f;}http_Response.fields=["status","contentType","body"];http_Response.prototype.toString=(function(){return http_Response_toString(this)});function http_Response_toString(c){return (((((((((((("Response(")+(((c).status)).toString()))+(", ").toString()))+(((c).contentType)).toString()))+(", ").toString()))+(((c).body)).toString()))+(")").toString());}function http_endResponse(c){return core_assign(http_response,{body:jsonStringify(c)});}function http_toUrl(c){return ("query/"+jsonStringify(c(http_endResponse)));}function svg_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:html_nodeInit();svg_width = html_newAttrib.bind(null,"width");svg_height = html_newAttrib.bind(null,"height");svg_fill = html_newAttrib.bind(null,"fill");svg_x = html_newAttrib.bind(null,"x");svg_y = html_newAttrib.bind(null,"y");svg_href = html_newAttrib.bind(null,"xlink:href");svg_stroke = html_newAttrib.bind(null,"stroke");svg_cy = html_newAttrib.bind(null,"cy");svg_cx = html_newAttrib.bind(null,"cx");svg_r = html_newAttrib.bind(null,"r");return;}}}()}function db_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:db_connect = _monk_connect;db_document = _monk_get;db_find = _monk_find;db_insert = _monk_insert;db_search = _monk_search;return;}}}()}function db_Parts(f){return [0,f]}function db_DB(){}db_DB.fields=[];function db_Collection(c,d){this.manager=c;this.name=d;}db_Collection.fields=["manager","name"];function main_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_nodeInit();main_headers = newVector("HOME","EXAMPLES","DOCS","COMMUNITY","BLOG");main_footer_text = "All code for this site is written in Top, including the server - Lucas Goetz";db_nodeInit();main__read = server_readFile;main_quit = process.exit;d=2;return main_read("Simulation.html",c);case 2:main_htmlFile = b;d=3;return main_read("images/variation.png",c);case 3:main_logo = b;d=4;return main_read("images/async.png",c);case 4:main_async = b;d=5;return main_read("images/tools.png",c);case 5:main_tools = b;d=6;return main_read("images/arrow.ico",c);case 6:main_favicon = b;d=7;return main_read("images/error.png",c);case 7:main_error = b;d=8;return main_read("images/enigma.png",c);case 8:main_enigma = b;main_monk = db_connect("mongodb://127.0.0.1:27017/enigma");main_coll = db_document(main_monk,"parts",core_json_struct(main_Part,[['name',core_json_string],['kind',core_json_string],['rating',core_json_int],['price',core_json_float],]));main_port = process.env.PORT || 3000;main_server = http_server(main_requestHandler);d=33;return (main_server).listen(main_port,c);case 33:log((((("started web server on port ")+((main_port)).toString()))+("").toString()));svg_nodeInit();main_random = toAsync(Math.random);main_cos = Math.cos;main_sin = Math.sin;main_sqrt = Math.sqrt;main_atan2 = Math.atan2;main_pi = Math.PI;main_abs = Math.abs;d=34;return serial((newVectorRange(0,100)).map(defer(main_generate_water)),c);case 34:main_appState = newAtom(new main_Game((b),10,100,0,0));return;}}}()}function main_Feature(c,d,f,g){this.id=c;this.name=d;this.description=f;this.image=g;}main_Feature.fields=["id","name","description","image"];main_Feature.prototype.toString=(function(){return main_Feature_toString(this)});function main_Feature_toString(c){return (((((((((((("Feature(")+(((c).id)).toString()))+(",").toString()))+(((c).name)).toString()))+(",").toString()))+(((c).image)).toString()))+(")").toString());}function main_PartsPage(c,d,f){this.parts=c;this.headers=d;this.kind=f;}main_PartsPage.fields=["parts","headers","kind"];function main_Home(c,d,f){this.features=c;this.headers=d;this.footer=f;}main_Home.fields=["features","headers","footer"];function main_Docs(c,d,f,g,h){this.overview=c;this.learn=d;this.packages=f;this.headers=g;this.footer=h;}main_Docs.fields=["overview","learn","packages","headers","footer"];function main_PageHome(f){return [0,f]}function main_PageDocs(g){return [1,g]}function main_PageKinds(h){return [2,h]}function main_PageParts(j){return [3,j]}function main_PagePart(k){return [4,k]}var main_PageNotFound=[5,];var main_PageGetStarted=[6,];function main_QueryDocs(l){return [0,l]}function main_QueryParts(m,n,p){return [1,m,n,p]}function main_QueryPart(q,r){return [2,q,r]}function main_map(c, d){return (d).map(c);}function main_filter(c, d){return (d).filter(c);}function main_reduce(c, d){return (d).reduce(c);}function main_comp(c, d){return c(d);}function main_zip(c, d){var f;f = EmptyVector;var g;g = 0;
while((g<(c).length)){f=(f).append((newVector(c.get(g),d.get(g))));g=((g+1)|0);}return f;}function main_append(c, d){return (d).append(c);}function main_first(c){return c.get(0);}function main_toEffect(c){function d(f,g){var k=0;return function j(h){while(1){switch(k){case 0:return g(c(f));}}}()}return d;}function main_read(c,d){var j;var k;var l;var h=0;return function g(f){while(1){switch(h){case 0:h=1;return main__read(c,g);case 1:return d(function(){var m=f; if (m[0]==0){var n=m[1];return n;} if (m[0]==1){log(("cannot find file, "+c));return main_quit(1);}}());}}}()}function main_query(c,d){var j;var k;var l;var m;var n;var p;var q;var r;var s;var h=0;return function g(f){while(1){switch(h){case 0:var t=c; if (t[0]==0){s=t[1];f=s(new main_Docs(newVector("Get Started","Examples","How to structure your program"),newVector("An Introduction to Top","FAQ","Syntax","Style Guide","The Zen of Top","Writing Documentation"),newVector("All Packages","Core","HTML"),main_headers,main_footer_text,main_footer_text));h=9;/*block*/break;}/*if*/case 10:/*notif*/ if (t[0]==1){r=t[1];n=t[2];s=t[3];log("handling");if((n==="")){h=12;return db_find(main_coll,{kind:r},g);}/*case*/h=13;break;/*case*/}/*case*/h=14;break;/*case*/case 12:f=s((f));h=11;/*block*/break;/*if*/case 13:/*notif*/{h=15;return db_search(main_coll,{kind:r},n,g);}/*case*/h=16;break;/*case*/case 15:f=s((f));h=11;/*block*/break;case 11:;h=9;/*block*/break;/*if*/case 14:/*notif*/ if (t[0]==2){r=t[1];s=t[2];h=17;return db_find(main_coll,{name:r},g);}/*case*/h=18;break;/*case*/case 17:f=s((f).get(0));h=9;/*block*/break;case 9:return d(f);}}}()}function main_requestHandler(c,d){var j;var k;var l;var m;var h=0;return function g(f){while(1){switch(h){case 0:log(("request, "+(c).url));if((http_isQuery((c).url))){h=20;return http_handleQuery((c).url,main_query,g);}/*case*/h=21;break;/*case*/case 20:;h=19;/*block*/break;/*if*/case 21:/*notif*/{var n=(c).url;var p=new RegExp('/parts/(.*)').exec(n);if (p){j=p[1];h=23;return main__read((("images/parts/"+j)+".jpg"),g);}/*case*/h=24;break;/*case*/}/*case*/h=25;break;/*case*/case 23:f=function(){var q=f; if (q[0]==0){var r=q[1];log("found something");return core_assign(http_response,{body:r,contentType:"image/jpg"});} if (q[0]==1){log((((("didn't find ")+(((j+".jpg"))).toString()))+("").toString()));return core_assign(http_response,{status:404});}}();h=22;/*block*/break;/*if*/case 24:/*notif*/ if (n=="/"){f=core_assign(http_response,{body:main_htmlFile,contentType:"text/html"});h=22;/*block*/break;}/*if*/case 26:/*notif*/ if (n=="/arrow.png"){f=core_assign(http_response,{body:main_logo,contentType:"image/png"});h=22;/*block*/break;}/*if*/case 27:/*notif*/ if (n=="/async.png"){f=core_assign(http_response,{body:main_async,contentType:"image/png"});h=22;/*block*/break;}/*if*/case 28:/*notif*/ if (n=="/tools.png"){f=core_assign(http_response,{body:main_tools,contentType:"image/png"});h=22;/*block*/break;}/*if*/case 29:/*notif*/ if (n=="/favicon.ico"){f=core_assign(http_response,{body:main_favicon,contentType:"image/x-icon"});h=22;/*block*/break;}/*if*/case 30:/*notif*/ if (n=="/error.png"){f=core_assign(http_response,{body:main_error,contentType:"image/png"});h=22;/*block*/break;}/*if*/case 31:/*notif*/ if (n=="/enigma.png"){f=core_assign(http_response,{body:main_enigma,contentType:"image/png"});h=22;/*block*/break;}/*if*/case 32:/*notif*/ if (1){f=core_assign(http_response,{status:404,body:"404 Page not found"});h=22;/*block*/break;}case 22:;h=19;/*block*/break;case 19:return d(f);}}}()}function main_Part(c,d,f,g){this.kind=c;this.name=d;this.rating=f;this.price=g;}main_Part.fields=["kind","name","rating","price"];main_Part.prototype.toString=(function(){return main_Part_toString(this)});function main_Part_toString(c){return ((((((((((((((((" Part(")+(((c).kind)).toString()))+(", ").toString()))+(((c).name)).toString()))+(", ").toString()))+(((c).rating)).toString()))+(" stars, $").toString()))+(((c).price)).toString()))+(")").toString());}var main_Water=[0,];var main_Coloring=[1,];function main_Particle(c,d,f,g,h,j,k,l){this.x=c;this.y=d;this.limitX=f;this.limitY=g;this.velX=h;this.velY=j;this.mass=k;this.kind=l;}main_Particle.fields=["x","y","limitX","limitY","velX","velY","mass","kind"];function main_Game(c,d,f,g){this.particles=c;this.speed=d;this.water=f;this.color=g;}main_Game.fields=["particles","speed","water","color"];function main_returnId(c){return c;}function main_generate_water(c,d){var j;var h=0;return function g(f){while(1){switch(h){case 0:j = 0.35;return d(new main_Particle((100.0+(7.0*(toFloat(c)))),10.0,800.0,500.0,0.0,j,1.0,main_Water,main_Water));}}}()}function main_generate_coloring(c,d){var j;var h=0;return function g(f){while(1){switch(h){case 0:j = 0.3;return d(new main_Particle((100.0+(7.0*(toFloat(c)))),10.0,800.0,500.0,0.0,j,1.0,main_Coloring,main_Coloring));}}}()}main_Particle.prototype.toString=(function(){return main_Particle_toString(this)});function main_Particle_toString(c){var d;d = function(){var f=(c).kind; if (f[0]==0){return "water";} if (f[0]==1){return "coloring";}}();return (((((((((((((((((((((((((((("Particle(")+(((c).x)).toString()))+(", ").toString()))+(((c).y)).toString()))+(", ").toString()))+(((c).limitX)).toString()))+(", ").toString()))+(((c).limitY)).toString()))+(", ").toString()))+(((c).velX)).toString()))+(", ").toString()))+(((c).velY)).toString()))+(", ").toString()))+((d)).toString()))+("").toString());}function main_particle(c, d){var f;f = 0.13;return (function(){if(((c).x>((c).limitX-20.0))){return core_assign(c,{x:((c).limitX-24.0),velX:(-(c).velX)});}else if(((c).x<0.0)){return core_assign(c,{x:5.0,velX:(-(c).velX)});}else if(((c).y>((c).limitY-20.0))){return core_assign(c,{y:((c).limitY-24.0),velY:((-(c).velY)+f)});}else if(((c).y<0.0)){return core_assign(c,{y:5.0,velY:((-(c).velY)+f)});}
else{return core_assign(c,{x:((c).x+((toFloat(d))*(c).velX)),y:((c).y+((toFloat(d))*(c).velY))});}})();}function main_setX(c, d){return new main_Particle((c).x,(c).y,(c).limitX,(c).limitY,d,(c).velY,(c).mass,(c).kind,(c).kind);}function main_setY(c, d){return new main_Particle((c).x,(c).y,(c).limitX,(c).limitY,(c).velX,d,(c).mass,(c).kind,(c).kind);}function main_collision(c){var d;d = c;var f;f = (c).length;var g;g = 0;
while((g<f)){var h;h = ((g+1)|0);
while((h<f)){var j;j = d.get(g);var k;k = d.get(h);var l;l = main_abs(((j).x-(k).x));var m;m = main_abs(((j).y-(k).y));var n;n = main_sqrt(((l*l)+(m*m)));if((n<40.0)){var p;p = main_manageBounce(j,k);d=(d).set(g,p.get(0));d=(d).set(h,p.get(1));;}h=((h+1)|0);}g=((g+1)|0);}return d;}function main_gameLoop(c, d,f){var k;var j=0;return function h(g){while(1){switch(j){case 0:k = (((c).particles).map((function(m){return function(l){return main_particle(l,m);}})(d)));return f(new main_Game((main_collision(k)),(c).speed,(c).water,(c).color,(c).color));}}}()}function main_manageBounce(c, d){var f;f = ((c).x-(d).x);var g;g = ((c).y-(d).y);var h;h = (main_atan2(g,f));var j;j = (main_sqrt((((c).velX*(c).velX)+((c).velY*(c).velY))));var k;k = (main_sqrt((((d).velX*(d).velX)+((d).velY*(d).velY))));var l;l = (main_atan2((c).velY,(c).velX));var m;m = (main_atan2((d).velY,(d).velX));var n;n = (j*(main_cos((l-h))));var p;p = (j*(main_sin((l-h))));var q;q = (k*(main_cos((m-h))));var r;r = (k*(main_sin((m-h))));var s;s = ((((((1.0-1.0))*n)+(((1.0+1.0))*q)))/((1.0+1.0)));var t;t = ((((((1.0+1.0))*n)+(((1.0-1.0))*q)))/((1.0+1.0)));var v;v = p;var w;w = r;var x;x = (((main_cos(h))*s)+((main_cos((h+(main_pi/2.0))))*v));var y;y = (((main_sin(h))*s)+((main_sin((h+(main_pi/2.0))))*v));var z;z = (((main_cos(h))*t)+((main_cos((h+(main_pi/2.0))))*w));var B;B = (((main_sin(h))*t)+((main_sin((h+(main_pi/2.0))))*w));var C;C = (function(){if((((c).y>0.0)&&((c).y<(d).y))){return ((c).y-0.25);}
else{return (c).y;}})();var D;D = (function(){if((((d).y>0.0)&&((c).y>(d).y))){return ((d).y-0.25);}
else{return (d).y;}})();return newVector(new main_Particle((c).x,C,(c).limitX,(c).limitY,x,y,(c).mass,(c).kind,(c).kind),new main_Particle((d).x,D,(d).limitX,(d).limitY,z,B,(d).mass,(d).kind,(d).kind));}function main_changeNumber(c, d, f,g){var l;var m;var n;var p;var q;var r;var k=0;return function j(h){while(1){switch(k){case 0:l = toInt(((f).target).value);m = ((d).particles).length;n = (1.0/(toFloat(((11-l)|0))));function s(t,v){var z;var B;var C;var D;var y=0;return function x(w){while(1){switch(y){case 0:var F=c; if (F[0]==0){y=36;return main_generate_water(t,x);}/*case*/y=37;break;/*case*/case 36:D = w;w=main_adjust(n,D);y=35;/*block*/break;/*if*/case 37:/*notif*/ if (F[0]==1){y=38;return main_generate_coloring(t,x);}/*case*/y=39;break;/*case*/case 38:D = w;log(D);w=main_adjust(n,D);y=35;/*block*/break;case 35:return v(w);}}}()}var G=c; if (G[0]==0){if((l>(d).water)){k=42;return serial((newVectorRange(0,((l-(d).water)|0))).map(defer(s)),j);}/*case*/k=43;break;/*case*/}/*case*/k=44;break;/*case*/case 42:h=new main_Game((((d).particles).slice(0,(d).water)).operator_add((h)).operator_add((((d).particles).slice((d).water,0))),(d).speed,l,(d).color,(d).color);k=41;/*block*/break;/*if*/case 43:/*notif*/if((l===0)){h=new main_Game((((d).particles).slice((d).water,0)),(d).speed,l,(d).color,(d).color);k=41;/*block*/break;}/*if*/case 45:/*notif*/{h=new main_Game((((d).particles).slice(0,l)).operator_add((((d).particles).slice((d).water,0))),(d).speed,l,(d).color,(d).color);k=41;/*block*/break;}case 41:;k=40;/*block*/break;/*if*/case 44:/*notif*/ if (G[0]==1){if((l>(d).color)){k=47;return serial((newVectorRange(0,((l-(d).color)|0))).map(defer(s)),j);}/*case*/k=48;break;/*case*/}/*case*/k=49;break;/*case*/case 47:h=new main_Game((d).particles.operator_add((h)),(d).speed,(d).water,l,l);k=46;/*block*/break;/*if*/case 48:/*notif*/if((l===0)){h=new main_Game((((d).particles).shorten(((m-(d).water)|0))),(d).speed,(d).water,l,l);k=46;/*block*/break;}/*if*/case 50:/*notif*/{h=new main_Game((((d).particles).shorten((((d).color-l)|0))),(d).speed,(d).water,l,l);k=46;/*block*/break;}case 46:;k=40;/*block*/break;case 40:r = h;log("====== should be");log((((("water ")+(((r).water)).toString()))+("").toString()));log((((("color ")+(((r).color)).toString()))+("").toString()));log((((r).water+(r).color)|0));log(((r).particles).length);return g(r);}}}()}function main_adjust(c, d){var f;f = ((d).velX*c);var g;g = ((d).velY*c);return main_setY((main_setX(d,f)),g);}function main_changeSpeed(c, d,f){var k;var l;var m;var n;var j=0;return function h(g){while(1){switch(j){case 0:k = toInt(((d).target).value);l = (1.0/(toFloat(((11-k)|0))));m = (1.0/(toFloat(((11-(c).speed)|0))));n = (l/m);return f(new main_Game(((c).particles).map(main_adjust.bind(null,n)),k,(c).water,(c).color,(c).color));}}}()}function html_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:html_style = html_newAttrib.bind(null,"style");html_placeHolder = html_newAttrib.bind(null,"placeholder");html_position = html_newAttrib.bind(null,"position");html__type = html_newAttrib.bind(null,"type");html_height = html_newAttrib.bind(null,"height");html_width = html_newAttrib.bind(null,"width");html_id = html_newAttrib.bind(null,"id");html_min = html_newAttrib.bind(null,"min");html_max = html_newAttrib.bind(null,"max");html_step = html_newAttrib.bind(null,"step");html_value = html_newAttrib.bind(null,"value");html_href = html_newAttrib.bind(null,"href");html_src = html_newAttrib.bind(null,"src");html__float = html_newAttrib.bind(null,"float");html_class = html_newAttrib.bind(null,"className");html_onClick = html_onEvent.bind(null,"onclick");html_onInput = html_onEvent.bind(null,"oninput");html_onChange = html_onEvent.bind(null,"onchange");html_noAttrib = EmptyVector;return;}}}()}function html_PosAtom(c,d){this.a=c;this.pos=d;}html_PosAtom.fields=["a","pos"];html_PosAtom.prototype.unary_read=(function(c){return html_PosAtom_unary_read(this,c)});function html_PosAtom_unary_read(d,f){var j=0;return function h(g){while(1){switch(j){case 0:j=1;return (d).a.unary_read(h);case 1:;return f(((d).pos).query(g));}}}()}html_PosAtom.prototype.operator_set=(function(c,d){return html_PosAtom_operator_set(this,c,d)});function html_PosAtom_operator_set(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=2;return (f).a.unary_read(k);case 2:;l=3;return ((f).a).operator_set(((f).pos).set(j,g),k);case 3:return h(j);}}}()}html_PosAtom.prototype.watch=(function(c,d){return html_PosAtom_watch(this,c,d)});function html_PosAtom_watch(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:function m(n,p){var s=0;return function r(q){while(1){switch(s){case 0:s=4;return (f).a.unary_read(r);case 4:;s=5;return g(((f).pos).query(q),r);case 5:return p(q);}}}()}l=6;return ((f).a).watch(m,k);case 6:return h(j);}}}()}function html_Event(c){this.target=c;}html_Event.fields=["target"];function html_Attribute(c,d){this.name=c;this.value=d;}html_Attribute.fields=["name","value"];function html_newAttrib(c, d){return new html_Attribute(c,d,d);}function html_onEvent(c, d, f){function g(h,j){var m=0;return function l(k){while(1){switch(m){case 0:m=7;return f.unary_read(l);case 7:;m=8;return d(k,h,l);case 8:m=9;return (f).operator_set(k,l);case 9:return j(k);}}}()}return new html_Attribute(c,g,g);}function html_async(c, d){function f(g){var k=0;return function j(h){while(1){switch(k){case 0:k=14;return d.unary_read(j);case 14:;k=15;return c(h,j);case 15:k=16;return (d).operator_set(h,j);case 16:return g(h);}}}()}return f;}function html_ignoreAct(c){function d(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=17;return c(f,k);case 17:return h(j);}}}()}return d;}function html_withId(c){function d(f, g, h,j){var n;var m=0;return function l(k){while(1){switch(m){case 0:m=18;return c(g.get(f),h,l);case 18:n = (k);return j((g).set(f,n));}}}()}return d;}function html_mapWithId(c, d, f){function g(h){return c(d.get(h),h,f);}return (newVectorRange(0,(d).length)).map(g);}function html_mapView(c, d, f){function g(h){var j;j = d.get(h);var k;k = newLens(function(l){return l.get(h)}, function(m,l){return m.set(h,l)});var n;n = new html_PosAtom(f,k,k);return c(j,n);}return (newVectorRange(0,(d).length)).map(g);}function html_viewFromLens(c, d, f, g){return c(((f).query(d)),new html_PosAtom(g,f,f));}function html_get(c){var g=0;return function f(d){while(1){switch(g){case 0:return c();}}}()}main_nodeInit();