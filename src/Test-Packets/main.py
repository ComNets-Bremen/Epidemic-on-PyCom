
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
import send


common.common_var.lock_all= _thread.allocate_lock()

_thread.start_new_thread(synch.sync,())
_thread.start_new_thread(rxr.rxr_data,())
_thread.start_new_thread(send.send_hello,())



#pycom.heartbeat(False)
#pycom.rgbled(0x7f7f00)
# 0xff00 turn on the RGB LED in green colour
#0x007f00  green
#0x7f7f00 yellow
#0x7f0000 red
