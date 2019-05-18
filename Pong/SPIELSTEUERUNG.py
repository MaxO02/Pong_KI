import pygame
from pygame.locals import *
from Pong.BALL import BALL
from Pong.paddel import PADDEL
from Pong.SPIELFELD import SPIELFELD
import random


class SPIELSTEUERUNG:
    def __init__(self):
        """initiates the first match, gives necessary options, starts the game on the ready-input"""
        leftpaddle = PADDEL(192, 540)
        rightpaddle = PADDEL(1728, 540)
        ball = BALL(960, 540, (960 * random.choice([-1, 1]), 540 * random.choice([-1, 1])))
        spf = SPIELFELD(ball, leftpaddle, rightpaddle)


    def match(self):
        """creates a new screen
           handles all objects floating on the screen"""
        pass

    def menu(self):
        """handles any settings, game pauses etc"""
        pass
