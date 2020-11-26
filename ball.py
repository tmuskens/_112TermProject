from cmu_112_graphics import *
class Ball(object):
    radius = 10
    def __init__(self, x, y, dx=0, dy=0):
        self.cx = x
        self.cy = y
        self.dx = dx
        self.time = 0
        self.dy = dy

    def drawBalls(mode, canvas):
        for ball in mode.balls:
            canvas.create_image(ball.cx, ball.cy, image=ImageTk.PhotoImage(mode.ballImage))
