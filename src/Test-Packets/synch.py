import utime
import time
import common
import ubinascii
import pycom

common.common_var.time_list = []
def sync():
    while True:
        with common.common_var.lock_all:
            if len(common.common_var.Rxr_hello)>0:
                if len(common.common_var.time_list) == 0:
                    sync_split = str(common.common_var.Rxr_hello).split(":")
                    if sync_split[1] == '70b3d54995080dc3':
                        common.common_var.time_list.append(sync_split[-2])
                        t=utime.localtime()
                        current_time=utime.mktime(t)
                        time_recieved = common.common_var.time_list[0]
                        common.common_var.difference = int(current_time - int(time_recieved))
                    #print(type(common.common_var.difference))
                    #print('hiihii')
                        pycom.heartbeat(False)
                        pycom.rgbled(0x7f7f00)
                        time.sleep(4)
                        f=open('/sd/file.txt','a')
                        f.write("Device syncronized")
                        common.print_str("Device syncronized")
                    else:
                        f=open('/sd/file.txt','a')
                        f.write("Device syncronizing in process")
                        common.print_str("Device syncronizing in process")

                else:
                    pass
            else:
                pass
            common.common_var.lock_all.release()
