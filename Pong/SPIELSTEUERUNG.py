import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.paddel import PADDEL
from Pong.WINDOW import WINDOW
import random


class SPIELSTEUERUNG:
    scoreleft, scoreright = 0, 0

    def __init__(self):
        """loads necessary modules, defines important objects, initiates the menu, gives necessary infos"""
        # objects
        self.leftpaddle = PADDEL(192, 540)
        self.rightpaddle = PADDEL(1728, 540)
        self.ball = BALL(960, 540, (960 * random.choice([-1, 1]), 540 * random.choice([-1, 1])))
        self.spf = WINDOW(self.ball, self.leftpaddle, self.rightpaddle)
        self.WIDTH, self.HEIGHT = self.spf.giveresolution()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.inputMap = [False, False, False, False]
        self.focus = [False, False, False, False, False]
        while True:
            self.mainmenu()

    def matchstart(self):
        """creates a new screen
           handles all objects floating on the screen
           waits for the first input to kickoff"""
        self.scoreleft, self.scoreright = 0, 0
        while self.scoreright <= 10 and self.scoreleft <= 10:
            self.spf.updategamescreen(self.scoreleft, self.scoreright)
            self.events()
            self.movepaddel(self.inputMap)
            self.ballhandeling(self.clock.tick(60))
            self.clock.tick(60)

    def mainmenu(self):
        """handles any settings, game pauses etc"""
        while True:
            self.events()
            self.spf.menuscreenmain(self.focus)
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_p]:
                    self.mainmenu()
                self.inputMap[0] = pressed_keys[K_DOWN]
                self.inputMap[1] = pressed_keys[K_UP]
                self.inputMap[2] = pressed_keys[K_s]
                self.inputMap[3] = pressed_keys[K_w]
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                self.focus[0] = y < self.HEIGHT * 0.25
                self.focus[1] = y < self.HEIGHT * 5 / 12
                self.focus[2] = y < self.HEIGHT / 12 * 7
                self.focus[3] = y < self.HEIGHT * 0.75
                self.focus[4] = y > self.HEIGHT * 0.75
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focus[0]:
                    self.matchstart()
                elif self.focus[1]:
                    self.settings()
                elif self.focus[2]:
                    self.help()
                elif self.focus[3]:
                    self.info()
                elif self.focus[4]:
                    exit()

    def movepaddel(self, inputmap):
        if self.rightpaddle.getypos() < 0 - self.rightpaddle.getheight() / 2:
            self.rightpaddle.setcmu(False)
        else:
            self.rightpaddle.setcmu(True)
        if self.rightpaddle.getypos() > self.HEIGHT - self.rightpaddle.getheight() / 2:
            self.rightpaddle.setcmd(False)
        else:
            self.rightpaddle.setcmd(True)
        if self.leftpaddle.getypos() < 0 - self.leftpaddle.getheight() / 2:
            self.leftpaddle.setcmu(False)
        else:
            self.leftpaddle.setcmu(True)
        if self.leftpaddle.getypos() > self.HEIGHT - self.leftpaddle.getheight() / 2:
            self.leftpaddle.setcmd(False)
            self.leftpaddle.setcmd(True)
        if self.rightpaddle.getcmd() and inputmap[0]:
            self.rightpaddle.moveydown()
        elif self.rightpaddle.getcmu() and inputmap[1]:
            self.rightpaddle.moveyup()
        if self.leftpaddle.getcmd() and inputmap[2]:
            self.leftpaddle.moveydown()
        elif self.leftpaddle.getcmu() and inputmap[3]:
            self.leftpaddle.moveyup()

    def ballhandeling(self, clocktick):
        self.ball.move(clocktick / 1000.0)
        if self.ball.getypos() > self.HEIGHT or self.ball.getypos() < 0:
            self.ball.changeydirection()
        if self.ball.getxpos() > self.rightpaddle.getxpos() or self.ball.getxpos() < self.leftpaddle.getxpos():
            if self.rightpaddle.getypos() < self.ball.getypos() < self.rightpaddle.getypos() + \
                    self.rightpaddle.getheight():
                self.ball.changexdirection()
            if self.leftpaddle.getypos() < self.ball.getypos() < self.leftpaddle.getypos() \
                    + self.leftpaddle.getheight():
                self.ball.changexdirection()
        if self.ball.getxpos() > self.WIDTH:
            self.goalleft()
            self.ball.reset((0.5 * self.WIDTH * random.choice([-1, 1]), 0.4 * self.HEIGHT * random.choice([-1, 1])))
        if self.ball.getxpos() < 0:
            self.goalright()
            self.ball.reset((0.5 * self.WIDTH * random.choice([-1, 1]), 0.4 * self.HEIGHT * random.choice([-1, 1])))

    @staticmethod
    def clearlist(l):
        for i in range(len(l)):
            l[i - 1] = False

    def settings(self):
        while True:
            self.spf.menuscreensettings()

    def help(self):
        while True:
            self.spf.menuscreenhelp()

    def info(self):
        while True:
            self.spf.menuscreeninfo()

    def goalright(self):
        self.scoreright += 1

    def goalleft(self):
        self.scoreleft += 1
