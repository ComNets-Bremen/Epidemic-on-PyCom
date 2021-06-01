#Epidemic layer
#
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import ucollections
import _thread
import machine
import os
import time
import utime
import common
import settings

#Lists in the epidemic layer
cache = None
neigh_list = None
served_list = None
picked_list = None

#locks for updating cache and neighbour list
cache_lock = None
neigh_list_lock = None
served_list_lock = None
picked_list_lock = None

#initialize epidemic layer
def initialize():
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock
    global served_list
    global picked_list

    #initialize Lists
    cache = {}
    neigh_list = {}
    common.served_list = ['Mac1']
    common.picked_list = ['Mac1']

    #initialize locks
    cache_lock = _thread.allocate_lock()
    neigh_list_lock = _thread.allocate_lock()
    served_list_lock = _thread.allocate_lock()
    picked_list_lock = _thread.allocate_lock()

#start function threads related to epidemic
def start():
    _thread.start_new_thread(data_from_app,())
    _thread.start_new_thread(new_neighbour,())
    _thread.start_new_thread(anti_entropy,())
    _thread.start_new_thread(receive_from_lora,())


#get data from application layer
def data_from_app():

    while True:
        time.sleep(1)

        #lock common queue and pop message from application
        with common.epidemic_upper_lock:
            try:
                #get data from queue
                data = common.epidemic_upper_q.popleft()
                #with common.logging_lock:
                #    common.log_activity('epid < appl |  ' + data)

            except:
                #print("error in epidemic")
                data = None

        if not data:
            continue

        #split the data to be saved in the cache
        items = data.split(':')
        #insert the items in the cache (or update the cache)
        #
        #with cache_lock:
        update_cache(items[1],items[0])
        #print('statement after update_cache')


#recieve data from neighbour discovery module
def new_neighbour():
    while True:
        time.sleep(1)

        #lock common queue and pop message from neighbour discovery
        with common.epidemic_side_lock:
            try:
                #get data from queue
                data = common.epidemic_side_q.popleft()
                #with common.logging_lock:
                    #common.log_activity('popped out data in Epidemic' + data)

                #update the new neighbour
                items = data.split('-')

                updating = {items[1]:items[0]}
                #print(updating)

                neigh_list.update(updating)
                #print(neigh_list)

                #with common.logging_lock:
                #    common.log_activity(neigh_list)
                #print('NL in Epide layer is' + neigh_list)
            except:
                pass




#picking a neighbour and start anti-entropy
def anti_entropy():
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock
    #global served_list
    global served_list_lock
    #global picked_list
    global picked_list_lock

    while True:

        #wait for sometime to pick the neighbour (8sec here)
        time.sleep(8)

        if len(cache) == 0:
            continue

        #pick a random neighbour to start the anti-entropy
        with neigh_list_lock:
            #check if there are neighbours in the neigh_list
            if len(neigh_list) == 0:
                continue
            MAC_list = list(neigh_list.keys())
            #print(MAC_list)
            #select random neighbour
            #dest = common.pick_item(list(neigh_list.keys()))
            #print("served_list is ", common.served_list)
            #print("picked_list is ", common.picked_list)
            for i in MAC_list:
                count = 0
                for j in common.served_list:
                    if i == j:
                        break
                    else:
                        for k in common.picked_list:
                            if k == i:
                                break
                            else:
                                count += 1
                                if count == len(common.served_list):#if it did not match until end of served list
                                    my_add = common.node_id
                                    if i in common.picked_list:
                                        break
                                    if i in common.served_list:
                                        break
                                    elif str(my_add) > i:#check if my address is greater than the picked destination address
                                        common.picked_list.append(i)
                                        with common.logging_lock:
                                            common.dest_id = i
                                            common.log_activity('neighbour picked' + i)
                                        with cache_lock:
                                            summary_vector = list(cache.keys())
                                            SV = '-'.join(summary_vector)
                                                #build message
                                                #format => SV:dest:flag1:flag2:info
                                            msg = 'SV' + ':' + i + ':' + 'FS' + ':' + 'N' + ':' + SV
                                                # queue message to send to link layer
                                            with common.logging_lock:
                                                common.dest_id = i
                                                common.packet_type = 'None'
                                                common.log_activity('Starting anti entropy session with' +' '+ i)
                                            with common.lora_upper_lock:
                                                try:
                                                    common.lora_upper_q.append(msg)
                                                    with common.logging_lock:
                                                        common.dest_id = i
                                                        common.packet_type = 'None'
                                                        #common.log_activity('epid > lora |  ' + msg)
                                                        common.log_activity('SV sent to lora' +' '+ msg)
                                                except:
                                                    pass
                                    else:
                                        common.picked_list.append(i)
                                        with common.logging_lock:
                                            common.dest_id = i
                                            common.packet_type = 'None'
                                            common.log_activity('waiting for anti entropy session to begin from the node' + ' '+ i)

                                else:
                                    pass


# receive data from lora layer
def receive_from_lora():

    # operate in an endless loop
    while True:

        # pause for some time
        time.sleep(1)

# lock common queue and pop message from lora layer
        with common.epidemic_lower_lock:
            try:
                # get message from the queue
                msg = common.epidemic_lower_q.popleft()
                #with common.logging_lock:
                #    common.log_activity('RRS   < link  | ' + msg)
            except:
                msg = None

        # message available?
        if not msg:
            continue

        # split into components
        items = msg.split(':')


        # request?
        if items[0] == 'R':
            with common.logging_lock:
                common.dest_id = items[1]
                common.packet_type = 'None'
                common.log_activity('Request recieved from '+ items[1] +' '+ msg)
            receive_request(list(items[1:]))

        #summary_vector?
        elif items[0] == 'SV':
            with common.logging_lock:
                common.dest_id = items[1]
                common.packet_type = 'None'
                common.log_activity('SV recieved from '+ items[1] +' '+ msg)
            receive_SV(list(items[1:]))

        #data?
        elif items[0] == 'D':
            with common.logging_lock:
                common.dest_id = items[1]
                common.packet_type = 'None'
                common.log_activity('Data recieved from '+ items[1] +' '+ msg)
            #print('data is rxed into epidemic' + str(list(items[1:])))
            #print('Epidemic Data D once rxred from lora' + msg)
            receive_Data(list(items[1:]))
        # unknown type of message
        else:
            pass


#when a request is recieved
def receive_request(R_list):
    global cache
    global cache_lock

    try:
        #fetch the required data
        data_required = cache.get(R_list[-1])
        #print('data packet last position' + data_required)
    except:
        with common.logging_lock:
            common.dest_id = R_list[0]
            common.packet_type = 'None'
            log_activity('data does not exist in cache')

    #create the data string to be passes to lora layer
    msg = 'D'+':'+ R_list[0] + ':' + R_list[1] + ':' + R_list[2] + ':' + str(data_required) + '-'+ R_list[-1]
    #print('data packet in epi is generated and it is' + msg)

    #push this item to the lora_upper_q to be sent out
    with common.lora_upper_lock:
        try:
            common.lora_upper_q.append(msg)
            with common.logging_lock:
                common.dest_id = R_list[0]
                common.packet_type = 'None'
                common.log_activity('data packet is sent to lora' + ' '+ msg)
        except:
            pass


#when a SV is recieved
def receive_SV(SV_list):

    global cache
    global cache_lock

    #print("entered rxr SV")

    #list of recieved indexes
    recieved_indexes = SV_list[-1].split('-')

    #get the current summary vector
    summary_vector = list(cache.keys())

        #check if there are any data that is needed
    try:
        indexes = list(set(recieved_indexes) - set(summary_vector))
        #print(indexes)
    except:
        pass

    #is there data that is needed
    if len(indexes) > 0:
        #print("entered rxr SV")
        #see if it is the last request or not
        count = 0
        for i in indexes:
            count += 1

            if count == len(indexes): #this is the last request
                #then setup the flags accordingly
                flag2 = 'L'
            else:
                flag2 = 'N'
            #create the msg to be pushed to the queue
            msg = 'R' + ':' + SV_list[0] + ':' + SV_list[1] + ':' + flag2 + ':' + i
            #push the msg to the lora_upper_q
            with common.lora_upper_lock:
                try:
                    common.lora_upper_q.append(msg)
                    with common.logging_lock:
                        common.packet_type = 'None'
                        common.log_activity('request sent to lora' +' '+ msg)
                except:
                    pass
    else:
        with common.logging_lock:
            common.packet_type = 'None'
            common.log_activity('Data not required')

        if SV_list[-3] ==  'FS':
            flag1 = 'RF'
            reply_SV(flag1,SV_list[0])

        elif SV_list[-3] == 'RF':
            with common.logging_lock:
                common.packet_type = 'None'
                common.log_activity('end of anti entropy with ' + SV_list[0])

        else:
            pass



#when a data is recieved
def receive_Data(Data_list):
    global cache
    global cache_lock
    #global served_list
    global served_list_lock
    #global picked_list
    global picked_list_lock

        #recieved data and store in cache
    items = Data_list[-1].split('-')
    #with cache_lock:
    #print(Data_list)
    update_cache(items[1],items[0])

        #flags of the recieved data packet
    flag1 = Data_list[1]
    flag2 = Data_list[2]
    if flag2 == 'L':
        #if the data is not the last data continue to recieve data

         #if it is the last data check if the sender has started the anti-entropy
        if flag1 == 'FS':
                #set the flag to RF to inform that I am now sending the SV in reply to the sender
            flag1 = 'RF'
            reply_SV(flag1,Data_list[0])

        elif flag1 == 'RF':
            #this means that end of anti entropy and that senders node has to be
            #inserted to served list and deleted from considered list
            #with served_list_lock:
            common.served_list.append(Data_list[0])
            #print(common.picked_list)
            #with picked_list_lock:
            common.picked_list.remove(Data_list[0])
            with common.logging_lock:
                common.dest_id = Data_list[0]
                common.packet_type = 'None'
                common.log_activity('end of anti-entropy with' +' '+ Data_list[0])

        else:
            pass
    else:
        pass

#send reply SV
def reply_SV(flag1,destination):
    global cache
    global cache_lock
    #print('entered reply_SV and sent to' + ' '+ destination)
    #get the current summary vector
    summary_vector = list(cache.keys())
    SV = '-'.join(summary_vector)
    #build message
    #format => SV:dest:flag1:flag2:info
    msg = 'SV' + ':' + destination + ':' + flag1 + ':' + 'N' + ':' + SV
    #print(msg)
    # queue message to send to link layer
    with common.lora_upper_lock:
        try:
            common.lora_upper_q.append(msg)
            with common.logging_lock:
                common.packet_type = 'None'
                common.log_activity('sent reply SV to Lora' + ' '+ msg)
        except:
            pass



#update cache
def update_cache(key,value):
    #print("Update cache")
    global cache
    global neigh_list
    global cache_lock
    global neigh_list_lock

    #lock cache and insert data
    with cache_lock:
        #print("Inside With UC   ")
        #update cache item
        cache[key] = value
        #with common.logging_lock:
            #common.log_activity('Epid > cach |  ' + key + ':' + value)

        #remove an entry if cache has exceeded the limit (10 here)
        if len(cache) > 10:
            rkey = list(cache)[0]
            rvalue = cache[rkey]
            #with common.logging_lock:
                #common.log_activity('Epid ! cach |  ' + rkey+':'+rvalue)
            del cache[rkey]



# update neighbour list
def update_neighbours(MAC,time):
    global neigh_list
    global neigh_list_lock

    with neigh_list_lock:
        # insert neighbours into list
        neigh_list[MAC] = time
        #with common.logging_lock:
            #common.log_activity('Epid > N_li |  ' + key + ':' + value)

        #update neighbour list
        current_time = utime.ticks_ms()
        for key, value in neigh_list.items():
                        if int(current_time) - int(value) > int(300):
                            del neigh_list[key]


#update served list
