#########################################
########## WARRIOR PLAYER ###############
#########################################

from ffxivppscalc.Jobs.Tank.Tank_Player import Tank

class Warrior(Tank):

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
        self.ThrillOfBattleCD = 0
        self.HolmgangCD = 0
        self.ShakeItOffCD = 0
        self.NascentFlashCD = 0
        self.BloodwhettingCD = 0
        self.EquilibriumCD = 0

        #JobMod
        self.JobMod = 105

    def updateCD(self, time):
        super().updateCD(time)
        if (self.InfuriateCD > 0) : self.InfuriateCD = max(0,self.InfuriateCD - time)
        if (self.UpheavalCD > 0) : self.UpheavalCD = max(0,self.UpheavalCD - time)
        if (self.InnerReleaseCD > 0) : self.InnerReleaseCD = max(0,self.InnerReleaseCD - time)
        if (self.OnslaughtCD > 0) : self.OnslaughtCD = max(0,self.OnslaughtCD - time)
        if (self.ThrillOfBattleCD > 0) : self.ThrillOfBattleCD = max(0,self.ThrillOfBattleCD - time)
        if (self.HolmgangCD > 0) : self.HolmgangCD = max(0,self.HolmgangCD - time)
        if (self.ShakeItOffCD > 0) : self.ShakeItOffCD = max(0,self.ShakeItOffCD - time)
        if (self.NascentFlashCD > 0) : self.NascentFlashCD = max(0,self.NascentFlashCD - time)
        if (self.BloodwhettingCD > 0) : self.BloodwhettingCD = max(0,self.BloodwhettingCD - time)
        if (self.EquilibriumCD > 0) : self.EquilibriumCD = max(0,self.EquilibriumCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.SurgingTempestTimer > 0) : self.SurgingTempestTimer = max(0,self.SurgingTempestTimer - time)
        if (self.PrimalRendTimer > 0) : self.PrimalRendTimer = max(0,self.PrimalRendTimer - time)
        if (self.NascentChaosTimer > 0) : self.NascentChaosTimer = max(0,self.NascentChaosTimer - time)