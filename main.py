from Fight import *
from Spell import *
from Enemy import *


Dummy = Enemy()

BLMAction = [T3]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [Unmend, EdgeShadow, BloodWeapon, HardSlash, FloodShadow, SyphonStrike, EdgeShadow, Souleater, LivingShadow, HardSlash]

DRKPlayer = DarkKnight(2.36, DRKAction, [], [DarksideEffect],Event)
BLMPlayer = BlackMage(2.17, BLMAction, [], [AstralFire, UmbralIce], Event)
Event.PlayerList = [BLMPlayer]

Event.SimulateFight(0.01, 50)

