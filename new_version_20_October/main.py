#Main
#
#
# @author: Yamani Dalpathadu & Sindhu Priya
# @date: 12-Oct-2020
#

import pycom
import gc
import os
import _thread
import machine
import time
import common
import settings

# basic initializations
time.sleep(2)
gc.enable()

# setup the environment
# load modules of the configured 3-layer protocol stack
app1 = __import__(settings.APP_LAYER)
epidemic1 = __import__(settings.FWD_LAYER)
link1 = __import__(settings.LINK)
Nd1 = __import__(settings.NEIGH_D)


    # initialize common environment
common.initialize()

    # initialize all layers
app1.initialize()
epidemic1.initialize()
link1.initialize()
Nd1.initialize()
    # activate all layers
app1.start()
epidemic1.start()
link1.start()
Nd1.start()
    # wait endlessly while the threads do their work
while True:
        # loop with a pause
        time.sleep(5)
