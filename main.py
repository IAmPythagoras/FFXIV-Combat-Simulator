from Fight import *
from Spell import *

from Enemy import *


Dummy = Enemy()

Action = [F3, Eno, T3, F4, F4]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [HardSlash, SaltedEarth]

DRKPlayer = DarkKnight(2.36, DRKAction, [], [DarksideEffect],Event)

Event.PlayerList = [DRKPlayer]

Event.SimulateFight(0.01, 100)

