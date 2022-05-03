from Jobs.Ranged.Ranged_Player import Ranged

class Bard(Ranged):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Expected Proc number
        self.ExpectedRefulgent = 0
        self.ExpectedRepertoire = 0
        self.ExpectedSoulVoiceGauge = 0
        self.ExpectedBloodLetterReduction = 0
        self.ExpectedTotalWandererRepertoire = 0

        #Used proc
        self.UsedRefulgent = 0
        self.UsedRepertoire = 0 #Only relevant for Wanderer and pitch perfect
        self.UsedSoulVoiceGauge = 0
        self.UsedBloodLetterReduction = 0
        self.UsedRepertoireAdd = 0 #This is repertoire stacks we used more than the expected value
        self.UsedTotalWandererRepertoire = 0


        #Gauge
        self.SoulVoiceGauge = 0
        self.Repertoire = 0
        self.MaximumRepertoire = 0 #Used for wanderer
        self.MaximumBloodLetterReduction = 0

        #Stack
        self.BloodLetterStack = 3


        #buff
        self.StraightShotReady = False
        self.BlastArrowReady = True


        #Song
        self.MageBallad = False
        self.ArmyPaeon = False
        self.WandererMinuet = False

        #Coda
        self.MageCoda = False
        self.ArmyCoda = False
        self.WandererCoda = False


        #CD
        self.SidewinderCD = 0
        self.EmpyrealArrowCD = 0
        self.WandererMinuetCD = 0
        self.ArmyPaeonCD = 0
        self.MageBalladCD = 0
        self.BattleVoiceCD = 0
        self.BloodLetterCD = 0
        self.BarrageCD = 0
        self.RagingStrikeCD = 0

        #Timer
        self.SongTimer = 0
        self.StormbiteDOTTimer = 0
        self.CausticbiteDOTTimer = 0
        self.BattleVoiceTimer = 0
        self.RagingStrikeTimer = 0
        self.RadiantFinaleTimer = 0

        #DOT
        self.StormbiteDOT = None
        self.CausticbiteDOT = None


        #DPSBonus
        self.MultDPSBonus = 1.2
        self.RadiantFinaleBonus = 1
    
    def updateCD(self, time):
        if (self.SidewinderCD > 0) : self.SidewinderCD = max(0,self.SidewinderCD - time)
        if (self.EmpyrealArrowCD > 0) : self.EmpyrealArrowCD = max(0,self.EmpyrealArrowCD - time)
        if (self.WandererMinuetCD > 0) : self.WandererMinuetCD = max(0,self.WandererMinuetCD - time)
        if (self.ArmyPaeonCD > 0) : self.ArmyPaeonCD = max(0,self.ArmyPaeonCD - time)
        if (self.MageBalladCD > 0) : self.MageBalladCD = max(0,self.MageBalladCD - time)
        if (self.BattleVoiceCD > 0) : self.BattleVoiceCD = max(0,self.BattleVoiceCD - time)
        if (self.BloodLetterCD > 0) : self.BloodLetterCD = max(0,self.BloodLetterCD - time)
        if (self.BarrageCD > 0) : self.BarrageCD = max(0,self.BarrageCD - time)
        if (self.RagingStrikeCD > 0) : self.RagingStrikeCD = max(0,self.RagingStrikeCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.SongTimer > 0) : self.SongTimer = max(0,self.SongTimer - time)
        if (self.StormbiteDOTTimer > 0) : self.StormbiteDOTTimer = max(0,self.StormbiteDOTTimer - time)
        if (self.CausticbiteDOTTimer > 0) : self.CausticbiteDOTTimer = max(0,self.CausticbiteDOTTimer - time)
        if (self.BattleVoiceTimer > 0) : self.BattleVoiceTimer = max(0,self.BattleVoiceTimer - time)
        if (self.RagingStrikeTimer > 0) : self.RagingStrikeTimer = max(0,self.RagingStrikeTimer - time)
        if (self.RadiantFinaleTimer > 0) : self.RadiantFinaleTimer = max(0,self.RadiantFinaleTimer - time)