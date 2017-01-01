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
}
function main_Init(){var d=0;return function c(b){while(1){switch (d){case 0:svg_Init();main_random = toAsync(Math.random);main_cos = Math.cos;main_sin = Math.sin;main_sqrt = Math.sqrt;main_atan2 = Math.atan2;main_pi = Math.PI;main_abs = Math.abs;d=1;return serial((newVectorRange(0,100)).map(defer(main_generate)),c);case 1:main_appState = newAtom(new main_Game((b),10,10));return;}}}()}var main_random;var main_cos;var main_sin;var main_sqrt;var main_atan2;var main_pi;var main_abs;var main_appState;function main_Particle(f,g,h,j,k,l){this.x=f;this.y=g;this.limitX=h;this.limitY=j;this.velX=k;this.velY=l;}main_Particle.fields=newVector("x","y","limitX","limitY","velX","velY");function main_Game(m,n){this.particles=m;this.speed=n;}main_Game.fields=newVector("particles","speed");function main_returnId(c){return c;}function main_generate(c,d){var j;var h=0;return function g(f){while(1){switch(h){case 0:h=2;return main_random(g);case 2:j = ((f)/2.0);h=3;return main_random(g);case 3:h=4;return main_random(g);case 4:return d(new main_Particle((800.0*f),(500.0*f),800.0,500.0,j,(0.5-j),(0.5-j)));}}}()}main_Particle.prototype.toString=(function(){return main_Particle_toString(this)});function main_Particle_toString(c){return (((((((((((((((((((((((("Particle(")+(((c).x)).toString()))+(", ").toString()))+(((c).y)).toString()))+(", ").toString()))+(((c).limitX)).toString()))+(", ").toString()))+(((c).limitY)).toString()))+(", ").toString()))+(((c).velX)).toString()))+(", ").toString()))+(((c).velY)).toString()))+(")").toString());}function main_particle(c, d){return (function(){if(((c).x>((c).limitX-20.0))){return new main_Particle(((c).limitX-21.0),(c).y,(c).limitX,(c).limitY,(-(c).velX),(c).velY,(c).velY);}else if(((c).x<0.0)){return new main_Particle(4.0,(c).y,(c).limitX,(c).limitY,(-(c).velX),(c).velY,(c).velY);}else if(((c).y>((c).limitY-20.0))){return new main_Particle((c).x,((c).limitY-21.0),(c).limitX,(c).limitY,(c).velX,((-(c).velY)+0.2),((-(c).velY)+0.2));}else if(((c).y<0.0)){return new main_Particle((c).x,4.0,(c).limitX,(c).limitY,(c).velX,((-(c).velY)+0.2),((-(c).velY)+0.2));}
else{return new main_Particle(((c).x+((toFloat(d))*(c).velX)),((c).y+((toFloat(d))*(c).velY)),(c).limitX,(c).limitY,(c).velX,(c).velY,(c).velY);}})();}function main_setX(c, d){return new main_Particle((c).x,(c).y,(c).limitX,(c).limitY,d,(c).velY,(c).velY);}function main_setY(c, d){return new main_Particle((c).x,(c).y,(c).limitX,(c).limitY,(c).velX,d,d);}function main_collision(c){var d;d = c;var f;f = (c).length;var g;g = 0;
while((g<f)){var h;h = ((g+1)|0);
while((h<f)){var j;j = d.get(g);var k;k = d.get(h);var l;l = main_abs(((j).x-(k).x));var m;m = main_abs(((j).y-(k).y));var n;n = main_sqrt(((l*l)+(m*m)));if((n<30.0)){var p;p = main_manageBounce(j,k);d=(d).set(g,p.get(0));d=(d).set(h,p.get(1));;}h=((h+1)|0);}g=((g+1)|0);}return d;}function main_gameLoop(c, d,f){var k;var j=0;return function h(g){while(1){switch(j){case 0:k = (((c).particles).map((function(m){return function(l){return main_particle(l,m);}})(d)));return f(new main_Game((main_collision(k)),(c).speed,(c).speed));}}}()}function main_render(c){return svg_image(newVector(svg_href("http://vignette2.wikia.nocookie.net/chemistry/images/d/d1/500px-Water_molecule.svg.png/revision/latest?cb=200100320204351"),svg_width("20"),svg_height("20"),svg_x(((c).x).toString()),svg_y(((c).y).toString())));}function main_manageBounce(c, d){var f;f = ((c).x-(d).x);var g;g = ((c).y-(d).y);var h;h = (main_atan2(g,f));var j;j = (main_sqrt((((c).velX*(c).velX)+((c).velY*(c).velY))));var k;k = (main_sqrt((((d).velX*(d).velX)+((d).velY*(d).velY))));var l;l = (main_atan2((c).velY,(c).velX));var m;m = (main_atan2((d).velY,(d).velX));var n;n = (j*(main_cos((l-h))));var p;p = (j*(main_sin((l-h))));var q;q = (k*(main_cos((m-h))));var r;r = (k*(main_sin((m-h))));var s;s = ((((((1.0-1.0))*n)+(((1.0+1.0))*q)))/((1.0+1.0)));var t;t = ((((((1.0+1.0))*n)+(((1.0-1.0))*q)))/((1.0+1.0)));var v;v = p;var w;w = r;var x;x = (((main_cos(h))*s)+((main_cos((h+(main_pi/2.0))))*v));var y;y = (((main_sin(h))*s)+((main_sin((h+(main_pi/2.0))))*v));var z;z = (((main_cos(h))*t)+((main_cos((h+(main_pi/2.0))))*w));var B;B = (((main_sin(h))*t)+((main_sin((h+(main_pi/2.0))))*w));var C;C = (function(){if((((c).y>0.0)&&((c).y<(d).y))){return ((c).y-0.25);}
else{return (c).y;}})();var D;D = (function(){if((((d).y>0.0)&&((c).y>(d).y))){return ((d).y-0.25);}
else{return (d).y;}})();return newVector(new main_Particle((c).x,C,(c).limitX,(c).limitY,x,y,y),new main_Particle((d).x,D,(d).limitX,(d).limitY,z,B,B));}function main_changeNumber(c, d,f){var k;var l;var m;var j=0;return function h(g){while(1){switch(j){case 0:k = toInt(((d).target).value);l = ((c).particles).length;m = (1.0/(toFloat(((11-k)|0))));function n(p,q){var v;var t=0;return function s(r){while(1){switch(t){case 0:t=5;return main_generate(p,s);case 5:v = r;return q(main_adjust(m,v));}}}()}if((k>l)){j=7;return serial((newVectorRange(0,((k-l)|0))).map(defer(n)),h);}j=8;break;case 7:g=new main_Game((c).particles.operator_add((g)),(c).speed,(c).speed);j=6;/*block*/break;/*if*/case 8:/*notif*/{g=new main_Game((((c).particles).shorten(((l-k)|0))),(c).speed,(c).speed);};j=6;/*block*/break;case 6:return f(g);}}}()}function main_adjust(c, d){var f;f = ((d).velX*c);var g;g = ((d).velY*c);return main_setY((main_setX(d,f)),g);}function main_changeSpeed(c, d,f){var k;var l;var m;var n;var j=0;return function h(g){while(1){switch(j){case 0:k = toInt(((d).target).value);l = (1.0/(toFloat(((11-k)|0))));m = (1.0/(toFloat(((11-(c).speed)|0))));n = (l/m);return f(new main_Game(((c).particles).map(main_adjust.bind(null,n)),k,k));}}}()}function main_game(c, d){return html_div(html_noAttrib,newVector(html_h1(html_noAttrib,"States of matter simulations, by Lucas Goetz"),html_h3(html_noAttrib,(((("")+((((c).particles).length)).toString()))+(" Particles").toString())),html_input(newVector((html__type("range")),(html_height("10")),(html_width("100")),(html_min(0)),(html_max(200)),html_onInput(main_changeNumber,d)),""),html_h3(html_noAttrib,(((("")+(((((((c).speed*10)|0)+4)|0))).toString()))+(" Degrees Celsius").toString())),html_input(newVector((html__type("range")),(html_height("10")),(html_width("100")),(html_min(1)),(html_max(10)),(html_value((((("")+(((c).speed)).toString()))+("").toString()))),html_onInput(main_changeSpeed,d)),""),svg__svg(newVector((svg_width("100%")),svg_height("100%")),newVector(svg_rect(newVector((svg_width("800")),(svg_height("500")),(svg_fill("rgba(0,0,0,0.0)")),svg_stroke("black"))),((c).particles).map(main_render)))));}function html_Init(){var d=0;return function c(b){while(1){switch (d){case 0:html_style = html_newAttrib.bind(null,"style");html_placeHolder = html_newAttrib.bind(null,"placeholder");html_position = html_newAttrib.bind(null,"position");html__type = html_newAttrib.bind(null,"type");html_height = html_newAttrib.bind(null,"height");html_width = html_newAttrib.bind(null,"width");html_min = html_newAttrib.bind(null,"min");html_max = html_newAttrib.bind(null,"max");html_step = html_newAttrib.bind(null,"step");html_value = html_newAttrib.bind(null,"value");html_onClick = html_onEvent.bind(null,"onclick");html_onInput = html_onEvent.bind(null,"oninput");html_onChange = html_onEvent.bind(null,"onchange");html_h = fromJS(html_h);html_createElement = virtualDom.create;html_diff = virtualDom.diff;html_patch = toAsync(virtualDom.patch);html_clear = toAsync(clearElement);html_cssSelector = document.querySelector.bind(document);html_h1 = html_h.bind(null,"h1");html_h2 = html_h.bind(null,"h2");html_h3 = html_h.bind(null,"h3");html_h4 = html_h.bind(null,"h4");html_h5 = html_h.bind(null,"h5");html_h6 = html_h.bind(null,"h6");html_button = html_h.bind(null,"button");html_input = html_h.bind(null,"input");html_noAttrib = newVector();html_div = html_h.bind(null,"div");html_p = html_h.bind(null,"p");html_appendChild = toAsync(html_appendChild);return;}}}()}var html_style;var html_placeHolder;var html_position;var html__type;var html_height;var html_width;var html_min;var html_max;var html_step;var html_value;var html_onClick;var html_onInput;var html_onChange;var html_h;var html_createElement;var html_diff;var html_patch;var html_clear;var html_cssSelector;var html_h1;var html_h2;var html_h3;var html_h4;var html_h5;var html_h6;var html_button;var html_input;var html_noAttrib;var html_div;var html_p;var html_appendChild;function html_PosAtom(f,g){this.a=f;this.pos=g;}html_PosAtom.fields=newVector("a","pos");html_PosAtom.prototype.unary_read=(function(c){return html_PosAtom_unary_read(this,c)});function html_PosAtom_unary_read(d,f){var j=0;return function h(g){while(1){switch(j){case 0:j=1;return (d).a.unary_read(h);case 1:;return f(((d).pos).query(g));}}}()}html_PosAtom.prototype.operator_set=(function(c,d){return html_PosAtom_operator_set(this,c,d)});function html_PosAtom_operator_set(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=2;return (f).a.unary_read(k);case 2:;l=3;return ((f).a).operator_set(((f).pos).set(j,g),k);case 3:return h(j);}}}()}html_PosAtom.prototype.watch=(function(c,d){return html_PosAtom_watch(this,c,d)});function html_PosAtom_watch(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:function m(n,p){var s=0;return function r(q){while(1){switch(s){case 0:s=4;return (f).a.unary_read(r);case 4:;s=5;return g(((f).pos).query(q),r);case 5:return p(q);}}}()}l=6;return ((f).a).watch(m,k);case 6:return h(j);}}}()}function html_Event(h){this.target=h;}html_Event.fields=newVector("target");function html_Attribute(j,k){this.name=j;this.value=k;}html_Attribute.fields=newVector("name","value");function html_newAttrib(c, d){return new html_Attribute(c,d,d);}function html_onEvent(c, d, f){function g(h,j){var m=0;return function l(k){while(1){switch(m){case 0:m=7;return f.unary_read(l);case 7:;m=8;return d(k,h,l);case 8:m=9;return (f).operator_set(k,l);case 9:return j(k);}}}()}return new html_Attribute(c,g,g);}function html_async(c, d){function f(g){var k=0;return function j(h){while(1){switch(k){case 0:k=10;return d.unary_read(j);case 10:;k=11;return c(h,j);case 11:k=12;return (d).operator_set(h,j);case 12:return g(h);}}}()}return f;}function html_ignoreAct(c){function d(f, g,h){var l=0;return function k(j){while(1){switch(l){case 0:l=13;return c(f,k);case 13:return h(j);}}}()}return d;}function html_withId(c){function d(f, g, h,j){var n;var m=0;return function l(k){while(1){switch(m){case 0:m=14;return c(g.get(f),h,l);case 14:n = (k);return j((g).set(f,n));}}}()}return d;}function html_mapWithId(c, d, f){function g(h){return c(d.get(h),h,f);}return (newVectorRange(0,(d).length)).map(g);}function html_mapView(c, d, f){function g(h){var j;j = d.get(h);var k;k = newLens(function(l){return l.get(h)}, function(m,l){return m.set(h,l)});var n;n = new html_PosAtom(f,k,k);return c(j,n);}return (newVectorRange(0,(d).length)).map(g);}function html_viewFromLens(c, d, f, g){return c(((f).query(d)),new html_PosAtom(g,f,f));}function html_render(c,d){var j;var k;var h=0;return function g(f){while(1){switch(h){case 0:j = html_createElement(c);k = html_cssSelector("#code");h=15;return html_clear(k,g);case 15:h=16;return html_appendChild(k,j,g);case 16:return d(j);}}}()}function html_get(c){var g=0;return function f(d){while(1){switch(g){case 0:return c();}}}()}function html_app(c, d,f){var k;var l;var j=0;return function h(g){while(1){switch(j){case 0:j=17;return d.unary_read(h);case 17:;k = c((g),d);j=18;return html_get(h);case 18:j=19;return html_render(k,h);case 19:l = g;function m(n,p){var t;var v;var s=0;return function r(q){while(1){switch(s){case 0:t = c(n,d);v = html_diff(k,t);s=20;return html_patch(l,v,r);case 20:l=q;k=t;return p();}}}()}j=21;return (d).watch(m,h);case 21:return f(g);}}}()}function svg_Init(){var d=0;return function c(b){while(1){switch (d){case 0:html_Init();svg_h = fromJS(svg_h);svg__svg = svg_h.bind(null,"svg");svg_rect = (function(f,h){return function(g){return svg_h(f,g,h);}})("rect","");svg_circle = (function(j,l){return function(k){return svg_h(j,k,l);}})("circle","");svg_image = (function(m,p){return function(n){return svg_h(m,n,p);}})("image","");svg_width = html_newAttrib.bind(null,"width");svg_height = html_newAttrib.bind(null,"height");svg_fill = html_newAttrib.bind(null,"fill");svg_x = html_newAttrib.bind(null,"x");svg_y = html_newAttrib.bind(null,"y");svg_href = html_newAttrib.bind(null,"xlink:href");svg_stroke = html_newAttrib.bind(null,"stroke");svg_cy = html_newAttrib.bind(null,"cy");svg_cx = html_newAttrib.bind(null,"cx");svg_r = html_newAttrib.bind(null,"r");svg_gameLoop = core_fps;return;}}}()}var svg_h;var svg__svg;var svg_rect;var svg_circle;var svg_image;var svg_width;var svg_height;var svg_fill;var svg_x;var svg_y;var svg_href;var svg_stroke;var svg_cy;var svg_cx;var svg_r;var svg_gameLoop;function svg_fps(c, d, f,g){var k=0;return function j(h){while(1){switch(k){case 0:function l(m,n){var r=0;return function q(p){while(1){switch(r){case 0:r=1;return d.unary_read(q);case 1:;r=2;return c(p,m,q);case 2:r=3;return (d).operator_set(p,q);case 3:r=4;return sleep(0,q);case 4:return n(p);}}}()}svg_gameLoop(l,f);return g();}}}()}