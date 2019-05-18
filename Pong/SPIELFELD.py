import pygame
import random

from Pong.BALL import BALL
from Pong.paddel import PADDEL


class SPIELFELD:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    paddle_color = (254, 115, 1)
    ball_color = (85, 57, 138)
    background_color = (1, 254, 240)
    font_color = paddle_color

    def __init__(self, tmm, ball, leftpaddle, rightpaddle):
        self.tmm = tmm
        pygame.init()
        self.resolution = (1920, 1080)
        self.WIDTH, self.HEIGHT = self.resolution

        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Pong by Max and Linus")
        self.score_font = pygame.font.SysFont("Clear Sans Regular", 80)
        self.menu_font = pygame.font.SysFont("Clear Sans Regular", 30)
        self.menu_font_focused = pygame.font.SysFont("Clear Sans Regular", 40)

        self.leftpaddel = leftpaddle
        self.rightpaddel = rightpaddle
        self.ball = ball
        """self.ball.waitforinput()"""

    def movepaddel(self, inputmap):
        if self.rightpaddel.getypos() < 0 - self.rightpaddel.getheight() / 2:
            self.rightpaddel.setcmu(False)
        else:
            self.rightpaddel.setcmu(True)
        if self.rightpaddel.getypos() > self.HEIGHT - self.rightpaddel.getheight() / 2:
            self.rightpaddel.setcmd(False)
        else:
            self.rightpaddel.setcmd(True)
        if self.leftpaddel.getypos() < 0 - self.leftpaddel.getheight() / 2:
            self.leftpaddel.setcmu(False)
        else:
            self.leftpaddel.setcmu(True)
        if self.leftpaddel.getypos() > self.HEIGHT - self.leftpaddel.getheight() / 2:
            self.leftpaddel.setcmd(False)
            self.leftpaddel.setcmd(True)

        if self.rightpaddel.getcmd() and inputmap[0]:
            self.rightpaddel.moveydown()
        elif self.rightpaddel.getcmu() and inputmap[1]:
            self.rightpaddel.moveyup()
        if self.leftpaddel.getcmd() and inputmap[2]:
            self.leftpaddel.moveydown()
        elif self.leftpaddel.getcmu() and inputmap[3]:
            self.leftpaddel.moveyup()

    def ballhandeling(self, clocktick):

        self.ball.move(clocktick / 1000.0)

        if self.ball.getypos() > self.HEIGHT or self.ball.getypos() < 0:
            self.ball.changeydirection()
        if self.ball.getxpos() > self.rightpaddel.getxpos() or self.ball.getxpos() < self.leftpaddel.getxpos():
            if self.rightpaddel.getypos() < self.ball.getypos() < self.rightpaddel.getypos() + \
                    self.rightpaddel.getheight():
                self.ball.changexdirection()
            if self.leftpaddel.getypos() < self.ball.getypos() < self.leftpaddel.getypos() \
                    + self.leftpaddel.getheight():
                self.ball.changexdirection()

        if self.ball.getxpos() > self.WIDTH:
            self.tmm.goalleft()
            self.ball.reset((0.5 * self.WIDTH * random.choice([-1, 1]), 0.4 * self.HEIGHT * random.choice([-1, 1])))

        if self.ball.getxpos() < 0:
            self.tmm.goalright()
            self.ball.reset((0.5 * self.WIDTH * random.choice([-1, 1]), 0.4 * self.HEIGHT * random.choice([-1, 1])))

    def updatescreen(self, scoreleft, scoreright):
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10,
                                                          self.leftpaddel.getheight()])
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10,
                                                          self.rightpaddel.getheight()])
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])

        self.screen.blit(self.score_font.render(str(scoreleft), True, self.font_color), (self.WIDTH / 4, 50))
        self.screen.blit(self.score_font.render(str(scoreright), True, self.font_color), (self.WIDTH / 1.25, 50))

        pygame.display.flip()

    def giveresolution(self):
        return self.resolution

    def changeresolution(self, newresolution):
        self.resolution = newresolution
        self.screen = pygame.display.set_mode(self.resolution)
        self.WIDTH, self.HEIGHT = self.resolution
        self.leftpaddel = PADDEL(int(self.WIDTH * 0.1), int(self.HEIGHT / 2))
        self.rightpaddel = PADDEL(int(self.WIDTH * 0.9), int(self.HEIGHT / 2))
        self.ball = BALL(int(self.WIDTH / 2), int(self.HEIGHT / 2), (0.5 * self.WIDTH * random.choice([-1, 1]),
                                                                     0.5 * self.HEIGHT * random.choice([-1, 1])))

    def menuscreen(self):
        self.screen.fill(0, 0, 0)
        """buttons:
        - Start Game
        - Settings
        - help
        - Info
        - Exit game
        - Player-Mode"""



        # nothing is focused
        self.screen.blit(self.menu_font.render("START A NEW GAME", True, (254, 254, 254)), (self.WIDTH/2, (self.HEIGHT -
                                                                                                           100)/5 + 50))
        self.screen.blit(self.menu_font.render("SETTINGS", True, (254, 254, 254)), (self.WIDTH/2, (self.HEIGHT - 100)/5
                                                                                    * 2 + 50))
        self.screen.blit(self.menu_font.render("HELP", True, (254, 254, 254)), (self.WIDTH/2, (self.HEIGHT - 100)/5 * 3
                                                                                + 50))
        self.screen.blit(self.menu_font.render("INFO", True, (254, 254, 254)), (self.WIDTH/2, (self.HEIGHT - 100)/5 * 4
                                                                                + 50))
        self.screen.blit(self.menu_font.render("EXIT GAME", True, (254, 254, 254)), (self.WIDTH/2, (self.HEIGHT - 50)))
