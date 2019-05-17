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

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_ESCAPE]:
                    exit()
                self.inputMap[0] = pressed_keys[K_DOWN]
                self.inputMap[1] = pressed_keys[K_UP]
                self.inputMap[2] = pressed_keys[K_s]
                self.inputMap[3] = pressed_keys[K_w]


    def goalright(self):
        self.scoreright += 1

    def goalleft(self):
        self.scoreleft += 1

    def getscreen(self):
        return self.screen

    
if __name__ == '__main__':    
    tmm = THEMAINMASTER()
