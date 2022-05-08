#########################################
########## SAMURAI PLAYER ###############
#########################################

from Jobs.Melee.Melee_Player import Melee

class Samurai(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buffs
        self.Fugetsu = False #13% DPS bonus
        self.Fuka = False #13% lest cast/recast time
        self.DirectCrit = False

        #Gauge
        self.KenkiGauge = 0
        self.Setsu = False
        self.Ka = False
        self.Getsu = False
        self.MeditationGauge = 0
        
        #Ready
        self.OgiNamikiriReady = False
        self.KaeshiNamikiriReady = False

        #Timer
        self.FugetsuTimer = 0
        self.FukaTimer = 0
        self.HiganbanaTimer = 0
        

        #CD
        self.MeikyoCD = 0
        self.IkishotenCD = 0
        self.KaeshiCD = 0
        self.SeneiCD = 0
        
        #stack
        self.MeikyoStack = 2

        #EffectStack
        self.Meikyo = 0

        #DOT
        self.Higanbana = None

        #JobMod
        self.JobMod = 112

    def updateCD(self, time):
        if (self.MeikyoCD > 0) : self.MeikyoCD = max(0,self.MeikyoCD - time)
        if (self.IkishotenCD > 0) : self.IkishotenCD = max(0,self.IkishotenCD - time)
        if (self.KaeshiCD > 0) : self.KaeshiCD = max(0,self.KaeshiCD - time)
        if (self.SeneiCD > 0) : self.SeneiCD = max(0,self.SeneiCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.FugetsuTimer > 0) : self.FugetsuTimer = max(0,self.FugetsuTimer - time)
        if (self.FukaTimer > 0) : self.FukaTimer = max(0,self.FukaTimer - time)
        if (self.HiganbanaTimer > 0) : self.HiganbanaTimer = max(0,self.HiganbanaTimer - time)