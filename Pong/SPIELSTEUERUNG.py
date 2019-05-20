import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.PADDLE import PADDEL
from Pong.WINDOW import WINDOW
from Pong.SOUNDS import SOUNDS
import random
from time import sleep


class SPIELSTEUERUNG:
    scoreleft, scoreright = 0, 0
    kickoffbool = True
    gamemode = '1v1'

    def __init__(self):
        """loads necessary modules, defines important objects, initiates the menu, gives necessary infos"""
        self.leftpaddle = PADDEL(192, 540)
        self.rightpaddle = PADDEL(1728, 540)
        self.ball = BALL(960, 540, (540 / 0.6 * random.choice([-1, 1]), 540 / 0.6 * random.choice([-1, 1])))
        self.spf = WINDOW(self.ball, self.leftpaddle, self.rightpaddle)
        self.width, self.hight = self.spf.giveresolution()
        pygame.init()
        self.inputMap = [False, False, False, False]
        self.focus = [False, False, False, False, False]
        while True:
            self.mainmenu()

    def matchstart(self):
        """creates a new screen
           handles all objects floating on the screen
           waits for the first input to kickoff"""
        self.kickoffbool = True
        while self.scoreright < 10 and self.scoreleft < 10:
            self.spf.updategamescreen(self.scoreleft, self.scoreright)
            self.events()
            if self.gamemode == '1v1':
                self.movepaddel1v1(self.inputMap)
            else:
                self.movepaddelsingleplayer(self.inputMap)
            self.ballhandeling(self.clock.tick(200))
            self.clock.tick(200)

    def kickoff(self):
        self.spf.kickoffScreen(self.scoreleft, self.scoreright, "PRESS 'SPACE'")
        while self.kickoffbool:
            self.events()
            sleep(0.1)
        self.kickoffbool = True
        SOUNDS.play('soundfiles/airhorn.wav')
        sleep(0.5)
        self.clock = pygame.time.Clock()
        self.matchstart()

    def mainmenu(self):
        """handles any settings, game pauses etc"""
        while True:
            """show the main menu and wait for an event"""
            self.events()
            self.spf.menuscreenmain(self.focus)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:
                    self.kickoffbool = False
                if pressed_keys[K_ESCAPE]:
                    self.mainmenu()
                self.inputMap[0] = pressed_keys[K_DOWN]
                self.inputMap[1] = pressed_keys[K_UP]
                self.inputMap[2] = pressed_keys[K_s]
                self.inputMap[3] = pressed_keys[K_w]
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                self.focus[0] = y < self.hight * 0.25 and self.width * 0.3 < x < self.width * 0.7
                self.focus[1] = self.hight * 0.25 < y < self.hight * 5 / 12 and self.width * 0.3 < x < self.width * 0.7
                self.focus[2] = self.hight * 5/12 < y < self.hight / 12 * 7 and self.width * 0.3 < x < self.width * 0.7
                self.focus[3] = self.hight / 12 * 7 < y < self.hight * 0.75 and self.width * 0.3 < x < self.width * 0.7
                self.focus[4] = y > self.hight * 0.75
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focus[0]:
                    self.kickoff()
                elif self.focus[1]:
                    self.settings()
                elif self.focus[2]:
                    self.help()
                elif self.focus[3]:
                    self.info()
                elif self.focus[4]:
                    exit()

    def movepaddel1v1(self, inputmap):
        if self.rightpaddle.getypos() < 1:
            self.rightpaddle.setcmu(False)
        else:
            self.rightpaddle.setcmu(True)
        if self.rightpaddle.getypos() >= self.hight - self.rightpaddle.gethight():
            self.rightpaddle.setcmd(False)
        else:
            self.rightpaddle.setcmd(True)
        if self.leftpaddle.getypos() < 1:
            self.leftpaddle.setcmu(False)
        else:
            self.leftpaddle.setcmu(True)
        if self.leftpaddle.getypos() >= self.hight - self.rightpaddle.gethight():
            self.leftpaddle.setcmd(False)
        else:
            self.leftpaddle.setcmd(True)
        if self.rightpaddle.getcmd() and inputmap[0]:
            self.rightpaddle.moveydown()
        elif self.rightpaddle.getcmu() and inputmap[1]:
            self.rightpaddle.moveyup()
        if self.leftpaddle.getcmd() and inputmap[2]:
            self.leftpaddle.moveydown()
        elif self.leftpaddle.getcmu() and inputmap[3]:
            self.leftpaddle.moveyup()

    def movepaddelsingleplayer(self, inputmap):
        if self.rightpaddle.getypos() < 1:
            self.rightpaddle.setcmu(False)
        else:
            self.rightpaddle.setcmu(True)
        if self.rightpaddle.getypos() >= self.hight - self.rightpaddle.gethight():
            self.rightpaddle.setcmd(False)
        else:
            self.rightpaddle.setcmd(True)
        if self.leftpaddle.getypos() < 1:
            self.leftpaddle.setcmu(False)
        else:
            self.leftpaddle.setcmu(True)
        if self.leftpaddle.getypos() >= self.hight - self.rightpaddle.gethight():
            self.leftpaddle.setcmd(False)
        else:
            self.leftpaddle.setcmd(True)
        if self.rightpaddle.getcmd() and inputmap[0]:
            self.rightpaddle.moveydown()
        elif self.rightpaddle.getcmu() and inputmap[1]:
            self.rightpaddle.moveyup()

        if self.leftpaddle.getcmd() and self.ball.getypos() > self.leftpaddle.getypos()+self.leftpaddle.gethight()/2:
            self.leftpaddle.moveydown()
        elif self.leftpaddle.getcmu() and self.ball.getypos() < self.leftpaddle.getypos()+self.leftpaddle.gethight()/2:
            self.leftpaddle.moveyup()

    def ballhandeling(self, clocktick):
        self.ball.move(clocktick / 1000.0)
        if not 21 < self.ball.getypos() < self.hight - 21:
            self.ball.changeydirection()
            SOUNDS.play('soundfiles/jump.wav')
        if self.leftpaddle.getxpos() + 5 < self.ball.getxpos() < self.leftpaddle.getxpos() + 16:
            if self.leftpaddle.getypos() < self.ball.getypos() < self.leftpaddle.getypos() \
                    + self.leftpaddle.gethight():
                self.ball.changexdirection()
                SOUNDS.play('soundfiles/jump.wav')
                if self.inputMap[2]:
                    self.ball.add_mfy(self.rightpaddle.getmfy() * 10)
                elif self.inputMap[3]:
                    self.ball.add_mfy(-self.rightpaddle.getmfy() * 10)
        if self.rightpaddle.getxpos() - 16 < self.ball.getxpos() < self.rightpaddle.getxpos() + 5:
            if self.rightpaddle.getypos() < self.ball.getypos() < self.rightpaddle.getypos() + \
                    self.rightpaddle.gethight():
                self.ball.changexdirection()
                SOUNDS.play('soundfiles/jump.wav')
                if self.inputMap[0]:
                    self.ball.add_mfy(self.rightpaddle.getmfy() * 10)
                elif self.inputMap[1]:
                    self.ball.add_mfy(-self.rightpaddle.getmfy() * 10)
        if self.ball.getxpos() >= self.width:
            SOUNDS.play('soundfiles/shatter.wav')
            self.resetpaddles()
            self.goalleft()
            self.ball.reset((0.5 * self.width * random.choice([-1, 1]), 0.5 * self.hight * random.choice([-1, 1])))
            self.kickoff()
        if self.ball.getxpos() < 1:
            SOUNDS.play('soundfiles/shatter.wav')
            self.resetpaddles()
            self.goalright()
            self.ball.reset((0.5 * self.width * random.choice([-1, 1]), 0.5 * self.hight * random.choice([-1, 1])))
            self.kickoff()

    @staticmethod
    def clearlist(l, data):
        for i in range(len(l)):
            l[i - 1] = data

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

    def resetpaddles(self):
        self.rightpaddle.setypos(self.hight/2)
        self.leftpaddle.setypos(self.hight/2)
