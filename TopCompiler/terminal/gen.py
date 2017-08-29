string = ""

"""
<head>
    <link rel="stylesheet" type="text/css" href="terminal.css">
    <script type="text/javascript" src="https:/cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="terminal.js"></script>
    <script src="../TopCompiler/runtime.js"></script>
</head>
"""

string += "<style>"+open("../terminal.css").read()+"</style>"
string += '<script type="text/javascript" src="https:/cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>'
string += "<script>" + open(__name__+"terminal.js").read() + "</script>"
string += "<script>" + open(__name__+"../TopCompiler/runtime.js").read() + "</script>"

d = "<head>" + string + "</head><body>"

