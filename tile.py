class Tile:
    
    def __init__(self, rect):
        self.clicked = False
        self.is_mine = False
        self.rect = rect

    def __str__(self):
        r = ''
        if self.clicked: 
            r += "I'm Clicked already"
        if self.is_mine: 
            r += "Mine!"

        return r