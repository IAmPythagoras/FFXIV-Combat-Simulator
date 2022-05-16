# FFXIVPPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights).
Note that this project is still in active development, and some things shown here might be subject to some kind of errors which we will
fix with time. This is simply to show what we have achieved so far, and what we want to do with this program.


So far, we have been able to simulate 8 players at the same time (this limit is in theory infinite and we could add as much as we want).
This simply shows that 8 man raids can now be simulated (only accounts for damage done).

The program will output a text of each player's damage, a graph showing the DPS over time and a graph of each player's DPS distribution.

It is possible to simulate with as much player as we want. Here is an example with only a Blackmage with 2.44 Crit BiS executing 4F4 Opener : 

![BLMAloneDPS](https://user-images.githubusercontent.com/62820030/168635582-5874112c-463e-46f4-b687-f0f9ccb4f3c9.PNG)
![DPSAloneDist](https://user-images.githubusercontent.com/62820030/168635607-28e6f8c4-23ff-4a09-874f-94b110ef9142.PNG)
![BLMAloneResult](https://user-images.githubusercontent.com/62820030/168635621-d68ec25f-dbb0-45e8-85a3-820677ce6145.PNG)


We have also implemented party buffs like Chain Stratagem, Trick Attack, Astrologian Arcanum personnal buff, dance partner, etc.. Here is an example where a Blackmage executing the previous opener (with same gear) will have its DPS increased by being the dance partner of the dancer : 
![BLMDNCGraph](https://user-images.githubusercontent.com/62820030/168635766-89266c1f-dbd8-4122-9f77-1d482a9c2797.PNG)
![BLMDNCDist](https://user-images.githubusercontent.com/62820030/168635777-507ab3c3-bc68-4f30-bd2b-61557c88231a.PNG)
![BLMDNCResult](https://user-images.githubusercontent.com/62820030/168635796-dc75a0c6-03e1-4742-867c-776e90f064ab.PNG)

As you can see, the Blackmage's DPS has been increased. Also, note that the standard deviation of the DPS distribution graph on Blackmage is bigger because
it has received some crit buffs by the Dancer.


It can also be used to directly compare damage within classes. Such as this examples that compares Tank damage in their respective Opener : 
 
![TankResult](https://user-images.githubusercontent.com/62820030/164585479-071c5e2c-7a21-4101-baab-f14d8d777be0.PNG)
![TankGraph](https://user-images.githubusercontent.com/62820030/164585481-c4aa80a7-e400-403b-b00b-3f8217a7539e.PNG)

Here is an example with a full standard team comp. Note that the DPS might be lower than expected for some classes, since not all of these players
will execute abilities for the whole duration of the simulation as it ends when no more player has anything to do.

![fullteamgraph](https://user-images.githubusercontent.com/62820030/168636009-20204bca-010a-4941-ab95-ee6cd653b7c1.PNG)
![fullteamdist](https://user-images.githubusercontent.com/62820030/168636017-2febd13c-843a-498f-b742-ccf754b3211f.PNG)
![Fullteamresult](https://user-images.githubusercontent.com/62820030/168636020-2f9bbfe7-5f2e-4e6a-8a2c-28a314d7dd5d.PNG)


We so far have implemented the following jobs :


Healer:

Whitemage : DONE

Scholar : DONE

Sage : DONE

Astrologian : DONE

Tank:

Warrior : DONE

Gunbreaker : DONE

DarkKnight : DONE

Paladin : DONE

Caster:

Blackmage : DONE

Summoner : DONE

Redmage : DONE

Phys Ranged:

Machinist : DONE

Bard : DONE

Dancer : DONE

Melee:

Ninja : DONE

Samurai : DONE

Reaper : IN WORK

Monk : IN WORK

Dragoon : DONE

UPDATED : May 16th 2022

And we plan to add the rest of them in due time.

We also plan to add Bluemage once we are done with the core program.



# HOW IT WORKS

The big advantage of this program is that instead of computing the average PPS (potency per second) and then using a damage formula to find the
DPS (Damage per second), it simulates the fight like it would happen in real time. That way, buffs are accurately taken into account. It is also able to discernate between oGCD and GCD, and will treat them accordingly (for weaving and stuff). The time-unit used for the program is by default 0.01s/step, but it can be put at whatever smaller (or bigger) number we prefer. It is also able to know when a certain ability cannot be casted, and using that ability anyway will result in an error that stops the simulation. We could in theory disable this checking if we wanted.

Each job in the game is implemented in a relatively similar way. We first create a class JobSpell, which will be an object that will represent a spell/ability/weaponskill of the job. Such an object will have information like casting time, recast time (if GCD), potency, manacost, effect of applying that spell and the requirements of that spell. We then also need to create a class JobPlayer, which will inherit certain traits for its parent class (Healer, Caster, Melee, Ranged or Tank) (This is also the case for spell). This JobPlayer class will contain information like Ability Cooldown, Buff Timer, DOTTimer and other stuff that need to be tracked during the execution of the simulation.

And that's about it, the code will take these two new classes (and object of the JobSpell class) and if everything is done correctly the simulator will be able to run without any issues.

# HOW TO USE

For now the program does not have any UI, so you will have to go change the code itself to make it run what you want. Here is a PDF explaining how to do just that : 
[How_to_use.pdf](https://github.com/IAmPythagoras/FFXIVPPSCalculator/files/8599169/How_to_use.pdf)


# IF YOU WANT TO HELP:)

If you want to help me in developing this program, you can contact me through discord Pythagoras#6312 :). Ill take any help avaible lol
