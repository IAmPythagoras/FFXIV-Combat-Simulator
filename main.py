from Fight import *
from Spell import *

from Enemy import *
from Spell import Bloodspiller
from Spell import Shadowbringer
from Spell import AbyssalDrain
from Spell import SyphonStrike
from Spell import CarveSpit
from Spell import LivingShadow
from Spell import WaitAbility


Dummy = Enemy()

Action = [F3, Eno, T3, F4, F4]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [EdgeShadow, Shadowbringer, Shadowbringer,]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)

Event.PlayerList = [DRKPlayer]

Event.SimulateFight(0.01, 200)

