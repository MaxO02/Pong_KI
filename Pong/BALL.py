import pygame
from pygame.locals import *
from time import sleep


class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos
        self.starty = self.ypos = startypos
        self.mfx, self.mfy = mfspeed

    def reset(self, mfspeed):
        self.xpos = self.startx
        self.ypos = self.starty
        self.mfx, self.mfy = mfspeed
        """self.waitforinput()"""

    def getxpos(self):
        return self.xpos

    def getypos(self):
        return self.ypos

    def move(self, timesec):
        self.xpos += self.mfx * timesec
        self.ypos += self.mfy * timesec

    def changeydirection(self):
        self.mfy = -self.mfy

    def changexdirection(self):
        self.mfx = -self.mfx

    def waitforinput(self):
        go = False
        while not go:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[K_SPACE]:
                        go = True
                        break
                    sleep(0.1)
