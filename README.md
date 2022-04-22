# FFXIVPPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights)


So far, we have been able to simulate 8 players at the same time (this limit is in theory infinite and we could add as much as we want).
This simply shows that 8 man raids can now be simulated (for DPS only).

Here is an example of running the program with an 8 player team consisting of : DRK, WAR, BLM, RDM, MCH, SAM, WHM, SCH.
All players are assumed to be BiS and we ask it to do the opener we could find on the balance and some more.

The program will output a text of each player's damage and a graph showing the DPS over time.

It is possible to simulate with as much player as we want. Here is an example with only a Blackmage with SpS BiS executing 4F4 Opener : 

![BLMResut](https://user-images.githubusercontent.com/62820030/164585293-35eeb621-5795-4ffe-94be-812416ab446d.PNG)

![BLMGraph](https://user-images.githubusercontent.com/62820030/164585292-6c0f5485-5ea9-4070-ab6a-abef2c01f35c.PNG)


We have also implemented party buffs like Chain Stratagem, Trick Attack, etc. Here is an example where a Blackmage executing the previous opener (with same gear)
will have its DPS increased by a scholar that uses Chain Stratagem in its opener : 

![BuffedBLMResult](https://user-images.githubusercontent.com/62820030/164585423-68449783-9beb-4714-ae1f-5c52b312862b.PNG)

![BuffedBLMGraph](https://user-images.githubusercontent.com/62820030/164585427-fc76e69b-5fa9-4d21-abc0-5d6e4486dda7.PNG)

It can also be used to directly compare damage within classes. Such as this examples that compares Tank damage in their respective Opener : 
 
![TankResult](https://user-images.githubusercontent.com/62820030/164585479-071c5e2c-7a21-4101-baab-f14d8d777be0.PNG)
![TankGraph](https://user-images.githubusercontent.com/62820030/164585481-c4aa80a7-e400-403b-b00b-3f8217a7539e.PNG)

Here is an example with a full standard team comp. Note that the DPS might be lower than expected for some classes, since not all of these players
will execute abilities for the whole duration of the simulation as it ends when no more player has anything to do.

![FullTeamResult](https://user-images.githubusercontent.com/62820030/164585700-e0aebc62-8ab8-47a9-a114-cb6dd0eb6fb0.PNG)
![FullTeamGraph](https://user-images.githubusercontent.com/62820030/164585712-5b8f5f5d-5f02-4188-b3a5-26c004ebca20.PNG)

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
-PLD
-GNB

And we plan to add the rest of them in due time.


If you want to help me in developing this program, you contact me through discord Pythagoras#6312
