from Jobs.Healer.Healer_Player import Healer
class Sage(Healer):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Stack
        self.AddersgallStack = 0
        self.AdderstingStack = 0

        #Buff
        self.Eukrasia = False

        #CD
        self.PneumaCD = 0
        self.PhlegmaCD = 0
        self.KrasisCD = 0
        self.PanhaimaCD = 0
        self.HolosCD = 0
        self.RhizomataCD = 0
        self.HaimaCD = 0
        self.TaurocholeCD = 0
        self.PepsiCD = 0
        self.ZoeCD = 0
        self.IxocholeCD = 0
        self.KeracholeCD = 0
        self.IcarusCD = 0
        self.SoteriaCD = 0
        self.PhysisCD = 0
        #Timer
        self.EukrasianTimer = 0
        self.AddersgallTimer = 40 #Starting at 40 since 20 sec countdown

        #DOT
        self.Eukrasian = None

        #Stack
        self.PhlegmaStack = 2
        self.AdderstingStack = 0

        self.EffectCDList.append(AddersgallCheck)


    def updateCD(self, time):
        super().updateCD(time)
        if (self.PneumaCD > 0) : self.PneumaCD = max(0,self.PneumaCD - time)
        if (self.PhlegmaCD > 0) : self.PhlegmaCD = max(0,self.PhlegmaCD - time)
        if (self.KrasisCD > 0) : self.KrasisCD = max(0,self.KrasisCD - time)
        if (self.PanhaimaCD > 0) : self.PanhaimaCD = max(0,self.PanhaimaCD - time)
        if (self.HolosCD > 0) : self.HolosCD = max(0,self.HolosCD - time)
        if (self.RhizomataCD > 0) : self.RhizomataCD = max(0,self.RhizomataCD - time)
        if (self.HaimaCD > 0) : self.HaimaCD = max(0,self.HaimaCD - time)
        if (self.TaurocholeCD > 0) : self.TaurocholeCD = max(0,self.TaurocholeCD - time)
        if (self.PepsiCD > 0) : self.PepsiCD = max(0,self.PepsiCD - time)
        if (self.ZoeCD > 0) : self.ZoeCD = max(0,self.ZoeCD - time)
        if (self.IxocholeCD > 0) : self.IxocholeCD = max(0,self.IxocholeCD - time)
        if (self.KeracholeCD > 0) : self.KeracholeCD = max(0,self.KeracholeCD - time)
        if (self.IcarusCD > 0) : self.IcarusCD = max(0,self.IcarusCD - time)
        if (self.SoteriaCD > 0) : self.SoteriaCD = max(0,self.SoteriaCD - time)
        if (self.PhysisCD > 0) : self.PhysisCD = max(0,self.PhysisCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.EukrasianTimer > 0) : self.EukrasianTimer = max(0,self.EukrasianTimer - time)
        if (self.AddersgallTimer > 0) : self.AddersgallTimer = max(0,self.AddersgallTimer - time)

def AddersgallCheck(Player, Enemy):
    if Player.AddersgallTimer <= 0:
        Player.AddersgallStack = min(3, Player.AddersgallStack + 1)
        Player.AddersgallTimer = 0