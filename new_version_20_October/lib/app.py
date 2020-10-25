#Application layer. Generate and sends data to the
#epidemic layer every 10ms
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import _thread
import ubinascii
import crypto
import utime
import time
import common
import os
import machine
import settings

#Initialize application layer
def initialize():
    pass

#Start the threads in application layer
def start():
    _thread.start_new_thread(generate_data,())
    _thread.start_new_thread(receive_from_epidemic,())

#function thread to generate and send data to epidemic layer
def generate_data():

    #will occur endlessly
    #while True:

        #waits for the amount of time set by the user.here 10ms
        #time.sleep(10)

        #generating the data
    d = ubinascii.hexlify(crypto.getrandbits(4)).decode("utf-8")
    t = str(utime.time())

        #message to send to epidemic
    data = d +':'+ t

        #lock common queue and insert message for epidemic to pop
    with common.epidemic_upper_lock:
        try:
            common.epidemic_upper_q.append(data)
            #with common.logging_lock:
            #    common.log_activity('appl > epid |  ' + data)
        except:
            pass


#function thread to recieve data from epidemic layer
def receive_from_epidemic():

    while True:

        #wait for some time
        time.sleep(1)

        #lock common queue and pop message from epidemic
        with common.app_lower_lock:
            try:
                data = common.app_lower_q.popleft()
                #with common.logging_lock:
                #    common.log_activity('appl < epid |  ' + data)
            except:
                pass
