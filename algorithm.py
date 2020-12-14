# Written by: Nick Gerend, @dataoutsider
# Viz: "RaceDay", enjoy!

from math import acos, pi, sqrt, cos, sin
import matplotlib.pyplot as plt
import operator

#region Data Class
class point:
    def __init__(self, row, column, path, x, y, circle = -1, shape = 0, polygon = True): 
        self.row = row
        self.column = column
        self.path = path
        self.x = x
        self.y = y
        self.circle = circle
        self.shape = shape
        self.polygon = polygon
#endregion

#region Functions
def angleA(a: float, b: float, c: float) -> float:
    x = (b**2 + c**2 - a**2) / (2 * b * c)
    return acos(x) * 180.0 / pi

def angleB(a: float, b: float, c: float) -> float:
    x = (c**2 + a**2 - b**2) / (2 * c * a)
    return acos(x) * 180.0 / pi

def between_radius(r1: float, r2: float, x: float) -> float: 
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

def draw_circle_list(r, x0, y0, points, circle = -1, draw_path = False, shape = 0):
    pointlist = []
    path = 0
    for i in range(points):
        if draw_path:
            path = i
        pointlist.append(point(0,0,path,(x0 + r * cos(2 * pi * i / points)),(y0 + r * sin(2 * pi * i / points)),circle,shape))
    return pointlist

def relative_midpoint(angle, r):
    x = cos(angle * pi/180) * r
    y = sin(angle * pi/180) * r
    return x, y
#endregion

#region Inputs
data = [4257, 62278, 164913, 188078, 101574, 53380, 25408, 11919, 2989, 878, 213, 53, 9, 3]
#27.0, 35.0, 22.4, 19.3, 62.8, 31.4, 40.2
#56, 1399, 5589, 8584, 5390, 2915, 1545, 805,  111,   10,    5,    1
#4257, 62278, 164913, 188078, 101574, 53380, 25408, 11919, 2989, 878, 213, 53, 9, 3, 0, 0, 0, 1
x = 50000.0
#25
#5000.0
buffer = min(data) * 5000.0
#1
#500.0
data = [o + buffer for o in data]
resolution = 1000
list_class_list = []
last_xi = 1
delta = 0
new_zero = 0
circle_xs = []
#endregion

#region Algorithm
for i in range(1, len(data)):
    
    r1 = data[i - 1]
    r2 = data[i]
    r3 = between_radius(r1, r2, x)

    a = r2 + r3
    b = r1 + r3
    c = r1 + r2 + x
    angleA_ = angleA(a, b, c)
    angleB_ = angleB(a, b, c)

    x_3, y_3 = relative_midpoint(angleA_, b)

    pointlist1 = draw_circle_list(r1, new_zero, 0, resolution)
    x_1, y_1 = relative_midpoint(angleA_, r1)
    pointlist1_shape = [o for o in pointlist1 if o.x <= new_zero + x_1]

    pointlist2 = draw_circle_list(r2, new_zero + c, 0, resolution)
    x_2, y_2 = relative_midpoint(180.0 - angleB_, r2)
    pointlist2_shape = [o for o in pointlist2 if o.x >= new_zero + c + x_2]

    pointlist3 = draw_circle_list(r3, new_zero + x_3, y_3, resolution)
    pointlist3_shape = [o for o in pointlist3 if (o.x >= new_zero + x_1) and (o.x <= new_zero + c + x_2) and (o.y <= max(y_1, y_2))]

    pointlist4 = draw_circle_list(r3, new_zero + x_3, -y_3, resolution)
    pointlist4_shape = [o for o in pointlist4 if (o.x >= new_zero + x_1) and (o.x <= new_zero + c + x_2) and (o.y >= min(-y_1, -y_2))]

    if i > 1:
        list_class_list[last_xi] = [o for o in list_class_list[last_xi] if o.x <= new_zero + x_1]
        last_xi += 3
    
    new_zero += c

    if i == 1:
        list_class_list.append(pointlist1_shape)
    list_class_list.append(pointlist2_shape)
    list_class_list.append(pointlist3_shape)
    list_class_list.append(pointlist4_shape)
#endregion

#region Store Results
collection = []
for i in range(len(list_class_list)):
    collection += list_class_list[i]
#endregion

#region Add Circles
new_zero = 0
for i in range(0, len(data)):
    if i > 0:
        new_zero += data[i] 
    collection += draw_circle_list(data[i] - buffer, new_zero, 0, resolution, 0)
    new_zero += data[i] + x
#endregion

#region Plot
# x = [o.x for o in collection]
# y = [o.y for o in collection]
# plt.scatter(x, y)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()
#endregion

#region Create final collection to copy certain rows for the path
collection_path = []
col_up_outer = [o for o in collection if (o.y >= 0) and (o.circle == -1)]
col_up_inner = [o for o in collection if o.y >= 0 and (o.circle == 0)]
col_down_inner = [o for o in collection if (o.y >= 0) and (o.circle == -1)]
col_down_outer = [o for o in collection if o.y >= 0 and (o.circle == 0)]

col_up_outer.sort(key=operator.attrgetter('x'), reverse = False)
col_up_inner.sort(key=operator.attrgetter('x'), reverse = True)
col_down_inner.sort(key=operator.attrgetter('x'), reverse = False)
col_down_outer.sort(key=operator.attrgetter('x'), reverse = True)

[collection_path.append(point(0, 0, i, o.x, o.y)) for i, o in enumerate(col_up_outer)]
[collection_path.append(point(0, 0, i + len(col_up_outer), o.x, o.y, 0)) for i, o in enumerate(col_up_inner)]
[collection_path.append(point(0, 0, i + len(col_up_outer) + len(col_up_inner), o.x, -o.y, 0)) for i, o in enumerate(col_down_inner)]
[collection_path.append(point(0, 0, i + len(col_up_outer) + len(col_up_inner) + len(col_down_inner), o.x, -o.y)) for i, o in enumerate(col_down_outer)]
#endregion

#region Add Extra Circle Polygons
new_zero = 0
for i in range(0, len(data)):
    if i > 0:
        new_zero += data[i]
    collection_path += draw_circle_list(data[i] - buffer, new_zero, 0, resolution, 0, True, i+1)
    new_zero += data[i] + x
#endregion

#region Add Extra Circle mid-points
new_zero = 0
for i in range(0, len(data)):
    if i > 0:
        new_zero += data[i]
    collection_path += [point(0,0,0, new_zero,0,0,i+1, False)]
    new_zero += data[i] + x
#endregion

#region Write out file

import csv
import os
with open(os.path.dirname(__file__) + '/r_chain_sum.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['x', 'y', 'path', 'shape', 'polygon'])
    for item in collection_path:
        writer.writerow([item.x, item.y, item.path, item.shape, item.polygon])
#endregion