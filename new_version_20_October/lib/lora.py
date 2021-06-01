#Lora(Link) layer
#
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import pycom
import ucollections
import _thread
import machine
import os
import common
import time
import socket
import utime
import network
import socket
import ubinascii
import settings

# current neighbour list
neigh_list = None

# used locks
socket_lock = None
neigh_list_lock = None
LED_blink_lock = None

# neighbour list renewal flag
neigh_list_updated = False

# LoRa interface parameters
lora = None

# socket var
sock = None


# initialize link layer
def initialize():

    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated
    global lora
    global sock

    # init neighbour list
    # self.neigh_list = ucollections.OrderedDict()
    neigh_list = {}

    # init locks
    socket_lock = _thread.allocate_lock()
    neigh_list_lock = _thread.allocate_lock()
    LED_blink_lock = _thread.allocate_lock()

    # neighbour list renewal flag
    neigh_list_updated = False

    # init LoRa interface
    # initialise LoRa in LORA mode
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    # more params can also be given, like frequency, tx power and spreading factor
    lora = network.LoRa(mode=network.LoRa.LORA, region=network.LoRa.EU868)

    # get a unique ID
    # mac() and hexlify() gives 16 byte address, we take only last 4 bytes
    common.node_long_id = ubinascii.hexlify(lora.mac()).upper().decode('utf-8')
    common.node_id = common.node_long_id[12:]
        # setup the send, recv socket
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# start link layer activity threads
def start():

    _thread.start_new_thread(send_msg, ())
    _thread.start_new_thread(recv_msg, ())
    _thread.start_new_thread(send_hello, ())


def send_msg():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated
    global sock

    # endless loop to check in queue and send messages out
    while True:

        # pause for some time
        time.sleep(1)

        # lock common queue and pop message from fwd layer
        with common.lora_upper_lock:
            try:
                msg = common.lora_upper_q.popleft()
                # with common.logging_lock:
                #     common.log_activity('Lora recieved the packet from epidemic')
            except:
                msg = None

        # message to send?
        if not msg:
            continue

        # prepend source (my) address to message
        # format: 3FD1:FFFF:D:3FD1:129
        # format: 3FD1:4DA6:D:3FD1:129

        items = msg.split(':')
        msg1 = items[0] + ':'  + common.node_id + ':' + items[1]+ ':' + items[2]+ ':' + items[3]+ ':' + items[4]
        with common.logging_lock:
            common.dest_id = items[1]
            common.packet_type = items[0] +'  '
            common.log_activity('The packet sent out from Lora is' + ' '+ msg1)

        # send the packet out
        sock.send(msg1)




# receive messages sent by neighbours
def recv_msg():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global neigh_list_updated
    global sock

    # endless loop to receive messages
    while True:

        # pause for some time
        time.sleep(1)

        # get message
        sock.setblocking(True)
        dbytes = sock.recv(64)

        # some bytes received?
        if not (len(dbytes) > 0):
            continue

        # convert to string
        try:
            msg = dbytes.decode("utf-8")
        except:
            continue

        # split to parts
        items = msg.split(':')

        # is valid message? (at least 4 components must be there)
        if len(items[1]) < 4:
            continue

        # log received msg
        #with common.logging_lock:
        #    common.log_activity('link  < LoRa  | ' + msg)

        # HELLO message received?
        if items[0] == 'H':

            # malformed HELLO message
            if len(items) != 6:
                continue


            # lock and insert neighbour
            with neigh_list_lock:
                t = utime.ticks_ms()
                new_neigh = str(t) + '-' + items[1]
            with common.ND_lower_lock:
                try:
                    common.ND_lower_q.append(new_neigh)
                    # with common.logging_lock:
                    #     common.log_activity('neighbour recieved' + items[1])
                except:
                    pass

        # data message received?
        else:

            # malformed data message
            if len(items) != 6:
                continue

            # is it destined to me?
            if not (items[2] == settings.BROADCAST_ADDRESS \
                or items[2] == common.node_id):
                continue
            #print(items)
            msg = items[0] + ':' + items[1] + ':' + items[3] + ':' +items[4] + ':' +items[5]
            #print('msg sent to epi from lora is' + msg)
            # push message to queue with fwd
            with common.epidemic_lower_lock:
                try:
                    common.epidemic_lower_q.append(msg)
                    with common.logging_lock:
                        common.dest_id = items[1]
                        common.packet_type = items[0]+'  '
                        common.log_activity('Packet is recieved in Lora and sending to epidemic' +' '+ msg)
                except:
                    pass


# send HELLO messeages to inform about being in neighbourhood
def send_hello():
    global neigh_list
    global socket_lock
    global neigh_list_lock
    global LED_blink_lock
    global neigh_list_updated
    global sock

    # endless loop that broadcast HELLOs
    while True:

        # pause for the interval
        time.sleep(settings.HELLO_INTERVAL_SEC)

        # build message and log activity
        # format: 3FD1:FFFF:H:3FD1
        msg = 'H' + ':' + common.node_id + ':' + settings.BROADCAST_ADDRESS + ':N'+':N' + ':N'
        #with common.logging_lock:
        #    common.log_activity('link  > LoRa  | ' + msg)

        # send HELLO out
        sock.send(msg)
