<<<<<<< HEAD
from network import LoRa
import time
import ubinascii
import common
import sys
import utime

# get the MAC address
def send_hello():
    with common.common_var.lock_LoRa_ND:
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        common.common_var.MAC_adress = lora.mac()
        cov_add = ubinascii.hexlify(common.common_var.MAC_adress)
        common.common_var.str_add = cov_add.decode("utf-8")
        common.common_var.lock_LoRa_ND.release()
=======
from network import LoRa
import time
import ubinascii
import common
import sys
import utime

# get the MAC address
def send_hello():
    with common.common_var.lock_LoRa_ND:
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        common.common_var.MAC_adress = lora.mac()
        cov_add = ubinascii.hexlify(common.common_var.MAC_adress)
        common.common_var.str_add = cov_add.decode("utf-8")
        common.common_var.lock_LoRa_ND.release()
>>>>>>> 6ea184f9c42a1a9c99dc5903651d11b7f2bd8234
