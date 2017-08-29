from flask import Flask, request
from TopCompiler import Parser
from TopCompiler import PackageParser
from TopCompiler import Lexer
from TopCompiler import ResolveSymbols
from TopCompiler import topc
from TopCompiler import ImportParser
from TopCompiler import CodeGen
import AST as Tree
import tempfile

import os

app = Flask(__name__)


@app.route("/toHTML", methods=["POST"])
def compile():
    code = request.data.decode("utf-8")

    if code == "":
        return ""

    try:
        object = tempfile.TemporaryDirectory(dir= "temps")
        id = object.name
        os.chdir(id)
        os.mkdir("src")
        os.mkdir("src/main")
        os.mkdir("bin")

        ignore = {}
        for item in os.listdir("../../src"):
            if not item in ["main", "port.json"]:
                ignore[item] = True
                os.symlink("../../../src/"+item, "src/"+item, target_is_directory=True)
        os.symlink("../../js", "js")
        os.symlink("../../lib", "lib")

        jsonFile = open("src/port.json", "w")
        json = """
        {
            "name": "code",
            "target": "client",
            "linkWith-client": ["js/exports.js", "js/bundle.js"],
            "linkWith-node": ["js/node.js"]
        }
        """

        jsonFile.write(json)
        jsonFile.close()

        jsonMainFile = open("src/main/port.json", "w")
        jsonMain = """
        {
            "files": ["anonymous"]
        }
        """

        jsonMainFile.write(jsonMain)
        jsonMainFile.close()

        anonymous = open("src/main/anonymous.top", "w")
        anonymous.write(code)
        anonymous.close()

        try:
            topc.modified_ = {"main": True}
            ImportParser.ignore = ignore
            topc.start(cache= core, _raise=True, _hotswap=True)

            res = open("bin/code.html", mode="r").read()
            os.chdir("../../")

            return res
        except EOFError as e:
            os.chdir("../../")
            return str(e).replace("\n", "<br>")
    except Exception as e:
        os.chdir("../../")
        raise e

if __name__ == "__main__":
    topc._modified = {"main": True}
    core = topc.start(_raise= True)
    app.run(port=8080)