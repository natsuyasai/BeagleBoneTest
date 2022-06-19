import Adafruit_BBIO.GPIO as GPIO
import time

Pin = "P9_41"
# 片方はGNDに接続，通常1，押下時0
GPIO.setup(Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print(GPIO.input(Pin))
    time.sleep(1)