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

        image[y][x] = color

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
            image[y][x] = color

def line_intersection(line1, line2):
    if line1[0][1] == line2[0][1]:
        return line2[0][0], line1[0][1]
    if line2[0][1] == line2[1][1]:
        return line2[1][0], line1[0][1]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



def polygon(color):
    global image, vertices, isDrawn
    for i in range(0, len(vertices) - 1):
        draw_line(vertices[i][0], vertices[i][1],
                vertices[i+1][0], vertices[i+1][1], color)
    if isDrawn:
        draw_line(vertices[-1][0], vertices[-1][1],
                vertices[0][0], vertices[0][1], color)

def fill_polygon(color):
    global image, vertices, isDrawn
    print("vertices:",vertices)
    maxy = vertices[0][1]
    miny = vertices[0][1]
    edges = []
    for i in range(0, len(vertices)):
        edges.append([vertices[i -1], vertices[i]])
    
    for point in vertices:
        if point[1] > maxy:
            maxy = point[1]
        if point[1] < miny:
            miny = point[1]
    
    for y in range(miny+1, maxy-1):
        xarr = []
        for edge in edges:
            vertA = edge[0]
            vertB = edge[1]
            if y < vertA[1] and y >= vertB[1] or y >= vertA[1] and y < vertB[1]:
                x,tmp = line_intersection([[0,y],[512,y]],edge)
                xarr.append(x)
        intersectionsAmount = len(xarr)
        print(xarr, y)
        if intersectionsAmount%2 == 1:
            print("mod = 1",xarr)
            intersectionsAmount = intersectionsAmount - 1
        for i in range(1, intersectionsAmount, 2):
            odd = int(xarr[i-1])
            even = int(xarr[i])
            draw_line(odd,y,even,y,color)
            for x in range(even,odd):
                if y == miny + 20:
                    print("x =", x)

def click_and_draw(event,x,y,flags,param):
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
            vertices.append([x,y])
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
