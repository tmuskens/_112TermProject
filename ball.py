from cmu_112_graphics import *
from utilities import *
import math
import numpy


class Ball(object):
    ballInContact = set()
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

def phiHelper(b1, b2):
    if b2.cx == b1.cx:
        if b2.cy - b1.cy > 0: return math.pi/2
        elif b2.cy - b1.cy < 0: return -math.pi/2
        else: return 0
    return math.atan((b2.cy - b1.cy) / (b2.cx - b1.cx))

def theta(b):
    if b.dx == 0:
        if b.dy > 0: return math.pi/2
        elif b.dy < 0: return -math.pi/2
        else: return 0
    return math.atan(b.dy / b.dx)

def vxHelper(v1, v2, theta1, theta2, phi, mass):
    return (v2 * math.cos(theta2 - phi) * math.cos(phi)) +  \
            (v1 * math.sin(theta1 - phi) * math.cos(phi + math.pi/2))

def vyHelper(v1, v2, theta1, theta2, phi, mass):
    return (v2 * math.cos(theta2 - phi) * math.sin(phi)) +  \
            (v1 * math.sin(theta1 - phi) * math.sin(phi + math.pi/2))


def ballCollision(b1, b2):
    # if b1.collided or b2.collided: return
    # b1.collided = True
    # b2.collided = True
    
    Ball.ballInContact.add((b1,b2))

    #https://www.vobarian.com/collisions/2dcollisions2.pdf
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

    # s1, s2 = distance(b1.dx, 0, b1.dy, 0), distance(b2.dx, 0, b2.dy, 0)
    # #scalar speed of ball1 and ball2
    # phi = phiHelper(b1, b2)
    # theta1, theta2 = theta(b1), theta(b2)
    # v1x = vxHelper(s1, s2, theta1, theta2, phi, Ball.mass)
    # v2x = vxHelper(s2, s1, theta2, theta1, phi, Ball.mass)
    # v1y = vyHelper(s1, s2, theta1, theta2, phi, Ball.mass)
    # v2y = vyHelper(s2, s1, theta2, theta1, phi, Ball.mass)
    # print("b1", "vx", b1.dx, "vy", b1.dy, "cx", b1.cx, "cy", b1.cy)
    # print("b2", "vx", b2.dx, "vy", b2.dy, "cx", b2.cx, "cy", b2.cy)
    # print('theta1', theta1, 'theta2', theta2, 'phi', phi)

    # b1.dx, b1.dy = v1x, v1y
    # b2.dx, b2.dy = v2x, v2y
    # print(b1.dx, b2.dx)
    

def checkBallCollision(mode):
    for i in range(len(mode.balls)):
        for j in range(i + 1,len(mode.balls)):
            if distance(mode.balls[i].cx, mode.balls[i].cy, 
                        mode.balls[j].cx, mode.balls[j].cy) <= (2 * Ball.radius):
                if (mode.balls[i], mode.balls[j]) and (mode.balls[j], mode.balls[i]) not in Ball.ballInContact:
                    ballCollision(mode.balls[i], mode.balls[j])
            else:
                if (mode.balls[i], mode.balls[j]) in Ball.ballInContact:
                    Ball.ballInContact.remove((mode.balls[i], mode.balls[j]))
                if (mode.balls[j], mode.balls[i]) in Ball.ballInContact:
                    Ball.ballInContact.remove((mode.balls[j], mode.balls[i]))
                    

def moveBalls(mode):
    for ball in mode.balls:
        ball.time += mode.timerDelay * (1/(1000))
        ball.dy += (ball.time * mode.gravity)
        ball.cy += (ball.dy * mode.timerDelay) / (1000)
        ball.cx += (ball.dx * mode.timerDelay) / (1000)
        if ball.cy > mode.frameHeight - Ball.radius and ball.dy > 0:
            ball.cy -= (ball.dy / (1000/mode.timerDelay))
            ball.dy *= -0.8
            ball.dx *= (1 - (0.5 * (mode.timerDelay/1000)))
        if (ball.cx - Ball.radius <= mode.margin) or (ball.cx + Ball.radius >= mode.width - mode.margin):
            mode.balls.remove(ball)
