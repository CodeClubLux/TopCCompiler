__author__ = 'antonellacalvia'

from TopCompiler import topc
from TopCompiler import CodegenJS

import sys
import logging
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from flask import Flask
app = Flask(__name__)

file = CodegenJS.__file__

jquery = file[0:file.rfind("/")+1] + "jquery.js"
file = open(jquery, "r")
jQuery = file.read()
file.close()


port = (3030 if len(sys.argv) == 1 else int(sys.argv[1]))
@app.route('/')
def initial():
    return """
<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML>
    <HEAD>
        <meta charset="UTF-8">
    </HEAD>
    <BODY>
        <div id= "code"></div>
        <div id= "error"></div>
    </BODY>
    <script>"""+jQuery+"""</script>
    <script>
        var received = false;
        function update(){
            $.getScript("//127.0.0.1:"""+str(port)+"""/js/\"+received.toString()).done(function (value, status, jqxhr){
                received = true;
                if (value !== "" && !error && ended) {
                    code.innerHTML = "";
                    document.getElementById("error").innerHTML = "";
                    main_Init();
                    received = false;
                }
                setTimeout(update, 200);
            }).fail(function (handler) {
                received = false;
                setTimeout(update, 200);
            })
        };
        update();
    </script>
    <script id= "js">"""+compile()+"""</script>
</HTML>"""

@app.route("/js/<received>", methods=["get", "post"])
def hot(received):
    i = topc.start(False, dev= True, init= received == "false")

    if i[0]:
        return "error= false;\n"+i[1]+ "ended=true;\n"

    if i[1] == "":
        return ""
    return """var error= true; document.getElementById("error").innerHTML = " """+i[1] + """ ";"""

def compile():
    i = topc.start(False, dev= True, init= True)
    if i[0]:
        return "var ended= false;var error= false;\n"+i[1]+";\nmain_Init();ended=true;"

    return """var error= true; document.getElementById("error").innerHTML = " """+i[1] + """ ";"""

if __name__ == '__main__':
    app.run(port= port)