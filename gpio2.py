import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for i in range(10):
    if GPIO.input(25):
        print("LED on")
        GPIO.output(18, True)
        time.sleep(1)
    else:
        print("LED off")
        GPIO.output(18, False)
        time.sleep(1)
GPIO.cleanup()

