from Jobs.Ranged.Ranged_Player import Ranged

class Bard(Ranged):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.SoulVoiceGauge = 0

        #Stack
        self.BloodLetterStack = 3


        #buff
        self.StraightShotReady = False
        self.RepertoireStack = 0


        #Song
        self.MageBallad = False
        self.ArmyPaeon = False
        self.WandererMinuet = False


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
        self.CausticDOTTimer = 0
        self.BattleVoiceTimer = 0
        self.RagingStrikeTimer = 0

        #DOT
        self.StormbiteDOT = None
        self.CausticbiteDOT = None
    
    def updateCD(self, time):
        if (self.ChainSawCD > 0) : self.ChainSawCD = max(0,self.ChainSawCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
