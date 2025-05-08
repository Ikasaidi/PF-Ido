## IKRAM SAIDI

import pigpio
import time

BUTTON = 17  
duree = 2  
pi = pigpio.pi()
pi.set_mode(BUTTON, pigpio.INPUT)


tempDebut = 0

while True:
    if pi.read(BUTTON) == 0:  
        if tempDebut == 0:
            tempDebut = time.time()
    else:  
        if tempDebut != 0:
            dureeBouton = time.time() - tempDebut
            tempDebut = 0
            if dureeBouton >= duree:
                print("long")
            else:
                print("court")
    
