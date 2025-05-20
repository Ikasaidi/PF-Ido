#yislaine
import paho.mqtt.client as pmc
import pigpio
import socket

BROKER = "mqttbroker.lan"
PORT = 1883
TOPIC_T = "final/+/T"
TOPIC_H = "final/+/H"

# GPIO des LED
LED_ROUGE = 16
LED_BLEUE = 12

pi = pigpio.pi()
pi.set_mode(LED_ROUGE, pigpio.OUTPUT)
pi.set_mode(LED_BLEUE, pigpio.OUTPUT)

# Données de tous les Pi
donnees_temp = {}
donnees_hum = {}

monPi = socket.gethostname()


def allumerLed():
    
    if donnees_temp:
        maxTempPi = max(donnees_temp, key=donnees_temp.get)
        if maxTempPi == monPi:
            pi.write(LED_ROUGE, 1)
        else:
            pi.write(LED_ROUGE, 0)
    
    if donnees_hum:
        maxHumPi = max(donnees_hum, key=donnees_hum.get)
        if maxHumPi == monPi:
            pi.write(LED_BLEUE, 1)
        else:
            pi.write(LED_BLEUE, 0)

def connexion(client, userdata, flags, rc, properties):
    print("Connecté au broker")
    client.subscribe(TOPIC_T)
    client.subscribe(TOPIC_H)

def reception_msg(client, userdata, msg):
    topic = msg.topic  # ex: final/host123/T
    value = msg.payload.decode()

    try:
        val = int(float(value))  # arrondi 
    except:
        print("Valeur non valide:", value)
        return

    parts = topic.split("/") # On découpe le topic en morceaux séparés par "/" pour pouvoir lire les donnes 
    if len(parts) != 3:  # On vérifie qu'il y a exactement 3 parties
        return

    host = parts[1]# le nom de host de chaque Pi
    typ = parts[2] # t /h

    if typ == "T":
        donnees_temp[host] = val
    elif typ == "H":
        donnees_hum[host] = val

    print(f"{typ} reçue de {host} : {val}")
    allumerLed()

client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.on_message = reception_msg

client.connect(BROKER, PORT)
client.loop_forever()