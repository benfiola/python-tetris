import sdl2.ext
import Colors
from Configuration import *


class GameBoard(object):
    def __init__(self):
        self.board = [[None for x in range(num_columns())] for x in range(num_rows()+2)]


class GameState(object):
    def __init__(self):
        self.game_over = False


class MovementInput(object):
    def __init__(self):
        self.rotate_cw = False
        self.rotate_ccw = False
        self.move_left = False
        self.move_right = False
        self.soft_drop = False
        self.hard_drop = False

    def reset(self):
        self.rotate_cw = False
        self.rotate_ccw = False
        self.soft_drop = False
        self.hard_drop = False
        self.move_left = False
        self.move_right = False


class BlockCollection(object):
    def __init__(self, blocks):
        self.blocks = blocks


class BoardCoordinates(object):
    def __init__(self, pos, offset):
        self.pos = (pos[0]+offset[0], pos[1]+offset[1])
        self.offset = offset

    def get_ccw_offset(self):
        return self.offset[1], -self.offset[0]

    def get_cw_offset(self):
        return -self.offset[1], self.offset[0]

    def get_normalized_coordinates(self):
        return self.pos[0]-self.offset[0], self.pos[1]-self.offset[1]

    def get_ccw_coordinates(self):
        center = self.get_normalized_coordinates()
        offset = self.get_ccw_offset()
        return center[0]+offset[0], center[1]+offset[1]

    def get_cw_coordinates(self):
        center = self.get_normalized_coordinates()
        offset = self.get_cw_offset()
        return center[0]+offset[0], center[1]+offset[1]


class MovementState(object):
    def __init__(self):
        self.locked = False


class AudioState(object):
    def __init__(self):
        self.play_soft_drop = False
        self.play_line_clear = False

    def reset(self):
        self.play_soft_drop = False
        self.play_line_clear = False


class EndGameCondition(sdl2.ext.Entity):
    def __init__(self, world, game_board):
        self.gamestate = GameState()
        self.gameboard = game_board


class ControllablePiece(sdl2.ext.Entity):
    def __init__(self, world, game_board, blocks):
        self.blocks = blocks
        self.movementinput = MovementInput()
        self.gameboard = game_board
        self.blockcollection = BlockCollection(blocks)
        self.movementstate = MovementState()
        self.audiostate = AudioState()

    def clear(self):
        self.delete()
        for block in self.blockcollection.blocks:
            block.delete()


class Block(sdl2.ext.Entity):
    def __init__(self, world, color, game_board, offset):
        center = (len(game_board.board[0])/2, 0)
        block_width = window_width()/num_columns()
        block_height = window_height()/(num_rows())
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

        self.boardcoordinates = BoardCoordinates(center, offset)
        posx = self.boardcoordinates.pos[0] * block_width
        posy = self.boardcoordinates.pos[1]-2 * block_height
        self.sprite = factory.from_color(Colors.WHITE, size=(block_width, block_height))
        self.sprite.position = (posx, posy)
        sdl2.ext.fill(self.sprite, color, (1, 1, block_width-2, block_height-2))


class IPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-2, 0))
        blocks[1] = Block(world, color, game_board, (-1, 0))
        blocks[2] = Block(world, color, game_board, (0, 0))
        blocks[3] = Block(world, color, game_board, (1, 0))
        super(IPiece, self).__init__(world, game_board, blocks)


class JPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 0))
        blocks[1] = Block(world, color, game_board, (0, 0))
        blocks[2] = Block(world, color, game_board, (1, 0))
        blocks[3] = Block(world, color, game_board, (1, 1))
        super(JPiece, self).__init__(world, game_board, blocks)


class LPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 0))
        blocks[1] = Block(world, color, game_board, (0, 0))
        blocks[2] = Block(world, color, game_board, (1, 0))
        blocks[3] = Block(world, color, game_board, (-1, 1))
        super(LPiece, self).__init__(world, game_board, blocks)


class OPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 0))
        blocks[1] = Block(world, color, game_board, (0, 0))
        blocks[2] = Block(world, color, game_board, (-1, 1))
        blocks[3] = Block(world, color, game_board, (0, 1))
        super(OPiece, self).__init__(world, game_board, blocks)


class SPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 1))
        blocks[1] = Block(world, color, game_board, (0, 1))
        blocks[2] = Block(world, color, game_board, (0, 0))
        blocks[3] = Block(world, color, game_board, (1, 0))
        super(SPiece, self).__init__(world, game_board, blocks)


class TPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 0))
        blocks[1] = Block(world, color, game_board, (0, 0))
        blocks[2] = Block(world, color, game_board, (1, 0))
        blocks[3] = Block(world, color, game_board, (0, 1))
        super(TPiece, self).__init__(world, game_board, blocks)


class ZPiece(ControllablePiece):
    def __init__(self, world, game_board, color):
        blocks = [None for x in range(4)]
        blocks[0] = Block(world, color, game_board, (-1, 0))
        blocks[1] = Block(world, color, game_board, (0, 0))
        blocks[2] = Block(world, color, game_board, (0, 1))
        blocks[3] = Block(world, color, game_board, (+1, 1))
        super(ZPiece, self).__init__(world, game_board, blocks)