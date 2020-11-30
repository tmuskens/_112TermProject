from cmu_112_graphics import *
from utilities import *
import math
import numpy

class Batter(object):
     def __init__(self, mode):
        self.leftFootX = mode.margin + 100
        self.leftFootY = mode.height - mode.lowerMargin
        self.rightFootX = mode.margin + 190
        self.rightFootY = mode.height - mode.lowerMargin

        self.leftElbowX = mode.margin + 150
        self.leftElbowY = mode.height - mode.lowerMargin - 130
        self.rightElbowX = mode.margin + 200
        self.rightElbowY = mode.height - mode.lowerMargin - 130

        self.batLength = 100
        self.shinLength = 50
        self.thighLength = 40
        self.bodyHeight = 80
        self.hipWidth = 40
        self.angle = 10

        self.rightHipY = mode.height - mode.lowerMargin - 81
        self.rightHipX = mode.margin + 195
        self.leftHipX = self.rightHipX - self.hipWidth
        self.leftHipY = self.rightHipY + self.angle
        self.rightShoulderX = self.rightHipX
        self.rightShoulderY = self.rightHipY - self.bodyHeight
        self.leftShoulderX = self.leftHipX
        self.leftShoulderY = self.leftHipY - self.bodyHeight
        print(self.leftHipX, self.leftHipY)
        print(self.leftFootX, self.leftFootY)
        print(distance(self.leftFootX, self.leftFootY, self.leftHipX, self.leftHipY))
        self.leftKneeX, self.leftKneeY = setKneePosition(mode, self.leftHipX, 
                    self.leftHipY, self.leftFootX, self.leftFootY, 
                    self.shinLength, self.thighLength)
        self.rightKneeX, self.rightKneeY = setKneePosition(mode, self.rightHipX, 
                        self.rightHipY, self.rightFootX, self.rightFootY, 
                        self.shinLength, self.thighLength)

        self.handleTopX = mode.margin + 225
        self.handleTopY = mode.height - mode.lowerMargin - 125
        self.toeX = mode.margin + 225
        self.toeY = mode.height - mode.lowerMargin - 25

def getDimensions(mode):
    leftEdge = mode.margin
    rightEdge = mode.width - mode.margin
    topEdge = mode.margin
    bottomEdge = mode.height - mode.lowerMargin
    gameWidth = rightEdge - leftEdge
    gameHeight = bottomEdge - topEdge
    return leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight

def setKneePosition(mode, hipX, hipY, footX, footY, shinLength, thighLength):
    #print(hipX, hipY)
    #print(footX, footY)
    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    a = shinLength
    b = thighLength
    c = distance(hipX, hipY, footX, footY)
    #print(c)
    angleC = cosineRuleAngle(a, b, c)
    angleB = sineRuleAngle(c, angleC, b) 
    if (hipX > footX):
        theta = math.atan((bottomEdge - hipY)/(hipX - (footX - leftEdge))) - angleB
    else: 
        theta = math.pi + math.atan((bottomEdge - hipY)/(hipX - (footX - leftEdge))) - angleB
    x = abs(a * math.cos(theta))
    y = abs(a * math.sin(theta))
    kneeX = footX + x
    kneeY = bottomEdge - y
    return (kneeX, kneeY)

def updateBatter(mode):
    batter = mode.batter
    cursor = mode.cursor
    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    x = 0
    y = 0
    if cursor.x > leftEdge + (gameWidth / 2):
        # batter.rightHipX = batter.rightFootX + 23
        # batter.rightHipY = bottomEdge - 60
        x = 49
    elif cursor.x < leftEdge:
        x = -89
    else: 
        # batter.rightHipX = batter.rightFootX - 17
        # batter.rightHipY = bottomEdge - 88
        x = (-leftEdge + cursor.x)/(gameWidth/2)*138 - 89
    batter.rightHipX = batter.rightFootX + x
    if cursor.y < bottomEdge - gameHeight/2:
        if x > -20:
            y = (8100 - (-x -40)**2)**0.5
        else:
            y = (8100 - x**2)**0.5
    elif bottomEdge - gameHeight/2 < cursor.y < bottomEdge:
        if x > - 20:
            ymax = ((8100 - (-x -40)**2)**0.5)
        else:
            ymax = ((8100 - x**2)**0.5)
        y = (((bottomEdge - cursor.y)/(gameHeight/2)) * ymax + 10)
        #print(ymax)
    elif cursor.y > bottomEdge:
        y = 10
    x, y = int(x), int(y)
    print(x, y)
    batter.rightHipY = bottomEdge - y


    batter.leftHipX = batter.rightHipX - batter.hipWidth
    batter.leftHipY = batter.rightHipY + batter.angle
    batter.rightShoulderX = batter.rightHipX
    batter.rightShoulderY = batter.rightHipY - batter.bodyHeight
    batter.leftShoulderX = batter.leftHipX
    batter.leftShoulderY = batter.leftHipY - batter.bodyHeight

    #knee position calculation
    batter.leftKneeX, batter.leftKneeY = setKneePosition(mode, batter.leftHipX, 
                    batter.leftHipY, batter.leftFootX, batter.leftFootY, 
                    batter.shinLength, batter.thighLength)
    batter.rightKneeX, batter.rightKneeY = setKneePosition(mode, batter.rightHipX, 
                    batter.rightHipY, batter.rightFootX, batter.rightFootY, 
                    batter.shinLength, batter.thighLength)



def drawBatter(mode, canvas):
    b = mode.batter
    canvas.create_line(b.leftFootX, b.leftFootY, b.leftKneeX, b.leftKneeY, fill='red') # left shin
    canvas.create_line(b.leftKneeX, b.leftKneeY, b.leftHipX, b.leftHipY, fill = 'green') # left thigh
    canvas.create_line(b.rightFootX, b.rightFootY, b.rightKneeX, b.rightKneeY, fill='red') # right shin
    canvas.create_line(b.rightKneeX, b.rightKneeY, b.rightHipX, b.rightHipY, fill = 'green') # right thigh
    
    
    canvas.create_line(b.leftHipX, b.leftHipY, b.leftShoulderX, b.leftShoulderY) #left side
    canvas.create_line(b.rightHipX, b.rightHipY, b.rightShoulderX, b.rightShoulderY) #right side
    canvas.create_line(b.leftHipX, b.leftHipY, b.rightHipX, b.rightHipY) # waist

    #canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.leftElbowX, b.leftElbowY) # left upper arm
    #canvas.create_line(b.rightShoulderX, b.rightShoulderY, b.rightElbowX, b.rightElbowY) # right upper arm
    canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.rightShoulderX, b.rightShoulderY) # shoulder line

    canvas.create_oval(b.leftShoulderX, b.leftShoulderY - 30, b.rightShoulderX, b.rightShoulderY)

    #canvas.create_line(b.leftElbowX, b.leftElbowY, b.handleTopX, b.handleTopY) # left forearm
    #canvas.create_line(b.rightElbowX, b.rightElbowY, b.handleTopX, b.handleTopY) # right forearm

    #canvas.create_line(b.handleTopX, b.handleTopY, b.toeX, b.toeY, width=3, fill='orange')

    