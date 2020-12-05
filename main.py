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

class Button(object):
    def __init__(self, x1, y1, x2, y2, color, hoverColor, onClick, text, textColor):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color 
        self.hoverColor = hoverColor
        self.text = text
        self.textColor = textColor
        self.onClick = onClick
    
    def inButton(self, x, y):
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            return True
        else:
            return False

class Cursor(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def restartGame(mode):
    mode.gameOver = False
    mode.paused = False
    mode.balls = []
    mode.count = 0
    mode.runs = 0
    mode.ballsBowled = 0
    mode.strikeRate = 0
    return mode.gameOver

class GameMode(Mode):
    def appStarted(mode):

        mode.gameOver = False
        mode.paused = False
        mode.balls = []
        mode.gravity = 90
        mode.count = 0
        mode.margin = 15
        mode.lowerMargin = 100
        mode.gameOverMargin = 50

        mode.frameHeight = mode.height - mode.lowerMargin
        mode.timerDelay = 1
        mode.runs = 0
        mode.ballsBowled = 0
        mode.strikeRate = 0

        ballSize = (Ball.radius * 2, Ball.radius * 2)
        ball = mode.loadImage("images/ball.png")
        mode.ballImage = ball.resize(ballSize,Image.ANTIALIAS)
        
        batSize = (100, 100)
        bat = mode.loadImage("images/bat.png")
        mode.batImage = bat.resize(batSize,Image.ANTIALIAS)

        helmetSize = (40, 34)
        helmet = mode.loadImage("images/helmet.png")
        mode.helmetImage = helmet.resize(helmetSize,Image.ANTIALIAS)

        mode.cursor = Cursor()
        mode.batter = Batter(mode)
        mode.stumps = Stumps(mode)
        createBorder(mode)
        mode.gameOverButtons = []
        gameOverButtons(mode)

        mode.runsLabels = []

    def keyPressed(mode, event):
        if event.key == "p":
            mode.paused = not mode.paused
        if event.key == "s":
            GameMode.doStep(mode)
        if event.key == "g":
            batterOut(mode)


    def mousePressed(mode, event):
        if not mode.gameOver:                
            newBall = Ball(event.x, event.y)
            mode.balls.append(newBall)
        else:
            for button in mode.gameOverButtons:
                if button.inButton(event.x, event.y):
                    if button.onClick == 'restartGame':
                        restartGame(mode)

    def timerFired(mode):
        if (not mode.paused) and (not mode.gameOver): 
            GameMode.doStep(mode)
            
    @staticmethod       
    def doStep(mode):
        moveBalls(mode)
        checkBallCollision(mode)
        checkBallBatCollision(mode)
        checkBallHitStumps(mode)
        updateBatter(mode)
        updateLabels(mode)
        mode.count += 1
        if mode.count % (0.5 * (1000/mode.timerDelay)) == 0:
            bowlBall(mode)

    @staticmethod       
    def drawBackground(mode, canvas):
        for border in mode.borders:
            canvas.create_rectangle(0, mode.frameHeight * border.leftStart, 
                                mode.margin, mode.frameHeight * border.leftEnd,
                                fill = border.color, width = 0)
            canvas.create_rectangle(mode.width * border.topStart, 0, 
                                    mode.width * border.topEnd, mode.margin, 
                                    fill=border.color, width = 0)
            canvas.create_rectangle(mode.width - mode.margin, 
                                mode.frameHeight * border.rightStart, mode.width, 
                                mode.frameHeight * border.rightEnd, 
                                fill = border.color, width = 0)
        canvas.create_rectangle(0, mode.frameHeight, mode.width, mode.height, fill = 'black')

    @staticmethod
    def drawRunsLabels(mode, canvas):
        for label in mode.runsLabels:
            canvas.create_oval(label.x - label.radius, label.y - label.radius, 
                                label.x + label.radius, label.y + label.radius,
                                fill = label.color)
            canvas.create_text(label.x, label.y, text = label.runs, fill = 'white', font = f'calibri {int(label.size)} bold')


    def mouseMoved(mode, event):
        mode.cursor.x = event.x
        mode.cursor.y = event.y

    def redrawAll(mode, canvas):
        print(mode.gameOver)
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'light blue')
        drawBatter(mode, canvas)
        drawStumps(mode, canvas)
        drawBalls(mode, canvas)
        GameMode.drawBackground(mode, canvas)
        GameMode.drawRunsLabels(mode, canvas)
        drawScore(mode, canvas)
        if mode.gameOver:
            drawGameOver(mode, canvas)

def updateLabels(mode):
    for label in mode.runsLabels:
        label.time += 1
        label.radius += label.dRadius
        label.size += label.dSize
        if label.time >= 0.1 * (1000/mode.timerDelay):
            mode.runsLabels.remove(label)

def drawGameOver(mode, canvas):
    canvas.create_rectangle(mode.margin + mode.gameOverMargin, 
                            mode.margin + mode.gameOverMargin, 
                            mode.width - (mode.margin + mode.gameOverMargin),
                            mode.height - (mode.lowerMargin + mode.gameOverMargin),
                            fill = 'black')
    canvas.create_text(mode.width/2, mode.margin + mode.gameOverMargin + 30, 
                        fill='red', text="GAME OVER", font = "Arial 30 bold")
    canvas.create_text(mode.width/2, mode.margin + mode.gameOverMargin + 70,
                        fill='white', text='Score = Runs x Strike Rate',
                        font = "Arial 18 bold")
    canvas.create_rectangle(mode.width/2 - 20, 
                            mode.margin + mode.gameOverMargin + 100, 
                            mode.width/2 + 20,
                            mode.margin + mode.gameOverMargin + 140,
                            fill = 'white')
    canvas.create_text(mode.width/2, mode.margin + mode.gameOverMargin + 120,
                        text=int(mode.runs*mode.strikeRate), 
                        font = "Arial 30 bold")
    for button in mode.gameOverButtons:
        canvas.create_rectangle(button.x1, button.y1, button.x2, button.y2, 
                                fill=button.color)
        canvas.create_text((button.x1 + button.x2)/2, (button.y1 + button.y2)/2, 
                                fill=button.textColor, text=button.text, 
                                font = "Arial 20 bold")                        



def gameOverButtons(mode):
    playAgain = Button(mode.width/3, mode.margin + mode.gameOverMargin + 180,
                    mode.width/2 - 20, mode.margin + mode.gameOverMargin + 240,
                    'red', 'black', 'restartGame', "Play Again", 'white')
    home = Button(mode.width/2 + 20, mode.margin + mode.gameOverMargin + 180,
                 2*mode.width/3, mode.margin + mode.gameOverMargin + 240,
                    'red', 'black', 'n/a', "Home", 'white')
    mode.gameOverButtons = [playAgain, home]

def drawScore(mode, canvas):
    font = "Arial 18 bold"
    canvas.create_text(mode.margin*2, mode.height - mode.lowerMargin + mode.margin,
                    fill='red', text="WHACK CRICKET", font = "Arial 50 bold",
                    anchor = 'nw')
    canvas.create_text(mode.width - mode.margin * 2, 
                        mode.height - mode.lowerMargin + mode.margin,
                        anchor = 'ne', text = f'Runs: {mode.runs}', 
                        fill= 'white', font = font)
    canvas.create_text(mode.width - mode.margin * 2, 
                        mode.height - mode.lowerMargin + 3* mode.margin,
                        anchor = 'ne', text = f'Strike Rate: {mode.strikeRate}',
                        fill= 'white', font = font)
    



def createBorder(mode):
    out = Border(0, 'yellow', 0, 1, 0, 1/2, 0, 0)
    run1 = Border(1, 'purple', 0, 0, 0, 0, 4/5, 1)
    run2 = Border(2, 'blue', 0, 0, 0, 0 , 3/5, 4/5)
    run4 = Border(4, 'green', 0, 0, 0, 0, 1/5, 3/5)
    run6 = Border(6, 'orange', 0, 0, 1/2, 1, 0, 1/5) 
    mode.borders = [out, run1, run2, run4, run6]

class Border(object):
    def __init__(self, runs, color, leftStart, leftEnd, topStart, topEnd, rightStart, rightEnd):
        self.runs = runs
        self.color = color
        self.topStart = topStart
        self.topEnd = topEnd
        self.rightStart = rightStart
        self.rightEnd = rightEnd
        self.leftStart = leftStart
        self.leftEnd = leftEnd

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 1

app = MyModalApp(width=830, height=515)










