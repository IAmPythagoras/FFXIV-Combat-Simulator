#########################################
########## BLACK MAGE PLAYER ############
#########################################
from Jobs.Caster.Caster_Player import Caster

class BlackMage(Caster):
    #This class will be blackmage object and will be the one used to simulate a black mage

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        self.EffectCDList = [BLMManaRegenCheck] #Add this effect
        #Gauge
        self.ElementalGauge = 0 #3 represents 3 astral fire and -3 represents 3 Umbral Ice
        self.PolyglotStack = 0
        self.Paradox = False
        self.UmbralHearts = 0
        self.Enochian = False

        #Stack
        self.TripleCastUseStack = 2
        self.SharpCastStack = 2

        #buff
        self.Thunder3Proc = False
        self.TripleCastStack = 0

        #CD
        self.TransposeCD = 0
        self.AmplifierCD = 0
        self.LeyLinesCD = 0
        self.TripleCastCD = 0
        self.SharpCastCD = 0

        #Timer
        self.PolyglotTimer = 0
        self.EnochianTimer = 0
        self.LeyLinesTimer = 0
        self.Thunder3DOTTimer = 0

        #DOT
        self.Thunder3DOT = None

    def AddFire(self):
        if self.ElementalGauge >= 0 :
            self.EnochianTimer = 15 #Reset Timer
            self.ElementalGauge = min(3, self.ElementalGauge + 1)
        else: #In Ice phase, so we loose it
            self.EnochianTimer = 0
            self.ElementalGauge = 0

    def AddIce(self):
        if self.ElementalGauge <= 0 :
            self.EnochianTimer = 15 #Reset Timer
            self.ElementalGauge = max(-3, self.ElementalGauge - 1)
        else: #In Fire phase, so we loose it
            self.EnochianTimer = 0
            self.ElementalGauge = 0

def BLMManaRegenCheck(Player, Enemy):   #Mana Regen Stuff
    if Player.ManaTick <= 0:
        Player.ManaTick = 3
        if Player.ElementalGauge < 0:
            if(Player.ElementalGauge == -1):
                Player.Mana = min(10000, Player.Mana + 3200)
            if(Player.ElementalGauge == -2):
                Player.Mana = min(10000, Player.Mana + 4700)
            if(Player.ElementalGauge == -3):
                Player.Mana = min(10000, Player.Mana + 6200)
