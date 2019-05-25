class PADDEL:

    def __init__(self, positionx, positiony):
        self.posx = positionx
        self.posy = positiony
        self.mf = 3.5
        self.canmoveup = True
        self.canmovedown = True
        self.height = 150

    def getxpos(self):
        return self.posx

    def setxpos(self, newxpos):
        self.posx = newxpos

    def getypos(self):
        return self.posy

    def setypos(self, newypos):
        self.posy = newypos

    def moveyup(self):
        self.posy -= self.mf

    def moveydown(self):
        self.posy += self.mf

    def getmfy(self):
        return self.mf

    def setcmd(self, boolean):
        self.canmovedown = boolean

    def setcmu(self, boolean):
        self.canmoveup = boolean

    def getcmd(self):
        return self.canmovedown

    def getcmu(self):
        return self.canmoveup

    def getheight(self):
        return self.height
