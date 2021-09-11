# methods for balls hitting bats and other balls, and going out of bounds

from cmu_112_graphics import *
from utilities import *
from batter import *
import math
import numpy
import random

#runs label class
class RunsLabel(object):
    dRadius = 0.05
    dSize = 0.1

    def __init__(self, runs, x, y, color):
        self.time = 0
        self.runs = runs
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10
        self.size = 12

#ball class
class Ball(object):
    ballInContact = set()
    ballContactBat = set()
    radius = 10
    mass = 1
    def __init__(self, x, y, dx=0, dy=0):
        self.cx = x
        self.cy = y
        self.dx = dx
        self.time = 0
        self.dy = dy
        self.collided = False

#draws ball using image
def drawBalls(mode, canvas):
    for ball in mode.balls:
        canvas.create_image(ball.cx, ball.cy, image=ImageTk.PhotoImage(mode.ballImage))

#generates new ball
def bowlBall(mode):
    cy = random.randint(mode.height//2 -75, mode.height//2 )
    dx = random.randint(-1800, -1500)
    dy = random.randint(0, 30)
    
    newBall = Ball(mode.width - 2 * mode.margin, cy, dx, dy)
    mode.balls.append(newBall)
    mode.ballsBowled += 1

#used when ball collides
def ballCollision(b1, b2):
    Ball.ballInContact.add((b1,b2))
    ############################################################################
    # Physics formula from https://www.vobarian.com/collisions/2dcollisions2.pdf
    ############################################################################
    
    normal  = (b2.cx - b1.cx, b2.cy - b1.cy) 
    unitNormal = normal / numpy.sqrt((b2.cx - b1.cx)**2 + (b2.cy - b1.cy)**2) 
    unitTangent = numpy.array((-unitNormal[1],unitNormal[0])) 
    
    v1normalInitial = numpy.vdot(unitNormal, (b1.dx, b1.dy)) 
    v1tangentFinal = numpy.vdot(unitTangent, (b1.dx, b1.dy)) # same as initial
    
    v2normalInitial = numpy.vdot(unitNormal, (b2.dx, b2.dy)) 
    v2tangentFinal = numpy.vdot(unitTangent, (b2.dx, b2.dy)) # same as initial
    
    v1tangentFinal *= unitTangent
    v2tangentFinal *= unitTangent

    v1normalFinal = v2normalInitial # both balls have same mass
    v2normalFinal = v1normalInitial
    
    v1normalFinal *= unitNormal
    v2normalFinal *= unitNormal
    
    v1 = v1normalFinal + v1tangentFinal 
    v2 = v1normalFinal + v2tangentFinal 

    #split vectors into components
    b1.dx = int(numpy.vdot(v1, (1,0)))
    b1.dy = int(numpy.vdot(v1, (0,1)))
    b2.dx = int(numpy.vdot(v2, (1,0)))
    b2.dy = int(numpy.vdot(v2, (0,1)))

#checks for ball collisions with other balls
def checkBallCollision(mode):
    for i in range(len(mode.balls)):
        for j in range(i + 1,len(mode.balls)):
            if distance(mode.balls[i].cx, mode.balls[i].cy, 
                        mode.balls[j].cx, mode.balls[j].cy) <= (2 * Ball.radius):
                if (mode.balls[i], mode.balls[j]) and (mode.balls[j], 
                            mode.balls[i]) not in Ball.ballInContact:
                    ballCollision(mode.balls[i], mode.balls[j])
            else:
                if (mode.balls[i], mode.balls[j]) in Ball.ballInContact:
                    Ball.ballInContact.remove((mode.balls[i], mode.balls[j]))
                elif (mode.balls[j], mode.balls[i]) in Ball.ballInContact:
                    Ball.ballInContact.remove((mode.balls[j], mode.balls[i]))

#used when ball collides with bat
def batBallCollision(batter, ball, mode):
    m = ball.mass
    M = batter.batMass
    v0 = distance(ball.dx, 0, ball.dy, 0) # scalar speed of ball

    V0top = distance(batter.handleTopX, batter.handleTopY, batter.prevPositions[0][0], 
                    batter.prevPositions[0][1]) * (1000/(mode.timerDelay * \
                    10 * len(batter.prevPositions))) # scalar speed of the bat handle
    V0bottom = distance(batter.toeX, batter.toeY, batter.prevPositions[0][2],   
                        batter.prevPositions[0][3]) * (1000/(mode.timerDelay * \
                        10 * len(batter.prevPositions))) # scalar speed of bat toe
    dTop = distance(ball.cx, batter.handleTopX, ball.cy, batter.handleTopY) # distance between ball and top of bat
    dBottom = distance(ball.cx, batter.toeX, ball.cy, batter.toeY) # distance between ball and bottom of bat
    dTotal = dTop + dBottom
    
    V0 = (dTop/dTotal) * V0top + (dBottom/dTotal) * V0bottom # velocity of the bat at the point where the ball is
    v = 0.75*abs((1/m) * (M*V0) + v0)
    batNormal = math.atan(-(batter.toeX - batter.handleTopX)/(batter.toeY - \
                                                            batter.handleTopY))
    try:
        ballAngle = math.atan(ball.dy/ball.dx)
    except:
        ballAngle = math.atan(ball.dy/-0.0001)
    if batNormal < 0:
        theta = batNormal - ballAngle
        newBallAngle = batNormal + theta + math.pi
        if newBallAngle > math.pi:
            ball.dy = v * math.cos(newBallAngle)
            ball.dx = v * math.sin(newBallAngle - math.pi/2)
            #print(ball.dx, ball.dy, newBallAngle, " exit path 0 ")
            return
    else: 
        theta = ballAngle - batNormal
        newBallAngle = batNormal - theta
        if newBallAngle > math.pi:
            ball.dy = v * math.cos(newBallAngle)
            ball.dx = v * math.sin(newBallAngle - math.pi)
            #print(ball.dx, ball.dy, newBallAngle, " exit path 1 ")
            return
        elif newBallAngle < 0:
            ball.dy = v * math.cos(newBallAngle)
            ball.dx = v * math.sin(newBallAngle + math.pi)
            #print(ball.dx, ball.dy, newBallAngle, " exit path 2 ")
            return
    
    ball.dy = v * math.cos(newBallAngle)
    ball.dx = v * math.sin(newBallAngle)
    #print(ball.dx, ball.dy, newBallAngle)

# checks for bat collision with ball
def checkBallBatCollision(mode):
    batter = mode.batter
    for ball in mode.balls:
        A, B, C = batEquation(batter)
        #batX = inverseBatEquationFunction(batter, ball.cy)
        #batY = batEquationFunction(batter, ball.cx)

        if ball.cy - ball.radius < batter.toeY and \
            ball.cy + ball.radius > batter.handleTopY and \
            ball.cx - ball.radius < max(batter.toeX, batter.handleTopX) and \
            ball.cx + ball.radius > min(batter.toeX, batter.handleTopX):
            #batter.handleTopX - ball.radius < batX < batter.toeX + ball.radius and \
            #batter.handleTopY - ball.radius < batY < batter.toeY + ball.radius
            if perpendicularDistance(A, B, C, ball.cx, ball.cy) <= ball.radius:
                if ball not in Ball.ballContactBat:
                    batBallCollision(batter, ball, mode)
                    Ball.ballContactBat.add(ball)
            else:
                if ball in Ball.ballContactBat:
                    Ball.ballContactBat.remove(ball)

# used when ball goes off screen
def ballOut(mode, runs, color, x, y):
    if runs != 0:
        runsLabel = RunsLabel(runs, x, y, color)
        mode.runsLabels.append(runsLabel)
        mode.runs += runs
        mode.strikeRate = round(mode.runs / mode.ballsBowled, 2)
    else:
        batterOut(mode)

# updates velocity and position of balls every timer fired
def moveBalls(mode):
    leftEdge, rightEdge, topEdge, bottomEdge, gameWidth, gameHeight = getDimensions(mode)
    for ball in mode.balls:
        ball.time += mode.timerDelay * (1/(1000))
        ball.dy += (ball.time * mode.gravity)
        ball.cy += (ball.dy * mode.timerDelay) / (1000)
        ball.cx += (ball.dx * mode.timerDelay) / (1000)
        if ball.cy > bottomEdge - Ball.radius and ball.dy > 0: # hitting ground
            ball.cy -= (ball.dy / (1000/mode.timerDelay))
            ball.dy *= -0.8
            ball.dx *= (1 - (0.5 * (mode.timerDelay/1000)))
        if (ball.cx - Ball.radius <= leftEdge): ##left edge
            for border in mode.borders:
                if mode.frameHeight * border.leftStart <= ball.cy < \
                    mode.frameHeight * border.leftEnd:
                    ballOut(mode, border.runs, border.color, ball.cx, ball.cy)
                    mode.balls.remove(ball)
        if (ball.cx + Ball.radius >= rightEdge): ##right edge
            for border in mode.borders:
                if mode.frameHeight * border.rightStart <= ball.cy < \
                    mode.frameHeight * border.rightEnd:
                    ballOut(mode, border.runs, border.color, ball.cx, ball.cy)
                    mode.balls.remove(ball)
        if (ball.cy - Ball.radius <= topEdge): ##left edge
            for border in mode.borders:
                if mode.width * border.topStart <= ball.cx < \
                    mode.width * border.topEnd:
                    ballOut(mode, border.runs, border.color, ball.cx, ball.cy)
                    mode.balls.remove(ball)
