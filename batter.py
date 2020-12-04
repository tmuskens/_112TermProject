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
        self.upperArmLength = 40
        self.foreArmLength = 40

        self.rightHipY = mode.height - mode.lowerMargin - 81
        self.rightHipX = mode.margin + 195
        
        setBatterBody(self)

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
        setBatPosition(self, mode.cursor)

def getDimensions(mode):
    leftEdge = mode.margin
    rightEdge = mode.width - mode.margin
    topEdge = mode.margin
    bottomEdge = mode.height - mode.lowerMargin
    gameWidth = rightEdge - leftEdge
    gameHeight = bottomEdge - topEdge
    return leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight

def setKneePosition(mode, hipX, hipY, footX, footY, shinLength, thighLength):

    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    a = shinLength
    b = thighLength
    c = distance(hipX, hipY, footX, footY)
    
    angleC = cosineRuleAngle(a, b, c)
    angleB = sineRuleAngle(c, angleC, b) 

    if (hipX > footX):
        theta = math.atan((bottomEdge - hipY)/(hipX - (footX - leftEdge))) - angleB
    else: 
        theta = math.pi + math.atan((bottomEdge - hipY)/(hipX - (footX - leftEdge))) - angleB
    x = a * math.cos(theta)
    y = abs(a * math.sin(theta))
    kneeX = footX + x
    kneeY = bottomEdge - y
    return (kneeX, kneeY)

def setElbowPosition(shoulderX, shoulderY, handleTopX, handleTopY, upperArmLength, forearmLength):
    a = upperArmLength
    b = forearmLength
    c = distance(shoulderX, shoulderY, handleTopX, handleTopY)
    angleC = cosineRuleAngle(a, b, c)
    angleB = sineRuleAngle(c, angleC, b) 
    phi = math.atan((shoulderX - handleTopX)/(shoulderY - handleTopY))
    #print(shoulderY, handleTopY, shoulderX - handleTopX)
    theta = phi + angleB
    #print(angleC, angleB, phi)
    x = upperArmLength * math.sin(theta)
    y = upperArmLength * math.cos(theta)
    #print(x, y)
    elbowX = shoulderX + x
    elbowY = shoulderY + y
    return elbowX, elbowY

def setBatPosition(batter, cursor):
    if cursor.y > batter.leftShoulderY:
        if cursor.x > batter.rightShoulderX:
            if distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY) > 80:
                theta = math.atan((cursor.y - batter.leftShoulderY)/(cursor.x - batter.leftShoulderX))
                x = 80 * math.cos(theta)
                y = 80 * math.sin(theta)
                batter.leftElbowX = batter.leftShoulderX + x/2
                batter.leftElbowY = batter.leftShoulderY + y/2
                batter.handleTopX = batter.leftShoulderX + x
                batter.handleTopY = batter.leftShoulderY + y
                batter.rightElbowX, batter.rightElbowY = setElbowPosition(batter.rightShoulderX, 
                                                        batter.rightShoulderY, batter.handleTopX, 
                                                        batter.handleTopY, batter.upperArmLength, 
                                                        batter.foreArmLength)
    else: 
        pass    
    
    setBatToePosition(batter, cursor)

def setBatToePosition(batter, cursor):
    #print(cursor.y, batter.rightShoulderY)
    if batter.rightShoulderY > cursor.y:
        #cursorY = batter.rightShoulderY
        cursorY = cursor.y
    else:    
        cursorY = cursor.y
    centreX = (batter.leftShoulderX + batter.rightShoulderX)/2
    centreY = (batter.rightShoulderX + batter.rightShoulderY)/2
    batAngle = math.atan((cursor.x - centreX)/(cursorY - centreY))
    batTopDistance = distance(centreX, centreY, batter.handleTopX, batter.handleTopY)
    #print(batTopDistance)
    gamma = math.atan((batter.handleTopX - centreX)/(batter.handleTopY - centreY))
    beta = gamma - batAngle
    zeta = math.asin((batTopDistance * math.sin(beta))/batter.batLength)
    alpha = math.pi - (beta + zeta) #angle sum of triangle
    batBottomDistance = ((batter.batLength * math.sin(alpha))/math.sin(beta))
    X = batBottomDistance * math.sin(batAngle)
    Y = batBottomDistance * math.cos(batAngle)
    batter.toeX = centreX + X
    batter.toeY = centreY + Y


def updateBatter(mode):
    batter = mode.batter
    cursor = mode.cursor
    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    x = 0
    y = 0
    if cursor.x > leftEdge + (gameWidth / 2):
        # batter.rightHipX = batter.rightFootX + 23
        # batter.rightHipY = bottomEdge - 60
        x = 39
    elif cursor.x < leftEdge:
        x = -87
    else: 
        # batter.rightHipX = batter.rightFootX - 17
        # batter.rightHipY = bottomEdge - 88
        x = (-leftEdge + cursor.x)/(gameWidth/2)*126 - 87
    batter.rightHipX = batter.rightFootX + x
    if cursor.y < bottomEdge - gameHeight/4:
        if x > -8:
            y = (8100 - (-50 - x)**2)**0.5 + 10
        else:
            y = (8100 - x**2)**0.5
    elif bottomEdge - gameHeight/4 < cursor.y < bottomEdge:
        if x > - 8:
            ymax = ((8100 - (-50 - x)**2)**0.5) + 10
        else:
            ymax = ((8100 - x**2)**0.5)
        y = (((bottomEdge - cursor.y)/(gameHeight/4)) * (ymax- 20) + 20)
        # print(bottomEdge, cursor.y, gameHeight/2)
        # print(ymax)
    elif cursor.y > bottomEdge:
        y = 20
    x, y = int(x), int(y)
    # print(x,y)
    # print(-50-x, y-10)
    batter.rightHipY = bottomEdge - y

    setBatterBody(batter)

    #knee position calculation
    batter.leftKneeX, batter.leftKneeY = setKneePosition(mode, batter.leftHipX, 
                    batter.leftHipY, batter.leftFootX, batter.leftFootY, 
                    batter.shinLength, batter.thighLength)
    batter.rightKneeX, batter.rightKneeY = setKneePosition(mode, batter.rightHipX, 
                    batter.rightHipY, batter.rightFootX, batter.rightFootY, 
                    batter.shinLength, batter.thighLength)
    
    setBatPosition(batter, cursor)

def setBatterBody(batter):
    batter.leftHipX = batter.rightHipX - batter.hipWidth
    batter.leftHipY = batter.rightHipY + batter.angle
    batter.rightShoulderX = batter.rightHipX
    batter.rightShoulderY = batter.rightHipY - batter.bodyHeight
    batter.leftShoulderX = batter.leftHipX
    batter.leftShoulderY = batter.leftHipY - batter.bodyHeight


# returns y for each x
def batEquationFunction(batter, x):
    gradient = (batter.toeY - batter.handleTopY)/(batter.toeX - batter.handleTopX)
    yInt = batter.toeY - gradient*batter.toeX
    return (gradient * x) + yInt

# returns equation where Ax + By + C = 0
def batEquation(batter):
    gradient = (batter.toeY - batter.handleTopY)/(batter.toeX - batter.handleTopX)
    yInt = batter.toeY - gradient*batter.toeX
    A = gradient
    B = -1
    C = yInt
    return A, B, C 

def drawBatter(mode, canvas):
    b = mode.batter
    canvas.create_line(b.leftFootX, b.leftFootY, b.leftKneeX, b.leftKneeY, fill='red') # left shin
    canvas.create_line(b.leftKneeX, b.leftKneeY, b.leftHipX, b.leftHipY, fill = 'green') # left thigh
    canvas.create_line(b.rightFootX, b.rightFootY, b.rightKneeX, b.rightKneeY, fill='red') # right shin
    canvas.create_line(b.rightKneeX, b.rightKneeY, b.rightHipX, b.rightHipY, fill = 'green') # right thigh
    
    
    canvas.create_line(b.leftHipX, b.leftHipY, b.leftShoulderX, b.leftShoulderY) #left side
    canvas.create_line(b.rightHipX, b.rightHipY, b.rightShoulderX, b.rightShoulderY) #right side
    canvas.create_line(b.leftHipX, b.leftHipY, b.rightHipX, b.rightHipY) # waist

    canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.leftElbowX, b.leftElbowY, fill = 'green') # left upper arm
    canvas.create_line(b.rightShoulderX, b.rightShoulderY, b.rightElbowX, b.rightElbowY, fill = 'green') # right upper arm
    canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.rightShoulderX, b.rightShoulderY) # shoulder line

    canvas.create_oval(b.leftShoulderX, b.leftShoulderY - 30, b.rightShoulderX, b.rightShoulderY)

    canvas.create_line(b.leftElbowX, b.leftElbowY, b.handleTopX, b.handleTopY, fill = 'red') # left forearm
    canvas.create_line(b.rightElbowX, b.rightElbowY, b.handleTopX, b.handleTopY, fill = 'red') # right forearm

    canvas.create_line(b.handleTopX, b.handleTopY, b.toeX, b.toeY, width=3, fill='orange')

    