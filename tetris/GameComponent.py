from GameSystems import *
from TetrisComponent import *
import MenuComponent

class Game(Component):
    def __init__(self, window, world):
        super(Game, self).__init__(window, world)
        self.game_board = GameBoard()
        self.end_game_condition = EndGameCondition(self.world, self.game_board)
        self.generator = Generator(self.world, self.game_board)
        self.current_piece = self.generator.create_piece()

    def prepare(self):
        self.world.add_system(MovementSystem())
        self.world.add_system(LineClearSystem())
        self.world.add_system(AudioSystem())
        self.world.add_system(BlockSpriteUpdateSystem())
        self.world.add_system(EndGameSystem())
        self.world.add_system(GameRenderer(self.window))

    def post_process(self):
        if self.current_piece.movementstate.locked and self.end_game_condition.gamestate.game_over is not True:
            self.current_piece.delete()
            self.current_piece = self.generator.create_piece()
        elif self.end_game_condition.gamestate.game_over is True:
            print "Game over"

    def handle_event(self, event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_DOWN:
                self.current_piece.movementinput.soft_drop = True
            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                self.current_piece.movementinput.move_right = True
            elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                self.current_piece.movementinput.move_left = True
            elif event.key.keysym.sym == sdl2.SDLK_SPACE:
                self.current_piece.movementinput.hard_drop = True
            elif event.key.keysym.sym == sdl2.SDLK_z:
                self.current_piece.movementinput.rotate_ccw = True
            elif event.key.keysym.sym == sdl2.SDLK_x:
                self.current_piece.movementinput.rotate_cw = True
            elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                self.handing_off = True
                self.next_state_class = MenuComponent.Menu
