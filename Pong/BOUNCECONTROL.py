import multitasking
import math
import configparser
from time import sleep
from Pong.SOUNDS import SOUNDS


config = configparser.ConfigParser()
config.read("sys.cfg")


class BOUNCECONTROL:
    def __init__(self, b, lpaddle, rpaddle):
        self.running = True
        self.blockedl = False
        self.blockedr = False
        self.ball = b
        self.leftpaddle = lpaddle
        self.rightpaddle = rpaddle

    @multitasking.task
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

    def stopall(self):
        self.running = False

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
