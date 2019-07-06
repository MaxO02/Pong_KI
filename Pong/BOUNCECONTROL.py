import multitasking
import math
import configparser
from Pong.SOUNDS import SOUNDS


config = configparser.ConfigParser()
config.read("sys.cfg")


class BOUNCECONTROL():
  
    def __init__(self):

        pass
  
    @staticmethod
    @multitasking.task
    def bounce(ball, leftpaddle, rightpaddle, height):
        blockedl = 0
        blockedr = 0
        def berechnung(m, xsp) -> float:
            a = 0.01
            mtangente = 2 * a * xsp
            ml = -1 / mtangente
            beta = math.atan(ml)
            alpha = math.atan(m)
            gamma = alpha - beta
            gammastrich = beta - gamma
            mn = math.tan(gammastrich)
            return mn
        
        def left():
            xsp = (leftpaddle.getypos() + leftpaddle.getheight()/2) - ball.getypos()
            m = -(ball.give_mfx())/-(ball.give_mfy())
            if xsp == 0:
                mn = -m
            else:
                mn = berechnung(m, xsp)
                if (mn<0 and m<0) or (mn>0 and m>0):
                    mn = -mn
            factor = math.sqrt((ball.give_mfx()**2+leftpaddle.getheight()**2)/(mn**2+1))
            mfxnew = int(mn*-factor)
            mfynew = int(-factor)

            print("m: " + str(m))
            print("xsp: " + str(xsp))
            print("mn: " + str(mn))
            if (ball.give_mfx() < 0 and mfxnew < 0) or (ball.give_mfx() > 0 and mfxnew > 0):
                mfxnew = -mfxnew
                mfynew = -mfynew
            mfnew = mfxnew, mfynew
            ball.set_mf(mfnew)
            SOUNDS.play('soundfiles/Jump1.wav')
      
        def right():
            xsp =  ball.getypos() - (rightpaddle.getypos() + rightpaddle.getheight() / 2)
            m = (ball.give_mfx()) / (ball.give_mfy())
            if xsp == 0:
                mn = -m
            else:
                mn = berechnung(m, xsp)
                if (mn<0 and m<0) or (mn>0 and m>0):
                    mn = -mn
            factor = math.sqrt((ball.give_mfx() ** 2 + leftpaddle.getheight() ** 2) / (mn ** 2 + 1))
            mfxnew = int(mn * -factor)
            mfynew = int(-factor)
            if (ball.give_mfx() < 0 and mfxnew < 0) or (ball.give_mfx() > 0 and mfxnew > 0):
                mfxnew = -mfxnew
                mfynew = -mfynew
            mfnew = mfxnew,mfynew
            print("m: " + str(m))
            print("xsp: " + str(xsp))
            print("mn: " + str(mn))
            ball.set_mf(mfnew)
            SOUNDS.play('soundfiles/Jump1.wav')

        def bottomtop():
            ball.changeydirection()
            SOUNDS.play('soundfiles/Jump1.wav')

        while config.get("Stuff", "running") == "True":
            if leftpaddle.getxpos() + 10 < ball.getxpos() < leftpaddle.getxpos() + 16 and blockedl == 0:  # in case the ball is in left paddles x-range
                if leftpaddle.getypos() - 10 < ball.getypos() < leftpaddle.getypos() + leftpaddle.getheight() + 10:  # in case the ball is in left paddles y-range
                    print("left")
                    left()
                    blockedl = 100000
                    ball.add_mfy(45 * ball.mfy / abs(
                        ball.mfy))  # speeds up the  ball in y direction, always increases speed
                    ball.add_mfx(30 * ball.mfx / abs(ball.mfx))
            if rightpaddle.getxpos() - 16 < ball.getxpos() < rightpaddle.getxpos() - 10 and blockedr == 0:  # in case the ball is in right paddles x-range
                if rightpaddle.getypos() - 10 < ball.getypos() < rightpaddle.getypos() + rightpaddle.getheight() + 10:  # in case the ball is in right paddles y-range
                    print("right")
                    right()
                    blockedr = 100000
                    ball.add_mfy(45 * ball.mfy / abs(
                        ball.mfy))  # speeds up the  ball in y direction, always increases speed
                    ball.add_mfx(30 * ball.mfx / abs(ball.mfx))
            if not 21 < ball.getypos() < height - 21:  # in case the ball touches the bottom or the top
                bottomtop()
            if blockedl >0:
                blockedl-=1
            if blockedr >0:
                blockedr-=1


