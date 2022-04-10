
from Fight import *
from Player import BlackMage, Scholar, Redmage
from Spell import *
from Enemy import *


Dummy = Enemy()

#Stat

BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 390, "SS": 2171, "Crit" : 715, "DH" : 1454} 
SCHStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 944, "Crit" : 2277, "DH" : 616}
RDMStat = {"MainStat": 2563, "WD":120, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2348, "DH" : 1340}
MCHStat = {"MainStat": 2572, "WD":120, "Det" : 1615, "Ten" : 400, "SS": 400, "Crit" : 2121, "DH" : 1626}
NINStat = {"MainStat": 2555, "WD":120, "Det" : 1749, "Ten" : 400, "SS": 400, "Crit" : 2283, "DH" : 1330}
DRKStat = {"MainStat": 2521, "WD":120, "Det" : 1680, "Ten" : 539, "SS": 650, "Crit" : 2343, "DH" : 976}
WARStat = {"MainStat": 2521, "WD":120, "Det" : 2130, "Ten" : 1018, "SS": 400, "Crit" : 2240, "DH" : 400}
WHMStat = {"MainStat": 2571, "WD":120, "Det" : 1830, "Ten" : 400, "SS": 489, "Crit" : 2301, "DH" : 940}

Event = Fight([], Dummy)


#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

BLMOpener = [Sharp, WaitAbility(16.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Swift, Despair, Transpo, Para, Xeno, T3, F3, F4, F4, F4, Despair, Xeno, Transpo, Para]
SCHOpener = [WaitAbility(17), Potion, WaitAbility(1), Broil, Biolysis, Aetherflow, Broil, Swift, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
RDMOpener = [WaitAbility(15), Verthunder, Verareo, Swift, Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, Riposte, Fleche, Zwerchhau, Contre, Redoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Verfire, Verthunder,Verfire, Verthunder,Verfire,Fleche]
MCHOpener = [WaitAbility(15), Reassemble, WaitAbility(2.25), Potion, WaitAbility(1.5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, Reassemble, WaitAbility(1), Wildfire, ChainSaw, Automaton,WaitAbility(1), Hypercharge, HeatBlast, Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet, Drill, SplitShot,GaussRound, SlugShot,Ricochet,CleanShot,GaussRound,SplitShot, SlugShot,CleanShot,SlugShot]
NINOpener = [WaitAbility(18.5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, AeolianEdge, WaitAbility(1.75), TrickAttack, Kamaitachi, Hyosho, Raiton, TenChiJin, Meisui, Raiju, Bhavacakra,Raiju, Bhavacakra, SpinningEdge, Raiton, Raiju]
DRKOpener = [WaitAbility(19.25), BloodWeapon, HardSlash, EdgeShadow, Delirium, SyphonStrike, Potion, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, SyphonStrike, Plunge, EdgeShadow, HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike]
WAROpener = [WaitAbility(20), Tomahawk, Infuriate, HeavySwing, Maim, WaitAbility(1),Potion, StormEye, InnerChaos, Upheaval, InnerRelease, PrimalRend, Onslaught, FellCleave,Onslaught, FellCleave,Onslaught, FellCleave, Infuriate, InnerChaos, HeavySwing,Maim, StormPath, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, Upheaval, StormEye]
WHMOpener = [WaitAbility(17), Potion, WaitAbility(1), Glare, Dia, Glare, Glare, Swift, Glare, Assize, PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare, Glare, Glare ]


BLMPlayer = BlackMage(2.5, BLMOpener, [], [AstralFire, UmbralIce], Event, BLMStat)
SCHPlayer = Scholar(2.5, SCHOpener, [], [], Event, SCHStat)
RDMPlayer = Redmage(2.5, RDMOpener, [], [DualCastEffect], Event, RDMStat)
MCHPlayer = Machinist(2.5, MCHOpener, [], [], Event, MCHStat)
NINPlayer = Ninja(2.5, NINOpener, [], [], Event, NINStat)
DRKPlayer = DarkKnight(2.5, DRKOpener, [], [], Event, DRKStat)
WARPlayer = Warrior(2.5, WAROpener, [], [SurgingTempestEffect], Event, WARStat)
WHMPlayer = Whitemage(2.5, WHMOpener, [], [], Event, WHMStat)
#NinjaPlayer = Ninja(2.5, NINAction, [], [AutoEffect, NinjutsuTimerEffect], Event)
Event.PlayerList = [BLMPlayer, SCHPlayer, RDMPlayer, MCHPlayer ,DRKPlayer,WARPlayer,WHMPlayer] #BLMPlayer, SCHPlayer, RDMPlayer, MCHPlayer ,DRKPlayer,WARPlayer
Event.SimulateFight(0.01, 100, 20)  

