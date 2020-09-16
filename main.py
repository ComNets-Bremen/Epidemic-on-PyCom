<<<<<<< HEAD

import _thread
import time
import os

import app
import common
import Epidemic_receieve_data
import LoRa_sending_out
import ND_send
import LoRa_recieve_from_out 
import ND_Rxr
import Epidemic_NewNeighbour
import Epidemic_SV_module
import epidemic_rxr_Request_from_Lora
import Epidemic_recieve_SV

import Epidemic_recieve_data_from_out
import test
import Epidemic_UpdateNeighbourList
#import epidemic
import synch
#import lora
from network import LoRa
import time
import socket
import utime
import ubinascii


lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s1 = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s1.setblocking(False)



# define locks
#lock_print = _thread.allocate_lock()
common.common_var.lock_app_epidemic_send = _thread.allocate_lock()
common.common_var.lock_LoRa_ND = _thread.allocate_lock()
common.common_var.lock_print = _thread.allocate_lock()

## define global variables
#buffer_print = ''



#buffer_app_epidemic_receive = ''

# start threads
#_thread.start_new_thread(common.print_str,())_thread.start_new_thread(app.send_data,())
#_thread.start_new_thread(epidemic.printing,())
#print(buffer_app_epidemic_send)
#common.common_var.x = 'def'
#print(common.common_var.buffer_app_epidemic_send)
#app.send_data()
_thread.start_new_thread(app.send_data,())
_thread.start_new_thread(Epidemic_receieve_data.buffer_generated_data,())
_thread.start_new_thread(ND_send.send_hello,())
_thread.start_new_thread(LoRa_sending_out.Lora_send_hello,())
_thread.start_new_thread(ND_Rxr.Send_Epidemic,())
_thread.start_new_thread(LoRa_recieve_from_out.Lora_rxr_data,())
_thread.start_new_thread(Epidemic_NewNeighbour.recieve_new_neighbour,())
_thread.start_new_thread(Epidemic_SV_module.SV_retrive,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_SV,())
_thread.start_new_thread(epidemic_rxr_Request_from_Lora.rxred_request,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_data,())
_thread.start_new_thread(Epidemic_recieve_SV.rxred_SV,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_request,())
_thread.start_new_thread(Epidemic_recieve_data_from_out.rxred_data,())
_thread.start_new_thread(synch.sync,())
_thread.start_new_thread(Epidemic_UpdateNeighbourList.Update_neighbour,())
#_thread.start_new_thread(test.update,())
_thread.start_new_thread(LoRa_sending_out.reply_SV,())

# #using common.common_var.lock_LoRa_ND:
# #print(buffer_app_epidemic_send)
=======

import _thread
import time
import os

import app
import common
import Epidemic_receieve_data
import LoRa_sending_out
import ND_send
import LoRa_recieve_from_out
import ND_Rxr
import Epidemic_NewNeighbour
import Epidemic_SV_module
import epidemic_rxr_Request_from_Lora
import Epidemic_recieve_SV

import Epidemic_recieve_data_from_out
import test
import Epidemic_UpdateNeighbourList
#import epidemic
import synch
#import lora
from network import LoRa
import time
import socket
import utime
import ubinascii


lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s1 = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s1.setblocking(False)



# define locks
#lock_print = _thread.allocate_lock()
common.common_var.lock_app_epidemic_send = _thread.allocate_lock()
common.common_var.lock_LoRa_ND = _thread.allocate_lock()
common.common_var.lock_print = _thread.allocate_lock()

## define global variables
#buffer_print = ''



#buffer_app_epidemic_receive = ''

# start threads
#_thread.start_new_thread(common.print_str,())_thread.start_new_thread(app.send_data,())
#_thread.start_new_thread(epidemic.printing,())
#print(buffer_app_epidemic_send)
#common.common_var.x = 'def'
#print(common.common_var.buffer_app_epidemic_send)
#app.send_data()
_thread.start_new_thread(app.send_data,())
_thread.start_new_thread(Epidemic_receieve_data.buffer_generated_data,())
_thread.start_new_thread(ND_send.send_hello,())
_thread.start_new_thread(LoRa_sending_out.Lora_send_hello,())
_thread.start_new_thread(ND_Rxr.Send_Epidemic,())
_thread.start_new_thread(LoRa_recieve_from_out.Lora_rxr_data,())
_thread.start_new_thread(Epidemic_NewNeighbour.recieve_new_neighbour,())
_thread.start_new_thread(Epidemic_SV_module.SV_retrive,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_SV,())
_thread.start_new_thread(epidemic_rxr_Request_from_Lora.rxred_request,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_data,())
_thread.start_new_thread(Epidemic_recieve_SV.rxred_SV,())
_thread.start_new_thread(LoRa_sending_out.LoRa_send_request,())
_thread.start_new_thread(Epidemic_recieve_data_from_out.rxred_data,())
_thread.start_new_thread(synch.sync,())
_thread.start_new_thread(Epidemic_UpdateNeighbourList.Update_neighbour,())
#_thread.start_new_thread(test.update,())
_thread.start_new_thread(LoRa_sending_out.reply_SV,())

# #using common.common_var.lock_LoRa_ND:
# #print(buffer_app_epidemic_send)
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
