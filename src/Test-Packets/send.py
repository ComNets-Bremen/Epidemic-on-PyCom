
import _thread
import os
#import Lora
from network import LoRa
import time
import socket
import utime
import ubinascii
import pycom
import common
import synch
import rxr

def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))
#lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def send_hello():
    while True:
        with common.common_var.lock_all:
            lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
            MAC_adress = lora.mac()
            cov_add = ubinascii.hexlify(MAC_adress)
            common.common_var.str_add = cov_add.decode("utf-8")
            common.common_var.hello_packet = "H"+":"+common.common_var.str_add+":"+"N"+":"+"N"+":"+"N"+":"+"N"+":"+"N"
            s.send(common.common_var.hello_packet)
        #print('hh')
            time.sleep(6)
            common.common_var.lock_all.release()
#pycom.heartbeat(False)
#pycom.rgbled(0x7f7f00)
# 0xff00 turn on the RGB LED in green colour
#0x007f00  green
#0x7f7f00 yellow
#0x7f0000 red
