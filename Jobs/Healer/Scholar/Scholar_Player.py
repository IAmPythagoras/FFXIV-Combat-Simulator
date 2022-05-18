#########################################
########## SCHOLAR PLAYER ###############
#########################################

from Jobs.Healer.Healer_Player import Healer

class Scholar(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        self.AetherFlowStack = 0

        self.AetherFlowCD = 0
        self.ChainStratagemCD = 0
        self.EnergyDrainCD = 0
        self.LucidDreamingCD = 0
        self.DissipationCD = 0

        self.BiolysisTimer = 0
        self.Biolysis = None

        self.LucidDreamingTimer = 0
        self.ChainStratagemTimer = 0


    def updateCD(self, time):
        super().updateCD(time)
        if (self.AetherFlowCD > 0) : self.AetherFlowCD = max(0,self.AetherFlowCD - time)
        if (self.ChainStratagemCD > 0) : self.ChainStratagemCD = max(0,self.ChainStratagemCD - time)
        if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.BiolysisTimer > 0) : self.BiolysisTimer = max(0,self.BiolysisTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.ChainStratagemTimer > 0) : self.ChainStratagemTimer = max(0,self.ChainStratagemTimer - time)