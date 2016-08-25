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
    if (key >= this.length && key < 0) {
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
    if (key >= this.length && key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

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
    if (key >= this.length && key < 0) {
        throw new Error("out of bounds: "+key.toString())
    }

    var bits = this.bits;
    var mask = this.mask;

    var self = this;

    function insert(node, level, key, value) {
        if (level > 0) {
            var pos = key >> level & mask;

            if (!node) {
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
    return "Vector("+this.toArray().join(",")+")"
}

Vector.prototype.operator_eq = function (other) {
    if (this.length !== other.length) return false;
    if (this === other) return true;

    for (var i = 0; i < this.length; i++) {
        if (!this.get(i).operator_eq(other.get(i))) {
            return false;
        }
    }
    return true;
}

Vector.prototype.map = function (func) {
    var newArr = EmptyVector;
    var len = this.length;
    for (var i = 0; i < len; i++) {
        newArr = newArr.append(func(this.get(i)));
    }
    return newArr;
}

Vector.prototype.filter = function (func) {
    var newArr = EmptyVector;
    var len = this.length;
    for (var i = 0; i < len; i++) {
        var el = this.get(i)
        if (func(el)) {
            newArr = newArr.append(el);
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

function newVector() {
    return fromArray(Array.prototype.slice.call(arguments))
}

function fromArray(arr) {
    var v = EmptyVector;
    for (var i = 0; i < arr.length; i++) {
        v = v.append(arr[i]);
    }
    return v;
}

function newVectorRange(start, end) {
    var arr = EmptyVector;
    for (var i = start; i < end; i++) {
        arr = arr.append(i)
    }
    return arr;
}

function newVectorInit(repeat, elem) {
    var arr = EmptyVector;
    for (var i = 0; i < repeat; i++) {
        arr = arr.append(i);
    }
    return arr;
}