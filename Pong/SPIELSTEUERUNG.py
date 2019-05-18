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
        self.spf = SPIELFELD(ball, leftpaddle, rightpaddle)
        self.WIDTH, self.HEIGHT = spf.giveresolution()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.inputMap = [False, False, False, False]
        self.focus = [False, False, False, False, False]

    def match(self):
        """creates a new screen
           handles all objects floating on the screen"""

        cancel = False
        while not cancel and self.scoreright <= 10 and self.scoreleft <= 10:
            self.events()
            self.spf.movepaddel(self.inputMap)
            self.spf.ballhandeling(self.clock.tick(60))
            self.spf.updatescreen(self.scoreleft, self.scoreright)
            self.clock.tick(60)

        pass

    def menu(self):
        """handles any settings, game pauses etc"""
        self.events()
        self.spf.menuscreen(self.focus)
        self.clock.tick(60)


    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_ESCAPE]:
                    exit()
                if pressed_keys[K_p]:
                    self.menu()
                self.inputMap[0] = pressed_keys[K_DOWN]
                self.inputMap[1] = pressed_keys[K_UP]
                self.inputMap[2] = pressed_keys[K_s]
                self.inputMap[3] = pressed_keys[K_w]

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < self.HEIGHT * 0.25:
                    self.focus[0] = True
                elif y < self.HEIGHT * 5 / 12:
                    self.focus[1] = True
                elif y < self.HEIGHT / 12 * 7:
                    self.focus[2] = True
                elif y < self.HEIGHT * 0.75:
                    self.focus[3] = True
                else:
                    self.focus[4] = True
                del x, y

            if event.type == pygame.MOUSEBUTTONUP:
                self.clearlist(self.focus)

    def clearlist(list):
        for i in range(len(list)):
            list[i - 1] = False

    def goalright(self):
        self.scoreright += 1

    def goalleft(self):
        self.scoreleft += 1
