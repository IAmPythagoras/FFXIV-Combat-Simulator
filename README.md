[![Discord](https://img.shields.io/discord/970724799464738977?color=7289da&label=Discord&logo=discord)](https://discord.gg/mZXKUNy2sw)

# Website

The website https://ffxivdpscalc.azurewebsites.net allows an easier time for people without coding knowledge to use the simulator.
It uses the most up to date version of FFIXV-Combat-Simulator, but has some limitations to keep computation time low.

# Install

You can install this library using pip (currently has issues) : 

```
pip install ffxivcalc
```

or using git (this would let you download from the dev branch "feature/GeneralDev"): 

```
pip install ffxiv-combat-simulator@git+https://github.com/IAmPythagoras/FFXIV-Combat-Simulator.git@main
```

*Note that you must have git installed : https://git-scm.com/download/win 

You can find the documentation here : https://iampythagoras.github.io/index.html or join the discord linked above if you have any questions.

If you want to locally use the API. Install the ffxiv-combat-simulator library and also install uvicorn :
```
pip install uvicorn
```
And then run this command:
```
python -m uvicorn ffxivcalc.API.API:app
```
This will locally launch the API.

# FFXIV-Combat-Simulator (ffxivcalc)

This Python library lets you simulate combat from the game Final Fantasy XIV. It allows for as many players as possible and will simulate the fight in "real time". It
accurately keeps track of MP, cooldown on abilities, HP, DOTs, raid buffs, personnal buffs, team composition bonus, potions buff, which allows for a dynamic environment that portrays as accurately as possible the real game's environment.

The simulator in its base state will output every player's DPS (Damage Per Second), PPS (Potency Per Second), TP (Total Potency), but it can be customized to output any other metric that could be useful. Furthermore, the simulator is able to output a distribution of the DPS which allows to see the different DPS' percentiles.

Here are some examples of simulations :

BlackMage doing opener and some more :

![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/5bde764b-7e4a-4fa5-9bc5-8668e716f1d9)
![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/8f8fd525-6b17-4582-a490-1da3ae8f0bfb)
![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/40304b27-af47-4181-bdff-d8d02b414cfd)

Here are some of the results the simulator will output : A text result, a graph of DPS over time and a graph of the distribution.

BlackMage, Dancer, Dragoon, Scholar doing opener and some more :

![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/e3e8e2c7-935d-49fa-91c8-745f134e01e1)
![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/f351ec39-c241-4ffb-9722-a6ce7098c5b9)
![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/9972f6aa-e0ef-4a63-a908-2b106ecff814)

Note that the Blackmage's DPS is higher because it received all the buffs.

This library also has a built-in BiS (best in slot) solver. The advantage of using this one is that instead of simply maximizing the DPS of a dummy rotation, the simulator allows the solver to take into account the different raid buffs and when they are in effect. This means that the solver will find a BiS that is dependant on the simulation you want it to optimize damage in.

Learn more about the simulator and how to use it by going to the official documentation website : https://iampythagoras.github.io/index.html

With version 0.8.10 you can now output a "Simulation record" as a pdf file that shows information about the simulation :

![image](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/assets/62820030/88069e5d-8ffa-4783-acc3-b1b02c3ce33e)

This record's goal is to act as a sort of log, but which is more easily understood and contains only the most useful information on the running of the simulation.
You can also export a text only version of this record.
# Rotation BiS Solver 

As of ffxivcalc version 0.8.00, this library now has a built in rotation BiS solver. You can use the ffxivcalclayout.py in order to experiment with it.

You can read this PDF [BiS_Solver_Algorithm_Documentation.pdf](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/files/12580553/BiS_Solver_Algorithm_Documentation.pdf) if you are interested in its
functionning. 

You can read about the experimental results of this solver here : https://docs.google.com/spreadsheets/d/1yVl-F1tHARYIYvz4ZPxIY6MayakYug3OEqpGnpZllqU/edit?usp=sharing

# Validity of simulator

As of version 0.8.30 I have started adding in depth testing of the simulator. The simulator will still have some flaws, but it is currently being checked by around 430 individual tests. More tests
will be added with time.

# Discord bot): 
DISCORD BOT IS CURRENTLY OFFLINE. WILL UPDATE HERE WHEN IT IS AVAILABLE
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

# Currently Working On

Adding code to support multiple enemies at the same time and individual targetting of enemy by the players.


# HOW IT WORKS

The big advantage of this program is that instead of computing the average PPS (potency per second) and then using a damage formula to find the
DPS (Damage per second), it simulates the fight like it would happen in real time. That way, buffs are accurately taken into account. It is also able to discernate between oGCD and GCD, and will treat them accordingly (for weaving and stuff).The program can also see if a rotation is illegal, and will stop if it is determined to be a rotation that cannot be done in the game.

The time-unit used for the program is by default 0.01s/step, but it can be put at whatever smaller (or bigger) number we prefer. It is also able to know when a certain ability cannot be casted, and using that ability anyway will result in an error that stops the simulation. We could in theory disable this checking if we wanted.

Each job in the game is implemented in a relatively similar way. We first create a class JobSpell, which will be an object that will represent a spell/ability/weaponskill of the job. Such an object will have information like casting time, recast time (if GCD), potency, manacost, effect of applying that spell and the requirements of that spell. We then also need to create a class JobPlayer, which will inherit certain traits for its parent class (Healer, Caster, Melee, Ranged or Tank) (This is also the case for spell). This JobPlayer class will contain information like Ability Cooldown, Buff Timer, DOTTimer and other stuff that need to be tracked during the execution of the simulation.

And that's about it, the code will take these two new classes (and object of the JobSpell class) and if everything is done correctly the simulator will be able to run without any issues.

# If you want to help

If you want to help or want to ask questions to me directly, feel free to join the discord linked above:)
