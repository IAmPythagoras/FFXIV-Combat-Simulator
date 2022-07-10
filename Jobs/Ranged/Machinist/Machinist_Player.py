#########################################
########## MACHINIST PLAYER #############
#########################################
from Jobs.Ranged.Ranged_Player import Ranged

class Machinist(Ranged):
    
    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.BatteryGauge = 0
        self.HeatGauge = 0


        #CD
        self.ChainSawCD = 0
        self.AirAnchorCD = 0
        self.BarrelStabilizerCD = 0
        self.DrillCD = 0
        self.WildFireCD = 0
        self.GaussRoundCD = 0
        self.ReassembleCD = 0
        self.HotShotCD = 0
        self.HyperchargeCD = 0
        self.RicochetCD = 0
        self.AutomatonQueenCD = 0
        self.FlamethrowerCD = 0
        self.TacticianCD = 0

        #Timer
        self.WildFireTimer = 0
        self.HyperchargeTimer = 0
        self.BioblasterDOTTimer = 0
        self.FlamethrowerDOTTimer = 0
        self.QueenStartUpTimer = 0

        #Stacks
        self.GaussRoundStack = 3
        self.ReassembleStack = 2
        self.RicochetStack = 3
        self.WildFireStack = 0  #Used to know how many weaponskills have hit during Wildfire
        self.Reassemble = False

        #Combo Action
        self.SlugShot = False
        self.CleanShot = False

        #DOT
        self.BioblasterDOT = None
        self.FlamethrowerDOT = None

        #Queen
        self.Queen = None
        self.Overdrive = False  #Used to know if we can cast overdrive. Its set to true once the Queen is summoned and set to false when Overdrive is used
        self.QueenOnField = False

        

    def updateCD(self, time):
        if (self.ChainSawCD > 0) : self.ChainSawCD = max(0,self.ChainSawCD - time)
        if (self.AirAnchorCD > 0) : self.AirAnchorCD = max(0,self.AirAnchorCD - time)
        if (self.BarrelStabilizerCD > 0) : self.BarrelStabilizerCD = max(0,self.BarrelStabilizerCD - time)
        if (self.DrillCD > 0) : self.DrillCD = max(0,self.DrillCD - time)
        if (self.GaussRoundCD > 0) : self.GaussRoundCD = max(0,self.GaussRoundCD - time)
        if (self.WildFireCD > 0) : self.WildFireCD = max(0,self.WildFireCD - time)
        if (self.HotShotCD > 0) : self.HotShotCD = max(0,self.HotShotCD - time)
        if (self.HyperchargeCD > 0) : self.HyperchargeCD = max(0,self.HyperchargeCD - time)
        if (self.RicochetCD > 0) : self.RicochetCD = max(0,self.RicochetCD - time)
        if (self.AutomatonQueenCD > 0) : self.AutomatonQueenCD = max(0,self.AutomatonQueenCD - time)
        if (self.FlamethrowerCD > 0) : self.FlamethrowerCD = max(0,self.FlamethrowerCD - time)
        if (self.TacticianCD > 0) : self.TacticianCD = max(0,self.TacticianCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.WildFireTimer > 0) : self.WildFireTimer = max(0,self.WildFireTimer - time)
        if (self.HyperchargeTimer > 0) : self.HyperchargeTimer = max(0,self.HyperchargeTimer - time)
        if (self.BioblasterDOTTimer > 0) : self.BioblasterDOTTimer = max(0,self.BioblasterDOTTimer - time)
        if (self.FlamethrowerDOTTimer > 0) : self.FlamethrowerDOTTimer = max(0,self.FlamethrowerDOTTimer - time)
        if (self.QueenStartUpTimer > 0) : self.QueenStartUpTimer = max(0,self.QueenStartUpTimer - time)


#Queen Player

class Queen(Ranged):

    def __init__(self, Machinist, Timer):
        super().__init__(Machinist.GCDTimer * Machinist.GCDREduction, [], [], [], Machinist.CurrentFight, Machinist.Stat)


        self.Master = Machinist

        self.Timer = Timer
        self.Master.Queen = self  #Giving the Queen's pointer to the Machinist
        self.Master.CurrentFight.PlayerList.append(self)
        #input(self.Master.CurrentFight.PlayerList)
        self.JobMod = 100

        self.f_WD = Machinist.f_WD
        self.f_DET = Machinist.f_DET
        self.f_TEN = Machinist.f_TEN
        self.f_SPD = Machinist.f_SPD
        self.CritRate = Machinist.CritRate
        self.CritMult = Machinist.CritMult
        self.DHRate = Machinist.DHRate

    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.Timer > 0) : self.Timer = max(0,self.Timer - time)