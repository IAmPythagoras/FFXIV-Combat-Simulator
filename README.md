[![Discord](https://img.shields.io/discord/970724799464738977?color=7289da&label=Discord&logo=discord)](https://discord.gg/mZXKUNy2sw)

# Website

Currently working on a website that will use the library, you can vist it here : https://ffxivdpscalc.azurewebsites.net/simulate/
(Note that it is still in development and might be offline sometimes)

# Install

Either download the code above or install it using pip with the following command : 
```
pip install ffxiv-combat-simulator@git+https://github.com/IAmPythagoras/FFXIV-Combat-Simulator.git@main
```
It is recommend to use pip to install it as a library.

*Note that you must have git installed : https://git-scm.com/download/win 

You can find the documentation here : https://iampythagoras.github.io/index.html or join the discord linked above if you have any questions.

If you want to locally use the API. Install the ffxiv-combat-simulator library and also install uvicorn:
```
pip install uvicorn
```
And then run this command:
```
python -m uvicorn ffxivcalc.API.API:app
```
This will locally launch the API.

# Discord bot (Still in testing, but in a working state): 
I made a disbord bot that uses the python library ffxivcalc in order to simulate fights. Feel free to install it using the link below. As of now, the main bot commands are :
```
!Simulate (With a JSON file as a file in the same message)
!Template <filename> <job1> <job2> ... (Generates a template JSON file used to simulate)
!Help (for help)
```
Use this link to install the bot on your server : 
```
https://discord.com/oauth2/authorize?client_id=1071922835011932290&permissions=274878024704&scope=bot
```

# FFXIVDPSCalculator
Environment in which the simulation of FF14 combat (with multiple people) will be possible. 
The goal is to create the environment first and then work on an AI that could optimize rotation (or even entire fights).
Note that this project is still in active development, and some things shown here might be subject to some kind of errors which we will
fix with time. This is simply to show what we have achieved so far, and what we want to do with this program.

So far, we have been able to simulate 8 players (we could do more) at the same time (this limit is in theory infinite and we could add as much as we want).
This simply shows that 8 man raids can now be simulated (only accounts for damage done).

The program will output a text of each player's damage, a graph showing the DPS over time and a graph of each player's DPS distribution. Here I will only show the outputed Graphs, since all the information the program gives can be seen here.

It is possible to simulate with as much player as we want. Here is an example with only a Blackmage with 2.44 Crit BiS executing 4F4 Opener : 

![BLMDist](https://user-images.githubusercontent.com/62820030/171497586-2fbcf405-c377-4684-807b-8ee74468d668.png)
![BLMGraph](https://user-images.githubusercontent.com/62820030/171495792-059caf23-77d7-4060-b600-4ddd17ac5d18.png)

The DPS distribution is the distribution of the expected DPS where the Direct Hit Rate is assumed to be the expected value and where Crit Rate can vary. The different colors show the 68-95-99 empirical rule. For those that do not know what this rule is, it basically implies that 68% of all trials will be within 1 standard deviation away from the mean (the red region), 95% of the trials will be within 2 standard deviation away (blue and red region) and 99.7% (basically 100%) will be within 3 standard deviation away from the mean (green, blue and red region).
Using the DPS over time graph, we can also see rapid increase in DPS, and stagnation of DPS. This can be used to make sure all raid buffs are put in at the optimal time so we maximize the DPS bonus.

We have also implemented party buffs like Chain Stratagem, Trick Attack, Astrologian Arcanum personnal buff, dance partner, etc.. Here is an example where a Blackmage executing the previous opener (with same gear) will have its DPS by a Scholar doing Chain Stratagem: 
![BLMScholarDist](https://user-images.githubusercontent.com/62820030/171496731-fb564013-fd67-48e3-b55a-da05c4b7c74f.PNG)
![BLMScholarGraph](https://user-images.githubusercontent.com/62820030/171496752-b35ea302-e57e-414e-8087-e3114f8cf88f.PNG)

As you can see, the Blackmage's DPS has been increased. Also, note that the standard deviation of the DPS distribution graph on Blackmage is bigger because
it has received some crit buffs by the Scholar.


It can also be used to directly compare damage within classes. Such as this examples that compares Tank damage in their respective Opener : 
 
![tankDist](https://user-images.githubusercontent.com/62820030/171497230-db066d01-3a29-4ba3-bffd-e4cec3217e61.PNG)
![tankGraph](https://user-images.githubusercontent.com/62820030/171497249-ac093177-336b-4a08-8931-e3a2f3d4694d.PNG)


Here is an example with a full standard team comp. Note that the DPS might be lower than expected for some classes, since not all of these players
will execute abilities for the whole duration of the simulation as it ends when no more player has anything to do.

![fullteamDist](https://user-images.githubusercontent.com/62820030/171497282-8acf5732-94e6-49df-952f-af3c4070b356.png)
![FullteamGraph](https://user-images.githubusercontent.com/62820030/171497291-93c94a7b-a9d9-471a-a132-bad3cd2a04e4.png)


# Currently Working On

Adding code to support multiple enemies at the same time and individual targetting of enemy by the players.


# HOW IT WORKS

The big advantage of this program is that instead of computing the average PPS (potency per second) and then using a damage formula to find the
DPS (Damage per second), it simulates the fight like it would happen in real time. That way, buffs are accurately taken into account. It is also able to discernate between oGCD and GCD, and will treat them accordingly (for weaving and stuff).The program can also see if a rotation is illegal, and will stop if it is determined to be a rotation that cannot be done in the game.

The time-unit used for the program is by default 0.01s/step, but it can be put at whatever smaller (or bigger) number we prefer. It is also able to know when a certain ability cannot be casted, and using that ability anyway will result in an error that stops the simulation. We could in theory disable this checking if we wanted.

Each job in the game is implemented in a relatively similar way. We first create a class JobSpell, which will be an object that will represent a spell/ability/weaponskill of the job. Such an object will have information like casting time, recast time (if GCD), potency, manacost, effect of applying that spell and the requirements of that spell. We then also need to create a class JobPlayer, which will inherit certain traits for its parent class (Healer, Caster, Melee, Ranged or Tank) (This is also the case for spell). This JobPlayer class will contain information like Ability Cooldown, Buff Timer, DOTTimer and other stuff that need to be tracked during the execution of the simulation.

And that's about it, the code will take these two new classes (and object of the JobSpell class) and if everything is done correctly the simulator will be able to run without any issues.


# IF YOU WANT TO HELP:)

If you want to help me in developing this program, you can contact me through discord Pythagoras#6312 :). Ill take any available help lol
