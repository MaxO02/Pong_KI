import pygame
import webbrowser
import random
import configparser
from time import sleep
import multitasking
import pygame.mixer
import math


config = configparser.ConfigParser()
config.read("config.cfg")


class GAMECONTROL:
    def __init__(self, resolution=(int(config.get("Settings", "reswidth")), int(config.get("Settings", "reslength"))), gm=config.get("Settings", "gamemode"), score=(0, 0)) -> None:
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
        self.backgroundmusic = config.get("Settings", "bgmusic") == "True"
        self.newcolor = [None, None, None]
        self.mbu2 = self.mbd2 = False
        self.mbu1 = self.mbd1 = False

        # themes
        self.experimentaltheme = ((255, 255, 0), (255, 0, 0), (0, 0, 255))  # strange looking  theme
        self.defaulttheme = ((254, 115, 1), (85, 57, 138), (1, 254, 240))  # best looking  theme

        # creates the starting theme from the config file
        colors = list(filter(None, config.get("Settings", "theme").replace(")", "(").replace(",", "(").replace(" ", "(").split("(")))
        starttheme = ((int(colors[0]), int(colors[1]), int(colors[2])), (int(colors[3]), int(colors[4]), int(colors[5])), (int(colors[6]), int(colors[7]), int(colors[8])))

        # objects
        self.clock = pygame.time.Clock()  # handles the timespans passing between operations,
        self.leftpaddle = PADDEL(0.1 * self.width, self.height / 2)  # paddle is created depending on the screens resolution
        self.rightpaddle = PADDEL(0.9 * self.width, self.height / 2)  # paddle is created depending on the screens resolution
        self.ball = BALL(self.width / 2, self.height / 2, (270 / 0.6 * random.choice([-1, 1]), 270 / 0.6 * random.choice([-1, 1])))  # Ball is created depending on the screens resolution, speed has a random direction
        self.spf = WINDOW(self.ball, self.leftpaddle, self.rightpaddle, resolution, starttheme)  # WINDOW gets the objects to show aswell as the resolution
        self.bc = BOUNCECONTROL(self.ball, self.leftpaddle, self.rightpaddle)

        # start the game
        pygame.init()  # initiates pygame
        # starts the annoying music in the background
        SOUNDS.backgroundmusicqueue(self.backgroundmusic)
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
                if pressed_keys[pygame.K_SPACE] and self.screen == 'kickoff':  # if space has been pressed
                    SOUNDS.play("soundfiles/start2.wav")
                    self.clock = pygame.time.Clock()  # reset the clock to prevent ball movement in kickoff screen
                    self.matchstart()  # let the match start / continue
                if pressed_keys[pygame.K_ESCAPE]:   # if escape has been pressed
                        self.mainmenu()  # start the menu screen
                if pressed_keys[pygame.K_r]:
                    self.spf.changetheme(((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))  # actually changes the theme to a random one
                """now fill the input map for any paddle controlling keystroke"""
                self.inputMap[0] = pressed_keys[pygame.K_DOWN]  # right player: move down
                self.inputMap[1] = pressed_keys[pygame.K_UP]  # right player: move up
                self.inputMap[2] = pressed_keys[pygame.K_s]  # left player: move down
                self.inputMap[3] = pressed_keys[pygame.K_w]  # left player: move up
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
                        config['Settings']['gamemode'] = self.enemymode = "1v1" if self.enemymode != "1v1" else "1v0"  # switch the enemymode
                        with open('config.cfg', 'w') as configfile:  # opens the config file
                            config.write(configfile)  # writes to the file
                    elif self.focus[2]:
                        self.resmenu()  # here you can switch the screen's resolution
                    elif self.focus[3]:
                        self.thememenu()  # here you can switch the theme of the game screen
                    elif self.focus[4]:
                        self.backgroundmusic = not self.backgroundmusic
                        config['Settings']['bgmusic'] = "True" if self.backgroundmusic else "False"
                        SOUNDS.backgroundmusicqueue(self.backgroundmusic)
                        with open('config.cfg', 'w') as configfile:  # opens the config file
                            config.write(configfile)  # writes to the file
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
                self.bc.stopall()
                exit()
            if event.type == pygame.KEYDOWN:
                if self.screen == "resmenu":
                    if event.key == pygame.K_RETURN:
                        res = self.inputresolution.split("x")
                        try:
                            newres = int(res[0]), int(res[1])
                            self.spf.changeresolution(newres)
                            config['Settings']["reswidth"] = res[0]  # saves the width to the config
                            config['Settings']['reslength'] = res[1]  # saves the length to the config
                            with open('config.cfg', 'w') as configfile:  # opens the config file
                                config.write(configfile)  # writes to the file
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
                            if self.newcolor[0] is not None and self.newcolor[1] is not None and self.newcolor[2] is not None:
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
            self.mbd1 = True
        elif self.mbd1:
            self.rightpaddle.reset()
            self.mbd1 = False
        elif self.rightpaddle.getcmu() and inputmap[1]:  # in case K_UP is pressed
            self.rightpaddle.moveyup()  # move rightpaddle up
            self.mbu1 = True
        elif self.mbu1:
            self.rightpaddle.reset()
            self.mbu1 = False
        if self.leftpaddle.getcmd() and inputmap[2]:  # in case K_S is pressed
            self.leftpaddle.moveydown()  # move leftpaddle down
            self.mbd2 = True
        elif self.mbd2:
            self.leftpaddle.reset()
            self.mbd2 = False
        elif self.leftpaddle.getcmu() and inputmap[3]:  # in case K_W is pressed
            self.leftpaddle.moveyup()  # move leftpaddle up
            self.mbu2 = True
        elif self.mbu2:
            self.leftpaddle.reset()
            self.mbu2 = False

    def movepaddlesingleplayer(self, inputmap) -> None:
        self.rightpaddle.setcmu(self.rightpaddle.getypos() > 1)  # blocks right movement on top of the screen
        self.rightpaddle.setcmd(self.rightpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks right's movement on the bottom of the screen
        self.leftpaddle.setcmu(self.leftpaddle.getypos() > 1)  # blocks left movement on top of the screen
        self.leftpaddle.setcmd(self.leftpaddle.getypos() < self.height - self.rightpaddle.getheight())  # blocks left's movement on the bottom of the screen
        if self.rightpaddle.getcmd() and inputmap[0]:  # in case K_DOWN is pressed
            self.rightpaddle.moveydown()  # move rightpaddle down
            self.mbd1 =True
        elif self.mbd1:
            self.rightpaddle.reset()
            self.mbd1 = False
        elif self.rightpaddle.getcmu() and inputmap[1]:  # in case K_UP is pressed
            self.rightpaddle.moveyup()  # move rightpaddle up
            self.mbu1 = True
        elif self.mbu1:
            self.rightpaddle.reset()
            self.mbu1 = False
        if self.leftpaddle.getcmd() and self.ball.getypos() > self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:  # in case the ball is lower than the left paddle
            self.leftpaddle.moveydown()  # move leftpaddle down
            self.mbd2 = True
        elif self.mbd2:
            self.leftpaddle.reset()
            self.mbd2 = False
        elif self.leftpaddle.getcmu() and self.ball.getypos() < self.leftpaddle.getypos()+self.leftpaddle.getheight()/2:  # in case the ball is higher than the left paddle
            self.leftpaddle.moveyup()  # move leftpaddle up
            self.mbu2 = True
        elif self.mbu2:
            self.leftpaddle.reset()
            self.mbu2 = False

    def ballhandling(self, clocktick) -> None:
        self.ball.move(clocktick / 1000.0)  # ball should relocate itself according to it's speed and the time
        if self.ball.getxpos() >= self.width:  # if the ball is touching the right side of the screen
            SOUNDS.play('soundfiles/win2.wav')  # play goal sound
            self.resetpaddles()  # replace paddles to the middle
            self.goalleft()  # add a goal for left
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # reset the balls position
            self.kickoff()  # wait for input to play another round
        if self.ball.getxpos() < 1:  # if the ball is touching the left side of the screen
            SOUNDS.play('soundfiles/win2.wav')  # play goal sound
            self.resetpaddles()  # replace paddles to the middle
            self.goalright()  # add a goal for left
            self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # reset the balls position
            self.kickoff()  # wait for input to play another round
        self.bc.bounce((self.width, self.height))


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
        self.spf.scorereset(False)  # no scoreFalse to be reset anymore
        self.resetpaddles()  # resets the paddles to middle position
        self.ball.reset((0.25 * self.width * random.choice([-1, 1]), 0.25 * self.height * random.choice([-1, 1])))  # puts ball back to it's original position


class PADDEL:

    def __init__(self, positionx, positiony) -> None:
        self.posx = positionx  # sets the x position
        self.posy = positiony  # sets the y position
        self.mf = self.basemf = 1   # sets the speed of movement
        self.canmoveup = True    # can paddle go higher
        self.canmovedown = True  # paddle go lower
        self.height = 150  # sets the height of the paddle

    def getxpos(self) -> int:
        return self.posx  # returns the x position

    def setxpos(self, newxpos) -> None:
        self.posx = newxpos  # sets the x position to given value

    def getypos(self) -> int:
        return self.posy  # returns the y position

    def setypos(self, newypos) -> None:
        self.posy = newypos  # sets the y position to given value

    def moveyup(self) -> None:
        self.posy -= self.mf  # moves the paddle up by one iteration
        self.mf = self.mf + 1 if self.mf < 7 else 7

    def moveydown(self) -> None:
        self.posy += self.mf  # moves the paddle down by one iteration
        self.mf = self.mf + 1 if self.mf < 7 else 7

    def getmfy(self) -> float:
        return self.mf  # returns the speed of movement

    def setcmd(self, boolean) -> None:
        self.canmovedown = boolean  # sets the movement boolean down to given value

    def setcmu(self, boolean) -> None:
        self.canmoveup = boolean  # sets the movement boolean up to given value

    def getcmd(self) -> bool:
        return self.canmovedown  # returns the movement down boolean

    def getcmu(self) -> bool:
        return self.canmoveup  # returns the movement up boolean

    def getheight(self) -> int:
        return self.height  # returns the paddle height

    def reset(self):
        self.mf = self.basemf


class BALL:
    def __init__(self, startxpos, startypos, mfspeed):
        self.startx = self.xpos = startxpos  # sets current x position aswell as x starting position
        self.starty = self.ypos = startypos  # sets current y position aswell as y starting position
        self.mfx, self.mfy = mfspeed  # sets current x speed aswell as y speed
        self.turnedx = False  # no x turn happened just now
        self.turnedy = False  # no y turn happened just now

    def reset(self, mfspeed) -> None:
        self.xpos = self.startx  # resets the x position to starting position
        self.ypos = self.starty  # resets the y position to starting position
        self.mfx, self.mfy = mfspeed  # sets the new speeds to given values

    def getxpos(self) -> int:
        return self.xpos  # returns the x position

    def getypos(self) -> int:
        return self.ypos  # returns the y position

    def setpos(self, position) -> None:
        self.xpos, self.ypos = position  # sets the position to given value

    def move(self, timesec) -> None:
        self.xpos += self.mfx * timesec  # moves the ball in x direction
        self.ypos += self.mfy * timesec  # moves the ball in y direction

    def changeydirection(self) -> None:
        if not self.turnedy:  # prevents the ball from getting stuck in a wall
            self.turnedy = True  # ball just turned in y direction
            self.mfy = -self.mfy  # inverts the movement
            self.resetturnedy()  # will wait to reset the turnedy

    def changexdirection(self) -> None:
        if not self.turnedx:  # prevents the ball from getting stuck in a wall
            self.turnedx = True  # ball just turned in x direction
            self.mfx = -self.mfx  # inverts the movement
            self.resetturnedx()  # will wait to reset the turnedy

    def setstartpos(self, coords) -> None:
        self.startx, self.starty = coords  # sets  the starting position to new coordinates

    def add_mfx(self, deltav) -> None:
        self.mfx += deltav  # adds x movement speed

    def add_mfy(self, deltav) -> None:
        self.mfy += deltav  # adds y movement speed

    def give_mfx(self) -> int:
        return self.mfx

    def give_mfy(self) -> int:
        return self.mfy

    def set_mf(self, mf):
        self.mfx, self.mfy = mf

    @multitasking.task
    def resetturnedx(self) -> None:
        sleep(0.5)  # waits for half a second
        self.turnedx = False  # sets back boolean

    @multitasking.task
    def resetturnedy(self) -> None:
        sleep(0.5)  # waits for half a second
        self.turnedy = False  # sets back boolean


class WINDOW:

    def __init__(self, ball, leftpaddle, rightpaddle, res, theme) -> None:
        pygame.init()  # initiates the pygame module
        self.resolution = res  # sets the resolution of the screen to given one
        self.width, self.height = self.resolution  # splits the resolution into width and height
        self.screen = pygame.display.set_mode(res)  # creates screen with given measures
        pygame.display.set_caption("Pong by Max and Linus")  # gives the window a name
        self.score_font = pygame.font.SysFont("Clear Sans Regular", 80)  # Font for the score
        self.menu_font = pygame.font.SysFont("Clear Sans Regular", 30)  # Font for the unfocused menu entries
        self.menu_font_focused = pygame.font.SysFont("Clear Sans Regular", 40)  # Font for the focused menu entries
        self.leftpaddel = leftpaddle  # gets the left  paddle
        self.rightpaddel = rightpaddle  # gets the right paddle
        self.ball = ball  # gets the ball
        self.offset = 100  # sets the natural offset for the input boxes
        self.resmenuerr = False  # no error happened yet (hopefully)
        self.changetheme(theme)  # sets the theme to the default one
        self.scoreresetv = False  # score can't be reset yet

    def updategamescreen(self, scoreleft, scoreright) -> None:
        pygame.mouse.set_visible(False)  # mouse won't show
        self.screen.fill(self.background_color)  # background is filled
        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10, self.leftpaddel.getheight()])  # left paddle is drawn
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10, self.rightpaddel.getheight()])  # right paddle is drawn
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])  # ball is drawn
        self.screen.blit(self.score_font.render(str(scoreleft), True, self.paddle_color), (self.width / 4, 50))  # left score is drawn
        self.screen.blit(self.score_font.render(str(scoreright), True, self.paddle_color), (self.width / 1.25, 50))  # right score is drawn
        pygame.display.flip()  # updates the screen

    def giveresolution(self) -> tuple:
        return self.resolution  # returns the resolution

    def changeresolution(self, newresolution) -> None:
        self.resolution = newresolution  # gets new resolution
        self.screen = pygame.display.set_mode(self.resolution)  # resizes the window
        self.width, self.height = self.resolution  # splits the new resolution to both width and height
        self.leftpaddel.setypos(self.height / 2)  # resets left paddle to the middle of the screen
        self.rightpaddel.setypos(self.height / 2)  # resets right paddle to the middle of the screen
        self.leftpaddel.setxpos(0.1*self.width)  # positions the left paddle in x direction
        self.rightpaddel.setxpos(0.9 * self.width)  # positions the right paddle in x direction
        self.ball.setstartpos((self.width/2, self.height/2))  # repositions the balls starting position
        self.ball.reset((270 / 0.6 * random.choice([-1, 1]), 270 / 0.6 * random.choice([-1, 1])))    # resets the ball

    def menuscreenmain(self, l) -> None:
        pygame.mouse.set_visible(True)  # mouse should show
        text_obj, widths, titles = [], [], ["RESET SCORE" if self.scoreresetv else '', "ENTER THE ARENA", "SETTINGS", "HELP", "INFO", "EXIT GAME"]  # assigns the arrays
        self.screen.fill((0, 0, 0))  # fills the screen black
        for t in range(0, len(titles)):
            text_obj.append(self.menu_font.render(titles[t], True, (254, 254, 254)) if not l[t] else self.menu_font_focused.render(titles[t], True, (254, 254, 254)))  # creates all text objects
            widths.append(text_obj[t].get_rect().width)  # calculates all the widths
            self.screen.blit(text_obj[t], ((self.width - widths[t]) / 2, self.height / 6 * t) if titles[t] != "RESET SCORE" else (0.7 * self.width + widths[t] / 2, self.height / 6))  # draws all the text objects
        pygame.display.flip()  # updates the screen

    def kickoffscreen(self, scoreleft, scoreright, i) -> None:  # can be shortened
        pygame.mouse.set_visible(False)  # mouse should not show
        self.screen.fill(self.background_color)  # fills the screen
        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10, self.leftpaddel.getheight()])  # left paddle is drawn
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10, self.rightpaddel.getheight()])  # right paddle is drawn
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])  # ball is drawn
        self.screen.blit(self.score_font.render(str(scoreleft), True, self.paddle_color), (self.width / 4, 50))  # left score is drawn
        self.screen.blit(self.score_font.render(str(scoreright), True, self.paddle_color), (self.width / 1.25, 50))  # right score is drawn
        inputtext = self.menu_font_focused.render(str(i), True, self.paddle_color)  # gets the message for the user
        width = inputtext.get_rect().width  # gets the message width
        self.screen.blit(inputtext, ((self.width - width) / 2, 50))  # draws the message
        pygame.display.flip()  # updates the screen

    def menuscreensettings(self, l) -> None:  # mess --> cleanup
        """Here we need to give a selection of all the options provided. Like Enemy-Skill, Window size, Ballspeed,
        ??Theme??"""
        pygame.mouse.set_visible(True)  # mouse should show
        self.screen.fill((0, 0, 0))  # fills the screen black
        texts, objects, widths = ["BACK", "CHANGE ENEMY-MODE", "CHANGE RESOLUTION", "CHANGE THEME", "TOGGLE BACKGROUND MUSIC"], [], []  # assigns the arrays
        for i in range(0, len(texts)):
            objects.append(self.menu_font.render(texts[i], True, (254, 254, 254)) if not l[i] else self.menu_font_focused.render(texts[i], True, (254, 254, 254)))  # creates all text objects
            widths.append(objects[i].get_rect().width)  # calculates all the widths
            self.screen.blit(objects[i], ((self.width - widths[i]) / 2, self.height / 6 * i) if texts[i] != "BACK" else (0.8 * self.width + widths[i] / 2, self.height / 6))  # draws all the text objects
        pygame.display.flip()  # updates the screen

    def menuscreenresolution(self, l, inputresolution) -> None:  # this method is a mess, needs cleanup
        pygame.mouse.set_visible(True)  # mouse should show
        self.screen.fill((0, 0, 0))  # fills the screen black
        texts, objects, widths = ["BACK", "Type in new Resolution", "Format: WIDTHxHEIGHT", "Please Type in a valid Resolution" if self.resmenuerr else None], [], []  # assigns the arrays
        for i in range(0, len(texts)):
            if texts[i] == "Please Type in a valid Resolution":
                objects.append(self.menu_font.render(texts[i], True, (255, 0, 0)))  # creates the error message's text object
            else:
                objects.append(self.menu_font.render(texts[i], True, (254, 254, 254)) if texts[i] != "BACK" or not l[i] else self.menu_font_focused.render(texts[i], True, (254, 254, 254)))  # creates all text objects
            widths.append(objects[i].get_rect().width)  # calculates all the widths
            self.screen.blit(objects[i], ((self.width - widths[i]) / 2, self.height / (12 - i * i)) if texts[i] != "BACK" else (0.8 * self.width + widths[i] / 2, self.height / 6))  # draws all the text objects
        input_box = pygame.Rect((self.width-self.offset) * 0.5, self.height / 6, 140, 32)  # creates a rectangle for the input box
        txt_surface = pygame.font.Font(None, 32).render(inputresolution, True, (254, 254, 254))  # render the current text inside the box
        input_box.w = self.offset = max(200, txt_surface.get_width() + 10)  # resize the box if the resolution is too long.
        self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  # draws the input text
        pygame.draw.rect(self.screen, (254, 254, 254), input_box, 2)  # draws the input box
        pygame.display.flip()  # updates the screen

    def menutheme(self, l) -> None:
        pygame.mouse.set_visible(True)  # mouse should show
        self.screen.fill((0, 0, 0))  # fills the screen black
        texts, widths, objects = ["BACK", "DEFAULT", "EXPERIMENTAL", "BLACK AND WHITE", 'RANDOM', 'CUSTOM'], [], []  # assigns the arrays
        for i in range(0, len(texts)):
            objects.append(self.menu_font.render(texts[i], True, (254, 254, 254)) if not l[i] else self.menu_font_focused.render(texts[i], True, (254, 254, 254)))
            widths.append(objects[i].get_rect().width)  # calculates all the widths
            self.screen.blit(objects[i], ((self.width - widths[i]) / 2, self.height / 6 * i) if texts[i] != "BACK" else (0.8 * self.width + widths[i] / 2, self.height / 6))  # draws all the text objects
        pygame.display.flip()  # updates the screen

    def menucustometheme(self, l, newcolors) -> None:
        pygame.mouse.set_visible(True)  # mouse should show
        self.screen.fill((0, 0, 0))  # fills the screen black
        texts, objects, widths = ["BACK", "PADDLE:", "BALL:", "BACKGROUND:"], [], []  # assigns the arrays for the texts
        for i in range(0, len(texts)):  # loop for the static texts
            objects.append(self.menu_font.render(texts[i], True, (254, 254, 254)) if texts[i] != "BACK" or not l[
                    i] else self.menu_font_focused.render(texts[i], True, (254, 254, 254)))  # creates all text objects
            widths.append(objects[i].get_rect().width)  # calculates all the widths
            self.screen.blit(objects[i], ((self.width - widths[i]) / 2, self.height / 6 * i) if texts[i] != "BACK" else (0.8 * self.width + widths[i] / 2, self.height / 6))  # draws all the text objects
        ins, widths, inputboxen, offsets, objects = newcolors, [], [], [100, 100, 100], []  # assigns more arrays (for the input boxes)
        for i in range(0, len(ins)):  # loop for the dynamic texts
            inputboxen.append(pygame.Rect((self.width - offsets[i]) * 0.5, self.height / 6 * (i + 1.5), 140, 32))  # creates all the input boxes
            objects.append(self.menu_font.render(ins[i], True, (254, 254, 254)))  # creates all texts inside of the boxes
            inputboxen[i].w = offsets[i] = max(200, objects[i].get_width() + 10)  # resize the input boxes to the input text
            self.screen.blit(objects[i], (inputboxen[i].x + 5, inputboxen[i].y + 5))  # draws the input texts inside the boxes
            pygame.draw.rect(self.screen, (254, 254, 254) if not (self.activebox-1) == i else (0, 206, 209), inputboxen[i], 2)  # draws the input boxes according to whether they are selected or not
        pygame.display.flip()  # updates the screen

    @multitasking.task
    def resmenuerror(self) -> None:
        self.resmenuerr = True  # will draw the error message
        sleep(5)  # waits for 5 secs
        self.resmenuerr = False  # hides the error message again

    def changetheme(self, theme) -> None:
        self.paddle_color, self.ball_color, self.background_color = theme  # splits the theme-tuple to the three colors
        config["Settings"]["theme"] = str(theme)  # sets the theme config to the theme we changed to
        with open('config.cfg', 'w') as configfile:  # opens the config file
            config.write(configfile)  # writes to the file

    def scorereset(self, boolean) -> None:
        self.scoreresetv = boolean  # sets the scorereset variable to given boolean

    def setactivebox(self, i) -> None:
        self.activebox = i  # sets, which input box in custom theme is focused

    def getactivebox(self) -> int:
        return self.activebox  # returns the number of the currently active input box in custom theme


class SOUNDS:

    @staticmethod
    def play(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does not wait for the sound to be finished"""
        pygame.mixer.init(22100, 16, allowedchanges=64)  # initiates the pygame mixer
        pygame.mixer.Sound(path).play()  # plays the soundfile from the given path

    @staticmethod
    def playandquit(path) -> None:
        """initiates the output of the soundfile with the directory-path path
        Does wait for the sound to be finished"""
        pygame.mixer.init(22100, -16, 2, 64)  # initiates the pygame mixer
        sound = pygame.mixer.Sound(path)  # gets the soundfile from path
        sound.play()  # plays the sound
        pygame.time.delay(int(sound.get_length() * 1000))  # delays for sounds duration
        pygame.mixer.quit()  # closes the mixer
        del sound  # removes the variable

    @staticmethod
    def backgroundmusicqueue(bool) -> None:
        pygame.init()  # initiates the pygame mixer
        pygame.mixer.init(22100, 16, 2, 64)  # initiates the pygame mixer
        pygame.mixer.music.load('soundfiles/background.mp3')  # loads soundfile from path
        pygame.mixer.music.set_volume(0.2)  # sets the volume
        if bool:
            pygame.mixer.music.play(-1)  # plays endless loop
        else:
            return


class BOUNCECONTROL:
    def __init__(self, b, lpaddle, rpaddle):
        self.blockedl = False
        self.blockedr = False
        self.ball = b
        self.leftpaddle = lpaddle
        self.rightpaddle = rpaddle

    def bounce(self, resolution):
        if self.leftpaddle.getxpos() + 10 < self.ball.getxpos() < self.leftpaddle.getxpos() + 16 and not self.blockedl:  # in case the self.ball is in left paddles x-range
            if self.leftpaddle.getypos() - 10 < self.ball.getypos() < self.leftpaddle.getypos() + self.leftpaddle.getheight() + 10:  # in case the self.ball is in left paddles y-range
                self.left()
                self.blockl()
                self.ball.add_mfy(45 * self.ball.mfy / abs(
                    self.ball.mfy))  # speeds up the  self.ball in y direction, always increases speed
                self.ball.add_mfx(30 * self.ball.mfx / abs(self.ball.mfx))
        if self.rightpaddle.getxpos() - 16 < self.ball.getxpos() < self.rightpaddle.getxpos() - 10 and not self.blockedr:  # in case the self.ball is in right paddles x-range
            if self.rightpaddle.getypos() - 10 < self.ball.getypos() < self.rightpaddle.getypos() + self.rightpaddle.getheight() + 10:  # in case the self.ball is in right paddles y-range
                self.right()
                self.blockr()
                self.ball.add_mfy(45 * self.ball.mfy / abs(
                    self.ball.mfy))  # speeds up the  self.ball in y direction, always increases speed
                self.ball.add_mfx(30 * self.ball.mfx / abs(self.ball.mfx))
        if not 21 < self.ball.getypos() < resolution[1] - 21:  # in case the self.ball touches the bottom or the top
            self.bottomtop()

    @multitasking.task
    def blockl(self):
        self.blockedl = True
        sleep(0.5)
        self.blockedl = False

    @multitasking.task
    def blockr(self):
        self.blockedr = True
        sleep(0.5)
        self.blockedr = False

    def bottomtop(self):
        self.ball.changeydirection()
        SOUNDS.play('soundfiles/Jump1.wav')

    def right(self):
        xsp = (self.ball.getypos() - (self.rightpaddle.getypos() + self.rightpaddle.getheight() / 2)) / 5
        m = (self.ball.give_mfx()) / (self.ball.give_mfy())
        if xsp == 0:
            mn = -m
        else:
            mn = self.berechnung(m, xsp)
            if (mn > 0 and m > 0) or (mn < 0 and m < 0):
                mn = -mn
        factor = self.ball.give_mfx()/mn
        mfxnew = int(mn * factor)
        mfynew = int(-factor)
        if (self.ball.give_mfx() < 0 and mfxnew < 0) or (self.ball.give_mfx() > 0 and mfxnew > 0):
            mfxnew = -mfxnew
            mfynew = -mfynew if self.ball.getypos() + 10 > self.rightpaddle.getypos() + self.rightpaddle.getheight()/2 else mfynew
        mfnew = mfxnew, mfynew
        self.ball.set_mf(mfnew)
        SOUNDS.play('soundfiles/Jump1.wav')

    def left(self):
        xsp = ((self.leftpaddle.getypos() + self.leftpaddle.getheight() / 2) - self.ball.getypos()) / 5
        m = -(self.ball.give_mfx()) / -(self.ball.give_mfy())
        if xsp == 0:
            mn = -m
        else:
            mn = self.berechnung(m, xsp)
            if (mn > 0 and m > 0) or (mn < 0 and m < 0):
                mn = -mn
        factor = self.ball.give_mfx()/mn
        mfxnew = int(mn * -factor)
        mfynew = int(-factor)
        if (self.ball.give_mfx() < 0 and mfxnew < 0) or (self.ball.give_mfx() > 0 and mfxnew > 0):
            mfxnew = -mfxnew
            mfynew = -mfynew if self.ball.getypos() + 10 > self.leftpaddle.getypos() + self.leftpaddle.getheight() / 2 else mfynew
        mfnew = mfxnew, mfynew
        self.ball.set_mf(mfnew)
        SOUNDS.play('soundfiles/Jump1.wav')

    def berechnung(self, m, xsp) -> float:
        return math.tan(2 * math.atan(-1 / (2 * 0.0005 * xsp)) - math.atan(m))


if __name__ == '__main__':  # If this file is directly execxuted (not just imported)
    game_management = GAMECONTROL()  # execute the GAMECONTROL class. This will handle anything else.
