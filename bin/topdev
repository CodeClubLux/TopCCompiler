__author__ = 'antonellacalvia'

from TopCompiler import topc
from TopCompiler import CodegenJS
from TopCompiler import Error

import sys
import logging
import os
import time

def main():
    error = ""
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

    while True:
        time.sleep(0.2)
        try:
            parser = topc.start(run= False, dev= True, hotswap= True, cache=parser)
            error = False
        except EOFError as e:
            e = str(e)
            if error != e:
                print(e, file=sys.stderr)
            error = e

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        import os
        os.remove("lib/main-node.js")