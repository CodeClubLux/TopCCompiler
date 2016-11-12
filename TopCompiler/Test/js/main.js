window.virtualDom = require("virtual-dom");

window.clearElement = function(elem) {
    elem.innerHTML = ""
}

window.html_h = function (type, attrib, children) {
    var at = {}
    for (var i = 0; i < attrib.length; i++) {
        at[attrib[i].name] = attrib[i].value;
    }
    return virtualDom.h(type, at, children);
}

window.core_watcher = function (a, b) {
    a.watch(b);
}

function Thunk(fn, arg, key) {
    this.fn = fn
    this.arg = arg
    this.key = key
}

Thunk.prototype.type = 'Thunk';
Thunk.prototype.render = render;

function render(previous) {
    if (!previous || previous.arg !== this.arg || previous.key !== this.key) {
        if (previous) {
            console.log("---------")
            console.log(previous.key);
            console.log(this.key);
            console.log("=========")
            console.log(previous.arg);
            console.log(this.arg);
        }
        return this.fn(this.arg, this.key);
    } else {
        return previous.vnode;
    }
}

window.newThunk = function (fn, arg, key) {
    return new Thunk(fn, arg, key)
}