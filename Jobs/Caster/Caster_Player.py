from Jobs.Base_Player import Player


class Caster(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across casters

        self.SwiftCastCD = 0
    
    def updateCD(self,time):
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)