import pygame.mixer


class SOUNDS:

    @staticmethod
    def play(path):
        pygame.mixer.init(22100, -16, 2, 64)
        pygame.mixer.Sound(path).play(loops=0, maxtime=0, fade_ms=0)

    @staticmethod
    def playandquit(path):
        pygame.mixer.init(22100, -16, 2, 64)
        sound = pygame.mixer.Sound(path)
        sound.play(loops=0, maxtime=0, fade_ms=0)
        print(sound.get_length()*1000)
        pygame.time.delay(int(sound.get_length() * 1000))
        pygame.mixer.quit()
        del sound
