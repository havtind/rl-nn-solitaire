from enum import Enum
from hexGrid import HexGrid
from hexGridVisualizer import HexGridVisualizer

class DiamondDirections(Enum):
    UP_RIGHT = 0
    DOWN_LEFT = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP = 5

class TriangleDirections(Enum):
    UP_LEFT = 0
    DOWN_RIGHT = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP = 5

class PegSolitaire:
    def __init__(self, size, shape, game_title, visualize=False,
                 empty_cell_pos=[], display_frequency=0.6):
        self.grid_shape = shape
        self.size = size
        self.board = HexGrid(size, self.grid_shape)
        self.board_content = self.board.get_grid_content()
        self.visualize = visualize
        self.game_title = game_title
        self.empty_cell_pos = empty_cell_pos
        if self.grid_shape == 'diamond':
            self.directions = DiamondDirections
        else:
            self.directions = TriangleDirections

        self.display_frequency = display_frequency
        self.initialize_grid()

        if visualize:
            self.display = HexGridVisualizer(self.board_content, self.grid_shape, self.display_frequency)
            self.display.update_display(self.game_title)

    def get_reward(self):
        # based on number of pegs left, returns a reward
        # returns reward only when game is over
        legal_moves = self.get_possible_moves()
        reward = 0
        if (len(legal_moves) < 1):
            if self.count_filled_cells() == 1:
                reward = 100
            elif self.count_filled_cells() == 2:
                reward = -50
            else:
                reward = -100
        return reward

    def count_filled_cells(self):
        # counts number of pegs on the board
        count = 0
        for r, row in enumerate(self.board.grid_content):
            for c, cell in enumerate(row):
                if cell.is_filled == 1:
                    count += 1
        return count

    def initialize_grid(self):
        # takes care of initializing the board with empty cells
        # by default the center cells, but can be given a list of empty cells as input
        if len(self.empty_cell_pos) > 0:
            for cell_pos in self.empty_cell_pos:
                start_cell = self.board_content[cell_pos[0]][cell_pos[1]]
                start_cell.is_filled = 0
        else:
            if self.grid_shape == 'diamond' and self.size==4:
                start_cell = self.board_content[2][1]
            else:
                start_cell = self.board.get_center_cell()
            start_cell.is_filled = 0

    def get_state_as_bitstring(self):
        # states are represented as strings of bits.
        bitstr = ""
        for r, row in enumerate(self.board.grid_content):
            for c, cell in enumerate(row):
                if cell.is_filled ==1:
                    bitstr += '1'
                else:
                    bitstr += '0'
        return bitstr

    def make_move(self, peg, direction):
        # performs a move on the game board.
        # peg is a tuple with position for jumping peg
        self.board.grid_content[peg[0]][peg[1]].is_filled = 0
        self.board.grid_content[peg[0]][peg[1]].neighbours[direction].is_filled = 0
        self.board.grid_content[peg[0]][peg[1]].neighbours[direction].neighbours[direction].is_filled = 1
        if self.visualize:
            self.display.update_display(self.game_title)


    def get_possible_moves(self):
        # returns a list of possible moves.
        # represented by the position of a peg and the direction for jumping
        # direction is represented as enum
        possible_moves = []
        for r, row in enumerate(self.board_content):
            for c, cell in enumerate(row):
                if cell.is_filled == 1:
                    for n, neighbour in enumerate(cell.neighbours):
                        if neighbour is not None:
                            if neighbour.is_filled == 1:
                                if neighbour.neighbours[n] is not None:
                                    if neighbour.neighbours[n].is_filled == 0:
                                        possible_moves.append(((r,c),n))

        return possible_moves


    def test_class(self):
        #str = self.get_state_as_bitstring()
        #print(str)
        self.board.print_grid()
        possible_moves = self.get_possible_moves()
        print(possible_moves)
        if self.visualize:
            display = HexGridVisualizer(self.board.grid_content, self.board.grid_type)
            display.draw_grid()
        i = 0
        peg = possible_moves[i][0]
        direction = possible_moves[i][1]
        self.make_move(peg,direction)
        self.board.print_grid()
        #display.draw_grid()
        #str = self.get_state_as_bitstring()
        #print(str)


