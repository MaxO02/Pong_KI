import pygame.mixer


class SOUNDS:

    @staticmethod
    def play(path):
        """initiates the output of the soundfile with the directory-path path
        Does not wait for the sound to be finished"""
        pygame.mixer.init(22100, -16, 2, 64)
        pygame.mixer.Sound(path).play(loops=0, maxtime=0, fade_ms=0)

    @staticmethod
    def playandquit(path):
        """initiates the output of the soundfile with the directory-path path
        Does wait for the sound to be finished"""
        pygame.mixer.init(22100, -16, 2, 64)
        sound = pygame.mixer.Sound(path)
        sound.play(loops=0, maxtime=0, fade_ms=0)
        pygame.time.delay(int(sound.get_length() * 1000))
        pygame.mixer.quit()
        del sound
