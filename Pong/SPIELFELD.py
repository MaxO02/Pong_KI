import pygame

from Pong.BALL import BALL
from Pong.paddel import PADDEL


class SPIELFELD:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    def __init__(self, tmm):
        self.tmm = tmm
        pygame.init()
        RESOLUTION = (1280, 720)
        self.WIDTH, self.HEIGHT = RESOLUTION

        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pong")
        self.score_font = pygame.font.SysFont("Clear Sans Regular", 30)

        self.leftpaddel = PADDEL(50, 50)
        self.rightpaddel = PADDEL(1220, 50)
        self.ball = BALL(int(self.WIDTH / 2), int(self.HEIGHT / 2))

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
        if self.rightpaddel.getcmu() and inputmap[1]:
            self.rightpaddel.moveyup()
        if self.leftpaddel.getcmd() and inputmap[2]:
            self.leftpaddel.moveydown()
        if self.leftpaddel.getcmu() and inputmap[3]:
            self.leftpaddel.moveyup()

        # Circle movement
        #circle_time_passed = clock.tick(60)
        #circle_time_sec = circle_time_passed / 1000.0
        #circle_posX += cmfX * circle_time_sec
        #circle_posY += cmfY * circle_time_sec

        # Circle collision
        #if circle_posY > HEIGHT or circle_posY < 0:
        #    cmfY = -cmfY
        #if circle_posX > self.rightpaddel.getxpos() or circle_posX < self.leftpaddel.getxpos():
        #    if circle_posY > self.rightpaddel.getxpos() and circle_posY < self.rightpaddel.getxpos() + self.rightpaddel.getheight:
        #        cmfX = -cmfX
        #    if circle_posY > self.leftpaddel.getypos() and circle_posY < self.leftpaddel.getypos() + self.leftpaddel.getheight:
        #        cmfX = -cmfX

        if self.ball.getxpos() > self.WIDTH:
            self.tmm.goalleft()
            self.ball.reset()

        if self.ball.getxpos() < 0:
            self.tmm.goalright()
            self.ball.reset()

    def updatescreen(self, scoreleft, scoreright):
        self.screen.fill(self.green)

        pygame.draw.rect(self.screen, self.blue, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10, self.leftpaddel.getheight()])
        pygame.draw.rect(self.screen, self.blue, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10, self.rightpaddel.getheight()])
        pygame.draw.rect(self.screen, self.red, [self.ball.getxpos(), self.ball.getypos(), 20, 20])

        self.screen.blit(self.score_font.render(str(scoreleft), True, self.blue), (self.WIDTH / 4, 50))
        self.screen.blit(self.score_font.render(str(scoreright), True, self.blue), (self.WIDTH / 1.25, 50))

        pygame.display.flip()

