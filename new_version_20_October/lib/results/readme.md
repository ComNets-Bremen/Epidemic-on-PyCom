## Evaluation Scenarios

The performance of this implementation has been tested with multiple
indoor and outdoor scenarios in several stages for finding out the base requirements and for step-wise improvements of the project.

**Preliminary test:** to identify the communication methods and mode of the devices<br/>
**Range test:** to identify the range of the devices both outdoor and indoor<br/>
**Initial evaluation:** to determine the parameter values like cache and queue sizes, amounts of bytes to be sent and received etc.<br/>
The list of different scenarios performed are below:
1. Three mobile nodes three stationary nodes indoor
2. Three mobile nodes three stationary nodes outdoor
3. All nodes stationary indoor
4. All nodes stationary outdoor
5. Three nodes slow-moving outdoor
6. Three nodes slow-moving indoor
7. All nodes stationary and data generation frequency reduced
8. All nodes stationary and cache size increased
9. All nodes stationary and queue size increased
10. All nodes stationary and both queue and cache size increased<br/>

The parameter values used are listed as below: <br/>
Number of nodes: 6,Tx Power: 14 dBm, Node distance: average distance between each device(node) is 2m in indoor scenarios and 5m in outdoor scenarios,Wait time before initialization: 300 sec, Data bytes received: max 128 bytes, Hello packets frequency: every 15 sec, Neighbour flushed out after 45 sec of no response, Re-synchronisation time-out: 40 sec, Data generation frequency: every 40 sec (scenario 1-5) and every 60 sec (scenario 6-10), Cache & Queue size: 50 items each (scenario 1-5) and 100 items each for modified parameter scenarios.

## Graphs and results

Several important metrics were identified to analyze the performance of the implementation. These metrics were calculated based on the results obtained from the performed scenarios.
1. Delivery Ratio
2. Average Delivery Delay
3. Packet Drop
4. Hop Count


