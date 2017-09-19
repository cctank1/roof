import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
for i in range(10):
    print(i)
    print("LED on")
    GPIO.output(18, True)
    time.sleep(1)
    print("LED off")
    GPIO.output(18, False)
    time.sleep(1)
GPIO.cleanup()

