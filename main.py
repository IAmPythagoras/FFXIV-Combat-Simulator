
from Fight import *
from Player import BlackMage, Scholar, Redmage
from Spell import *
from Enemy import *


Dummy = Enemy()

#Stat

BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 390, "SS": 2171, "Crit" : 715, "DH" : 1454} 
SCHStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 944, "Crit" : 2277, "DH" : 616}
RDMStat = {"MainStat": 2563, "WD":120, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2348, "DH" : 1340}

Event = Fight([], Dummy)


#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

BLMOpener = [Sharp, WaitAbility(16.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Swift, Despair, Transpo, Para, Xeno, T3, F3, F4, F4, F4, Despair, Xeno, Transpo, Para]
SCHOpener = [WaitAbility(17), Potion, WaitAbility(1), Broil, Biolysis, Aetherflow, Broil, Swift, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
RDMOpener = [WaitAbility(15), Verthunder, Verareo, Swift, Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, Riposte, Fleche, Zwerchhau, Contre, Redoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Verfire, Verthunder,Verfire, Verthunder,Verfire,Fleche]


BLMPlayer = BlackMage(2.5, BLMOpener, [], [AstralFire, UmbralIce], Event, BLMStat)
SCHPlayer = Scholar(2.5, SCHOpener, [], [], Event, SCHStat)
RDMPlayer = Redmage(2.5, RDMOpener, [], [DualCastEffect], Event, RDMStat)
#NinjaPlayer = Ninja(2.5, NINAction, [], [AutoEffect, NinjutsuTimerEffect], Event)
Event.PlayerList = [RDMPlayer, BLMPlayer, SCHPlayer]
Event.SimulateFight(0.01, 100, 20)  

