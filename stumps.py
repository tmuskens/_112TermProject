#Stumps class - drawing and check collisions

from cmu_112_graphics import *
from utilities import *
import math
import numpy
from batter import *

#stumps class
class Stumps(object):
    def __init__(self, mode):
        self.topX = mode.margin + 50
        self.topY = mode.height - mode.lowerMargin - 100
        self.bottomX = mode.margin + 50
        self.bottomY = mode.height - mode.lowerMargin

#draws stumps
def drawStumps(mode, canvas):
    canvas.create_line(mode.stumps.topX, mode.stumps.topY, mode.stumps.bottomX, 
                        mode.stumps.bottomY, width=5, fill='orange')

#checks if ball hits stumps
def checkBallHitStumps(mode):
    stumps = mode.stumps
    for ball in mode.balls:
        if ball.cx - ball.radius < stumps.topX < ball.cx + ball.radius and \
                stumps.topY < ball.cy + ball.radius < stumps.bottomY:
            batterOut(mode)