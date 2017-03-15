# virtual-hyperscript-svg

create virtual-dom nodes for svg using hyperscript syntax

# example

svg.js:

``` js
var h = require('virtual-hyperscript-svg');

module.exports = function () {
    return h('svg', { width: 400, height: 300 }, [
        h('circle', { fill: 'lime', cx: 100, cy: 250, r: 20 }),
        h('rect', { fill: 'red', x: 50, y: 50, width: 300, height: 100 })
    ]);
};
```

then you can use `virtual-dom-stringify` to render some html strings from node:

```
var str = require('virtual-dom-stringify');
var svg = require('./svg.js')();
console.log(str(svg));
```

```
$ node str.js
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><circle fill="lime" cx="100" cy="250" r="20"></circle><rect fill="red" x="50" y="50" width="300" height="100"></rect></svg>
```

or use use `virtual-dom/create-element` browser-side:

``` js
var createElement = require('virtual-dom/create-element');
var svg = require('./svg.js')();
document.body.appendChild(createElement(svg));
```

# methods

``` js
var h = require('virtual-hyperscript-svg')
```

## var tree = h(name, props={}, children)

Create a virtual-dom `tree` for a tag name/selector, some properties, and an
array of `children`.

Implicitly, the svg namespace (http://www.w3.org/2000/svg) is used and all
properties are treated as attributes.

# install

With [npm](https://npmjs.org) do:

```
npm install virtual-hyperscript-svg
```

# license

MIT
