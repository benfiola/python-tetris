import PreInit
from Configuration import *
import sys
import sdl2
import sdl2.ext
from MenuComponent import Menu

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Tetris", size=(window_width(), window_height()))
    world = sdl2.ext.World()
    window.show()
    curr = Menu(window, world)
    curr.prepare()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            curr.handle_event(event)
        curr.world.process()
        curr.post_process()
        if curr.handing_off is True:
            curr = curr.hand_off()
    return 0

if __name__ == "__main__":
    sys.exit(run())

