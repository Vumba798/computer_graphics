import numpy as np
import cv2 as cv

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
                vertices[i+1][0], vertices[i+1][1], 255)
    if isDrawn:
        draw_line(vertices[-1][0], vertices[-1][1],
                vertices[0][0], vertices[0][1], color)

def cyrus_beck():
    global vertices, _from, _to
    normal = []
    for i in range(0, len(vertices)):
        normal.append((
                vertices[i][1] - vertices[(i+1) % len(vertices)][1],
                vertices[(i+1) % len(vertices)][0] - vertices[i][0]
                ))
    diff = [_to[0] - _from[0], _to[1] - _from[1]]

    P0_PEi = []
    for i in range(0, len(vertices)):
        P0_PEi.append([vertices[i][0] - _from[0], vertices[i][1] - _from[1]])
    numerator = []
    denominator = []
    for i in range(0, len(vertices)):
        numerator.append(normal[i][0]*P0_PEi[i][0] + normal[i][1]*P0_PEi[i][1])
        denominator.append(normal[i][0]*diff[0] + normal[i][1]*diff[1])
    tE = []
    tL = []
    for i in range(0, len(vertices)):
        t = numerator[i] / denominator[i]
        if denominator[i] > 0:
            tE.append(t)
        else:
            tL.append(t)
    tmp = [0.0, 1.0]
    for value in tE:
        if value > tmp[0]:
            tmp[0] = value
    for value in tL:
        if value < tmp[1]:
            tmp[1] = value

    if tmp[0] > tmp[1]:
        _from = [-1,-1]
        _to = [-1][-1]
        return

    _from = [_from[0] + diff[0]*tmp[0], _from[1] + diff[1]*tmp[0]]
    _to = [_from[0] + diff[0]*tmp[1], _from[1] + diff[1]*tmp[1]]


def click_and_draw(event,y,x, flags, param):
    global vertices, isDrawn, image, _from, _to

    if event == cv.EVENT_LBUTTONDOWN:
        if not isDrawn:
            vertices.append([x,y])
        elif _from == [-1, -1]:
            _from = [x,y]
        elif _to == [-1,-1]:
            _to = [x,y]
            image = np.zeros((512,512,3),np.uint8)
            polygon(255)
            cyrus_beck()
            if _from != [-1,-1] and _to != [-1,-1]:
                draw_line(_from[0],_from[1],_to[0],_to[1],255)
            _from = [-1,-1]
            _to = [-1,-1]
            cv.imshow("lab02", image)
    elif event ==cv.EVENT_MOUSEMOVE:
        if len(vertices) != 0 and not isDrawn:
            image = np.zeros((512,512,3),np.uint8)
            polygon(255)
            _from = vertices[-1]
            draw_line(_from[0],_from[1], x, y, 255)
            cv.imshow("lab02", image)
        elif isDrawn and _from != [-1,-1] and _to == [-1,-1]:
            image = np.zeros((512,512,3),np.uint8)
            polygon(255)
            draw_line(_from[0], _from[1], x, y, 255)
            cv.imshow("lab02", image)
    elif event == cv.EVENT_MBUTTONUP:
        if len(vertices) != 0:
            isDrawn = True
            image = np.zeros((512,512,3),np.uint8)
            polygon(255)
            cv.imshow("lab02", image)


cv.namedWindow("lab02")
cv.imshow("lab02", image)
cv.setMouseCallback("lab02", click_and_draw)
cv.waitKey(0)
cv.imwrite("result.jpg", image)
