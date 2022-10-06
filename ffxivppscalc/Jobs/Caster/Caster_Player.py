from Jobs.Base_Player import Player
from Jobs.ActionEnum import CasterActions


class Caster(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across casters
        
        #CD
        self.SwiftcastCD = 0
        self.LucidDreamingCD = 0
        self.SurecastCD = 0
        self.AddleCD = 0

        #Timer
        self.LucidDreamingTimer = 0

        #jobmod
        self.JobMod = 115

        #trait
        self.Trait = 1.3 #magik and mend

        #ActionEnum
        self.ClassAction = CasterActions
    
    def updateCD(self,time):
        if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)
        if (self.AddleCD > 0) : self.AddleCD = max(0,self.AddleCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)