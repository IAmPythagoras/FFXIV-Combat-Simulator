#########################################
########## WARRIOR PLAYER ###############
#########################################

from Jobs.Base_Player import Player

class Warrior(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buffs
        self.SurgingTempest = False #If surging tempest is on, set to true

        #Gauge
        self.BeastGauge = 0

        #Stack
        self.InnerReleaseStack = 0
        self.NoBeastCostStack = 0
        self.OnslaughtStack = 3
        self.InfuriateStack = 2

        #Timer
        self.SurgingTempestTimer = 0
        self.PrimalRendTimer = 0
        self.NascentChaosTimer = 0

        #CD
        self.InfuriateCD = 0
        self.UpheavalCD = 0
        self.InnerReleaseCD = 0
        self.OnslaughtCD = 0

    def updateCD(self, time):
        if (self.InfuriateCD > 0) : self.InfuriateCD = max(0,self.InfuriateCD - time)
        if (self.UpheavalCD > 0) : self.UpheavalCD = max(0,self.UpheavalCD - time)
        if (self.InnerReleaseCD > 0) : self.InnerReleaseCD = max(0,self.InnerReleaseCD - time)
        if (self.OnslaughtCD > 0) : self.OnslaughtCD = max(0,self.OnslaughtCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.SurgingTempestTimer > 0) : self.SurgingTempestTimer = max(0,self.SurgingTempestTimer - time)
        if (self.PrimalRendTimer > 0) : self.PrimalRendTimer = max(0,self.PrimalRendTimer - time)
        if (self.NascentChaosTimer > 0) : self.NascentChaosTimer = max(0,self.NascentChaosTimer - time)