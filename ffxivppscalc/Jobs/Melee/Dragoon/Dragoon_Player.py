#########################################
########## DRAGOON PLAYER ###############
#########################################

from ffxivppscalc.Jobs.Melee.Melee_Player import Melee

class Dragoon(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Special
        self.LanceMastery = False #Let us know if we are in Wheeling Thrust and FangAndClaw combo

        #Gauge
        self.DragonGauge = 0
        self.FirstmindGauge = 0
        #Stack
        self.SpineshafterStack = 2
        self.LifeSurgeStack = 2

        #Buff
        self.WheelInMotion = False
        self.FangAndClaw = False
        self.LifeOfTheDragon = False
        self.DiveReady = False
        self.DraconianFire = False
        #CD
        self.LanceChargeCD = 0
        self.BattleLitanyCD = 0
        self.DragonSightCD = 0
        self.GeirskogulCD = 0
        self.NastrondCD = 0
        self.HighJumpCD = 0
        self.SpineshafterCD = 0
        self.LifeSurgeCD = 0
        self.StardiverCD = 0
        self.DragonFireDiveCD = 0
        self.WyrmwindThrustCD = 0
        #Timer
        self.PowerSurgeTimer = 0
        self.ChaoticSpringDOTTimer = 0
        self.LanceChargeTimer = 0
        self.BattleLitanyTimer = 0
        self.DragonSightTimer = 0
        self.LifeOfTheDragonTimer = 0

        #DOT
        self.ChaoticSpringDOT = None

        #Next crit
        self.NextCrit = False

        #JobMod
        self.JobMod = 115

    def updateCD(self, time):
        super().updateCD(time)
        if (self.LanceChargeCD > 0) : self.LanceChargeCD = max(0,self.LanceChargeCD - time)
        if (self.BattleLitanyCD > 0) : self.BattleLitanyCD = max(0,self.BattleLitanyCD - time)
        if (self.DragonSightCD > 0) : self.DragonSightCD = max(0,self.DragonSightCD - time)
        if (self.GeirskogulCD > 0) : self.GeirskogulCD = max(0,self.GeirskogulCD - time)
        if (self.NastrondCD > 0) : self.NastrondCD = max(0,self.NastrondCD - time)
        if (self.HighJumpCD > 0) : self.HighJumpCD = max(0,self.HighJumpCD - time)
        if (self.SpineshafterCD > 0) : self.SpineshafterCD = max(0,self.SpineshafterCD - time)
        if (self.LifeSurgeCD > 0) : self.LifeSurgeCD = max(0,self.LifeSurgeCD - time)
        if (self.StardiverCD > 0) : self.StardiverCD = max(0,self.StardiverCD - time)
        if (self.DragonFireDiveCD > 0) : self.DragonFireDiveCD = max(0,self.DragonFireDiveCD - time)
        if (self.WyrmwindThrustCD > 0) : self.WyrmwindThrustCD = max(0,self.WyrmwindThrustCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.PowerSurgeTimer > 0) : self.PowerSurgeTimer = max(0,self.PowerSurgeTimer - time)
        if (self.ChaoticSpringDOTTimer > 0) : self.ChaoticSpringDOTTimer = max(0,self.ChaoticSpringDOTTimer - time)
        if (self.LanceChargeTimer > 0) : self.LanceChargeTimer = max(0,self.LanceChargeTimer - time)
        if (self.BattleLitanyTimer > 0) : self.BattleLitanyTimer = max(0,self.BattleLitanyTimer - time)
        if (self.DragonSightTimer > 0) : self.DragonSightTimer = max(0,self.DragonSightTimer - time)
        if (self.LifeOfTheDragonTimer > 0) : self.LifeOfTheDragonTimer = max(0,self.LifeOfTheDragonTimer - time)