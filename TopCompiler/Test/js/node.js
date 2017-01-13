var main_fs = require("fs");
var http = require("http");

function server_readFile(f,next) {
    main_fs.readFile(f,function(e,res){
        if(e){
            next([1])
        } else {
            next([0,res])
        }
    })
}

function _http_get(url, next) {
    http.get({path: url}, next);
}

function server_createServer(func) {
    return http.createServer(function (req, res) {
        func(req, function (_res) {
            res.writeHead(_res.status, {'Content-Type': _res.contentType});
            res.end(_res.body, _res.encoding);
        })
    })
}

function server_handleQuery(url, func, next) {
        var req = url.slice(url.indexOf("/", 2)+1);
        req = JSON.parse(req);
        req[req.length-1] = function (res) {
            return {
                body: JSON.stringify(res),
                status: 200,
                contentType: "text",
            }
        };

        func(req, next);
}

function server_isQuery(url) {
    return url.slice(1, url.indexOf("/", 2)) === "query"
}