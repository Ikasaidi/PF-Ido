from pigpio_dht import DHT11
import paho.mqtt.client as pmc
import pigpio
import time
import schedule
from flask import Flask, jsonify, request
import socket
from flask_cors import CORS
import threading

########################### Yislaine ############################
gpio = 4 # BCM Numbering
sensor = DHT11(gpio)
BUTTON = 17  
duree = 2 
envoie = True


# GPIO des LED
LED_ROUGE = 16
LED_BLEUE = 12
LED_BLANCHE = 20

pi = pigpio.pi()
pi.set_mode(BUTTON, pigpio.INPUT)
pi.set_mode(LED_BLANCHE,pigpio.INPUT) 
pi.set_mode(LED_ROUGE, pigpio.OUTPUT)
pi.set_mode(LED_BLEUE, pigpio.OUTPUT)


BROKER ="mqttbroker.lan"
PORT= 1883
TOPIC1= "final/yisikam/T"
TOPIC2= "final/yisikam/H"
TOPIC_T = "final/+/T"
TOPIC_H = "final/+/H"

# Données de tous les Pi
donnees_temp = {}
donnees_hum = {}

monPi = socket.gethostname()

##################################################################

################################## Ikram ###################################
app = Flask(__name__)
CORS(app)


@app.route('/etat', methods=['POST'])
def bouton():
    global envoie
    if request.method == "POST":
        json = request.get_json()
        if "etat" in json:
            if json["etat"] == 1:
                envoie = True
            elif json["etat"] == 0:
                envoie = False
            else:
                return jsonify({'Erreur': 'Mauvaise valeur'}),500
        else:
            return jsonify({'Erreur': 'Mauvais attribut'}),500
    else:
        return jsonify({'Erreur': 'Requetes POST seulement'}),500
    return jsonify({'Etat': json["etat"]}),200


@app.route('/donnees', methods=['GET'])
def donnees():
    data = lireCap()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"erreur": "Mauvaise lecture"}), 500



def flash():
    if __name__ == '__main__':
        app.run(host='0.0.0.0',port=3000)

thread_flash = threading.Thread(target=flash, daemon=True)
thread_flash.start()

def offLed():
    # Les fermer au debut et la fin
    pi.write(LED_ROUGE,0)
    pi.write(LED_BLEUE,0)
    pi.write(LED_BLANCHE,0)


def lireCap():
    result = sensor.read()
    if result["valid"] == True:
        return {
            "temp_c": result["temp_c"],
            "humidity": result["humidity"]
        }
    else:
        return None


def envoyer():
    data = lireCap()

    if data :
        client.publish(TOPIC1, data["temp_c"])
        print(f"{data['temp_c']}°C")
        client.publish(TOPIC2, data["humidity"])
        print(f"{data['humidity']}%")
    else:
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
                print("Appuie long")
                envoie = not envoie
            else:
                print("Envoie des données")
                if envoie:
                    envoyer()
##############################################################

########################### Yislaine ############################

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

def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté au broker")
        client.subscribe(TOPIC_T)
        client.subscribe(TOPIC_H) 
    else:
        print("Erreur code %d\n", code)
           

def reception_msg(client, userdata, msg):
    topic = msg.topic  # ex: final/host123/T
    value = msg.payload.decode()

    try:
        val = int(float(value))  # arrondi possible
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

client.connect(BROKER,PORT)
client.loop_start()
#####################################################################

################################## Ikram ############################
tempDebut = 0

schedule.every(30).seconds.do(envoyer)


try:
    while True:

        if envoie:
            pi.write(LED_BLANCHE,1) ## Yislaine
            schedule.run_pending()
        else :
            pi.write(LED_BLANCHE,0) ## Yislaine
            
        
        controle_bouton()
            

except KeyboardInterrupt:
    offLed()
    client.disconnect()
    client.loop_stop()
    print("Arrêt du programme")
     

##########################################################################################
