import pygame.mixer


class SOUNDS:

    @staticmethod
    def play(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does not wait for the sound to be finished"""
        pygame.mixer.init(22100, 16, allowedchanges=64)
        pygame.mixer.Sound(path).play()

    @staticmethod
    def playandquit(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does wait for the sound to be finished"""
        pygame.mixer.init(22100, -16, 2, 64)
        sound = pygame.mixer.Sound(path)
        sound.play()
        pygame.time.delay(int(sound.get_length() * 1000))
        pygame.mixer.quit()
        del sound

    @staticmethod
    def backgroundmusicqueue() -> None:
        pygame.init()
        pygame.mixer.init(22100, 16, 2, 64)
        pygame.mixer.music.load('soundfiles/background.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
