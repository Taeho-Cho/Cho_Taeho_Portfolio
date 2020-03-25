# 7-seg : GPIO pin map
# pin 1 : GPIO 2
# pin 2 : GPIO 3
# pin 3 : GPIO 26
# pin 4 : GPIO 4
# pin 5 : GPIO 17
# pin 6 : GPIO 27
# pin 7 : GPIO 22
# pin 8 : GPIO 10
# pin 9 : GPIO 9
# pin 10 : GPIO 11
# pin 11 : GPIO 5
# pin 12 : GPIO 6

# code modified, tweaked and tailored from code by bertwert
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins
segments =  (5,22,4,3,2,11,17,26)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (6,9,10,27)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
    
    
try:
        while True:
                n = time.ctime()[11:13]+time.ctime()[14:16]
                s = str(n).rjust(4)
                for digit in range(4):
                        for loop in range(0,7):
                                GPIO.output(segments[loop], num[s[digit]][loop])
                                if digit == 1 :
                                        GPIO.output(26, 1)
                                else :
                                        GPIO.output(26, 0)
                        GPIO.output(digits[digit], 0)
                        time.sleep(0.001)
                        GPIO.output(digits[digit], 1)
finally:
    GPIO.cleanup()
    
