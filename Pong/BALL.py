class BALL:
    def __init__(self, startxpos, startypos):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mfx = 450
        self.mfy = 450

    def reset(self):
        self.xpos = self.startx
        self.ypos = self.starty

    def getxpos(self):
        return self.xpos

    def getypos(self):
        return self.ypos

    def movex(self, timesec):
        self.xpos += self.mfx * timesec

    def movey(self, timesec):
        self.ypos += self.mfy * timesec

    def changeydirection(self):
        self.mfy = -self.mfy

    def changexdirection(self):
        self.mfx = -self.mfx
