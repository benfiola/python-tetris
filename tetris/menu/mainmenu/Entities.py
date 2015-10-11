import os

import sdl2.ext
from tetris.menu.AbstractEntities import *
from tetris.configuration.Configuration import *
from tetris.configuration.Colors import *
import tetris.game.GameComponent
import tetris.exit.ExitComponent


class GameButton(MenuButton):
    def __init__(self, world):
        super(GameButton, self).__init__(world, ButtonState("Start", 14, WHITE, BLACK, tetris.game.GameComponent.Game))

        #assuming our title sprite is 60 - 30 + 30
        self.sprite.position = (window_width()/2 - self.sprite.area[2]/2, window_height()/2)


class ExitButton(MenuButton):
    def __init__(self, world):
        super(ExitButton, self).__init__(world, ButtonState("Exit", 14, WHITE, BLACK, tetris.exit.ExitComponent.Exit))
        self.sprite.position = (window_width()/2 - self.sprite.area[2]/2, window_height()/2 + 28)

class TestBag(object):
    def __init__(self):
        pass


class MenuEntity(sdl2.ext.Entity):
    def __init__(self, world):
        self.menustate = MenuState()
        self.testbag = TestBag()

        self.menustate.add_button(GameButton(world))
        self.menustate.add_button(ExitButton(world))






