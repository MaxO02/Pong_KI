from time import sleep
import multitasking


class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos  # sets current x position aswell as x starting position
        self.starty = self.ypos = startypos  # sets current y position aswell as y starting position
        self.mfx, self.mfy = mfspeed  # sets current x speed aswell as y speed
        self.turnedx = False  # no x turn happened just now
        self.turnedy = False  # no y turn happened just now

    def reset(self, mfspeed) -> None:
        self.xpos = self.startx  # resets the x position to starting position
        self.ypos = self.starty  # resets the y position to starting position
        self.mfx, self.mfy = mfspeed  # sets the new speeds to given values

    def getxpos(self) -> int:
        return self.xpos  # returns the x position

    def getypos(self) -> int:
        return self.ypos  # returns the y position

    def setpos(self, position) -> None:
        self.xpos, self.ypos = position  # sets the position to given value

    def move(self, timesec) -> None:
        self.xpos += self.mfx * timesec  # moves the ball in x direction
        self.ypos += self.mfy * timesec  # moves the ball in y direction

    def changeydirection(self) -> None:
        if not self.turnedy:  # prevents the ball from getting stuck in a wall
            self.turnedy = True  # ball just turned in y direction
            self.mfy = -self.mfy  # inverts the movement
            self.resetturnedy()  # will wait to reset the turnedy

    def changexdirection(self) -> None:
        if not self.turnedx:  # prevents the ball from getting stuck in a wall
            self.turnedx = True  # ball just turned in x direction
            self.mfx = -self.mfx  # inverts the movement
            self.resetturnedx()  # will wait to reset the turnedy

    def setstartpos(self, coords) -> None:
        self.startx, self.starty = coords  # sets  the starting position to new coordinates

    def add_mfx(self, deltav) -> None:
        self.mfx += deltav  # adds x movement speed

    def add_mfy(self, deltav) -> None:
        self.mfy += deltav  # adds y movement speed

    @multitasking.task
    def resetturnedx(self) -> None:
        sleep(0.5)  # waits for half a second
        self.turnedx = False  # sets back boolean

    @multitasking.task
    def resetturnedy(self) -> None:
        sleep(0.5)  # waits for half a second
        self.turnedy = False  # sets back boolean
