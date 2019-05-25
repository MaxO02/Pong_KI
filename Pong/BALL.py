from time import sleep
import multitasking


class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mfx, self.mfy = mfspeed
        self.turnedx = False
        self.turnedy = False

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
        if not self.turnedy:
            self.turnedy = True
            self.mfy = -self.mfy
            self.resetturnedy()

    def changexdirection(self):
        if not self.turnedx:
            self.turnedx = True
            self.mfx = -self.mfx
            self.resetturnedx()

    def setstartpos(self, coords):
        self.startx, self.starty = coords

    def add_mfx(self, deltav):
        self.mfx += deltav

    def add_mfy(self, deltav):
        self.mfy += deltav

    @multitasking.task
    def resetturnedx(self):
        sleep(0.5)
        self.turnedx = False

    @multitasking.task
    def resetturnedy(self):
        sleep(0.5)
        self.turnedy = False
