# Written by: Nick Gerend, @dataoutsider
# Viz: "Race Day", enjoy!

from math import acos, pi, sqrt, cos, sin
import matplotlib.pyplot as plt
import operator
import os
import pandas as pd
import numpy as np
import random

#region Data Class
class point:
    def __init__(self, row, column, path, x, y, circle = -1, shape = 0, polygon = True, year = 0, val = -1): 
        self.row = row
        self.column = column
        self.path = path
        self.x = x
        self.y = y
        self.circle = circle
        self.shape = shape
        self.polygon = polygon
        self.year = year
        self.val = val
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
#data
df = pd.read_csv(os.path.dirname(__file__) + '/allyears.csv', engine='python')
#df = df.loc[df['year'].isin([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])]
df = df.loc[df['year'] >= 1990]
# df = df.loc[df['year'] == 2019]
# df['year'] = 0
df_group = df.groupby('year')
#variables
x = 5000.0
hr_res = 2
resolution = 1000
ring_scale = 10.0
gender = True
#constants
buffer = 0
last_xi = 1
new_zero = 0
#lists
list_class_list = []
circle_xs = []
collection = []
collection_path = []
final_list = []
data = []
idata = []
databins = []
#endregion

for year in df_group:
    
    if year[0] == 1996:
        stuff = 2

    #region Initialize
    if gender:
        check = year[1].groupby(['gender'])['gender'].agg('count')
        idata = year[1].groupby(['gender'])['gender'].agg('count')._values[:2]
        x = (min(idata)/2)*((max(idata)/min(idata))**2)
    else:
        values = year[1]['seconds']._values / 3600
        tmax = int(max(values)) + 1   
        hmax = tmax * hr_res + 1
        xbins = [x * (1/hr_res) for x in range(0, hmax)]
        hist = np.histogram(values, bins=xbins)
        databins = hist[1]
        idata = hist[0]
        idata = np.trim_zeros(hist[0])

    list_class_list.clear()
    last_xi = 1
    new_zero = 0
    buffer = max(idata) / ring_scale    
    data = [o + buffer + random.random() for o in idata]
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
    collection.clear()
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

    #region Create final collection to copy certain rows for the path
    collection_path.clear()
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
        collection_path += [point(0,0,0, new_zero,0,0,i+1, False, 0, idata[i])]
        new_zero += data[i] + x
    #endregion

    #region Finalize Output
    for i in range(0, len(collection_path)):
        collection_path[i].year = year[0]
        if collection_path[i].shape == 0:
            collection_path[i].val = sum(idata)
    [final_list.append(x) for x in collection_path]
    #endregion
    
    print(year[0])

#region Write out file
import csv
import os
with open(os.path.dirname(__file__) + '/r_chain_gender1990_2019.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['x', 'y', 'path', 'shape', 'polygon', 'year', 'value'])
    for item in final_list:
        writer.writerow([item.x, item.y, item.path, item.shape, item.polygon, item.year, item.val])
print('finished')
#endregion