Import PRI.GPIO as GPIO
Import  time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)
For I in range of (20)
GPIO.output(17,true)
Time.sleep(1)
GPIO.output(17,false)
Time.sleep(1)
GPIO.cleanup()
