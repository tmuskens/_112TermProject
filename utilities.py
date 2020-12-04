import math

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def cosineRuleAngle(a,b,c):
    cosTheta = (a**2 + b**2 - c**2)/(2*a*b)
    #print(a, b, c, cosTheta)
    if cosTheta > 1:
        print(a, b, c, cosTheta)
        print('error')
        cosTheta = 1
    if cosTheta < -1:
        print(a, b, c, cosTheta)
        print('error')
        cosTheta = -1
    return math.acos(cosTheta)

def sineRuleAngle(side1, theta1, side2):
    return math.asin((side2 * math.sin(theta1))/side1)

def perpendicularDistance(A, B, C, x, y):
    numerator = abs(A*x + B*y + C)
    denominator = (A**2 + B**2)**0.5
    return numerator/denominator