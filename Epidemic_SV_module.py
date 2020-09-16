import time
import queue
import common
import utime
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')



common.common_var.Served_list=['MACA', 'MACB']
picked_list=['MAC1']
def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def SV_retrive():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.neighbor_list)>0:
                    if len(common.common_var.generated_data_buffer)>0:
                        tt =utime.localtime()
                        current_time1=utime.mktime(tt)
                        sync_time = str(int(current_time1) - int(common.common_var.difference))
                        sync_time1=int(sync_time)
                        MAC_list = list(common.common_var.neighbor_list.keys()) ###MAC addresses are extracted here
                        #print("MAC list is:{}".format(MAC_list))
                        for i in MAC_list:
                            count = 0
                            for j in common.common_var.Served_list:
                                if i == j:
                                    break
                                else:
                                    for k in picked_list:
                                        if k == i:
                                            break
                                        else:
                                            count += 1
                                            if count == len(common.common_var.Served_list): #if it did not match until end of served list
                                                #picked_Neighbour = i
                                                #print("picked node is: {}".format(picked_Neighbour))
                                                my_add = common.common_var.str_add #picking up my address because adresses has to be compared now

                                                if str(my_add) < str(i):
                                                    if i in picked_list:
                                                        break
                                                    else:
                                                        f=open('/sd/file.txt','a')
                                                        f.write("{0}  {1}  Epedemic  msg    Available Neighbours are {2}".format(Time_conversion(sync_time1),common.common_var.str_add,MAC_list))
                                                        f.write("{0}  {1}  Epedemic  msg    {2} is picked from neighbours".format(Time_conversion(sync_time1),common.common_var.str_add,i))
                                                        f.write('/n')
                                                        f.close()
                                                        common.print_str("{0}  {1}  Epedemic  msg    Available Neighbours are {2}".format(Time_conversion(sync_time1),common.common_var.str_add,MAC_list))
                                                        common.print_str("{0}  {1}  Epedemic  msg    {2} is picked from neighbours".format(Time_conversion(sync_time1),common.common_var.str_add,i))
                                                        #t2 =utime.localtime()
                                                        #current_time2=utime.mktime(t2)
                                                        picked_list.append(i)
                                                        f=open('/sd/file.txt','a')
                                                        f.write("{0}  {1}  Epedemic  msg    Starting anti-entropy session with {2}".format(Time_conversion(sync_time1),common.common_var.str_add,i))
                                                        common.print_str("{0}  {1}  Epedemic  msg    Starting anti-entropy session with {2}".format(Time_conversion(sync_time1),common.common_var.str_add,i))
                                                        f.write('/n')
                                                        f.close()
                                                        #common.print_str('Starting anti-entropy session--------{}'.format(sync_time))
                                                        common.common_var.SV_list=list(common.common_var.generated_data_buffer.keys())
                                                        f=open('/sd/file.txt','a')
                                                        f.write("{0}  {1}  Epedemic  msg    List of Indexes extracted is {2}".format(Time_conversion(sync_time1),common.common_var.str_add,common.common_var.SV_list))
                                                        common.print_str("{0}  {1}  Epedemic  msg    List of Indexes extracted is {2}".format(Time_conversion(sync_time1),common.common_var.str_add,common.common_var.SV_list))
                                                        f.write('/n')
                                                        f.close()
                                                        common.common_var.SV_string='-'.join(common.common_var.SV_list)
                                                        common.common_var.SV_sending_to_LoRa = str(i) +":"+ common.common_var.SV_string
                                                        f=open('/sd/file.txt','a')
                                                        f.write("{0}  {1}  Epedemic  msg    SV is sent to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                                                        common.print_str("{0}  {1}  Epedemic  msg    SV is sent to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                                                        f.write('\n')
                                                        f.close()
                                                else:
                                                    pass
                                            else:
                                                pass
                    else:
                        pass
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
