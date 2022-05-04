from Jobs.Ranged.Ranged_Player import Ranged

class Dancer(Ranged):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.MaxFourfoldFeather = 0
        self.MaxEspritGauge = 0

        #Dancer Partner
        self.DancePartner = None


        #Used total proc
        self.UsedSilkenFlow = 0
        self.UsedSilkenSymettry = 0
        self.UsedFourfoldFeather = 0
        self.UsedThreefoldFan = 0



        #expected proc traking
        self.ExpectedSilkenSymettry = 0
        self.ExpectedSilkenFlow = 0
        self.ExpectedFourfoldFeather = 0
        self.ExpectedThreefoldFan = 0

        #buff
        self.NextDirectCrit = False #True if next 
        self.Dancing = False #True if dancing
        self.StandardFinishDPSMult = 1
        self.TechnicalFinishDPSMult = 1
        #Dance move
        self.Emboite = False
        self.Entrechat = False
        self.Jete = False
        self.Pirouette = False


        #AbilityReady
        self.SilkenSymettry = False
        self.SilkenFlow = False
        self.StandardFinish = False
        self.TechnicalFinish = False
        self.FlourishingFinish = False
        self.FlourishingStarfall = False
        #Flourish
        self.FlourishingSymettry = False
        self.FlourishingFlow = False
        self.ThreefoldFan = False
        self.FourfoldFan = False


        #CD
        self.StandardStepCD = 0
        self.TechnicalStepCD = 0
        self.DevilmentCD = 0
        self.FlourishCD = 0
        self.ClosedPositionCD = 0

        #Timer
        self.StandardFinishTimer = 0
        self.TechnicalFinishTimer = 0
        self.DevilmentTimer = 0



    def updateCD(self, time):
        if (self.StandardStepCD > 0) : self.StandardStepCD = max(0,self.StandardStepCD - time)
        if (self.TechnicalStepCD > 0) : self.TechnicalStepCD = max(0,self.TechnicalStepCD - time)
        if (self.DevilmentCD > 0) : self.DevilmentCD = max(0,self.DevilmentCD - time)
        if (self.FlourishCD > 0) : self.FlourishCD = max(0,self.FlourishCD - time)
        if (self.ClosedPositionCD > 0) : self.ClosedPositionCD = max(0,self.ClosedPositionCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.StandardFinishTimer > 0) : self.StandardFinishTimer = max(0,self.StandardFinishTimer - time)
        if (self.TechnicalFinishTimer > 0) : self.TechnicalFinishTimer = max(0,self.TechnicalFinishTimer - time)
        if (self.DevilmentTimer > 0) : self.DevilmentTimer = max(0,self.DevilmentTimer - time)