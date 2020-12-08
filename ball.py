from cmu_112_graphics import *
from utilities import *
from batter import *
import math
import numpy

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

def drawBalls(mode, canvas):
    for ball in mode.balls:
        canvas.create_image(ball.cx, ball.cy, image=ImageTk.PhotoImage(mode.ballImage))

def bowlBall(mode):
    newBall = Ball(mode.width - 2 * mode.margin, mode.height//2, -1500, 10)
    mode.balls.append(newBall)
    mode.ballsBowled += 1

def ballCollision(b1, b2):
    Ball.ballInContact.add((b1,b2))
    ############################################################################
    # Physics formula from https://www.vobarian.com/collisions/2dcollisions2.pdf
    ############################################################################
    
    normal  = (b2.cx - b1.cx, b2.cy - b1.cy) # normal vector
    unitNormal = normal / numpy.sqrt((b2.cx - b1.cx)**2 + (b2.cy - b1.cy)**2) #unit normal vector
    unitTangent = numpy.array((-unitNormal[1],unitNormal[0])) #unit tangent vector
    u1n = numpy.vdot(unitNormal, (b1.dx, b1.dy)) #initial velocity in normal direction for first ball
    v1t = numpy.vdot(unitTangent, (b1.dx, b1.dy)) #initial velocity in tangent direction (remains unchanged)
    u2n = numpy.vdot(unitNormal, (b2.dx, b2.dy)) #second ball
    v2t = numpy.vdot(unitTangent, (b2.dx, b2.dy))
    v1n = u2n
    v2n = u1n
    v1n *= unitNormal
    v2n *= unitNormal
    v1t *= unitTangent
    v2t *= unitTangent
    v1 = v1n + v1t #ball 1 final velocity
    v2 = v2n + v2t #ball 2 final velocity

    b1.dx = int(numpy.vdot(v1, (1,0))) #splitting final velocities into x and y components again
    b1.dy = int(numpy.vdot(v1, (0,1)))
    b2.dx = int(numpy.vdot(v2, (1,0)))
    b2.dy = int(numpy.vdot(v2, (0,1)))

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
                if (mode.balls[j], mode.balls[i]) in Ball.ballInContact:
                    Ball.ballInContact.remove((mode.balls[j], mode.balls[i]))

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
    v = abs((1/m) * (M*V0) + v0)
    batNormal = math.atan(-(batter.toeX - batter.handleTopX)/(batter.toeY - \
                                                            batter.handleTopY))
    
    ballAngle = math.atan(ball.dy/ball.dx)
    if batNormal < 0:
        theta = batNormal - ballAngle
        newBallAngle = batNormal + theta + math.pi
    else: 
        theta = ballAngle - batNormal
        newBallAngle = batNormal - theta
    ball.dy = v * math.cos(newBallAngle)
    ball.dx = v * math.sin(newBallAngle)

def checkBallBatCollision(mode):
    batter = mode.batter
    for ball in mode.balls:
        A, B, C = batEquation(batter)
        if perpendicularDistance(A, B, C, ball.cx, ball.cy) <= Ball.radius and \
                                ball.cy - Ball.radius < batter.toeY and \
                                ball.cy + Ball.radius > batter.handleTopY:
            if ball not in Ball.ballContactBat:
                batBallCollision(batter, ball ,mode)
                Ball.ballContactBat.add(ball)
        else:
            if ball in Ball.ballContactBat:
                Ball.ballContactBat.remove(ball)

def ballOut(mode, runs, color, x, y):
    if runs != 0:
        runsLabel = RunsLabel(runs, x, y, color)
        mode.runsLabels.append(runsLabel)
        mode.runs += runs
        mode.strikeRate = round(mode.runs / mode.ballsBowled, 2)
    else:
        batterOut(mode)


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
