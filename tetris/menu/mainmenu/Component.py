from tetris.menu.AbstractComponents import *
from tetris.menu.AbstractEntities import *
from Systems import *
from Entities import *
from tetris.game import GameComponent


class Menu(MenuComponent):
    def __init__(self, window, world):
        super(Menu, self).__init__(window, world)
        self.entity = MenuEntity(world)

    def prepare(self):
        self.world.add_system(MainMenuRenderer(self.window))
        self.world.add_system(ButtonUpdateSystem())

    def post_process(self):
        pass

    def handle_event(self, event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_RETURN:
                menu_state = self.entity.menustate
                if menu_state.selected_index is not None:
                    self.handing_off = True
                    self.next_state_class = menu_state.buttons[menu_state.selected_index].buttonstate.next_state_class
            if event.key.keysym.sym == sdl2.SDLK_UP:
                self.entity.menustate.next_button()
            if event.key.keysym.sym == sdl2.SDLK_DOWN:
                self.entity.menustate.next_button()

