import Adafruit_BBIO.GPIO as GPIO
import time
import traceback
    
PinIn = "P8_7"

# GPIO.setup(PinIn, GPIO.IN)
GPIO.setup(PinIn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


        
def poll_sensor(): #Pulls data from sensor

    value = GPIO.input(PinIn) #Current pin state
    while value: #Waits until pin is pulled low
        value = GPIO.input(PinIn)
    
    startTime = time.time() #Sets start time

    num1s = 0 #Number of consecutive 1s
    command = [] #Pulses and their timings
    previousValue = 0 #The previous pin state
    while True:
        if value != previousValue: #Waits until change in state occurs
            now = time.time() #Records the current time
            pulseLength = (now - startTime) * 1000000 #Calculate time in between pulses in microseconds
            startTime = now #Resets the start time
            command.append((previousValue, pulseLength)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
        
        #Interrupts code if an extended high period is detected (End Of Command)    
        if value:
            num1s += 1
        else:
            num1s = 0
        
        if num1s > 10000:
            break
        
        #Reads values again
        previousValue = value
        value = GPIO.input(PinIn)
        
    binary = 0b1 #Decoded binary command
    #Covers data to binary
    for (typ, tme) in command:
        if typ == 1:
            binary = binary << 1
            if tme > 1000: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
                binary += 1
                
    if binary.bit_length() > 34: #Sometimes the binary has two rouge charactes on the end
        binary = binary >> (binary.bit_length() - 34)
        
    return binary
    
#Main program loop
try:
    while True:
        command = poll_sensor()
        print("command:", hex(command))
except:
    print(traceback.format_exc())
finally:
    GPIO.cleanup()
