from Fight import *
from Spell import *

from Enemy import *
from Spell import Bloodspiller


Dummy = Enemy()

Action = [F3, Eno, T3, F4, F4]
PrePull = []
Event = Fight([], Dummy)
DRKAction = [Delirium, Bloodspiller, Quietus, Bloodspiller, LivingShadow]

DRKPlayer = DarkKnight(2.43, DRKAction, [], [DarksideEffect], Event)

Event.PlayerList = [DRKPlayer]

Event.SimulateFight(0.01, 100)

