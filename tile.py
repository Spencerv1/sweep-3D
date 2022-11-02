class Tile:
    
    def __init__(self, rect):
        self.clicked = False
        self.rect = rect

    def __str__(self):
        if self.clicked: 
            return "I'm Clicked already"
        return "Newly clicked"