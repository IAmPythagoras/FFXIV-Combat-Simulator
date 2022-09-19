from Jobs.Base_Player import Player

class Ranged(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across melees
        #CD
        self.LegGrazeCD = 0
        self.SecondWindCD = 0
        self.FootGrazeCD = 0
        self.PelotonCD = 0
        self.HeadGrazeCD = 0
        self.ArmLengthCD = 0

        #JobMod
        self.JobMod = 115

        #trait
        self.Trait = 1.2 #Common to all phys ranged
    
    def updateCD(self,time):
        if (self.LegGrazeCD > 0) : self.LegGrazeCD = max(0,self.LegGrazeCD - time)
        if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
        if (self.FootGrazeCD > 0) : self.FootGrazeCD = max(0,self.FootGrazeCD - time)
        if (self.PelotonCD > 0) : self.PelotonCD = max(0,self.PelotonCD - time)
        if (self.HeadGrazeCD > 0) : self.HeadGrazeCD = max(0,self.HeadGrazeCD - time)
        if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)