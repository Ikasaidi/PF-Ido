from pigpio_dht import DHT11
import paho.mqtt.client as pmc
import pigpio
import time
import schedule

###### Yislaine
gpio = 4 # BCM Numbering
sensor = DHT11(gpio)
BUTTON = 17  
duree = 2  
pi = pigpio.pi()
pi.set_mode(BUTTON, pigpio.INPUT)
pi.set_mode(20,pigpio.INPUT) # led blanche 


BROKER ="mqttbroker.lan"
PORT= 1883
TOPIC1= "final/yisikam/T"
TOPIC2= "final/yisikam/H"
SubTopic1 = "final/+/T"
SubTopic2 = "final/+/"

######




###### Ikram
def envoyer():
    result = sensor.read()
    if result["valid"] == True:
        
        temp = result["temp_c"]
        hum = result["humidity"]
    
        ## 
        client.publish(TOPIC1,temp)
        print(f"{temp}°C")
        
        client.publish(TOPIC2, hum)
        print(f"{hum}%")
    else :
        print("Mauvaise lecture")

def controle_bouton():
    global tempDebut
    global envoie

    if pi.read(BUTTON) == 0:  
        if tempDebut == 0:
            tempDebut = time.time()
    else:  
        if tempDebut != 0:
            dureeBouton = time.time() - tempDebut
            tempDebut = 0
            if dureeBouton >= duree:
                print("long")
                envoie = not envoie
            else:
                print("court")
                if envoie:
                    envoyer()
###### 

###### Yislaine
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)

def reception_msg(cl,userdata,msg):
    print("Reçu:",msg.payload.decode())
    

client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.on_message = reception_msg

client.connect(BROKER,PORT)

## modifier le sub
client.subscribe(SubTopic1) 
client.subscribe(SubTopic2)

client.loop_start()
######

###### Ikram
tempDebut = 0
envoie = True

# Condition d'envoie de données : à chaque appui sur le bouton et à chaque 30 secondes
schedule.every(30).seconds.do(envoyer)


## Quand envoie est désactivé, il devrait pas fermer le programme mais juste attendre qu'il soit réactivé
try:
    while True:

        if envoie:
            pi.write(20,1) ## Yislaine
            schedule.run_pending()
        else :
            pi.write(20,0) ## Yislaine
            
        
        controle_bouton()
            

except KeyboardInterrupt:
    pi.write(20,0)  ## Yislaine
    client.disconnect()
    client.loop_stop()

######
