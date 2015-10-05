import sdl2.ext
from Configuration import *
import Colors
import os

FONT_PATH = os.path.join(os.environ["windir"],"Fonts","Arial.ttf")
class TitleSprite(sdl2.ext.Entity):
    def __init__(self, world):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        font_manager = sdl2.ext.FontManager(font_path=FONT_PATH, size=30, color=Colors.WHITE)
        self.sprite = factory.from_text("Pytris",fontmanager=font_manager)
        self.sprite.position = (window_width()/2 - self.sprite.area[2]/2, 30)


class PressEnterToContinueSprite(sdl2.ext.Entity):
    def __init__(self, world):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        font_manager = sdl2.ext.FontManager(font_path=FONT_PATH, size = 16, color=Colors.BLACK)
        self.sprite = factory.from_text("Press Enter to Continue",fontmanager=font_manager)
        self.sprite.position = (window_width()/2 - self.sprite.area[2]/2, window_height()/2 - self.sprite.area[3]/2)
