from .EscapeAnalysis import *

#Memory Scope
BlockScoped = 0
Return = 1
Frame = 2
ThreadLocal = 3
Global = 4



def escapePass(parser, ast):
    pass