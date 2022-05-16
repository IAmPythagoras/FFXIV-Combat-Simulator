from Jobs.Melee.Melee_Player import Melee

class Reaper(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)



        #Gauge
        self.SoulGauge = 0
        self.ImmortalSacrificeStack = 0
        self.SoulReaverStack = 2
        self.ShroudGauge = 0

        #Ready Effect


        #Stack
        self.SoulSliceStack = 2

        #CD
        self.SoulSliceCD = 0 #30 sec CD
        self.ArcaneCircleCD = 0 #120 sec CD
        self.GluttonyCD = 0 #60 sec CD
        self.EnshroudCD = 0 #15 sec CD


        #buff
        self.SoulSow = False #Has to be true to cast Harvest Moon
        self.EnhancedGibbet = False #Buffs Gibbet's Potency
        self.EnhancedGallows = False #Buffs Gallow's Potency

        #Timer
        self.DeathDesignTimer = 0
        self.ArcaneCircleTimer = 0 #on for 20 sec
        self.CircleOfSacrificeTimer = 5 #On for 5 sec
        self.AvatarTimer = 0 #Timer for summoning Avatar, used in Enshroud
        self.GallowsEffectTimer = 0
        self.GibbetEffectTimer = 0
        self.BloodsownTime = 0


    def AddGauge(self, Amount):
        self.SoulGauge = min(100, self.SoulGauge + Amount)
    def AddShroud(self, Amount):
        self.SoulGauge = min(100, self.ShroudGauge + Amount)

