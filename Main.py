import socket
import sys
import os
import numpy as np
import pdb

import cv2
import time

import move
from Image import *
from Utils import *

from picamera.array import PiRGBArray
from picamera import PiCamera

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0
Images=[]
N_SLICES = 6

MAX_POWER = 40

led = move.PWM()

for q in range(N_SLICES):
    Images.append(Image())

##video_capture = cv2.VideoCapture(0)
##for i in range(0, 30):
##    video_capture.read()
##    time.sleep(0.15)
    
pidSum = 0
pidPrev = 0
pidCurr = 0

pidK1 = 0.7#0.75    
pidK2 = 1.7#1.5#1.5   
pidK3 = 0.01#0.025#0.01  

camera = PiCamera()
#camera.resolution = (320, 240)
#camera.resolution = (240, 160)
camera.resolution = (160, 128)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=camera.resolution)
# allow the camera to warmup
time.sleep(0.1)

def roi(img, vertices):
    return img[vertices[0][0]:vertices[0][1], vertices[0][2]:vertices[0][3]]

print('press enter to start')
input()
try:
    #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    while True:
        
            t1 = time.clock()
            
            camera.capture(rawCapture, format="bgr", use_video_port=True)
            #img = cv2.imread('2.585188.png', 1)
            #img = cv2.imread('4.76795.png', 1)
            #img = cv2.imread('5.54745.png', 1)
            #img = frame.array
            img = rawCapture.array
            #rawCapture.seek(0)
            img = cv2.flip(img, -1)
            #cv2.imshow('asd', img)
            #cv2.waitKey(1)
            #continue
            #imshape = img.shape
            #vertices = [np.array([0,imshape[0]*9/10, imshape[1]/8,imshape[1]-imshape[1]/8],dtype=np.int32)]
            #img = roi(img, vertices)
            
            imshape = img.shape
            vertices = [np.array([imshape[0]/5,imshape[0], imshape[1]*0, imshape[1]],dtype=np.int32)]
            img = roi(img, vertices)
            direction = 0
            img = RemoveBackground(img, True)
            if img is not None:
                SlicePart(img, Images, N_SLICES)
                count = 0
                for i in range(N_SLICES):
                    direction += Images[i].dir
                    if Images[i].dir != 0:
                        count += 1
                    Images[i].dir = 0
                    
                
                if count > 0:
                    average = direction / count
                    pidSum += average * pidK3
                    pidCurrent = average * pidK1 + (average - pidPrev) * pidK2 + pidSum
                
                    pidPrev = average
                
                    #print(count, direction, average)
                
                    fm = RepackImages(Images)
                    t2 = time.clock()
                    cv2.putText(fm,"Time: " + str((t2-t1)*1000) + " ms, dir: "+str(average),(10, 200), font, 0.3,(0,0,255),1,cv2.LINE_AA)
                    #cv2.imwrite('./imgs/'+str(t1)+'.png', fm)
                    print('Time:', (t2-t1)*1000)
                    print('average:', average)
                    print('pid:',pidCurrent)
                    slope = abs(pidCurrent) / 40
                    if pidCurrent < 0:
                        # go left
                        led.set(move.PWM.PIN_LEFT_FORWARD, MAX_POWER)
                        led.set(move.PWM.PIN_RIGHT_FORWARD, MAX_POWER*(1-slope))
                        led.set(move.PWM.PIN_LEFT_BACKWARD, 0)
                        led.set(move.PWM.PIN_RIGHT_BACKWARD, 0)
                    else:
                        led.set(move.PWM.PIN_LEFT_FORWARD, MAX_POWER*(1-slope))
                        led.set(move.PWM.PIN_RIGHT_FORWARD, MAX_POWER)
                        led.set(move.PWM.PIN_LEFT_BACKWARD, 0)
                        led.set(move.PWM.PIN_RIGHT_BACKWARD, 0)
                        # go right
                    
                else:
                    average = 0
                    pidPrev = 0
                    pidSum = 0
                    led.set(move.PWM.PIN_LEFT_FORWARD, 0)
                    led.set(move.PWM.PIN_RIGHT_FORWARD, 0)
                    led.set(move.PWM.PIN_LEFT_BACKWARD, MAX_POWER)
                    led.set(move.PWM.PIN_RIGHT_BACKWARD, MAX_POWER)
                    
               
                led.update()
                #cv2.imwrite('./imgs/'+str(t1)+'.png', fm)
                cv2.imshow("canny", fm)
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
except KeyboardInterrupt:
    led.set(move.PWM.PIN_LEFT_FORWARD, 0)
    led.set(move.PWM.PIN_RIGHT_FORWARD, 0)
    led.set(move.PWM.PIN_LEFT_BACKWARD, 0)
    led.set(move.PWM.PIN_RIGHT_BACKWARD, 0)
    led.update()
    camera.close()
        
finally:
    # Clean up the connection
    #cv2.destroyAllWindows()
    pass
