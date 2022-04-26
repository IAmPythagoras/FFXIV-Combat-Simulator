from Jobs.Healer.Healer_Player import Healer


class Sage(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buff
        self.Eukrasia = False

        #CD
        self.PneumaCD = 0
        self.PhlegmaCD = 0

        #Timer
        self.EukrasianTimer = 0

        #DOT
        self.Eukrasian = None

        #Stack
        self.PhlegmaStack = 2


    def updateCD(self, time):
        super().updateCD(time)
        if (self.PneumaCD > 0) : self.PneumaCD = max(0,self.PneumaCD - time)
        if (self.PhlegmaCD > 0) : self.PhlegmaCD = max(0,self.PhlegmaCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.EukrasianTimer > 0) : self.EukrasianTimer = max(0,self.EukrasianTimer - time)