__author__ = 'antonellacalvia'

from .node import *

class Cast(Node):
    def __init__(self, f, to, owner=None):
        Node.__init__(self, owner)
        self.f = f
        self.to = to

    def __str__(self):
        return self.f + " to " + self.to
