
from Fight import *
from Spell import *
from Enemy import *


Dummy = Enemy()

Action = [WaitAbility(3), Sharp, WaitAbility(8.43), F3, Eno, T3, F4, Triple, F4, Ley, F4, Swift, F4, Amp,Despair, Mana, F4, Despair, B3, Sharp, T3, Xeno]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [Delirium, Bloodspiller, Quietus, Bloodspiller, LivingShadow]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.17, Action, [], [AstralFire, UmbralIce], Event)
Event.PlayerList = [BLMPlayer]
Event.SimulateFight(0.01, 100, 15)

