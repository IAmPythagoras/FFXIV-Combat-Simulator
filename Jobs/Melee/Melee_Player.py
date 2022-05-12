from Jobs.Base_Player import Player

class Melee(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across melees
        
        #Trait
        self.Trait = 1
    
    def updateCD(self,time):
        pass