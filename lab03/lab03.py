import cv2 as cv
import numpy as np
import math

source = cv.imread("source.jpg")
result = source.copy()

def sobel_filter():
    global source, result
    kx = [[-1,0,1],[-2,0,2],[-1,0,1]]
    ky = [[1,2,1],[0,0,0],[-1,-2,-1]]

    height, width, channels = source.shape

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            tmp = source[y-1:y+2, x-1:x+2]
            matrix = tmp.sum(axis=2) / 3
            sumx = 0
            sumy = 0
            for s in range(0, 3):
                for t in range(0, 3):
                    sumx = sumx + matrix[s, t]*kx[s][t]
                    sumy = sumy + matrix[s, t]*ky[s][t]
            newValue = math.sqrt(sumx*sumx + sumy*sumy)
            if newValue < 0:
                newValue = 0
            elif newValue > 255:
                newValue = 255
            result[y, x] = [newValue,newValue,newValue]

sobel_filter()
cv.imshow("lab03",result)
cv.waitKey()
cv.imwrite("result.jpg", result)
