import numpy as np
import cv2 as cv
import math

vertices = []
isDrawn = False
image = np.zeros((512,512,3),np.uint8)
_from = [-1,-1]
_to = [-1,-1]

def draw_line(x1,y1,x2,y2,color):
        global image
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

        image[x][y] = color

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
            image[x][y] = color


def polygon(color):
    global image, vertices, isDrawn
    for i in range(0, len(vertices) - 1):
        draw_line(vertices[i][0], vertices[i][1],
                vertices[i+1][0], vertices[i+1][1], color)
    if isDrawn:
        draw_line(vertices[-1][0], vertices[-1][1],
                vertices[0][0], vertices[0][1], color)

def fill_polygon(color):
    global image, vertices, _from, _to, isDrawn
    maxy = vertices[0][1]
    miny = vertices[0][1]
    for point in vertices:
        if point[1] > maxy:
            maxy = point[1]
        if point[1] < miny:
            miny = point[1]
    yarr = [[0.0]]
    for i in range (1, maxy):
        yarr.append([])
    for i in range(0, len(vertices)):
        next = 0
        if i != len(vertices) - 1:
            next = i + 1
        up, down = 0, 0
        if vertices[i][1] > vertices[next][1]:
            up = i
            down = next
        elif vertices[i][1] < vertices[next][1]:
            up = next
            down = i
        else: continue

        k = (vertices[up][1] - vertices[down][1]) / (vertices[up][0] - vertices[down][0])
        for j in range(int(vertices[down][1]), int(vertices[up][1])):
            yarr[j].append((j - vertices[down][1])/k + vertices[down][0])
        for y in range(int(miny), int(maxy)):
            xarr = yarr[y]
            xarr.sort()
            for j in range(0,int(len(xarr)/2)):
                x = xarr[j*2]
                while x < xarr[j*2 + 1]:
                    image[math.floor(x)][y] = color
                    x+=1

def click_and_draw(event,y,x,flags,param):
    global image, vertices,_from,_to, isDrawn
    if event == cv.EVENT_LBUTTONDOWN:
        if not isDrawn:
            vertices.append([x,y])
    elif event == cv.EVENT_MOUSEMOVE:
        if len(vertices) != 0 and not isDrawn:
            image = np.zeros((512,512,3), np.uint8)
            polygon(255)
            _from = vertices[-1]
            draw_line(_from[0], _from[1], x, y, 255)
            cv.imshow("lab05", image)
    elif event == cv.EVENT_MBUTTONDOWN:
        if len(vertices) != 0:
            isDrawn = True
            image = np.zeros((512,512,3), np.uint8)
            polygon(255)
            fill_polygon(255)
            cv.imshow("lab05", image)

cv.namedWindow("lab05")
cv.imshow("lab05", image)
cv.setMouseCallback("lab05", click_and_draw)
cv.waitKey(0)
cv.imwrite("result.jpg",image)
