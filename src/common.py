class common_var:
###locks are defined here####
    lock_app_epidemic_send = ''
    lock_ND_epidemic = ''
    lock_LoRa_ND = ''
    lock_print = ''
    lock_time=''


###variables are defined here######
    string_sent_to_epidemic = ''
    generated_data_buffer = ''
    MAC_adress = ''
    str_add=''
    Rxr_hello=''
    Nd_epi=''
    neighbor_list=''
    SV_sending_to_LoRa = ''
    Rxr_request=''
    requested_data=''
    Rxr_SV=''
    SV_list =''
    wanted =''
    Rxr_data=''
    SV_packet=''
    Served_list=''
    nd_t1=''
    #sync_time =''
    SV_string=''
    t=''
    SV_packet1=''
    time_list=''
    difference=''
    sending=''
    total_rxr=''
    total_send=''



def print_str(str):
    with common_var.lock_print:
        print(str)
        common_var.lock_print.release()
