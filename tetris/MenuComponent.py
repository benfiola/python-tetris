from TetrisComponent import *
from MenuSystems import *
from MenuEntities import *
import GameComponent

class Menu(Component):
    def __init__(self, window, world):
        super(Menu, self).__init__(window, world)
        self.title_sprite = TitleSprite(self.world)
        self.enter_sprite = PressEnterToContinueSprite(self.world)

    def prepare(self):
        self.world.add_system(MenuRenderer(self.window))

    def post_process(self):
        pass

    def handle_event(self, event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_RETURN:
                self.handing_off = True
                self.next_state_class = GameComponent.Game

