from Jobs.Melee.Melee_Player import Melee

class Reaper(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)



        #Gauge
        self.SoulGauge = 0
        self.ImmortalSacrificeStack = 0
        self.SoulReaverStack = 2
        self.ShroudGauge = 0
        self.LemureGauge = 0
        self.VoidShroudGauge = 0

        #Ready Effect


        #Stack
        self.SoulSliceStack = 2

        #CD
        self.SoulSliceCD = 0 #30 sec CD
        self.ArcaneCircleCD = 0 #120 sec CD
        self.GluttonyCD = 0 #60 sec CD
        self.EnshroudCD = 0 #15 sec CD
        self.HellIngressCD = 0 #20 sec CD
        self.ArcaneCrestCD = 0 # 30 sec CD


        #buff
        self.SoulSow = False #Has to be true to cast Harvest Moon
        self.EnhancedGibbet = False #Buffs Gibbet's Potency
        self.EnhancedGallows = False #Buffs Gallow's Potency

        #Timer
        self.DeathDesignTimer = 0
        self.ArcaneCircleTimer = 0 #on for 20 sec
        self.CircleOfSacrificeTimer = 5 #On for 5 sec
        self.AvatarTimer = 0 #Timer for summoning Avatar, used in Enshroud
        self.GallowsEffectTimer = 0 #Effect of Enhanced Gibbet
        self.GibbetEffectTimer = 0 #Effect of Enhanced Gallows
        self.BloodsownTimer = 0 #Timer before casting Plentiful Harvest
        self.VoidReapingTimer = 0 #timer of enhanced CrossReaping
        self.CrossReapingTimer = 0 #Timer of enhanced VoidReaping
        self.HellIngressTimer = 0 #Timer for insta-casting harpe


        self.JobMod = 115

    def AddGauge(self, Amount):
        self.SoulGauge = min(100, self.SoulGauge + Amount)
    def AddShroud(self, Amount):
        self.ShroudGauge = min(100, self.ShroudGauge + Amount)

    def updateCD(self, time):
        if (self.SoulSliceCD > 0) : self.SoulSliceCD = max(0,self.SoulSliceCD - time)
        if (self.ArcaneCircleCD > 0) : self.ArcaneCircleCD = max(0,self.ArcaneCircleCD - time)
        if (self.GluttonyCD > 0) : self.GluttonyCD = max(0,self.GluttonyCD - time)
        if (self.EnshroudCD > 0) : self.EnshroudCD = max(0,self.EnshroudCD - time)
        if (self.HellIngressCD > 0) : self.HellIngressCD = max(0,self.HellIngressCD - time)
        if (self.ArcaneCrestCD > 0) : self.ArcaneCrestCD = max(0,self.ArcaneCrestCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.DeathDesignTimer > 0) : self.DeathDesignTimer = max(0,self.DeathDesignTimer - time)
        if (self.ArcaneCircleTimer > 0) : self.ArcaneCircleTimer = max(0,self.ArcaneCircleTimer - time)
        if (self.CircleOfSacrificeTimer > 0) : self.CircleOfSacrificeTimer = max(0,self.CircleOfSacrificeTimer - time)
        if (self.AvatarTimer > 0) : self.AvatarTimer = max(0,self.AvatarTimer - time)
        if (self.GallowsEffectTimer > 0) : self.GallowsEffectTimer = max(0,self.GallowsEffectTimer - time)
        if (self.GibbetEffectTimer > 0) : self.GibbetEffectTimer = max(0,self.GibbetEffectTimer - time)
        if (self.BloodsownTimer > 0) : self.BloodsownTimer = max(0,self.BloodsownTimer - time)
        if (self.VoidReapingTimer > 0) : self.VoidReapingTimer = max(0,self.VoidReapingTimer - time)
        if (self.CrossReapingTimer > 0) : self.CrossReapingTimer = max(0,self.CrossReapingTimer - time)
        if (self.HellIngressTimer > 0) : self.HellIngressTimer = max(0,self.HellIngressTimer - time)