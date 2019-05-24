import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.PADDLE import PADDEL
from Pong.WINDOW import WINDOW
from Pong.SOUNDS import SOUNDS
import random


class GAMECONTROL:
    def __init__(self, resolution=(1920, 1080), gm='1v1', score=(0, 0)):
        """defines important variables: height and width of the screen, arrays for the event-handling, gamemode, score
        defines objects of other classes: game's clock, paddles, ball, window
        initiates pygame and the menu"""

        # variables:
        self.width, self.height = resolution  # sets the variables depending on the current resolution
        self.inputMap = [False, False, False, False]  # tells wich control keys are pressed
        self.focus = [False, False, False, False, False, False]  # tells which area the mouse is hovering over
        self.gamemode = gm  # sets the gamemode: either player vs player or computer vs player
        self.scoreleft, self.scoreright = score  # self explainatory, right? the score
        self.mousevisibility = True  # is the mouse even showing

        # objects
        self.clock = pygame.time.Clock()  # handles the timespans passing between operations,
        self.leftpaddle = PADDEL(0.1 * self.width, self.height / 2)  # paddle is created depending on the screens
        # resolution
        self.rightpaddle = PADDEL(0.9 * self.width, self.height / 2)  # paddle is created depending on the screens
        # resolution
        self.ball = BALL(self.width / 2, self.height / 2, (270 / 0.6 * random.choice([-1, 1]), 270 / 0.6 * random.
                                                           choice([-1, 1])))  # Ball is created depending on the screens
        # resolution, speed has a random direction
        self.spf = WINDOW(self.ball, self.leftpaddle, self.rightpaddle, resolution)  # WINDOW gets the objects to show
        # aswell as the resolution

        # start the game
        pygame.init()  # initiates pygame
        while True:
            self.mainmenu()  # shows the menu screen

    def matchstart(self):
        """creates a new screenFalse
           handles all objects floating on the screen
           waits for the first input to kickoff"""

        while self.scoreright < 10 and self.scoreleft < 10:  # make sure the game's not over yet
            self.spf.updategamescreen(self.scoreleft, self.scoreright)  # draw a frame of the game
            self.eventsingame()  # read the events
            if self.gamemode == '1v1':  # movement depending on the gamemode
                self.movepaddle1v1(self.inputMap)  # both paddles are controlled by people
            else:
                self.movepaddlesingleplayer(self.inputMap)  # only one paddle is under human control
            self.ballhandling(self.clock.tick(200))  # move the ball adequately and wait for a short time

    def kickoff(self):
        """wait for a the players to get ready"""
        pygame.mouse.set_visible(False)  # mouse won't show
        self.spf.kickoffscreen(self.scoreleft, self.scoreright, "PRESS SPACE")  # show the kickoff screen
        self.screen = "game"
        while True:
            self.eventsingame()  # read the events

    def mainmenu(self):
        """handles any settings, game pauses etc"""
        self.screen = "mainmenu"
        pygame.mouse.set_visible(True)  # mouse will show
        while True:
            """show the main menu and wait for an event"""
            self.eventsmenu()  # read the events
            self.spf.menuscreenmain(self.focus)  # show the menu-screen depending on where the mouse is

    def eventsingame(self):
        for event in pygame.event.get():  # get every event
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # all the key events
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:  # if space has been pressed
                    self.clock = pygame.time.Clock()  # reset the clock to prevent ball movement in kickoff screen
                    self.matchstart()  # let the match start / continue
                if pressed_keys[K_ESCAPE]:   # if escape has been pressed
                        self.mainmenu() # start the menu screen
                """now fill the input map for any paddle controlling keystroke"""
                self.inputMap[0] = pressed_keys[K_DOWN]  # right player: move down
                self.inputMap[1] = pressed_keys[K_UP]  # right player: move up
                self.inputMap[2] = pressed_keys[K_s]  # left player: move down
                self.inputMap[3] = pressed_keys[K_w]  # left player: move up

    def eventsmenu(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION and self.mousevisibility:  # if mouse has been moved you need to update
                # the focused area
                x, y = pygame.mouse.get_pos()  # get where the mouse is hovering
                if self.screen == "mainmenu":
                    self.focus[0] = y < self.height * 0.25 and self.width * 0.3 < x < self.width * 0.7
                    self.focus[1] = self.height * 0.25 < y < self.height * 5 / 12 and self.width * 0.3 < x < \
                        self.width * 0.7
                    self.focus[2] = self.height * 5 / 12 < y < self.height / 12 * 7 and self.width * 0.3 < x < \
                        self.width * 0.7
                    self.focus[3] = self.height / 12 * 7 < y < self.height * 0.75 and self.width * 0.3 < x < \
                        self.width * 0.7
                    self.focus[4] = y > self.height * 0.75 and self.width * 0.3 < x < self.width * 0.7
                    self.focus[5] = y < self.height * 0.25 and x > self.width * 0.7
                elif self.screen == "settings":
                    self.focus[0] = y < self.height * 0.25 and x > self.width * 0.8
                    self.focus[1] = y < self.height * 0.25 and self.width * 0.3 < x < self.width * 0.7
            if event.type == pygame.MOUSEBUTTONDOWN and self.mousevisibility:  # if mouse has been pressed, take action
                # depending on the current mouse position
                if self.screen == "mainmenu":
                    if self.focus[0]:
                        self.kickoff()  # will start the kickoff
                    elif self.focus[1]:
                        self.settings()  # will enter the 'settings' menu
                    elif self.focus[2]:
                        self.help()  # will enter the 'help' menu
                    elif self.focus[3]:
                        self.info()  # will enter the 'info' menu
                    elif self.focus[4]:
                        exit()  # will close the gamed
                    elif self.focus[5]:
                        self.resetscore()  # will reset the score
                elif self.screen == "settings":
                    if self.focus[0]:
                        self.mainmenu()
                    if self.focus[1]:
                        self.gamemode = "1v1" if self.gamemode != "1v1" else "1v0"

    def movepaddle1v1(self, inputmap):
        if self.rightpaddle.getypos() <= 1:  # paddle at minimum height
            self.rightpaddle.setcmu(False)  # no further upwards movement
        else:
            self.rightpaddle.setcmu(True)
        if self.rightpaddle.getypos() >= self.height - self.rightpaddle.getheight():  # paddle at maximum height
            self.rightpaddle.setcmd(False)  # no further
        else:
            self.rightpaddle.setcmd(True)
        if self.leftpaddle.getypos() < 1:
            self.leftpaddle.setcmu(False)
        else:
            self.leftpaddle.setcmu(True)
        if self.leftpaddle.getypos() >= self.height - self.rightpaddle.getheight():
            self.leftpaddle.setcmd(False)
        else:
            self.leftpaddle.setcmd(True)
        if self.rightpaddle.getcmd() and inputmap[0]:
            self.rightpaddle.moveydown()
        elif self.rightpaddle.getcmu() and inputmap[1]:
            self.rightpaddle.moveyup()
        if self.leftpaddle.getcmd() and inputmap[2]:
            self.leftpaddle.moveydown()
        elif self.leftpaddle.getcmu() and inputmap[3]:
            self.leftpaddle.moveyup()

    def movepaddlesingleplayer(self, inputmap):
        if self.rightpaddle.getypos() < 1:
            self.rightpaddle.setcmu(False)
        else:
            self.rightpaddle.setcmu(True)
        if self.rightpaddle.getypos() >= self.height - self.rightpaddle.getheight():
            self.rightpaddle.setcmd(False)
        else:
            self.rightpaddle.setcmd(True)
        if self.leftpaddle.getypos() < 1:
            self.leftpaddle.setcmu(False)
        else:
            self.leftpaddle.setcmu(True)
        if self.leftpaddle.getypos() >= self.height - self.rightpaddle.getheight():
            self.leftpaddle.setcmd(False)
        else:
            self.leftpaddle.setcmd(True)
        if self.rightpaddle.getcmd() and inputmap[0]:
            self.rightpaddle.moveydown()
        elif self.rightpaddle.getcmu() and inputmap[1]:
            self.rightpaddle.moveyup()

        if self.leftpaddle.getcmd() and self.ball.getypos() > self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:
            self.leftpaddle.moveydown()
        elif self.leftpaddle.getcmu() and self.ball.getypos() < self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:
            self.leftpaddle.moveyup()

    def ballhandling(self, clocktick):
        self.ball.move(clocktick / 1000.0)
        if not 21 < self.ball.getypos() < self.height - 21:
            self.ball.changeydirection()
            SOUNDS.play('soundfiles/jump.wav')
        if self.leftpaddle.getxpos() + 10 < self.ball.getxpos() < self.leftpaddle.getxpos() + 16:
            if self.leftpaddle.getypos() < self.ball.getypos() < self.leftpaddle.getypos() \
                    + self.leftpaddle.getheight():
                self.ball.changexdirection()
                SOUNDS.play('soundfiles/jump.wav')
                if self.inputMap[2]:
                    self.ball.add_mfy(self.rightpaddle.getmfy() * 10)
                elif self.inputMap[3]:
                    self.ball.add_mfy(-self.rightpaddle.getmfy() * 10)
        if self.rightpaddle.getxpos() - 16 < self.ball.getxpos() < self.rightpaddle.getxpos() - 10:
            if self.rightpaddle.getypos() < self.ball.getypos() < self.rightpaddle.getypos() + \
                    self.rightpaddle.getheight():
                self.ball.changexdirection()
                SOUNDS.play('soundfiles/jump.wav')
                if self.inputMap[0]:
                    self.ball.add_mfy(self.rightpaddle.getmfy() * 10)
                elif self.inputMap[1]:
                    self.ball.add_mfy(-self.rightpaddle.getmfy() * 10)
        if self.ball.getxpos() >= self.width:
            SOUNDS.play('soundfiles/shatter.wav')
            self.resetpaddles()
            self.goalleft()
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))
            self.kickoff()
        if self.ball.getxpos() < 1:
            SOUNDS.play('soundfiles/shatter.wav')
            self.resetpaddles()
            self.goalright()
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))
            self.kickoff()

    @staticmethod
    def clearlist(l, data):
        """clears any list full of booleans, came in handy with an earlier approach to the events of ours
        not used anymore"""
        for i in range(len(l)):
            l[i - 1] = data

    def settings(self):
        """the screen specifically made for the game's settings

        needs revision in WINDOW-class"""
        pygame.mouse.set_visible(True)  # mouse will show
        self.screen = "settings"
        while True:
            self.eventsmenu()  # read the events
            self.spf.menuscreensettings(self.focus)

    def help(self):
        """the screen specifically made for providing help, should point towards the github project

        needs revision in WINDOW-class"""
        while True:
            self.spf.menuscreenhelp()

    def info(self):
        """the screen for basic information about the game, credits

        needs revision in WINDOW-class"""
        while True:
            self.spf.menuscreeninfo()

    def goalright(self):
        """increases the right player's score by one"""
        self.scoreright += 1

    def goalleft(self):
        """increases the left player's score by one"""
        self.scoreleft += 1

    def resetpaddles(self):
        """sets both paddles back to the middle of the screen, used after a goal has been scored"""
        self.rightpaddle.setypos(self.height / 2)
        self.leftpaddle.setypos(self.height / 2)

    def increaseballspeed(self):
        """speeds up the ball in both x and y direction (but by different values)

        currently unused"""
        self.ball.add_mfx(9 * self.ball.mfx / abs(self.ball.mfx))
        self.ball.add_mfy(3 * self.ball.mfy / abs(self.ball.mfy))

    def resetscore(self):
        """sets both scores back to 0
        used to rematch or to restart a running game

        needs output like 'successfully reset score' -> WINDOW-class """
        self.scoreleft = 0
        self.scoreright = 0
