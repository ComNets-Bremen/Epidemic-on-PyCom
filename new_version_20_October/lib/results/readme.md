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

### Network wide Delivery Ratio
The delivery ratio values range between 25\% - 50\%. The maximum delivery ratio was nearly 50\% for the scenario where three nodes were stationary and three nodes were mobile placed inside a building. This can be because of the reason that in the indoor scenarios, the delivery ratio could go high due to the reflections and multi-path propagation from the many walls present inside the confined space of the building.

![image](https://user-images.githubusercontent.com/63702181/126646293-70a05ab7-ae3e-4e5a-ba30-e012aaba8fbd.png)
### Network wide Delivery Delay
The delivery delay displayed an unpredictable behaviour for all the scenarios and has an average value of 46.86 sec. When the data generation frequency is reduced, the delivery delay has improved in comparison to the 3rd scenario. But it was observed that higher delivery ratios can be achieved for an offset of higher delivery delays.

![image](https://user-images.githubusercontent.com/63702181/126646533-f2a07ae1-16e4-4351-a15f-597b7f444fde.png)
### Network wide packet loss
Losses of packets was observed when looking into the output logs and all the scenarios displayed packet losses. It was also observed that the scenarios with low performance like, the 4th and 5th scenarios where the delivery ratio was low, displayed high packet losses. Therefore it is evident that one major reason for the low delivery ratios was the loss of packets. 

![image](https://user-images.githubusercontent.com/63702181/126647017-bd38beba-feb9-4f84-af5d-e4510640b34d.png)



