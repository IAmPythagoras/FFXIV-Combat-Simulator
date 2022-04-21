from Jobs.Tank.Tank_Player import Tank

class Paladin(Tank):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

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
        self.FightOrFlighTimer = 0

        #DOT
        self.GoringDOT = None
        self.CircleScornDOT = None

        #CD
        self.RequestACatCD = 0
        self.CircleScornCD = 0
        self.InternveneCD = 0
        self.ExpiacionCD = 0
        self.FightOrFlightCD = 0