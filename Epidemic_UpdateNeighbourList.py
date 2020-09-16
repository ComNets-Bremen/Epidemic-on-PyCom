import time
import utime
import common
from machine import SD
import os


sd=SD()
#os.mount(sd,'/sd')
#os.mkfs('/sd')
os.listdir('/sd')

#from Epidemic_NewNeighbour import neighbor_list ####this doesnt work. find a solution
#print(str(neighbor_list))
def Update_neighbour():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                t = utime.localtime()
                t1=utime.mktime(t)
                dict= common.common_var.neighbor_list
                if len(dict) > 0:
                    for key, value in dict.items():
                        if int(t1) - int(value) > int(300):
                            del dict[key]
                            #print(key, 'is the key for the value', value)
                        else:
                            pass
                    else:
                        pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.close()
                time.sleep(10)
            common.common_var.lock_LoRa_ND.release()
