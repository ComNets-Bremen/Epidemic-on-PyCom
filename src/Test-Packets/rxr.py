from network import LoRa
import socket
import time
import ubinascii
import common
import utime
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)

def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxr_data():
    while True:
        with common.common_var.lock_all:
            data = s.recv(64)
            if len(data)>0:
                a = data.decode('utf-8').split(':')
                if a[0]=='H':
                    common.common_var.Rxr_hello=data
                    t1 =utime.localtime()
                    current_time=utime.mktime(t1)

                #print(type(common.common_var.difference))
                #x = str(common.common_var.difference)
                #print(type(x))
                    if len(str(common.common_var.difference)) > 0:
                    #print('vvv')
                    #print(type(current_time))
                    #print(type(common.common_var.difference))
                        sync_time = str(int(current_time) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        f=open('/sd/file.txt','a')
                        f.write("{0}   Hello is recieved from a node {1}".format(Time_conversion(sync_time1),a[1]))
                        common.print_str("{0}   Hello is recieved from a node {1}".format(Time_conversion(sync_time1),a[1]))
                        f.close()
                        time.sleep(6)
                        common.common_var.hello_packet=''
                    else:
                        pass
                else:
                    pass
            else:
                pass
            common.common_var.lock_all.release()
