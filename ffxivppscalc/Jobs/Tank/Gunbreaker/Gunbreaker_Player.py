from ffxivppscalc.Jobs.Tank.Tank_Player import Tank

class Gunbreaker(Tank):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Stack
        self.RoughDivideStack = 2
        self.AuroraStack = 2
        #Gauge
        self.PowderGauge = 0

        #ComboAction
        self.ReadyToRip = False
        self.ReadyToTear = False
        self.ReadyToGouge = False
        self.ReadyToBlast = False

        #cd
        self.GnashingFangCD = 0
        self.BlastingZoneCD = 0
        self.BloodfestCD = 0
        self.DoubleDownCD = 0
        self.SonicBreakCD = 0
        self.BowShockCD = 0
        self.RoughDivideCD = 0
        self.NoMercyCD = 0
        self.AuroraCD = 0
        self.SuperbolideCD = 0
        self.HeartOfLightCD = 0
        self.HeartOfCorundumCD = 0
        self.CamouflageCD = 0

        #Timer
        self.BowShockTimer = 0
        self.SonicBreakTimer = 0
        self.NoMercyTimer = 0

        #DOT
        self.SonicBreakDOT = None
        self.BowShowDOT = None

        #JobMod
        self.JobMod = 100

    def updateCD(self, time):
        super().updateCD(time)
        if (self.GnashingFangCD > 0) : self.GnashingFangCD = max(0,self.GnashingFangCD - time)
        if (self.BlastingZoneCD > 0) : self.BlastingZoneCD = max(0,self.BlastingZoneCD - time)
        if (self.BloodfestCD > 0) : self.BloodfestCD = max(0,self.BloodfestCD - time)
        if (self.DoubleDownCD > 0) : self.DoubleDownCD = max(0,self.DoubleDownCD - time)
        if (self.SonicBreakCD > 0) : self.SonicBreakCD = max(0,self.SonicBreakCD - time)
        if (self.BowShockCD > 0) : self.BowShockCD = max(0,self.BowShockCD - time)
        if (self.RoughDivideCD > 0) : self.RoughDivideCD = max(0,self.RoughDivideCD - time)
        if (self.NoMercyCD > 0) : self.NoMercyCD = max(0,self.NoMercyCD - time)
        if (self.AuroraCD > 0) : self.AuroraCD = max(0,self.AuroraCD - time)
        if (self.SuperbolideCD > 0) : self.SuperbolideCD = max(0,self.SuperbolideCD - time)
        if (self.HeartOfLightCD > 0) : self.HeartOfLightCD = max(0,self.HeartOfLightCD - time)
        if (self.HeartOfCorundumCD > 0) : self.HeartOfCorundumCD = max(0,self.HeartOfCorundumCD - time)
        if (self.CamouflageCD > 0) : self.CamouflageCD = max(0,self.CamouflageCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.BowShockTimer > 0) : self.BowShockTimer = max(0,self.BowShockTimer - time)
        if (self.SonicBreakTimer > 0) : self.SonicBreakTimer = max(0,self.SonicBreakTimer - time)
        if (self.NoMercyTimer > 0) : self.NoMercyTimer = max(0,self.NoMercyTimer - time)