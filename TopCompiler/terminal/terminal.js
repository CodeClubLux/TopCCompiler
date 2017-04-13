/**@license
 *       __ _____                     ________                              __
 *      / // _  /__ __ _____ ___ __ _/__  ___/__ ___ ______ __ __  __ ___  / /
 *  __ / // // // // // _  // _// // / / // _  // _//     // //  \/ // _ \/ /
 * /  / // // // // // ___// / / // / / // ___// / / / / // // /\  // // / /__
 * \___//____ \\___//____//_/ _\_  / /_//____//_/ /_/ /_//_//_/ /_/ \__\_\___/
 *           \/              /____/                              version 1.0.12
 *
 * This file is part of jQuery Terminal. http://terminal.jcubic.pl
 *
 * Copyright (c) 2010-2017 Jakub Jankiewicz <http://jcubic.pl>
 * Released under the MIT license
 *
 * Contains:
 *
 * Storage plugin Distributed under the MIT License
 * Copyright (c) 2010 Dave Schindler
 *
 * jQuery Timers licenced with the WTFPL
 * <http://jquery.offput.ca/timers/>
 *
 * Cross-Browser Split 1.1.1
 * Copyright 2007-2012 Steven Levithan <stevenlevithan.com>
 * Available under the MIT License
 *
 * jQuery Caret
 * Copyright (c) 2009, Gideon Sireling
 * 3 clause BSD License
 *
 * sprintf.js
 * Copyright (c) 2007-2013 Alexandru Marasteanu <hello at alexei dot ro>
 * licensed under 3 clause BSD license
 *
 * Date: Sat, 11 Mar 2017 20:41:54 +0000
 */
(function(e) {
    var n = function() {
        if (!n.cache.hasOwnProperty(arguments[0])) {
            n.cache[arguments[0]] = n.parse(arguments[0])
        }
        return n.format.call(null, n.cache[arguments[0]], arguments)
    };
    n.format = function(e, r) {
        var o = 1,
            a = e.length,
            s = "",
            l, f = [],
            c, u, p, m, h, g;
        for (c = 0; c < a; c++) {
            s = t(e[c]);
            if (s === "string") {
                f.push(e[c])
            } else if (s === "array") {
                p = e[c];
                if (p[2]) {
                    l = r[o];
                    for (u = 0; u < p[2].length; u++) {
                        if (!l.hasOwnProperty(p[2][u])) {
                            throw n('[sprintf] property "%s" does not exist', p[2][u])
                        }
                        l = l[p[2][u]]
                    }
                } else if (p[1]) {
                    l = r[p[1]]
                } else {
                    l = r[o++]
                }
                if (/[^s]/.test(p[8]) && t(l) !== "number") {
                    throw n("[sprintf] expecting number but found %s", t(l))
                }
                switch (p[8]) {
                    case "b":
                        l = l.toString(2);
                        break;
                    case "c":
                        l = String.fromCharCode(l);
                        break;
                    case "d":
                        l = parseInt(l, 10);
                        break;
                    case "e":
                        l = p[7] ? l.toExponential(p[7]) : l.toExponential();
                        break;
                    case "f":
                        l = p[7] ? parseFloat(l).toFixed(p[7]) : parseFloat(l);
                        break;
                    case "o":
                        l = l.toString(8);
                        break;
                    case "s":
                        l = (l = String(l)) && p[7] ? l.substring(0, p[7]) : l;
                        break;
                    case "u":
                        l = l >>> 0;
                        break;
                    case "x":
                        l = l.toString(16);
                        break;
                    case "X":
                        l = l.toString(16).toUpperCase();
                        break
                }
                l = /[def]/.test(p[8]) && p[3] && l >= 0 ? " +" + l : l;
                h = p[4] ? p[4] === "0" ? "0" : p[4].charAt(1) : " ";
                g = p[6] - String(l).length;
                m = p[6] ? i(h, g) : "";
                f.push(p[5] ? l + m : m + l)
            }
        }
        return f.join("")
    };
    n.cache = {};
    n.parse = function(e) {
        var n = e,
            r = [],
            t = [],
            i = 0;
        while (n) {
            if ((r = /^[^\x25]+/.exec(n)) !== null) {
                t.push(r[0])
            } else if ((r = /^\x25{2}/.exec(n)) !== null) {
                t.push("%")
            } else if ((r = /^\x25(?:([1-9]\d*)\$|\(([^\)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-fosuxX])/.exec(n)) !== null) {
                if (r[2]) {
                    i |= 1;
                    var o = [],
                        a = r[2],
                        s = [];
                    if ((s = /^([a-z_][a-z_\d]*)/i.exec(a)) !== null) {
                        o.push(s[1]);
                        while ((a = a.substring(s[0].length)) !== "") {
                            if ((s = /^\.([a-z_][a-z_\d]*)/i.exec(a)) !== null) {
                                o.push(s[1])
                            } else if ((s = /^\[(\d+)\]/.exec(a)) !== null) {
                                o.push(s[1])
                            } else {
                                throw "[sprintf] huh?"
                            }
                        }
                    } else {
                        throw "[sprintf] huh?"
                    }
                    r[2] = o
                } else {
                    i |= 2
                }
                if (i === 3) {
                    throw "[sprintf] mixing positional and named placeholders is not (yet) supported"
                }
                t.push(r)
            } else {
                throw "[sprintf] huh?"
            }
            n = n.substring(r[0].length)
        }
        return t
    };
    var r = function(e, r, t) {
        t = r.slice(0);
        t.splice(0, 0, e);
        return n.apply(null, t)
    };

    function t(e) {
        return Object.prototype.toString.call(e).slice(8, -1).toLowerCase()
    }

    function i(e, n) {
        for (var r = []; n > 0; r[--n] = e) {}
        return r.join("")
    }
    e.sprintf = n;
    e.vsprintf = r
})(typeof global !== "undefined" ? global : window);
(function(e, n) {
    "use strict";
    e.omap = function(n, r) {
        var t = {};
        e.each(n, function(e, i) {
            t[e] = r.call(n, e, i)
        });
        return t
    };
    var r = {
        clone_object: function(n) {
            var r = {};
            if (typeof n === "object") {
                if (e.isArray(n)) {
                    return this.clone_array(n)
                } else if (n === null) {
                    return n
                } else {
                    for (var t in n) {
                        if (e.isArray(n[t])) {
                            r[t] = this.clone_array(n[t])
                        } else if (typeof n[t] === "object") {
                            r[t] = this.clone_object(n[t])
                        } else {
                            r[t] = n[t]
                        }
                    }
                }
            }
            return r
        },
        clone_array: function(n) {
            if (!e.isFunction(Array.prototype.map)) {
                throw new Error("Your browser don't support ES5 array map " + "use es5-shim")
            }
            return n.slice(0).map(function(e) {
                if (typeof e === "object") {
                    return this.clone_object(e)
                } else {
                    return e
                }
            }.bind(this))
        }
    };
    var t = function(e) {
        return r.clone_object(e)
    };
    var i = function() {
        var e = "test",
            n = window.localStorage;
        try {
            n.setItem(e, "1");
            n.removeItem(e);
            return true
        } catch (r) {
            return false
        }
    };
    var o = i();

    function a(e, n) {
        var r;
        if (typeof e === "string" && typeof n === "string") {
            localStorage[e] = n;
            return true
        } else if (typeof e === "object" && typeof n === "undefined") {
            for (r in e) {
                if (e.hasOwnProperty(r)) {
                    localStorage[r] = e[r]
                }
            }
            return true
        }
        return false
    }

    function s(e, n) {
        var r, t, i;
        r = new Date;
        r.setTime(r.getTime() + 31536e6);
        t = "; expires=" + r.toGMTString();
        if (typeof e === "string" && typeof n === "string") {
            document.cookie = e + "=" + n + t + "; path=/";
            return true
        } else if (typeof e === "object" && typeof n === "undefined") {
            for (i in e) {
                if (e.hasOwnProperty(i)) {
                    document.cookie = i + "=" + e[i] + t + "; path=/"
                }
            }
            return true
        }
        return false
    }

    function l(e) {
        return localStorage[e]
    }

    function f(e) {
        var n, r, t, i;
        n = e + "=";
        r = document.cookie.split(";");
        for (t = 0; t < r.length; t++) {
            i = r[t];
            while (i.charAt(0) === " ") {
                i = i.substring(1, i.length)
            }
            if (i.indexOf(n) === 0) {
                return i.substring(n.length, i.length)
            }
        }
        return null
    }

    function c(e) {
        return delete localStorage[e]
    }

    function u(e) {
        return s(e, "", -1)
    }
    e.extend({
        Storage: {
            set: o ? a : s,
            get: o ? l : f,
            remove: o ? c : u
        }
    });
    var p = e;
    p.fn.extend({
        everyTime: function(e, n, r, t, i) {
            return this.each(function() {
                p.timer.add(this, e, n, r, t, i)
            })
        },
        oneTime: function(e, n, r) {
            return this.each(function() {
                p.timer.add(this, e, n, r, 1)
            })
        },
        stopTime: function(e, n) {
            return this.each(function() {
                p.timer.remove(this, e, n)
            })
        }
    });
    p.extend({
        timer: {
            guid: 1,
            global: {},
            regex: /^([0-9]+)\s*(.*s)?$/,
            powers: {
                ms: 1,
                cs: 10,
                ds: 100,
                s: 1e3,
                das: 1e4,
                hs: 1e5,
                ks: 1e6
            },
            timeParse: function(e) {
                if (e === n || e === null) {
                    return null
                }
                var r = this.regex.exec(p.trim(e.toString()));
                if (r[2]) {
                    var t = parseInt(r[1], 10);
                    var i = this.powers[r[2]] || 1;
                    return t * i
                } else {
                    return e
                }
            },
            add: function(e, n, r, t, i, o) {
                var a = 0;
                if (p.isFunction(r)) {
                    if (!i) {
                        i = t
                    }
                    t = r;
                    r = n
                }
                n = p.timer.timeParse(n);
                if (typeof n !== "number" || isNaN(n) || n <= 0) {
                    return
                }
                if (i && i.constructor !== Number) {
                    o = !!i;
                    i = 0
                }
                i = i || 0;
                o = o || false;
                if (!e.$timers) {
                    e.$timers = {}
                }
                if (!e.$timers[r]) {
                    e.$timers[r] = {}
                }
                t.$timerID = t.$timerID || this.guid++;
                var s = function() {
                    if (o && s.inProgress) {
                        return
                    }
                    s.inProgress = true;
                    if (++a > i && i !== 0 || t.call(e, a) === false) {
                        p.timer.remove(e, r, t)
                    }
                    s.inProgress = false
                };
                s.$timerID = t.$timerID;
                if (!e.$timers[r][t.$timerID]) {
                    e.$timers[r][t.$timerID] = window.setInterval(s, n)
                }
                if (!this.global[r]) {
                    this.global[r] = []
                }
                this.global[r].push(e)
            },
            remove: function(e, n, r) {
                var t = e.$timers,
                    i;
                if (t) {
                    if (!n) {
                        for (var o in t) {
                            if (t.hasOwnProperty(o)) {
                                this.remove(e, o, r)
                            }
                        }
                    } else if (t[n]) {
                        if (r) {
                            if (r.$timerID) {
                                window.clearInterval(t[n][r.$timerID]);
                                delete t[n][r.$timerID]
                            }
                        } else {
                            for (var a in t[n]) {
                                if (t[n].hasOwnProperty(a)) {
                                    window.clearInterval(t[n][a]);
                                    delete t[n][a]
                                }
                            }
                        }
                        for (i in t[n]) {
                            if (t[n].hasOwnProperty(i)) {
                                break
                            }
                        }
                        if (!i) {
                            i = null;
                            delete t[n]
                        }
                    }
                    for (i in t) {
                        if (t.hasOwnProperty(i)) {
                            break
                        }
                    }
                    if (!i) {
                        e.$timers = null
                    }
                }
            }
        }
    });
    if (/(msie) ([\w.]+)/.exec(navigator.userAgent.toLowerCase())) {
        p(window).one("unload", function() {
            var e = p.timer.global;
            for (var n in e) {
                if (e.hasOwnProperty(n)) {
                    var r = e[n],
                        t = r.length;
                    while (--t) {
                        p.timer.remove(r[t], n)
                    }
                }
            }
        })
    }(function(e) {
        if (!String.prototype.split.toString().match(/\[native/)) {
            return
        }
        var n = String.prototype.split,
            r = /()??/.exec("")[1] === e,
            t;
        t = function(t, i, o) {
            if (Object.prototype.toString.call(i) !== "[object RegExp]") {
                return n.call(t, i, o)
            }
            var a = [],
                s = (i.ignoreCase ? "i" : "") + (i.multiline ? "m" : "") + (i.extended ? "x" : "") + (i.sticky ? "y" : ""),
                l = 0,
                f, c, u, p;
            i = new RegExp(i.source, s + "g");
            t += "";
            if (!r) {
                f = new RegExp("^" + i.source + "$(?!\\s)", s)
            }
            o = o === e ? -1 >>> 0 : o >>> 0;
            while (c = i.exec(t)) {
                u = c.index + c[0].length;
                if (u > l) {
                    a.push(t.slice(l, c.index));
                    if (!r && c.length > 1) {
                        c[0].replace(f, function() {
                            for (var n = 1; n < arguments.length - 2; n++) {
                                if (arguments[n] === e) {
                                    c[n] = e
                                }
                            }
                        })
                    }
                    if (c.length > 1 && c.index < t.length) {
                        Array.prototype.push.apply(a, c.slice(1))
                    }
                    p = c[0].length;
                    l = u;
                    if (a.length >= o) {
                        break
                    }
                }
                if (i.lastIndex === c.index) {
                    i.lastIndex++
                }
            }
            if (l === t.length) {
                if (p || !i.test("")) {
                    a.push("")
                }
            } else {
                a.push(t.slice(l))
            }
            return a.length > o ? a.slice(0, o) : a
        };
        String.prototype.split = function(e, n) {
            return t(this, e, n)
        };
        return t
    })();
    e.fn.caret = function(e) {
        var n = this[0];
        var r = n.contentEditable === "true";
        if (arguments.length === 0) {
            if (window.getSelection) {
                if (r) {
                    n.focus();
                    var t = window.getSelection().getRangeAt(0),
                        i = t.cloneRange();
                    i.selectNodeContents(n);
                    i.setEnd(t.endContainer, t.endOffset);
                    return i.toString().length
                }
                return n.selectionStart
            }
            if (document.selection) {
                n.focus();
                if (r) {
                    var t = document.selection.createRange(),
                        i = document.body.createTextRange();
                    i.moveToElementText(n);
                    i.setEndPoint("EndToEnd", t);
                    return i.text.length
                }
                var e = 0,
                    o = n.createTextRange(),
                    i = document.selection.createRange().duplicate(),
                    a = i.getBookmark();
                o.moveToBookmark(a);
                while (o.moveStart("character", -1) !== 0) e++;
                return e
            }
            return 0
        }
        if (e === -1) e = this[r ? "text" : "val"]().length;
        if (window.getSelection) {
            if (r) {
                n.focus();
                window.getSelection().collapse(n.firstChild, e)
            } else n.setSelectionRange(e, e)
        } else if (document.body.createTextRange) {
            var o = document.body.createTextRange();
            o.moveToElementText(n);
            o.moveStart("character", e);
            o.collapse(true);
            o.select()
        }
        if (!r) n.focus();
        return e
    };

    function m(e, n) {
        var r = [];
        var t = e.length;
        if (t < n) {
            return [e]
        } else if (n < 0) {
            throw new Error("str_parts: length can't be negative")
        }
        for (var i = 0; i < t; i += n) {
            r.push(e.substring(i, i + n))
        }
        return r
    }

    function h(n) {
        var r = n ? [n] : [];
        var t = 0;
        e.extend(this, {
            get: function() {
                return r
            },
            rotate: function() {
                if (!r.filter(Boolean).length) {
                    return
                }
                if (r.length === 1) {
                    return r[0]
                } else {
                    if (t === r.length - 1) {
                        t = 0
                    } else {
                        ++t
                    }
                    if (r[t]) {
                        return r[t]
                    } else {
                        return this.rotate()
                    }
                }
            },
            length: function() {
                return r.length
            },
            remove: function(e) {
                delete r[e]
            },
            set: function(e) {
                for (var n = r.length; n--;) {
                    if (r[n] === e) {
                        t = n;
                        return
                    }
                }
                this.append(e)
            },
            front: function() {
                if (r.length) {
                    var e = t;
                    var n = false;
                    while (!r[e]) {
                        e++;
                        if (e > r.length) {
                            if (n) {
                                break
                            }
                            e = 0;
                            n = true
                        }
                    }
                    return r[e]
                }
            },
            append: function(e) {
                r.push(e)
            }
        })
    }

    function g(n) {
        var r = n instanceof Array ? n : n ? [n] : [];
        e.extend(this, {
            data: function() {
                return r
            },
            map: function(n) {
                return e.map(r, n)
            },
            size: function() {
                return r.length
            },
            pop: function() {
                if (r.length === 0) {
                    return null
                } else {
                    var e = r[r.length - 1];
                    r = r.slice(0, r.length - 1);
                    return e
                }
            },
            push: function(e) {
                r = r.concat([e]);
                return e
            },
            top: function() {
                return r.length > 0 ? r[r.length - 1] : null
            },
            clone: function() {
                return new g(r.slice(0))
            }
        })
    }

    function d(n, r, t) {
        var i = true;
        var o = "";
        if (typeof n === "string" && n !== "") {
            o = n + "_"
        }
        o += "commands";
        var a;
        if (t) {
            a = []
        } else {
            a = e.Storage.get(o);
            a = a ? e.parseJSON(a) : []
        }
        var s = a.length - 1;
        e.extend(this, {
            append: function(n) {
                if (i) {
                    if (a[a.length - 1] !== n) {
                        a.push(n);
                        if (r && a.length > r) {
                            a = a.slice(-r)
                        }
                        s = a.length - 1;
                        if (!t) {
                            e.Storage.set(o, JSON.stringify(a))
                        }
                    }
                }
            },
            set: function(n) {
                if (n instanceof Array) {
                    a = n;
                    if (!t) {
                        e.Storage.set(o, JSON.stringify(a))
                    }
                }
            },
            data: function() {
                return a
            },
            reset: function() {
                s = a.length - 1
            },
            last: function() {
                return a[a.length - 1]
            },
            end: function() {
                return s === a.length - 1
            },
            position: function() {
                return s
            },
            current: function() {
                return a[s]
            },
            next: function() {
                if (s < a.length - 1) {
                    ++s
                }
                if (s !== -1) {
                    return a[s]
                }
            },
            previous: function() {
                var e = s;
                if (s > 0) {
                    --s
                }
                if (e !== -1) {
                    return a[s]
                }
            },
            clear: function() {
                a = [];
                this.purge()
            },
            enabled: function() {
                return i
            },
            enable: function() {
                i = true
            },
            purge: function() {
                if (!t) {
                    e.Storage.remove(o)
                }
            },
            disable: function() {
                i = false
            }
        })
    }
    var v = 0;
    e.fn.cmd = function(r) {
        var t = this;
        var i = t.data("cmd");
        if (i) {
            return i
        }
        var o = v++;
        t.addClass("cmd");
        t.append('<span class="prompt"></span><span></span>' + '<span class="cursor">&nbsp;</span><span></span>');
        var a = e("<textarea>").attr({
            autocapitalize: "off",
            spellcheck: "false"
        }).addClass("clipboard").appendTo(t);
        if (r.width) {
            t.width(r.width)
        }
        var s;
        var l;
        var f = t.find(".prompt");
        var c = false;
        var u = "";
        var p = null;
        var h;
        var g = r.mask || false;
        var w = "";
        var b;
        var k = "";
        var x = 0;
        var T;
        var R;
        var C = r.historySize || 60;
        var E, S;
        var A = t.find(".cursor");
        var F;
        var L = 0;

        function O() {
            var n = e("<span>&nbsp;</span>").appendTo(t);
            var r = n[0].getBoundingClientRect();
            n.remove();
            return r
        }

        function P(e) {
            var n = t.find(".prompt").text().length;
            var r = O();
            var i = r.width;
            var o = r.height;
            var a = t.offset();
            var s = Math.floor((e.x - a.left) / i);
            var l = Math.floor((e.y - a.top) / o);
            var f = ne(w);
            var c;
            if (l > 0 && f.length > 1) {
                c = s + f.slice(0, l).reduce(function(e, n) {
                    return e + n.length
                }, 0)
            } else {
                c = s - n
            }
            var u = w.replace(/\t/g, "\x00\x00\x00\x00");
            var p = u.slice(0, c);
            var m = p.replace(/\x00{4}/g, "	").replace(/\x00+/, "").length;
            return m > w.length ? w.length : m
        }

        function j(e) {
            if (!("KeyboardEvent" in window && "key" in window.KeyboardEvent.prototype)) {
                throw new Error("key event property not supported try " + "https://github.com/cvan/keyboardevent-key-polyfill")
            }
            if (e.key) {
                var n = e.key.toUpperCase();
                if (n === "CONTROL") {
                    return "CTRL"
                } else {
                    var r = [];
                    if (e.ctrlKey) {
                        r.push("CTRL")
                    }
                    if (e.metaKey && n !== "META") {
                        r.push("META")
                    }
                    if (e.shiftKey && n !== "SHIFT") {
                        r.push("SHIFT")
                    }
                    if (e.altKey && n !== "ALT") {
                        r.push("ALT")
                    }
                    if (e.key) {
                        r.push(n)
                    }
                    return r.join("+")
                }
            }
        }
        var I;
        var N = {
            "ALT+D": function() {
                t.set(w.slice(0, x) + w.slice(x).replace(/ *[^ ]+ *(?= )|[^ ]+$/, ""), true);
                return false
            },
            ENTER: function() {
                if (S && w && !g && (e.isFunction(r.historyFilter) && r.historyFilter(w)) || r.historyFilter instanceof RegExp && w.match(r.historyFilter) || !r.historyFilter) {
                    S.append(w)
                }
                var n = w;
                S.reset();
                t.set("");
                if (r.commands) {
                    r.commands(n)
                }
                if (e.isFunction(T)) {
                    ie()
                }
                e(".clipboard").val("");
                return true
            },
            "SHIFT+ENTER": function() {
                t.insert("\n");
                return false
            },
            BACKSPACE: function() {
                if (c) {
                    u = u.slice(0, -1);
                    V()
                } else if (w !== "" && x > 0) {
                    t["delete"](-1)
                }
                return false
            },
            TAB: function() {
                t.insert("	")
            },
            "CTRL+D": function() {
                t["delete"](1);
                return false
            },
            DELETE: function() {
                t["delete"](1);
                return true
            },
            ARROWUP: D,
            UP: D,
            "CTRL+P": D,
            ARROWDOWN: B,
            DOWN: B,
            "CTRL+N": B,
            ARROWLEFT: W,
            LEFT: W,
            "CTRL+B": W,
            "CTRL+ARROWLEFT": function() {
                var e = x - 1;
                var n = 0;
                if (w[e] === " ") {
                    --e
                }
                for (var r = e; r > 0; --r) {
                    if (w[r] === " " && w[r + 1] !== " ") {
                        n = r + 1;
                        break
                    } else if (w[r] === "\n" && w[r + 1] !== "\n") {
                        n = r;
                        break
                    }
                }
                t.position(n)
            },
            "CTRL+R": function() {
                if (c) {
                    Z(true)
                } else {
                    h = T;
                    V();
                    b = w;
                    t.set("");
                    te();
                    c = true
                }
                return false
            },
            "CTRL+G": function() {
                if (c) {
                    T = h;
                    ie();
                    t.set(b);
                    te();
                    c = false;
                    u = "";
                    return false
                }
            },
            ARROWRIGHT: M,
            "CTRL+F": M,
            RIGHT: M,
            "CTRL+ARROWRIGHT": function() {
                if (w[x] === " ") {
                    ++x
                }
                var e = /\S[\n\s]{2,}|[\n\s]+\S?/;
                var n = w.slice(x).match(e);
                if (!n || n[0].match(/^\s+$/)) {
                    t.position(w.length)
                } else if (n[0][0] !== " ") {
                    x += n.index + 1
                } else {
                    x += n.index + n[0].length - 1;
                    if (n[0][n[0].length - 1] !== " ") {
                        --x
                    }
                }
                te()
            },
            F12: $,
            END: q,
            "CTRL+E": q,
            HOME: U,
            "CTRL+A": U,
            "SHIFT+INSERT": H,
            "CTRL+SHIFT+T": $,
            "CTRL+W": function() {
                if (w !== "" && x !== 0) {
                    var e = w.slice(0, x).match(/([^ ]+ *$)/);
                    k = t["delete"](-e[0].length);
                    K(t, k)
                }
                return false
            },
            "CTRL+H": function() {
                if (w !== "" && x > 0) {
                    t["delete"](-1)
                }
                return false
            },
            "CTRL+X": $,
            "CTRL+C": $,
            "CTRL+T": $,
            "CTRL+Y": function() {
                if (k !== "") {
                    t.insert(k)
                }
            },
            "CTRL+V": H,
            "META+V": H,
            "CTRL+K": function() {
                k = t["delete"](w.length - x);
                K(t, k);
                return false
            },
            "CTRL+U": function() {
                if (w !== "" && x !== 0) {
                    k = t["delete"](-x);
                    K(t, k)
                }
                return false
            },
            "CTRL+TAB": function() {
                return false
            },
            "META+`": $,
            "META+R": $,
            "META+L": $
        };

        function $() {
            return true
        }

        function H() {
            a.val("");
            L = 0;
            a.focus();
            a.on("input", function e(n) {
                oe(n);
                a.off("input", e)
            });
            return true
        }

        function D() {
            if (se) {
                b = w;
                t.set(S.current())
            } else {
                t.set(S.previous())
            }
            se = false;
            return false
        }

        function B() {
            t.set(S.end() ? b : S.next());
            return false
        }

        function W() {
            if (x > 0) {
                t.position(-1, true);
                te()
            }
        }

        function M() {
            if (x < w.length) {
                t.position(1, true)
            }
            return false
        }

        function U() {
            t.position(0)
        }

        function q() {
            t.position(w.length)
        }

        function J() {
            var e = a.is(":focus");
            if (R) {
                if (!e) {
                    a.focus();
                    t.oneTime(10, function() {
                        a.focus()
                    })
                }
            } else if (e) {
                a.blur()
            }
        }

        function G() {
            t.oneTime(10, function() {
                a.val(w);
                if (R) {
                    t.oneTime(10, function() {
                        try {
                            a.caret(x)
                        } catch (e) {}
                    })
                }
            })
        }
        if (y && !_) {
            F = function(e) {
                if (e) {
                    A.addClass("blink")
                } else {
                    A.removeClass("blink")
                }
            }
        } else {
            var Y = false;
            F = function(e) {
                if (e && !Y) {
                    Y = true;
                    A.addClass("inverted blink");
                    t.everyTime(500, "blink", X)
                } else if (Y && !e) {
                    Y = false;
                    t.stopTime("blink", X);
                    A.removeClass("inverted blink")
                }
            }
        }

        function X() {
            A.toggleClass("inverted")
        }

        function V() {
            T = "(reverse-i-search)`" + u + "': ";
            ie()
        }

        function Q() {
            T = h;
            c = false;
            p = null;
            u = ""
        }

        function Z(n) {
            var r = S.data();
            var i, o;
            var a = r.length;
            if (n && p > 0) {
                a -= p
            }
            if (u.length > 0) {
                for (var s = u.length; s > 0; s--) {
                    o = e.terminal.escape_regex(u.substring(0, s));
                    i = new RegExp(o);
                    for (var l = a; l--;) {
                        if (i.test(r[l])) {
                            p = r.length - l;
                            t.position(r[l].indexOf(o));
                            t.set(r[l], true);
                            te();
                            if (u.length !== s) {
                                u = u.substring(0, s);
                                V()
                            }
                            return
                        }
                    }
                }
            }
            u = ""
        }

        function ee() {
            var e = t.width();
            var n = A[0].getBoundingClientRect().width;
            s = Math.floor(e / n)
        }

        function ne(e) {
            var n;
            if (e.match(/\n/)) {
                var r = e.split("\n");
                var t = s - l - 1;
                for (var i = 0; i < r.length - 1; ++i) {
                    r[i] += " "
                }
                if (r[0].length > t) {
                    n = [r[0].substring(0, t)];
                    var o = r[0].substring(t);
                    n = n.concat(m(o, s))
                } else {
                    n = [r[0]]
                }
                for (i = 1; i < r.length; ++i) {
                    if (r[i].length > s) {
                        n = n.concat(m(r[i], s))
                    } else {
                        n.push(r[i])
                    }
                }
            } else {
                var a = e.substring(0, s - l);
                var f = e.substring(s - l);
                n = [a].concat(m(f, s))
            }
            return n
        }

        function re(n) {
            var r = e.terminal.defaults.formatters;
            for (var t = 0; t < r.length; ++t) {
                try {
                    if (typeof r[t] === "function") {
                        var i = r[t](n);
                        if (typeof i === "string") {
                            n = i
                        }
                    }
                } catch (o) {
                    alert("formatting error at formatters[" + t + "]\n" + (o.stack ? o.stack : o))
                }
            }
            return e.terminal.format(e.terminal.encode(n))
        }
        var te = function() {
            var r = A.prev();
            var i = A.next();

            function o(e, n) {
                var t = e.length;
                if (n === t) {
                    r.html(re(e));
                    A.html("&nbsp;");
                    i.html("")
                } else if (n === 0) {
                    r.html("");
                    A.html(re(e.slice(0, 1)));
                    i.html(re(e.slice(1)))
                } else {
                    var o = e.slice(0, n);
                    r.html(re(o));
                    var a = e.slice(n, n + 1);
                    A.html(re(a));
                    if (n === e.length - 1) {
                        i.html("")
                    } else {
                        i.html(re(e.slice(n + 1)))
                    }
                }
            }

            function a(e) {
                return "<div>" + re(e) + "</div>"
            }

            function f(n) {
                var r = i;
                e.each(n, function(n, t) {
                    r = e(a(t)).insertAfter(r)
                })
            }

            function c(n) {
                e.each(n, function(e, n) {
                    r.before(a(n))
                })
            }
            return function() {
                var u;
                switch (typeof g) {
                    case "boolean":
                        u = g ? w.replace(/./g, "*") : w;
                        break;
                    case "string":
                        u = w.replace(/./g, g);
                        break
                }
                var p;
                t.find("div").remove();
                r.html("");
                if (u.length > s - l - 1 || u.match(/\n/)) {
                    var m = u.match(/\t/g);
                    var h = m ? m.length * 3 : 0;
                    if (m) {
                        u = u.replace(/\t/g, "\x00\x00\x00\x00")
                    }
                    var d = ne(u);
                    if (m) {
                        d = e.map(d, function(e) {
                            return e.replace(/\x00\x00\x00\x00/g, "	")
                        })
                    }
                    var v = d[0].length;
                    if (v === 0 && d.length === 1) {} else if (x < v) {
                        o(d[0], x);
                        f(d.slice(1))
                    } else if (x === v) {
                        r.before(a(d[0]));
                        o(d[1] || "", 0);
                        if (d.length > 1) {
                            f(d.slice(2))
                        }
                    } else {
                        var y = d.length;
                        if (x < v) {
                            o(d[0], x);
                            f(d.slice(1))
                        } else if (x === v) {
                            r.before(a(d[0]));
                            o(d[1], 0);
                            f(d.slice(2))
                        } else {
                            var _ = d.slice(-1)[0];
                            var b = u.length - x - h;
                            var k = _.length;
                            var T = 0;
                            if (b <= k) {
                                c(d.slice(0, -1));
                                if (k === b) {
                                    T = 0
                                } else {
                                    T = k - b
                                }
                                o(_, T)
                            } else if (y === 3) {
                                var R = re(d[0]);
                                r.before("<div>" + R + "</div>");
                                o(d[1], x - v - 1);
                                R = re(d[2]);
                                i.after("<div>" + R + "</div>")
                            } else {
                                var C;
                                var E;
                                T = x;
                                for (p = 0; p < d.length; ++p) {
                                    var S = d[p].length;
                                    if (T > S) {
                                        T -= S
                                    } else {
                                        break
                                    }
                                }
                                E = d[p];
                                C = p;
                                if (T === E.length) {
                                    T = 0;
                                    E = d[++C];
                                    if (E === n) {
                                        var F = e.terminal.defaults.strings.redrawError;
                                        throw new Error(F)
                                    }
                                }
                                o(E, T);
                                c(d.slice(0, C));
                                f(d.slice(C + 1))
                            }
                        }
                    }
                } else if (u === "") {
                    r.html("");
                    A.html("&nbsp;");
                    i.html("")
                } else {
                    o(u, x)
                }
            }
        }();
        var ie = function() {
            function n(n) {
                f.html(e.terminal.format(e.terminal.encode(n)));
                l = f.text().length
            }
            return function() {
                switch (typeof T) {
                    case "string":
                        n(T);
                        break;
                    case "function":
                        T(n);
                        break
                }
            }
        }();

        function oe() {
            if (L++ > 0) {
                return
            }
            if (t.isenabled()) {
                var e = t.find("textarea");
                if (!e.is(":focus")) {
                    e.focus()
                }
                t.oneTime(100, function() {
                    t.insert(e.val());
                    e.val("");
                    G()
                })
            }
        }

        function ae() {
            if (e.isFunction(r.onCommandChange)) {
                r.onCommandChange(w)
            }
        }
        e.extend(t, {
            name: function(e) {
                if (e !== n) {
                    E = e;
                    var i = S && S.enabled() || !S;
                    S = new d(e, C, r.history === "memory");
                    if (!i) {
                        S.disable()
                    }
                    return t
                } else {
                    return E
                }
            },
            purge: function() {
                S.clear();
                return t
            },
            history: function() {
                return S
            },
            "delete": function(e, n) {
                var r;
                if (e === 0) {
                    return t
                } else if (e < 0) {
                    if (x > 0) {
                        r = w.slice(0, x).slice(e);
                        w = w.slice(0, x + e) + w.slice(x, w.length);
                        if (!n) {
                            t.position(x + e)
                        }
                        ae()
                    }
                } else if (w !== "" && x < w.length) {
                    r = w.slice(x).slice(0, e);
                    w = w.slice(0, x) + w.slice(x + e, w.length);
                    ae()
                }
                te();
                G();
                return r
            },
            set: function(e, r) {
                if (e !== n) {
                    w = e;
                    if (!r) {
                        t.position(w.length)
                    }
                    te();
                    G();
                    ae()
                }
                return t
            },
            keymap: function(n) {
                if (typeof n === "undefined") {
                    return I
                } else {
                    I = e.extend({}, N, e.omap(n || {}, function(e, n) {
                        return function(r) {
                            return n(r, N[e])
                        }
                    }));
                    return t
                }
            },
            insert: function(e, n) {
                if (x === w.length) {
                    w += e
                } else if (x === 0) {
                    w = e + w
                } else {
                    w = w.slice(0, x) + e + w.slice(x)
                }
                if (!n) {
                    t.position(e.length, true)
                } else {
                    G()
                }
                te();
                ae();
                return t
            },
            get: function() {
                return w
            },
            commands: function(e) {
                if (e) {
                    r.commands = e;
                    return t
                } else {
                    return e
                }
            },
            destroy: function() {
                ve.unbind("keypress.cmd", ye);
                ve.unbind("keydown.cmd", de);
                ve.unbind("paste.cmd", oe);
                ve.unbind("input.cmd", _e);
                t.stopTime("blink", X);
                t.find(".cursor").next().remove().end().prev().remove().end().remove();
                t.find(".prompt, .clipboard").remove();
                t.removeClass("cmd").removeData("cmd").off(".cmd");
                return t
            },
            prompt: function(e) {
                if (e === n) {
                    return T
                } else {
                    if (typeof e === "string" || typeof e === "function") {
                        T = e
                    } else {
                        throw new Error("prompt must be a function or string")
                    }
                    ie();
                    te();
                    return t
                }
            },
            kill_text: function() {
                return k
            },
            position: function(n, i) {
                if (typeof n === "number") {
                    if (i) {
                        x += n
                    } else if (n < 0) {
                        x = 0
                    } else if (n > w.length) {
                        x = w.length
                    } else {
                        x = n
                    }
                    if (e.isFunction(r.onPositionChange)) {
                        r.onPositionChange(x)
                    }
                    te();
                    G();
                    return t
                } else {
                    return x
                }
            },
            visible: function() {
                var e = t.visible;
                return function() {
                    e.apply(t, []);
                    te();
                    ie()
                }
            }(),
            show: function() {
                var e = t.show;
                return function() {
                    e.apply(t, []);
                    te();
                    ie()
                }
            }(),
            resize: function(e) {
                if (e) {
                    s = e
                } else {
                    ee()
                }
                te();
                return t
            },
            enable: function() {
                R = true;
                t.addClass("enabled");
                try {
                    a.caret(x)
                } catch (e) {}
                F(true);
                J();
                return t
            },
            isenabled: function() {
                return R
            },
            disable: function() {
                R = false;
                t.removeClass("enabled");
                F(false);
                J();
                return t
            },
            mask: function(e) {
                if (typeof e === "undefined") {
                    return g
                } else {
                    g = e;
                    te();
                    return t
                }
            }
        });
        t.name(r.name || r.prompt || "");
        if (typeof r.prompt === "string") {
            T = r.prompt
        } else {
            T = "> "
        }
        ie();
        if (r.enabled === n || r.enabled === true) {
            t.enable()
        }
        var se = true;
        var le = false;
        var fe = false;
        var ce = false;
        var ue = false;
        var pe = false;
        var me = false;
        var he;
        var ge;

        function de(i) {
            var o;
            fe = ue && ce;
            ce = i.key && i.key.length === 1;
            pe = String(i.key).toLowerCase() === "unidentified";
            me = i.key.toUpperCase() === "BACKSPACE" || i.which === 8;
            ge = a.val();
            ue = true;
            if (R) {
                if (e.isFunction(r.keydown)) {
                    o = r.keydown(i);
                    if (o !== n) {
                        return o
                    }
                }
                var s = j(i);
                he = ["CTRL+V"].indexOf(s) !== -1;
                if (i.which !== 38 && !(i.which === 80 && i.ctrlKey)) {
                    se = true
                }
                if (c && (i.which === 35 || i.which === 36 || i.which === 37 || i.which === 38 || i.which === 39 || i.which === 40 || i.which === 13 || i.which === 27)) {
                    Q();
                    ie();
                    if (i.which === 27) {
                        t.set("")
                    }
                    te();
                    de.call(this, i)
                } else if (e.isFunction(I[s])) {
                    o = I[s]();
                    if (o === true) {
                        return
                    }
                    if (o !== n) {
                        return o
                    }
                } else if (i.altKey) {
                    return
                } else {
                    le = false;
                    return
                }
                i.preventDefault()
            }
        }
        var ve = e(document.documentElement || window);
        t.keymap(r.keymap);

        function ye(i) {
            var o;
            ue = false;
            if ((i.ctrlKey || i.metaKey) && [99, 118, 86].indexOf(i.which) !== -1) {
                return
            }
            if (le) {
                return
            }
            if (!c && e.isFunction(r.keypress)) {
                o = r.keypress(i)
            }
            var a;
            if (z()) {
                a = i.key
            }
            if (!a || pe) {
                a = String.fromCharCode(i.which)
            }
            if (a.toUpperCase() === "SPACEBAR") {
                a = " "
            }
            if (o === n || o) {
                if (R) {
                    if (e.inArray(i.which, [13, 0, 8]) > -1) {
                        if (i.keyCode === 123) {
                            return
                        }
                        return false
                    } else if (a && (!i.ctrlKey || i.ctrlKey && i.ctrlKey) && (!(i.altKey && i.which === 100) || i.altKey) && !fe) {
                        if (c) {
                            u += a;
                            Z();
                            V()
                        } else {
                            t.insert(a)
                        }
                        return false
                    }
                }
            } else {
                return o
            }
        }

        function _e() {
            if ((ue || fe) && !he && (ce || pe) && !me) {
                var e = x;
                var n = a.val();
                if (n !== "") {
                    if (c) {
                        u = n;
                        Z();
                        V()
                    } else {
                        t.set(n)
                    }
                    if (me || n.length < ge.length) {
                        t.position(e - 1)
                    } else {
                        t.position(e + Math.abs(n.length - ge.length))
                    }
                }
            }
        }
        ve.bind("keypress.cmd", ye).bind("keydown.cmd", de).bind("input.cmd", _e);
        (function() {
            var n = false;
            var i = false;
            var a = 0;
            t.on("mousedown.cmd", function() {
                i = true;
                t.oneTime(1, function() {
                    e(window).on("mousemove.cmd_" + o, function() {
                        n = true;
                        e(window).off("mousemove.cmd_" + o)
                    })
                })
            }).on("mouseup.cmd", function(s) {
                var l = n;
                n = false;
                e(window).off("mousemove.cmd_" + o);
                if (!l) {
                    var f = "click_" + o;
                    if (++a === 1) {
                        var c = i;
                        t.oneTime(r.clickTimeout, f, function() {
                            if (!e(s.target).is(".prompt") && c) {
                                t.position(P({
                                    x: s.pageX,
                                    y: s.pageY
                                }))
                            }
                            a = 0
                        })
                    } else {
                        t.stopTime(f);
                        a = 0
                    }
                }
                i = false
            })
        })();
        t.data("cmd", t);
        return t
    };
    var y = function() {
        var e = false,
            r = "Webkit Moz O ms Khtml".split(" "),
            t = document.createElement("div");
        if (t.style.animationName) {
            e = true
        }
        if (e === false) {
            for (var i = 0; i < r.length; i++) {
                var o = r[i] + "AnimationName";
                if (t.style[o] !== n) {
                    e = true;
                    break
                }
            }
        }
        return e
    }();
    var _ = navigator.userAgent.toLowerCase().indexOf("android") !== -1;
    var w = function() {
        return "ontouchstart" in window || !!window.DocumentTouch && document instanceof window.DocumentTouch
    }();

    function b(e, n) {
        var r = n(e);
        if (r.length) {
            var t = r.shift();
            var i = e.substring(t.length).trim();
            return {
                command: e,
                name: t,
                args: r,
                rest: i
            }
        } else {
            return {
                command: e,
                name: "",
                args: [],
                rest: ""
            }
        }
    }
    var k = /(\[\[[!gbiuso]*;[^;]*;[^\]]*\](?:[^\]]*\\\][^\]]*|[^\]]*|[^[]*\[[^\]]*)\]?)/i;
    var x = /\[\[([!gbiuso]*);([^;]*);([^;\]]*);?([^;\]]*);?([^\]]*)\]([^\]]*\\\][^\]]*|[^\]]*|[^[]*\[[^\]]*)\]?/gi;
    var T = /\[\[([!gbiuso]*;[^;\]]*;[^;\]]*(?:;|[^\]()]*);?[^\]]*)\]([^\]]*\\\][^\]]*|[^\]]*|[^[]*\[[^\]]*)\]?/gi;
    var R = /\[\[([!gbiuso]*;[^;\]]*;[^;\]]*(?:;|[^\]()]*);?[^\]]*)\]([^\]]*\\\][^\]]*|[^\]]*|[^[]*\[[^\]]*)\]/gi;
    var C = /^\[\[([!gbiuso]*;[^;\]]*;[^;\]]*(?:;|[^\]()]*);?[^\]]*)\]([^\]]*\\\][^\]]*|[^\]]*|[^[]*\[[^\]]*)\]$/gi;
    var E = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i;
    var S = /(\bhttps?:\/\/(?:(?:(?!&[^;]+;)|(?=&amp;))[^\s"'<>\][)])+\b)/gi;
    var A = /\b(https?:\/\/(?:(?:(?!&[^;]+;)|(?=&amp;))[^\s"'<>\][)])+)\b(?![^[\]]*])/gi;
    var F = /((([^<>('")[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,})))/g;
    var L = /('(?:[^']|\\')*'|"(\\"|[^"])*"|(?:\/(\\\/|[^\/])+\/[gimy]*)(?=:? |$)|(\\\s|\S)+|[\w-]+)/gi;
    var O = /(\[\[[!gbiuso]*;[^;]*;[^\]]*\])/i;
    var P = /^(\[\[[!gbiuso]*;[^;]*;[^\]]*\])/i;
    var j = /\[\[[!gbiuso]*;[^;]*;[^\]]*\]?$/i;
    var I = /(\[\[(?:[^\]]|\\\])*\]\])/;
    var N = /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/;
    var $ = /^\/((?:\\\/|[^\/]|\[[^\]]*\/[^\]]*\])+)\/([gimy]*)$/;
    e.terminal = {
        version: "1.0.12",
        color_names: ["transparent", "currentcolor", "black", "silver", "gray", "white", "maroon", "red", "purple", "fuchsia", "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua", "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey", "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"],
        valid_color: function(n) {
            if (n.match(E)) {
                return true
            } else {
                return e.inArray(n.toLowerCase(), e.terminal.color_names) !== -1
            }
        },
        escape_regex: function(e) {
            if (typeof e === "string") {
                var n = /([-\\^$[\]()+{}?*.|])/g;
                return e.replace(n, "\\$1")
            }
        },
        have_formatting: function(e) {
            return typeof e === "string" && !!e.match(R)
        },
        is_formatting: function(e) {
            return typeof e === "string" && !!e.match(C)
        },
        format_split: function(e) {
            return e.split(k)
        },
        split_equal: function(n, r, t) {
            var i = false;
            var o = false;
            var a = "";
            var s = [];
            var l = n.replace(T, function(e, n, r) {
                var t = n.match(/;/g).length;
                if (t >= 4) {
                    return e
                } else if (t === 2) {
                    t = ";;"
                } else if (t === 3) {
                    t = ";"
                } else {
                    t = ""
                }
                var i = r.replace(/\\\]/g, "&#93;").replace(/\n/g, "\\n").replace(/&nbsp;/g, " ");
                return "[[" + n + t + i + "]" + r + "]"
            }).split(/\n/g);

            function f() {
                return m.substring(y - 6, y) === "&nbsp;" || m.substring(y - 1, y) === " "
            }

            function c() {
                var e = d.match(T);
                if (e) {
                    var n = e[e.length - 1];
                    if (n[n.length - 1] !== "]") {
                        a = n.match(O)[1];
                        d += "]"
                    } else if (d.match(j)) {
                        d = d.replace(j, "");
                        a = n.match(O)[1]
                    }
                }
            }
            for (var u = 0, p = l.length; u < p; ++u) {
                if (l[u] === "") {
                    s.push("");
                    continue
                }
                var m = l[u];
                var h = 0;
                var g = 0;
                var d;
                var v = -1;
                for (var y = 0, _ = m.length; y < _; ++y) {
                    if (m.substring(y).match(P)) {
                        i = true;
                        o = false
                    } else if (i && m[y] === "]") {
                        if (o) {
                            i = false;
                            o = false
                        } else {
                            o = true
                        }
                    } else if (i && o || !i) {
                        if (m[y] === "&") {
                            var w = m.substring(y).match(/^(&[^;]+;)/);
                            if (!w) {
                                throw new Error("Unclosed html entity in line " + (u + 1) + " at char " + (y + 1))
                            }
                            y += w[1].length - 2;
                            if (y === _ - 1) {
                                s.push(d + w[1])
                            }
                            continue
                        } else if (m[y] === "]" && m[y - 1] === "\\") {
                            --g
                        } else {
                            ++g
                        }
                    }
                    if (f() && (i && o || !i || m[y] === "[" && m[y + 1] === "[")) {
                        v = y
                    }
                    if ((g === r || y === _ - 1) && (i && o || !i)) {
                        var b = e.terminal.strip(m.substring(v));
                        b = e("<span>" + b + "</span>").text();
                        var k = b.length;
                        b = b.substring(0, y + r + 1);
                        var x = !!b.match(/\s/) || y + r + 1 > k;
                        if (t && v !== -1 && y !== _ - 1 && x) {
                            d = m.substring(h, v);
                            y = v - 1
                        } else {
                            d = m.substring(h, y + 1)
                        }
                        if (t) {
                            d = d.replace(/(&nbsp;|\s)+$/g, "")
                        }
                        v = -1;
                        h = y + 1;
                        g = 0;
                        if (a) {
                            d = a + d;
                            if (d.match("]")) {
                                a = ""
                            }
                        }
                        c();
                        s.push(d)
                    }
                }
            }
            return s
        },
        encode: function(e) {
            e = e.replace(/&(?!#[0-9]+;|[a-zA-Z]+;)/g, "&amp;");
            return e.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "&nbsp;").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;")
        },
        escape_formatting: function(n) {
            return e.terminal.escape_brackets(e.terminal.encode(n))
        },
        format: function(n, r) {
            var t = e.extend({}, {
                linksNoReferrer: false
            }, r || {});
            if (typeof n === "string") {
                var i = e.terminal.format_split(n);
                n = e.map(i, function(n) {
                    if (n === "") {
                        return n
                    } else if (e.terminal.is_formatting(n)) {
                        n = n.replace(/\[\[[^\]]+\]/, function(e) {
                            return e.replace(/&nbsp;/g, " ")
                        });
                        return n.replace(x, function(n, r, i, o, a, s, l) {
                            if (l === "") {
                                return ""
                            }
                            l = l.replace(/\\]/g, "]");
                            var f = "";
                            if (r.indexOf("b") !== -1) {
                                f += "font-weight:bold;"
                            }
                            var c = [];
                            if (r.indexOf("u") !== -1) {
                                c.push("underline")
                            }
                            if (r.indexOf("s") !== -1) {
                                c.push("line-through")
                            }
                            if (r.indexOf("o") !== -1) {
                                c.push("overline")
                            }
                            if (c.length) {
                                f += "text-decoration:" + c.join(" ") + ";"
                            }
                            if (r.indexOf("i") !== -1) {
                                f += "font-style:italic;"
                            }
                            if (e.terminal.valid_color(i)) {
                                f += "color:" + i + ";";
                                if (r.indexOf("g") !== -1) {
                                    f += "text-shadow:0 0 5px " + i + ";"
                                }
                            }
                            if (e.terminal.valid_color(o)) {
                                f += "background-color:" + o
                            }
                            var u;
                            if (s === "") {
                                u = l
                            } else {
                                u = s.replace(/&#93;/g, "]")
                            }
                            var p;
                            if (r.indexOf("!") !== -1) {
                                if (u.match(F)) {
                                    p = '<a href="mailto:' + u + '" '
                                } else {
                                    p = '<a target="_blank" href="' + u + '" ';
                                    if (t.linksNoReferrer) {
                                        p += 'rel="noreferrer" '
                                    }
                                }
                            } else {
                                p = "<span"
                            }
                            if (f !== "") {
                                p += ' style="' + f + '"'
                            }
                            if (a !== "") {
                                p += ' class="' + a + '"'
                            }
                            if (r.indexOf("!") !== -1) {
                                p += ">" + l + "</a>"
                            } else {
                                p += ' data-text="' + u.replace('"', "&quote;") + '">' + l + "</span>"
                            }
                            return p
                        })
                    } else {
                        return "<span>" + n.replace(/\\\]/g, "]") + "</span>"
                    }
                }).join("");
                return n.replace(/<span><br\s*\/?><\/span>/gi, "<br/>")
            } else {
                return ""
            }
        },
        escape_brackets: function(e) {
            return e.replace(/\[/g, "&#91;").replace(/\]/g, "&#93;")
        },
        strip: function(e) {
            return e.replace(x, "$6")
        },
        active: function() {
            return Z.front()
        },
        last_id: function() {
            var e = Z.length();
            if (e) {
                return e - 1
            }
        },
        parse_arguments: function(n) {
            return e.map(n.match(L) || [], function(n) {
                var r = n.match($);
                if (r) {
                    return new RegExp(r[1], r[2])
                } else if (n[0] === "'" && n[n.length - 1] === "'" && n.length > 1) {
                    return n.replace(/^'|'$/g, "")
                } else if (n[0] === '"' && n[n.length - 1] === '"' && n.length > 1) {
                    return e.parseJSON(n)
                } else if (n.match(/^-?[0-9]+$/)) {
                    return parseInt(n, 10)
                } else if (n.match(N)) {
                    return parseFloat(n)
                } else if (n.match(/^['"]$/)) {
                    return ""
                } else {
                    return n.replace(/\\(['"() ])/g, "$1")
                }
            })
        },
        split_arguments: function(n) {
            return e.map(n.match(L) || [], function(e) {
                if (e[0] === "'" && e[e.length - 1] === "'") {
                    return e.replace(/^'|'$/g, "")
                } else if (e[0] === '"' && e[e.length - 1] === '"') {
                    return e.replace(/^"|"$/g, "").replace(/\\([" ])/g, "$1")
                } else if (e.match(/\/.*\/[gimy]*$/)) {
                    return e
                } else {
                    return e.replace(/\\ /g, " ")
                }
            })
        },
        parse_command: function(n) {
            return b(n, e.terminal.parse_arguments)
        },
        split_command: function(n) {
            return b(n, e.terminal.split_arguments)
        },
        extended_command: function(e, n) {
            try {
                re = false;
                e.exec(n, true).then(function() {
                    re = true
                })
            } catch (r) {}
        }
    };
    e.fn.visible = function() {
        return this.css("visibility", "visible")
    };
    e.fn.hidden = function() {
        return this.css("visibility", "hidden")
    };
    e.fn.scroll_element = function() {
        var n = e.fn.scroll_element.defaults;
        return this.map(function() {
            var r = e(this);
            if (r.is("body")) {
                var t = e("html");
                var i = e("body");
                var o = i.scrollTop() || t.scrollTop();
                var a = e("<pre/>").css(n.pre).appendTo("body");
                a.html(new Array(n.lines).join("\n"));
                e("body,html").scrollTop(10);
                var s;
                if (i.scrollTop() === 10) {
                    i.scrollTop(o);
                    s = i[0]
                } else if (t.scrollTop() === 10) {
                    t.scrollTop(o);
                    s = t[0]
                }
                a.remove();
                return s
            } else {
                return this
            }
        })
    };
    e.fn.scroll_element.defaults = {
        lines: 2e3,
        pre: {
            "font-size": "14px",
            "white-space": "pre"
        }
    };

    function z() {
        if (!("KeyboardEvent" in window && "key" in window.KeyboardEvent.prototype)) {
            return false
        }
        var e = window.KeyboardEvent.prototype;
        var n = Object.getOwnPropertyDescriptor(e, "key").get;
        return n.toString().match(/\[native code\]/)
    }

    function H(e) {
        if (console && console.warn) {
            console.warn(e)
        } else {
            throw new Error("WARN: " + e)
        }
    }
    var D = {};
    e.jrpc = function(n, r, t, i, o) {
        var a;
        if (e.isPlainObject(n)) {
            a = n
        } else {
            a = {
                url: n,
                method: r,
                params: t,
                success: i,
                error: o
            }
        }

        function s(e) {
            return typeof e.id === "number" && typeof e.result !== "undefined" || a.method === "system.describe" && e.name === "DemoService" && typeof e.id !== "undefined" && e.procs instanceof Array
        }
        D[a.url] = D[a.url] || 0;

        var l = {
            jsonrpc: "2.0",
            method: a.method,
            params: a.params,
            id: ++D[a.url]
        };
        return e.ajax({
            url: a.url,
            beforeSend: function(n, r) {
                if (e.isFunction(a.request)) {
                    a.request(n, l)
                }
                r.data = JSON.stringify(l)
            },
            success: function(n, r, t) {
                var i = t.getResponseHeader("Content-Type");
                if (!i.match(/(application|text)\/json/)) {
                    H("Response Content-Type is neither application/json" + " nor text/json")
                }
                var o;
                try {
                    o = e.parseJSON(n)
                } catch (l) {
                    if (a.error) {
                        a.error(t, "Invalid JSON", l)
                    } else {
                        throw new Error("Invalid JSON")
                    }
                    return
                }
                if (e.isFunction(a.response)) {
                    a.response(t, o)
                }
                if (s(o)) {
                    a.success(o, r, t)
                } else if (a.error) {
                    a.error(t, "Invalid JSON-RPC")
                } else {
                    throw new Error("Invalid JSON-RPC")
                }
            },
            error: a.error,
            contentType: "application/json",
            dataType: "text",
            async: true,
            cache: false,
            type: "POST"
        })
    };

    function B() {
        var n = e('<div class="terminal temp"><div class="cmd"><span cla' + 'ss="cursor">&nbsp;</span></div></div>').appendTo("body");
        var r = n.find("span");
        var t = {
            width: r.width(),
            height: r.outerHeight()
        };
        n.remove();
        return t
    }

    function W(n) {
        var r = e('<div class="terminal wrap"><span class="cursor">' + "&nbsp;</span></div>").appendTo("body").css("padding", 0);
        var t = r.find("span");
        var i = t[0].getBoundingClientRect().width;
        var o = Math.floor(n.find("iframe").width() / i);
        r.remove();
        return o
    }

    function M(e) {
        return Math.floor(e.height() / B().height)
    }

    function U() {
        if (window.getSelection || document.getSelection) {
            var e = (window.getSelection || document.getSelection)();
            if (e.text) {
                return e.text
            } else {
                return e.toString()
            }
        } else if (document.selection) {
            return document.selection.createRange().text
        }
    }

    function K(n, r) {
        var t = e("<div>" + r.replace(/\n/, "<br/>") + "<div>");
        var i;
        n.append(t);
        if (document.body.createTextRange) {
            i = document.body.createTextRange();
            i.moveToElementText(t[0]);
            i.select()
        } else if (window.getSelection) {
            var o = window.getSelection();
            if (o.setBaseAndExtent) {
                o.setBaseAndExtent(t[0], 0, t[0], 1)
            } else if (document.createRange) {
                i = document.createRange();
                i.selectNodeContents(t[0]);
                o.removeAllRanges();
                o.addRange(i)
            }
        }
        try {
            document.execCommand("copy")
        } catch (a) {}
        t.remove()
    }
    var q = !e.terminal.version.match(/^\{\{/);
    var J = "Copyright (c) 2011-2017 Jakub Jankiewicz <http://jcubic" + ".pl>";
    var G = q ? " v. " + e.terminal.version : " ";
    var Y = new RegExp(" {" + G.length + "}$");
    var X = "jQuery Terminal Emulator" + (q ? G : "");
    var V = [
        ["jQuery Terminal", "(c) 2011-2017 jcubic"],
        [X, J.replace(/^Copyright | *<.*>/g, "")],
        [X, J.replace(/^Copyright /, "")],
        ["      _______                 ________                        __", "     / / _  /_ ____________ _/__  ___/______________  _____  / /", " __ / / // / // / _  / _/ // / / / _  / _/     / /  \\/ / _ \\/ /", "/  / / // / // / ___/ // // / / / ___/ // / / / / /\\  / // / /__", "\\___/____ \\\\__/____/_/ \\__ / /_/____/_//_/_/_/ /_/  \\/\\__\\_\\___/", "         \\/          /____/                                   ".replace(Y, " ") + G, J],
        ["      __ _____                     ________                            " + "  __", "     / // _  /__ __ _____ ___ __ _/__  ___/__ ___ ______ __ __  __ ___ " + " / /", " __ / // // // // // _  // _// // / / // _  // _//     // //  \\/ // _ " + "\\/ /", "/  / // // // // // ___// / / // / / // ___// / / / / // // /\\  // // " + "/ /__", "\\___//____ \\\\___//____//_/ _\\_  / /_//____//_/ /_/ /_//_//_/ /_/ \\" + "__\\_\\___/", ("          \\/              /____/                                      " + "    ").replace(Y, "") + G, J]
    ];
    e.terminal.defaults = {
        prompt: "> ",
        history: true,
        exit: true,
        clear: true,
        enabled: true,
        historySize: 60,
        maskChar: "*",
        wrap: true,
        checkArity: true,
        raw: false,
        exceptionHandler: null,
        memory: false,
        cancelableAjax: true,
        processArguments: true,
        linksNoReferrer: false,
        processRPCResponse: null,
        Token: true,
        convertLinks: true,
        extra: {},
        historyState: false,
        importHistory: false,
        echoCommand: true,
        scrollOnEcho: true,
        login: null,
        outputLimit: -1,
        formatters: [],
        onAjaxError: null,
        scrollBottomOffset: 20,
        wordAutocomplete: true,
        clickTimeout: 200,
        request: e.noop,
        response: e.noop,
        onRPCError: null,
        completion: false,
        historyFilter: null,
        softPause: false,
        onInit: e.noop,
        onClear: e.noop,
        onBlur: e.noop,
        onFocus: e.noop,
        onTerminalChange: e.noop,
        onExit: e.noop,
        onPush: e.noop,
        onPop: e.noop,
        keypress: e.noop,
        keydown: e.noop,
        strings: {
            comletionParameters: "From version 1.0.0 completion function need to" + " have two arguments",
            wrongPasswordTryAgain: "Wrong password try again!",
            wrongPassword: "Wrong password!",
            ajaxAbortError: "Error while aborting ajax call!",
            wrongArity: "Wrong number of arguments. Function '%s' expects %s got" + " %s!",
            commandNotFound: "Command '%s' Not Found!",
            oneRPCWithIgnore: "You can use only one rpc with ignoreSystemDescr" + "ibe or rpc without system.describe",
            oneInterpreterFunction: "You can't use more than one function (rpc " + "without system.describe or with option ignoreSystemDescribe cou" + "nts as one)",
            loginFunctionMissing: "You didn't specify a login function",
            noTokenError: "Access denied (no token)",
            serverResponse: "Server responded",
            wrongGreetings: "Wrong value of greetings parameter",
            notWhileLogin: "You can't call `%s' function while in login",
            loginIsNotAFunction: "Authenticate must be a function",
            canExitError: "You can't exit from main interpreter",
            invalidCompletion: "Invalid completion",
            invalidSelector: 'Sorry, but terminal said that "%s" is not valid ' + "selector!",
            invalidTerminalId: "Invalid Terminal ID",
            login: "login",
            password: "password",
            recursiveCall: "Recursive call detected, skip",
            notAString: "%s function: argument is not a string",
            redrawError: "Internal error, wrong position in cmd redraw"
        }
    };
    var Q = [];
    var Z = new h;
    var ee = [];
    var ne;
    var re = false;
    var te = true;
    var ie = true;
    e.fn.terminal = function(r, i) {
        function o(n) {
            if (n) {
                this.storage = {}
            }
            this.set = function(r, t) {
                if (n) {
                    this.storage[r] = t
                } else {
                    e.Storage.set(r, t)
                }
            };
            this.get = function(r) {
                if (n) {
                    return this.storage[r]
                } else {
                    return e.Storage.get(r)
                }
            };
            this.remove = function(r) {
                if (n) {
                    delete this.storage[r]
                } else {
                    e.Storage.remove(r)
                }
            }
        }

        function a(n) {
            if (e.isFunction(Ee.processArguments)) {
                return b(n, Ee.processArguments)
            } else if (Ee.processArguments) {
                return e.terminal.parse_command(n)
            } else {
                return e.terminal.split_command(n)
            }
        }

        function s(n) {
            if (typeof n === "string") {
                se.echo(n)
            } else if (n instanceof Array) {
                se.echo(e.map(n, function(e) {
                    return JSON.stringify(e)
                }).join(" "))
            } else if (typeof n === "object") {
                se.echo(JSON.stringify(n))
            } else {
                se.echo(n)
            }
        }

        function l(n) {
            var r = /(.*):([0-9]+):([0-9]+)$/;
            var t = n.match(r);
            if (t) {
                se.pause(Ee.softPause);
                e.get(t[1], function(n) {
                    var r = location.href.replace(/[^\/]+$/, "");
                    var i = t[1].replace(r, "");
                    se.echo("[[b;white;]" + i + "]");
                    var o = n.split("\n");
                    var a = +t[2] - 1;
                    se.echo(o.slice(a - 2, a + 3).map(function(n, r) {
                        if (r === 2) {
                            n = "[[;#f00;]" + e.terminal.escape_brackets(n) + "]"
                        }
                        return "[" + (a + r) + "]: " + n
                    }).join("\n")).resume()
                }, "text")
            }
        }

        function f(n) {
            if (e.isFunction(Ee.onRPCError)) {
                Ee.onRPCError.call(se, n)
            } else {
                se.error("&#91;RPC&#93; " + n.message);
                if (n.error && n.error.message) {
                    n = n.error;
                    var r = "	" + n.message;
                    if (n.file) {
                        r += ' in file "' + n.file.replace(/.*\//, "") + '"'
                    }
                    if (n.at) {
                        r += " at line " + n.at
                    }
                    se.error(r)
                }
            }
        }

        function c(n, r) {
            var t = function(r, t) {
                se.pause(Ee.softPause);
                e.jrpc({
                    url: n,
                    method: r,
                    params: t,
                    request: function(e, n) {
                        try {
                            Ee.request.apply(se, e, n, se)
                        } catch (r) {
                            y(r, "USER")
                        }
                    },
                    response: function(e, n) {
                        try {
                            Ee.response.apply(se, e, n, se)
                        } catch (r) {
                            y(r, "USER")
                        }
                    },
                    success: function(n) {
                        if (n.error) {
                            f(n.error)
                        } else if (e.isFunction(Ee.processRPCResponse)) {
                            Ee.processRPCResponse.call(se, n.result, se)
                        } else {
                            s(n.result)
                        }
                        se.resume()
                    },
                    error: p
                })
            };
            return function(e, n) {
                if (e === "") {
                    return
                }
                try {
                    e = a(e)
                } catch (i) {
                    y(i, "TERMINAL (get_processed_command)");
                    return
                }
                if (!r || e.name === "help") {
                    t(e.name, e.args)
                } else {
                    var o = n.token();
                    if (o) {
                        t(e.name, [o].concat(e.args))
                    } else {
                        n.error("&#91;AUTH&#93; " + Ae.noTokenError)
                    }
                }
            }
        }

        function u(r, t, i, o) {
            return function(s, l) {
                if (s === "") {
                    return
                }
                var f;
                try {
                    f = a(s)
                } catch (c) {
                    if (e.isFunction(Ee.exception)) {
                        Ee.exception(c, se)
                    } else {
                        se.error(c.toString())
                    }
                    return
                }
                var p = r[f.name];
                var m = e.type(p);
                if (m === "function") {
                    if (t && p.length !== f.args.length) {
                        se.error("&#91;Arity&#93; " + sprintf(Ae.wrongArity, f.name, p.length, f.args.length))
                    } else {
                        return p.apply(se, f.args)
                    }
                } else if (m === "object" || m === "string") {
                    var h = [];
                    if (m === "object") {
                        h = Object.keys(p);
                        p = u(p, t, i)
                    }
                    l.push(p, {
                        prompt: f.name + "> ",
                        name: f.name,
                        completion: m === "object" ? h : n
                    })
                } else if (e.isFunction(o)) {
                    o(s, se)
                } else if (e.isFunction(Ee.onCommandNotFound)) {
                    Ee.onCommandNotFound.call(se, s, se)
                } else {
                    l.error(sprintf(Ae.commandNotFound, f.name))
                }
            }
        }

        function p(n, r, t) {
            se.resume();
            if (e.isFunction(Ee.onAjaxError)) {
                Ee.onAjaxError.call(se, n, r, t)
            } else if (r !== "abort") {
                se.error("&#91;AJAX&#93; " + r + " - " + Ae.serverResponse + ":\n" + e.terminal.escape_brackets(n.responseText))
            }
        }

        function m(n, r, t) {
            function i(n) {
                if (n.error) {
                    f(n.error)
                } else if (e.isFunction(Ee.processRPCResponse)) {
                    Ee.processRPCResponse.call(se, n.result, se)
                } else {
                    s(n.result)
                }
                se.resume()
            }

            function o(e, n) {
                try {
                    Ee.request.call(se, e, n, se)
                } catch (r) {
                    y(r, "USER")
                }
            }

            function a(e, n) {
                try {
                    Ee.response.call(se, e, n, se)
                } catch (r) {
                    y(r, "USER")
                }
            }

            function l(s) {
                if (s.procs) {
                    var l = {};
                    e.each(s.procs, function(t, s) {
                        l[s.name] = function() {
                            var t = r && s.name !== "help";
                            var l = Array.prototype.slice.call(arguments);
                            var f = l.length + (t ? 1 : 0);
                            if (Ee.checkArity && s.params && s.params.length !== f) {
                                se.error("&#91;Arity&#93; " + sprintf(Ae.wrongArity, s.name, s.params.length, f))
                            } else {
                                se.pause(Ee.softPause);
                                if (t) {
                                    var c = se.token(true);
                                    if (c) {
                                        l = [c].concat(l)
                                    } else {
                                        se.error("&#91;AUTH&#93; " + Ae.noTokenError)
                                    }
                                }
                                e.jrpc({
                                    url: n,
                                    method: s.name,
                                    params: l,
                                    request: o,
                                    response: a,
                                    success: i,
                                    error: p
                                })
                            }
                        }
                    });
                    l.help = l.help || function(n) {
                        if (typeof n === "undefined") {
                            var r = s.procs.map(function(e) {
                                return e.name
                            }).join(", ") + ", help";
                            se.echo("Available commands: " + r)
                        } else {
                            var t = false;
                            e.each(s.procs, function(e, r) {
                                if (r.name === n) {
                                    t = true;
                                    var i = "";
                                    i += "[[bu;#fff;]" + r.name + "]";
                                    if (r.params) {
                                        i += " " + r.params.join(" ")
                                    }
                                    if (r.help) {
                                        i += "\n" + r.help
                                    }
                                    se.echo(i);
                                    return false
                                }
                            });
                            if (!t) {
                                if (n === "help") {
                                    se.echo("[[bu;#fff;]help] [method]\ndisplay help " + "for the method or list of methods if not" + " specified")
                                } else {
                                    var i = "Method `" + n + "' not found ";
                                    se.error(i)
                                }
                            }
                        }
                    };
                    t(l)
                } else {
                    t(null)
                }
            }
            return e.jrpc({
                url: n,
                method: "system.describe",
                params: [],
                success: l,
                request: function(e, n) {
                    try {
                        Ee.request.call(se, e, n, se)
                    } catch (r) {
                        y(r, "USER")
                    }
                },
                response: function(e, n) {
                    try {
                        Ee.response.call(se, e, n, se)
                    } catch (r) {
                        y(r, "USER")
                    }
                },
                error: function() {
                    t(null)
                }
            })
        }

        function h(n, r, t) {
            t = t || e.noop;
            var i = e.type(n);
            var o;
            var a = {};
            var s = 0;
            var l;
            if (i === "array") {
                o = {};
                (function f(n, t) {
                    if (n.length) {
                        var i = n[0];
                        var a = n.slice(1);
                        var u = e.type(i);
                        if (u === "string") {
                            se.pause(Ee.softPause);
                            if (Ee.ignoreSystemDescribe) {
                                if (++s === 1) {
                                    l = c(i, r)
                                } else {
                                    se.error(Ae.oneRPCWithIgnore)
                                }
                                f(a, t)
                            } else {
                                m(i, r, function(n) {
                                    if (n) {
                                        e.extend(o, n)
                                    } else if (++s === 1) {
                                        l = c(i, r)
                                    } else {
                                        se.error(Ae.oneRPCWithIgnore)
                                    }
                                    se.resume();
                                    f(a, t)
                                })
                            }
                        } else if (u === "function") {
                            if (l) {
                                se.error(Ae.oneInterpreterFunction)
                            } else {
                                l = i
                            }
                            f(a, t)
                        } else if (u === "object") {
                            e.extend(o, i);
                            f(a, t)
                        }
                    } else {
                        t()
                    }
                })(n, function() {
                    t({
                        interpreter: u(o, false, r, l.bind(se)),
                        completion: Object.keys(o)
                    })
                })
            } else if (i === "string") {
                if (Ee.ignoreSystemDescribe) {
                    o = {
                        interpreter: c(n, r)
                    };
                    if (e.isArray(Ee.completion)) {
                        o.completion = Ee.completion
                    }
                    t(o)
                } else {
                    se.pause(Ee.softPause);
                    m(n, r, function(e) {
                        if (e) {
                            a.interpreter = u(e, false, r);
                            a.completion = Object.keys(e)
                        } else {
                            a.interpreter = c(n, r)
                        }
                        t(a);
                        se.resume()
                    })
                }
            } else if (i === "object") {
                t({
                    interpreter: u(n, Ee.checkArity),
                    completion: Object.keys(n)
                })
            } else {
                if (i === "undefined") {
                    n = e.noop
                } else if (i !== "function") {
                    throw new Error(i + " is invalid interpreter value")
                }
                t({
                    interpreter: n,
                    completion: Ee.completion
                })
            }
        }

        function d(n, r) {
            var t = e.type(r) === "boolean" ? "login" : r;
            return function(r, i, o) {
                se.pause(Ee.softPause);
                e.jrpc({
                    url: n,
                    method: t,
                    params: [r, i],
                    request: function(e, n) {
                        try {
                            Ee.request.call(se, e, n, se)
                        } catch (r) {
                            y(r, "USER")
                        }
                    },
                    response: function(e, n) {
                        try {
                            Ee.response.call(se, e, n, se)
                        } catch (r) {
                            y(r, "USER")
                        }
                    },
                    success: function(e) {
                        if (!e.error && e.result) {
                            o(e.result)
                        } else {
                            o(null)
                        }
                        se.resume()
                    },
                    error: p
                })
            }
        }

        function v(e) {
            if (typeof e === "string") {
                return e
            } else if (typeof e.fileName === "string") {
                return e.fileName + ": " + e.message
            } else {
                return e.message
            }
        }

        function y(n, r) {
            if (e.isFunction(Ee.exceptionHandler)) {
                Ee.exceptionHandler.call(se, n, r)
            } else {
                se.exception(n, r)
            }
        }

        function _() {
            var e;
            if (le.prop) {
                e = le.prop("scrollHeight")
            } else {
                e = le.attr("scrollHeight")
            }
            le.scrollTop(e)
        }

        function k(n, r) {
            try {
                if (e.isFunction(r)) {
                    r(function() {})
                } else if (typeof r !== "string") {
                    var t = n + " must be string or function";
                    throw t
                }
            } catch (i) {
                y(i, n.toUpperCase());
                return false
            }
            return true
        }
        var x = [];
        var T = 1;

        function R(r, t) {
            if (Ee.convertLinks && !t.raw) {
                r = r.replace(F, "[[!;;]$1]").replace(A, "[[!;;]$1]")
            }
            var i = e.terminal.defaults.formatters;
            var o, a;
            if (!t.raw) {
                if (t.formatters) {
                    for (o = 0; o < i.length; ++o) {
                        try {
                            if (typeof i[o] === "function") {
                                var s = i[o](r);
                                if (typeof s === "string") {
                                    r = s
                                }
                            }
                        } catch (l) {
                            if (e.isFunction(Ee.exceptionHandler)) {
                                Ee.exceptionHandler.call(se, l, "FORMATTERS")
                            } else {
                                alert("formatting error at formatters[" + o + "]\n" + (l.stack ? l.stack : l))
                            }
                        }
                    }
                }
                r = e.terminal.encode(r)
            }
            x.push(T);
            if (!t.raw && (r.length > he || r.match(/\n/)) && (Ee.wrap === true && t.wrap === n || Ee.wrap === false && t.wrap === true)) {
                var f = t.keepWords;
                var c = e.terminal.split_equal(r, he, f);
                for (o = 0, a = c.length; o < a; ++o) {
                    if (c[o] === "" || c[o] === "\r") {
                        x.push("<span></span>")
                    } else if (t.raw) {
                        x.push(c[o])
                    } else {
                        x.push(e.terminal.format(c[o], {
                            linksNoReferrer: Ee.linksNoReferrer
                        }))
                    }
                }
            } else if (!t.raw) {
                r = e.terminal.format(r, {
                    linksNoReferrer: Ee.linksNoReferrer
                });
                r.split(/\n/).forEach(function(e) {
                    x.push(e)
                })
            } else {
                x.push(r)
            }
            x.push(t.finalize)
        }

        function C(n, r) {
            try {
                var t = e.extend({
                    exec: true,
                    raw: false,
                    finalize: e.noop
                }, r || {});
                var i = e.type(n) === "function" ? n() : n;
                i = e.type(i) === "string" ? i : String(i);
                if (i !== "") {
                    i = e.map(i.split(I), function(n) {
                        if (n.match(I) && !e.terminal.is_formatting(n)) {
                            n = n.replace(/^\[\[|\]\]$/g, "");
                            if (t.exec) {
                                if (fe && fe.command === n) {
                                    se.error(Ae.recursiveCall)
                                } else {
                                    e.terminal.extended_command(se, n)
                                }
                            }
                            return ""
                        } else {
                            return n
                        }
                    }).join("");
                    if (i !== "") {
                        R(i, t)
                    }
                }
            } catch (o) {
                x = [];
                if (e.isFunction(Ee.exceptionHandler)) {
                    Ee.exceptionHandler.call(se, o, "TERMINAL")
                } else {
                    alert("[Internal Exception(process_line)]:" + v(o) + "\n" + o.stack)
                }
            }
        }

        function E() {
            Be.resize(he);
            var n = pe.empty().detach();
            var r;
            if (Ee.outputLimit >= 0) {
                var t;
                if (Ee.outputLimit === 0) {
                    t = se.rows()
                } else {
                    t = Ee.outputLimit
                }
                r = ue.slice(ue.length - t - 1)
            } else {
                r = ue
            }
            try {
                x = [];
                e.each(r, function(e, n) {
                    C.apply(null, n)
                });
                Be.before(n);
                se.flush()
            } catch (i) {
                if (e.isFunction(Ee.exceptionHandler)) {
                    Ee.exceptionHandler.call(se, i, "TERMINAL (redraw)")
                } else {
                    alert("Exception in redraw\n" + i.stack)
                }
            }
        }

        function L() {
            if (Ee.greetings === n) {
                se.echo(se.signature)
            } else if (Ee.greetings) {
                var e = typeof Ee.greetings;
                if (e === "string") {
                    se.echo(Ee.greetings)
                } else if (e === "function") {
                    Ee.greetings.call(se, se.echo)
                } else {
                    se.error(Ae.wrongGreetings)
                }
            }
        }

        function O(n) {
            var r = Be.prompt();
            var t = Be.mask();
            switch (typeof t) {
                case "string":
                    n = n.replace(/./g, t);
                    break;
                case "boolean":
                    if (t) {
                        n = n.replace(/./g, Ee.maskChar)
                    } else {
                        n = e.terminal.escape_formatting(n)
                    }
                    break
            }
            var i = {
                finalize: function(e) {
                    e.addClass("command")
                }
            };
            if (e.isFunction(r)) {
                r(function(e) {
                    se.echo(e + n, i)
                })
            } else {
                se.echo(r + n, i)
            }
        }

        function P(e) {
            var n = Z.get()[e[0]];
            if (!n) {
                throw new Error(Ae.invalidTerminalId)
            }
            var r = e[1];
            if (ee[r]) {
                n.import_view(ee[r])
            } else {
                re = false;
                var t = e[2];
                if (t) {
                    n.exec(t).then(function() {
                        re = true;
                        ee[r] = n.export_view()
                    })
                }
            }
        }

        function j() {
            if (re) {
                te = false;
                location.hash = "#" + JSON.stringify(ne);
                setTimeout(function() {
                    te = true
                }, 100)
            }
        }
        var N = true;
        var $ = [];

        function z(r, t, i) {
            if (N) {
                N = false;
                if (Ee.historyState || Ee.execHash && i) {
                    if (!ee.length) {
                        se.save_state()
                    } else {
                        se.save_state(null)
                    }
                }
            }

            function o() {
                if (!i) {
                    re = true;
                    if (Ee.historyState) {
                        se.save_state(r, false)
                    }
                    re = f
                }
                l.resolve();
                if (e.isFunction(Ee.onAfterCommand)) {
                    Ee.onAfterCommand.call(se, se, r)
                }
            }
            try {
                if (e.isFunction(Ee.onBeforeCommand)) {
                    if (Ee.onBeforeCommand.call(se, se, r) === false) {
                        return
                    }
                }
                if (!i) {
                    fe = e.terminal.split_command(r)
                }
                if (!G()) {
                    if (i && (e.isFunction(Ee.historyFilter) && Ee.historyFilter(r) || r.match(Ee.historyFilter))) {
                        Be.history().append(r)
                    }
                }
                var a = De.top();
                if (!t && Ee.echoCommand) {
                    O(r)
                }
                var l = new e.Deferred;
                var f = re;
                if (r.match(/^\s*login\s*$/) && se.token(true)) {
                    if (se.level() > 1) {
                        se.logout(true)
                    } else {
                        se.logout()
                    }
                    o()
                } else if (Ee.exit && r.match(/^\s*exit\s*$/) && !ke) {
                    var c = se.level();
                    if (c === 1 && se.get_token() || c > 1) {
                        if (se.get_token(true)) {
                            se.set_token(n, true)
                        }
                        se.pop()
                    }
                    o()
                } else if (Ee.clear && r.match(/^\s*clear\s*$/) && !ke) {
                    se.clear();
                    o()
                } else {
                    var u = ue.length - 1;
                    var p = a.interpreter.call(se, r, se);
                    if (p !== n) {
                        se.pause(Ee.softPause);
                        return e.when(p).then(function(e) {
                            if (e && u === ue.length - 1) {
                                s(e)
                            }
                            o();
                            se.resume()
                        })
                    } else if (Oe) {
                        $.push(function() {
                            o()
                        })
                    } else {
                        o()
                    }
                }
                return l.promise()
            } catch (m) {
                y(m, "USER");
                se.resume();
                throw m
            }
        }

        function H() {
            if (e.isFunction(Ee.onBeforeLogout)) {
                try {
                    if (Ee.onBeforeLogout.call(se, se) === false) {
                        return
                    }
                } catch (n) {
                    y(n, "onBeforeLogout")
                }
            }
            D();
            if (e.isFunction(Ee.onAfterLogout)) {
                try {
                    Ee.onAfterLogout.call(se, se)
                } catch (n) {
                    y(n, "onAfterlogout")
                }
            }
            se.login(Ee.login, true, J)
        }

        function D() {
            var e = se.prefix_name(true) + "_";
            Se.remove(e + "token");
            Se.remove(e + "login")
        }

        function B(n) {
            var r = se.prefix_name() + "_interpreters";
            var t = Se.get(r);
            if (t) {
                t = e.parseJSON(t)
            } else {
                t = []
            }
            if (e.inArray(n, t) === -1) {
                t.push(n);
                Se.set(r, JSON.stringify(t))
            }
        }

        function K(n) {
            var r = De.top();
            var t = se.prefix_name(true);
            if (!G()) {
                B(t)
            }
            Be.name(t);
            if (e.isFunction(r.prompt)) {
                Be.prompt(function(e) {
                    r.prompt.call(se, e, se)
                })
            } else {
                Be.prompt(r.prompt)
            }
            if (e.isPlainObject(r.keymap)) {
                Be.keymap(e.omap(r.keymap, function(e, n) {
                    return function() {
                        var e = [].slice.call(arguments);
                        try {
                            return n.apply(se, e)
                        } catch (r) {
                            y(r, "USER KEYMAP");
                            throw r
                        }
                    }
                }))
            }
            Be.set("");
            _e.resolve();
            if (!n && e.isFunction(r.onStart)) {
                r.onStart.call(se, se)
            }
        }

        function q() {
            if (te && Ee.execHash) {
                try {
                    if (location.hash) {
                        var n = location.hash.replace(/^#/, "");
                        ne = e.parseJSON(decodeURIComponent(n))
                    } else {
                        ne = []
                    }
                    if (ne.length) {
                        P(ne[ne.length - 1])
                    } else if (ee[0]) {
                        se.import_view(ee[0])
                    }
                } catch (r) {
                    y(r, "TERMINAL")
                }
            }
        }

        function J() {
            K();
            L();
            if (ue.length) {
                E()
            }
            var n = false;
            if (e.isFunction(Ee.onInit)) {
                xe = function() {
                    n = true
                };
                try {
                    Ee.onInit.call(se, se)
                } catch (r) {
                    y(r, "OnInit")
                } finally {
                    xe = e.noop;
                    if (!n && se.enabled()) {
                        se.resume()
                    }
                }
            }
            if (ie) {
                ie = false;
                e(window).on("hashchange", q)
            }
        }

        function G() {
            return ke || Be.mask() !== false
        }

        function Y(r) {
            var t, i = De.top();
            if (e.isFunction(i.keydown)) {
                t = i.keydown.call(se, r, se);
                if (t !== n) {
                    return t
                }
            } else if (e.isFunction(Ee.keydown)) {
                t = Ee.keydown.call(se, r, se);
                if (t !== n) {
                    return t
                }
            }
        }
        var X = {
            "CTRL+D": function(e, r) {
                if (!ke) {
                    if (Be.get() === "") {
                        if (De.size() > 1 || Ee.login !== n) {
                            se.pop("")
                        } else {
                            se.resume();
                            se.echo("")
                        }
                    } else {
                        r()
                    }
                }
                return false
            },
            "CTRL+L": function() {
                se.clear()
            },
            TAB: function(r, t) {
                var i = De.top(),
                    o;
                if (Ee.completion && e.type(Ee.completion) !== "boolean" && i.completion === n) {
                    o = Ee.completion
                } else {
                    o = i.completion
                }
                if (o === "settings") {
                    o = Ee.completion
                }
                if (o) {
                    switch (e.type(o)) {
                        case "function":
                            var a = se.before_cursor(Ee.wordAutocomplete);
                            if (o.length === 3) {
                                var s = new Error(Ae.comletionParameters);
                                y(s, "USER");
                                return false
                            }
                            o.call(se, a, function(e) {
                                se.complete(e, {
                                    echo: true
                                })
                            });
                            break;
                        case "array":
                            se.complete(o, {
                                echo: true
                            });
                            break;
                        default:
                            throw new Error(Ae.invalidCompletion)
                    }
                } else {
                    t()
                }
                return false
            },
            "CTRL+V": function(e, n) {
                n(e);
                se.oneTime(200, function() {
                    _()
                });
                return true
            },
            "CTRL+TAB": function() {
                if (Z.length() > 1) {
                    se.focus(false);
                    return false
                }
            },
            PAGEDOWN: function() {
                se.scroll(se.height())
            },
            PAGEUP: function() {
                se.scroll(-se.height())
            }
        };

        function oe(r) {
            var t, i;
            if (!se.paused() && se.enabled()) {
                t = Y(r);
                if (t !== n) {
                    return t
                }
                if (r.which !== 9) {
                    ce = 0
                }
                se.attr({
                    scrollTop: se.attr("scrollHeight")
                })
            } else if (r.which === 68 && r.ctrlKey) {
                t = Y(r);
                if (t !== n) {
                    return t
                }
                if (Q.length) {
                    for (i = Q.length; i--;) {
                        var o = Q[i];
                        if (o.readyState !== 4) {
                            try {
                                o.abort()
                            } catch (a) {
                                if (e.isFunction(Ee.exceptionHandler)) {
                                    Ee.exceptionHandler.call(se, r, "AJAX ABORT")
                                } else {
                                    se.error(Ae.ajaxAbortError)
                                }
                            }
                        }
                    }
                    Q = [];
                    se.resume()
                }
                return false
            }
        }

        function ae(e) {
            return function(n) {
                if (e.state() !== "resolved") {
                    e.then(n.bind(se))
                } else {
                    n.call(se)
                }
            }
        }
        var se = this;
        if (this.length > 1) {
            return this.each(function() {
                e.fn.terminal.call(e(this), r, e.extend({
                    name: se.selector
                }, i))
            })
        }
        if (se.data("terminal")) {
            return se.data("terminal")
        }
        if (se.length === 0) {
            throw sprintf(e.terminal.defaults.strings.invalidSelector, se.selector)
        }
        var le;
        var fe;
        var ce = 0;
        var ue = [];
        var pe;
        var me = Z.length();
        var he;
        var ge;
        var de;
        var ve = new g;
        var ye = e.Deferred();
        var _e = e.Deferred();
        var we = ae(_e);
        var be = ae(ye);
        var ke = false;
        var xe = e.noop;
        var Te, Re;
        var Ce = [];
        var Ee = e.extend({}, e.terminal.defaults, {
            name: se.selector
        }, i || {});
        var Se = new o(Ee.memory);
        var Ae = e.extend({}, e.terminal.defaults.strings, Ee.strings);
        var Fe = Ee.enabled,
            Le = false;
        var Oe = false;
        var Pe = true;
        e.extend(se, e.omap({
            id: function() {
                return me
            },
            clear: function() {
                pe.html("");
                ue = [];
                try {
                    Ee.onClear.call(se, se)
                } catch (e) {
                    y(e, "onClear")
                }
                se.attr({
                    scrollTop: 0
                });
                return se
            },
            export_view: function() {
                var n = {};
                if (e.isFunction(Ee.onExport)) {
                    try {
                        n = Ee.onExport.call(se)
                    } catch (r) {
                        y(r, "onExport")
                    }
                }
                return e.extend({}, {
                    focus: Fe,
                    mask: Be.mask(),
                    prompt: se.get_prompt(),
                    command: se.get_command(),
                    position: Be.position(),
                    lines: t(ue),
                    interpreters: De.clone(),
                    history: Be.history().data
                }, n)
            },
            import_view: function(n) {
                if (ke) {
                    throw new Error(sprintf(Ae.notWhileLogin, "import_view"))
                }
                if (e.isFunction(Ee.onImport)) {
                    try {
                        Ee.onImport.call(se, n)
                    } catch (r) {
                        y(r, "onImport")
                    }
                }
                we(function i() {
                    se.set_prompt(n.prompt);
                    se.set_command(n.command);
                    Be.position(n.position);
                    Be.mask(n.mask);
                    if (n.focus) {
                        se.focus()
                    }
                    ue = t(n.lines);
                    De = n.interpreters;
                    if (Ee.importHistory) {
                        Be.history().set(n.history)
                    }
                    E()
                });
                return se
            },
            save_state: function(r, t, i) {
                if (typeof i !== "undefined") {
                    ee[i] = se.export_view()
                } else {
                    ee.push(se.export_view())
                }
                if (!e.isArray(ne)) {
                    ne = []
                }
                if (r !== n && !t) {
                    var o = [me, ee.length - 1, r];
                    ne.push(o);
                    j()
                }
            },
            exec: function(n, r, t) {
                var i = t || new e.Deferred;
                be(function o() {
                    if (e.isArray(n)) {
                        (function t() {
                            var e = n.shift();
                            if (e) {
                                se.exec(e, r).then(t)
                            } else {
                                i.resolve()
                            }
                        })()
                    } else if (Oe) {
                        Ce.push([n, r, i])
                    } else {
                        z(n, r, true).then(function() {
                            i.resolve(se)
                        })
                    }
                });
                return i.promise()
            },
            autologin: function(e, n, r) {
                se.trigger("terminal.autologin", [e, n, r]);
                return se
            },
            login: function(r, t, i, o) {
                ve.push([].slice.call(arguments));
                if (ke) {
                    throw new Error(sprintf(Ae.notWhileLogin, "login"))
                }
                if (!e.isFunction(r)) {
                    throw new Error(Ae.loginIsNotAFunction)
                }
                ke = true;
                if (se.token() && se.level() === 1 && !Pe) {
                    ke = false;
                    se.logout(true)
                } else if (se.token(true) && se.login_name(true)) {
                    ke = false;
                    if (e.isFunction(i)) {
                        i()
                    }
                    return se
                }
                if (Ee.history) {
                    Be.history().disable()
                }
                var a = se.level();

                function s(r, s, l) {
                    if (s) {
                        while (se.level() > a) {
                            se.pop(n, true)
                        }
                        if (Ee.history) {
                            Be.history().enable()
                        }
                        var f = se.prefix_name(true) + "_";
                        Se.set(f + "token", s);
                        Se.set(f + "login", r);
                        ke = false;
                        if (e.isFunction(i)) {
                            i()
                        }
                    } else {
                        if (t) {
                            if (!l) {
                                se.error(Ae.wrongPasswordTryAgain)
                            }
                            se.pop(n, true).set_mask(false)
                        } else {
                            ke = false;
                            if (!l) {
                                se.error(Ae.wrongPassword)
                            }
                            se.pop(n, true).pop(n, true)
                        }
                        if (e.isFunction(o)) {
                            o()
                        }
                    }
                    se.off("terminal.autologin")
                }
                se.on("terminal.autologin", function(e, n, r, t) {
                    s(n, r, t)
                });
                se.push(function(e) {
                    se.set_mask(Ee.maskChar).push(function(n) {
                        try {
                            r.call(se, e, n, function(n, r) {
                                s(e, n, r)
                            })
                        } catch (t) {
                            y(t, "AUTH")
                        }
                    }, {
                        prompt: Ae.password + ": ",
                        name: "password"
                    })
                }, {
                    prompt: Ae.login + ": ",
                    name: "login"
                });
                return se
            },
            settings: function() {
                return Ee
            },
            before_cursor: function(e) {
                var n = Be.position();
                var r = Be.get().substring(0, n);
                var t = r.split(" ");
                var i;
                if (e) {
                    if (t.length === 1) {
                        i = t[0]
                    } else {
                        var o = r.match(/(\\?")/g);
                        var a = o ? o.filter(function(e) {
                            return !e.match(/^\\/)
                        }).length : 0;
                        o = r.match(/'/g);
                        var s = o ? o.length : 0;
                        if (s % 2 === 1) {
                            i = r.match(/('[^']*)$/)[0]
                        } else if (a % 2 === 1) {
                            i = r.match(/("(?:[^"]|\\")*)$/)[0]
                        } else {
                            i = t[t.length - 1];
                            for (ze = t.length - 1; ze > 0; ze--) {
                                var l = t[ze - 1];
                                if (l[l.length - 1] === "\\") {
                                    i = t[ze - 1] + " " + i
                                } else {
                                    break
                                }
                            }
                        }
                    }
                } else {
                    i = r
                }
                return i
            },
            complete: function(n, r) {
                r = e.extend({
                    word: true,
                    echo: false
                }, r || {});
                var t = se.before_cursor(r.word).replace(/\\"/g, '"');
                var i = false;
                if (t.match(/^"/)) {
                    i = '"'
                } else if (t.match(/^'/)) {
                    i = "'"
                }
                if (i) {
                    t = t.replace(/^["']/, "")
                }
                n = n.slice();
                if (Ee.clear && e.inArray("clear", n) === -1) {
                    n.push("clear")
                }
                if (Ee.exit && e.inArray("exit", n) === -1) {
                    n.push("exit")
                }
                if (ce % 2 === 0) {
                    de = se.before_cursor(r.word)
                } else {
                    var o = se.before_cursor(r.word);
                    if (o !== de) {
                        return
                    }
                }
                var a = e.terminal.escape_regex(t).replace(/\\(["'() ])/g, "\\?$1");
                var s = new RegExp("^" + a);
                var l = [];
                for (var f = n.length; f--;) {
                    if (s.test(n[f])) {
                        var c = n[f];
                        if (i === '"') {
                            c = c.replace(/"/g, '\\"')
                        }
                        if (!i) {
                            c = c.replace(/(["'() ])/g, "\\$1")
                        }
                        l.push(c)
                    }
                }
                if (l.length === 1) {
                    se.insert(l[0].replace(s, "") + (i || ""));
                    de = se.before_cursor(r.word);
                    return true
                } else if (l.length > 1) {
                    if (++ce >= 2) {
                        ce = 0;
                        if (r.echo) {
                            var u = l.reverse().join("	");
                            se.echo(e.terminal.escape_brackets(u), {
                                keepWords: true
                            });
                            return true
                        }
                    } else {
                        var p = false;
                        var m;
                        e: for (m = t.length; m < l[0].length; ++m) {
                            for (f = 1; f < l.length; ++f) {
                                if (l[0].charAt(m) !== l[f].charAt(m)) {
                                    break e
                                }
                            }
                            p = true
                        }
                        if (p) {
                            se.insert(l[0].slice(0, m).replace(s, ""));
                            de = se.before_cursor(r.word);
                            return true
                        }
                    }
                }
            },
            commands: function() {
                return De.top().interpreter
            },
            set_interpreter: function(n, r) {
                function t() {
                    se.pause(Ee.softPause);
                    h(n, !!r, function(n) {
                        se.resume();
                        var r = De.top();
                        e.extend(r, n);
                        K(true)
                    })
                }
                if (e.type(n) === "string" && r) {
                    se.login(d(n, r), true, t)
                } else {
                    t()
                }
                return se
            },
            greetings: function() {
                L();
                return se
            },
            paused: function() {
                return Oe
            },
            pause: function(n) {
                be(function r() {
                    xe();
                    Oe = true;
                    Be.disable();
                    if (!n) {
                        Be.hidden()
                    }
                    if (e.isFunction(Ee.onPause)) {
                        Ee.onPause.call(se)
                    }
                });
                return se
            },
            resume: function() {
                be(function n() {
                    Oe = false;
                    if (Z.front() === se) {
                        Be.enable()
                    }
                    Be.visible();
                    var n = Ce;
                    Ce = [];
                    for (var r = 0; r < n.length; ++r) {
                        se.exec.apply(se, n[r])
                    }
                    se.trigger("resume");
                    var t = $.shift();
                    if (t) {
                        t()
                    }
                    _();
                    if (e.isFunction(Ee.onResume)) {
                        Ee.onResume.call(se)
                    }
                });
                return se
            },
            cols: function() {
                return Ee.numChars ? Ee.numChars : W(se)
            },
            rows: function() {
                return Ee.numRows ? Ee.numRows : M(se)
            },
            history: function() {
                return Be.history()
            },
            history_state: function(e) {
                function n() {
                    Ee.historyState = true;
                    if (!ee.length) {
                        se.save_state()
                    } else if (Z.length() > 1) {
                        se.save_state(null)
                    }
                }
                if (e) {
                    if (typeof window.setImmediate === "undefined") {
                        setTimeout(n, 0)
                    } else {
                        setImmediate(n)
                    }
                } else {
                    Ee.historyState = false
                }
                return se
            },
            clear_history_state: function() {
                ne = [];
                ee = [];
                return se
            },
            next: function() {
                if (Z.length() === 1) {
                    return se
                } else {
                    Z.front().disable();
                    var n = Z.rotate().enable();
                    var r = n.offset().top - 50;
                    e("html,body").animate({
                        scrollTop: r
                    }, 500);
                    try {
                        Ee.onTerminalChange.call(n, n)
                    } catch (t) {
                        y(t, "onTerminalChange")
                    }
                    return n
                }
            },
            focus: function(e, n) {
                be(function r() {
                    var r;
                    if (Z.length() === 1) {
                        if (e === false) {
                            try {
                                r = Ee.onBlur.call(se, se);
                                if (!n && r !== false || n) {
                                    se.disable()
                                }
                            } catch (t) {
                                y(t, "onBlur")
                            }
                        } else {
                            try {
                                r = Ee.onFocus.call(se, se);
                                if (!n && r !== false || n) {
                                    se.enable()
                                }
                            } catch (t) {
                                y(t, "onFocus")
                            }
                        }
                    } else if (e === false) {
                        se.next()
                    } else {
                        var i = Z.front();
                        if (i !== se) {
                            i.disable();
                            if (!n) {
                                try {
                                    Ee.onTerminalChange.call(se, se)
                                } catch (t) {
                                    y(t, "onTerminalChange")
                                }
                            }
                        }
                        Z.set(se);
                        se.enable()
                    }
                });
                return se
            },
            freeze: function(e) {
                we(function n() {
                    if (e) {
                        se.disable();
                        Le = true
                    } else {
                        Le = false;
                        se.enable()
                    }
                })
            },
            frozen: function() {
                return Le
            },
            enable: function() {
                if (!Fe && !Le) {
                    if (he === n) {
                        se.resize()
                    }
                    be(function e() {
                        Be.enable();
                        Fe = true
                    })
                }
                return se
            },
            disable: function() {
                be(function e() {
                    Fe = false;
                    Be.disable()
                });
                return se
            },
            enabled: function() {
                return Fe
            },
            signature: function() {
                var e = se.cols();
                var n;
                if (e < 15) {
                    n = null
                } else if (e < 35) {
                    n = 0
                } else if (e < 55) {
                    n = 1
                } else if (e < 64) {
                    n = 2
                } else if (e < 75) {
                    n = 3
                } else {
                    n = 4
                }
                if (n !== null) {
                    return V[n].join("\n") + "\n"
                } else {
                    return ""
                }
            },
            version: function() {
                return e.terminal.version
            },
            cmd: function() {
                return Be
            },
            get_command: function() {
                return Be.get()
            },
            set_command: function(e) {
                we(function n() {
                    Be.set(e)
                });
                return se
            },
            insert: function(e) {
                if (typeof e === "string") {
                    we(function n() {
                        var n = se.is_bottom();
                        Be.insert(e);
                        if (Ee.scrollOnEcho || n) {
                            _()
                        }
                    });
                    return se
                } else {
                    throw new Error(sprintf(Ae.notAString, "insert"))
                }
            },
            set_prompt: function(n) {
                we(function r() {
                    if (k("prompt", n)) {
                        if (e.isFunction(n)) {
                            Be.prompt(function(e) {
                                n(e, se)
                            })
                        } else {
                            Be.prompt(n)
                        }
                        De.top().prompt = n
                    }
                });
                return se
            },
            get_prompt: function() {
                return De.top().prompt
            },
            set_mask: function(e) {
                we(function n() {
                    Be.mask(e === true ? Ee.maskChar : e)
                });
                return se
            },
            get_output: function(n) {
                if (n) {
                    return ue
                } else {
                    return e.map(ue, function(n) {
                        return e.isFunction(n[0]) ? n[0]() : n[0]
                    }).join("\n")
                }
            },
            resize: function(n, r) {
                if (!se.is(":visible")) {
                    se.stopTime("resize");
                    se.oneTime(500, "resize", function() {
                        se.resize(n, r)
                    })
                } else {
                    if (n && r) {
                        se.width(n);
                        se.height(r)
                    }
                    n = se.width();
                    r = se.height();
                    var t = se.cols();
                    var i = se.rows();
                    if (t !== he || i !== ge) {
                        he = t;
                        ge = i;
                        E();
                        var o = De.top();
                        if (e.isFunction(o.resize)) {
                            o.resize(se)
                        } else if (e.isFunction(Ee.onResize)) {
                            Ee.onResize.call(se, se)
                        }
                        _()
                    }
                }
                return se
            },
            flush: function() {
                try {
                    var n = se.is_bottom();
                    var r;
                    e.each(x, function(n, t) {
                        if (t === T) {
                            r = e("<div></div>")
                        } else if (e.isFunction(t)) {
                            r.appendTo(pe);
                            try {
                                t(r)
                            } catch (i) {
                                y(i, "USER:echo(finalize)")
                            }
                        } else {
                            e("<div/>").html(t).appendTo(r).width("100%")
                        }
                    });
                    if (Ee.outputLimit >= 0) {
                        var t;
                        if (Ee.outputLimit === 0) {
                            t = se.rows()
                        } else {
                            t = Ee.outputLimit
                        }
                        var i = pe.find("div div");
                        if (i.length > t) {
                            var o = i.length - t + 1;
                            var a = i.slice(0, o);
                            var s = a.parent();
                            a.remove();
                            s.each(function() {
                                var n = e(this);
                                if (n.is(":empty")) {
                                    n.remove()
                                }
                            })
                        }
                    }
                    ge = M(se);
                    if (Ee.scrollOnEcho || n) {
                        _()
                    }
                    x = []
                } catch (l) {
                    if (e.isFunction(Ee.exceptionHandler)) {
                        Ee.exceptionHandler.call(se, l, "TERMINAL (Flush)")
                    } else {
                        alert("[Flush] " + v(l) + "\n" + l.stack)
                    }
                }
                return se
            },
            update: function(e, n) {
                we(function r() {
                    if (e < 0) {
                        e = ue.length + e
                    }
                    if (!ue[e]) {
                        se.error("Invalid line number " + e)
                    } else {
                        if (n === null) {
                            ue.splice(e, 1)
                        } else {
                            ue[e][0] = n
                        }
                        E()
                    }
                });
                return se
            },
            last_index: function() {
                return ue.length - 1
            },
            echo: function(n, r) {
                function t(n) {
                    try {
                        var t = e.extend({
                            flush: true,
                            raw: Ee.raw,
                            finalize: e.noop,
                            keepWords: false,
                            formatters: true
                        }, r || {});
                        if (t.flush) {
                            if (x.length) {
                                se.flush()
                            }
                            x = []
                        }
                        C(n, t);
                        ue.push([n, e.extend(t, {
                            exec: false
                        })]);
                        if (t.flush) {
                            se.flush()
                        }
                    } catch (i) {
                        if (e.isFunction(Ee.exceptionHandler)) {
                            Ee.exceptionHandler.call(se, i, "TERMINAL (echo)")
                        } else {
                            alert("[Terminal.echo] " + v(i) + "\n" + i.stack)
                        }
                    }
                }
                n = n || "";
                var i = e.type(n);
                if (i === "function" || i === "string") {
                    t(n)
                } else {
                    e.when(n).then(t)
                }
                return se
            },
            error: function(n, r) {
                r = e.extend({}, r, {
                    raw: false,
                    formatters: false
                });
                var t = e.terminal.escape_brackets(n).replace(/\\$/, "&#92;").replace(S, "]$1[[;;;error]");
                return se.echo("[[;;;error]" + t + "]", r)
            },
            exception: function(n, r) {
                var t = v(n);
                if (r) {
                    t = "&#91;" + r + "&#93;: " + t
                }
                if (t) {
                    se.error(t, {
                        finalize: function(e) {
                            e.addClass("exception message")
                        },
                        keepWords: true
                    })
                }
                if (typeof n.fileName === "string") {
                    se.pause(Ee.softPause);
                    e.get(n.fileName, function(e) {
                        var r = n.lineNumber - 1;
                        var t = e.split("\n")[r];
                        if (t) {
                            se.error("[" + n.lineNumber + "]: " + t)
                        }
                        se.resume()
                    }, "text")
                }
                if (n.stack) {
                    var i = e.terminal.escape_brackets(n.stack);
                    se.echo(i.split(/\n/g).map(function(e) {
                        return "[[;;;error]" + e.replace(S, function(e) {
                            return "]" + e + "[[;;;error]"
                        }) + "]"
                    }).join("\n"), {
                        finalize: function(e) {
                            e.addClass("exception stack-trace")
                        },
                        formatters: false
                    })
                }
            },
            scroll: function(e) {
                var n;
                e = Math.round(e);
                if (le.prop) {
                    if (e > le.prop("scrollTop") && e > 0) {
                        le.prop("scrollTop", 0)
                    }
                    n = le.prop("scrollTop");
                    le.scrollTop(n + e)
                } else {
                    if (e > le.attr("scrollTop") && e > 0) {
                        le.attr("scrollTop", 0)
                    }
                    n = le.attr("scrollTop");
                    le.scrollTop(n + e)
                }
                return se
            },
            logout: function(e) {
                if (ke) {
                    throw new Error(sprintf(Ae.notWhileLogin, "logout"))
                }
                we(function r() {
                    if (e) {
                        var r = ve.pop();
                        se.set_token(n, true);
                        se.login.apply(se, r)
                    } else if (De.size() === 1 && se.token()) {
                        se.logout(true)
                    } else {
                        while (De.size() > 1) {
                            if (se.token()) {
                                se.logout(true).pop().pop()
                            } else {
                                se.pop()
                            }
                        }
                    }
                });
                return se
            },
            token: function(e) {
                return Se.get(se.prefix_name(e) + "_token")
            },
            set_token: function(e, n) {
                var r = se.prefix_name(n) + "_token";
                if (typeof e === "undefined") {
                    Se.remove(r, e)
                } else {
                    Se.set(r, e)
                }
                return se
            },
            get_token: function(e) {
                return se.token(e)
            },
            login_name: function(e) {
                return Se.get(se.prefix_name(e) + "_login")
            },
            name: function() {
                return De.top().name
            },
            prefix_name: function(e) {
                var n = (Ee.name ? Ee.name + "_" : "") + me;
                if (e && De.size() > 1) {
                    var r = De.map(function(e) {
                        return e.name || ""
                    }).slice(1).join("_");
                    if (r) {
                        n += "_" + r
                    }
                }
                return n
            },
            read: function(n, r) {
                var t = new e.Deferred;
                se.push(function(n) {
                    se.pop();
                    if (e.isFunction(r)) {
                        r(n)
                    }
                    t.resolve(n)
                }, {
                    prompt: n
                });
                return t.promise()
            },
            push: function(r, t) {
                be(function i() {
                    t = t || {};
                    var i = {
                        infiniteLogin: false
                    };
                    var o = e.extend({}, i, t);
                    if (!o.name && fe) {
                        o.name = fe.name
                    }
                    if (o.prompt === n) {
                        o.prompt = (o.name || ">") + " "
                    }
                    var a = De.top();
                    if (a) {
                        a.mask = Be.mask()
                    }
                    var s = Oe;

                    function l() {
                        Ee.onPush.call(se, a, De.top(), se);
                        K()
                    }
                    h(r, !!t.login, function(n) {
                        De.push(e.extend({}, n, o));
                        if (o.completion === true) {
                            if (e.isArray(n.completion)) {
                                De.top().completion = n.completion
                            } else if (!n.completion) {
                                De.top().completion = false
                            }
                        }
                        if (o.login) {
                            var t;
                            var i = e.type(o.login);
                            if (i === "function") {
                                t = o.infiniteLogin ? e.noop : se.pop;
                                se.login(o.login, o.infiniteLogin, l, t)
                            } else if (e.type(r) === "string" && i === "string" || i === "boolean") {
                                t = o.infiniteLogin ? e.noop : se.pop;
                                se.login(d(r, o.login), o.infiniteLogin, l, t)
                            }
                        } else {
                            l()
                        }
                        if (!s && se.enabled()) {
                            se.resume()
                        }
                    })
                });
                return se
            },
            pop: function(r, t) {
                if (r !== n) {
                    O(r)
                }
                var i = se.token(true);
                var o;
                if (De.size() === 1) {
                    o = De.top();
                    if (Ee.login) {
                        H();
                        if (e.isFunction(Ee.onExit)) {
                            try {
                                Ee.onExit.call(se, se)
                            } catch (a) {
                                y(a, "onExit")
                            }
                        }
                    } else {
                        se.error(Ae.canExitError)
                    }
                    if (!t) {
                        Ee.onPop.call(se, o, null, se)
                    }
                } else {
                    if (i) {
                        D()
                    }
                    var s = De.pop();
                    o = De.top();
                    K();
                    if (!t) {
                        Ee.onPop.call(se, s, o)
                    }
                    if (ke && se.get_prompt() !== Ae.login + ": ") {
                        ke = false
                    }
                    if (e.isFunction(s.onExit)) {
                        try {
                            s.onExit.call(se, se)
                        } catch (a) {
                            y(a, "onExit")
                        }
                    }
                    se.set_mask(o.mask)
                }
                return se
            },
            option: function(n, r) {
                if (typeof r === "undefined") {
                    if (typeof n === "string") {
                        return Ee[n]
                    } else if (typeof n === "object") {
                        e.each(n, function(e, n) {
                            Ee[e] = n
                        })
                    }
                } else {
                    Ee[n] = r
                }
                return se
            },
            level: function() {
                return De.size()
            },
            reset: function() {
                we(function e() {
                    se.clear();
                    while (De.size() > 1) {
                        De.pop()
                    }
                    J()
                });
                return se
            },
            purge: function() {
                we(function n() {
                    var n = se.prefix_name() + "_";
                    var r = Se.get(n + "interpreters");
                    e.each(e.parseJSON(r), function(e, n) {
                        Se.remove(n + "_commands");
                        Se.remove(n + "_token");
                        Se.remove(n + "_login")
                    });
                    Be.purge();
                    Se.remove(n + "interpreters")
                });
                return se
            },
            destroy: function() {
                we(function n() {
                    Be.destroy().remove();
                    pe.remove();
                    je.remove();
                    e(document).unbind(".terminal_" + se.id());
                    e(window).unbind(".terminal_" + se.id());
                    se.unbind("click mousewheel mousedown mouseup");
                    se.removeData("terminal").removeClass("terminal");
                    if (Ee.width) {
                        se.css("width", "")
                    }
                    if (Ee.height) {
                        se.css("height", "")
                    }
                    e(window).off("blur", Ue).off("focus", Me);
                    Ie.remove();
                    Z.remove(me);
                    if (!Z.length()) {
                        e(window).off("hashchange")
                    }
                });
                return se
            },
            scroll_to_bottom: _,
            is_bottom: function() {
                if (Ee.scrollBottomOffset === -1) {
                    return false
                } else {
                    var n, r, t;
                    if (se.is("body")) {
                        n = e(document).height();
                        r = e(window).scrollTop();
                        t = window.innerHeight
                    } else {
                        n = le[0].scrollHeight;
                        r = le.scrollTop();
                        t = le.outerHeight()
                    }
                    var i = n - Ee.scrollBottomOffset;
                    return r + t > i
                }
            }
        }, function(e, n) {
            return function() {
                try {
                    return n.apply(se, [].slice.apply(arguments))
                } catch (r) {
                    if (e !== "exec" && e !== "resume") {
                        y(r, "TERMINAL")
                    }
                    throw r
                }
            }
        }));
        if (Ee.width) {
            se.width(Ee.width)
        }
        if (Ee.height) {
            se.height(Ee.height)
        }
        le = se.scroll_element();
        e(document).bind("ajaxSend.terminal_" + se.id(), function(e, n) {
            Q.push(n)
        });
        var je = e('<div class="terminal-wrapper"/>').appendTo(se);
        var Ie = e("<iframe/>").appendTo(je);
        pe = e("<div>").addClass("terminal-output").appendTo(je);
        se.addClass("terminal");
        if (Ee.login && e.isFunction(Ee.onBeforeLogin)) {
            try {
                if (Ee.onBeforeLogin.call(se, se) === false) {
                    Pe = false
                }
            } catch (Ne) {
                y(Ne, "onBeforeLogin");
                throw Ne
            }
        }
        var $e;
        if (typeof r === "string") {
            $e = r
        } else if (r instanceof Array) {
            for (var ze = 0, He = r.length; ze < He; ++ze) {
                if (typeof r[ze] === "string") {
                    $e = r[ze];
                    break
                }
            }
        }
        if ($e && (typeof Ee.login === "string" || Ee.login === true)) {
            Ee.login = d($e, Ee.login)
        }
        Z.append(se);
        var De;
        var Be;
        var We;

        function Me() {
            if (We) {
                se.focus()
            }
        }

        function Ue() {
            We = Fe;
            se.disable()
        }
        h(r, !!Ee.login, function(r) {
            if (Ee.completion && typeof Ee.completion !== "boolean" || !Ee.completion) {
                r.completion = "settings"
            }
            var t = e.extend({}, X, Ee.keymap || {});
            De = new g(e.extend({}, Ee.extra, {
                name: Ee.name,
                prompt: Ee.prompt,
                keypress: Ee.keypress,
                keydown: Ee.keydown,
                resize: Ee.onResize,
                greetings: Ee.greetings,
                mousewheel: Ee.mousewheel,
                keymap: t
            }, r));
            Be = e("<div/>").appendTo(je).cmd({
                prompt: Ee.prompt,
                history: Ee.memory ? "memory" : Ee.history,
                historyFilter: Ee.historyFilter,
                historySize: Ee.historySize,
                width: "100%",
                enabled: Fe && !w,
                keydown: oe,
                keymap: t,
                clickTimeout: Ee.clickTimeout,
                keypress: function(n) {
                    var r = De.top();
                    if (e.isFunction(r.keypress)) {
                        return r.keypress.call(se, n, se)
                    } else if (e.isFunction(Ee.keypress)) {
                        return Ee.keypress.call(se, n, se)
                    }
                },
                onCommandChange: function(n) {
                    if (e.isFunction(Ee.onCommandChange)) {
                        try {
                            Ee.onCommandChange.call(se, n, se)
                        } catch (r) {
                            y(r, "onCommandChange");
                            throw r
                        }
                    }
                    _()
                },
                commands: z
            });
            if (Fe && se.is(":visible") && !w) {
                se.focus(n, true)
            } else {
                se.disable()
            }
            se.oneTime(100, function() {
                function n(n) {
                    var r = e(n.target);
                    if (!r.closest(".terminal").length && se.enabled() && Ee.onBlur.call(se, se) !== false) {
                        se.disable()
                    }
                }
                e(document).bind("click.terminal_" + se.id(), n).bind("contextmenu.terminal_" + se.id(), n)
            });
            var i = e(window);
            if (!w) {
                i.on("focus.terminal_" + se.id(), Me).on("blur.terminal_" + se.id(), Ue)
            } else {}
            if (w) {
                se.click(function() {
                    if (!se.enabled() && !Le) {
                        se.focus();
                        Be.enable()
                    } else {
                        se.focus(false)
                    }
                })
            } else {
                (function() {
                    var n = 0;
                    var r = false;
                    var t;
                    se.mousedown(function(i) {
                        var o = e(i.target).parents();
                        if (o.addBack) {
                            t = o.addBack()
                        } else {
                            t = o.andSelf()
                        }
                        se.oneTime(1, function() {
                            e(window).on("mousemove.terminal_" + se.id(), function() {
                                r = true;
                                n = 0;
                                e(window).off("mousemove.terminal_" + se.id())
                            })
                        })
                    }).mouseup(function() {
                        var i = r;
                        r = false;
                        e(window).off("mousemove.terminal_" + se.id());
                        if (!i) {
                            if (++n === 1) {
                                if (!se.enabled() && !Le) {
                                    se.focus();
                                    Be.enable()
                                }
                                var o = "click_" + se.id();
                                se.oneTime(Ee.clickTimeout, o, function() {
                                    if (!t.is(".terminal-output") && !t.is(".cmd") && t.is(".terminal > div")) {
                                        Be.position(Be.get().length)
                                    }
                                    n = 0
                                })
                            } else {
                                se.stopTime("click_" + se.id());
                                n = 0
                            }
                        }
                    }).dblclick(function() {
                        n = 0;
                        se.stopTime("click_" + se.id())
                    })
                })()
            }
            se.delegate(".exception a", "click", function(n) {
                var r = e(this).attr("href");
                if (r.match(/:[0-9]+$/)) {
                    n.preventDefault();
                    l(r)
                }
            });
            se.mousedown(function(e) {
                if (e.which === 2) {
                    var n = U();
                    se.insert(n)
                }
            });
            if (se.is(":visible")) {
                he = se.cols();
                Be.resize(he);
                ge = M(se)
            }
            ye.resolve();
            if (Ee.login) {
                se.login(Ee.login, true, J)
            } else {
                J()
            }

            function o() {
                if (se.is(":visible")) {
                    var e = se.width();
                    var n = se.height();
                    if (Re !== n || Te !== e) {
                        se.resize()
                    }
                    Re = n;
                    Te = e
                }
            }
            se.oneTime(100, function() {
                function e() {
                    Ie[0].contentWindow.onresize = o
                }
                if (Ie.is(":visible")) {
                    e()
                } else {
                    Ie.on("load", e)
                }
            });

            function a(n) {
                var r = Z.get()[n[0]];
                if (r && me === r.id()) {
                    if (n[2]) {
                        try {
                            if (Oe) {
                                var t = e.Deferred();
                                $.push(function() {
                                    return r.exec(n[2]).then(function() {
                                        r.save_state(n[2], true, n[1]);
                                        t.resolve()
                                    })
                                });
                                return t.promise()
                            } else {
                                return r.exec(n[2]).then(function() {
                                    r.save_state(n[2], true, n[1])
                                })
                            }
                        } catch (i) {
                            var o = r.settings();
                            if (e.isFunction(o.exceptionHandler)) {
                                o.exceptionHandler.call(se, i, "EXEC HASH")
                            } else {
                                var a = e.terminal.escape_brackets(de);
                                var s = "Error while exec with command " + a;
                                r.error(s).exception(i)
                            }
                        }
                    }
                }
            }
            if (Ee.execHash) {
                if (location.hash) {
                    setTimeout(function() {
                        try {
                            var n = location.hash.replace(/^#/, "");
                            ne = e.parseJSON(decodeURIComponent(n));
                            var r = 0;
                            (function i() {
                                var e = ne[r++];
                                if (e) {
                                    a(e).then(i)
                                } else {
                                    re = true
                                }
                            })()
                        } catch (t) {}
                    })
                } else {
                    re = true
                }
            } else {
                re = true
            }
            if (e.event.special.mousewheel) {
                var s = false;
                e(document).bind("keydown.terminal_" + se.id(), function(e) {
                    if (e.shiftKey) {
                        s = true
                    }
                }).bind("keyup.terminal_" + se.id(), function(e) {
                    if (e.shiftKey || e.which === 16) {
                        s = false
                    }
                });
                se.mousewheel(function(n, r) {
                    if (!s) {
                        var t = De.top();
                        var i;
                        if (e.isFunction(t.mousewheel)) {
                            i = t.mousewheel(n, r, se);
                            if (i === false) {
                                return
                            }
                        } else if (e.isFunction(Ee.mousewheel)) {
                            i = Ee.mousewheel(n, r, se);
                            if (i === false) {
                                return
                            }
                        }
                        if (r > 0) {
                            se.scroll(-40)
                        } else {
                            se.scroll(40)
                        }
                    }
                })
            }
        });
        se.data("terminal", se);
        return se
    }
})(jQuery);