import utime
import time
import common
import ubinascii
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

def Send_Epidemic():

    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.Rxr_hello)>0:

                    #common.print_str('Recieved hello:{}'.format(common.common_var.sync_time))
                    rxr_lora_split = str(common.common_var.Rxr_hello).split(":")
                    nd_t=utime.localtime()
                    common.common_var.nd_t1=utime.mktime(nd_t)
                    if len(rxr_lora_split)>0:
                        common.common_var.Nd_epi= rxr_lora_split[1]+":"+str(common.common_var.nd_t1)
                        #common.print_str("recieved new hello msg: {}".format(common.common_var.Nd_epi))
                    else:
                        pass
                    common.common_var.Rxr_hello = ''

                else:
                    #common.print_str('no neighbour recieved {}'.format(common.common_var.sync_time))
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                print('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
