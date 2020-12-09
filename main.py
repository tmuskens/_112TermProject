# Trent Muskens Term Project
#main file - run this file 
import math, copy, random
import time
###############################################################################
# CMU 112 Graphics from https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
# All associated functions from this module are attributed to CMU 112 Graphics
###############################################################################
from cmu_112_graphics import *

from utilities import *
from ball import *
from batter import *
from stumps import *
from fileMethods import *

#button class
class Button(object):
    def __init__(self, x1, y1, x2, y2, color, hoverColor, onClick, 
                    text, textColor):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color 
        self.hoverColor = hoverColor
        self.text = text
        self.textColor = textColor
        self.onClick = onClick
        self.hover = False
    
    #checks if x,y is in a button
    def inButton(self, x, y):
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            return True
        else:
            return False
#game border class
class Border(object):
    def __init__(self, runs, color, leftStart, leftEnd, topStart, 
                    topEnd, rightStart, rightEnd):
        self.runs = runs
        self.color = color
        self.topStart = topStart
        self.topEnd = topEnd
        self.rightStart = rightStart
        self.rightEnd = rightEnd
        self.leftStart = leftStart
        self.leftEnd = leftEnd

#cursor class
class Cursor(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.type = 'arrow'

###############################################################################
# Splash Screen Mode Class from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
###############################################################################

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.cursor = Cursor()
        mode.margin = 50 
        changeUser = Button(mode.width/2 - 275, mode.margin + 250, 
                            mode.width/2 - 125, mode.margin + 300, 
                            'red', 'black', 'changeUser', "Change User", 
                            'white')
        playButton = Button(mode.width/2 - 75, mode.margin + 250, 
                            mode.width/2 + 75, mode.margin + 300, 
                            'red', 'black', 'playGame', "Play", 'white')
        leaderboard = Button(mode.width/2 + 125, mode.margin + 250, 
                            mode.width/2 + 275, mode.margin + 300, 
                            'red', 'black', 'showLeaderboard', "Leaderboard", 
                            'white')
        graphics = "Graphics: Fancy" if mode.app.graphics else "Graphics: Fast"
        graphicsButton = Button(mode.width/2 - 75, mode.margin + 400, 
                            mode.width/2 + 75, mode.margin + 450, 
                            'red', 'black', 'toggleGraphics', graphics, 'white')
        mode.splashButtons = [playButton, changeUser, leaderboard, graphicsButton]
        

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height,
                                fill = 'black')
        canvas.create_text(mode.width/2, mode.margin + 30, 
                            fill='red', text="SWING CRICKET", 
                            font = "Arial 50 bold")
        canvas.create_text(mode.width/2, mode.margin + 150, 
                            text=f"Username: {mode.app.user}", fill='white', 
                            font = "Calibri 20 bold")
        for button in mode.splashButtons:
            if button.hover:
                color = button.hoverColor
            else: 
                color = button.color
            canvas.create_rectangle(button.x1 - 5, button.y1 -5, button.x2 + 5,
                                    button.y2 + 5, fill=button.color)
            canvas.create_rectangle(button.x1, button.y1, button.x2, button.y2, 
                                    fill=color, width = 0)
            canvas.create_text((button.x1 + button.x2)/2, (button.y1 + button.y2)/2, 
                                    fill=button.textColor, text=button.text, 
                                    font = "Arial 20 bold")
        canvas.config(cursor=mode.cursor.type)     
      
    def mouseMoved(mode, event):
        mode.cursor.x = event.x
        mode.cursor.y = event.y
        mode.cursor.type = 'arrow'
        for button in mode.splashButtons:
            if button.inButton(mode.cursor.x, mode.cursor.y):
                button.hover = True
                mode.cursor.type = "hand"
            else:
                button.hover = False
          
    def mousePressed(mode, event):
        for button in mode.splashButtons:
            if button.inButton(event.x, event.y):
                mode.appStarted()
                if button.onClick == 'playGame':
                    mode.app.setActiveMode(mode.app.gameMode)
                    restartGame(mode)
                elif button.onClick == 'changeUser':
                    inputUser(mode)
                elif button.onClick == 'showLeaderboard':
                    mode.app.setActiveMode(mode.app.leaderboardMode)
                elif button.onClick == "toggleGraphics":
                    mode.app.graphics = not mode.app.graphics
                    if mode.app.graphics:
                        mode.splashButtons[3].text = "Graphics: Fancy"
                    else: 
                        mode.splashButtons[3].text = "Graphics: Fast"
#change username function
def inputUser(mode):
    prevName = mode.app.user
    mode.app.user = mode.getUserInput('Username:') #get user input from CMU 112 graphics
    if (mode.app.user == None):
        mode.app.user = prevName
    else:
        mode.app.highScore = readHighScore('highScores.txt', mode.app.user)
        mode.app.leaderboard = readLeaderboardFile("leaderboard.txt")
        mode.app.learboardLowest = min(mode.app.leaderboard)

#restart game function
def restartGame(mode):
    mode.gameOver = False
    mode.paused = False
    mode.balls = []
    mode.count = 0
    mode.runs = 0
    mode.ballsBowled = 0
    mode.strikeRate = 0
    return mode.gameOver

#loads images
def loadImages(mode):
    # All unreferenced images were drawn by me
    ###########################################################################
    # Image Reference
    # https://www.clipartkey.com/mpngs/m/40-401897_cricket-ball-png-clip-art-cricket-ball-image.png
    ###########################################################################
    ballSize = (Ball.radius * 2, Ball.radius * 2)
    ball = mode.loadImage("images/ball.png")
    mode.ballImage = ball.resize(ballSize,Image.ANTIALIAS)

    bodySize = (60, 130)
    body = mode.loadImage("images/body2.png")
    mode.bodyImage = body.resize(bodySize,Image.ANTIALIAS)
    
    head = mode.loadImage("images/head.png")
    mode.headImage = head.resize(bodySize,Image.ANTIALIAS)

    ###########################################################################
    # Image Reference
    # https://www.123rf.com/photo_96155158_stock-vector-cricket-bat-set-on-a-white-background-vector-illustration-.html
    ###########################################################################
    batSize = (120, 120)
    bat = mode.loadImage("images/bat.png")
    mode.batImage = bat.resize(batSize,Image.ANTIALIAS)
    
    shoeSize = (20, 10)
    shoe = mode.loadImage("images/shoe.png")
    mode.shoeImage = shoe.resize(shoeSize,Image.ANTIALIAS)

    padSize = (74, 74)
    pad = mode.loadImage("images/pad3.png")
    mode.padImage = pad.resize(padSize,Image.ANTIALIAS)

    thighSize = (60, 60)
    thigh = mode.loadImage("images/thigh.png")
    mode.thighImage = thigh.resize(thighSize,Image.ANTIALIAS)
    
    upperArmSize = (50, 50)
    upperArm = mode.loadImage("images/upperArm.png")
    mode.upperArmImage = upperArm.resize(upperArmSize, Image.ANTIALIAS)
    
    forearmSize = (50, 50)
    forearm = mode.loadImage("images/forearm.png")
    mode.forearmImage = forearm.resize(forearmSize, Image.ANTIALIAS)
    
###############################################################################
# Game Mode Class from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
###############################################################################
class GameMode(Mode):
    def appStarted(mode):

        mode.gameOver = False
        mode.paused = False
        mode.balls = []
        mode.gravity = 90
        mode.count = 0
        mode.margin = 20
        mode.lowerMargin = 100
        mode.gameOverMargin = 50
        loadImages(mode)
        mode.frameHeight = mode.height - mode.lowerMargin
        mode.timerDelay = 1
        mode.runs = 0
        mode.ballsBowled = 0
        mode.strikeRate = 0

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
        if event.key == "d":
            newBall = Ball(mode.cursor.x, mode.cursor.y)
            mode.balls.append(newBall)
        if event.key == "g":
            batterOut(mode)


    def mousePressed(mode, event):
        if not mode.gameOver:    
            pass            
            #newBall = Ball(event.x, event.y)
            #mode.balls.append(newBall)
        else:
            for button in mode.gameOverButtons:
                if button.inButton(event.x, event.y):
                    if button.onClick == 'restartGame':
                        restartGame(mode)
                    elif button.onClick == 'goHome':
                        mode.appStarted()
                        mode.app.setActiveMode(mode.app.splashScreenMode)

    def timerFired(mode):
        if (not mode.paused) and (not mode.gameOver): 
            GameMode.doStep(mode)
            
    @staticmethod #runs when game isnt paused      
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
        font = 'Arial 14 bold'
        for border in mode.borders:
            color = 'black' if border.color == 'yellow' else 'white'
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
            if border.leftStart != border.leftEnd:
                canvas.create_text(7, mode.frameHeight * border.leftStart + 2,
                                    anchor = 'nw', text = border.runs, 
                                    font = font, fill = color)
                canvas.create_text(7, mode.frameHeight * border.leftEnd - 2,
                                    anchor = 'sw', text = border.runs, 
                                    font = font, fill = color)
            if border.topStart != border.topEnd:
                canvas.create_text(mode.width * border.topStart + 7, 2,
                                    anchor = 'nw', text = border.runs,
                                    font = font, fill = color)
                canvas.create_text(mode.width * border.topEnd - 7, 2,
                                    anchor = 'ne', text = border.runs,
                                    font = font, fill = color)
            if border.rightStart != border.rightEnd:
                canvas.create_text(mode.width - 7, mode.frameHeight * border.rightStart + 2,
                                    anchor = 'ne', text = border.runs,
                                    font = font, fill = color)
                canvas.create_text(mode.width - 7, mode.frameHeight * border.rightEnd - 2,
                                    anchor = 'se', text = border.runs,
                                    font = font, fill = color)

        canvas.create_rectangle(0, mode.frameHeight, mode.width, mode.height, 
                                fill = 'black')

    @staticmethod
    def drawRunsLabels(mode, canvas):
        for label in mode.runsLabels:
            canvas.create_oval(label.x - label.radius, label.y - label.radius, 
                                label.x + label.radius, label.y + label.radius,
                                fill = label.color)
            canvas.create_text(label.x, label.y, text = label.runs, 
                                fill = 'white', 
                                font = f'calibri {int(label.size)} bold')


    def mouseMoved(mode, event):
        mode.cursor.x = event.x
        mode.cursor.y = event.y
        mode.cursor.type = 'arrow'
        if mode.gameOver:
            for button in mode.gameOverButtons:
                if button.inButton(mode.cursor.x, mode.cursor.y):
                    button.hover = True
                    mode.cursor.type = "hand"
                else:
                    button.hover = False
        

    def redrawAll(mode, canvas):
        canvas.config(cursor=mode.cursor.type)
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill = 'light blue')
        GameMode.drawBackground(mode, canvas)
        drawBatter(mode, canvas)
        drawStumps(mode, canvas)
        drawBalls(mode, canvas)
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
                        text=mode.score, 
                        font = "Arial 30 bold")
    for button in mode.gameOverButtons:
        if button.hover:
            color = button.hoverColor
        else:
            color = button.color
        canvas.create_rectangle(button.x1 - 5, button.y1 - 5, button.x2 + 5, 
                                button.y2 + 5, fill=button.color)
        canvas.create_rectangle(button.x1, button.y1, button.x2, button.y2, 
                                fill=color, width = 0)
        canvas.create_text((button.x1 + button.x2)/2, (button.y1 + button.y2)/2, 
                                fill=button.textColor, text=button.text, 
                                font = "Arial 20 bold")                        



def gameOverButtons(mode):
    playAgain = Button(mode.width/3, mode.margin + mode.gameOverMargin + 180,
                    mode.width/2 - 20, mode.margin + mode.gameOverMargin + 240,
                    'red', 'black', 'restartGame', "Play Again", 'white')
    home = Button(mode.width/2 + 20, mode.margin + mode.gameOverMargin + 180,
                 2*mode.width/3, mode.margin + mode.gameOverMargin + 240,
                    'red', 'black', 'goHome', "Home", 'white')
    mode.gameOverButtons = [playAgain, home]

def drawScore(mode, canvas):
    font = "Arial 18 bold"
    canvas.create_text(mode.margin*2, mode.height - mode.lowerMargin + mode.margin,
                    fill='red', text="SWING CRICKET", font = "Arial 50 bold",
                    anchor = 'nw')
    canvas.create_text(mode.width - mode.margin * 2, 
                        mode.height - mode.lowerMargin + 0.75 * mode.margin,
                        anchor = 'ne', text = f'Runs: {mode.runs}', 
                        fill= 'white', font = font)
    canvas.create_text(mode.width - mode.margin * 2, 
                        mode.height - mode.lowerMargin + 2 * mode.margin,
                        anchor = 'ne', text = f'Strike Rate: {mode.strikeRate}',
                        fill= 'white', font = font)
    canvas.create_text(mode.width - mode.margin * 2, 
                        mode.height - mode.lowerMargin + 3.25 * mode.margin,
                        anchor = 'ne', text = f'High Score: {mode.app.highScore}',
                        fill= 'white', font = font)
    




def createBorder(mode):
    out = Border(0, 'yellow', 0, 1, 0, 1/2, 0, 0)
    run1 = Border(1, 'purple', 0, 0, 0, 0, 4/5, 1)
    run2 = Border(2, 'blue', 0, 0, 0, 0 , 3/5, 4/5)
    run4 = Border(4, 'green', 0, 0, 0, 0, 1/5, 3/5)
    run6 = Border(6, 'orange', 0, 0, 1/2, 1, 0, 1/5) 
    mode.borders = [out, run1, run2, run4, run6]

class LeaderboardMode(Mode):
    def appStarted(mode):        
        mode.cursor = Cursor()
        mode.margin = 50 
        home = Button(mode.width/2 - 50, mode.margin + 375, 
                            mode.width/2 + 50, mode.margin + 425, 
                            'red', 'black', 'goHome', "Home", 'white')
        mode.buttons = [home]
        
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height,
                                fill = 'black')
        canvas.create_text(mode.width/2, mode.margin + 30, 
                            fill='red', text="SWING CRICKET", 
                            font = "Arial 50 bold")
        
        canvas.create_rectangle(mode.width/2 - 200, mode.margin + 100,
                                mode.width/2 - 150, mode.margin + 120,
                                outline='white')
        canvas.create_rectangle(mode.width/2 - 150, mode.margin + 100,
                                mode.width/2 + 150, mode.margin + 120,
                                outline='white')
        canvas.create_rectangle(mode.width/2 + 150, mode.margin + 100,
                                mode.width/2 + 200, mode.margin + 120,
                                outline='white')
        canvas.create_text(mode.width/2 - 175, mode.margin + 110,
                            fill='white', text = '#', font="Arial 12 bold")
        canvas.create_text(mode.width/2, mode.margin + 110,
                        fill='white', text = "Username", font="Arial 12 bold")
        canvas.create_text(mode.width/2 + 175, mode.margin + 110,
                            fill='white', text = "Score", font="Arial 12 bold")

        tempLeaderboard = copy.copy(mode.app.leaderboard)
        index = 0
        while len(tempLeaderboard) > 0:
            index += 1
            maxScore = max(tempLeaderboard)
            maxName = tempLeaderboard[maxScore]
            del tempLeaderboard[maxScore]

            # leaderboard position
            canvas.create_rectangle(mode.width/2 - 200, 
                                    mode.margin + 100 + index*20,
                                    mode.width/2 - 150, 
                                    mode.margin + 120 + index*20,
                                    outline='white')
            canvas.create_text(mode.width/2 - 175, mode.margin + 110 + index*20,
                                    fill='white', text = index)
            # name
            canvas.create_rectangle(mode.width/2 - 150, 
                                    mode.margin + 100 + index*20,
                                    mode.width/2 + 150, 
                                    mode.margin + 120 + index*20,
                                    outline='white')
            canvas.create_text(mode.width/2, mode.margin + 110 + index*20,
                                    fill='white', text = maxName)
            
            # score
            canvas.create_rectangle(mode.width/2 + 150, 
                                    mode.margin + 100 + index*20,
                                    mode.width/2 + 200, 
                                    mode.margin + 120 + index*20,
                                    outline='white')
            canvas.create_text(mode.width/2 + 175, mode.margin + 110 + index*20,
                                    fill='white', text = maxScore)

        for button in mode.buttons:
            if button.hover:
                color = button.hoverColor
            else: 
                color = button.color
            canvas.create_rectangle(button.x1 - 5, button.y1 -5, button.x2 + 5,
                                    button.y2 + 5, fill=button.color)
            canvas.create_rectangle(button.x1, button.y1, button.x2, button.y2, 
                                    fill=color, width = 0)
            canvas.create_text((button.x1 + button.x2)/2, (button.y1 + button.y2)/2, 
                                    fill=button.textColor, text=button.text, 
                                    font = "Arial 20 bold")
        canvas.config(cursor=mode.cursor.type)     
      
    def mouseMoved(mode, event):
        mode.cursor.x = event.x
        mode.cursor.y = event.y
        mode.cursor.type = 'arrow'
        for button in mode.buttons:
            if button.inButton(mode.cursor.x, mode.cursor.y):
                button.hover = True
                mode.cursor.type = "hand"
            else:
                button.hover = False
          
    def mousePressed(mode, event):
        for button in mode.buttons:
            if button.inButton(event.x, event.y):
               if button.onClick == 'goHome':
                   mode.appStarted()
                   mode.app.setActiveMode(mode.app.splashScreenMode)



###############################################################################
# App setup from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
###############################################################################
class SwingCricket(ModalApp):
    def appStarted(app):
        app.user = "player1"
        app.highScore = readHighScore('highScores.txt', app.user)
        app.leaderboard = readLeaderboardFile("leaderboard.txt")
        app.learboardLowest = min(app.leaderboard)
        app.graphics = True

        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.leaderboardMode = LeaderboardMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 1

app = SwingCricket(width=840, height=520)










