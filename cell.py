class Cell:
    def __init__(self, position, is_filled=0):
        self.position = position
        self.neighbours = []
        self.is_filled = is_filled