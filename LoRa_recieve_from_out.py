<<<<<<< HEAD
#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

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

def Lora_rxr_data():

    count_SV_rxr=0
    count_R_rxr=0
    count_D_rxr=0
    #common.common_var.total_rxr=0
    while True:
        with common.common_var.lock_LoRa_ND:
            data = s.recv(64)
            #common.print_str(data) #check this
            if len(data)>0: #check this


                a = data.decode('utf-8').split(':')

                if a[0]=='H':
                    common.common_var.Rxr_hello=data



                elif a[0] == 'SV':
                    count_SV_rxr+=1
                    common.common_var.Rxr_SV=data

                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  SV.    SV is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved SV is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                elif a[0]=='R':
                    count_R_rxr+=1
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    common.common_var.Rxr_request=data
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  R..    Request is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved Request is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()

                elif a[0] == 'D':
                    count_D_rxr+=1
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)

                    common.common_var.Rxr_data=data
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  D..    Data is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved Data is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()

                else:
                    pass
                common.common_var.total_rxr=count_SV_rxr+count_R_rxr+count_D_rxr
                common.common_var.lock_LoRa_ND.release()
=======
#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

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

def Lora_rxr_data():

    count_SV_rxr=0
    count_R_rxr=0
    count_D_rxr=0
    #common.common_var.total_rxr=0    
    while True:
        with common.common_var.lock_LoRa_ND:
            data = s.recv(64)
            #common.print_str(data) #check this
            if len(data)>0: #check this


                a = data.decode('utf-8').split(':')

                if a[0]=='H':
                    common.common_var.Rxr_hello=data



                elif a[0] == 'SV':
                    count_SV_rxr+=1
                    common.common_var.Rxr_SV=data

                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  SV.    SV is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved SV is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                elif a[0]=='R':
                    count_R_rxr+=1
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    common.common_var.Rxr_request=data
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  R..    Request is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved Request is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()

                elif a[0] == 'D':
                    count_D_rxr+=1
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)

                    common.common_var.Rxr_data=data
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  D..    Data is recieved from a node".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write("{0}  {1}  LORA....  msg    Recieved Data is sent to Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()

                else:
                    pass
                common.common_var.total_rxr=count_SV_rxr+count_R_rxr+count_D_rxr
                common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
