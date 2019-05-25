import pygame


class WINDOW:
    paddle_color = (254, 115, 1)
    ball_color = (85, 57, 138)
    background_color = (1, 254, 240)
    font_color = paddle_color
    inputresolution = ''

    def __init__(self, ball, leftpaddle, rightpaddle, res):
        pygame.init()
        self.resolution = res
        self.width, self.height = self.resolution
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Pong by Max and Linus")
        self.score_font = pygame.font.SysFont("Clear Sans Regular", 80)
        self.menu_font = pygame.font.SysFont("Clear Sans Regular", 30)
        self.menu_font_focused = pygame.font.SysFont("Clear Sans Regular", 40)
        self.leftpaddel = leftpaddle
        self.rightpaddel = rightpaddle
        self.ball = ball

    def updategamescreen(self, scoreleft, scoreright):
        pygame.mouse.set_visible(False)
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10,
                                                          self.leftpaddel.getheight()])
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10,
                                                          self.rightpaddel.getheight()])
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])
        self.screen.blit(self.score_font.render(str(scoreleft), True, self.font_color), (self.width / 4, 50))
        self.screen.blit(self.score_font.render(str(scoreright), True, self.font_color), (self.width / 1.25, 50))
        pygame.display.flip()

    def giveresolution(self):
        return self.resolution

    def changeresolution(self, newresolution):
        self.resolution = newresolution
        self.screen = pygame.display.set_mode(self.resolution)
        self.width, self.height = self.resolution
        self.leftpaddel.setypos(self.height / 2)
        self.rightpaddel.setypos(self.height / 2)
        self.ball.setstartpos((self.width/2, self.height/2))

    def menuscreenmain(self, l):
        pygame.mouse.set_visible(True)
        text_obj, widths, titles, focus = [], [], ["ENTER THE ARENA", "SETTINGS", "HELP", "INFO", "EXIT GAME"], l
        self.screen.fill((0, 0, 0))
        for t in range(0, len(titles)):
            text_obj.append(self.menu_font.render(titles[t], True, (254, 254, 254)) if not focus[t] else
                            self.menu_font_focused.render(titles[t], True, (254, 254, 254)))
            widths.append(text_obj[t].get_rect().width)
            self.screen.blit(text_obj[t], ((self.width - widths[t]) / 2, self.height / 6 * (t + 1)))
        scorereset = self.menu_font.render("RESET SCORE", True, (254, 254, 254)) if not focus[5] else self.\
            menu_font_focused.render("RESET SCORE", True, (254, 254, 254))
        scorewidth = scorereset.get_rect().width
        self.screen.blit(scorereset, (0.7*self.width + scorewidth / 2, self.height / 6))
        pygame.display.flip()

    def kickoffscreen(self, scoreleft, scoreright, i):
        pygame.mouse.set_visible(False)
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.paddle_color, [self.leftpaddel.getxpos(), self.leftpaddel.getypos(), 10,
                                                          self.leftpaddel.getheight()])
        pygame.draw.rect(self.screen, self.paddle_color, [self.rightpaddel.getxpos(), self.rightpaddel.getypos(), 10,
                                                          self.rightpaddel.getheight()])
        pygame.draw.rect(self.screen, self.ball_color, [self.ball.getxpos(), self.ball.getypos(), 20, 20])
        self.screen.blit(self.score_font.render(str(scoreleft), True, self.font_color), (self.width / 4, 50))
        self.screen.blit(self.score_font.render(str(scoreright), True, self.font_color), (self.width / 1.25, 50))
        inputtext = self.menu_font_focused.render(str(i), True, self.font_color)
        width = inputtext.get_rect().width
        self.screen.blit(inputtext, ((self.width - width) / 2, 50))
        pygame.display.flip()

    def menuscreensettings(self, l):
        """Here we need to give a selection of all the options provided. Like Enemy-Skill, Window size, Ballspeed,
        ??Theme??"""
        pygame.mouse.set_visible(True)
        self.screen.fill((0, 0, 0))
        focus = l
        back = self.menu_font.render("BACK", True, (254, 254, 254)) if not focus[0] else self. \
            menu_font_focused.render("BACK", True, (254, 254, 254))
        backwidth = back.get_rect().width
        self.screen.blit(back, (0.8 * self.width + backwidth / 2, self.height / 6))

        changegm = self.menu_font.render("CHANGE GAMEMODE", True, (254, 254, 254)) if not focus[1] else self. \
            menu_font_focused.render("CHANGE GAMEMDOE", True, (254, 254, 254))
        gmwidth = changegm.get_rect().width
        self.screen.blit(changegm, ((self.width - gmwidth) / 2, self.height / 6 * 1))

        changeres = self.menu_font.render("CHANGE RESOLUTION", True, (254, 254, 254)) if not focus[2] else self. \
            menu_font_focused.render("CHANGE RESOLUTION", True, (254, 254, 254))
        gmwidth = changeres.get_rect().width
        self.screen.blit(changeres, ((self.width - gmwidth) / 2, self.height / 6 * 2))

        pygame.display.flip()

    def menuscreenhelp(self):
        """What to do if you need help? Go to GitHub and open a new issue with exact descriptions. We might be able to
        help you. Keep in mind, that this is just a hobby school project and non-profit."""
        pass

    def menuscreeninfo(self):
        """All about the game you need to know. Who are the maintainers, How did this project happen? How did we
        work? Why did we choose this? Are there other projects to check out? Which links to follow?"""
        pass

    def menuscreenresolution(self, l, inputresolution):
        pygame.mouse.set_visible(True)
        self.screen.fill((0, 0, 0))
        back = self.menu_font.render("BACK", True, (254, 254, 254)) if not l[5] else self. \
            menu_font_focused.render("BACK", True, (254, 254, 254))
        backwidth = back.get_rect().width
        self.screen.blit(back, (0.8 * self.width + backwidth / 2, self.height / 6))
        font = pygame.font.Font(None, 32)
        color = (254, 254, 254)
        input_box = pygame.Rect(100, 100, 140, 32)
        txt_surface = font.render(inputresolution, True, color)  # Render the current text inside the box
        input_box.w = max(200, txt_surface.get_width() + 10)  # Resize the box if the resolution is too long.
        self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(self.screen, color, input_box, 2)
        pygame.display.flip()