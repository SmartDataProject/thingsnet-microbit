# Shove accelerometer data through the uart.
from microbit import accelerometer, sleep, uart, pin0, pin1
uart.init(rx=pin0,tx=pin1)

while True:
    uart.write(bytes(','.join([str(v) for v in accelerometer.get_values()]),'ascii')+'\n')
    sleep(20000)