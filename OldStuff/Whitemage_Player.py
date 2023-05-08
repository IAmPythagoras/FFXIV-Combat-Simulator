#########################################
########## WHITEMAGE PLAYER #############
#########################################

from Jobs.Healer.Healer_Player import Healer
from Jobs.ActionEnum import WhiteMageActions
class Whitemage(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Stack
        self.LilyStack = 0
        self.BloomLily = False
        self.UsedLily = 0

        #CD
        self.LucidDreamingCD = 0
        self.AssizeCD = 0
        self.ThinAirCD = 0
        self.PresenceOfMindCD = 0
        self.BellCD = 0
        self.AquaveilCD = 0
        self.TemperanceCD = 0
        self.PlenaryIndulgenceCD = 0
        self.DivineBenisonCD = 0
        self.TetragrammatonCD = 0
        self.AsylumCD = 0
        self.BenedictionCD = 0


        #Timer
        self.DiaTimer = 0
        self.LucidDreamingTimer = 0
        self.PresenceOfMindTimer = 0
        self.LilyTimer = 40 #Initiated at 40 sec since we have 20 sec CD

        #DOT
        self.Dia = None

        self.EffectCDList.append(LilyCheck) #Starting with this check

        #ActionEnum
        self.JobAction = WhiteMageActions

    def updateCD(self, time):
        super().updateCD(time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.AssizeCD > 0) : self.AssizeCD = max(0,self.AssizeCD - time)
        if (self.ThinAirCD > 0) : self.ThinAirCD = max(0,self.ThinAirCD - time)
        if (self.PresenceOfMindCD > 0) : self.PresenceOfMindCD = max(0,self.PresenceOfMindCD - time)
        if (self.BellCD > 0) : self.BellCD = max(0,self.BellCD - time)
        if (self.AquaveilCD > 0) : self.AquaveilCD = max(0,self.AquaveilCD - time)
        if (self.TemperanceCD > 0) : self.TemperanceCD = max(0,self.TemperanceCD - time)
        if (self.PlenaryIndulgenceCD > 0) : self.PlenaryIndulgenceCD = max(0,self.PlenaryIndulgenceCD - time)
        if (self.DivineBenisonCD > 0) : self.DivineBenisonCD = max(0,self.DivineBenisonCD - time)
        if (self.TetragrammatonCD > 0) : self.TetragrammatonCD = max(0,self.TetragrammatonCD - time)
        if (self.AsylumCD > 0) : self.AsylumCD = max(0,self.AsylumCD - time)
        if (self.BenedictionCD > 0) : self.BenedictionCD = max(0,self.BenedictionCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.DiaTimer > 0) : self.DiaTimer = max(0,self.DiaTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.PresenceOfMindTimer > 0) : self.PresenceOfMindTimer = max(0,self.PresenceOfMindTimer - time)
        if (self.LilyTimer > 0) : self.LilyTimer = max(0,self.LilyTimer - time)

def LilyCheck(Player, Enemy):
    if Player.LilyTimer <= 0:
        Player.LilyStack = min(3, Player.LilyStack + 1)
        Player.LilyTimer = 20 #Reset Timer