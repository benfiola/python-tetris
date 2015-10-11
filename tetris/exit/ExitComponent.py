from tetris.AbstractComponents import *
import sys


class Exit(Component):
    def __init__(self, window, world):
        super(Exit, self).__init__(window, world)

    def prepare(self):
        sys.exit(0)

    def post_process(self):
        pass

    def handle_event(self, event):
        pass
