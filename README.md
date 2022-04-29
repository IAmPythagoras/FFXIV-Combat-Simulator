# FFXIVPPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights)


So far, we have been able to simulate 8 players at the same time (this limit is in theory infinite and we could add as much as we want).
This simply shows that 8 man raids can now be simulated (only accounts for damage done).

The program will output a text of each player's damage and a graph showing the DPS over time.

It is possible to simulate with as much player as we want. Here is an example with only a Blackmage with SpS BiS executing 4F4 Opener : 

![BLMResut](https://user-images.githubusercontent.com/62820030/164585293-35eeb621-5795-4ffe-94be-812416ab446d.PNG)

![BLMGraph](https://user-images.githubusercontent.com/62820030/164585292-6c0f5485-5ea9-4070-ab6a-abef2c01f35c.PNG)


We have also implemented party buffs like Chain Stratagem, Trick Attack and Astrologian Arcanum personnal buff. Here is an example where a Blackmage executing the previous opener (with same gear)
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


Healer:
Whitemage - DONE
Scholar - DONE
Sage - DONE
Astrologian - DONE

Tank:
Warrior - DONE
Gunbreaker - DONE
DarkKnight - DONE
Paladin - DONE

Caster:
Blackmage - DONE
Summoner - DONE
Redmage - DONE

Phys Ranged:
Machinist - DONE
Bard - not done
Dancer - not done

Melee:
Ninja - DONE
Samurai - DONE
Reaper - not done
Monk - not done
Dragoon - not done

And we plan to add the rest of them in due time.



# HOW IT WORKS

The big advantage of this program is that instead of computing the average PPS (potency per second) and then using a damage formula to find the
DPS (Damage per second), it simulates the fight like it would happen in real time. That way, buffs are accurately taken into account. It is also able to discernate between oGCD and GCD, and will treat them accordingly (for weaving and stuff). The time-unit used for the program is by default 0.01s/step, but it can be put at whatever smaller (or bigger) number we prefer. It is also able to know when a certain ability cannot be casted, and using that ability anyway will result in an error that stops the simulation. We could in theory disable this checking if we wanted.

Each job in the game is implemented in a relatively similar way. We first create a class JobSpell, which will be an object that will represent a spell/ability/weaponskill of the job. Such an object will have information like casting time, recast time (if GCD), potency, manacost, effect of applying that spell and the requirements of that spell. We then also need to create a class JobPlayer, which will inherit certain traits for its parent class (Healer, Caster, Melee, Ranged or Tank) (This is also the case for spell). This JobPlayer class will contain information like Ability Cooldown, Buff Timer, DOTTimer and other stuff that need to be tracked during the execution of the simulation.

And that's about it, the code will take these two new classes (and object of the JobSpell class) and if everything is done correctly the simulator will be able to run without any issues.





If you want to help me in developing this program, you can contact me through discord Pythagoras#6312 :). Ill take any help avaible lol
