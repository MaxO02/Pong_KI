class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mfx, self.mfy = mfspeed

    def reset(self, mfspeed):
        self.xpos = self.startx
        self.ypos = self.starty
        self.mfx, self.mfy = mfspeed

    def getxpos(self):
        return self.xpos

    def getypos(self):
        return self.ypos

    def setpos(self, position):
        self.xpos, self.ypos = position

    def move(self, timesec):
        self.xpos += self.mfx * timesec
        self.ypos += self.mfy * timesec

    def changeydirection(self):
        self.mfy = -self.mfy

    def changexdirection(self):
        self.mfx = -self.mfx

    def setstartpos(self, coords):
        self.startx, self.starty = coords
