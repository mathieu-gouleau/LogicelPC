import RPi.GPIO as GPIO
import time
import sys
import math
import numpy as np
from decimal import Decimal
from hx711 import HX711 

def cleanAndExit():
    print ("Cleaning...")
    #GPIO.cleanup()
    print ("Bye!")
    sys.exit()


    
    
hx = HX711(5,6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(92)

hx.reset()
hx.tare()

#while True:
def capture_poids():    
    try:        
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        #np_arr8_string = hx.get_np_arr8_string()
        ##binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        #val = abs(hx.get_weight(5))*5.88/1000
        val = hx.get_weight(5)
        
        a = abs(((val)/5)*0.001)
        #print (a)
##        if a >= 0 and a < 0.5:
##            print round(0.8*a, 1)
##        elif a >= 0.5 and a < 1.0:
##            print round(0.8*a, 1)
##        elif a >= 1.0 and a < 1.5:
##            print round(0.75*a, 1)
##        elif a >= 1.5 and a < 2.0:
##            print round(0.45*a, 1)
##        elif a >= 2.0 and a < 2.5:
##            print round(0.85*a, 1)
##        elif a >= 2.5 and a < 3.0:
##            print round(0.48*a, 1)
##        
##        elif a >= 4.5:
##            print "capteur detruit"
##       
##        
##        else:
##            print round(a, 1)
        

        hx.power_down()
        hx.power_up()

        #if val>100:
        #    cleanAndExit()

        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
        GPIO.setwarnings(False)
        
    return a

