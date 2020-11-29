from cmu_112_graphics import *
from utilities import *
import math
import numpy

class Stumps(object):
    def __init__(self, mode):
        self.topX = mode.margin + 50
        self.topY = mode.height - mode.lowerMargin - 100
        self.bottomX = mode.margin + 50
        self.bottomY = mode.height - mode.lowerMargin

def drawStumps(mode, canvas):

    canvas.create_line(mode.stumps.topX, mode.stumps.topY, mode.stumps.bottomX, mode.stumps.bottomY, width=5, fill='yellow')