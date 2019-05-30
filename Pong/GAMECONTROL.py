import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.PADDLE import PADDEL
from Pong.WINDOW import WINDOW
from Pong.SOUNDS import SOUNDS
import webbrowser
import random


class GAMECONTROL:
    def __init__(self, resolution=(1920, 1080), gm='1v1', score=(0, 0)) -> None:
        """defines important variables: height and width of the screen, arrays for the event-handling, gamemode, score
        defines objects of other classes: game's clock, paddles, ball, window
        initiates pygame and the menu"""

        # variables:
        self.width, self.height = resolution  # sets the variables depending on the current resolution
        self.inputMap = [False, False, False, False]  # tells wich control keys are pressed
        self.focus = [False, False, False, False, False, False]  # tells which area the mouse is hovering over
        self.enemymode = gm  # sets the enemymode: either player vs player or computer vs player
        self.scoreleft, self.scoreright = score  # self explainatory, right? the score
        self.screens = {"game": False, "mainmenu": True, "settings": False, "help": False, "info": False, "resmenu": False, "thememenu": False}  # which screen is active
        self.enemymodes = {"1v1": '1v1' == gm, "1v0": '1v0' == gm}  # wich enemy mode is active
        self.inputresolution = ''  # which new resolution has been input
        self.screen = ''  # which screen is active
        self.newcolors = ["", "", ""]
        self.backgroundmusic = False
        self.newcolor = [None, None, None]

        # themes
        self.experimentaltheme = ((255, 255, 0), (255, 0, 0), (0, 0, 255))  # strange looking  theme
        self.defaulttheme = ((254, 115, 1), (85, 57, 138), (1, 254, 240))  # best looking  theme

        # objects
        self.clock = pygame.time.Clock()  # handles the timespans passing between operations,
        self.leftpaddle = PADDEL(0.1 * self.width, self.height / 2)  # paddle is created depending on the screens resolution
        self.rightpaddle = PADDEL(0.9 * self.width, self.height / 2)  # paddle is created depending on the screens resolution
        self.ball = BALL(self.width / 2, self.height / 2, (270 / 0.6 * random.choice([-1, 1]), 270 / 0.6 * random.choice([-1, 1])))  # Ball is created depending on the screens resolution, speed has a random direction
        self.spf = WINDOW(self.ball, self.leftpaddle, self.rightpaddle, resolution, self.defaulttheme)  # WINDOW gets the objects to show aswell as the resolution

        # start the game
        pygame.init()  # initiates pygame
        # starts the annoying music in the background
        if self.backgroundmusic: SOUNDS.backgroundmusicqueue()
        self.mainmenu()  # shows the menu screen

    def matchstart(self) -> None:
        """creates a new screenFalse
           handles all objects floating on the screen
           waits for the first input to kickoff"""
        self.screen = 'game'  # sets the screen to 'game'
        while self.scoreright < 10 and self.scoreleft < 10:  # make sure the game's not over yet
            self.spf.updategamescreen(self.scoreleft, self.scoreright)  # draw a frame of the game
            self.eventsingame()  # read the events
            if self.enemymode == "1v1":  # movement depending on the enemymode
                self.movepaddle1v1(self.inputMap)  # both paddles are controlled by people
            else:
                self.movepaddlesingleplayer(self.inputMap)  # only one paddle is under human control
            self.ballhandling(self.clock.tick(200))  # move the ball adequately and wait for a short time
        else:
            self.mainmenu()  # should rather be a victory screen

    def kickoff(self) -> None:
        """wait for a the players to get ready"""
        pygame.mouse.set_visible(False)  # mouse won't show
        self.screen = "kickoff"  # sets the screen to 'kickoff'
        while True:
            self.eventsingame()  # read the events
            self.spf.kickoffscreen(self.scoreleft, self.scoreright, "PRESS SPACE")  # show the kickoff screen

    def mainmenu(self) -> None:
        """handles any settings, game pauses etc"""
        self.screen = "mainmenu"  # sets the screen to 'mainmenu'
        pygame.mouse.set_visible(True)  # mouse will show
        while True:
            """show the main menu and wait for an event"""
            self.eventsmenu()  # read the events
            self.spf.menuscreenmain(self.focus)  # show the menu-screen depending on where the mouse is

    def eventsingame(self) -> None:
        for event in pygame.event.get():  # get every event
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # all the key events
                pressed_keys = pygame.key.get_pressed()  # gets which keys are  being pressed
                if pressed_keys[K_SPACE] and self.screen == 'kickoff':  # if space has been pressed
                    SOUNDS.play("soundfiles/start.wav")
                    self.clock = pygame.time.Clock()  # reset the clock to prevent ball movement in kickoff screen
                    self.matchstart()  # let the match start / continue
                if pressed_keys[K_ESCAPE]:   # if escape has been pressed
                        self.mainmenu() # start the menu screen
                if pressed_keys[K_r]:
                    self.spf.changetheme(((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))  # actually changes the theme to a random one
                """now fill the input map for any paddle controlling keystroke"""
                self.inputMap[0] = pressed_keys[K_DOWN]  # right player: move down
                self.inputMap[1] = pressed_keys[K_UP]  # right player: move up
                self.inputMap[2] = pressed_keys[K_s]  # left player: move down
                self.inputMap[3] = pressed_keys[K_w]  # left player: move up
            if event.type == pygame.QUIT:  # in case one wants to close the window
                exit()  # exit pygame and therefore close the window

    def eventsmenu(self) -> None:
        for event in pygame.event.get():  # get every event
            if event.type == pygame.MOUSEMOTION:  # if mouse has been moved you need to update the focused area
                x, y = pygame.mouse.get_pos()  # get where the mouse is hovering
                if not self.screen == "custometheme":
                    for i in range(0, len(self.focus)):
                        self.focus[i] = self.height / 6 * i - self.height / 12 < y < self.height / 6 * i + self.height / 12 and self.width * 0.3 < x < self.width * 0.7 if not i == 0 else y < self.height * 0.25 and x > self.width * 0.7
                else:
                    for i in range(0, len(self.focus)):
                        self.focus[i] = self.height / 6 * i+0.5 - self.height / 12 < y < self.height / 6 * (i+0.5) + self.height / 12 and self.width * 0.3 < x < self.width * 0.7 if not i == 0 else y < self.height * 0.25 and x > self.width * 0.7

            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse has been pressed, take action depending on the current mouse position
                if self.screen == "mainmenu":  # depends on which screen you are
                    if self.focus[1]:
                        self.kickoff()  # will start the kickoff
                    elif self.focus[2]:
                        self.settings()  # will enter the 'settings' menu
                    elif self.focus[3]:
                        self.help()  # will open the github help page
                    elif self.focus[4]:
                        self.info()  # will enter the github readme file
                    elif self.focus[5]:
                        exit()  # will close the game
                    elif self.focus[0]:
                        self.resetscore()  # will reset the score
                elif self.screen == "settings":  # depends on which screen you are
                    if self.focus[0]:
                        self.mainmenu()  # back to main menu
                    elif self.focus[1]:
                        self.enemymode = "1v1" if self.enemymode != "1v1" else "1v0"  # switch the enemymode
                    elif self.focus[2]:
                        self.resmenu()  # here you can switch the screen's resolution
                    elif self.focus[3]:
                        self.thememenu()  # here you can switch the theme of the game screen
                elif self.screen == "resmenu":
                    if self.focus[0]:
                        self.settings()  # back to settings menu
                elif self.screen == "thememenu":
                    if self.focus[0]:
                        self.settings()  # back to settings menu
                    elif self.focus[1]:
                        self.spf.changetheme(self.defaulttheme)
                        self.settings()  # back to settings menu
                    elif self.focus[2]:
                        self.spf.changetheme(self.experimentaltheme)  # actually changes the theme to experimental
                        self.settings()  # back to settings menu
                    elif self.focus[3]:
                        self.spf.changetheme(((255, 255, 255), (255, 255, 255), (0, 0, 0)))  # actually changes the theme to black-and-white
                        self.settings()  # back to settings menu
                    elif self.focus[4]:
                        self.spf.changetheme(((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))  # actually changes the theme to a random one
                        self.settings()  # back to settings menu
                    elif self.focus[5]:
                        self.spf.setactivebox(0)
                        self.custometheme()
                        self.settings()  # back to settings menu
                elif self.screen == "custometheme":
                    if self.focus[0]:
                        self.thememenu()
                    elif self.focus[1]:
                        self.spf.setactivebox(1)
                    elif self.focus[2]:
                        self.spf.setactivebox(2)
                    elif self.focus[3]:
                        self.spf.setactivebox(3)
            if event.type == pygame.QUIT:  # close the window
                exit()
            if event.type == KEYDOWN:
                if self.screen == "resmenu":
                    if event.key == pygame.K_RETURN:
                        res = self.inputresolution.split("x")
                        try:
                            newres = int(res[0]), int(res[1])
                            self.spf.changeresolution(newres)
                        except Exception as e:
                            print(e)
                            self.spf.resmenuerror()
                        self.inputresolution = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.inputresolution = self.inputresolution[:-1]  # delete the last input character
                    else:
                        self.inputresolution += event.unicode
                elif self.screen == "custometheme":
                    if event.key == pygame.K_RETURN:
                        RGB = self.newcolors[self.spf.getactivebox()-1].split(",")
                        try:
                            self.newcolor[self.spf.getactivebox()-1] = (int(RGB[0]), int(RGB[1]), int(RGB[2]))

                            if self.newcolor[0] != None and self.newcolor[1] != None and self.newcolor[2] != None:
                                newtheme = self.newcolor[0], self.newcolor[1], self.newcolor[2]
                                self.spf.changetheme(newtheme)
                                self.newcolor = [None, None, None]
                        except Exception as e:
                            print(e)
                        self.newcolors[self.spf.getactivebox()-1] = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.newcolors[self.spf.getactivebox()-1] = self.newcolors[self.spf.getactivebox()-1][:-1]
                    else:
                        self.newcolors[self.spf.getactivebox()-1] += event.unicode

    def movepaddle1v1(self, inputmap) -> None:
        self.rightpaddle.setcmu(self.rightpaddle.getypos() > 1)  # blocks right movement on top of the screen
        self.rightpaddle.setcmd(self.rightpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks right's movement on the bottom of the screen
        self.leftpaddle.setcmu(self.leftpaddle.getypos() > 1)  # blocks left movement on top of the screen
        self.leftpaddle.setcmd(self.leftpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks left's movement on the bottom of the screen
        if self.rightpaddle.getcmd() and inputmap[0]:  # in case K_DOWN is pressed
            self.rightpaddle.moveydown()  # move rightpaddle down
        elif self.rightpaddle.getcmu() and inputmap[1]:  # in case K_UP is pressed
            self.rightpaddle.moveyup()  # move rightpaddle up
        if self.leftpaddle.getcmd() and inputmap[2]:  # in case K_S is pressed
            self.leftpaddle.moveydown()  # move leftpaddle down
        elif self.leftpaddle.getcmu() and inputmap[3]:  # in case K_W is pressed
            self.leftpaddle.moveyup()  # move leftpaddle up

    def movepaddlesingleplayer(self, inputmap) -> None:
        self.rightpaddle.setcmu(self.rightpaddle.getypos() > 1)  # blocks right movement on top of the screen
        self.rightpaddle.setcmd(self.rightpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks right's movement on the bottom of the screen
        self.leftpaddle.setcmu(self.leftpaddle.getypos() > 1)  # blocks left movement on top of the screen
        self.leftpaddle.setcmd(self.leftpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks left's movement on the bottom of the screen
        if self.rightpaddle.getcmd() and inputmap[0]:  # in case K_DOWN is pressed
            self.rightpaddle.moveydown()  # move rightpaddle down
        elif self.rightpaddle.getcmu() and inputmap[1]:  # in case K_UP is pressed
            self.rightpaddle.moveyup()  # move rightpaddle up
        if self.leftpaddle.getcmd() and self.ball.getypos() > self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:  # in case the ball is lower than the left paddle
            self.leftpaddle.moveydown()  # move leftpaddle down
        elif self.leftpaddle.getcmu() and self.ball.getypos() < self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:  # in case the ball is higher than the left paddle
            self.leftpaddle.moveyup()  # move leftpaddle up

    def ballhandling(self, clocktick) -> None:
        self.ball.move(clocktick / 1000.0)  # ball should relocate itself according to it's speed and the time

        if not 21 < self.ball.getypos() < self.height - 21:  # in case the ball touches the bottom or the top
            self.ball.changeydirection()  # change balls direction of movement in y
            SOUNDS.play(random.choice(['soundfiles/bing1.wav', 'soundfiles/bing2.wav']))  # play a bump sound
        if self.leftpaddle.getxpos() + 10 < self.ball.getxpos() < self.leftpaddle.getxpos() + 16:  # in case the ball is in left paddles x-range
            if self.leftpaddle.getypos() - 10 < self.ball.getypos() < self.leftpaddle.getypos() + self.leftpaddle.getheight() + 10:  # in case the ball is in left paddles y-range
                self.ball.changexdirection()  # make ball jump
                SOUNDS.play(random.choice(['soundfiles/bing2.wav', 'soundfiles/bing1.wav']))  # play jumping shot
                if self.inputMap[2] or self.inputMap[3]:  # if left paddle is moving
                    self.increaseballspeed()  # speed up the ball
        if self.rightpaddle.getxpos() - 16 < self.ball.getxpos() < self.rightpaddle.getxpos() - 10:  # in case the ball is in right paddles x-range
            if self.rightpaddle.getypos() - 10 < self.ball.getypos() < self.rightpaddle.getypos() + self.rightpaddle.getheight() + 10:  # in case the ball is in right paddles y-range
                self.ball.changexdirection()  # make ball jump
                SOUNDS.play(random.choice(['soundfiles/bing2.wav', 'soundfiles/bing1.wav']))  # play jumping shot
                if self.inputMap[0] or self.inputMap[1]:  # if right paddle is moving
                    self.increaseballspeed()  # speed up the ball
        if self.ball.getxpos() >= self.width:  # if the ball is touching the right side of the screen
            SOUNDS.play('soundfiles/win.ogg')  # play goal sound
            self.resetpaddles()  # replace paddles to the middle
            self.goalleft()  # add a goal for left
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # reset the balls position
            self.kickoff()  # wait for input to play another round
        if self.ball.getxpos() < 1:  # if the ball is touching the left side of the screen
            SOUNDS.play('soundfiles/win.ogg')  # play goal sound
            self.resetpaddles()  # replace paddles to the middle
            self.goalright()  # add a goal for left
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # reset the balls position
            self.kickoff()  # wait for input to play another round

    @staticmethod
    def clearlist(l, data) -> None:
        """clears any list full of booleans, came in handy with an earlier approach to the events of ours
        not used anymore"""
        for i in range(len(l)):  # for every position in given array
            l[i - 1] = data  # place given data
        return l  # and then return the cleared list

    def settings(self) -> None:
        """the screen specifically made for the game's settings"""
        pygame.mouse.set_visible(True)  # mouse will show
        self.screen = "settings"  # sets the screen variable to 'settings'
        while True:
            self.eventsmenu()  # read the events
            self.spf.menuscreensettings(self.focus)  # draws the right menu screen

    def help(self) -> None:
        """the screen specifically made for providing help, should point towards the github project"""
        webbrowser.open("https://github.com/MaxO02/Pong_KI/issues")  # opens the github issue page in web browser

    def info(self) -> None:
        webbrowser.open("https://github.com/MaxO02/Pong_KI/blob/master/README.md")  # opens the github README file  in web browser

    def resmenu(self) -> None:
        """the screen for changing the resolution"""
        self.screen = "resmenu"  # sets the screen variable to 'resmenu'
        while True:
            self.width, self.height = self.spf.giveresolution()  # reads the resolution from the screen
            self.eventsmenu()  # reads necessary events
            self.spf.menuscreenresolution(self.focus, self.inputresolution)  # draws the screen for changing the  resolution

    def thememenu(self) -> None:
        self.screen = "thememenu"  # sets the screen variable to 'resmenu'
        while True:
            self.eventsmenu()  # reads necessary events
            self.spf.menutheme(self.focus)  # draws the screen for changing the theme

    def custometheme(self) -> None:
        self.screen = "custometheme"
        while True:
            self.eventsmenu()
            self.spf.menucustometheme(self.focus, self.newcolors)

    def goalright(self) -> None:
        """increases the right player's score by one"""
        self.scoreright += 1  # increases the goal count right by one
        self.spf.scorereset(True)  # there is a score to be reset

    def goalleft(self) -> None:
        """increases the left player's score by one"""
        self.scoreleft += 1  # increases the goal count right by one
        self.spf.scorereset(True)  # there is a score to be reset

    def resetpaddles(self) -> None:
        """sets both paddles back to the middle of the screen, used after a goal has been scored"""
        self.rightpaddle.setypos(self.height / 2)  # sets right paddle to the middle of the screen
        self.leftpaddle.setypos(self.height / 2)  # sets left paddle to the middle of the screen

    def increaseballspeed(self) -> None:
        """speeds up the ball in both x and y direction (but by different values)"""
        self.ball.add_mfy(45 * self.ball.mfy / abs(self.ball.mfy))  # speeds up the  ball in y direction, always increases speed
        self.ball.add_mfx(30 * self.ball.mfx / abs(self.ball.mfx))  # speeds up the  ball in x direction, always increases speed

    def resetscore(self) -> None:
        """sets both scores back to 0
        used to rematch or to restart a running game"""
        self.scoreleft = 0  # sets back the left score to zero
        self.scoreright = 0  # sets back the left score to zero
        self.spf.scorereset(False)  # no score to be reset anymore
        self.resetpaddles()  # resets the paddles to middle position
        self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # puts ball back to it's original position
