__author__ = 'antonellacalvia'

from TopCompiler import topc
from TopCompiler import CodegenJS

import sys
import logging
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#sys.stderr = open(os.devnull, "w")

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
        <style>
            .error {
                font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace, serif;
                background-color: lightblue;
                position: fixed; bottom: 0; margin: 0; width: 100%;
                padding-top: 10px; padding-left: 30px;
            }
        </style>
    </HEAD>
    <BODY>
        <div id= "code"></div>
        <div id= "error"></div>
    </BODY>
    <script>"""+jQuery+"""</script>
    <script>
        var received = false;
        function update(){
            $.getScript("//127.0.0.1:"""+str(port)+"""/js/"+received.toString()+","+error.toString()).done(function (value, status, jqxhr){
                received = true;
                if (value !== "" && !error && ended) {
                    document.getElementById("error").innerHTML = "";
                    //console.log("reset");
                    //main_Init();
                }
                setTimeout(update, 500);
            }).fail(function (handler) {
                received = false;
                setTimeout(update, 500);
            })
        };
        update();
    </script>
    <script id= "js">"""+compile()+"""</script>
</HTML>"""

@app.route("/js/<received>,<error>", methods=["get", "post"])
def hot(received, error):
    error = error == "true"
    i = topc.start(False, dev= True, init= received == "false", hotswap= not error)
    topc.error = ""

    if i[0]:
        #print("resetting")
        return "error= false;\n"+i[1]+ "ended=true;\nmain_Init();\n"

    if i[1] == "":
        #print("not ressetting")
        return ""
    return """var error= true; document.getElementById("error").innerHTML = " """+i[1] + """ ";\n"""

def compile():
    print("initing")
    i = topc.start(False, dev= True, init= True, hotswap= False)
    topc.error = ""
    if i[0]:
        return "var ended= false;var error= false;\n"+i[1]+";\nmain_Init();ended=true; main_Init()\n"

    return """var error= true; document.getElementById("error").innerHTML = " """+i[1] + """ ";"""

if __name__ == '__main__':
    app.run(port= port)