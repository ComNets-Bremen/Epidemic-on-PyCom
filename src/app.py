import ubinascii
import crypto
import utime
import time
import common
from machine import SD
import os


# sd=SD()
# os.mount(sd,'/sd')
# #os.mkfs('/sd')
# os.listdir('/sd')


#class Application:
def send_data():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                if len(common.common_var.generated_data_buffer) == 0:
                    #generating the data
                    x = crypto.getrandbits(4)
                    hex_data = ubinascii.hexlify(x) # coversion from hexa decimal
                    str_data = hex_data.decode("utf-8") # decoding to string

                    #get the EPOCH time: to create an index for each data that will be crated and finally stored
                    t = str(utime.time())
                    common.common_var.string_sent_to_epidemic = str_data +':'+ t
                    #print(common.common_var.string_sent_to_epidemic)
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
