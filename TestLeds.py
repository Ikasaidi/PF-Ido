#yislaine
import pigpio
import time

pi = pigpio.pi()
pi.set_mode(20,pigpio.INPUT) # led blanche 
pi.set_mode(16,pigpio.INPUT)#led rougue
pi.set_mode(12,pigpio.INPUT)# led blue


pi.write(12,0)
pi.write(16,0)
pi.write(12,0)

i=0
try:
    while True:
        pi.write(20,1)
        pi.write(16,0)
        pi.write(12,0)
        time.sleep(0.5)
        pi.write(20,0)
        pi.write(16,1)
        pi.write(12,0)
        time.sleep(0.5)
        pi.write(20,0)
        pi.write(16,0)
        pi.write(12,1)
        time.sleep(0.5)
        i+=1
        pi.write(12,0)
        pi.write(16,0)
        pi.write(12,0)
except KeyboardInterrupt:
    pi.write(12,0)
    pi.write(16,0)
    pi.write(12,0)

    
