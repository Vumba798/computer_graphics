import time
import math
import argparse
import cv2 as cv
import numpy as np
from PIL import Image

def draw_circle(data,x0, y0, r):
    x = x0
    y = y0
    disp_x = x
    disp_y = y
    x = 0
    y = r
    delta = (1-2*r)
    error = 0
    while y >= 0:
        data[disp_x + x][disp_y + y] = 255
        data[disp_x + x][disp_y - y] = 255
        data[disp_x - x][disp_y + y] = 255
        data[disp_x - x][disp_y - y] = 255

        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <=0)):
            x+=1
            delta = delta + (2*x+1)
            continue
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            y -= 1
            delta = delta + (1 - 2 * y)
            continue
        x += 1
        delta = delta + (2 * (x - y))
        y -= 1

def draw_line(data,x1,y1,x2,y2,color):
         
        dx = x2 - x1
        dy = y2 - y1
        
        sign_x = 1 if dx>0 else -1 if dx<0 else 0
        sign_y = 1 if dy>0 else -1 if dy<0 else 0
        
        if dx < 0: dx = -dx
        if dy < 0: dy = -dy
        
        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy
        
        x, y = x1, y1
        
        error, t = el/2, 0        
        
        data[x][y] = color
        
        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            data[x][y] = color
alpha = 0.0
radius = 100
x0 = 200
y0 = 200
data = np.zeros((512,512,3), np.uint8)

draw_circle(data,x0,y0,radius)
while True:
    draw_line(data, x0,y0, x0+radius*math.cos(alpha), y0+radius*math.sin(alpha), 255)
    cv.imshow("lab01", data)
    cv.imwrite("result.jpg", data)
    cv.waitKey(1)
    time.sleep(1)
    draw_line(data, x0,y0, x0+(radius-1)*math.cos(alpha), y0+(radius-1)*math.sin(alpha), 0)
    alpha += math.pi / 30

