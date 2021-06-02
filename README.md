# Epidemic-on-PyCom
A Python implementation of Epidemic data dissemination in PyCom using LoRa communications. Dissemination of data is by using an extended version of the Epidemic Routing Protocol. There is a slight deviation from traditional Epidemic Routing Protocol by introducing synchronization timeout.It was observed from the preliminary tests that, many of the nodes have entered into an anti-entropy but have never synchronized. As a result, if two nodes have not synchronized after few seconds, they will re-enter into an anti-entropy session which is a slight deviation from traditional Epidemic.This repository, Epidemic-on-LoPy provides a collection of source code that implements the functionality to operate nodes for LoPy4 (PyCom) devices.

This implementation is a 3-layer protocol stack architecture.

-	**Application layer** - This layer generates and receives data.<br/>
-	**Forwarding layer** - implements the forwarding protocol for dissemination of data and does the neighbourhood management.<br/>
-	**Link layer** - implements direct communications over an available link technology.

Depending on the requirement, each layer can be configured to use different implementations.

## Current Implementation Status
This is work-in-progress. Below is a list of the status of the current implementation.At the moment, the parameters have default values of Spreading Factor(SF) = 7 and power level is 14dBm. The operating frequency was set to 868 MHz. The proposed system allows the radio to receive 128 bytes of data and is programmed into the devices using Atom environment in MicroPython. The proposed sysytem is efficient with delivery ratio of approximately 50%.<br/>
In future, the parameters mentioned above could be changed and try for a delivery ratio of 90 to 95 percentage.<br/>

Implemetation uses LoRa for direct communications between nodes (in .new_version_20_October/lib/lora.py)<br/>
Implemetation uses the Epidemic Routing protocol (in .new_version_20_October/lib/epidemic.py module)<br/>
This has a simple application that generates periodic data (in .new_version_20_October/lib/app.py module)<br/>
##Activity Logging
All activities can be logged to the console and/or the log file. These have to be configured in the new_version_20_October/lib/settings.py file. Below is a sample of a log.
![image](https://user-images.githubusercontent.com/63702181/120488197-d9c59180-c3b6-11eb-9ab2-fe8aed22b4e4.png)
##Firmware Versions
This version of the modules has been tested on the following LoPy4 firmware versions.

- Pycom MicroPython 1.20.2.r1 [v1.11-a5aa0b8] on 2020-09-09; LoPy4 with ESP32
- Pybytes Version: 1.6.0
