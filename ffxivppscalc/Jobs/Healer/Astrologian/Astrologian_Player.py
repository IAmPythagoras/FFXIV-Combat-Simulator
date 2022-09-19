from Jobs.Healer.Healer_Player import Healer

class Astrologian(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Stack
        self.DrawStack = 2
        self.EssentialDignityStack = 2
        self.CelestialIntersectionStack = 2
        #Gauge
        self.Lunar = False #Balance and Bole
        self.Solar = False #Arrow and Ewer
        self.Celestial = False #Spear and Spire
        self.HasCard = True #Assumed to True since we can just draw before. Easier for Pre Pull
        self.Redraw = False #True if we can redraw

        #Buff
        self.LordOfCrown = False

        #CD
        self.LightspeedCD = 0
        self.DivinationCD = 0
        self.MinorArcanaCD = 0
        self.DrawCD = 0
        self.MacrocosmosCD = 0
        self.ExaltationCD = 0
        self.NeutralSectCD = 0
        self.HoroscopeCD = 0
        self.CelestialIntersectionCD = 0
        self.EarthlyStarCD = 0
        self.CelestialOppositionCD = 0
        self.CollectiveCD = 0 #Collective Uncounscious
        self.SynastryCD = 0
        self.EssentialDignityCD = 0

        #timer
        self.CumbustDOTTimer = 0
        self.LightspeedTimer = 0
        self.DivinationTimer = 0
        self.BodyTimer = 0

        #DOT
        self.CumbustDOT = None



    def updateCD(self, time):
        super().updateCD(time)
        if (self.LightspeedCD > 0) : self.LightspeedCD = max(0,self.LightspeedCD - time)
        if (self.DivinationCD > 0) : self.DivinationCD = max(0,self.DivinationCD - time)
        if (self.MinorArcanaCD > 0) : self.MinorArcanaCD = max(0,self.MinorArcanaCD - time)
        if (self.DrawCD > 0) : self.DrawCD = max(0,self.DrawCD - time)
        if (self.MacrocosmosCD > 0) : self.MacrocosmosCD = max(0,self.MacrocosmosCD - time)
        if (self.ExaltationCD > 0) : self.ExaltationCD = max(0,self.ExaltationCD - time)
        if (self.NeutralSectCD > 0) : self.NeutralSectCD = max(0,self.NeutralSectCD - time)
        if (self.HoroscopeCD > 0) : self.HoroscopeCD = max(0,self.HoroscopeCD - time)
        if (self.CelestialIntersectionCD > 0) : self.CelestialIntersectionCD = max(0,self.CelestialIntersectionCD - time)
        if (self.EarthlyStarCD > 0) : self.EarthlyStarCD = max(0,self.EarthlyStarCD - time)
        if (self.CelestialOppositionCD > 0) : self.CelestialOppositionCD = max(0,self.CelestialOppositionCD - time)
        if (self.CollectiveCD > 0) : self.CollectiveCD = max(0,self.CollectiveCD - time)
        if (self.SynastryCD > 0) : self.SynastryCD = max(0,self.SynastryCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.CumbustDOTTimer > 0) : self.CumbustDOTTimer = max(0,self.CumbustDOTTimer - time)
        if (self.LightspeedTimer > 0) : self.LightspeedTimer = max(0,self.LightspeedTimer - time)
        if (self.DivinationTimer > 0) : self.DivinationTimer = max(0,self.DivinationTimer - time)
        if (self.BodyTimer > 0) : self.BodyTimer = max(0,self.BodyTimer - time)