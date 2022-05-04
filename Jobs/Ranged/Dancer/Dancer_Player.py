from Jobs.Ranged.Ranged_Player import Ranged

class Dancer(Ranged):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)


        #Dancer Partner
        self.DancePartner = None

        #expected proc traking
        self.ExpectedTotalSilkenSymettry = 0
        self.ExpectedTotalSilkenFlow = 0

        #buff
        self.NextDirectCrit = False #True if next 
        self.Dancing = False #True if dancing

        #Dance move
        self.Emboite = False
        self.Entrechat = False
        self.Jete = False
        self.Pirouette = False


        #AbilityReady
        self.SilkenSymettry = False
        self.SilkenFlow = False
        self.StandardFinish = False

        #CD
        self.StandardStepCD = 0



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