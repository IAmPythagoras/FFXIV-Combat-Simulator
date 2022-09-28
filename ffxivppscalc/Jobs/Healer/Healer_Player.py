from Jobs.Base_Player import Player
from Jobs.Base_Player import ManaRegenCheck
from Jobs.ActionEnum import HealerActions

class Healer(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across casters
        self.EffectCDList.append(ManaRegenCheck) #Mana Regen

        #CD
        self.SurecastCD = 0
        self.RescueCD = 0
        self.SwiftcastCD = 0
        self.LucidDreamingCD = 0

        
        #Timer
        self.LucidDreamingTimer = 0

        #JobMod
        self.JobMod = 115

        #Trait
        self.Trait = 1.3 #Magik and mend

        #ActionEnum
        self.ClassAction = HealerActions
    
    def updateCD(self,time):
        if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.RescueCD > 0) : self.RescueCD = max(0,self.RescueCD - time)
        if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

