from cell import Cell
import math

class HexGrid:
    def __init__(self, grid_size, grid_type):
        self.grid_type = grid_type
        self.grid_content = []
        self.grid_size = grid_size

        self.create_grid(grid_size)


    def create_cell(self, x, y, is_filled=1):
        cell = Cell((x, y), is_filled)
        return cell

    def create_grid(self, grid_size):
        if (self.grid_type=='diamond'):
            for r in range(grid_size):
                cell_row = []
                for c in range(grid_size):
                    cell = self.create_cell(r, c)
                    cell_row.append(cell)
                self.grid_content.append(cell_row)
        elif (self.grid_type=='triangle'):
            for r in range(grid_size):
                cell_row = []
                for c in range(r+1):
                    cell = self.create_cell(r, c)
                    cell_row.append(cell)
                self.grid_content.append(cell_row)
        self.create_neighbourhood()

    def create_neighbourhood(self):
        for r, row in enumerate(self.grid_content):
            for c, cell in enumerate(row):
                # gets the neighbour positions according to grid type (diamond/triangle)
                neighbour_positions = self.get_neighbour_positions(r, c)
                for neighbour_pos in neighbour_positions:
                    if self.neighbour_pos_is_valid(neighbour_pos, r, c, self.grid_size):
                        # for edge/corner cells, some of the neighbour positions may not be legal
                        neighbour = self.grid_content[neighbour_pos[0]][neighbour_pos[1]]
                        self.add_neighbour(cell, neighbour)
                    else:
                        self.add_neighbour(cell, None)

    def neighbour_pos_is_valid(self, neighbour_pos, row_index, col_index, grid_size):
        # for both grid types, a neighbour position must be non zero and less than length size
        if not ((neighbour_pos[0] < 0 or neighbour_pos[1] < 0) or (neighbour_pos[0] >= grid_size or neighbour_pos[1] >= grid_size)):
            if self.grid_type == 'diamond':
                return True
            elif self.grid_type == 'triangle':
                # for triangle, for a cell along the diagonal, the neighbour cannot lie outside of the diagonal
                if (not (neighbour_pos[1] == col_index and neighbour_pos[0] < row_index+1 and col_index == row_index)
                        and not (neighbour_pos[0] <= row_index and neighbour_pos[1] >= row_index+1)):
                    return True
        return False

    def get_grid_content(self):
        return self.grid_content

    def add_neighbour(self, cell, neighbour):
        cell.neighbours.append(neighbour)

    def get_neighbour_positions(self, r, c):
        if self.grid_type == 'triangle':
            return [(r - 1, c - 1), (r + 1, c + 1), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c)]
        elif self.grid_type == 'diamond':
            return [(r - 1, c + 1), (r + 1, c - 1), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c)]

    def print_grid(self):
        # for debugging
        for row in self.grid_content:
            for cell in row:
                print(cell.is_filled, end=" ")
            print('')

    def get_center_cell(self):
        # returns a center cell, used for initializing empty cell on game board
        var = math.ceil(self.grid_size/2)-1
        return self.grid_content[var][var]


