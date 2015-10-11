import sdl2.ext
from tetris.configuration.Configuration import *
from tetris.configuration.Colors import *


class MenuState(object):
    def __init__(self):
        self.selected_index = None
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
        if self.selected_index is None:
            self.selected_index = 0

    def next_button(self):
        self.selected_index = (((self.selected_index + 1) % len(self.buttons)) + len(self.buttons)) % len(self.buttons)

    def previous_button(self):
        self.selected_index = (((self.selected_index - 1) % len(self.buttons)) + len(self.buttons)) % len(self.buttons)


class LabelState(object):
    def __init__(self, display_text, text_size, text_color):
        self.display_text = display_text
        self.text_size = text_size
        self.text_color = text_color


class ButtonState(object):
    def __init__(self, display_text, text_size, unselected_color, selected_color, next_state_class):
        self.display_text = display_text
        self.text_size = text_size
        self.unselected_color = unselected_color
        self.selected_color = selected_color
        self.next_state_class = next_state_class


class MenuLabel(sdl2.ext.Entity):
    def __init__(self, world, label_state, pos=(0, 0)):
        self.labelstate = label_state
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        font_manager = sdl2.ext.FontManager(font_path=font_path(), size=label_state.text_size, color=label_state.text_color)
        self.sprite = factory.from_text(label_state.display_text, fontmanager=font_manager)
        self.sprite.position = pos


class MenuButton(sdl2.ext.Entity):
    def __init__(self, world, button_state, pos=(0,0)):
        self.buttonstate = button_state

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        font_manager = sdl2.ext.FontManager(font_path=font_path(), size=button_state.text_size, color=button_state.unselected_color)
        self.sprite = factory.from_text(button_state.display_text, fontmanager=font_manager)
        self.sprite.position = pos


class TitleSprite(MenuLabel):
    def __init__(self, world):
        super(TitleSprite, self).__init__(world, LabelState("Pytris", 30, WHITE))
        self.sprite.position = (window_width()/2 - self.sprite.area[2]/2, 30)



