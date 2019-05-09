import pygame

from Pong.BALL import BALL
from Pong.paddel import PADDEL


class SPIELFELD:

    pygame.init()

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    RESOLUTION = (1280, 720)
    WIDTH, HEIGHT = RESOLUTION

    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pong")

    score_font = pygame.font.SysFont("Clear Sans Regular", 30)
    leftpaddel = PADDEL(50, 50)
    rightpaddel = PADDEL(1220, 50)

    ball = BALL(int(WIDTH / 2), int(HEIGHT / 2))

    

    # Circle movement factor
    cmfX = 450
    cmfY = 450

    # Main Loop
    cancel = False

    def movepaddel(self, inputMap):
        
        if self.self.rightpaddel.getypos() < 0 - self.rightpaddel.getheight / 2:
            self.rightpaddel.setcmu(False)
        else:
            self.rightpaddel.setcmu(True)
        if self.rightpaddel.getypos() > self.HEIGHT - self.rightpaddel.getheight / 2:
            self.rightpaddel.setcmd(False)
        else:
            self.rightpaddel.setcmd(True)
        if self.leftpaddel.getypos() < 0 - self.leftpaddel.getheight / 2:
            self.leftpaddel.setcmu(False)
        else:
            self.leftpaddel.setcmu(True)
        if self.leftpaddel.getypos() > self.HEIGHT - self.leftpaddel.getheight / 2:
            self.leftpaddel.setcmd(False)
            self.leftpaddel.setcmd(True)

        if self.rightpaddel.getcmd() and inputMap[0]:
            self.rightpaddel.moveydown()
        if self.rightpaddel.getcmu() and inputMap[1]:
            self.rightpaddel.moveyup()
        if self.leftpaddel.getcmd() and inputMap[2]:
            self.leftpaddel.moveydown()
        if self.leftpaddel.getcmu() and inputMap[3]:
            self.leftpaddel.moveyup()

        # Circle movement
        circle_time_passed = clock.tick(60)
        circle_time_sec = circle_time_passed / 1000.0
        circle_posX += cmfX * circle_time_sec
        circle_posY += cmfY * circle_time_sec

        # Circle collision
        if circle_posY > HEIGHT or circle_posY < 0:
            cmfY = -cmfY
        if circle_posX > self.rightpaddel.getxpos() or circle_posX < self.leftpaddel.getxpos():
            if circle_posY > self.rightpaddel.getxpos() and circle_posY < self.rightpaddel.getxpos() + self.rightpaddel.getheight:
                cmfX = -cmfX
            if circle_posY > self.leftpaddel.getypos() and circle_posY < self.leftpaddel.getypos() + self.leftpaddel.getheight:
                cmfX = -cmfX

        if circle_posX > WIDTH:
            score_left += 1
            circle_posX = circle_start_posX
            circle_posY = circle_start_posY

        if circle_posX < 0:
            score_right += 1
            circle_posX = circle_start_posX
            circle_posY = circle_start_posY

        def updatescreen(self, scoreleft, scorright):
            self.screen.fill(self.green)

            pygame.draw.rect(self.screen, self.blue, [self.self.leftpaddel.getxpos(), self.self.leftpaddel.getypos(), 10, self.self.leftpaddel.getheight])
            pygame.draw.rect(self.screen, self.blue, [self.self.rightpaddel.getxpos(), self.self.rightpaddel.getxpos(), 10, self.self.rightpaddel.getheight])
            pygame.draw.rect(self.screen, self.red, [self.circle_posX, self.circle_posY, 20, 20])

            self.screen.blit(self.score_font.render(str(self.scoreleft), True, self.blue), (self.WIDTH / 4, 50))
            self.screen.blit(self.score_font.render(str(self.scoreright), True, self.blue), (self.WIDTH / 1.25, 50))

            pygame.display.flip()

