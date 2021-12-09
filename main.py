
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

Opener3 = [Sharp, WaitAbility(11.23), F3, Amp, T3, F4, Triple, F4, Potion, F4, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, T3, Swift, Despair]
#288.74 potency/sec, Would have to look for mana tick (needs mana to be at least 7200)

Opener4 = [Sharp, WaitAbility(11.23), F3, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, F4, T3, Swift, Despair]
#323.90 potency/second
Eksu = [Sharp, WaitAbility(11.23), F3, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, F3, F4, F4, F4, F4, F4, T3, Swift, Despair]
#320.870 Potency/second
EksuOpenerMod = [Sharp, WaitAbility(11.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, F3, F4, F4, F4, T3, Swift, Despair]

#Lines Testing
Line1 = [B3, WaitAbility(10), F3, Sharp, F4, F4, F4, F1, F4, Despair, F3, Transpo, Para, Xeno,] #249.67 Potency/sec (24 second)

Line2 = [B3, WaitAbility(7.5), T3, F3, F4, F4, F4, Despair, Transpo, Para, Xeno,] #273.78 potency/sec

Line3 = [B3, WaitAbility(7.5), T3, F3, F4, F4, F4, Despair, B3, Para, Xeno]

Line4 = [B3, B4, T3, F3, F4, F4, F4, Para, F4, F4, F4, Despair] #324.72 potency

#Testing Fire/ice Rotation

Test1 = [B3,WaitAbility(10), F3, F4, F4, F4, Para, F4, Despair, B3, Sharp, Para, T3]
Test2 = [B3,WaitAbility(10), F3, F4, F4, F4,F4, Despair, B3, Sharp, T3, B4, F3, F4, F4, F4, Para, F4, F4, F4, Despair, B3]
Test3 = [B3, WaitAbility(10), F3, Triple, F4, Swift, F4, F4, F4, Despair, Transpo, Para, Sharp, T3]
Test3 = [B3, WaitAbility(10), F3, Triple, F4, Swift, F4, F4, F4, Despair, Transpo, Para, Sharp, T3, F3, F4, F4, F4, Despair]
Action3 = [Triple, Triple]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [EdgeShadow, Shadowbringer, Shadowbringer,]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.5, Opener4, [], [AstralFire, UmbralIce, EnochianEffect], Event)
Event.PlayerList = [BLMPlayer]
Event.SimulateFight(0.01, 100, 15)  

