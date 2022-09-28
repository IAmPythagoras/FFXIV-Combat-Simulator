#########################################
########## NINJA PLAYER #################
#########################################
from Jobs.Melee.Melee_Player import Melee
from ffxivppscalc.Jobs.ActionEnum import NinjaActions

class Ninja(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.NinkiGauge = 0

        #buff
        self.Suiton = False
        self.Kassatsu = False
        self.Ten = False
        self.Chi = False
        self.Jin = False

        #Stack
        self.NinjutsuStack = 2
        self.RaijuStack = 0
        self.BunshinStack = 0

        #Ready
        self.RaijuReady = False
        self.PhantomKamaitachiReady = False
        

        #Timer
        self.HutonTimer = 0
        self.MugTimer = 0
        self.TrickAttackTimer = 0
        self.MeisuiTimer = 0
        self.KassatsuTimer = 0
        self.SuitonTimer = 0
        self.PhantomKamaitachiReadyTimer = 0
        self.TenChiJinTimer = 0
        self.DotonTimer = 0

        #CD
        self.DreamWithinADreamCD = 0
        self.MugCD = 0
        self.TrickAttackCD = 0
        self.MeisuiCD = 0
        self.NinjutsuCD = 0
        self.KassatsuCD = 0
        self.TenChiJinCD = 0
        self.BunshinCD = 0
        self.ShadeShiftCD = 0

        #Ninjutsu
        self.CurrentRitual = [] #List of currently done ritual
        self.TenChiJinRitual = [] #List of Ritual's done in TenChiJin

        #DOT
        self.DotonDOT = None

        #JobMod
        self.JobMod = 110

        #Shadow 
        self.Shadow = None #Pointer to Shadow object

        #ActionEnum
        self.JobAction = NinjaActions
        
    def ResetRitual(self):
        self.CurrentRitual = []


    def updateCD(self, time):
        super().updateCD(time)
        if (self.DreamWithinADreamCD > 0) : self.DreamWithinADreamCD = max(0,self.DreamWithinADreamCD - time)
        if (self.MugCD > 0) : self.MugCD = max(0,self.MugCD - time)
        if (self.TrickAttackCD > 0) : self.TrickAttackCD = max(0,self.TrickAttackCD - time)
        if (self.MeisuiCD > 0) : self.MeisuiCD = max(0,self.MeisuiCD - time)
        if (self.NinjutsuCD > 0) : self.NinjutsuCD = max(0,self.NinjutsuCD - time)
        if (self.KassatsuCD > 0) : self.KassatsuCD = max(0,self.KassatsuCD - time)
        if (self.TenChiJinCD > 0) : self.TenChiJinCD = max(0,self.TenChiJinCD - time)
        if (self.BunshinCD > 0) : self.BunshinCD = max(0,self.BunshinCD - time)
        if (self.ShadeShiftCD > 0) : self.ShadeShiftCD = max(0,self.ShadeShiftCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.HutonTimer > 0) : self.HutonTimer = max(0,self.HutonTimer - time)
        if (self.MugTimer > 0) : self.MugTimer = max(0,self.MugTimer - time)
        if (self.TrickAttackTimer > 0) : self.TrickAttackTimer = max(0,self.TrickAttackTimer - time)
        if (self.MeisuiTimer > 0) : self.MeisuiTimer = max(0,self.MeisuiTimer - time)
        if (self.KassatsuTimer > 0) : self.KassatsuTimer = max(0,self.KassatsuTimer - time)
        if (self.SuitonTimer > 0) : self.SuitonTimer = max(0,self.SuitonTimer - time)
        if (self.PhantomKamaitachiReadyTimer > 0) : self.PhantomKamaitachiReadyTimer = max(0,self.PhantomKamaitachiReadyTimer - time)
        if (self.TenChiJinTimer > 0) : self.TenChiJinTimer = max(0,self.TenChiJinTimer - time)

    def AddNinki(self, amount):
        self.NinkiGauge = min(100, self.NinkiGauge + amount)
        #input("NinkiGauge is now : " + str(self.NinkiGauge))

    def AddHuton(self, amount):
        self.HutonTimer = min(60, self.HutonTimer + amount)


class Shadow(Ninja):
    def __init__(self, Master):
        super().__init__(Master.GCDTimer * Master.GCDReduction * 0.85, [], [], [], Master.CurrentFight, Master.Stat) #GCD assumes Huton
        #This won't change anything, since the Master is directing the attacks anyway

        self.Master = Master
        self.Master.Shadow = self  #Giving Master the pointer of the shadow
        self.Master.CurrentFight.PlayerList.append(self)
        self.JobMod = 100
        #Giving already computed values
        self.f_WD = Master.f_WD
        self.f_DET = Master.f_DET
        self.f_TEN = Master.f_TEN
        self.f_SPD = Master.f_SPD
        self.CritRate = Master.CritRate
        self.CritMult = Master.CritMult
        self.DHRate = Master.DHRate