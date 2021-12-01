from Fight import *
from Spell import *

from Enemy import *
from Spell import Bloodspiller
from Spell import Shadowbringer


Dummy = Enemy()

Action = [F3, Eno, T3, F4, F4]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [HardSlash, EdgeShadow, Shadowbringer, SyphonStrike, Shadowbringer, Souleater, Shadowbringer]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)

Event.PlayerList = [DRKPlayer]

Event.SimulateFight(0.01, 100)

