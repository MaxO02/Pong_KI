class PADDEL:

    def __init__(self, positionx, positiony) -> None:
        self.posx = positionx  # sets the x position
        self.posy = positiony  # sets the y position
        self.mf =self.basemf = 1   # sets the speed of movement
        self.canmoveup = True    # can paddle go higher
        self.canmovedown = True  # paddle go lower
        self.height = 150  # sets the height of the paddle

    def getxpos(self) -> int:
        return self.posx  # returns the x position

    def setxpos(self, newxpos) -> None:
        self.posx = newxpos  # sets the x position to given value

    def getypos(self) -> int:
        return self.posy  # returns the y position

    def setypos(self, newypos) -> None:
        self.posy = newypos  # sets the y position to given value

    def moveyup(self) -> None:
        self.posy -= self.mf  # moves the paddle up by one iteration
        self.mf +=1

    def moveydown(self) -> None:
        self.posy += self.mf  # moves the paddle down by one iteration
        self.mf +=1

    def getmfy(self) -> float:
        return self.mf  # returns the speed of movement

    def setcmd(self, boolean) -> None:
        self.canmovedown = boolean  # sets the movement boolean down to given value

    def setcmu(self, boolean) -> None:
        self.canmoveup = boolean  # sets the movement boolean up to given value

    def getcmd(self) -> bool:
        return self.canmovedown  # returns the movement down boolean

    def getcmu(self) -> bool:
        return self.canmoveup  # returns the movement up boolean

    def getheight(self) -> int:
        return self.height  # returns the paddle height

    def reset(self):
        self.mf = self.basemf
