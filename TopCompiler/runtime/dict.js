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
}