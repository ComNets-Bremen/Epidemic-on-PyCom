from network import LoRa
import socket
import time
import ubinascii
import os
from machine import SD


sd=SD()

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


while True:

    data = s.recv(64)
    f=open('/sd/file.txt', 'a')
    f.write('recieved packet:{}'.format(data) + '\n')
    f.close()
    print(data)
    time.sleep(6)
