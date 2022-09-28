from Jobs.Base_Player import Player
from ffxivppscalc.Jobs.ActionEnum import MeleeActions

class Melee(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across melees

        #self.TrueNorthStack = 2

        #CD
        self.SecondWindCD = 0 #120 sec
        self.LegSweepCD = 0 #40s 
        self.BloodbathCD = 0 #90s
        self.FeintCD = 0 #90
        self.ArmLengthCD = 0 #120s
        self.TrueNorthCD = 0 #45s, but 2 stacks

        #Stacks
        self.TrueNorthStack = 2
        
        #Trait
        self.Trait = 1

        #ActionEnum
        self.ClassAction = MeleeActions
    
    def updateCD(self,time):
        if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
        if (self.LegSweepCD > 0) : self.LegSweepCD = max(0,self.LegSweepCD - time)
        if (self.BloodbathCD > 0) : self.BloodbathCD = max(0,self.BloodbathCD - time)
        if (self.FeintCD > 0) : self.FeintCD = max(0,self.FeintCD - time)
        if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)
        if (self.TrueNorthCD > 0) : self.TrueNorthCD = max(0,self.TrueNorthCD - time)