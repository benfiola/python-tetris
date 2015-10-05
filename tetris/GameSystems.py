import sdl2.ext
import datetime
import random
from Configuration import *
import Colors
from GameEntities import *
from sdl2 import *
from sdl2.ext import Resources
from sdl2.ext.compat import byteify
from sdl2.sdlmixer import *


class GameRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(GameRenderer, self).__init__(window)

    def render(self, components, x=None, y=None):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(GameRenderer, self).render(components)


class BlockSpriteUpdateSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(BlockSpriteUpdateSystem, self).__init__()
        self.componenttypes = BoardCoordinates, sdl2.ext.Sprite

    def process(self, world, componentsets):
        block_height = window_height()/(num_rows())
        block_width = window_width()/num_columns()
        for board_coordinates, sprite in componentsets:
            posx = board_coordinates.pos[0] * block_width
            posy = (board_coordinates.pos[1] - 2) * block_height
            sprite.position = (posx, posy)

class AudioSystem(sdl2.ext.Applicator) :
    def __init__(self):
        super(AudioSystem, self).__init__()
        self.resources = "C:\\Users\\Ben\\PycharmProjects\\TetrisDemo\\resources\\"
        SDL_Init(SDL_INIT_AUDIO)
        Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024)
        soft_drop_file = self.resources + "soft-drop.wav"
        line_clear_file = self.resources + "line-clear.wav"
        self.soft_drop_sample = Mix_LoadWAV(byteify(soft_drop_file, "utf-8"))
        self.line_clear_sample = Mix_LoadWAV(byteify(line_clear_file, "utf-8"))
        self.componenttypes = MovementInput, AudioState

    def process(self, world, componentsets):
        for movement_input, audio_state in componentsets:
            if audio_state.play_soft_drop is True:
                Mix_PlayChannel(-1, self.soft_drop_sample, 0)
            if audio_state.play_line_clear is True:
                Mix_PlayChannel(-1, self.line_clear_sample, 0)
            audio_state.reset()


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(MovementSystem, self).__init__()
        self.componenttypes = MovementInput, MovementState, BlockCollection, GameBoard, AudioState
        self.last_drop = datetime.datetime.now()
        self.drop_timer = 500*1000

    def process(self, world, componentsets):
        curr_time = datetime.datetime.now()
        for movement_input, movement_state, block_collection, game_board, audio_state in componentsets:
            if movement_input.rotate_cw and self.check_rotate(game_board, block_collection):
                self.rotate(block_collection)
            if movement_input.rotate_ccw and self.check_rotate(game_board, block_collection, True):
                self.rotate(block_collection, True)
            if movement_input.soft_drop and self.check_move(game_board, block_collection, (0, 1)):
                self.last_drop = curr_time
                audio_state.play_soft_drop = True
                self.move(block_collection, (0, 1))
            if movement_input.move_left and self.check_move(game_board, block_collection, (-1, 0)):
                self.move(block_collection, (-1, 0))
            if movement_input.move_right and self.check_move(game_board, block_collection, (1, 0)):
                self.move(block_collection, (1, 0))
            if movement_input.hard_drop:
                while self.check_move(game_board, block_collection, (0, 1)):
                    self.move(block_collection, (0, 1))
                    movement_state.locked = True
            movement_input.reset()
            if (curr_time - self.last_drop).microseconds > self.drop_timer:
                self.last_drop = curr_time
                if self.check_move(game_board, block_collection, (0, 1)):
                    self.move(block_collection, (0, 1))
                else:
                    movement_state.locked = True

            if movement_state.locked is True:
                for block in block_collection.blocks:
                    game_board.board[block.boardcoordinates.pos[1]][block.boardcoordinates.pos[0]] = block

    def check_rotate(self, game_board, block_collection, ccw=False):
        for block in block_collection.blocks:
            coords = block.boardcoordinates.get_cw_coordinates()
            if ccw is True:
                coords = block.boardcoordinates.get_ccw_coordinates()

            if self.is_pos_valid(game_board, coords) is False:
                return False
        return True


    def rotate(self, block_collection, ccw=False):
        for block in block_collection.blocks:
            coords = block.boardcoordinates.get_cw_coordinates()
            offset = block.boardcoordinates.get_cw_offset()
            if ccw is True:
                coords = block.boardcoordinates.get_ccw_coordinates()
                offset = block.boardcoordinates.get_ccw_offset()

            block.boardcoordinates.pos = (coords[0], coords[1])
            block.boardcoordinates.offset = offset

    def is_pos_valid(self, game_board, pos):
        if pos[0] < 0 or pos[0] >= num_columns() or pos[1] < 0 or pos[1] >= (num_rows()+2) or game_board.board[pos[1]][pos[0]] is not None:
            return False
        return True

    def check_move(self, game_board, block_collection, position_modifier):
        for block in block_collection.blocks:
            check_y = block.boardcoordinates.pos[1] + position_modifier[1]
            check_x = block.boardcoordinates.pos[0] + position_modifier[0]
            if self.is_pos_valid(game_board, (check_x, check_y)) is False:
                return False
        return True

    def move(self, block_collection, position_modifier):
        for block in block_collection.blocks:
            block.boardcoordinates.pos = (block.boardcoordinates.pos[0] + position_modifier[0], block.boardcoordinates.pos[1] + position_modifier[1])


class LineClearSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(LineClearSystem, self).__init__()
        self.componenttypes = MovementState, BlockCollection, GameBoard, AudioState

    def process(self, world, componentsets):
        for movement_state, block_collection, game_board, audio_state in componentsets:
            #if we've locked the block we're controlling, we might need to clear lines
            if movement_state.locked:
                row_dict = {}
                line_cleared = False

                # for each block in our collection of controlled blocks, if an entire row is full, it needs
                # to be cleared.  these will be marked True in the row_dict
                for block in block_collection.blocks:
                    row = block.boardcoordinates.pos[1]
                    if row not in row_dict:
                        row_dict[row] = True
                        for space in game_board.board[row]:
                            if space is None:
                                row_dict[row] = False
                                break


                # we want to clear them from top to bottom.
                for row in sorted(row_dict.keys()):
                    # if we need to clear this row
                    if row_dict[row] is True:
                        line_cleared = True
                        # delete all entities in the row thats being cleared
                        for space in game_board.board[row]:
                            space.delete()

                        # shuffle the rest of the rows down one starting from the row above the one
                        # that was just cleared
                        for y in range(row-1, -1, -1):
                            # we're going from left to right
                            for x in range(0, len(game_board.board[y])):
                                space = game_board.board[y][x]

                                # if there's an entity in this space,
                                # adjust its block coordinates (these are used for rendering)
                                if space is not None:
                                    space.boardcoordinates.pos = (space.boardcoordinates.pos[0], space.boardcoordinates.pos[1]+1)

                                # set the old location to None, set the new location to the block
                                game_board.board[y][x] = None
                                game_board.board[y+1][x] = space

                if line_cleared is True:
                    audio_state.play_line_clear = True


class EndGameSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(EndGameSystem, self).__init__()
        self.componenttypes = GameState, GameBoard

    def process(self, world, componentsets):
        for game_state, game_board in componentsets:
            for row in range(0,2):
                for space in game_board.board[row]:
                    if space is not None:
                        game_state.game_over = True


class Generator():
    def __init__(self, world, game_board):
        self.world = world
        self.game_board = game_board
        self.piece_map = [None for x in range(7)]
        self.piece_map[0] = IPiece
        self.piece_map[1] = JPiece
        self.piece_map[2] = LPiece
        self.piece_map[3] = OPiece
        self.piece_map[4] = SPiece
        self.piece_map[5] = TPiece
        self.piece_map[6] = ZPiece

        self.color_map = [None for x in range(3)]
        self.color_map[0] = Colors.RED
        self.color_map[1] = Colors.GREEN
        self.color_map[2] = Colors.BLUE

    def create_piece(self):
        piece_num = random.randrange(7)
        color_num = random.randrange(3)

        color = self.color_map[color_num]
        piece_class = self.piece_map[piece_num]

        return piece_class(self.world, self.game_board, color)

    def create_specific_piece(self, piece_num):
        color_num = random.randrange(3)
        color = self.color_map[color_num]
        piece_class = self.piece_map[piece_num]
        return piece_class(self.world, self.game_board, color)




