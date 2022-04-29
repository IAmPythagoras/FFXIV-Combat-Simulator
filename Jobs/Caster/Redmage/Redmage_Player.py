#########################################
########## REDMAGE PLAYER ###############
#########################################
from Jobs.Caster.Caster_Player import Caster

class Redmage(Caster):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        self.BlackMana = 0
        self.WhiteMana = 0
        
        #CD
        self.EmboldenCD = 0
        self.ManaficationCD = 0
        self.LucidDreamingCD = 0
        self.AccelerationCD = 0
        self.FlecheCD = 0
        self.ContreCD = 0
        self.EngagementCD = 0
        self.CorpsCD = 0

        #Timer
        self.EmboldenTimer = 0
        self.ManaficationTimer = 0
        #self.SwiftCastTimer = 0
        self.LucidDreamingTimer = 0
        #self.AccelerationTimer = 0

        #stack
        self.AccelerationStack = 2
        self.EngagementStack = 2
        self.CorpsStack = 2

        self.DualCast = False #True if DualCast cast


        #ComboAction

        self.Zwerchhau = False #If can execute
        self.Redoublement = False
        self.Verholy = False
        self.Scorch = False
        self.Resolution = False

        self.MultDPSBonus = 1.3 #magik and mend

    def updateCD(self, time):
        super().updateCD(time)
        if (self.EmboldenCD > 0) : self.EmboldenCD = max(0,self.EmboldenCD - time)
        if (self.ManaficationCD > 0) : self.ManaficationCD = max(0,self.ManaficationCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.AccelerationCD > 0) : self.AccelerationCD = max(0,self.AccelerationCD - time)
        if (self.FlecheCD > 0) : self.FlecheCD = max(0,self.FlecheCD - time)
        if (self.ContreCD > 0) : self.ContreCD = max(0,self.ContreCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.EmboldenTimer > 0) : self.EmboldenTimer = max(0,self.EmboldenTimer - time)
        if (self.ManaficationTimer > 0) : self.ManaficationTimer = max(0,self.ManaficationTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)