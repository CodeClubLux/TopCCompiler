function toString(s) {
    return s.toString()
}

function string_toString(s) {return s}
function int_toString(s) { return s.toString() }
function float_toString(s) { return s.toString() }
function array_toString(s) { return s.toString() }

function float_toInt(s) { return s | 0 }
function int_toInt(s) { return s }

function float_toFloat(s) { return s }
function int_toFloat(s) { return s }

function log(s) { console.log(s.toString()); }

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

        return fromJS(func.apply(null, args))
    }
}

function unary_read() {
    return this.arg;
}

function operator_set(val) {
    this.arg = val;
    for (var i = 0; i < this.events.length; i++ ) {
        this.events[i](val);
    }
}

function atom_watch(func) {
    this.events.push(func)
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