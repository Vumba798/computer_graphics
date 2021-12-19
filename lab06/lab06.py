import cv2 as cv
import numpy as np
import math

_first = [-1,-1]
_second = [-1,-1]
_third = [-1,-1]
image = np.zeros((512,512,3),np.uint8)

def draw_line(point_from,point_to,color):
    global image
    x1 = point_from[0]
    y1 = point_from[1]
    x2 = point_to[0]
    y2 = point_to[1]
     
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

    x = int(x)
    y = int(y)
    image[x,y] = color
    
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
        image[x,y] = [color, color, color]

def distance(p0, p1, p2):
    k = (p2[1] - p0[1]) / (p2[0] - p0[0])
    b = -k * p0[0] + p0[1]
    return abs(-k * p1[0] + p1[1] - b) / math.sqrt(k*k + 1)

def bezier(p0, p1, p2, color):
    global image
    if distance(p0,p1,p2) > 1:
        p0_1 = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2]
        p1_1 = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
        p0_2 = [(p0_1[0] + p1_1[0]) / 2, (p0_1[1] + p1_1[1]) / 2]
        bezier(p0,p0_1,p0_2,color)
        bezier(p0_2,p1_1, p2, color)
    else:
        draw_line(p0,p2,255)

def bezierRotateX(p0,p1,p2,color):
    global image
    point0 = [p0[0],p0[1],0]
    point1 = [p1[0],p1[1],0]
    point2 = [p2[0],p2[1],0]
    tmp0 = point0
    tmp2 = point2

    for a in range(0,360,10):
        alpha = a * math.pi / 180
        tmp0[0] -= point1[0]
        tmp0[1] -= point1[1]
        tmp2[0] -= point1[0]
        tmp2[1] -= point1[1]
        data = [[1,0,0,0],
                [0,math.cos(alpha),-math.sin(alpha),0],
                [0,math.sin(alpha),math.cos(alpha),0],
                [0,0,0,1]]

        out = []
        vec = [tmp0[0],tmp0[1],tmp0[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP0 = [out[0][0]+point1[0],out[0][1]+point1[1]]

        out = []
        vec = [tmp2[0],tmp2[1],tmp2[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP2 = [out[0][0]+point1[0], out[0][1]+point1[1]]

        bezier(futureP0, p1, futureP2, color)
        tmp0 = point0
        tmp2 = point2

def bezierRotateY(p0,p1,p2,color):
    global image
    point0 = [p0[0],p0[1],0]
    point1 = [p1[0],p1[1],0]
    point2 = [p2[0],p2[1],0]
    tmp0 = point0
    tmp2 = point2

    for a in range(0,360,10):
        alpha = a * math.pi / 180
        tmp0[0] -= point1[0]
        tmp0[1] -= point1[1]
        tmp2[0] -= point1[0]
        tmp2[1] -= point1[1]
        data = [[math.sin(alpha),0,math.cos(alpha),0],
                [0,1,0,0],
                [math.cos(alpha),0,-math.sin(alpha),0],
                [0,0,0,1]]

        out = []
        vec = [tmp0[0],tmp0[1],tmp0[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP0 = [out[0][0]+point1[0],out[0][1]+point1[1]]

        out = []
        vec = [tmp2[0],tmp2[1],tmp2[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP2 = [out[0][0]+point1[0], out[0][1]+point1[1]]

        bezier(futureP0, p1, futureP2, color)

        tmp0 = point0
        tmp2 = point2

def bezierRotateZ(p0,p1,p2,color):
    global image
    point0 = [p0[0],p0[1],0]
    point1 = [p1[0],p1[1],0]
    point2 = [p2[0],p2[1],0]
    tmp0 = point0
    tmp2 = point2

    for a in range(0,360,10):
        alpha = a * math.pi / 180
        tmp0[0] -= point1[0]
        tmp0[1] -= point1[1]
        tmp2[0] -= point1[0]
        tmp2[1] -= point1[1]
        data = [[math.cos(alpha), -math.sin(alpha),0,0],
                [math.sin(alpha), math.cos(alpha),0,0],
                [0,0,0,0],
                [0,0,0,1]]

        out = []
        vec = [tmp0[0],tmp0[1],tmp0[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP0 = [out[0][0]+point1[0],out[0][1]+point1[1]]

        out = []
        vec = [tmp2[0],tmp2[1],tmp2[2],1]
        for i in range(0,3):
            tmp = 0
            for j in range(0,3):
                tmp += data[i][j] * vec[j]
            out.append(tmp)
        futureP2 = [out[0][0]+point1[0], out[0][1]+point1[1]]

        bezier(futureP0, p1, futureP2, color)

        tmp0 = point0
        tmp2 = point2

def click_and_draw(event,y,x,flags,params):
    global _first,_second,_third,image
    if event == cv.EVENT_LBUTTONDOWN:
        if _first == [-1,-1]:
            _first = [-1,-1]
        elif _second == [-1,-1]:
            _second = [x,y]
        elif _third == [-1,-1]:
            _third = [x,y]
            image = np.zeros((512,512,3),np.uint8)
            bezier(_first,_second,_third, 255)
            cv.imshow("lab06", image)
    elif event == cv.EVENT_MOUSEMOVE:
        if _first != [-1,-1] and _second != [-1,-1] and _third == [-1,-1]:
            third = [x,y]
            image = np.zeros((512,512,3),np.uint8)
            bezier(_first,_second,third,255)
            cv.imshow("lab06",image)
    elif event == cv.EVENT_MBUTTONDOWN:
        bezierRotateX(_first,_second,_third, 255)
        cv.imshow("lab06", image)
cv.namedWindow("lab06")
cv.imshow("lab06", image)
cv.setMouseCallback("lab06", click_and_draw)
cv.waitKey(0)
cv.imwrite("result.jpg",image)
