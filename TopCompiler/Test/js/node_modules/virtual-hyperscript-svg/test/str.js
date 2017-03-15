var test = require('tape');
var str = require('virtual-dom-stringify');
var h = require('../');

var expected = '<svg xmlns="http://www.w3.org/2000/svg" width="400" '
+ 'height="300"><circle fill="lime" cx="100" cy="250" r="20"></circle>'
+ '<rect fill="red" x="50" y="50" width="300" height="100"></rect></svg>';

test('str', function (t) {
    t.plan(1);
    var svg = h('svg', { width: 400, height: 300 }, [
        h('circle', { fill: 'lime', cx: 100, cy: 250, r: 20 }),
        h('rect', { fill: 'red', x: 50, y: 50, width: 300, height: 100 })
    ]);
    t.equal(str(svg), expected);
});
