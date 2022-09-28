from Jobs.Base_Player import Player
from ffxivppscalc.Jobs.ActionEnum import TankActions

class Tank(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Shared ressources across tank

        #buff
        self.TankStanceOn = False

        #CD
        self.RampartCD = 0
        self.LowBlowCD = 0
        self.ProvokeCD = 0
        self.InterjectCD = 0
        self.ReprisalCD = 0
        self.ArmLengthCD = 0
        self.ShirkCD = 0
        self.BigMitCD = 0
        self.TankStanceCD = 0

        #ActionEnum
        self.ClassAction = TankActions
    
    def updateCD(self,time):
        if (self.RampartCD > 0) : self.RampartCD = max(0,self.RampartCD - time)
        if (self.LowBlowCD > 0) : self.LowBlowCD = max(0,self.LowBlowCD - time)
        if (self.ProvokeCD > 0) : self.ProvokeCD = max(0,self.ProvokeCD - time)
        if (self.InterjectCD > 0) : self.InterjectCD = max(0,self.InterjectCD - time)
        if (self.ShirkCD > 0) : self.ShirkCD = max(0,self.ShirkCD - time)
        if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)
        if (self.ReprisalCD > 0) : self.ReprisalCD = max(0,self.ReprisalCD - time)
        if (self.BigMitCD > 0) : self.BigMitCD = max(0,self.BigMitCD - time)
        if (self.TankStanceCD > 0) : self.TankStanceCD = max(0,self.TankStanceCD - time)
