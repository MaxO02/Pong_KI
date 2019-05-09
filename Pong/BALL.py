class BALL:
    def __init__(self, startxpos, startypos):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mf = 450

    def reset(self):
        self.xpos = self.startx
        self.ypos = self.starty

    def getxpos(self):
        return self.xpos

    def getypos(self):
        return self.ypos
