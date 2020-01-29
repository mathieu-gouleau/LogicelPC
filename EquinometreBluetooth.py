# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html


from bluetooth import *
import time
import RPi.GPIO as GPIO
import time
import sys
import math
import numpy as np
from decimal import Decimal
from hx711 import HX711
import Adafruit_CharLCD as LCD
# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)


def cleanAndExit():
    print ("Cleaning...")
    #GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def receiveMessages():
    server_sock=BluetoothSocket( RFCOMM )
  
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
  
    client_sock,address = server_sock.accept()
    print "Accepted connection from " + str(address)
  
    data = client_sock.recv(1024)
    print "received [%s]" % data
  
    client_sock.close()
    server_sock.close()

    return data
   
def capture_poids():    
    try:        

        val = hx.read_long()
        poids=round(abs(val-8334639)/115000.0,3)

        hx.power_down()
        hx.power_up()
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
        GPIO.setwarnings(False)
        
    return poids


def CalculForce(Force):
    port = 1
    sock=BluetoothSocket( RFCOMM )
    sock.connect(('dc:a6:32:49:ff:0e', port))
    
    force0=0
    force1=0
    while (not((int(force1)==int(force0)+1 and Force-0.2<force0 and force0<=Force) or (int(force1)==int(force0)-1 and Force<=force0 and force0<Force+0.2))):
      force1=force0
      force0=capture_poids()
      lcd.clear()
      lcd.message('Force mesuree :\n '+ str(force0))
      print ("force0 : ",force0,", force1 : ",force1)
    print (force0)
    lcd.clear()
    lcd.message('-------OK-------')
    print("Debut envoi")
    sock.send("OK")
    sock.close()

print("DEBUT")
lcd.clear()
lcd.message('PRET A ETRE\nUTILISE')
hx = HX711(5,6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(22.5)

hx.reset()
hx.tare()
while(True):
  Force=float(receiveMessages())
  CalculForce(Force)
