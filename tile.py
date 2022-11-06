

class Tile:
    
    def __init__(self, rect):
        self.clicked = False
        self.is_mine = False
        self.rect = rect
        self.num_mines = 0

    def __str__(self):
        r = f'Clicked: {self.clicked} Mine: {self.is_mine} Num Mines: {self.num_mines}'
        return r