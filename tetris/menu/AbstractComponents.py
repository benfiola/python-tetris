from tetris.AbstractComponents import *
from tetris.menu.AbstractEntities import *

class MenuComponent(Component):
    def __init__(self, window, world):
        super(MenuComponent, self).__init__(window, world)
        self.title_sprite = TitleSprite(self.world)

    def prepare(self):
        pass

    def post_process(self):
        pass

    def handle_event(self, event):
        pass
