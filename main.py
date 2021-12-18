
from Fight import *
from Spell import *
from Enemy import *
from Spell import EdgeShadow
from Spell import BloodWeapon
from Spell import HardSlash
from Spell import SyphonStrike
from Spell import Souleater
from Spell import LivingShadow
from Spell import SaltDarkness
from Spell import SaltedEarth


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

Opener4 = [Sharp, WaitAbility(11.23), F3, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, F4, T3, Swift, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, Despair]
#323.90 potency/second
Eksu = [Sharp, WaitAbility(11.23), F3, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, F3, F4, F4, F4, F4, F4, T3, Swift, Despair, B3, Para]
#320.870 Potency/second
EksuOpenerMod = [Sharp, WaitAbility(11.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, F3, F4, F4, F4, T3, Swift, Despair, B3, Para]

Opener5 = [Sharp,WaitAbility(12.17), F1, F3, Transpo, Para, Potion, F3, Triple, F4, Ley, F4, Amp, F4, Swift, F4, Triple, F4, Despair, Mana, F4, Despair, Xeno, Transpo, Para, Xeno, F3, F4, F4, F4, F4, Despair ]

Opener6 = [Sharp, WaitAbility(12.17), F3, Sharp, T3, F4, Triple, F4, Potion,F4, Amp, Ley, F4, Triple, Despair, Mana, F4, Sharp, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, F4, T3, Swift, Despair, Transpo, Para, Xeno, F3, F4, F4, F4, F4, Despair]




#Lines Testing
Line1 = [B3Starter, F3, Sharp, F4, F4, F4, F1, F4, Despair, F3, Transpo, Para, Xeno,] #249.67 Potency/sec (24 second)

Line2 = [B3Starter, Thunder3Starter, F3, F4, F4, F4, F4, Despair, Transpo, Para, Xeno] #273.78 potency/sec

Line3 = [F3Starter,B3, T3, Para, F3, F4, F4, F4,F4, Despair] #205.52 potency/sec
#Fast Fire Phase with Para in Ice Phase

Line4 = [F3Starter,B3, T3, F3, F4, F4, F4,F4, Para, Despair]#205.11 potency/sec
#Fast Fire Phase with Para in Fire Phase

Line5 = [F3Starter,B3, T3, Para, B4, F3, F4, F4, F4, Para, F4, F4, F4, Despair] #217.00 potency/sec 
#Line 5 is normal Ice/Fire Rotation with a Thunder 3 reset in Ice Phase

Line6 = [F3Starter, PolyglotStarter,B3, T3,  Xeno, F3, F4, F4, F4, F4, Para, Despair]#219.11 potency/sec, 24 sec
#Fast Fire Phase with Para in Fire Phase and one Xeno in this phase

Line7 = [F3Starter, PolyglotStarter, Thunder3Starter,B3, Para, Xeno, B4, F3, F4, F4, F4, Para, F4, F4, F4, Despair] #239.33 potency/sec 32 sec
#Line 4 is normal Ice/Fire Rotation with a Thunder 3 reset in Ice Phase and Xeno

Line8 = [F3Starter, PolyglotStarter, Thunder3Starter, B3, Para, Xeno, F3, F4, F4, F4, F4, Despair]#240.85 potency/sec, 22.65 sec
#Fast fire phase with no thunder 3 reset (Line 7 with no thunder 3 reset is about 0.5 potency/sec faster)
#This line might be good after opener

Line9 = [F3Starter, PolyglotStarter, Thunder3Starter, Transpo, Para, Xeno, F3, F4, F4, F4, F4, Despair]#248.70 potency/sec, 21.25 sec
#This is a fast Ice phase and fast Fire phase. It assumes Thunder3 is running the whole time.

Line10 = [F3Starter, PolyglotStarter, Thunder3Starter, Transpo, Xeno, F3, F4, F4, F4, F4,Para,Despair]#249.8 potency/sec, 21.27 sec
#Variation of Line9 where we only do 1 gcd in ice phase (not sure why its higher?)

Line11 = [F3Starter, PolyglotStarter, Thunder3Starter,F3ProckStarter,Transpo,WaitAbility(1), Para, Xeno,WaitAbility(1.5), Transpo, F3, F4, F4, F4, Despair]#235.8 potency/sec, 20.22 sec
#This line uses Transpose to enter ice Phase and Tranpose to leave Fire phase and then uses F3Prock to gain F3. This results
#in a loss of time in Fire phase (by either more than or a bit less than 1 gcd), which results in short fire phase (not optimal)

Line12 = [F3Starter, PolyglotStarter, Thunder3Starter,F3ProckStarter,Transpo,WaitAbility(1), Xeno, Amp, Xeno,WaitAbility(1.5), Transpo, F3, F4, F4, F4,Para, F4, Despair]
#249.9 potency/sec, 25.18 sec
#Variation of line11 where we do two Xeno in Ice phase to get 2 gcd and be sure to have full mana and use paradox in Fire phase to allow for one more
#fire 4



Line13 = [F3Starter, Thunder3Starter, F4, F4, F4, F4, Despair]

Line14 = [F3Starter, Thunder3Starter, F4, F4, F4, F4, Para, Despair]







#Testing Fire/ice Rotation

Test1 = [B3,WaitAbility(10), F3, F4, F4, F4, Para, F4, Despair, B3, Sharp, Para, T3]
Test2 = [B3,WaitAbility(10), F3, F4, F4, F4,F4, Despair, B3, Sharp, T3, B4, F3, F4, F4, F4, Para, F4, F4, F4, Despair, B3]
Test3 = [B3, WaitAbility(10), F3, Triple, F4, Swift, F4, F4, F4, Despair, Transpo, Para, Sharp, T3]
Test3 = [B3Starter, F3, Triple, F4, Swift, F4, F4, F4, Despair, Transpo, Para, Sharp, T3, F3, F4, F4, F4, Despair]
Action3 = [Triple, Triple]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [Unmend, EdgeShadow, BloodWeapon, HardSlash, EdgeShadow, SyphonStrike, Souleater, LivingShadow, SaltedEarth]

DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.5, Line13, [], [AstralFire, UmbralIce, EnochianEffect], Event)
Event.PlayerList = [BLMPlayer, DRKPlayer]
Event.SimulateFight(0.01, 100, 0)  

