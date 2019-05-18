import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.paddel import PADDEL
from Pong.SPIELFELD import SPIELFELD
import random


class SPIELSTEUERUNG:
    # variables
    scoreleft, scoreright = 0, 0

    def __init__(self):
        """initiates the first match, gives necessary infos, starts the game on the ready-input"""
        # objects
        leftpaddle = PADDEL(192, 540)
        rightpaddle = PADDEL(1728, 540)
        ball = BALL(960, 540, (960 * random.choice([-1, 1]), 540 * random.choice([-1, 1])))
        spf = SPIELFELD(ball, leftpaddle, rightpaddle)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.inputMap = [False, False, False, False]

    def match(self):
        """creates a new screen
           handles all objects floating on the screen"""

        cancel = False
        while not cancel and self.scoreright <= 10 and self.scoreleft <= 10:
            self.events()
            spf.movepaddel(self.inputMap)
            spf.ballhandeling(self.clock.tick(60))
            spf.updatescreen(self.scoreleft, self.scoreright)
            self.clock.tick(60)

        pass

    def menu(self):
        """handles any settings, game pauses etc"""
        pass

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
