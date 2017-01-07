window.virtualDom = require("virtual-dom");
//require("./three_wrapper");

window.clearElement = function(elem) {
    elem.innerHTML = ""
}

window.html_hyper = function (type, attrib, children) {
    var at = {}
    for (var i = 0; i < attrib.length; i++) {
        if (typeof attrib[i].value === "function") {
            at[attrib[i].name] = toSync(attrib[i].value);
            //toSync(attrib[i].value);
        } else {
            at[attrib[i].name] = attrib[i].value;
        }
    }

    var res = virtualDom.h(type, at, children);
    return res;
}

var _svg_h = require('virtual-hyperscript-svg');

window.svg_h = function (type, attrib, children) {
    var at = {}
    for (var i = 0; i < attrib.length; i++) {
        if (typeof attrib[i].value === "function") {
            at[attrib[i].name] = toSync(attrib[i].value);
            //toSync(attrib[i].value);
        } else {
            at[attrib[i].name] = attrib[i].value;
        }
    }

    var res = _svg_h(type, at, children);
    return res;
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

window.http_get = function (theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}

window.json_prettify = function (obj, indent) {
    console.log(obj);
    return JSON.stringify(JSON.parse(obj), null, indent);
}

window.html_appendChild = function (a,b) {
    a.appendChild(b);
}

window.core_fps = function core_fps(update, maxFPS) {
    var timestep = 1000 / maxFPS;
    var delta = 0;
    var lastFrameTimeMs = 0;

    function _fps(timestamp) {
        if (timestamp < lastFrameTimeMs + (1000 / maxFPS)) {
            requestAnimationFrame(_fps);
            return
        }



        // Track the accumulated time that hasn't been simulated yet
        delta += timestamp - lastFrameTimeMs; // note += here
        lastFrameTimeMs = timestamp;


        // Simulate the total elapsed time in fixed-size chunks
        function func() {
            if (delta >= timestep) {
                update(timestep, func);
                delta -= timestep;
            } else {
                requestAnimationFrame(_fps);
            }
        }

        func()
    }
    requestAnimationFrame(_fps);
}

function isElementInViewport (el) {

    //special bonus for those using jQuery
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }

    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /*or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /*or $(window).width() */
    );
}

function isElementInViewport (el) {
    var rect = el.getBoundingClientRect();

    return (
        rect.bottom - 100 < (window.innerHeight || document.documentElement.clientHeight)
    )

    /*or $(window).height() */
        //rect.right <= (window.innerWidth || document.documentElement.clientWidth) /*or $(window).width() */
    //);
}

function onVisibilityChange(el, callback) {
    var old_visible = false;
    return function () {
        if (!old_visible) {
            if (isElementInViewport(el)) {
                old_visible = true;
                callback();
            }
        }
    }
}

var handlers = [];

var handler = function () {
    var l = handlers.length;
    for (var i = 0; i < l; i++) {
        console.log(i);
        handlers[i]();
    }
}

window.html_handle = handler;

window.html_addClassOnVisible = function html_addClassOnVisible(el, className, next) {
    handlers.push(onVisibilityChange(el, function() {
        el.className += " "+className;
    }))
    next();
};

if (window.addEventListener) {
    addEventListener('DOMContentLoaded', handler, false);
    addEventListener('load', handler, false);
    addEventListener('scroll', handler, false);
    addEventListener('resize', handler, false);
} else if (window.attachEvent)  {
    attachEvent('onDOMContentLoaded', handler); // IE9+ :(
    attachEvent('onload', handler);
    attachEvent('onscroll', handler);
    attachEvent('onresize', handler);
}



