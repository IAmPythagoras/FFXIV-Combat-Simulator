
from Fight import *
from Player import BlackMage
from Spell import *
from Enemy import *


Dummy = Enemy()

#Stat

BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 390, "SS": 2171, "Crit" : 715, "DH" : 1454} 


Event = Fight([], Dummy)


#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

Opener7 = [Sharp, WaitAbility(16.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Swift, Despair, Transpo, Para, Xeno, T3, F3, F4, F4, F4, Despair, Xeno, Transpo, Para]
Opener6 = [Sharp, WaitAbility(16.5), F3, Sharp, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, F4, T3, Swift, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, Despair]
BLMPlayer2 = BlackMage(2.5, Opener7, [], [AstralFire, UmbralIce], Event, BLMStat)
BLMPlayer = BlackMage(2.5, Opener7, [], [AstralFire, UmbralIce], Event, BLMStat)
#NinjaPlayer = Ninja(2.5, NINAction, [], [AutoEffect, NinjutsuTimerEffect], Event)
Event.PlayerList = [BLMPlayer, BLMPlayer2]
Event.SimulateFight(0.01, 100, 20)  

