function op_add(x,y) {return x.op_add(y)}
function op_sub(x,y) {return x.op_sub(y)}
function op_mul(x,y) {return x.op_mul(y)}
function op_div(x,y) {return x.op_div(y)}
function op_mod(x,y) {return x.op_mod(y)}
function op_eq(x,y) {return x.op_eq(y)}
function op_pow(x,y) {return Math.pow(x,y)}
function op_lt(x,y) {return x.op_lt(y)}
function op_gt(x,y) {return x.op_gt(y)}
function op_or(x,y) {return x || y}
function op_not(x) {return !x}
function op_and(x,y) { return x && y }
function op_ne(x,y) { return x.op_ne(y) }

function unary_add(x) {return x}
function unary_sub(x) {return -x}

Number.prototype.op_add = function (other) { return this + other }
Number.prototype.op_div = function (other) { return this / other }
Number.prototype.op_sub = function (other) { return this - other }
Number.prototype.op_mul = function (other) { return this * other }
Number.prototype.op_eq = function (other) { return this == other }
Number.prototype.op_mod = function (other) { return this % other }
Number.prototype.op_lt = function (other) { return this < other }
Number.prototype.op_gt = function (other) { return this > other }
Number.prototype.op_ne = function (other) { return this != other }

Number.prototype.toFloat = function () { return this }
Number.prototype.toInt = function () { return this | 0 }

String.prototype.op_eq = function (other) { return this == other }
String.prototype.op_ne = function (other) { return this != other }
String.prototype.op_add = function (other) { return this + other }
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
String.prototype.op_eq = function(s) { return this == s }

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

function op_set(val, next) {
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

function atom_update(func, next) {
  this.op_set(func(this.arg), next);
}

function newAtom(arg) {
    return {
        unary_read: unary_read,
        op_set: op_set,
        arg: arg,
        watch: atom_watch,
        events: [],
        toString: function(){return ""},
        update: atom_update
    }
}

function newLens(reader, setter, string) {
    return {
        query: function(item) {
            return reader(item);
        },
        set: function(old, item) {
            return setter(old, item)
        },
        toString: function() {
            return string;
        }
    }
}

function defer(func) {
    return function (x) {
        return function (callback) { func(x, callback) }
    }
}

function Maybe(x) {
    this[0] = x;
}

function Some(x) {
    var s = new Maybe(0);
    s[1] = x;
    return s
}

var None = new Some(1);

function Maybe_withDefault(self,def){
    if (def[0] == 0) {
        return self[1];
    } else {
        return def;
    }
}


function Maybe_map(self,func){
    if (def[0] == 0) {
        return Some(func(def[1]));
    } else {
        return None;
    }
}

Maybe.prototype.withDefault = function(def){
    return Maybe_withDefault(this,def);
}

Maybe.prototype.map = function(func){
    return Maybe_map(this,def);
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

Vector.prototype.serial = function (func, next) {
    serial(this.map(defer(func)), next);
}

Vector.prototype.parallel = function (func, next) {
    parallel(this.map(defer(func)), next);
}

Vector.prototype.toJSON = function() {
    return this.toArray();
}

Vector.prototype.indexOf = function(find) {
    var index = -1;
    for (var i = 0; i < this.length; i++) {
        if (this.get(i).op_eq(find)) {
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
            tmp = [];
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
                var newNode = [];
            } else {
                var newNode = node.slice();
            }

            newNode[pos] = update(newNode[pos], level - bits, key);
            return newNode;
        } else {
            var pos = key & mask;

            if (node == null) {
                var newNode = [];
            } else {
                var newNode = node.slice();
            }
            newNode[pos] = value;
            return newNode
        }
    }

    var width = Vector.prototype.width;

    if (Math.pow(width, this.depth) === this.length) {
        var n = [];
        n[0] = this.root;
        n[1] = [];

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

Vector.prototype.op_eq = function (other) {
    if (this.length !== other.length) return false;
    if (this === other) return true;

    for (var i = 0; i < this.length; i++) {
        if (!(this.get(i).op_eq(other.get(i)))) {
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
        if (this.get(i).op_eq(s)) {
            return true;
        }
    }
    return false;
}

Vector.prototype.op_add = function (s) {
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
}
'use strict';

var Map;
var nil;

(function() {
    var create_if_new, new_node, with_lev, with_lo_hi, with_lo, with_hi, go_lo,
        has, get, put, rm, skew, split, keys, values, to_object, to_pair_array, print, map;

    Map = function(node, lt) {
        this.length = node ? node.length : 0;
        this.contains = function(key) {
            return has(node, key, lt);
        };
        this.get = function(key, fail) {
            return get(node, key, fail, lt);
        };
        this.set = function(key, val) {
            return create_if_new(this, node, put(node, key, val, lt), lt);
        };
        this.remove = function(key) {
            return create_if_new(this, node, rm(node, key, lt), lt);
        };
        this.keys = function(into) {
            return keys(node, into || []);
        };
        this.values = function(into) {
            return values(node, into || []);
        };
        this.toObject = function(into) {
            return to_object(node, into || {});
        };
        this.toString = function() {
            return node ? '{ ' + print(node) + ' }' : '{}';
        };

        this.map = function(func, into) {
          console.log(node);
          return map(func, node, into||new Map(nil,nil));
        }
    }

    create_if_new = function(map, node, new_node, lt) {
        return node === new_node ? map : new Map(new_node, lt);
    };

    new_node = function(key, val, lev, lo, hi) {
        var length = 1 + (lo ? lo.length : 0) + (hi ? hi.length : 0);
        return {
            key: key,
            val: val,
            lev: lev,
            lo: lo,
            hi: hi,
            length: length
        };
    };

    with_lev = function(node, lev) {
        return new_node(node.key, node.val, lev, node.lo, node.hi);
    };
    with_lo_hi = function(node, lo, hi) {
        return new_node(node.key, node.val, node.lev, lo, hi);
    };
    with_lo = function(node, lo) {
        return lo && lo.op_eq(node.lo) ? node : with_lo_hi(node, lo, node.hi);
    };
    with_hi = function(node, hi) {
        return hi === node.hi ? node : with_lo_hi(node, node.lo, hi);
    };
    go_lo = function(node, key, lt) {
        return (lt && lt(key, node.key)) || (!lt && key.op_lt( node.key));
    };


    has = function(node, key, lt) {
        while (node) {
            if (key.op_eq(node.key)) {
                return true;
            }
            node = go_lo(node, key, lt) ? node.lo : node.hi;
        }
        return false;
    };

    map = function(func, node, a) {
          if (node) {
              a = map(func, node.lo, a);
              a = a.set(node.key, func(node.val));
              a = map(func, node.hi, a);
          }
          return a;
    };

    get = function(node, key, fail, lt) {
        while (node) {
            if (key.op_eq(node.key)) {
                return node.val;
            }
            node = go_lo(node, key, lt) ? node.lo : node.hi;
        }
        return fail;
    };

    put = function(node, key, val, lt) {
        if (!node) {
            return new_node(key, val, 0);
        }
        if (key.op_eq(node.key)) {
            return val.op_eq(node.val) ? node : new_node(key, val, node.lev, node.lo, node.hi);
        }
        node = go_lo(node, key, lt) ? skew(node, put(node.lo, key, val, lt)) :
            skew(with_hi(node, put(node.hi, key, val, lt)));
        return split(node);
    };

    rm = function(node, key, lt) {
        if (node) {
            var lo = node.lo,
                hi = node.hi,
                hi_lo, lev = node.lev;
            if (key.op_eq(node.key)) {
                if (!lo || !hi) {
                    return lo || hi;
                }
                hi_lo = hi;
                while (hi_lo.lo) { // find replacement
                    hi_lo = hi_lo.lo;
                }
                hi = rm(hi, hi_lo.key, lt);
                node = new_node(hi_lo.key, hi_lo.val, lev, lo, hi);
            } else if (go_lo(node, key, lt)) {
                lo = rm(lo, key, lt);
                node = with_lo(node, lo);
            } else {
                hi = rm(hi, key, lt);
                node = with_hi(node, hi);
            }
            if ((lo && lo.lev < lev - 1) || (hi && hi.lev < lev - 1)) {
                node = new_node(node.key, node.val, lev - 1, lo, hi && hi.lev .op_gt( lev) ? with_lev(hi, lev - 1) : hi);
                node = skew(node);
                if (node.hi) {
                    node = with_hi(node, skew(node.hi));
                }
                if (node.hi && node.hi.hi) {
                    node = with_hi(node, with_hi(node.hi, skew(node.hi.hi)));
                }
                node = split(node);
                if (node.hi) {
                    node = with_hi(node, split(node.hi));
                }
            }
        }
        return node;
    };

    skew = function(node, lo) {
        lo = lo || node.lo;
        return !lo || node.lev > lo.lev ? with_lo(node, lo) : with_hi(lo, with_lo(node, lo.hi));
    };

    split = function(node) {
        var hi = node.hi;
        return !hi || !hi.hi || node.lev > hi.hi.lev ? node : new_node(hi.key, hi.val, hi.lev + 1, with_hi(node, hi.lo), hi.hi);
    };

    keys = function(node, a) {
        if (node) {
            keys(node.lo, a);
            a.push(node.key);
            keys(node.hi, a);
        }
        return a;
    };

    values = function(node, a) {
        if (node) {
            values(node.lo, a);
            a.push(node.val);
            values(node.hi, a);
        }
        return a;
    };

    to_object = function(node, o) {
        if (node) {
            to_object(node.lo, o);
            o[node.key] = node.val;
            to_object(node.hi, o);
        }
        return o;
    };

    to_pair_array = function(node, a) {
        if (node) {
            to_pair_array(node.lo, a);
            a.push(node.key + ': ' + node.val);
            to_pair_array(node.hi, a);
        }
        return a;
    };

    print = function(node) {
        return to_pair_array(node, []).join(', ');
    };

})();

function dict(obj,lt) {
  var map = new Map(nil,lt);
  for (var i = 0; i < obj.length; i++) {
    var res = obj.get(i);
    map = map.set(res[0], res[1]);
  }
  return map;
}function _sub_batch(subs) {
  function diff(other) {
    if (other.type == "sub") {
      var new_subs = this.subs.map(function(i, index){
        return i.diff(other.subs[index]);
      });
      return {type: "sub", subs: new_subs, init: init, diff: diff, reset: reset, end: end, count: this.count + 1};
    } else {
      other.count += 1;
      return other;
    }
  }

  function reset() {
    this.count = 0;
    this.subs.forEach(function(i) {
      i.reset();
    });
  }

  function end() {
    if (this.count == 0) {
      this.subs.forEach(function(i) {
        i.end();
      })
    }
  }

  function init() {
    this.subs.forEach(function (i) {
      i.init();
    });
  }

  return {type: "sub", reset: reset, diff: diff, subs: subs.toArray(), init: init, end: end, count: 0};
}

var _sub_none = (function() {
    function reset() {}
    function diff() { return this }
    function init() {}
    function end() {}

    return {type: "none", reset: reset, diff: diff, init: init, end: end, count: 0}
})()

function _sub_register(a, func, next) {
  a.unary_read(function(i) {
    var subs = func(i, a);
    subs.init();


    function changed(model, next) {
      var new_subs = func(model, a);
      subs.reset();
      nsubs = subs.diff(new_subs);
      subs.end();
      subs = nsubs;
      nsubs.init();

      return next();
    };

    a.watch(changed, function(){});
    next();
  });
}
;function _time_currentDate(next) {
    var t = new Date();
    next({
        hours: t.getHours(),
        minutes: t.getMinutes(),
        seconds: t.getSeconds()
    });
}

function _time_every(interval, a, func) {
  function diff(other) {
    if (other.type == "every" && other.interval == this.interval) {
      this.count += 1;
      return this;
    } else {
      other.count += 1;
      return other;
    }
  }

  function reset() {
    this.count = 0;
  }

  function end() {
    if (this.count == 0) {
    if (this.id) {
      clearInterval(this.id);
    }
    };
  }

  function call() {
    var self = this;
    _time_currentDate(function(time) {
        self.a.update(function(state) { return self.func(state, time) }, function(){});
    });
  }

  function init() {
    if (!this.id) {
      this.id = setInterval(call.bind(this), this.interval);
    }
  }

  return {type: "every", call: call, reset: reset, func: func, a: a, interval: interval, diff: diff, init: init, end: end, count: 0};
};function _router_onUrlChange(a, func) {
  function diff(other) {
    if (other.type == "urlchange") {
      this.count += 1;
      return this;
    } else {
      other.count += 1;
      return other;
    }
  }

  function reset() {
    this.count = 0;
  }

  function end() {
    if (this.count == 0) {
    if (this.initialized) {
      window.removeEventListener("hashchange", call);
    }
    };
  }

  function call() {
    var self = this;
    self.a.update(function(state){
        return self.func(state, window.location.hash);
    }, function(){})
  }

  function init() {
    if (!this.initialized) {
        this.initialized = true;
        window.addEventListener("hashchange", call.bind(this));
    }
  }

  return {type: "urlchange", call: call, reset: reset, func: func, a: a, diff: diff, init: init, end: end, count: 0};
}

function new_sub(a, func) {
    function diff(other) {
        return (other.type == "urlchange")
    }

  function end() {
    if (this.initialized) {
      window.removeEventListener("hashchange", call);
    }
  }

  function call() {
    var self = this;
    self.a.update(function(state){
        return self.func(state, window.location.hash);
    }, function(){})
  }

  function init() {
        this.initialized = true;
        window.addEventListener("hashchange", call.bind(this));
  }

  return create_new_sub({type: "urlchange", call: call, func: func, a: a, diff: diff, init: init, end: end});
}

function _router_getHash(next) {
    next(window.location.hash);
}

function _router_changeHash(str, next) {
    window.location.hash = str;
    next();
};var main_fs = require("fs");
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

var _html_changeName = function _html_changeName(event, name) {
    function hello(x,y,z) {
        event(x,y,z);
    }
    Object.defineProperty(hello, 'name', { writable: true });
    hello.name = name;
    return hello;
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
function router_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:sub_nodeInit();;router_Sub= typeof sub_Sub=='undefined'||sub_Sub;;;return;}}}()}function sub_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:;sub_register = _sub_register;sub_batch = _sub_batch;sub_nil = _sub_none;;return;}}}()}function sub_Sub(){}sub_Sub._fields=[];function main_nodeInit(){var d=0;return function c(b){while(1){switch (d){case 0:router_nodeInit();;main_Sub= typeof router_Sub=='undefined'||router_Sub;;main_nil= typeof sub_nil=='undefined'||sub_nil;main_batch= typeof sub_batch=='undefined'||sub_batch;main_register= typeof sub_register=='undefined'||sub_register;main_Sub= typeof sub_Sub=='undefined'||sub_Sub;;;;log("hello world");;return;}}}()}function main_Attrib(){}main_Attrib._fields=[];function main_Html(){}main_Html._fields=[];function main_h(){;}main_nodeInit();