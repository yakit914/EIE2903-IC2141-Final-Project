import paho.mqtt.client as mqtt
from .models import Event
import json

ID= ["B08"] # Sensor ID
mqtt_broker = "ia.ic.polyu.edu.hk" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
mqtt_topic = "iot/sensor-A"
#location = ["W311A","W311B","W311D-Z1","W311D-Z2","W311-H1","W311-H2","W311H3"] 

def mqtt_on_message(client, userdata, msg):
    # Do something
    try:
        d_msg = str(msg.payload.decode("utf-8"))
        iotData = json.loads(d_msg)
        print("Received message on topic %s : %s" % (msg.topic, iotData))
        p = Event(node_id=iotData["node_id"], loc=iotData["loc"], temp=iotData["temp"],hum=iotData["hum"],light = iotData["light"], snd =iotData["snd"]  )
        p.save()
    except Exception as e:
        print("error: ",e)


mqtt_client = mqtt.Client("django-24132859d") # Create a Client Instance
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")
mqtt_client.subscribe(mqtt_topic, mqtt_qos)

mqtt_client.loop_start()
