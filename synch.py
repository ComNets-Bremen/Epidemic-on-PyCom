import utime
import time
import common
import ubinascii

common.common_var.time_list = []
def sync():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.Rxr_hello)>0:
                if len(common.common_var.time_list) == 0:
                    sync_split = str(common.common_var.Rxr_hello).split(":")
                    if sync_split[1] == '70b3d54995080dc3':    ##70b3d54995080dc3 Mac of source
                        common.common_var.time_list.append(sync_split[-2])
                        t=utime.localtime()
                        current_time=utime.mktime(t)
                        time_recieved = common.common_var.time_list[0]
                        #print(time_recieved)
                        common.common_var.difference = int(current_time - int(time_recieved))
                    else:
                        pass
                        #print('not from standard')
                else:
                    pass
            else:
                pass
                #print('no hello')
            common.common_var.lock_LoRa_ND.release()
            #time.sleep(6)
