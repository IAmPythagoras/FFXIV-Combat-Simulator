# FFXIVPPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights)


So far, I have been able to simulate 8 players at the same time (this limit is in theory infinite and I could add as much as I want).
This simply shows that 8 man raids can now be simulated (for DPS only).

Here is an example of running the program with an 8 player team consisting of : DRK, WAR, BLM, RDM, MCH, SAM, WHM, SCH.
All players are assumed to be BiS and I ask it to do the opener I could find on the balance and some more.

The program will output a text of each player's damage and a graph showing the DPS over time.

OUTPUT OF PROGRAM
=============================================================================

The Fight finishes at: 50.68
The Total Potency done by player <class 'Jobs.Caster.Blackmage.BlackMage_Player.BlackMage'> was : 9918.0
This same player had a Potency Per Second of: 195.698500394633
This same Player had an average of 330.6 Potency/Spell
This same Player had an average of 489.24625098658254 Potency/GCD
The DPS is : 9722.61070936688
=======================================================
The Total Potency done by player <class 'Jobs.Healer.Scholar.Scholar_Player.Scholar'> was : 6020      
This same player had a Potency Per Second of: 118.78453038674033
This same Player had an average of 207.58620689655172 Potency/Spell
This same Player had an average of 296.96132596685084 Potency/GCD
The DPS is : 3731.127970635973
=======================================================
The Total Potency done by player <class 'Jobs.Caster.Redmage.Redmage_Player.Redmage'> was : 9580      
This same player had a Potency Per Second of: 189.02920284135755
This same Player had an average of 299.375 Potency/Spell
This same Player had an average of 472.5730071033939 Potency/GCD
The DPS is : 7750.053520968826
=======================================================
The Total Potency done by player <class 'Jobs.Ranged.Machinist.Machinist_Player.Machinist'> was : 9720
This same player had a Potency Per Second of: 191.79163378058405
This same Player had an average of 220.9090909090909 Potency/Spell
This same Player had an average of 479.47908445146015 Potency/GCD
The DPS is : 7782.222293973016
=======================================================
The Total Potency done by player <class 'Jobs.Tank.DarkKnight.DarkKnight_Player.DarkKnight'> was : 11840.0
This same player had a Potency Per Second of: 233.62273086029992
This same Player had an average of 358.7878787878788 Potency/Spell
This same Player had an average of 584.0568271507499 Potency/GCD
The DPS is : 7800.349957091797
=======================================================
The Total Potency done by player <class 'Jobs.Tank.Warrior.Warrior_Player.Warrior'> was : 8430
This same player had a Potency Per Second of: 166.33780584056828
This same Player had an average of 281.0 Potency/Spell
This same Player had an average of 415.8445146014207 Potency/GCD
The DPS is : 6733.565094593528
=======================================================
The Total Potency done by player <class 'Jobs.Healer.Whitemage.Whitemage_Player.Whitemage'> was : 6940
This same player had a Potency Per Second of: 136.93764798737175
This same Player had an average of 266.9230769230769 Potency/Spell
This same Player had an average of 342.34411996842937 Potency/GCD
The DPS is : 4263.596363456983
=======================================================
The Total Potency done by player <class 'Jobs.Melee.Samurai.Samurai_Player.Samurai'> was : 10180
This same player had a Potency Per Second of: 200.86819258089977
This same Player had an average of 328.38709677419354 Potency/Spell
This same Player had an average of 502.1704814522494 Potency/GCD
The DPS is : 7932.735715938535
=======================================================
The Enemy has received a total potency of: 72628.0
The Potency Per Second on the Enemy is: 1433.0702446724547
The Enemy's total DPS is 55716.26162602546

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

And I plan to add the rest of them in due time.


If you want to help me in developing this program, you contact me through discord Pythagoras#6312
