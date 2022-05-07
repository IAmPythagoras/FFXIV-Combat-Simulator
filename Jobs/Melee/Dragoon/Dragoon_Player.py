#########################################
########## DRAGOON PLAYER ###############
#########################################

from Jobs.Melee.Melee_Player import Melee

class Dragoon(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buff
        self.WheelInMotion = False
        self.FangAndClaw = False

        #CD
        self.LanceChargeCD = 0
        self.BattleLittanyCD = 0
        self.DragonSightCD = 0

        #Timer
        self.PowerSurgeTimer = 0
        self.ChaoticSpringDOTTimer = 0
        self.LanceChargeTimer = 0
        self.BattleLittanyTimer = 0
        self.DragonSightTimer = 0

        #DOT
        self.ChaoticSpringDOT = None