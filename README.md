In which we connect a BBC MicroBit's accelerometer to the ThingsNetwork.

Was it worth it? -Judge for yourselves.

1. Put code on the MicroBit.
![microbitcode](/img/microbit_py.png)
-Mount the MicroBit as mass-storage and copy across the .hex file as usual.

2. Pin 0 of the MicroBit goes to pin 7 of the ThingsUno, pin 1 goes to pin 8. Remember to connect the grounds. We'll send the accelerometer data as three comma-separated values.
![spaghetti](/img/thingsmicrobit.jpg)

3. Set up an app at https://staging.thethingsnetwork.org. Add the decoder and validator js functions.

4. Copy the various keys from the app to the ThingsUno sketch as per the tutorial.

5. Upload and run the sketch. The data from the Ardunio serial console should show up in the app.
![itsalive](/img/thing_accel.png)

6. We'll use the Paho MQTT client to grab the data from the app, then shove to a web-socket server made with the AutoBahn library via ZMQ. Run the socket-server first:

`python socket_server.py` 
`python mqtt_demo.py`

7. Open "web_demo.html" in your browser.

8. Profit:
![internet_of_connected_root_shells](/img/net_of_trash.png)




