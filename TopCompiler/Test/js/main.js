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