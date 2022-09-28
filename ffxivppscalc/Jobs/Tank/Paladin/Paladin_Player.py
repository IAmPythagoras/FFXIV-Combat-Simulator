from Jobs.Tank.Tank_Player import Tank
from Jobs.Base_Player import ManaRegenCheck
from ffxivppscalc.Jobs.ActionEnum import PaladinActions
class Paladin(Tank):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        self.EffectCDList.append(ManaRegenCheck) #Mana Regen

        #Gauge
        self.OathGauge = 100


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
        self.InterveneCD = 0
        self.ExpiacionCD = 0
        self.FightOrFlightCD = 0
        self.DivineVeilCD = 0
        self.HolySheltronCD = 0
        self.CoverCD = 0
        self.InterventionCD = 0
        self.PassageOfArmsCD = 0
        self.HallowedGroundCD = 0

        #JobMod
        self.JobMod = 100

        #ActionEnum
        self.JobAction = PaladinActions

    def updateCD(self, time):
        super().updateCD(time)
        if (self.RequestACatCD > 0) : self.RequestACatCD = max(0,self.RequestACatCD - time)
        if (self.CircleScornCD > 0) : self.CircleScornCD = max(0,self.CircleScornCD - time)
        if (self.InterveneCD > 0) : self.InterveneCD = max(0,self.InterveneCD - time)
        if (self.ExpiacionCD > 0) : self.ExpiacionCD = max(0,self.ExpiacionCD - time)
        if (self.FightOrFlightCD > 0) : self.FightOrFlightCD = max(0,self.FightOrFlightCD - time)
        if (self.HolySheltronCD > 0) : self.HolySheltronCD = max(0,self.HolySheltronCD - time)
        if (self.CoverCD > 0) : self.CoverCD = max(0,self.CoverCD - time)
        if (self.InterventionCD > 0) : self.InterventionCD = max(0,self.InterventionCD - time)
        if (self.PassageOfArmsCD > 0) : self.PassageOfArmsCD = max(0,self.PassageOfArmsCD - time)
        if (self.HallowedGroundCD > 0) : self.HallowedGroundCD = max(0,self.HallowedGroundCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.GoringDOTTimer > 0) : self.GoringDOTTimer = max(0,self.GoringDOTTimer - time)
        if (self.CircleScornTimer > 0) : self.CircleScornTimer = max(0,self.CircleScornTimer - time)
        if (self.FightOrFlighTimer > 0) : self.FightOrFlighTimer = max(0,self.FightOrFlighTimer - time)
        if (self.ValorDOTTimer > 0) : self.ValorDOTTimer = max(0,self.ValorDOTTimer - time)


#Oath Gauge Effect
def OathGauge(Player, Spell):
    if Spell.id == -22: #AA's DOT have id -1
        Player.OathGauge = min(100, Player.OathGauge + 5) #adding 5 Gauge each AA
