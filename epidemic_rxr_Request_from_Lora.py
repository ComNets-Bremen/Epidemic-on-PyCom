<<<<<<< HEAD
import time
import common
import utime
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

#Request1 = "R:source:destination:FS:N:N:13"
#Request2 = "R:source:destination:FS:L:N:33"
def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxred_request():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                #common.print_str('recieved request: {}'.format(common.common_var.Rxr_request))
                if len(common.common_var.Rxr_request)>0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt', 'a')
                    f.write("{0}  {1}  Epidemic  msg    Recieved Request from LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('/n')
                    f.close()
                    #common.print_str('Recieved request {0}--------{1}'.format(common.common_var.Rxr_request.decode("utf-8"),sync_time))
                    rxr_rqst_split=common.common_var.Rxr_request.decode("utf-8").split(':')
                    if rxr_rqst_split[2] == common.common_var.str_add:
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epedemic  R..    Recieved Request packet from {2} for {3} and packet is {4} ".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[1],rxr_rqst_split[-1],common.common_var.Rxr_request.decode("utf-8")))
                        f.write('/n')
                        f.close()
                        #rxr_rqst_split = Request1.split(':')
                        needed_data = common.common_var.generated_data_buffer.get(rxr_rqst_split[-1]) #finding the relevant data in the dictionary using the key
                        #common.print_str("{0}  {1}  Epidemic  msg    Retrieved required data for rquest {2} ".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[-1]))
                        flag1 = rxr_rqst_split[3]
                        flag2 = rxr_rqst_split[4]
                        destination_adress = rxr_rqst_split[1]


                        #common.print_str('starting to send data for {0}--------{1}'.format(rxr_rqst_split[-1],sync_time))
                        common.common_var.requested_data= str(needed_data) + ":" + str(flag1) + ":" + str(flag2) + ":" + str(destination_adress)+":"+rxr_rqst_split[-1]
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epidemic  msg    Sending relevant data for request {2} to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[-1]))
                        f.write('/n')
                        f.close()
                    else:
                        pass

                else:
                    pass
                common.common_var.Rxr_request=''
            else:
                f=open('/sd/file.txt', 'a')
                f.write('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
=======
import time
import common
import utime
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

#Request1 = "R:source:destination:FS:N:N:13"
#Request2 = "R:source:destination:FS:L:N:33"
def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxred_request():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                #common.print_str('recieved request: {}'.format(common.common_var.Rxr_request))
                if len(common.common_var.Rxr_request)>0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt', 'a')
                    f.write("{0}  {1}  Epidemic  msg    Recieved Request from LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('/n')
                    f.close()
                    #common.print_str('Recieved request {0}--------{1}'.format(common.common_var.Rxr_request.decode("utf-8"),sync_time))
                    rxr_rqst_split=common.common_var.Rxr_request.decode("utf-8").split(':')
                    if rxr_rqst_split[2] == common.common_var.str_add:
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epedemic  R..    Recieved Request packet from {2} for {3} and packet is {4} ".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[1],rxr_rqst_split[-1],common.common_var.Rxr_request.decode("utf-8")))
                        f.write('/n')
                        f.close()
                        #rxr_rqst_split = Request1.split(':')
                        needed_data = common.common_var.generated_data_buffer.get(rxr_rqst_split[-1]) #finding the relevant data in the dictionary using the key
                        #common.print_str("{0}  {1}  Epidemic  msg    Retrieved required data for rquest {2} ".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[-1]))
                        flag1 = rxr_rqst_split[3]
                        flag2 = rxr_rqst_split[4]
                        destination_adress = rxr_rqst_split[1]


                        #common.print_str('starting to send data for {0}--------{1}'.format(rxr_rqst_split[-1],sync_time))
                        common.common_var.requested_data= str(needed_data) + ":" + str(flag1) + ":" + str(flag2) + ":" + str(destination_adress)+":"+rxr_rqst_split[-1]
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epidemic  msg    Sending relevant data for request {2} to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add,rxr_rqst_split[-1]))
                        f.write('/n')
                        f.close()
                    else:
                        pass

                else:
                    pass
                common.common_var.Rxr_request=''
            else:
                f=open('/sd/file.txt', 'a')
                f.write('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
