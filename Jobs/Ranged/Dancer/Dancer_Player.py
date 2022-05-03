from Jobs.Ranged.Ranged_Player import Ranged

class Dancer(Ranged):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #buff
        self.NextDirectCrit = False #True if next 