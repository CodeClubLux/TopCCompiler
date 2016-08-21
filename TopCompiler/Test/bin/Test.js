"use strict";

function main_Init() {
    main_T
}

function main_T(a) {
    this.x = a;
}

function main_toString(b) {
    return newString(b);
}

function log(t) {
    console.log(t.toString())
}

function alert(t) {
    alert(t.toString())
}

function println(t) {
    stdout.innerHTML += t.toString() + "<br>"
}

function print(t) {
    stdout.innerHTML += t
}

function operator_add(t, r) {
    return t.operator_add(r)
}

function operator_sub(t, r) {
    return t.operator_sub(r)
}

function operator_mul(t, r) {
    return t.operator_mul(r)
}

function operator_div(t, r) {
    return t.operator_div(r)
}

function operator_mod(t, r) {
    return t.operator_mod(r)
}

function operator_eq(t, r) {
    return t.operator_eq(r)
}

function operator_pow(t, r) {
    return Math.pow(t, r)
}

function operator_lt(t, r) {
    return t.operator_lt(r)
}

function operator_gt(t, r) {
    return t.operator_gt(r)
}

function operator_or(t, r) {
    return t || r
}

function operator_not(t) {
    return !t
}

function operator_and(t, r) {
    return t && r
}

function unary_add(t) {
    return t
}

function unary_sub(t) {
    return -t
}

function newString(t) {
    return t.toString()
}

function string_toString(t) {
    return t
}

function int_toString(t) {
    return t.toString()
}

function float_toString(t) {
    return t.toString()
}

function array_toString(t) {
    return t.toString()
}

function log(t) {
    console.log(t.toString())
}

function isOdd(t) {
    return t % 2 != 0
}

function isEven(t) {
    return t % 2 == 0
}

function min(t, r) {
    return r > t ? t : r
}

function max(t, r) {
    return t > r ? t : r
}

function List(t, r) {
    this.head = t, this.tail = r, null === r ? null === t ? this.length = 0 : this.length = 1 : this.length = r.length + 1
}

function listFromArray(t) {
    for (var r = t.length, e = EmptyList, n = 0; r > n; n++) e = e.append(t[n]);
    return e
}

function newList() {
    return listFromArray(Array.prototype.slice.call(arguments))
}

function newListRange(t, r) {
    for (var e = EmptyList, n = t; r > n; n++) e = e.append(n);
    return e
}

function newListInit(t, r) {
    for (var e = EmptyList, n = 0; t > n; n++) e = e.append(n);
    return e
}

function Vector(t, r, e) {
    this.shift = (e - 1) * this.bits, this.root = t, this.length = r, this.depth = e
}

function newVector() {
    return fromArray(Array.prototype.slice.call(arguments))
}

function fromArray(t) {
    for (var r = EmptyVector, e = 0; e < t.length; e++) r = r.append(t[e]);
    return r
}

function newVectorRange(t, r) {
    for (var e = EmptyVector, n = t; r > n; n++) e = e.append(n);
    return e
}

function newVectorInit(t, r) {
    for (var e = EmptyVector, n = 0; t > n; n++) e = e.append(n);
    return e
}
var stdout = document.getElementById("code");
Number.prototype.operator_add = function(t) {
    return this + t
}, Number.prototype.operator_div = function(t) {
    return this / t
}, Number.prototype.operator_sub = function(t) {
    return this - t
}, Number.prototype.operator_mul = function(t) {
    return this * t
}, Number.prototype.operator_eq = function(t) {
    return this == t
}, Number.prototype.operator_mod = function(t) {
    return this % t
}, Number.prototype.operator_lt = function(t) {
    return t > this
}, Number.prototype.operator_gt = function(t) {
    return this > t
};
var EmptyList = new List(null, null);
List.prototype.append = function(t) {
    return new List(t, this)
}, List.prototype.toArray = function() {
    for (var t = [], r = this, e = 0; e < this.length; e++) t.push(r.head), r = r.tail;
    return t.reverse()
}, List.prototype.getProperIndex = function(t) {
    return 0 > t ? this.length + t : t
}, List.prototype.getList = function(t) {
    t = this.getProperIndex(t);
    for (var r = this.length - t - 1, e = this, n = 0; r > n; n++) e = e.tail;
    return e
}, List.prototype.get = function(t) {
    return this.getList(t).head
}, List.prototype.toString = function() {
    return "List(" + this.join(", ") + ")"
}, List.prototype.join = function(t) {
    null === t && (t = ",");
    var r = this;
    if (0 === this.length) return "";
    for (var e = r.head.toString(), n = 1; n < this.length; n++) r = r.tail, e = r.head.toString() + t.toString() + e;
    return e
}, List.prototype.insert = function(t, r) {
    function e(t, r, n) {
        if (0 > r) throw new Exception;
        return 0 === r ? t.append(n) : e(t.tail, r - 1, n).append(t.head)
    }
    return t = this.getProperIndex(t), e(this, this.length - t, r)
}, List.prototype.del = function(t) {
    function r(t, e) {
        if (0 > e) throw new Error("");
        if (1 === e) {
            var n = t.tail;
            return null === n && (n = EmptyList), n
        }
        return r(t.tail, e - 1).append(t.head)
    }
    return t = this.getProperIndex(t), r(this, this.length - t)
}, List.prototype.slice = function(t, r) {
    null == t && (t = 0), null == r && (r = this.length), r = this.getProperIndex(r - 1), t = this.getProperIndex(t);
    var e = this.getList(r),
        n = new List(e.head, e.tail);
    return n.length = r - t + 1, n
}, List.prototype.reverse = function() {
    for (var t = EmptyList, r = this, e = 0; e < this.length; e++) t = t.append(r.head), r = r.tail;
    return t
}, List.prototype.operator_eq = function(t) {
    if (this.length !== t.length) return !1;
    if (r === t) return !0;
    for (var r = this, e = 0; e < this.length; e++) {
        if (!r.head.operator_eq(t.head)) return !1;
        r = r.tail, t = t.tail
    }
    return !0
}, List.prototype.operator_add = function(t) {
    function r(t, e, n) {
        if (0 > e) throw new Exception;
        return 0 == e ? new List(n.head, n.tail) : r(t.tail, e - 1, n).append(t.head)
    }
    return r(t, t.length, this)
}, List.prototype.copy = function() {
    function t(r, e) {
        if (0 > e) throw new Exception;
        return 0 == e ? r : t(r.tail, e - 1).append(r.head)
    }
    return t(this, this.length)
}, List.prototype.set = function(t, r) {
    function e(t, r, n) {
        if (0 > r) throw new Exception;
        return 0 === r ? new List(n, t.tail) : e(t.tail, r - 1, n).append(t.head)
    }
    return t = this.getProperIndex(t), e(this, this.length - t - 1, r)
}, Vector.prototype.bits = 5, Vector.prototype.width = 1 << Vector.prototype.bits, Vector.prototype.mask = Vector.prototype.width - 1;
var EmptyVector = new Vector(Array(Vector.prototype.width), 0, 1);
Vector.prototype.get = function(t) {
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    for (var r = this.root, e = this.bits, n = this.mask, o = this.shift; o > 0; o -= e) r = r[t >> o & n];
    return r[t & n]
}, Vector.prototype.append = function(t) {
    function r(i, u, p) {
        if (u > 0) {
            var h = p >> u & n;
            if (i) var s = i.slice();
            else var s = Array(o);
            return s[h] = r(s[h], u - e, p), s
        }
        var h = p & n;
        if (null == i) var s = Array(o);
        else var s = i.slice();
        return s[h] = t, s
    }
    var e = this.bits,
        n = this.mask,
        o = Vector.prototype.width;
    if (Math.pow(o, this.depth) === this.length) {
        var i = Array(o);
        i[0] = this.root, i[1] = Array(o);
        var u = r(i, this.depth * this.bits, this.length);
        return new Vector(u, this.length + 1, this.depth + 1)
    }
    var u = r(this.root, this.shift, this.length);
    return new Vector(u, this.length + 1, this.depth)
}, Vector.prototype.set = function(t, r) {
    function e(t, u, p) {
        if (u > 0) {
            var h = p >> u & o;
            if (t) var s = t.slice();
            else var s = Array(i);
            return s[h] = e(s[h], u - n, p), s
        }
        var h = p & o,
            s = t.slice();
        return s[h] = r, s
    }
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    var n = this.bits,
        o = this.mask,
        i = Vector.prototype.width,
        u = e(this.root, this.shift, t);
    return new Vector(u, this.length, this.depth)
}, Vector.prototype.insert = function(t, r) {
    function e(t, r, p, h) {
        if (r > 0) {
            var s = p >> r & i;
            if (t) var a = t.slice();
            else var a = Array(u);
            var c = e(a[s], r - o, p, h);
            a[s] = c[0];
            var f = null;
            if (c[1]) {
                f = c[1];
                for (var l = s + 1; u > l; l++) {
                    var c = e(a[l], r - o, l << r, f);
                    a[l] = c[0], f = c[1]
                }
            }
            return [a, f]
        }
        var s = p & i;
        return n(t, s, h)
    }

    function n(t, r, e) {
        for (var n = [], o = 0; u - 1 > o; o++) r === o && n.push(e), n.push(t[o]);
        return r === o && n.push(e), [n, t[u - 1]]
    }
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    var o = this.bits,
        i = this.mask,
        u = Vector.prototype.width,
        p = e(this.root, this.shift, t, r);
    return p[1] ? new Vector(p[0], this.length + 1, this.depth).append(p[1]) : new Vector(p[0], this.length + 1, this.depth)
}, Vector.prototype.toArray = function() {
    for (var t = Array(this.length), r = 0; r < this.length; r++) t[r] = this.get(r);
    return t
}, Vector.prototype.toString = function() {
    return "Vector(" + this.toArray().join(",") + ")"
}, Vector.prototype.operator_eq = function(t) {
    if (this.length !== t.length) return !1;
    if (this === t) return !0;
    for (var r = 0; r < this.length; r++)
        if (!this.get(r).operator_eq(t.get(r))) return !1;
    return !0
}, Vector.prototype.map = function(t) {
    for (var r = EmptyVector, e = this.length, n = 0; e > n; n++) r = r.append(t(this.get(n)));
    return r
}, Vector.prototype.filter = function(t) {
    for (var r = EmptyVector, e = this.length, n = 0; e > n; n++) {
        var o = this.get(n);
        t(o) && (r = r.append(o))
    }
    return r
}, Vector.prototype.reduce = function(t) {
    if (1 == this.length) return this.get(0);
    if (0 === this.length) throw Error("Cannot reduce empty vector");
    for (var r = this.length, e = this.get(0), n = 1; r > n; n++) e = t(e, this.get(n));
    return e
};