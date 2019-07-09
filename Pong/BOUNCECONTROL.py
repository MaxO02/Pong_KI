import multitasking
import math
import configparser
from time import sleep
from Pong.SOUNDS import SOUNDS


config = configparser.ConfigParser()
config.read("sys.cfg")


class BOUNCECONTROL:
    def __init__(self):
        self.running = True
        self.blockedl = False
        self.blockedr = False

    @multitasking.task
    def bounce(self, ball, leftpaddle, rightpaddle, resolution):

        def berechnung(m, xsp) -> float:
            return math.tan(2 * math.atan(-1 / (2 * 0.0005 * xsp)) - math.atan(m))

        def left():
            xsp = ((leftpaddle.getypos() + leftpaddle.getheight()/2) - ball.getypos()) / 10
            m = -(ball.give_mfx())/-(ball.give_mfy())
            if xsp == 0:
                mn = -m
            else:
                mn = berechnung(m, xsp)
                if (mn > 0 and m > 0) or (mn < 0 and m < 0):
                    mn = -mn
            factor = math.sqrt((ball.give_mfx()**2+leftpaddle.getheight()**2)/(mn**2+1))
            mfxnew = int(mn*-factor)
            mfynew = int(-factor)
            if (ball.give_mfx() < 0 and mfxnew < 0) or (ball.give_mfx() > 0 and mfxnew > 0):
                mfxnew = -mfxnew
                mfynew = -mfynew if ball.getypos() + 10 > leftpaddle.getypos() + leftpaddle.getheight()/2 else mfynew
            mfnew = mfxnew, mfynew
            ball.set_mf(mfnew)
            SOUNDS.play('soundfiles/Jump1.wav')
      
        def right():
            xsp = (ball.getypos() - (rightpaddle.getypos() + rightpaddle.getheight() / 2)) / 5
            m = (ball.give_mfx()) / (ball.give_mfy())
            if xsp == 0:
                mn = -m
            else:
                mn = berechnung(m, xsp)
                if (mn > 0 and m > 0) or (mn < 0 and m < 0):
                    mn = -mn
            factor = math.sqrt((ball.give_mfx() ** 2 + leftpaddle.getheight() ** 2) / (mn ** 2 + 1))
            mfxnew = int(mn * factor)
            mfynew = int(-factor)
            if (ball.give_mfx() < 0 and mfxnew < 0) or (ball.give_mfx() > 0 and mfxnew > 0):
                mfxnew = -mfxnew
                mfynew = -mfynew if ball.getypos() + 10 > rightpaddle.getypos() + rightpaddle.getheight()/2 else mfynew
            mfnew = mfxnew, mfynew
            ball.set_mf(mfnew)
            SOUNDS.play('soundfiles/Jump1.wav')

        def bottomtop():
            ball.changeydirection()
            SOUNDS.play('soundfiles/Jump1.wav')

        while self.running:
            if leftpaddle.getxpos() + 10 < ball.getxpos() < leftpaddle.getxpos() + 16 and not self.blockedl == 0:  # in case the ball is in left paddles x-range
                if leftpaddle.getypos() - 10 < ball.getypos() < leftpaddle.getypos() + leftpaddle.getheight() + 10:  # in case the ball is in left paddles y-range
                    left()
                    self.blockl()
                    ball.add_mfy(45 * ball.mfy / abs(
                        ball.mfy))  # speeds up the  ball in y direction, always increases speed
                    ball.add_mfx(30 * ball.mfx / abs(ball.mfx))
            if rightpaddle.getxpos() - 16 < ball.getxpos() < rightpaddle.getxpos() - 10 and not self.blockedr:  # in case the ball is in right paddles x-range
                if rightpaddle.getypos() - 10 < ball.getypos() < rightpaddle.getypos() + rightpaddle.getheight() + 10:  # in case the ball is in right paddles y-range
                    right()
                    self.blockr()
                    ball.add_mfy(45 * ball.mfy / abs(
                        ball.mfy))  # speeds up the  ball in y direction, always increases speed
                    ball.add_mfx(30 * ball.mfx / abs(ball.mfx))
            if not 21 < ball.getypos() < resolution[1] - 21:  # in case the ball touches the bottom or the top
                bottomtop()

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
