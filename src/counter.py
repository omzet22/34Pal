from re import A
import RPi.GPIO as GPIO 
import  time
import cv2
import numpy as np
import RPi.GPIO as GPIO
upperorange = np.array([20, 255, 255])
lowerorange = np.array([10, 100, 100])

webcam_video = cv2.VideoCapture(2)
upperblue = np.array([120, 205, 185])  # for blue lines
lowerblue = np.array([88, 70, 50])
counter = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
in1  =  5  # Forward
in2  = 22  # Backward
in3  = 27  # Left
in4  = 17  # Right
en   = 26  # The pin that we can control the voltage of L298N to motor from it
temp = 1   # Just true for while loop
color = 0
dd=0
GPIO.setup(in1,GPIO.OUT)  #Setup pin  5 as Output
GPIO.setup(in2,GPIO.OUT)  #Setup pin 22 as Output
GPIO.setup(in3,GPIO.OUT)  #Setup pin 27 as Output
GPIO.setup(in4,GPIO.OUT)  #Setup pin 17 as Output
GPIO.setup(en,GPIO.OUT)   #Setup pin 26 as Voltage Control

GPIO.output(in1,GPIO.LOW) #Trun off pin  5
GPIO.output(in2,GPIO.LOW) #Trun off pin 22
GPIO.output(in3,GPIO.LOW) #Trun off pin 27
GPIO.output(in4,GPIO.LOW) #Trun off pin 17

p = GPIO.PWM(en,1000)     #p = control the voltage of l298n "Percentage?"
p.start(25)               #Start the motor with 25% of max speed

TRIG = 18
ECHO = 24
maxTime = 0.04
#set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
def distance1():

        GPIO.output(TRIG,False)

        time.sleep(0.01)

        GPIO.output(TRIG,True)

        time.sleep(0.00001)

        GPIO.output(TRIG,False)

        pulse_start = time.time()
        timeout = pulse_start + maxTime
        while GPIO.input(ECHO) == 0 and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()
        timeout = pulse_end + maxTime
        while GPIO.input(ECHO) == 1 and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        return distance

TRIG2 = 16
ECHO2 = 25
maxTime2 = 0.04
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

def distance2():

        GPIO.output(TRIG2,False)

        time.sleep(0.01)

        GPIO.output(TRIG2,True)

        time.sleep(0.00001)

        GPIO.output(TRIG2,False)

        pulse_start = time.time()
        timeout = pulse_start + maxTime2
        while GPIO.input(ECHO2) == 0 and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()
        timeout = pulse_end + maxTime
        while GPIO.input(ECHO2) == 1 and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        return distance
def orangefinder():
    success, video = webcam_video.read() # Reading webcam footage
    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
    GPIO.output(in1,True)     #Turn on the forward motor
    p.ChangeDutyCycle(35)     #Set the spped of the motor 55% of the full speed
    maskorange = cv2.inRange(img, lowerorange, upperorange) # Masking the image to find our color
    mask_contours, hierarchy = cv2.findContours(maskorange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    maskblue = cv2.inRange(img, lowerblue, upperblue) # Masking the image to find our color
    mask_contoursblue, hierarchy = cv2.findContours(maskblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image


    if len(mask_contours) !=0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                return 1
            else:
                return 0
def bluefinder():
    success, video = webcam_video.read() # Reading webcam footage
    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
    GPIO.output(in1,True)     #Turn on the forward motor
    p.ChangeDutyCycle(35)     #Set the spped of the motor 55% of the full speed
    maskorange = cv2.inRange(img, lowerorange, upperorange) # Masking the image to find our color
    mask_contours, hierarchy = cv2.findContours(maskorange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    maskblue = cv2.inRange(img, lowerblue, upperblue) # Masking the image to find our color
    mask_contoursblue, hierarchy = cv2.findContours(maskblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image



    if len(mask_contoursblue) != 0:
        for mask_contourblue in mask_contoursblue:
            if cv2.contourArea(mask_contourblue) > 500:
                return 1

while(1):
    success, video = webcam_video.read() # Reading webcam footage
    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
    GPIO.output(in1,True)     #Turn on the forward motor
    p.ChangeDutyCycle(35)     #Set the spped of the motor 55% of the full speed
    maskorange = cv2.inRange(img, lowerorange, upperorange) # Masking the image to find our color
    mask_contours, hierarchy = cv2.findContours(maskorange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    maskblue = cv2.inRange(img, lowerblue, upperblue) # Masking the image to find our color
    mask_contoursblue, hierarchy = cv2.findContours(maskblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    if len(mask_contours) !=0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                dd = 1
            else:
                dd = 0
    if len(mask_contoursblue) != 0:
        for mask_contourblue in mask_contoursblue:
            if cv2.contourArea(mask_contourblue) > 500:
                dd = 2

            else:
                dd = 0
    if dd == 1:
            color = 1
            break
    elif dd == 2:
            color = 2
            break

if color == 1:
    while 1:
        if counter == 12:
            GPIO.output(in1,GPIO.LOW) #Trun off pin  5
            GPIO.output(in2,GPIO.LOW) #Trun off pin 22
            GPIO.output(in3,GPIO.LOW) #Trun off pin 27
            GPIO.output(in4,GPIO.LOW) #Trun off pin 17
            break

        success, video = webcam_video.read() # Reading webcam footage
        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
        maskorange = cv2.inRange(img, lowerorange, upperorange) # Masking the image to find our color
        mask_contours, hierarchy = cv2.findContours(maskorange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
        if len(mask_contours) !=0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 500:
                    counter+=1
                    break
        print(counter)
        purble = distance1()
        yellow = distance2()
        GPIO.output(in1,GPIO.HIGH)
        p.ChangeDutyCycle(60)
        if purble > 90:
            pruble = 90
        if yellow > 90:
            yellow = 90
        if purble > yellow:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(43)
                time.sleep(0.3)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW) #Trun off pin  5
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(90)
                time.sleep(0.6)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
        elif yellow > purble:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(60)
                time.sleep(0.2)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(90)
                time.sleep(0.2)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in1,GPIO.LOW)
        else:
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(82)

        if purble > yellow:
                if orangefinder() == 1:
                    counter+=1
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(62)
                time.sleep(0.2)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW) #Trun off pin  5
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(50)
                time.sleep(0.6)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
                if orangefinder() == 1:
                    counter+=1

        elif yellow > purble:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(100)
                time.sleep(0.7)
                if orangefinder() == 1:
                    counter+=1
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(40)
                time.sleep(0.2)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in1,GPIO.LOW)
        else:
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(82)
                if orangefinder() == 1:
                    counter+=1

elif color == 2:
    while 1:
        if counter == 12:
            GPIO.output(in1,GPIO.LOW) #Trun off pin  5
            GPIO.output(in2,GPIO.LOW) #Trun off pin 22
            GPIO.output(in3,GPIO.LOW) #Trun off pin 27
            GPIO.output(in4,GPIO.LOW) #Trun off pin 17
            break
        print(counter)
        success, video = webcam_video.read() # Reading webcam footage
        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
        maskblue = cv2.inRange(img, lowerblue, upperblue) # Masking the image to find our color
        mask_contoursblue, hierarchy = cv2.findContours(maskblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
        if len(mask_contoursblue) != 0:
            for mask_contourblue in mask_contoursblue:
                if cv2.contourArea(mask_contourblue) > 500:
                    counter+=1
        purble = distance1()
        yellow = distance2()
        GPIO.output(in1,GPIO.HIGH)
        p.ChangeDutyCycle(60)
        if purble > 90:
            pruble = 90
        if yellow > 90:
            yellow = 90
        if purble > yellow:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(90)
                time.sleep(0.6)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW) #Trun off pin  5
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(43)
                time.sleep(0.2)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
        elif yellow > purble:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
                p.ChangeDutyCycle(90)
                time.sleep(0.2)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW) #Trun off pin  5
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(60)
                time.sleep(0.2)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in1,GPIO.LOW)
        else:
                GPIO.output(in1,GPIO.HIGH)
                p.ChangeDutyCycle(82)
