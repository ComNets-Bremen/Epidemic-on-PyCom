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

common.common_var.generated_data_buffer = {}

#script.className.variablename = dosomething
def buffer_generated_data():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                generated_data = common.common_var.string_sent_to_epidemic
                if len(generated_data) >0:
                    splitted_data = generated_data.split(':')
                    #print(splitted_data)
                    raw_data = splitted_data[0]
                    data_index = splitted_data[-1]
                    final_data={data_index:raw_data}
                    if len(common.common_var.generated_data_buffer) < 1:
                        if len(raw_data) >0:
                            common.common_var.generated_data_buffer.update(final_data)
                            #print(common.common_var.generated_data_buffer)
                            #print("len of buffer:{}".format(len(common.common_var.generated_data_buffer)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
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

common.common_var.generated_data_buffer = {}

#script.className.variablename = dosomething
def buffer_generated_data():
    while True:
        with common.common_var.lock_LoRa_ND:
            if len(common.common_var.time_list) >0:
                generated_data = common.common_var.string_sent_to_epidemic
                if len(generated_data) >0:
                    splitted_data = generated_data.split(':')
                    #print(splitted_data)
                    raw_data = splitted_data[0]
                    data_index = splitted_data[-1]
                    final_data={data_index:raw_data}
                    if len(common.common_var.generated_data_buffer) < 1:
                        if len(raw_data) >0:
                            common.common_var.generated_data_buffer.update(final_data)
                            #print(common.common_var.generated_data_buffer)
                            #print("len of buffer:{}".format(len(common.common_var.generated_data_buffer)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                f=open('/sd/file.txt','a')
                f.write('synching in progress')
                f.close()
                time.sleep(6)
            common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
