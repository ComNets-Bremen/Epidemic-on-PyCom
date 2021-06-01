#Has all the common variables and functions
#
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import _thread
import machine
import os
import ucollections
import utime
import settings

# logging related variables
logging_lock = None

# queues and locks for communication between app and epidemic layers
epidemic_upper_q = None
app_lower_q = None
epidemic_upper_lock = None
app_lower_lock = None

# queues and locks for communication between lora and epidemic layers
lora_upper_q = None
lora_upper_lock = None

# queues and locks for communication between epidemic and neighbour discovery layers
epidemic_side_q = None
epidemic_side_lock = None
ND_side_q = None
ND_side_lock = None

# queues and locks for communication between lora and ND
ND_lower_q = None
ND_lower_lock = None



# node unique ID
node_id = 'None'
dest_id = 'None'
packet_type = 'None'

picked_list = 'None'
served_list = 'None'

# initialize
def initialize():
    global logging_lock
    global epidemic_upper_q
    global app_lower_q
    global epidemic_upper_lock
    global app_lower_lock
    global lora_upper_q
    global lora_upper_lock
    global epidemic_lower_q
    global epidemic_lower_lock
    global epidemic_side_lock
    global epidemic_side_q
    global ND_side_q
    global ND_side_lock
    global ND_lower_q
    global ND_lower_lock


    # setup logging
    logging_lock = _thread.allocate_lock()

    # log start of init
    with logging_lock:
        log_activity('initialization started...')

    # queues and locks for communication between app and fwd layers
    epidemic_upper_q = ucollections.deque((), 50)
    app_lower_q = ucollections.deque((), 50)
    epidemic_upper_lock = _thread.allocate_lock()
    app_lower_lock = _thread.allocate_lock()

    #queues and locks for communication between fwd and lora layer
    lora_upper_q = ucollections.deque((), 50)
    epidemic_lower_q = ucollections.deque((), 50)
    lora_upper_lock = _thread.allocate_lock()
    epidemic_lower_lock = _thread.allocate_lock()

    #queues and locks for communication between epidemic and ND layer
    epidemic_side_q = ucollections.deque((), 50)
    ND_side_q = ucollections.deque((), 50)
    epidemic_side_lock = _thread.allocate_lock()
    ND_side_lock = _thread.allocate_lock()

    #queues and locks for communication between ND and lora layer
    ND_lower_q = ucollections.deque((), 50)
    ND_lower_lock = _thread.allocate_lock()

    # log completion of init
    with logging_lock:
        log_activity('initialization completed')

# log activity given as string
def log_activity(info):
    global node_id
    global dest_id
    global packet_type

    # build log string
    log_str = str(utime.ticks_ms()) + ' ' + node_id +  ' ' + dest_id +' '+ packet_type + ' ' + info

    #print to console
    print(log_str)

# get a random item from a list (by Peter Hinch)
def pick_item(sequence):
    div = 0xffffff // len(sequence)
    return sequence[machine.rng() // div]
