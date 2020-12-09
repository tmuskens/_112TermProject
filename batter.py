#Controls for batter body and bat movement and drawing

from cmu_112_graphics import *
from utilities import *
import math
import numpy
from fileMethods import *

#batter class
class Batter(object):
    batMass = 10
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

        self.prevPositions = []

# run when the batter gets out
def batterOut(mode):
    mode.score = int(mode.runs*mode.strikeRate)
    if mode.score > mode.app.learboardLowest or (len(mode.app.leaderboard) < 10 
                                                and mode.score > 0):
        name = mode.app.leaderboard.get(mode.score, None)
        if name == None:
            mode.app.leaderboard[mode.score] = mode.app.user
        else:
            l = name.split(',')
            if mode.app.user not in l:
                mode.app.leaderboard[mode.score] = f'{name}, {mode.app.user}'
        if len(mode.app.leaderboard) > 10:
            del mode.app.leaderboard[min(mode.app.leaderboard)]
        writeFileFromLeaderboard('leaderboard.txt', mode.app.leaderboard)
        mode.app.learboardLowest = min(mode.app.leaderboard)
    if mode.score > mode.app.highScore:
        mode.app.highScore = mode.score
        writeHighScore(mode.app.user, mode.score, "highScores.txt")
    mode.gameOver = True
    
#gets dimensions of playing area
def getDimensions(mode):
    leftEdge = mode.margin
    rightEdge = mode.width - mode.margin
    topEdge = mode.margin
    bottomEdge = mode.height - mode.lowerMargin
    gameWidth = rightEdge - leftEdge
    gameHeight = bottomEdge - topEdge
    return leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight

# sets knee position given the foot and hip positions
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

#sets elbow positions given the hands and shoulder positions
def setElbowPosition(shoulderX, shoulderY, handleTopX, handleTopY, upperArmLength, forearmLength, side):
    a = upperArmLength
    b = forearmLength
    c = distance(shoulderX, shoulderY, handleTopX, handleTopY)
    angleC = cosineRuleAngle(a, b, c)
    angleB = sineRuleAngle(c, angleC, b) 
    if (shoulderY - handleTopY) == 0:
        if (shoulderY - handleTopY) < 0:
            phi = -math.pi/2
        else:
            phi = math.pi/2
    else:
        phi = math.atan((shoulderX - handleTopX)/(shoulderY - handleTopY))
    
    if side == 'right':
        theta = phi + angleB
    else:
        theta = phi - angleB
    x = upperArmLength * math.sin(theta)
    y = upperArmLength * math.cos(theta)
    elbowX = shoulderX + x
    elbowY = shoulderY + y
    return elbowX, elbowY

# sets bat position based on cursor
def setBatPosition(batter, cursor):
    if cursor.x > batter.rightShoulderX:
        #cursor is to the right of the right shoulder
        if distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY) > 80:
            #not within 80 of left shoulder
            try:
                theta = math.atan((cursor.y - batter.leftShoulderY)/(cursor.x - batter.leftShoulderX))
            except:
                theta = math.atan((cursor.y - batter.leftShoulderY))
            x = 80 * math.cos(theta)
            y = 80 * math.sin(theta) if cursor.y > batter.leftShoulderY else 0
            batter.leftElbowX = batter.leftShoulderX + x/2
            batter.leftElbowY = batter.leftShoulderY + y/2
            batter.handleTopX = batter.leftShoulderX + x
            batter.handleTopY = batter.leftShoulderY + y
            batter.rightElbowX, batter.rightElbowY = setElbowPosition(batter.rightShoulderX, 
                                                    batter.rightShoulderY, batter.handleTopX, 
                                                    batter.handleTopY, batter.upperArmLength, 
                                                    batter.foreArmLength, 'right')
        else:
            d = distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY)
            try:
                theta = math.atan((cursor.y - batter.leftShoulderY)/(cursor.x - batter.leftShoulderX))
            except:
                theta = math.atan((cursor.y - batter.leftShoulderY))
            x = d * math.cos(theta)
            y = d * math.sin(theta) if cursor.y > batter.leftShoulderY else 0
            batter.handleTopX = batter.leftShoulderX + x
            batter.handleTopY = batter.leftShoulderY + y
            batter.rightElbowX, batter.rightElbowY = setElbowPosition(batter.rightShoulderX, 
                                                    batter.rightShoulderY, batter.handleTopX, 
                                                    batter.handleTopY, batter.upperArmLength, 
                                                    batter.foreArmLength, 'right')
            batter.leftElbowX, batter.leftElbowY = setElbowPosition(batter.leftShoulderX, 
                                                batter.leftShoulderY, batter.handleTopX, 
                                                batter.handleTopY, batter.upperArmLength, 
                                                batter.foreArmLength, 'left')
    
    elif batter.leftShoulderX <= cursor.x <= batter.rightShoulderX:   #Cursor is between the two shoulders
        if distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY) < 80 and \
            distance(cursor.x, cursor.y, batter.rightShoulderX, batter.rightShoulderY): # cursor is within the arc of both shoulders
            d = distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY)
            try:
                theta = math.atan((cursor.y - batter.leftShoulderY)/(cursor.x - batter.leftShoulderX))
            except:
                theta = math.atan((cursor.y - batter.leftShoulderY))
            x = d * math.cos(theta)
            y = d * math.sin(theta) if cursor.y > batter.leftShoulderY else 0
            batter.handleTopX = batter.leftShoulderX + x
            batter.handleTopY = batter.leftShoulderY + y
            batter.rightElbowX, batter.rightElbowY = setElbowPosition(batter.rightShoulderX, 
                                                    batter.rightShoulderY, batter.handleTopX, 
                                                    batter.handleTopY, batter.upperArmLength, 
                                                    batter.foreArmLength, 'right')
            batter.leftElbowX, batter.leftElbowY = setElbowPosition(batter.leftShoulderX, 
                                                batter.leftShoulderY, batter.handleTopX, 
                                                batter.handleTopY, batter.upperArmLength, 
                                                batter.foreArmLength, 'left')
    else: #cursor is to the left of the left shoulder
        if distance(cursor.x, cursor.y, batter.rightShoulderX, batter.rightShoulderY) > 80:
            # not within 80 of right shoulder
            try:
                theta = math.atan((cursor.y - batter.rightShoulderY)/(cursor.x - batter.rightShoulderX))
            except:
                theta = math.atan((cursor.y - batter.rightShoulderY))
            x = -80 * math.cos(theta)
            y = -80 * math.sin(theta) if cursor.y > batter.leftShoulderY else 0
            batter.rightElbowX = batter.rightShoulderX + x/2
            batter.rightElbowY = batter.rightShoulderY + y/2
            batter.handleTopX = batter.rightShoulderX + x
            batter.handleTopY = batter.rightShoulderY + y
            batter.leftElbowX, batter.leftElbowY = setElbowPosition(batter.leftShoulderX, 
                                                batter.leftShoulderY, batter.handleTopX, 
                                                batter.handleTopY, batter.upperArmLength, 
                                                batter.foreArmLength, 'left')
        else:
            d = distance(cursor.x, cursor.y, batter.leftShoulderX, batter.leftShoulderY)
            try:
                theta = math.atan((cursor.y - batter.leftShoulderY)/(cursor.x - batter.leftShoulderX))
            except:
                theta = math.atan((cursor.y - batter.leftShoulderY))
            x = -d * math.cos(theta)
            y = -d * math.sin(theta) if cursor.y > batter.leftShoulderY else 0
            batter.handleTopX = batter.leftShoulderX + x
            batter.handleTopY = batter.leftShoulderY + y
            batter.rightElbowX, batter.rightElbowY = setElbowPosition(batter.rightShoulderX, 
                                                    batter.rightShoulderY, batter.handleTopX, 
                                                    batter.handleTopY, batter.upperArmLength, 
                                                    batter.foreArmLength, 'right')
            batter.leftElbowX, batter.leftElbowY = setElbowPosition(batter.leftShoulderX, 
                                                batter.leftShoulderY, batter.handleTopX, 
                                                batter.handleTopY, batter.upperArmLength, 
                                                batter.foreArmLength, 'left')
            
    
    setBatToePosition(batter, cursor)

#sets the angle and position of the bat
def setBatToePosition(batter, cursor):
    #print(cursor.y, batter.rightShoulderY)
    if cursor.y < batter.leftShoulderY:
        cursorY = batter.leftShoulderY
    else:    
        cursorY = cursor.y
    centreX = (batter.leftShoulderX + batter.rightShoulderX)/2
    centreY = (batter.rightShoulderX + batter.rightShoulderY)/2
    batAngle = math.atan((cursor.x - centreX)/(cursorY - centreY))
    batTopDistance = distance(centreX, centreY, batter.handleTopX, batter.handleTopY)
    #print(batTopDistance)
    gamma = math.atan((batter.handleTopX - centreX)/(batter.handleTopY - centreY))
    beta = gamma - batAngle
    
    if beta == 0:
        X = (batter.batLength + batTopDistance) * math.sin(batAngle)
        Y = (batter.batLength + batTopDistance) * math.cos(batAngle)
    else:
        sinZeta = (batTopDistance * math.sin(beta))/batter.batLength
        if sinZeta < -1:
            zeta = -math.pi/2
        elif sinZeta > 1:
            zeta = math.pi/2
        else:
            zeta = math.asin(sinZeta)
        alpha = math.pi - (beta + zeta) #angle sum of triangle
        batBottomDistance = ((batter.batLength * math.sin(alpha))/math.sin(beta))
        X = batBottomDistance * math.sin(batAngle)
        Y = batBottomDistance * math.cos(batAngle)
    
    batter.toeX = centreX + X
    batter.toeY = centreY + Y

#updaetd batters  position every timer fired
def updateBatter(mode):
    batter = mode.batter
    batter.prevPositions.append((batter.handleTopX, batter.handleTopY, batter.toeX, batter.toeY))
    if len(batter.prevPositions) > 10:
        batter.prevPositions.pop(0)
    cursor = mode.cursor
    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    x = 0
    y = 0
    if cursor.x > leftEdge + (gameWidth / 2): #right half of screen => max x
        x = 39
    elif cursor.x < leftEdge: # over left margin => min x
        x = -87
    else: # within "field of play"
        x = (-leftEdge + cursor.x)/(gameWidth/2)*126 - 87
    if x < -39:
        x = -39 #set -39 as min x
    batter.rightHipX = batter.rightFootX + x
    if cursor.y < bottomEdge - gameHeight/4: # above bottom quarter => min y
        if x > -8:
            y = (8100 - (-50 - x)**2)**0.5 + 10
        else:
            y = (8100 - x**2)**0.5
    elif bottomEdge - gameHeight/4 <= cursor.y <= bottomEdge: # within field of play
        if x > - 8:
            ymax = ((8100 - (-50 - x)**2)**0.5) + 10
        else:
            ymax = ((8100 - x**2)**0.5)
        y = (((bottomEdge - cursor.y)/(gameHeight/4)) * (ymax- 20) + 20)
    elif cursor.y > bottomEdge: # below bottom edge => max y
        y = 20
    x, y = int(x), int(y)
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

#sets batter body based on right hip
def setBatterBody(batter):
    batter.leftHipX = batter.rightHipX - batter.hipWidth
    batter.leftHipY = batter.rightHipY + batter.angle
    batter.rightShoulderX = batter.rightHipX
    batter.rightShoulderY = batter.rightHipY - batter.bodyHeight
    batter.leftShoulderX = batter.leftHipX
    batter.leftShoulderY = batter.leftHipY - batter.bodyHeight


# returns y for each x
def batEquationFunction(batter, x):
    try:
        gradient = (batter.toeY - batter.handleTopY)/(batter.toeX - batter.handleTopX)
    except:
        gradient = (batter.toeY - batter.handleTopY)
    yInt = batter.toeY - gradient*batter.toeX
    return (gradient * x) + yInt

# returns x for each y
def inverseBatEquationFunction(batter, y):
    try:
        gradient = (batter.toeY - batter.handleTopY)/(batter.toeX - batter.handleTopX)
    except:
        gradient = (batter.toeY - batter.handleTopY)
    yInt = batter.toeY - gradient*batter.toeX
    return (y - yInt)/gradient

# returns equation where Ax + By + C = 0
def batEquation(batter):
    try:
        gradient = (batter.toeY - batter.handleTopY)/(batter.toeX - batter.handleTopX)
    except:
        gradient = (batter.toeY - batter.handleTopY)
    yInt = batter.toeY - gradient*batter.toeX
    A = gradient
    B = -1
    C = yInt
    return A, B, C 

#draws batter
def drawBatter(mode, canvas):
    b = mode.batter
    if mode.app.graphics:
        #body
        canvas.create_image(b.leftHipX - 10, b.leftHipY + 10, anchor = 'sw',
                        image=ImageTk.PhotoImage(mode.bodyImage))
        #right upperArm
        drawMovingImage(canvas, b.rightShoulderX, b.rightShoulderY, b.rightElbowX, b.rightElbowY,  mode.upperArmImage, 25, -5, False)
        #head
        canvas.create_image(b.leftHipX - 10, b.leftHipY + 10, anchor = 'sw',
                        image=ImageTk.PhotoImage(mode.headImage))

        canvas.create_image(b.leftFootX, b.leftFootY, anchor = 'sw',
                        image=ImageTk.PhotoImage(mode.shoeImage))

        canvas.create_image(b.rightFootX, b.rightFootY, anchor = 'sw',
                        image=ImageTk.PhotoImage(mode.shoeImage))
        #left upperArm
        drawMovingImage(canvas, b.leftShoulderX, b.leftShoulderY, b.leftElbowX, b.leftElbowY,  mode.upperArmImage, 25, -5, True)
        #left thigh
        drawMovingImage(canvas, b.leftHipX, b.leftHipY, b.leftKneeX, b.leftKneeY,  mode.thighImage, 30, -10, False)
        #right thigh
        drawMovingImage(canvas, b.rightHipX, b.rightHipY, b.rightKneeX, b.rightKneeY,  mode.thighImage, 30, -10, False)
        #leftPad
        drawMovingImage(canvas, b.leftKneeX, b.leftKneeY, b.leftFootX, b.leftFootY, mode.padImage, 37, -25, False)
        #rightPad
        drawMovingImage(canvas, b.rightKneeX, b.rightKneeY, b.rightFootX, b.rightFootY, mode.padImage, 37, -25, False)
        #bat
        drawMovingImage(canvas, b.handleTopX, b.handleTopY, b.toeX, b.toeY, mode.batImage, 50, -20, False)
        #left forearm
        drawMovingImage(canvas, b.leftElbowX, b.leftElbowY, b.handleTopX, b.handleTopY + 5, mode.forearmImage, 25, -5, True)
        #right forearm
        drawMovingImage(canvas, b.rightElbowX, b.rightElbowY, b.handleTopX, b.handleTopY - 5, mode.forearmImage, 25, -5, True)
    else:
        canvas.create_polygon(b.leftShoulderX - 5, b.leftShoulderY - 5, b.rightShoulderX + 5, 
                            b.rightShoulderY - 5, b.rightHipX + 5, b.rightHipY+ 5, 
                            b.leftHipX - 5, b.leftHipY+ 5, fill='white')
        canvas.create_oval(b.leftShoulderX, b.leftShoulderY - 50, b.rightShoulderX, 
                        b.rightShoulderY, fill = 'peach puff')
    
        canvas.create_line(b.leftFootX, b.leftFootY, b.leftKneeX, b.leftKneeY, 
                        b.leftHipX, b.leftHipY, fill='grey', width = 15) # left shin
        canvas.create_line(b.rightFootX, b.rightFootY, b.rightKneeX, b.rightKneeY, 
                            b.rightHipX, b.rightHipY, fill='grey', width = 15) # right shin
        canvas.create_line(b.leftShoulderX, b.leftShoulderY, b.leftElbowX, 
                        b.leftElbowY, b.handleTopX, b.handleTopY, 
                        fill='grey', width=10)
    
        canvas.create_line(b.rightShoulderX, b.rightShoulderY, b.rightElbowX, 
                        b.rightElbowY, b.handleTopX, b.handleTopY, 
                        fill='grey', width=10)
        #canvas.create_line(b.handleTopX, b.handleTopY, b.toeX, b.toeY, width=3, fill='orange')
        #bat
        drawMovingImage(canvas, b.handleTopX, b.handleTopY, b.toeX, b.toeY, mode.batImage, 50, -20, False)
        
#draw image function to rotate body parts 
def drawMovingImage(canvas, x1, y1, x2, y2, image, length, offset, condition):
    try:
        gradient = (y2 - y1)/(x2- x1)
    except:
        gradient = (y2 - y1)
    angle = ((math.atan(gradient) - math.pi/2) * -180/math.pi)
    if gradient < 0 and y1 < y2: 
        angle += 180
    if x2 < x1 and y1 > y2 and condition:
        angle -= 180
    x = (length + offset) * math.sin(angle * math.pi/180)
    y = length - (length + offset) * math.cos(angle * math.pi/180)
    canvas.create_image(x1 + x, y1 - y, anchor = 'n',
                        image=ImageTk.PhotoImage(image.rotate(angle)))

