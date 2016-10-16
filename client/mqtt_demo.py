import paho.mqtt.client as mqtt
import zmq

import json
import time

def zocket_send(**kwargs):
    zcontext = zmq.Context()
    socket = zcontext.socket(zmq.PUSH)
    socket.bind("ipc:///tmp/sock")
    socket.send_json(kwargs)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    accel = json.loads(msg.payload)["fields"]
    accel['timestamp'] = json.loads(msg.payload)["metadata"][0]['server_time']
    print(accel)
    zocket_send(**accel)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('70B3D57ED00011D5',password='J13wtqlBJCc/fYZ27wLZkj2G//5JdN0kK9n4I6+Qumk=')

client.connect("staging.thethingsnetwork.org", port=1883, keepalive=60)
client.subscribe('+/devices/+/up')

client.loop_forever()
