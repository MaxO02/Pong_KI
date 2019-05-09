from Pong.SPIELFELD import SPIELFELD
import pygame
class THEMAINMASTER:
    def __init__(self):
        spf = SPIELFELD()

        pygame.init()
        clock = pygame.time.Clock()

        cancel = False

        while not cancel:
            self.scoreleft = 1
            self.scoreright = 5














            spf.updatescreen(self.scoreleft, self.scorright)
            clock.tick(60)

