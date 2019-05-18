from Pong.SPIELFELD import SPIELFELD
import pygame
from pygame.locals import *

class THEMAINMASTER:
    def __init__(self):
        spf = SPIELFELD(self)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.scoreleft = 0
        self.scoreright = 0
        self.inputMap = [False, False, False, False]
        cancel = False
        while not cancel and self.scoreright <= 10 and self.scoreleft <= 10:
            self.events()
            spf.movepaddel(self.inputMap)
            spf.ballhandeling(self.clock.tick(60))
            spf.updatescreen(self.scoreleft, self.scoreright)
            self.clock.tick(60)

    
if __name__ == '__main__':    
    tmm = THEMAINMASTER()
