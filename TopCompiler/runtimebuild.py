__author__ = 'antonellacalvia'

import requests

url = 'https://javascript-minifier.com/raw'

files = ["dom.js", "number.js", "utility.js", "list.js", "vector.js"]

filesC = [open("runtime/"+i, "r").read() for i in files]

content = "\n".join(filesC)
contentTest = "\n".join(filesC[1:])+"\n"+open("runtime/test.js", "r" ).read()+"""
function assert(condition) {
    if (!condition) {
        throw new Error("Assertion failed");
    }
}

function assertEq(value, shouldBe) {
    if (!value.operator_eq(shouldBe)){
        throw new Error("Expecting result to be: "+shouldBe+",\\n not "+value);
    }
}
"""

data = {'input': content}

response = requests.post(url, data=data)

runtime = open("runtime.js", "w")
runtime.write(response.text)
runtime.close()

test = open("runtime/tmp.js", "w")
test.write(contentTest)
test.close()

import subprocess
subprocess.call(["node", "runtime/tmp.js"])
