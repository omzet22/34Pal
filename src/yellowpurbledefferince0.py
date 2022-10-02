from re import A
import RPi.GPIO as GPIO 
import  time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
in1  =  5  # Forward
in2  = 22  # Backward
in3  = 27  # Left
in4  = 17  # Right
en   = 26  # The pin that we can control the voltage of L298N to motor from it
temp = 1   # Just true for while loop

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
while 1:
    purble = distance1()
    yellow = distance2()
    GPIO.output(in1,GPIO.HIGH)
    p.ChangeDutyCycle(70)
    if purble > 90:
        purble = 90
    if yellow > 90:
        yellow = 90
    if purble > yellow:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in3,GPIO.HIGH) #Trun off pin  5
            p.ChangeDutyCycle(90)
            time.sleep(0.2)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW) #Trun off pin  5
    elif yellow > purble:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in4,GPIO.HIGH) #Trun off pin  5
            p.ChangeDutyCycle(90)
            time.sleep(0.4)

            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW) #Trun off pin  5
    else:
            GPIO.output(in1,GPIO.HIGH)
            p.ChangeDutyCycle(52)

