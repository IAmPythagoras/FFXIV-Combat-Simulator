
from Fight import *
from Spell import *
from Enemy import *
from Spell import Souleater
from Spell import LivingShadow
from Spell import SaltedEarth
from Spell import HardSlash
from Spell import EdgeShadow
from Spell import SyphonStrike
from Spell import Delirium
from Spell import Bloodspiller
from Spell import CarveSpit
from Spell import Shadowbringer
from Spell import SaltDarkness


Dummy = Enemy()

Action = [WaitAbility(3), Sharp, WaitAbility(8.43), B3, T3, B4, F3, Ley, F4, F4, F4, Para, T3, Triple, F4, Swift, F4, Amp, F4, Despair, Mana, F4, Despair, B3, Xeno]
Action2 = [WaitAbility(3), Sharp, WaitAbility(8), F3, T3, F4, Triple, F4, Ley, F4, Swift, F4, Amp, Despair, Mana, F4, Despair, B3, Sharp, T3, Xeno]
Action3 = [Triple, Triple]
PrePull = []
Event = Fight([], Dummy)


DRKOpener1 = [Unmend, TBN, BloodWeapon, HardSlash, EdgeShadow, SyphonStrike, EdgeShadow, Souleater, LivingShadow, SaltedEarth, HardSlash, SyphonStrike, Delirium,  Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, EdgeShadow, Shadowbringer, Bloodspiller, EdgeShadow, Shadowbringer, Souleater
, SaltDarkness]

DRKPlayer = DarkKnight(2.43, DRKOpener1, [], [DarksideEffect], Event)
BLMPlayer = BlackMage(2.5, Action, [], [AstralFire, UmbralIce, EnochianEffect], Event)
Event.PlayerList = [DRKPlayer]
Event.SimulateFight(0.01, 100, 0)  

