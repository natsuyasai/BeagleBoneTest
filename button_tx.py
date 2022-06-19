import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import traceback


def tx_ir(pin: str, command: int):
    print(hex(command))
    #PWM.start(channel, duty, freq=2000, polarity=0)
    PWM.start(pin, 0)
    PWM.set_duty_cycle(pin, 50)
    time.sleep(0.5)
    PWM.stop(pin)


def main():
    pinTx = "P9_14"
    pinButton = "P9_41"
    # 送受信設定
    GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pinTx, GPIO.OUT)

    TargetCommand = [0x301a3734d, 0x301a310ef, 0x301a7748b, 0x3051aa55e]

    try:
        while True:
            if(not GPIO.input(pinButton)):
                tx_ir(pinTx, 0x301a3734d)
    except:
        print(traceback.format_exc())
    finally:
        GPIO.cleanup()
        PWM.cleanup()


if __name__ == "__main__":
    main()
