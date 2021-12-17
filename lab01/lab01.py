from PIL import Image
import numpy as np
import cv2 as cv

def draw_circle(data,r):
    print(data.size)
    x = 250
    y = 250
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


data = np.zeros((512,512,3), np.uint8)
draw_circle(data, 100)

image = Image.fromarray(data, 'RGB')
image.save("circle.png")
image.show()


