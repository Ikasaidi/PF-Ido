from pigpio_dht import DHT11
import paho.mqtt.client as pmc
import pigpio
import time

gpio = 4 # BCM Numbering
sensor = DHT11(gpio)
BUTTON = 17  
duree = 2  
pi = pigpio.pi()
pi.set_mode(BUTTON, pigpio.INPUT)

BROKER ="mqttbroker.lan"
PORT= 1883
TOPIC1= "final/yisikam/T"
TOPIC2= "final/yisikam/H"


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
client.subscribe(TOPIC1)
client.subscribe(TOPIC2)

client.loop_start()

try:
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


        result = sensor.read()
        if result["valid"] == True:
            
            temp = result["temp_c"]
            hum = result["humidity"]
        
            #envoyer le donnes
            client.publish(TOPIC1,temp)
            print(f"Mesured Temperature: {temp}°C")
            #envoyer le donnes 
            client.publish(TOPIC2, hum)
            print(f"Mesured Humidity: {hum}%")
        else :
            print("Erreur")
        
        time.sleep(30)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()


