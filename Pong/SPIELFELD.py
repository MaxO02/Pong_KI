import pygame

from Pong.BALL import BALL
from Pong.paddel import PADDEL


class SPIELFELD:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    paddle_color = (254, 115, 1)
    ball_color = (85, 57, 138)
    background_color = (1, 254, 240)
#    font_color = (254, 1, 14)
    font_color = paddle_color

    def __init__(self, tmm):
        self.tmm = tmm
        pygame.init()
        resolution = (1920, 1080)
        self.WIDTH, self.HEIGHT = resolution

        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Pong")
        self.score_font = pygame.font.SysFont("Clear Sans Regular", 80)

        self.leftpaddel = PADDEL(int(self.WIDTH*0.1), int(self.HEIGHT/2))
        self.rightpaddel = PADDEL(int(self.WIDTH*0.9), int(self.HEIGHT/2))
        self.ball = BALL(int(self.WIDTH / 2), int(self.HEIGHT / 2), (0.5 * self.WIDTH, 0.5 * self.HEIGHT))

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
            if self.rightpaddel.getypos() < self.ball.getypos() < self.rightpaddel.getypos() + self.rightpaddel.getheight():
                self.ball.changexdirection()
            if self.leftpaddel.getypos() < self.ball.getypos() < self.leftpaddel.getypos() + self.leftpaddel.getheight():
                self.ball.changexdirection()

        if self.ball.getxpos() > self.WIDTH:
            self.tmm.goalleft()
            self.ball.reset()

        if self.ball.getxpos() < 0:
            self.tmm.goalright()
            self.ball.reset()

    def updatescreen(self, scoreleft, scoreright):
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10, self.leftpaddel.getheight()])
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10, self.rightpaddel.getheight()])
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])

        self.screen.blit(self.score_font.render(str(scoreleft), True, self.font_color), (self.WIDTH / 4, 50))
        self.screen.blit(self.score_font.render(str(scoreright), True, self.font_color), (self.WIDTH / 1.25, 50))

        pygame.display.flip()

