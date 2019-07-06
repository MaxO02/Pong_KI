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
    def Berechnung(m, xsp) -> float:
      a = 0.001
      mtangente = 2 * a * xsp
      ml = -1 / mtangente
      BETA = math.atan(ml)
      ALPHA = math.atan(m)
      GAMMA = ALPHA - BETA
      GAMMASTRICH = BETA - GAMMA
      mn = math.tan(GAMMASTRICH)
      return mn
    def left():
      xsp = (leftpaddle.getypos() + leftpaddle.getheight()/2)-ball.getypos()
      m = -(ball.give_mfx())/-(ball.give_mfy())
      if xsp == 0:
        mn = -m
      else:
        mn = Berechnung(m,xsp)
      factor = -math.sqrt((ball.give_mfx()^2+leftpaddle.getheight()^2)/(mn^2+1))
      mfxnew = int(mn*factor)
      mfynew = int(factor)
      ball.set_mf(mfxnew, mfynew)
      SOUNDS.play('soundfiles/Jump1.wav')
      
    def right():
      xsp = ball.getypos() - (rightpaddle.getypos() + rightpaddle.getheight() / 2)
      m = (ball.give_mfx()) / (ball.give_mfy())
      if xsp == 0:
        mn = -m
      else:
        mn = Berechnung(m, xsp)
      factor = -math.sqrt((ball.give_mfx() ^ 2 + leftpaddle.getheight() ^ 2) / (mn ^ 2 + 1))
      mfxnew = int(mn * factor)
      mfynew = int(factor)
      ball.set_mf(mfxnew, mfynew)
      SOUNDS.play('soundfiles/Jump1.wav')
    
    def bottomtop():
        ball.changeydirection()
        SOUNDS.play('soundfiles/Jump1.wav')
    while config.get("Stuff", "running") == "True":
      if leftpaddle.getxpos() + 10 < ball.getxpos() < leftpaddle.getxpos() + 16:  # in case the ball is in left paddles x-range
        if leftpaddle.getypos() - 10 < ball.getypos() < leftpaddle.getypos() + leftpaddle.getheight() + 10:  # in case the ball is in left paddles y-range
          left()
      if rightpaddle.getxpos() - 16 < ball.getxpos() < rightpaddle.getxpos() - 10:  # in case the ball is in right paddles x-range
        if rightpaddle.getypos() - 10 < ball.getypos() < rightpaddle.getypos() + rightpaddle.getheight() + 10:  # in case the ball is in right paddles y-range
          right()
      if not 21 < ball.getypos() < height - 21:  # in case the ball touches the bottom or the top
        bottomtop()


