import pygame.mixer


class SOUNDS:

    @staticmethod
    def play(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does not wait for the sound to be finished"""
        try:
            pygame.mixer.init(22100, 16, allowedchanges=64)  # initiates the pygame mixer
            pygame.mixer.Sound(path).play()  # plays the soundfile from the given path
        except Exception:
            pass

    @staticmethod
    def playandquit(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does wait for the sound to be finished"""
        try:
            pygame.mixer.init(22100, -16, 2, 64)  # initiates the pygame mixer
            sound = pygame.mixer.Sound(path)  # gets the soundfile from path
            sound.play()  # plays the sound
            pygame.time.delay(int(sound.get_length() * 1000))  # delays for sounds duration
            pygame.mixer.quit()  # closes the mixer
            del sound  # removes the variable
        except Exception:
            pass

    @staticmethod
    def backgroundmusicqueue(bool) -> None:
        pygame.init()  # initiates the pygame mixer
        try:
            pygame.mixer.init(22100, 16, 2, 64)  # initiates the pygame mixer
            pygame.mixer.music.load('soundfiles/background.mp3')  # loads soundfile from path
            pygame.mixer.music.set_volume(0.2)  # sets the volume
            if bool:
                pygame.mixer.music.play(-1)  # plays endless loop
            else:
                return
        except Exception :
            pass