from cmu_112_graphics import *
from utilities import *
import math
import numpy

class Batter(object):
     def __init__(self, mode):
        self.leftFootX = mode.margin + 100
        self.leftFootY = mode.height - mode.lowerMargin
        self.rightFootX = mode.margin + 200
        self.rightFootY = mode.height - mode.lowerMargin
        
        self.leftKneeX = mode.margin + 125
        self.leftKneeY = mode.height - mode.lowerMargin - 40
        self.rightKneeX = mode.margin + 175
        self.rightKneeY = mode.height - mode.lowerMargin - 40
        
        self.leftHipX = mode.margin + 125
        self.leftHipY = mode.height - mode.lowerMargin - 80
        self.rightHipX = mode.margin + 175
        self.rightHipY = mode.height - mode.lowerMargin - 80

        self.leftShoulderX = mode.margin + 125
        self.leftShoulderY = mode.height - mode.lowerMargin - 160
        self.rightShoulderX = mode.margin + 175
        self.rightShoulderY = mode.height - mode.lowerMargin - 160

        self.leftElbowX = mode.margin + 150
        self.leftElbowY = mode.height - mode.lowerMargin - 130
        self.rightElbowX = mode.margin + 200
        self.rightElbowY = mode.height - mode.lowerMargin - 130

        self.handleTopX = mode.margin + 225
        self.handleTopY = mode.height - mode.lowerMargin - 125
        self.toeX = mode.margin + 225
        self.toeY = mode.height - mode.lowerMargin - 25

def drawBatter(mode, canvas):
    b = mode.batter
    canvas.create_line(b.leftFootX, b.leftFootY, b.leftKneeX, b.leftKneeY) # left shin
    canvas.create_line(b.leftKneeX, b.leftKneeY, b.leftHipX, b.leftHipY) # left thigh
    canvas.create_line(b.rightFootX, b.rightFootY, b.rightKneeX, b.rightKneeY) # right shin
    canvas.create_line(b.rightKneeX, b.rightKneeY, b.rightHipX, b.rightHipY) # right thigh
    
    
    canvas.create_line(b.leftHipX, b.leftHipY, b.leftShoulderX, b.leftShoulderY) #left side
    canvas.create_line(b.rightHipX, b.rightHipY, b.rightShoulderX, b.rightShoulderY) #right side
    canvas.create_line(b.leftHipX, b.leftHipY, b.rightHipX, b.rightHipY) # waist

    canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.leftElbowX, b.leftElbowY) # left upper arm
    canvas.create_line(b.rightShoulderX, b.rightShoulderY, b.rightElbowX, b.rightElbowY) # right upper arm
    canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.rightShoulderX, b.rightShoulderY) # shoulder line

    canvas.create_oval(b.leftShoulderX, b.leftShoulderY - 30, b.rightShoulderX, b.rightShoulderY)

    canvas.create_line(b.leftElbowX, b.leftElbowY, b.handleTopX, b.handleTopY) # left forearm
    canvas.create_line(b.rightElbowX, b.rightElbowY, b.handleTopX, b.handleTopY) # right forearm

    canvas.create_line(b.handleTopX, b.handleTopY, b.toeX, b.toeY, width=3, fill='orange')

    