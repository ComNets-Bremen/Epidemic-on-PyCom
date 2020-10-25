#Neighbour Discovery layer
#
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import ucollections
import _thread
import machine
import os
import time
import utime
import common
import settings
from network import LoRa
import sys
import ubinascii

#initialize ND layer
def initialize():
    pass

#start function threads related to epidemic
def start():
    _thread.start_new_thread(ND_from_Lora_to_Epi,())




def ND_from_Lora_to_Epi():

    while True:

        #wait for some time
        time.sleep(1)

        #lock common queue and pop message from epidemic
        with common.ND_lower_lock:
            try:
                hello_msg = common.ND_lower_q.popleft()
                with common.logging_lock:
                    common.log_activity('popped out the msg in ND' + hello_msg)
                with common.epidemic_side_lock:
                    try:
                        common.epidemic_side_q.append(hello_msg)
                        with common.logging_lock:
                            common.log_activity('appended to Epid q' + hello_msg)
                    except:
                        pass
            except:
                pass
