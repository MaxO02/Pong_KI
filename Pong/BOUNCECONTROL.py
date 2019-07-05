import multithreating
from math import atan, tan
import configparser
from Pong.SOUNDS import SOUNDS


config = configparser.ConfigParser()
config.read("sys.cfg")


class BOUNCECONTROL():
  
  def __init__(self):
    pass
  
  @staticmethod
  @multithreating.task
  def bounce(ball, leftpaddle, rightpaddle):
    def left():
      
    def right():
    
    def bottomtop():
      
    while config.get("Stuff", "running") == "True":
      
      
