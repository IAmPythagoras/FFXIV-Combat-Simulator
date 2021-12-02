
from Fight import *
from Spell import *
from Enemy import *


Dummy = Enemy()

Action = [WaitAbility(3), Sharp, WaitAbility(8.43), B3, T3, B4, F3, Ley, F4, F4, F4, Para, T3, Triple, F4, Swift, F4, Amp, F4, Despair, Mana, F4, Despair, B3, Xeno]
Action2 = [WaitAbility(3), Sharp, WaitAbility(8), F3, T3, F4, Triple, F4, Ley, F4, Swift, F4, Amp, Despair, Mana, F4, Despair, B3, Sharp, T3, Xeno]

#Trial Openers:

Opener1 = [WaitAbility(3), Sharp, WaitAbility(8), B3, T3, B4, F3, Triple, F4, Ley, F4, Sharp, F4, Swift, Para, Triple,F4,Amp, F4,  F4, Despair, F3, Mana, F4, Despair, B3, Xeno, T3, F3, F4, F4, F4,Para, F4, Despair]
#Work for any mana tick
Opener2 = [WaitAbility(3), Sharp, WaitAbility(8), B3, T3, B4, F3, Triple, F4, Ley, F4, Sharp, F4, Swift, Para, Triple,F4, Potion, F4, Amp, F4, Despair, F3, Mana, F4, Despair, B3, Xeno, F3, F4, F4, F4,Para, F4, Despair]
#Opener2 works with Player.ManaTick at 1.5s at start)

Action3 = [Triple, Triple]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [EdgeShadow, Shadowbringer, Shadowbringer,]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.5, Opener2, [], [AstralFire, UmbralIce, EnochianEffect], Event)
Event.PlayerList = [BLMPlayer]
Event.SimulateFight(0.01, 100, 15)  

