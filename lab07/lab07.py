import cv2 as cv
import numpy as np
import math

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
    image[y,x] = color
    
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
        image[y,x] = color

def fill_polygon(vertices, color):
    global image
    maxy = vertices[0][1]
    miny = vertices[0][1]
    for point in vertices:
        if point[1] > maxy:
            maxy = point[1]
        if point[1] < miny:
            miny = point[1]
    yarr = [[0.0]]

    for i in range (1, int(maxy)):
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
                    image[y][math.floor(x)] = color
                    x+=1
def cos(a, b):
    print("a = ", a)
    print("b = ", b)
    dotProduct = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    if dotProduct == 0: return 0
    return dotProduct / (math.sqrt(a[0]**2 + a[1]**2 + a[2]**2) *
                         math.sqrt(b[0]**2 + b[1]**2 + b[2]**2))

def render_diamond():
    global image
    x0 = 250
    y0 = 200
    z0 = -200
    vertices = []
    vertices.append([x0 + 0, y0 + 0, z0 + 78])
    vertices.append([x0 + 45, y0 + 45, z0 + 0])
    vertices.append([x0 + 45, y0 - 45, z0 + 0])
    vertices.append([x0 - 45, y0 - 45, z0 + 0])
    vertices.append([x0 - 45, y0 + 45, z0 + 0])
    vertices.append([x0 + 0, y0 + 0, z0 - 78])

    alpha = math.pi / 2
    betha = math.pi / 6
    
    dataX = [[1,0,0,0],
            [0, math.cos(alpha),-math.sin(alpha), 0],
            [0, math.sin(alpha), math.cos(alpha), 0],
            [0, 0, 0, 1]]
    dataY = [[math.sin(betha),0,math.cos(betha),0],
            [0,1,0,0],
            [math.cos(betha), 0, -math.sin(betha), 0],
            [0,0,0,1]]
    
    for i in range(0, len(vertices)):
        rotated = []
        vec = [vertices[i][0], vertices[i][1], vertices[i][2], 1]
        for j in range(0, 4):
            tmp = 0
            for k in range(0, 4):
                tmp+= dataX[j][k] * vec[k]
            rotated.append(tmp)
        tmpVec = []
        for j in range(0, 4):
            tmp = 0
            for k in range(0, 4):
                tmp += dataY[j][k] * rotated[k]
            tmpVec.append(tmp)
        rotated = tmpVec
        vertices[i] = [rotated[0], rotated[1], rotated[2]]

    facets = [[0,1,2],
              [0,2,3],
              [0,3,4],
              [0,4,1],
              [5,4,3],
              [5,3,2],
              [5,2,1],
              [5,1,4]]
    
    I_fon = 20.0
    I_p = 235.0
    K_p = 0.4

    lamp = [50, 30 ,-20]
    for facet in facets:
        p0 = vertices[facet[0]]
        p1 = vertices[facet[1]]
        p2 = vertices[facet[2]]
        center12 = [(p1[0] + p2[0])/2, (p1[1] + p2[1])/2, (p1[2] + p2[2])/2]
        center = [(center12[0]+p0[0])/2,(center12[1]+p0[1])/2,(center12[2]+p0[2])/2]
        light = [lamp[0] - center[0], lamp[1] - center[1], lamp[2] - center[2]]

        normal = [(p1[1]-p0[1]) * (p2[2]-p0[2]) - (p2[1]-p0[1]) * (p1[2]-p0[2]),
                  (p2[0]-p0[0]) * (p1[2]-p0[2]) - (p1[0]-p0[0]) * (p2[2]-p0[2]),
                  (p1[0]-p0[0]) * (p2[1]-p0[1]) - (p2[0]-p0[0]) * (p1[1]-p0[1])]

        observer = [0,0,-1]
        if (cos(normal,observer) >= 0):
            cos_phi = cos(light, normal)
            I = I_fon + K_p * I_p * cos_phi
            point0 = [p0[0], p0[1]]
            point1 = [p1[0], p1[1]]
            point2 = [p2[0], p2[1]]


            fill_polygon([point0,point1,point2],I)

            draw_line(point0, point1, 60)
            draw_line(point0, point2, 60)
            draw_line(point2, point1, 60)


render_diamond()
cv.namedWindow("lab07")
cv.imshow("lab07", image)
cv.waitKey()
cv.imwrite("result.jpg", image)

