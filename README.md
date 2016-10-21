In which we connect a BBC MicroBit's accelerometer to the ThingsNetwork.

Was it worth it? -Judge for yourselves.

1. Put code on the MicroBit. [MicroBit](http://microbit.org/)
![microbitcode](/img/microbit_py.png)
-Mount the MicroBit as mass-storage and copy across the .hex file as usual.

2. Pin 0 of the MicroBit goes to pin 7 of the ThingsUno, pin 1 goes to pin 8. Remember to connect the grounds. We'll send the accelerometer data as three comma-separated values.
![spaghetti](/img/thingsmicrobit.jpg) (In the end, we want to turn the three values into signed 16-bit integers, a total of six bytes. We could do this in Python, but if we send ASCII text, it's easier to test that it's shown up at the Arduino un mutiliated.)

3. Set up an app at https://staging.thethingsnetwork.org. Add the decoder and validator js functions.

4. Copy the various keys from the app to the ThingsUno sketch as per the tutorial: https://github.com/TheThingsNetwork/workshops

5. Upload and run the sketch. The data from the Ardunio serial console should show up in the app.
![itsalive](/img/thing_accel.png)

6. We'll use the Paho MQTT client to grab the data from the app. https://github.com/eclipse/paho.mqtt.python We can shove to a web-socket server made with the AutoBahn library via ZMQ [PyZMQ](https://pyzmq.readthedocs.io/en/latest/). Run the socket-server first:

````python socket_server.py 
python mqtt_demo.py```

Now open "web_demo.html" in your browser.

![internet_of_connected_root_shells](/img/net_of_trash.png) (Hooray, we turned an updating list of values on the hub into and updating list of values on our cheap web-page. The things network could provide the MicroBit with a low-cost, low power way of getting to the internet, though. Also, the MicroBit provides a simple way for school-age children to engage with the network.)
   




