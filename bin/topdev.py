__author__ = 'antonellacalvia'

from TopCompiler import topc
from TopCompiler import CodegenJS
from TopCompiler import Error

import sys
import logging
import os
import time
import socketRepl
import threading

mutex = threading.Lock()

def main():
    error = ""
    mutex.acquire()
    while True:
        try:
            parser = topc.start(run= True, dev=True)
            time.sleep(0.2)
            error = False
            break
        except EOFError as e:
            e = str(e)
            if error != e:
                print(e, file=sys.stderr)
            error = e
            time.sleep(0.2)

    mutex.release()

    socketRepl.init()
    socketRepl.parser = parser

    server = threading.Thread(target=initRepl).start()

    while True:
        time.sleep(0.2)
        mutex.acquire()
        try:
            parser = topc.start(run= False, dev= True, hotswap= True, cache=parser)
            if parser.didCompile:
                socketRepl.socketio.emit("reload", open("bin/"+parser.outputFile+"-client.js").read())
            error = False
        except EOFError as e:
            e = str(e)
            if error != e:
                print(e, file=sys.stderr)
                #socketRepl.socketio.emit("error", "Compile Error\n\n"+str(e))
                socketRepl.socketio.emit("comp_error", str(e).replace("\t", "    ").replace(" ", "&nbsp;").replace("\n", "<br>"))
            error = e
        finally:
            mutex.release()

def initRepl():
    socketRepl.lock = mutex
    socketRepl.socketio.run(socketRepl.app, port=9000)

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        import os
        os.remove("lib/main-node.js")