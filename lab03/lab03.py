import cv2 as cv
import numpy as np
import math

source = cv.imread("source.jpg")
result = source.copy()

def sobel_filter():
    global source, result
    kx = [[-1,0,1],[1,-2,0],[-1,0,1]]
    ky = [[1,2,1],[0,0,0],[-1,-2,-1]]

    height, width, channels = source.shape

    for y in range(1, height - 1):
        for x in range(1, width - 1):
                a = source[y-1,x-1]
                b = source[y,x-1]
                c = source[y+1,x-1]
                d = source[y-1,x]
                e = source[y,x]
                f = source[y+1,x]
                g = source[y-1,x+1]
                h = source[y, x+1]
                i = source[y+1,x+1]

                x1 = a[0]/3+a[1]/3+a[2]
                x2 = b[0]/3+b[1]/3+b[2]/3
                x3 = c[0]/3+c[1]/3+c[2]/3
                x4 = d[0]/3+d[1]/3+d[2]/3
                x5 = e[0]/3+e[1]/3+e[2]/3
                x6 = f[0]/3+f[1]/3+f[2]/3
                x7 = g[0]/3+g[1]/3+g[2]/3
                x8 = h[0]/3+h[1]/3+h[2]/3
                x9 = i[0]/3+i[1]/3+i[2]/3
                matrix = [[x1,x2,x3],
                        [x4,x5,x6],
                        [x7,x8,x9]]

                sumx = 0
                sumy = 0

                for s in range(0, 3):
                    for t in range(0, 3):
                        sumx = sumx + matrix[s][t]*kx[s][t]
                        sumy = sumy + matrix[s][t]*ky[s][t]

                newValue = math.sqrt(sumx*sumx + sumy*sumy)

                if newValue < 0:
                    newValue = 0
                elif newValue > 255:
                    newValue = 255
                result[y][x] = [newValue,newValue,newValue]


sobel_filter()
cv.imshow("lab03",result)
cv.waitKey()
