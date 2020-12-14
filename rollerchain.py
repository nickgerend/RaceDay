# Written by: Nick Gerend, @dataoutsider
# Viz: "RaceDay", enjoy!

from math import acos, pi, sqrt, cos, sin
import matplotlib.pyplot as plt

class point:
    def __init__(self, row, column, path, x, y, circle = -1): 
        self.row = row
        self.column = column
        self.path = path
        self.x = x
        self.y = y
        self.circle = circle

def angleA(a, b, c):
    x = (b**2 + c**2 - a**2) / (2 * b * c)
    return acos(x) * 180.0 / pi

def angleB(a, b, c):
    x = (c**2 + a**2 - b**2) / (2 * c * a)
    return acos(x) * 180.0 / pi

def angleC(a, b, c):
    x = (a**2 + b**2 - c**2) / (2 * a * b)
    return acos(x) * 180.0 / pi

def rad1(a, b, c):
    return (-b**2 + a**2 + b*c - c*a) / (2 * (b - a))

def rad2(a, b, c):
    return (-b**2 + a**2 - b*c + c*a) / (2 * (b - a))

def rad3(r1, r2, x): 
    b = max(r1, r2) 
    a = min(r2, r1)
    c = r1 + r2 + x
    rad = ( 
        (2*b*c**3-2*c**3*a+6*c*a**3-2*b*c*a**2+2*b**2*c*a-6*b**3*c+
            sqrt(
                (-2*b*c**3+2*c**3*a-6*c*a**3+2*b*c*a**2-2*b**2*c*a+6*b**3*c)**2-
                4*(-4*c*a**2+4*b**2*c)*(-2*b**2*c**3+2*c**3*a**2-2*c*a**4+2*b**4*c)
                )
        )/(2*(-4*c*a**2+4*b**2*c))
        )

    return rad

def draw_circle(r, x0, y0, points):
    x = []
    y = []
    for i in range(points):
        x.append(x0 + r * cos(2 * pi * i / points))
        y.append(y0 + r * sin(2 * pi * i / points))
    return x, y

def draw_circle_list(r, x0, y0, points):
    pointlist = []
    for i in range(points):
        pointlist.append(point(0,0,0,(x0 + r * cos(2 * pi * i / points)),(y0 + r * sin(2 * pi * i / points)),0))
    return pointlist

def relmidpoint(angle, r):
    x = cos(angle * pi/180) * r
    y = sin(angle * pi/180) * r
    return x, y

def rad4(r1, r2, x, A):
    a = r2
    b = r1
    c = r1 + r2 + x
    return (2 * b * cos(A * pi/180) - b**2 - c**2 + a**2) / (2 * (b-a))

#region point test
r2 = 10.0
r1 = 35.0
x = 50.0
r3 = rad3(r1, r2, x)
angleA = angleA(r2 + r3, r1 + r3, r1 + r2 + x)
angleB = angleB(r2 + r3, r1 + r3, r1 + r2 + x)
print(angleA)
x_3, y_3 = relmidpoint(angleA, r1 + r3)
# x1, y1 = draw_circle(r1, 0, 0, 100)
# x2, y2 = draw_circle(r2, r1 + r2 + x, 0, 100)
# x3, y3 = draw_circle(r3, x_3, y_3, 100)
# x4, y4 = draw_circle(r3, x_3, -y_3, 100)
# plt.scatter(x1 + x2 + x3 + x4, y1 + y2 + y3 + y4)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()
#endregion

pointlist1 = draw_circle_list(r1, 0, 0, 100)
x_1, y_1 = relmidpoint(angleA, r1)
x1 = [o.x for o in pointlist1 if o.x <= x_1]
y1 = [o.y for o in pointlist1 if o.x <= x_1]
pointlist2 = draw_circle_list(r2, r1 + r2 + x, 0, 100)
x_2, y_2 = relmidpoint(180.0 - angleB, r2)
x2 = [o.x for o in pointlist2 if o.x >= r1 + r2 + x + x_2]
y2 = [o.y for o in pointlist2 if o.x >= r1 + r2 + x + x_2]
pointlist3 = draw_circle_list(r3, x_3, y_3, 100)
x3 = [o.x for o in pointlist3 if (o.x >= x_1) and (o.x <= r1 + r2 + x + x_2) and (o.y <= max(y_1, y_2))]
y3 = [o.y for o in pointlist3 if (o.x >= x_1) and (o.x <= r1 + r2 + x + x_2) and (o.y <= max(y_1, y_2))]
pointlist4 = draw_circle_list(r3, x_3, -y_3, 100)
x4 = [o.x for o in pointlist4 if (o.x >= x_1) and (o.x <= r1 + r2 + x + x_2) and (o.y >= min(-y_1, -y_2))]
y4 = [o.y for o in pointlist4 if (o.x >= x_1) and (o.x <= r1 + r2 + x + x_2) and (o.y >= min(-y_1, -y_2))]
plt.scatter(x1 + x2 + x3 + x4, y1 + y2 + y3 + y4)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()