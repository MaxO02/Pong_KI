class PADDEL:

    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.mf = 10
        self.canmoveup = True
        self.canmovedown = True
        self.height = 150

    def getxpos(self):
        return self.posx

    def getypos(self):
        return self.posy

    def getmf(self):
        return self.mf

    def setypos(self, newypos):
        self.posy = newypos

    def moveyup(self):
        self.posy - self.mf

    def moveydown(self):
        self.posy + self.mf

    def setcmd(self, bool):
        self.canmovedown = bool

    def setcmu(self, boll):
        self.canmoveup = boll

    def getcmd(self):
        return self.canmovedown

    def getcmu(self):
        return self.canmoveup

    def getheight(self):
        return self.height
