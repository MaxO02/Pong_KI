class PADDEL:

    def __init__(self, positionx, positiony) -> None:
        self.posx = positionx
        self.posy = positiony
        self.mf = 2
        self.canmoveup = True
        self.canmovedown = True
        self.height = 150

    def getxpos(self) -> int:
        return self.posx

    def setxpos(self, newxpos) -> None:
        self.posx = newxpos

    def getypos(self) -> int:
        return self.posy

    def setypos(self, newypos) -> None:
        self.posy = newypos

    def moveyup(self) -> None:
        self.posy -= self.mf

    def moveydown(self) -> None:
        self.posy += self.mf

    def getmfy(self) -> float:
        return self.mf

    def setcmd(self, boolean) -> None:
        self.canmovedown = boolean

    def setcmu(self, boolean) -> None:
        self.canmoveup = boolean

    def getcmd(self) -> bool:
        return self.canmovedown

    def getcmu(self) -> bool:
        return self.canmoveup

    def getheight(self) -> int:
        return self.height
