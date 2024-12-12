import networkx as nx
import matplotlib.pyplot as plt

class HexGridVisualizer:
    def __init__(self, hex_grid, grid_type, display_frequency):
        self.grid_graph = nx.Graph()
        self.create_grid_graph(hex_grid)
        self.grid_positions = self.get_cell_positions(grid_type)
        self.display_frequency = display_frequency

    def get_edges(self, grid_content):
        # an edge is added between every cell and its neighbours
        edges = []
        for row in grid_content:
            for cell in row:
                for neighbor in cell.neighbours:
                    if neighbor is not None:
                        edges.append((cell, neighbor))
        return edges

    def create_grid_graph(self, hex_grid):
        # add egdes to graph
        edges = self.get_edges(hex_grid)
        self.grid_graph.add_edges_from(edges)

    def get_cell_positions(self, board_type):
        # calculates the positions of the graph cells
        # performs a 45 degree rotation for a diamond
        # for a triangle, positiions are moved horisontally
        width = 13
        cell_positions = {}
        for cell in self.grid_graph:
            x_pos = cell.position[0]
            y_pos = cell.position[1]
            if board_type == "diamond":
                x = width + (-width/7) * x_pos + width/7 * y_pos
                y = width + (-width/7) * x_pos + (-width/7) * y_pos
            else: # = triangle
                x = width + (-width/8) * (x_pos/2) + width/8 * y_pos
                y = width + (-width/8) * x_pos

            cell_positions[cell] = (x,y)
        return cell_positions


    def draw_grid(self, game_title):
        plt.clf()
        plt.title(game_title)
        nx.draw(self.grid_graph, pos=self.grid_positions,
                node_color=self.get_cell_colors(), with_labels=False)


    def update_display(self, game_title, last_window=False):
        plt.clf()
        self.draw_grid(game_title)
        plt.pause(self.display_frequency)
        if last_window:
            # if last move, then dont close window
            plt.show()

    def get_cell_colors(self):
        colors = []
        for cell in self.grid_graph:
            if cell.is_filled == 1:
                colors.append('#d71e3e')
            else:
                colors.append('#efefef')
        return colors

