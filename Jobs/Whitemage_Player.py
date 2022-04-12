#########################################
########## WHITEMAGE PLAYER #############
#########################################

class Whitemage(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)



        #CD
        self.SwiftCastCD = 0
        self.LucidDreamingCD = 0
        self.AssizeCD = 0
        self.ThinAirCD = 0
        self.PresenceOfMindCD = 0


        #Timer
        self.DiaTimer = 0
        self.LucidDreamingTimer = 0
        self.PresenceOfMindTimer = 0

        #DOT
        self.Dia = None

    def updateCD(self, time):
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.AssizeCD > 0) : self.AssizeCD = max(0,self.AssizeCD - time)
        if (self.ThinAirCD > 0) : self.ThinAirCD = max(0,self.ThinAirCD - time)
        if (self.PresenceOfMindCD > 0) : self.PresenceOfMindCD = max(0,self.PresenceOfMindCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.DiaTimer > 0) : self.DiaTimer = max(0,self.DiaTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.PresenceOfMindTimer > 0) : self.PresenceOfMindTimer = max(0,self.PresenceOfMindTimer - time)