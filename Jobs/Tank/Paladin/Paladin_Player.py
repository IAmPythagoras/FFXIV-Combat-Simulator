from Jobs.Tank.Tank_Player import Tank
from Jobs.Base_Player import ManaRegenCheck
class Paladin(Tank):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        self.EffectCDList.append(ManaRegenCheck) #Mana Regen
        #Stack
        self.SwordOathStack = 0
        self.RequestACatStack = 0
        self.InterveneStack = 2

        #BIGSWORDCOMBO
        self.BladeFaith = False
        self.BladeTruth = False
        self.BladeValor = False


        #Buff
        self.RequestACat = False

        #Timer
        self.GoringDOTTimer = 0
        self.CircleScornTimer = 0
        self.ValorDOTTimer = 0
        self.FightOrFlighTimer = 0

        #DOT
        self.GoringDOT = None
        self.CircleScornDOT = None
        self.ValorDOT = None

        #CD
        self.RequestACatCD = 0
        self.CircleScornCD = 0
        self.InternveneCD = 0
        self.ExpiacionCD = 0
        self.FightOrFlightCD = 0

        #JobMod
        self.JobMod = 100

    def updateCD(self, time):
        if (self.RequestACatCD > 0) : self.RequestACatCD = max(0,self.RequestACatCD - time)
        if (self.CircleScornCD > 0) : self.CircleScornCD = max(0,self.CircleScornCD - time)
        if (self.InternveneCD > 0) : self.InternveneCD = max(0,self.InternveneCD - time)
        if (self.ExpiacionCD > 0) : self.ExpiacionCD = max(0,self.ExpiacionCD - time)
        if (self.FightOrFlightCD > 0) : self.FightOrFlightCD = max(0,self.FightOrFlightCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.GoringDOTTimer > 0) : self.GoringDOTTimer = max(0,self.GoringDOTTimer - time)
        if (self.CircleScornTimer > 0) : self.CircleScornTimer = max(0,self.CircleScornTimer - time)
        if (self.FightOrFlighTimer > 0) : self.FightOrFlighTimer = max(0,self.FightOrFlighTimer - time)
        if (self.ValorDOTTimer > 0) : self.ValorDOTTimer = max(0,self.ValorDOTTimer - time)