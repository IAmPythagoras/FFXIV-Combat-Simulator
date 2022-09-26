from ffxivppscalc.Jobs.Caster.Caster_Player import Caster
from ffxivppscalc.Jobs.Base_Player import ManaRegenCheck


class Summoner(Caster):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        self.EffectCDList.append(ManaRegenCheck)#Mana Regen
        #Gauge
        self.AetherflowGauge = 0

        #Trance
        self.FirebirdTrance = False #Birdy
        self.DreadwyrmTrance = False #Bahamut
        self.LastTranceBahamut = False #If false, next trance is bahamut. If true, next trance is phoenix

        #Primal Stacks
        self.GarudaStack = 0
        self.IfritStack = 0
        self.TitanStack = 0

        #Gems Stack (For summoning Primals)
        self.TitanGem = False
        self.GarudaGem = False
        self.IfritGem = False

        #Primal Special Attack
        self.GarudaSpecial = False
        self.IfritSpecial = False
        self.IfritSpecialCombo = False
        self.TitanSpecial = False

        #CD
        self.TranceCD = 0
        self.SearingLightCD = 0
        self.EnergyDrainCD = 0
        self.SummonCD = 0

        #buff
        self.FurtherRuin = False #Used for Ruin IV
        self.Enkindle = False
        self.Deathflare = False #Used for deathflare

        #Timer
        self.TranceTimer = 0
        self.SearingLightTimer = 0
        self.SlipstreamDOTTimer = 0
        self.SummonDOTTimer = 0

        #DOT
        self.SlipstreamDOT = None
        self.SummonDOT = None

        #Summon
        self.Summon = None

    def updateCD(self, time):
        super().updateCD(time)
        if (self.TranceCD > 0) : self.TranceCD = max(0,self.TranceCD - time)
        if (self.SearingLightCD > 0) : self.SearingLightCD = max(0,self.SearingLightCD - time)
        if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
        if (self.SummonCD > 0) : self.SummonCD = max(0,self.SummonCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.TranceTimer > 0) : self.TranceTimer = max(0,self.TranceTimer - time)
        if (self.SearingLightTimer > 0) : self.SearingLightTimer = max(0,self.SearingLightTimer - time)
        if (self.SlipstreamDOTTimer > 0) : self.SlipstreamDOTTimer = max(0,self.SlipstreamDOTTimer - time)
        if (self.SummonDOTTimer > 0) : self.SummonDOTTimer = max(0,self.SummonDOTTimer - time)

class BigSummon(Summoner): #Bahamut of phoenix
    def __init__(self, Master):
        super().__init__(Master.GCDTimer * Master.GCDReduction, [], [], [], Master.CurrentFight, Master.Stat) #GCD assumes Huton

        self.Master = Master
        self.Master.Shadow = self  #Giving Master the pointer of the summon
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