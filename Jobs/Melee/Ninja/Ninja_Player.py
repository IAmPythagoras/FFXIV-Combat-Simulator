#########################################
########## NINJA PLAYER #################
#########################################
from Jobs.Melee.Melee_Player import Melee

class Ninja(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.NinkiGauge = 0

        #buff
        self.Suiton = False


        #Ready
        self.RaijuReady = False
        

        #Timer
        self.HutonTimer = 0
        self.MugTimer = 0
        self.TrickAttackTimer = 0
        self.MeisuiTimer = 0

        #CD
        self.DreamWithinADreamCD = 0
        self.MugCD = 0
        self.TrickAttackCD = 0
        self.MeisuiCD = 0



    def AddNinki(self, amount):
        self.NinkiGauge = min(100, self.NinkiGauge + amount)

    def AddHuton(self, amount):
        self.HutonTimer = min(60, self.HutonTimer + amount)