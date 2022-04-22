# FFXIVPPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights)


So far, we have been able to simulate 8 players at the same time (this limit is in theory infinite and we could add as much as we want).
This simply shows that 8 man raids can now be simulated (for DPS only).

Here is an example of running the program with an 8 player team consisting of : DRK, WAR, BLM, RDM, MCH, SAM, WHM, SCH.
All players are assumed to be BiS and we ask it to do the opener we could find on the balance and some more.

The program will output a text of each player's damage and a graph showing the DPS over time.

Note that the outputed DPS will be lower than expected, since some players are not doing damage over the whole duration. This is
simply for example's sake.

![outpout3](https://user-images.githubusercontent.com/62820030/164307505-a1ae397b-98cb-4d0b-8e96-bd32c76b0e70.PNG)


![OUTPUT](https://user-images.githubusercontent.com/62820030/164307120-50d7cda1-2396-4bcb-8862-759649e17d71.PNG)



We so far have implemented the following jobs :

-WAR
-DRK
-BLM
-RDM
-NIN
-SAM
-MCH
-SCH
-WHM

And we plan to add the rest of them in due time.


If you want to help me in developing this program, you contact me through discord Pythagoras#6312
