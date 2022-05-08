from Jobs.Base_Player import Player


class Caster(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across casters

        self.SwiftCastCD = 0
        self.LucidDreamingCD = 0

        #Timer
        self.LucidDreamingTimer = 0

        #jobmod
        self.JobMod = 115
    
    def updateCD(self,time):
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)