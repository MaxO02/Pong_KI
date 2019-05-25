from time import sleep
import multitasking


class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mfx, self.mfy = mfspeed
        self.turnedx = False
        self.turnedy = False

    def reset(self, mfspeed) -> None:
        self.xpos = self.startx
        self.ypos = self.starty
        self.mfx, self.mfy = mfspeed

    def getxpos(self) -> int:
        return self.xpos

    def getypos(self) -> int:
        return self.ypos

    def setpos(self, position) -> None:
        self.xpos, self.ypos = position

    def move(self, timesec) -> None:
        self.xpos += self.mfx * timesec
        self.ypos += self.mfy * timesec

    def changeydirection(self) -> None:
        if not self.turnedy:
            self.turnedy = True
            self.mfy = -self.mfy
            self.resetturnedy()

    def changexdirection(self) -> None:
        if not self.turnedx:
            self.turnedx = True
            self.mfx = -self.mfx
            self.resetturnedx()

    def setstartpos(self, coords) -> None:
        self.startx, self.starty = coords

    def add_mfx(self, deltav) -> None:
        self.mfx += deltav

    def add_mfy(self, deltav) -> None:
        self.mfy += deltav

    @multitasking.task
    def resetturnedx(self) -> None:
        sleep(0.5)
        self.turnedx = False

    @multitasking.task
    def resetturnedy(self) -> None:
        sleep(0.5)
        self.turnedy = False
