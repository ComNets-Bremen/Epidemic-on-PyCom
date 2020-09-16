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

#from teasting1 import msg

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))
#create hello message and send out
def Lora_send_hello():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                hello_packet = "H"+":"+common.common_var.str_add+":"+"N"+":"+"N"+":"+"N"+":"+"N"+":"+"N"
                tt =utime.localtime()
                current_time1=utime.mktime(tt)
                sync_time = str(int(current_time1) - int(common.common_var.difference))
                sync_time1=int(sync_time)
                s.send(hello_packet)
                #common.print_str('sent hello {0}--------{1}'.format(hello_packet, sync_time))
                time.sleep(6)
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.write('\n')
                f.close()
            common.common_var.lock_LoRa_ND.release()

##sending SV recieved from Epidemic_SV_module
def LoRa_send_SV():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.SV_sending_to_LoRa) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    SV is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                    SV_split = common.common_var.SV_sending_to_LoRa.split(":")
                    common.common_var.SV_packet= "SV"+":"+common.common_var.str_add+":"+SV_split[0]+":"+"FS"+":"+"N"+":"+"N"+":"+SV_split[-1]
                    if len(SV_split[-1]) > 0:
                        tt =utime.localtime()
                        current_time1=utime.mktime(tt)
                        sync_time = str(int(current_time1) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        s.send(common.common_var.SV_packet)
                        count_SV_send+=1
                        f=open('/sd/file.txt','a')
                        f.write("{0}  {1}  LORA....  SV.    SV is sent to {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,SV_split[0], common.common_var.SV_packet))
                        f.write('\n')
                        f.close()
                        #common.print_str('sent SV {0}----------{1}'.format(common.common_var.SV_packet, sync_time))
                        #print("length of sending SV packet is: {}".format(len(SV_packet)))

                    else:
                        pass
                        #print("no MAC selected")

                else:
                    pass
                common.common_var.SV_sending_to_LoRa=''
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.close()
            common.common_var.lock_LoRa_ND.release()
            time.sleep(6)

##send data requests according to compared SV
def LoRa_send_request():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                tt =utime.localtime()
                current_time1=utime.mktime(tt)
                sync_time = str(int(current_time1) - int(common.common_var.difference))
                sync_time1=int(sync_time)
                if len(common.common_var.sending) > 0:
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Recieved data requests from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                    y = common.common_var.sending.split(':')
                    wanted= y[-1].split('-')
                    ####
                    if len(wanted) > 0:
                        count = 0
                        for i in wanted:
                            count += 1
                            if count == len(wanted):
                                f=open('/sd/file.txt','a')
                                f.write("{0}  {1}  LORA....  msg    Starting to send last request for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0]))
                                f.write('\n')
                                f.close()
                                #common.print_str('starting to send last request for {0}--------{1}'.format(i,sync_time))
                                request_packet = "R" + ":" + common.common_var.str_add +":"+ y[0] +":"+ y[1] +":"+ "L" +":"+ "N" + ":" + i

                                #print(common.common_var.wanted)
                            else:
                                f=open('/sd/file.txt','a')
                                f.write("{0}  {1}  LORA....  msg    Starting to send request for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0]))
                                f.write('\n')
                                f.close()
                                #common.print_str('starting to send request for {0}--------{1}'.format(i,sync_time))
                                request_packet = "R" + ":" + common.common_var.str_add +":"+ y[0] +":"+ y[1] +":"+ "N" +":"+ "N" + ":" + i

                    ####
                            s.send(request_packet)
                            count_R_send+=1
                            f=open('/sd/file.txt','a')
                            f.write("{0}  {1}  LORA....  R..    Request sent for {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0],request_packet))
                            f.write('\n')
                            f.close()
                            #common.print_str('request sent {0}---------{1}'.format(request_packet, sync_time))
                    else:
                        #print("no data to send")
                        pass

                else:
                    pass
                common.common_var.sending=''
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()



###send data for the requests recieved
def LoRa_send_data():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.requested_data) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    x = common.common_var.requested_data.split(':')
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Recieved relevant data for {2} to node {3} from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1], x[-2]))
                    f.write("{0}  {1}  LORA....  msg    Starting to send data for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1], x[-2]))
                    f.write('\n')
                    f.close()
                    Data_packet= "D" + ":" + common.common_var.str_add +":"+ x[-2] +":"+ x[1] +":"+ x[2] +":"+ "N" + ":" + x[0]+"-"+x[-1]
                    if len(x[0]) > 0:
                        tt =utime.localtime()
                        current_time1=utime.mktime(tt)
                        sync_time = str(int(current_time1) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        s.send(Data_packet)
                        count_D_send+=1
                        f=open('/sd/file.txt','a')
                        f.write("{0}  {1}  LORA....  D..    Data sent for request {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1],x[-2],Data_packet))
                        f.write('\n')
                        f.close()
                        common.print_str("{0}  {1}  LORA....  D..    Data sent for request {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1],x[-2],Data_packet))

                        #common.print_str('data sent {0}------------{1}'.format(Data_packet, sync_time))
                    else:
                        #print("no data to send")
                        pass
                    common.common_var.requested_data=''
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()


###send reply SV
def reply_SV():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.SV_packet1) >0:
                    split=common.common_var.SV_packet1.split(':')
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Reply SV for {2} is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,split[2]))
                    common.print_str("{0}  {1}  LORA....  msg    Reply SV for {2} is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,split[2]))
                    s.send(common.common_var.SV_packet1)
                    count_R_send+=1
                    f.write("{0}  {1}  LORA....  SV.    Reply SV sent to node {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,split[2],common.common_var.SV_packet1))
                    common.print_str("{0}  {1}  LORA....  SV.    Reply SV sent to node {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,split[2],common.common_var.SV_packet1))
                    f.write('\n')
                    f.close()
                    #common.print_str('reply SV sent {0}------------{1}'.format(common.common_var.SV_packet1, sync_time))
                else:
                    #print("no data to send")
                    pass
                common.common_var.SV_packet1=''

            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.total_send=count_D_send+count_R_send+count_SV_send
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

#from teasting1 import msg

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))
#create hello message and send out
def Lora_send_hello():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                hello_packet = "H"+":"+common.common_var.str_add+":"+"N"+":"+"N"+":"+"N"+":"+"N"+":"+"N"
                tt =utime.localtime()
                current_time1=utime.mktime(tt)
                sync_time = str(int(current_time1) - int(common.common_var.difference))
                sync_time1=int(sync_time)
                s.send(hello_packet)
                #common.print_str('sent hello {0}--------{1}'.format(hello_packet, sync_time))
                time.sleep(6)
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.write('\n')
                f.close()
            common.common_var.lock_LoRa_ND.release()

##sending SV recieved from Epidemic_SV_module
def LoRa_send_SV():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.SV_sending_to_LoRa) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    SV is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                    SV_split = common.common_var.SV_sending_to_LoRa.split(":")
                    common.common_var.SV_packet= "SV"+":"+common.common_var.str_add+":"+SV_split[0]+":"+"FS"+":"+"N"+":"+"N"+":"+SV_split[-1]
                    if len(SV_split[-1]) > 0:
                        tt =utime.localtime()
                        current_time1=utime.mktime(tt)
                        sync_time = str(int(current_time1) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        s.send(common.common_var.SV_packet)
                        count_SV_send+=1
                        f=open('/sd/file.txt','a')
                        f.write("{0}  {1}  LORA....  SV.    SV is sent to {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,SV_split[0], common.common_var.SV_packet))
                        f.write('\n')
                        f.close()
                        #common.print_str('sent SV {0}----------{1}'.format(common.common_var.SV_packet, sync_time))
                        #print("length of sending SV packet is: {}".format(len(SV_packet)))

                    else:
                        pass
                        #print("no MAC selected")

                else:
                    pass
                common.common_var.SV_sending_to_LoRa=''
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.close()
            common.common_var.lock_LoRa_ND.release()
            time.sleep(6)

##send data requests according to compared SV
def LoRa_send_request():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                tt =utime.localtime()
                current_time1=utime.mktime(tt)
                sync_time = str(int(current_time1) - int(common.common_var.difference))
                sync_time1=int(sync_time)
                if len(common.common_var.sending) > 0:
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Recieved data requests from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('\n')
                    f.close()
                    y = common.common_var.sending.split(':')
                    wanted= y[-1].split('-')
                    ####
                    if len(wanted) > 0:
                        count = 0
                        for i in wanted:
                            count += 1
                            if count == len(wanted):
                                f=open('/sd/file.txt','a')
                                f.write("{0}  {1}  LORA....  msg    Starting to send last request for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0]))
                                f.write('\n')
                                f.close()
                                #common.print_str('starting to send last request for {0}--------{1}'.format(i,sync_time))
                                request_packet = "R" + ":" + common.common_var.str_add +":"+ y[0] +":"+ y[1] +":"+ "L" +":"+ "N" + ":" + i

                                #print(common.common_var.wanted)
                            else:
                                f=open('/sd/file.txt','a')
                                f.write("{0}  {1}  LORA....  msg    Starting to send request for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0]))
                                f.write('\n')
                                f.close()
                                #common.print_str('starting to send request for {0}--------{1}'.format(i,sync_time))
                                request_packet = "R" + ":" + common.common_var.str_add +":"+ y[0] +":"+ y[1] +":"+ "N" +":"+ "N" + ":" + i

                    ####
                            s.send(request_packet)
                            count_R_send+=1
                            f=open('/sd/file.txt','a')
                            f.write("{0}  {1}  LORA....  R..    Request sent for {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,i,y[0],request_packet))
                            f.write('\n')
                            f.close()
                            #common.print_str('request sent {0}---------{1}'.format(request_packet, sync_time))
                    else:
                        #print("no data to send")
                        pass

                else:
                    pass
                common.common_var.sending=''
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()



###send data for the requests recieved
def LoRa_send_data():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.requested_data) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    x = common.common_var.requested_data.split(':')
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Recieved relevant data for {2} to node {3} from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1], x[-2]))
                    f.write("{0}  {1}  LORA....  msg    Starting to send data for {2} to node {3}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1], x[-2]))
                    f.write('\n')
                    f.close()
                    Data_packet= "D" + ":" + common.common_var.str_add +":"+ x[-2] +":"+ x[1] +":"+ x[2] +":"+ "N" + ":" + x[0]+"-"+x[-1]
                    if len(x[0]) > 0:
                        tt =utime.localtime()
                        current_time1=utime.mktime(tt)
                        sync_time = str(int(current_time1) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        s.send(Data_packet)
                        count_D_send+=1
                        f=open('/sd/file.txt','a')
                        f.write("{0}  {1}  LORA....  D..    Data sent for request {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1],x[-2],Data_packet))
                        f.write('\n')
                        f.close()
                        common.print_str("{0}  {1}  LORA....  D..    Data sent for request {2} to node {3} and packet is {4}".format(Time_conversion(sync_time1),common.common_var.str_add,x[-1],x[-2],Data_packet))

                        #common.print_str('data sent {0}------------{1}'.format(Data_packet, sync_time))
                    else:
                        #print("no data to send")
                        pass
                    common.common_var.requested_data=''
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()


###send reply SV
def reply_SV():
    count_D_send=0
    count_R_send=0
    count_SV_send=0
    #common.common_var.total_send=0
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.SV_packet1) >0:
                    split=common.common_var.SV_packet1.split(':')
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  LORA....  msg    Reply SV for {2} is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,split[2]))
                    common.print_str("{0}  {1}  LORA....  msg    Reply SV for {2} is recieved from Epidemic layer".format(Time_conversion(sync_time1),common.common_var.str_add,split[2]))
                    s.send(common.common_var.SV_packet1)
                    count_R_send+=1
                    f.write("{0}  {1}  LORA....  SV.    Reply SV sent to node {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,split[2],common.common_var.SV_packet1))
                    common.print_str("{0}  {1}  LORA....  SV.    Reply SV sent to node {2} and packet is {3}".format(Time_conversion(sync_time1),common.common_var.str_add,split[2],common.common_var.SV_packet1))
                    f.write('\n')
                    f.close()
                    #common.print_str('reply SV sent {0}------------{1}'.format(common.common_var.SV_packet1, sync_time))
                else:
                    #print("no data to send")
                    pass
                common.common_var.SV_packet1=''

            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.write('\n')
                f.close()
                time.sleep(6)
            common.common_var.total_send=count_D_send+count_R_send+count_SV_send
            common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
