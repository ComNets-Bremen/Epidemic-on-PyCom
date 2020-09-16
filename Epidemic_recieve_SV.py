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


#SV = "SV:source:destination:FS:N:N:13-33-23"
def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxred_SV():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.Rxr_SV) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt', 'a')
                    f.write("{0}  {1}  Epedemic  msg    Recieved a SV packet from LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('/n')
                    f.close()
                    recieved_sv_split = common.common_var.Rxr_SV.decode("utf-8").split(':') #this is the recieved total SV packet splitted

                    if recieved_sv_split[2] == common.common_var.str_add:
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epedemic  SV.    Recieved SV packet from {2} and packet is {3} ".format(Time_conversion(sync_time1),common.common_var.str_add,recieved_sv_split[1],common.common_var.Rxr_SV.decode("utf-8")))
                        f.write('/n')
                        f.close()
                        Recieved_SV_list = recieved_sv_split[-1].split('-') #list of indexes recieved
                        own_SV = common.common_var.SV_list
                        list_of_wanted_data = list(set(Recieved_SV_list) - set(own_SV))
                        if len(list_of_wanted_data) >0:
                            string1='-'.join(list_of_wanted_data)
                            common.common_var.sending=recieved_sv_split[1]+':'+recieved_sv_split[3]+':'+string1
                            f=open('/sd/file.txt', 'a')
                            f.write("{0}  {1}  Epedemic  msg    Sending data requests to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                            f.write('/n')
                            f.close()

                        #common.print_str('recieved SV: {} {}'.format(list_of_wanted_data, common.common_var.sync_time))
                        else:
                            f=open('/sd/file.txt', 'a')
                            f.write("{0}  {1}  Epedemic  msg    Data not required".format(Time_conversion(sync_time1),common.common_var.str_add))
                            f.write('/n')
                            f.close()
                        #else:
                        #    pass        #print(common.common_var.wanted)
                    else:
                        pass
                        #common.print_str("no data is required {}".format(common.common_var.sync_time))

                else:
                    pass
                common.common_var.Rxr_SV=''
            else:
                f=open('/sd/file.txt', 'a')
                f.write('synching in progress')
                f.write('/n')
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


#SV = "SV:source:destination:FS:N:N:13-33-23"
def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxred_SV():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.Rxr_SV) >0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt', 'a')
                    f.write("{0}  {1}  Epedemic  msg    Recieved a SV packet from LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('/n')
                    f.close()
                    recieved_sv_split = common.common_var.Rxr_SV.decode("utf-8").split(':') #this is the recieved total SV packet splitted

                    if recieved_sv_split[2] == common.common_var.str_add:
                        f=open('/sd/file.txt', 'a')
                        f.write("{0}  {1}  Epedemic  SV.    Recieved SV packet from {2} and packet is {3} ".format(Time_conversion(sync_time1),common.common_var.str_add,recieved_sv_split[1],common.common_var.Rxr_SV.decode("utf-8")))
                        f.write('/n')
                        f.close()
                        Recieved_SV_list = recieved_sv_split[-1].split('-') #list of indexes recieved
                        own_SV = common.common_var.SV_list
                        list_of_wanted_data = list(set(Recieved_SV_list) - set(own_SV))
                        if len(list_of_wanted_data) >0:
                            string1='-'.join(list_of_wanted_data)
                            common.common_var.sending=recieved_sv_split[1]+':'+recieved_sv_split[3]+':'+string1
                            f=open('/sd/file.txt', 'a')
                            f.write("{0}  {1}  Epedemic  msg    Sending data requests to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                            f.write('/n')
                            f.close()

                        #common.print_str('recieved SV: {} {}'.format(list_of_wanted_data, common.common_var.sync_time))
                        else:
                            f=open('/sd/file.txt', 'a')
                            f.write("{0}  {1}  Epedemic  msg    Data not required".format(Time_conversion(sync_time1),common.common_var.str_add))
                            f.write('/n')
                            f.close()
                        #else:
                        #    pass        #print(common.common_var.wanted)
                    else:
                        pass
                        #common.print_str("no data is required {}".format(common.common_var.sync_time))

                else:
                    pass
                common.common_var.Rxr_SV=''
            else:
                f=open('/sd/file.txt', 'a')
                f.write('synching in progress')
                f.write('/n')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
