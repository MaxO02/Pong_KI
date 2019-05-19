import pygame


class SOUNDS:

    @staticmethod
    def play(path):
        pygame.mixer.init(22100, -16, 2, 64)
        sound = pygame.mixer.Sound(path)
        sound.play(loops=0, maxtime=0, fade_ms=0)
