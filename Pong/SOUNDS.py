import pygame.mixer


class SOUNDS:

    @staticmethod
    def play(path):
        pygame.mixer.init(22100, -16, 2, 64)
        pygame.mixer.Sound(path).play(loops=0, maxtime=0, fade_ms=0)
