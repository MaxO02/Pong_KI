import pygame
import random
from time import sleep
import multitasking
import configparser

#reading the config
config = configparser.ConfigParser()
config.read("config.cfg")

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
        texts, objects, widths = ["BACK", "CHANGE ENEMY-MODE", "CHANGE RESOLUTION", "CHANGE THEME"], [], []  # assigns the arrays
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
        #config["Settings"]["theme"]["paddelcolor"] = self.paddle_color[1]
        #config["Settings"]["theme"]["ball_color"] = self.paddle_color[1]
        #config["Settings"]["theme"]["background_color"] = self.paddle_color[1]
        #with open('config.cfg', 'w') as configfile:
         #   config.write(configfile)

    def scorereset(self, boolean) -> None:
        self.scoreresetv = boolean  # sets the scorereset variable to given boolean

    def setactivebox(self, i) -> None:
        self.activebox = i  # sets, which input box in custom theme is focused

    def getactivebox(self) -> int:
        return self.activebox  # returns the number of the currently active input box in custom theme
