from Fight import *
from Spell import *
from Enemy import *


Dummy = Enemy()

Action = [Sharp, T3, T3, T3, T3, T3, T3, T3, T3, T3, T3, T3, T3, WaitAbility(25)]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [Delirium, Bloodspiller, Quietus, Bloodspiller, LivingShadow]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.17, Action, [], [AstralFire, UmbralIce], Event)
Event.PlayerList = [BLMPlayer]
Event.SimulateFight(0.01, 100)

