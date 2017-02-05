__author__ = 'antonellacalvia'

from TopCompiler import topc
from TopCompiler import CodegenJS
from TopCompiler import Error

import sys
import logging
import os
import time

def main():
    error = False
    while True:
        try:
            parser = topc.start(run= True, dev=True)
            time.sleep(0.2)
            error = False
            break
        except EOFError as e:
            if not error:
                print(e, file=sys.stderr)
            error = True
            time.sleep(0.2)

    while True:
        time.sleep(0.2)
        try:
            parser = topc.start(run= False, dev= True, hotswap= True, cache=parser)
            error = False
        except EOFError as e:
            if not error:
                print(e, file=sys.stderr)
            error = True
if __name__ == '__main__':
    main()