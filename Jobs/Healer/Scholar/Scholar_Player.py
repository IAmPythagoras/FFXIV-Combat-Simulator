#########################################
########## SCHOLAR PLAYER ###############
#########################################

from Jobs.Healer.Healer_Player import Healer

class Scholar(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        #Stack
        self.AetherFlowStack = 0
        self.ConsolationStack = 0
        #CD
        self.AetherFlowCD = 0
        self.ChainStratagemCD = 0
        self.EnergyDrainCD = 0
        self.LucidDreamingCD = 0
        self.DissipationCD = 0
        self.ExpedientCD = 0
        self.ExpedientCD = 0
        self.ProtractionCD = 0
        self.RecitationCD = 0
        self.EmergencyTacticCD = 0
        self.DeploymentTacticCD = 0
        self.ExcogitationCD = 0
        self.SacredSoilCD = 0
        self.LustrateCD = 0
        self.IndomitabilityCD = 0
        self.SummonSeraphCD = 0
        self.FeyIlluminationCD = 0
        self.FeyBlessingCD = 0
        self.WhisperingDawnCD = 0
        #Timer
        self.BiolysisTimer = 0
        self.LucidDreamingTimer = 0
        self.ChainStratagemTimer = 0
        self.SummonTimer = 0
        #DOT
        self.Biolysis = None
        #Buff
        self.RecitationBuff = False #True if we have it


    def updateCD(self, time):
        super().updateCD(time)
        if (self.AetherFlowCD > 0) : self.AetherFlowCD = max(0,self.AetherFlowCD - time)
        if (self.ChainStratagemCD > 0) : self.ChainStratagemCD = max(0,self.ChainStratagemCD - time)
        if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.DissipationCD > 0) : self.DissipationCD = max(0,self.DissipationCD - time)
        if (self.ExpedientCD > 0) : self.ExpedientCD = max(0,self.ExpedientCD - time)
        if (self.ProtractionCD > 0) : self.ProtractionCD = max(0,self.ProtractionCD - time)
        if (self.RecitationCD > 0) : self.RecitationCD = max(0,self.RecitationCD - time)
        if (self.EmergencyTacticCD > 0) : self.EmergencyTacticCD = max(0,self.EmergencyTacticCD - time)
        if (self.DeploymentTacticCD > 0) : self.DeploymentTacticCD = max(0,self.DeploymentTacticCD - time)
        if (self.ExcogitationCD > 0) : self.ExcogitationCD = max(0,self.ExcogitationCD - time)
        if (self.SacredSoilCD > 0) : self.SacredSoilCD = max(0,self.SacredSoilCD - time)
        if (self.LustrateCD > 0) : self.LustrateCD = max(0,self.LustrateCD - time)
        if (self.IndomitabilityCD > 0) : self.IndomitabilityCD = max(0,self.IndomitabilityCD - time)
        if (self.SummonSeraphCD > 0) : self.SummonSeraphCD = max(0,self.SummonSeraphCD - time)
        if (self.FeyIlluminationCD > 0) : self.FeyIlluminationCD = max(0,self.FeyIlluminationCD - time)
        if (self.FeyBlessingCD > 0) : self.FeyBlessingCD = max(0,self.FeyBlessingCD - time)
        if (self.WhisperingDawnCD > 0) : self.WhisperingDawnCD = max(0,self.WhisperingDawnCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.BiolysisTimer > 0) : self.BiolysisTimer = max(0,self.BiolysisTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.ChainStratagemTimer > 0) : self.ChainStratagemTimer = max(0,self.ChainStratagemTimer - time)
        if (self.SummonTimer > 0) : self.SummonTimer = max(0,self.SummonTimer - time)