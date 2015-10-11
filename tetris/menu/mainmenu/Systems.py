import sdl2.ext

from tetris.menu.AbstractSystems import *
from tetris.menu.AbstractEntities import *
from tetris.menu.mainmenu.Entities import *

class MainMenuRenderer(MenuRenderer):
    def __init__(self, window):
        super(MenuRenderer, self).__init__(window)


class ButtonUpdateSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(ButtonUpdateSystem, self).__init__()
        self.componenttypes = MenuState, TestBag

    def process(self, world, componentsets):
        for menu_state, testbag in componentsets:
            for button in menu_state.buttons:
                color = button.buttonstate.unselected_color
                if menu_state.selected_index is not None and menu_state.buttons[menu_state.selected_index] == button :
                    color = button.buttonstate.selected_color
                factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
                font_manager = sdl2.ext.FontManager(font_path=font_path(), size=button.buttonstate.text_size, color=color)
                old_pos = button.sprite.position
                button.sprite = factory.from_text(button.buttonstate.display_text, fontmanager=font_manager)
                button.sprite.position = old_pos
