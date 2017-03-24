(function(){
            var fs = require("fs");
            var io = require("socket.io").listen(8080);

            var watch = require("chokidar");

            watch.watch('EC-client.js').on("change", (filename) => {
            //console.log("I think it changed");
                if (filename) {
                    fs.readFile('./EC-client.js', function (err, data) {
                        if (!err) {
                            data = String(data);
                            io.sockets.emit('reload', data);
                        }
                    });
                }
            });

            watch.watch([], {cwd: "../"}).on("change", (filename) => {
                fs.readFile("../" + filename, function (err, data) {
                    if (!err) {
                        console.log("\n==== reloaded stylesheets ====");
                        data = String(data);
                        io.sockets.emit('style', {name: filename, content: data});
                    }
                })
            })
        })();function operator_add(x,y) {return x.operator_add(y)}
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
String.prototype.operator_eq = function(s) { return this == s }

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
    previousState = {
        unary_read: unary_read,
        operator_set: operator_set,
        arg: arg,
        watch: atom_watch,
        events: [],
    }
    return previousState;
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

var None = [1];

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
    return obj;
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
        var len = array.length;
        for (var i = 0; i < len; i++) {
            var arr = array[i];
            obj[arr[0]] = arr[1](realObj[arr[0]]);
        }
        return obj;
    }
}

function core_json_enum(array) {
    return function (realObj) {
        var iter = realObj[0]
        var _enum = [iter];
        for (var i = 1; i < realObj.length; i++) {
            _enum[i] = array[iter][i-1](realObj[i]);
        }
        return _enum;
    }
}

function core_json_vector(decoder) {
    return function (realObj) {
        return fromArray(realObj.map(decoder));
    }
}

function core_json_tuple(decoder) {
    return function (arr) {
        var a = [];
        for (var i = 0; i < arr.length; i++) {
            a.push(decoder[i](arr[i]));
        }
        return a;
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

Vector.prototype.indexOf = function(find) {
    var index = -1;
    for (var i = 0; i < this.length; i++) {
        if (this.get(i).operator_eq(find)) {
            index += 1;
            return index;
        }
    }
    return -1;
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
    return "["+this.join(",")+"]"
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
    if (this.length == 0) { return "" }
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
function http_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_response = new http_Response(200,"text/plain","","");http_port = process.env.PORT || 3000;http_server = server_createServer;http_handleQuery = server_handleQuery;http_isQuery = server_isQuery;;return;}}}()}var http_response;var http_port;var http_server;var http_handleQuery;var http_isQuery;function http_Server(c){this.listen=c;}http_Server.fields=["listen"];function http_NodeHTTP(c){this.createServer=c;}http_NodeHTTP.fields=["createServer"];function http_Request(c){this.url=c;}http_Request.fields=["url"];function http_Response(c,d,f){this.status=c;this.contentType=d;this.body=f;}http_Response.fields=["status","contentType","body"];http_Response.prototype.toString=(function(){return http_Response_toString(this)});function http_Response_toString(http_self){;return (((((((((((("Response(")+(((http_self).status)).toString()))+(", ").toString()))+(((http_self).contentType)).toString()))+(", ").toString()))+(((http_self).body)).toString()))+(")").toString());}function http_endResponse(http_x){;return core_assign(http_response,{body:jsonStringify(http_x)});}function http_toUrl(http_expects){;return ("query/"+jsonStringify(http_expects(http_endResponse)));}function html_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:html_style = html_newAttrib.bind(null,"style");html_placeHolder = html_newAttrib.bind(null,"placeholder");html_position = html_newAttrib.bind(null,"position");html__type = html_newAttrib.bind(null,"type");html_height = html_newAttrib.bind(null,"height");html_width = html_newAttrib.bind(null,"width");html_id = html_newAttrib.bind(null,"id");html_min = html_newAttrib.bind(null,"min");html_max = html_newAttrib.bind(null,"max");html_step = html_newAttrib.bind(null,"step");html_value = html_newAttrib.bind(null,"value");html_href = html_newAttrib.bind(null,"href");html_src = html_newAttrib.bind(null,"src");html_kind = html_newAttrib.bind(null,"type");html__float = html_newAttrib.bind(null,"float");html_class = html_newAttrib.bind(null,"className");html_onClick = html_onEvent.bind(null,"onclick");html_onInput = html_onEvent.bind(null,"oninput");html_onChange = html_onEvent.bind(null,"onchange");html_noAttrib = EmptyVector;;return;}}}()}var html_style;var html_placeHolder;var html_position;var html__type;var html_height;var html_width;var html_id;var html_min;var html_max;var html_step;var html_value;var html_href;var html_src;var html_kind;var html__float;var html_class;var html_onClick;var html_onInput;var html_onChange;var html_noAttrib;function html_PosAtom(c,d){this.a=c;this.pos=d;}html_PosAtom.fields=["a","pos"];html_PosAtom.prototype.unary_read=(function(c){return html_PosAtom_unary_read(this,c)});function html_PosAtom_unary_read(html_self,d){var h=0;return function g(f){while(1){switch(h){case 0:h=1;return (html_self).a.unary_read(g);case 1:;;return d(((html_self).pos).query(f));}}}()}html_PosAtom.prototype.operator_set=(function(c,d){return html_PosAtom_operator_set(this,c,d)});function html_PosAtom_operator_set(html_self, html_new,f){var j=0;return function h(g){while(1){switch(j){case 0:j=2;return (html_self).a.unary_read(h);case 2:;j=3;return ((html_self).a).operator_set(((html_self).pos).set(g,html_new),h);case 3:;return f();}}}()}html_PosAtom.prototype.watch=(function(c,d){return html_PosAtom_watch(this,c,d)});function html_PosAtom_watch(html_self, html_f,f){var j=0;return function h(g){while(1){switch(j){case 0:function html_func(html_x,k){var n=0;return function m(l){while(1){switch(n){case 0:n=4;return (html_self).a.unary_read(m);case 4:;n=5;return html_f(((html_self).pos).query(l),m);case 5:;return k();}}}()}j=6;return ((html_self).a).watch(html_func,h);case 6:;return f();}}}()}function html_comp(html_func){;return html_func;}function html_Event(c){this.target=c;}html_Event.fields=["target"];function html_Attribute(c,d){this.name=c;this.value=d;}html_Attribute.fields=["name","value"];function html_newAttrib(html_name, html_value){;return new html_Attribute(html_name,html_value,html_value);}function html_onEvent(html_name, html_x, html_a){function html_clicked(html_e,c){var g=0;return function f(d){while(1){switch(g){case 0:g=7;return html_a.unary_read(f);case 7:;g=8;return html_x(d,html_e,f);case 8:g=9;return (html_a).operator_set(d,f);case 9:;return c();}}}()};return new html_Attribute(html_name,html_clicked,html_clicked);}function html_async(html_x, html_a){function html_fired(c){var g=0;return function f(d){while(1){switch(g){case 0:g=14;return html_a.unary_read(f);case 14:;g=15;return html_x(d,f);case 15:g=16;return (html_a).operator_set(d,f);case 16:;return c();}}}()};return html_fired;}function html_ignoreAct(html_f){function html_func(html_x, html_y,c){var g=0;return function f(d){while(1){switch(g){case 0:g=17;return html_f(html_x,f);case 17:;return c(d);}}}()};return html_func;}function html_withId(html_f){function html_func(html_id, html_m, html_e,c){var html_res;var g=0;return function f(d){while(1){switch(g){case 0:g=18;return html_f(html_m.get(html_id),html_e,f);case 18:html_res = (d);;return c((html_m).set(html_id,html_res));}}}()};return html_func;}function html_mapWithId(html_v, html_arr, html_a){function html_func(html_id){;return html_v(html_arr.get(html_id),html_id,html_a);};return (newVectorRange(0,(html_arr).length)).map(html_func);}function html_toEffect(html_f){function html_func(html_x, html_ev,c){var g=0;return function f(d){while(1){switch(g){case 0:;return c(html_f(html_x,html_ev));}}}()};return html_func;}function html_mapView(html_v, html_model, html_a){function html_mapper(html_idx){var html_result;html_result = html_model.get(html_idx);var html_pos;html_pos = newLens(function(c){return c.get(html_idx)}, function(d,c){return d.set(html_idx,c)});var html_newA;html_newA = new html_PosAtom(html_a,html_pos,html_pos);;return html_v(html_result,html_newA);};return (newVectorRange(0,(html_model).length)).map(html_mapper);}function html_viewFromLens(html_v, html_model, html_pos, html_a){;return html_v(((html_pos).query(html_model)),new html_PosAtom(html_a,html_pos,html_pos));}function html_get(c){var g=0;return function f(d){while(1){switch(g){case 0:;return c();}}}()}function main_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:http_nodeInit();main__read = server_readFile;main_quit = process.exit;main_server = http_server(main_requestHandler);d=5;return (main_server).listen(http_port,c);case 5:log((((("started web server on port ")+((http_port)).toString()))+("").toString()));html_nodeInit();main_onChange= typeof html_onChange=='undefined'||html_onChange;main_app= typeof html_app=='undefined'||html_app;main_style= typeof html_style=='undefined'||html_style;main_render= typeof html_render=='undefined'||html_render;main_onClick= typeof html_onClick=='undefined'||html_onClick;main_comp= typeof html_comp=='undefined'||html_comp;main_mapView= typeof html_mapView=='undefined'||html_mapView;main_toEffect= typeof html_toEffect=='undefined'||html_toEffect;main_unique = main_for.bind(null,((function(main_elem, main_indiv){;return (function(){if((!((main_indiv).has(main_elem)))){return [(Some(main_elem)),(main_indiv).append(main_elem)];}
else{return [None,main_indiv];}})();})),EmptyVector);main_sort = function(arr){
    return fromArray(arr.toArray().sort(function(x,y){
        return x > y
    } ));
} ;main__console = console.log;main_math = (function(main_x, main_a){;return main_div(EmptyVector,newVector(main_input(newVector(main_onChange(main_enter,main_a)),""),main_answer(main_x)));});main_appState = newAtom((previousState).arg);;return;}}}()}var main__read;var main_quit;var main_server;var main_unique;var main_sort;var main__console;var main_math;var main_appState;var main_h1;var main_onChange;var main_input;var main_span;var main_p;var main_br;var main_button;var main_app;var main_div;var main_style;var main_render;var main_onClick;var main_comp;var main_mapView;var main_toEffect;function main_read(main_path,c){var main_Some;var main_x;var main_None;var g=0;return function f(d){while(1){switch(g){case 0:g=1;return main__read(main_path,f);case 1:;return c(function(){var h=d; if (h[0]==0){var main_x=h[1];return main_x;} if (h[0]==1){log(("cannot find file, "+main_path));return main_quit(1);}}());}}}()}function main_requestHandler(main_req,c){var main_Some;var main_content;var main_None;var g=0;return function f(d){while(1){switch(g){case 0:log(("request, "+(main_req).url));var h=(main_req).url; if (h=="/"){g=3;return main__read("EC.html",f);}/*case*/g=4;break;/*case*/case 3:d=function(){var j=d; if (j[0]==0){var main_content=j[1];return core_assign(http_response,{body:main_content,contentType:"text/html"});} if (j[0]==1){return core_assign(http_response,{status:404});}}();g=2;/*block*/break;/*if*/case 4:/*notif*/ if (1){d=core_assign(http_response,{status:404,body:"404 Page not found"});g=2;/*block*/break;}case 2:;return c(d);}}}()}function main_Result(f){this[0]=f}function main_Data(c){var f = new main_Result(0);f[1]=c;return f}var main_Error= new main_Result(1);function main_for(main_func, main__state, main_arr){var main_state;main_state = main__state;var main_new;main_new = EmptyVector;var main_length;main_length = (main_arr).length;var main_i;main_i = 0;
while((main_i<main_length)){var main_tx;main_tx = main_func(main_arr.get(main_i),main_state);var main_t;main_t = (main_tx)[0];main_state=(main_tx)[1];main_new=function(){var c=main_t; if (c[0]==0){var main_tmp=c[1];return (main_new).append(main_tmp);} if (c[0]==1){return main_new;}}();main_i=((main_i+1)|0);};return main_new;}main_Result.prototype.withDefault=(function(c){return main_Result_withDefault(this,c)});function main_Result_withDefault(main_self, main_default){;return function(){var d=main_self; if (d[0]==0){var main_x=d[1];return main_x;} if (d[0]==1){return main_default;}}();}main_Result.prototype.map=(function(c){return main_Result_map(this,c)});function main_Result_map(main_self, main_func){;return function(){var d=main_self; if (d[0]==0){var main_x=d[1];return main_Data(main_func(main_x));} if (d[0]==1){return main_Error;}}();}function main_median(main_x){var main_length;main_length = (main_x).length;var main_tmp;main_tmp = main_sort(main_x);;return (function(){if((((main_length%2)|0)===0)){return (((main_tmp.get(((main_length/2)|0))+main_tmp.get(((((main_length/2)|0)-1)|0))))/2.0);}
else{return main_tmp.get((((((main_length-1)|0))/2)|0));}})();}function main_average(main_x){;return (((main_x).reduce((operator_add)))/toFloat((main_x).length));}function main_debug(main_x){main__console((main_x).toString());;return main_x;}function main_mode(main_x){var main_uniques;main_uniques = (main_unique(main_x));var main_u;main_u = (main_uniques).map((function(main_i){;return [(((("")+((main_i)).toString()))+("").toString()),(((main_x).filter(operator_eq.bind(null,main_i)))).length,0];}));var main_count;main_count = (main_u).reduce((function(main_a, main_b){;return (function(){if(((main_a)[1]>(main_b)[1])){return main_a;}else if(((main_a)[1]===(main_b)[1])){return ["b",(main_b)[1],(((main_a)[2]+1)|0)];}
else{return main_b;}})();}));var main__;main__ = main_debug((main_count)[2]);;return (function(){if(((main_count)[2]===(((main_uniques).length-1)|0))){return "n";}
else{return (main_count)[0];}})();}function main_enter(main_x, main_ev,c){var g=0;return function f(d){while(1){switch(g){case 0:;return c(parseJson(core_json_vector(core_json_float),(((("[")+((((main_ev).target).value)).toString()))+("]").toString())));}}}()}main_nodeInit();