#########################################
########## SAMURAI PLAYER ###############
#########################################

from Jobs.Melee.Melee_Player import Melee
from Jobs.ActionEnum import SamuraiActions

class Samurai(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buffs
        self.Fugetsu = False #13% DPS bonus
        self.Fuka = False #13% lest cast/recast time
        self.DirectCrit = False
        self.KaeshiHiganbana = False #True if we can cast
        self.KaeshiGoken = False #True if we can cast
        self.KaeshiSetsugekka = False #True if we can cast


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
        self.EnhancedEnpiTimer = 0
        

        #CD
        self.MeikyoCD = 0
        self.IkishotenCD = 0
        self.KaeshiCD = 0
        self.SeneiCD = 0
        self.ThirdEyeCD = 0
        self.GyotenCD = 0
        self.YatenCD = 0
        self.MeditateCD = 0
        self.KyutenCD = 0
        self.TsubamegaeshiCD = 0
        self.HagakureCD = 0
        
        #stack
        self.MeikyoStack = 2
        self.TsubamegaeshiStack = 2

        #EffectStack
        self.Meikyo = 0

        #DOT
        self.Higanbana = None

        #JobMod
        self.JobMod = 112

        #ActionEnum
        self.JobAction = SamuraiActions

    def updateCD(self, time):
        super().updateCD(time)
        if (self.MeikyoCD > 0) : self.MeikyoCD = max(0,self.MeikyoCD - time)
        if (self.IkishotenCD > 0) : self.IkishotenCD = max(0,self.IkishotenCD - time)
        if (self.KaeshiCD > 0) : self.KaeshiCD = max(0,self.KaeshiCD - time)
        if (self.SeneiCD > 0) : self.SeneiCD = max(0,self.SeneiCD - time)
        if (self.ThirdEyeCD > 0) : self.ThirdEyeCD = max(0,self.ThirdEyeCD - time)
        if (self.GyotenCD > 0) : self.GyotenCD = max(0,self.GyotenCD - time)
        if (self.YatenCD > 0) : self.YatenCD = max(0,self.YatenCD - time)
        if (self.MeditateCD > 0) : self.MeditateCD = max(0,self.MeditateCD - time)
        if (self.KyutenCD > 0) : self.KyutenCD = max(0,self.KyutenCD - time)
        if (self.TsubamegaeshiCD > 0) : self.TsubamegaeshiCD = max(0,self.TsubamegaeshiCD - time)
        if (self.HagakureCD > 0) : self.HagakureCD = max(0,self.HagakureCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.FugetsuTimer > 0) : self.FugetsuTimer = max(0,self.FugetsuTimer - time)
        if (self.FukaTimer > 0) : self.FukaTimer = max(0,self.FukaTimer - time)
        if (self.HiganbanaTimer > 0) : self.HiganbanaTimer = max(0,self.HiganbanaTimer - time)
        if (self.EnhancedEnpiTimer > 0) : self.EnhancedEnpiTimer = max(0,self.EnhancedEnpiTimer - time)