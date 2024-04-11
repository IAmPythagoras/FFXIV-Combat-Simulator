[![Discord](https://img.shields.io/discord/970724799464738977?color=7289da&label=Discord&logo=discord)](https://discord.gg/mZXKUNy2sw)

# Desktop app

You can download the desktop app to use the simulator without having to code : https://github.com/IAmPythagoras/ffxivcalcWebApp .

# Install

You can install this library using pip : 

```
pip install ffxivcalc
```

Or can download latest unstable version using : 

```
pip install ffxiv-combat-simulator@git+https://github.com/IAmPythagoras/FFXIV-Combat-Simulator.git@feature/GeneralDev
```

*Note that you must have git installed : https://git-scm.com/download/win 

You can find the documentation here : https://iampythagoras.github.io/index.html or join the discord linked above if you have any questions.

*The unstable version can be removed using
```
pip uninstall ffxiv-combat-simulator
```

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

As of ffxivcalc version 0.8.00, this library now has a built in rotation BiS solver. You can use the ffxivcalclayout.py in order to experiment with it or download the desktop app.

You can read this PDF [BiS_Solver_Algorithm_Documentation.pdf](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/files/12580553/BiS_Solver_Algorithm_Documentation.pdf) if you are interested in its
functionning. 

You can read about the experimental results of this solver here : https://docs.google.com/spreadsheets/d/1yVl-F1tHARYIYvz4ZPxIY6MayakYug3OEqpGnpZllqU/edit?usp=sharing

# Validity of simulator

As of version 0.8.940 I have started adding in depth testing of the simulator. The simulator will still have some flaws, but it is currently being checked by around 800 individual tests. More tests will be added with time.

# Other simulators

Make sure to check out this alternative FFXIV simulator [Amas-FF14-Combat-Sim](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim) or join its [Discord](https://discord.gg/8GjA5uRcDX)

# If you want to help

If you want to help or want to ask questions to me directly, feel free to join the discord linked above:)

# Update log

(Recent only read __init__.py for all update logs)

0.9.940:
    - Oups, forgot to ever implement Army Ethos/Army Muse effect on Bard. This is now fixed.
    - Other bug fixes.

0.8.930:
    - Added Player.getPlayerPrePullTime() which returns the length of the prepull (time before first damage action).
    - Added Fight.getPlayerPrepullLength() which returns the prepull length of all players
    - added Fight.syncPlayerPrePull() which syncs all player's prepull so they all do damage at the same time.
    - Added test suite 'Prepull length test suite' that tests the Player.GetPlayerPrePullTime() function.
    - Removed access to ffxvivcalc.API, ffxivcalc.codeParser and ffxivcalc.Request.FFLogsAPIRequest modules (outdated modules).
    - Other minor bug fix.
