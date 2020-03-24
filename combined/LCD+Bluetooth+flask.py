
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND


#import
import RPi.GPIO as GPIO
import time
import threading
from bluepy import btle
from flask import Flask, render_template


# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


app = Flask(__name__)

#res = ''

humidity = ''
temperature = ''
light = ''
noise = ''

class MyDelegate(btle.DefaultDelegate):
        def __init__(self) :
                btle.DefaultDelegate.__init__(self)

        def handleNotification(self,cHandle,data):
                print("handling notification...")
                #print(cHandle) #18
                #print(data),
                dev.writeCharacteristic(cHandle, "recv: " + data.rstrip()+"\n")
                #lcd_string("recv: " + data.rstrip(), LCD_LINE_1)

                #if self.prev == '' :
                        #lcd_string("start receiving", LCD_LINE_2)
                #else :
                        #lcd_string("recv: " + self.prev, LCD_LINE_2)

                #global res
                #res = data.rstrip()
                
                print(data.rstrip())
                global humidity, temperature, light, noise
                temp = data.rstrip().split(',')
                humidity = temp[0]
                temperature = temp[1]
                light = temp[2]
                noise = temp[3]
                #print(humidity+' '+temperature+' '+light+' '+noise)
                lcd_string("H : "+humidity.split('.')[0]+"  T : "+temperature.split('.')[0] , LCD_LINE_1)
                lcd_string("L : "+light+"  N : "+noise , LCD_LINE_2)


#print("Connecting...")

#dev = btle.Peripheral("90:E2:02:9F:DA:75")
#time.sleep(4)

#print("Services...")

#MyDele = MyDelegate()
#dev.withDelegate(MyDele)

#dev.writeCharacteristic(18, "\nLet's do it\n")


def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_init()

  lcd_string("Rasbperry Pi", LCD_LINE_1)
  lcd_string("16x2 LCD Test",LCD_LINE_2)

  while True:

    if dev.waitForNotifications(1.0):
      #print("received data")
      continue

    time.sleep(1)
    
    
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)    
  

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()  
  

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)



def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    

@app.route('/')
def index():
        if dev.waitForNotifications(2.0) :
                #return render_template('index.html', response=MyDele.prev)
                #return render_template('index.html', response=res)
                return render_template('index.html', humidity=humidity, temperature=temperature, light=light, noise=noise)
        else :
                return render_template('index.html')

@app.route('/tovideo')
def tovideo() :
        return render_template('tovideo.html')


@app.route('/<_name>')
def hello(_name):
        return render_template('page.html', name=_name)


print("Connecting...")

dev = btle.Peripheral("90:E2:02:9F:DA:75")
time.sleep(4)

print("Services...")


#MyDele = MyDelegate()
#dev.withDelegate(MyDele)

dev.writeCharacteristic(18, "\nLet's do it\n")


if __name__ == '__main__':

  #th = threading.Thread(target=main)
  #th.start()

  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_init()

  lcd_string("Rasbperry Pi", LCD_LINE_1)
  lcd_string("16x2 LCD Test",LCD_LINE_2)      
  
  dev.withDelegate(MyDelegate())        
  
  try:
    app.run(host='0.0.0.0', port='5000') # thread No.1
    #main() # thread No.2
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
    #th.join(4)
    dev.disconnect()   
