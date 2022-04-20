#########################################
########## NINJA PLAYER #################
#########################################
from Jobs.Base_Player import Player

class Ninja(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        
        #Gauge
        self.HutonGauge = 60 #Assumes we start with 60 sec of Huton
        self.NinkiGauge = 0 #Starts with 0

        #oGCD Cooldown
        self.TenChiJinCd = 0    #120 sec
        self.DreamWithinADreamCd = 0 #60 sec
        self.KassatsuCd = 0 #60 sec
        self.MeisuiCd = 0 #120 sec
        self.MugCd = 0 #120 sec
        self.TrickAttackCd = 0 #60 sec
        self.BunshinCd = 0

        #effectTimer
        self.TenChiJinTimer = 0
        self.KassatsuTimer = 0
        self.MeisuiTimer = 0
        self.TrickAttackTimer = 0
        self.MugTimer = 0

        #Ninjutsu Stacks
        self.NinjutsuStack = 2
        self.NinjutsuCd = 0

        #Raiton Stacks
        self.RaitonStacks = 0
        self.RaitonStacksTimer = 0

        #Suiton
        self.SuitonTimer = 0

        #Bunshin
        self.BunshinStacks = 0
        self.BunshinTimer = 0
        self.KamaitachiTimer = 0

    def updateCD(self, time):
        if (self.TenChiJinCd > 0) : self.TenChiJinCd = max(0,self.TenChiJinCd - time)
        if (self.DreamWithinADreamCd > 0) : self.DreamWithinADreamCd = max(0,self.DreamWithinADreamCd - time)
        if (self.KassatsuCd > 0) : self.KassatsuCd = max(0,self.KassatsuCd - time)
        if (self.MeisuiCd > 0) : self.MeisuiCd = max(0,self.MeisuiCd - time)
        if (self.MugCd > 0) : self.MugCd = max(0,self.MugCd - time)
        if (self.TrickAttackCd > 0) : self.TrickAttackCd = max(0,self.TrickAttackCd - time)

    def updateTimer(self, time):
        super().updateTimer(time)

        if (self.TenChiJinTimer > 0) : self.TenChiJinTimer = max(0,self.TenChiJinTimer - time)
        if (self.KassatsuTimer > 0) : self.KassatsuTimer = max(0,self.KassatsuTimer - time)
        if (self.MeisuiTimer > 0) : self.MeisuiTimer = max(0,self.MeisuiTimer - time)
        if (self.HutonGauge > 0) : self.HutonGauge = max(0,self.HutonGauge - time)
        if (self.RaitonStacksTimer > 0) : self.RaitonStacksTimer = max(0,self.RaitonStacksTimer - time)
        if (self.SuitonTimer > 0) : self.SuitonTimer = max(0,self.SuitonTimer - time)
        if (self.BunshinTimer > 0) : self.BunshinTimer = max(0,self.BunshinTimer - time)
        if (self.KamaitachiTimer > 0) : self.KamaitachiTimer = max(0,self.KamaitachiTimer - time)
        if (self.MugTimer > 0) : self.MugTimer = max(0,self.MugTimer - time)