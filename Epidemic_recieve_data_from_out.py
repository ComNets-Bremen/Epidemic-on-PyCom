import time
import common
import utime
from machine import SD
import os



sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

#recieved_data_buffer = []

def Time_conversion(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return ("%d:%02d:%02d" % (hour, minutes, seconds))

def rxred_data():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:

                #common.print_str('recieved data: {0} {1}'.format(common.common_var.Rxr_data, common.common_var.sync_time))
                if len(common.common_var.Rxr_data)>0:
                    tt =utime.localtime()
                    current_time1=utime.mktime(tt)
                    sync_time = str(int(current_time1) - int(common.common_var.difference))
                    sync_time1=int(sync_time)
                    f=open('/sd/file.txt','a')
                    f.write("{0}  {1}  Epidemic  msg    Recieved Data from LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                    f.write('/n')
                    f.close()
                    #common.print_str("{0}  {1}  Epedemic  D  received Data {2}".format(Time_conversion(sync_time1),common.common_var.str_add, common.common_var.Rxr_data.decode("utf-8")))
                    #common.print_str('received data {0}-------{1}'.format(common.common_var.Rxr_data.decode("utf-8"), sync_time))
                    rxr_data_split=common.common_var.Rxr_data.decode("utf-8").split(':')
                    if str(rxr_data_split[2]) == common.common_var.str_add:

                        #common.print_str("{0}  {1}  Epedemic  D  received Data {2}".format(Time_conversion(sync_time1),common.common_var.str_add, common.common_var.Rxr_data.decode("utf-8")))
                        relevant_data= str(rxr_data_split[-1])
                        pair=relevant_data.split('-')
                        f=open('/sd/file.txt','a')
                        f.write("{0}  {1}  Epedemic  D..    Recieved Data packet for request {2} from node {3} and packet is {4} ".format(Time_conversion(sync_time1),common.common_var.str_add,pair[-1],rxr_data_split[1],common.common_var.Rxr_data.decode("utf-8")))
                        to_store={pair[-1]:pair[0]}
                        common.common_var.generated_data_buffer.update(to_store)
                        f.write("{0}  {1}  Epidemic  msg    Data saved in buffer".format(Time_conversion(sync_time1),common.common_var.str_add))
                        f.write('/n')
                        f.close()
                        flag1 = str(rxr_data_split[3])
                        flag2 = str(rxr_data_split[4])
                        adress_of_sender = str(rxr_data_split[1])
                        if flag2 == 'L':
                            if flag1 == 'FS':
                                new_flag = 'RF'

                                #common.print_str('starting to send reply as SV--------{}'.format(sync_time))
                                index_list=list(common.common_var.generated_data_buffer.keys())
                                SV_string1='-'.join(index_list)
                                common.common_var.SV_packet1 = "SV"+":"+common.common_var.str_add+":"+adress_of_sender+":"+new_flag+":"+"N"+":"+"N"+":"+SV_string1
                                f=open('/sd/file.txt', 'a')
                                f.write("{0}  {1}  Epidemic  msg    Sending reply SV to LoRa layer".format(Time_conversion(sync_time1),common.common_var.str_add))
                                f.write('/n')
                                f.close()
                            elif flag1=='RF':

                                common.common_var.Served_list.append(adress_of_sender)
                                f=open('/sd/file.txt', 'a')
                                f.wirte("{0}  {1}  Epidemic  msg    End of anti-entropy session with {2}".format(Time_conversion(sync_time1),common.common_var.str_add,adress_of_sender))
                                common.print_str("{0}  {1}  Epidemic  msg    End of anti-entropy session with {2}".format(Time_conversion(sync_time1),common.common_var.str_add,adress_of_sender))
                                f.write('/n')
                                f.close()
                                #$common.print_str('{0} End of anti-entropy session'.format(Time_conversion(sync_time1)))
                                # end of anti entophy and adding to served list
                            else:
                                pass
                        else:
                            pass

                    else:
                        pass

                else:
                    pass
                common.common_var.Rxr_data=''
            else:
                f=open('/sd/file.txt', 'a')
                f.write('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
