from Pong.SPIELFELD import SPIELFELD
import pygame
class THEMAINMASTER:
    def __init__(self):

        spf = SPIELFELD(self)

        pygame.init()
        self.clock = pygame.time.Clock()

        self.scoreleft = 0
        self.scoreright = 0

        inputMap = [False, False, False, False]

        cancel = False

        while not cancel:
            if self.scoreright == 10 or self.scoreleft == 10:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cancel = True
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        inputMap[0] = True
                    if event.key == pygame.K_UP:
                        inputMap[1] = True
                    if event.key == pygame.K_s:
                        inputMap[2] = True
                    if event.key == pygame.K_w:
                        inputMap[3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        inputMap[0] = False
                    if event.key == pygame.K_UP:
                        inputMap[1] = False
                    if event.key == pygame.K_s:
                        inputMap[2] = False
                    if event.key == pygame.K_w:
                        inputMap[3] = False

            spf.movepaddel(inputMap)
            spf.ballhandeling(self.clock.tick(60))
            spf.updatescreen(self.scoreleft, self.scoreright)

            self.clock.tick(60)

    def goalright(self):
        self.scoreright += 1

    def goalleft(self):
        self.scoreleft += 1

    def getscreen(self):
        return self.screen

tmm = THEMAINMASTER()