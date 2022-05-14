from Jobs.Base_Player import Player

class Ranged(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across melees

        #JobMod
        self.JobMod = 115

        #trait
        self.Trait = 1.2
    
    def updateCD(self,time):
        pass