# Trent Muskens Term Project

import math, copy, random
import time
from cmu_112_graphics import *

from utilities import *
from ball import *
from batter import *
from stumps import *

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='Little Master Cricket!', font=font)
      
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class Cursor(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class GameMode(Mode):
    def appStarted(mode):
        mode.paused = False
        mode.balls = []
        mode.gravity = 100
        mode.count = 0
        mode.margin = 15
        mode.lowerMargin = 100
        mode.frameHeight = mode.height - mode.lowerMargin
        mode.timerDelay = 1
        ballSize = (Ball.radius * 2, Ball.radius * 2)
        ball = mode.loadImage("images/ball.png")
        mode.ballImage = ball.resize(ballSize,Image.ANTIALIAS)
        mode.cursor = Cursor()
        mode.batter = Batter(mode)
        mode.stumps = Stumps(mode)
        

    def keyPressed(mode, event):
        if event.key == "p":
            mode.paused = not mode.paused
        if event.key == "s":
            GameMode.doStep(mode)


    def mousePressed(mode, ebvent):
        newBall = Ball(event.x, event.y)
        mode.balls.append(newBall)

    def timerFired(mode):
        if not mode.paused:
            GameMode.doStep(mode)
            
    @staticmethod       
    def doStep(mode):
        moveBalls(mode)
        checkBallCollision(mode)
        checkBallBatCollision(mode)
        updateBatter(mode)
        mode.count += 1
        if mode.count % (1 * (1000/mode.timerDelay)) == 0:
            bowlBall(mode)

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
        canvas.create_rectangle(0, mode.frameHeight, mode.width, mode.height)
    
    def mouseMoved(mode, event):
        mode.cursor.x = event.x
        mode.cursor.y = event.y

    def redrawAll(mode, canvas):
        drawBatter(mode, canvas)
        drawStumps(mode, canvas)
        drawBalls(mode, canvas)
        GameMode.drawBackground(mode, canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 1

app = MyModalApp(width=830, height=515)










