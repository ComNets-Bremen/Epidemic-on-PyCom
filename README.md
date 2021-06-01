# Epidemic-on-PyCom
A Python implementation of Epidemic data dissemination in PyCom using LoRa communications. Dissemination of data is by using an extended version of the Epidemic Routing Protocol. There is a slight deviation from traditional Epidemic Routing Protocol by introducing synchronization timeout. 
It was observed from the preliminary tests that, many of the nodes have entered into an anti-entropy but have never synchronized. As a result, if two nodes have not synchronized after few seconds, they will re-enter into an anti-entropy session which is a slight deviation from traditional Epidemic.
This repository, Epidemic-on-LoPy provides a collection of source code that implements the functionality to operate nodes for LoPy4 (PyCom) devices.

This implementation is a 3-layer protocol stack architecture.

•	**Application layer** - This layer generates and receives data.

•	**Forwarding layer** - implements the forwarding protocol for dissemination of data and does the neighbourhood management.

•	**Link layer** - implements direct communications over an available link technology.

Depending on the requirement, each layer can be configured to use different implementations.
