import numpy as np
import cv2
import time
from Image import *

def SlicePart(im, images, slices):
    height, width = im.shape[:2]
    sl = int(height/slices);
    
    for i in range(slices):
        part = sl*i
        crop_img = im[part:part+sl, 0:width]
        images[i].image = crop_img
        images[i].Process()
    
def RepackImages(images):
    img = images[0].image
    for i in range(len(images)):
        if i == 0:
            img = np.concatenate((img, images[1].image), axis=0)
        if i > 1:
            img = np.concatenate((img, images[i].image), axis=0)
            
    return img

def Center(moments):
    if moments["m00"] == 0:
        return 0
        
    x = int(moments["m10"]/moments["m00"])
    y = int(moments["m01"]/moments["m00"])

    return x, y
    
def roi(img, vertices):
    return img[vertices[0][0]:vertices[0][1], vertices[0][2]:vertices[0][3]]
    
def RemoveBackground(image, b):

    #lower = np.array([60, 20, 0], dtype = "uint8") #rgb
    lower = np.array([0, 20, 60], dtype = "uint8") #bgr
    #upper = np.array([230, 230, 230], dtype = "uint8") #rgb
    upper = np.array([230, 230, 230], dtype = "uint8") #bgr
    #----------------COLOR SELECTION-------------- (Remove any area that is whiter than 'upper')
    if b == True:
        image = cv2.blur(image, (5, 7), 0)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(image, lower, upper)
        image = mask#(255-mask)
        #cv2.imshow('asd',mask)
        #image = cv2.bitwise_and(image, image, mask = mask)
        #image = cv2.bitwise_not(image, image, mask = mask)
        #image[np.where((image == [0,0,0]).all(axis = 2))] = [255,255,255]
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        #cv2.imshow("canny", image)
        return image
    else:
        return image
    #////////////////COLOR SELECTION/////////////
    