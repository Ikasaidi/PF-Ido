# IKRAM SAIDI
#yislaine 

from pigpio_dht import DHT11
import time

gpio = 4 # BCM Numbering

sensor = DHT11(gpio)

while True:
    # Read the sensor
    result = sensor.read()
    temp = result["temp_c"]
    hum = result["humidity"]
    # Wait for 2 seconds before the next read
    time.sleep(2)

    print(f"Mesured Temperature: {temp}°C")
    print(f"Mesured Humidity: {hum}%")

