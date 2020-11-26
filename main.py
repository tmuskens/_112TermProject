# Trent Muskens Term Project

import math, copy, random
import time
from cmu_112_graphics import *

from utilities import *
from ball import *

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='Little Master Cricket!', font=font)
      
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class GameMode(Mode):
    def appStarted(mode):
        mode.balls = []
        mode.gravity = 5
        mode.count = 0
        mode.margin = 15
        mode.lowerMargin = 100
        mode.frameHeight = mode.height - mode.lowerMargin
        mode.timerDelay = mode.app.timerDelay
        ballSize = (Ball.radius * 2, Ball.radius * 2)
        ball = mode.loadImage("images/ball.png")
        mode.ballImage = ball.resize(ballSize,Image.ANTIALIAS)

    def mousePressed(mode, event):
        newBall = Ball(event.x, event.y)
        mode.balls.append(newBall)

    def timerFired(mode):
        GameMode.moveBalls(mode)
        mode.count += 1
        if mode.count % 100 == 0:
            GameMode.bowlBall(mode)

    @staticmethod
    def bowlBall(mode):
        newBall = Ball(mode.width, mode.height//2, -10, 10)
        mode.balls.append(newBall)

    @staticmethod
    def moveBalls(mode):
        for ball in mode.balls:
            ball.time += 1/(1000/mode.timerDelay)
            ball.dy += (ball.time * mode.gravity)
            ball.cy += (ball.dy / mode.timerDelay)

            ball.cx += ball.dx
            if ball.cy > mode.frameHeight - Ball.radius and ball.dy > 0:
                ball.cy -= (ball.dy / mode.timerDelay)
                ball.dy *= -0.8
                ball.dx *= 1
                #ball.cy -= (ball.dy / app.timerDelay)
    
    @staticmethod       
    def drawBackground(mode, canvas):
        #canvas.create_rectangle(0,0, mode.width, mode.height, width = 2)
        canvas.create_rectangle(0,0, mode.width//2, mode.margin, fill="yellow", width = 0)
        canvas.create_rectangle(mode.width//2, 0, mode.width, mode.margin, fill="green", width = 0)
        canvas.create_rectangle(0, 0, mode.margin, mode.frameHeight, fill="yellow", width = 0)
        canvas.create_rectangle(mode.width - mode.margin, 0, mode.width, mode.frameHeight/5, fill="green", width = 0)
        canvas.create_rectangle(mode.width - mode.margin, 1*mode.frameHeight/5, mode.width, 3*mode.frameHeight/5, fill="orange", width = 0)
        canvas.create_rectangle(mode.width - mode.margin, 3*mode.frameHeight/5, mode.width, 4*mode.frameHeight/5, fill="blue", width = 0)
        canvas.create_rectangle(mode.width - mode.margin, 4*mode.frameHeight/5, mode.width, mode.frameHeight, fill="purple", width = 0)
        canvas.create_rectangle(0, mode.frameHeight, mode.width, mode.height, fill='black')

    def redrawAll(mode, canvas):
        Ball.drawBalls(mode, canvas)
        GameMode.drawBackground(mode, canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 5

app = MyModalApp(width=800, height=500)










