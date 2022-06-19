import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import traceback


def rx_ir(pin: str) -> int:
    num1s: int = 0  # 1秒カウント用
    command: list[tuple[int, int]] = []  # パルスと発生タイミング
    previousInputValue: int = 0  # 前回のpin状態
    
    # 初期読み出し
    inputValue: int = GPIO.input(pin)
    # 入力待ち
    while inputValue:
        inputValue = GPIO.input(pin)
    # 開始時刻取得
    startTime: float = time.perf_counter()

    while True:
        if inputValue != previousInputValue:  # Waits until change in state occurs
            now: float = time.perf_counter()
            pulseLength = (now - startTime) * 1000000  # マイクロ秒単位でパルス間の時間計算
            startTime = now  # 開始時刻更新
            # 前回値はそのタイミングでパルスがONかOFFかを記録する
            command.append((previousInputValue, pulseLength))

        # 1秒間入力されたままなら中断
        if inputValue:
            num1s += 1
        else:
            num1s = 0
        if num1s > 10000:
            break

        # 最新値再取得
        previousInputValue = inputValue
        inputValue = GPIO.input(pin)

    # デコード
    binary = 0b1
    #Covers data to binary
    for (type, tm) in command:
        if type == 1:  # ON
            binary = binary << 1
            # NECプロトコルによると、1687.5マイクロ秒のギャップは論理的な1を表すため、
            # 1000を超えると十分に大きな区別ができます。
            if tm > 1000:
                binary += 1

    # Sometimes the binary has two rouge charactes on the end
    if binary.bit_length() > 34:
        binary = binary >> (binary.bit_length() - 34)
    print(command)
    return binary


def tx_ir(pin: str, command: int):
    print(hex(command))
    #PWM.start(channel, duty, freq=2000, polarity=0)
    PWM.start(pin, 50)
    PWM.stop(pin)


def main():
    pinRx = "P9_11"
    pinTx = "P9_14"
    # 送受信設定
    GPIO.setup(pinRx, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pinTx, GPIO.OUT)

    TargetCommand = [0x301a3734d, 0x301a310ef, 0x301a7748b, 0x3051aa55e]

    try:
        while True:
            command = rx_ir(pinRx)
            #hexCommand = hex(command)
            tx_ir(pinTx, command)
    except:
        print(traceback.format_exc())
    finally:
        GPIO.cleanup()
        PWM.cleanup()


if __name__ == "__main__":
    main()
