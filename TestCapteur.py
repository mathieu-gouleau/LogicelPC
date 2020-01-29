# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html


import time

import capteur

print("DEBUT")

Force=5
force=0
while (force<Force):
    force=capteur.capture_poids()
    print (force)



print("Fin")
