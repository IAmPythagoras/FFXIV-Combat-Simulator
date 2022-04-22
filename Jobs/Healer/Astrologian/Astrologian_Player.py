from Jobs.Healer.Healer_Player import Healer

class Astrologian(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Stack
        self.DrawStack = 2

        #Gauge
        self.Lunar = False #Balance and Bole
        self.Solar = False #Arrow and Ewer
        self.Celestial = False #Spear and Spire
        self.HasCard = True #Assumed to True since we can just draw before. Easier for Pre Pull

        #Buff
        self.LordOfCrown = False

        #CD
        self.LightspeedCD = 0
        self.DivinationCD = 0
        self.MinorArcanaCD = 0
        self.DrawCD = 0
        #Timer
        self.CumbustDOTTimer = 0
        self.LightspeedTimer = 0
        self.DivinationTimer = 0
        self.BodyTimer = 0

        #DOT
        self.CumbustDOT = None #That's the actual name of the spell

    def updateCD(self, time):
        super().updateCD(time)
        if (self.LightspeedCD > 0) : self.LightspeedCD = max(0,self.LightspeedCD - time)
        if (self.DivinationCD > 0) : self.DivinationCD = max(0,self.DivinationCD - time)
        if (self.MinorArcanaCD > 0) : self.MinorArcanaCD = max(0,self.MinorArcanaCD - time)
        if (self.DrawCD > 0) : self.DrawCD = max(0,self.DrawCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.CumbustDOTTimer > 0) : self.CumbustDOTTimer = max(0,self.CumbustDOTTimer - time)
        if (self.LightspeedTimer > 0) : self.LightspeedTimer = max(0,self.LightspeedTimer - time)
        if (self.DivinationTimer > 0) : self.DivinationTimer = max(0,self.DivinationTimer - time)
        if (self.BodyTimer > 0) : self.BodyTimer = max(0,self.BodyTimer - time)