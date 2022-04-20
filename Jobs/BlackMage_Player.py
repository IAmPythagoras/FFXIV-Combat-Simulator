#########################################
########## BLACK MAGE PLAYER ############
#########################################
from Jobs.Base_Player import Player
class BlackMage(Player):
    #This class will be blackmage object and will be the one used to simulate a black mage

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        self.EffectCDList = [BLMManaRegenCheck]
        #Prock
        self.T3Prock = False
        self.F3Prock = False
        self.Paradox = True
        self.Enochian = False
        self.SharpCastGoThroughOnce = False

        #Ability Effect Stack
        self.SharpCastStack = 0
        self.TripleCastStack = 0
        self.SwiftCastStack = 0
        self.AstralFireStack = 0
        self.UmbralIceStack = 0
        self.PolyglotStack = 1
        self.UmbralHeartStack = 0

        #Ability Timer
        self.T3Timer = 0
        self.F3Timer = 0
        self.LeyLinesTimer = 0
        self.TripleCastTimer = 0
        self.SwiftCastTimer = 0
        self.SharpCastTimer = 0
        self.AFUITimer = 0

        #Charges
        self.SharpCastCharges = 2
        self.TripleCastCharges = 2

        #Ability CD
        self.LeyLinesCD = 0
        self.SharpCastCD = 0
        self.TripleCastCD = 0
        self.SwiftCastCD = 0
        self.EnochianCD = 0
        self.ManaFrontCD = 0
        self.TransposeCD = 0
        self.AmplifierCD = 0


        self.MultDPSBonus = 1.3 * 1.2   #Mult bonus for DPS, Magik and Mend * Enochian
        self.T3 = None
    
    def updateCD(self, time):
        if (self.LeyLinesCD > 0) : self.LeyLinesCD = max(0,self.LeyLinesCD - time)
        if (self.SharpCastCD > 0) :self.SharpCastCD = max(0,self.SharpCastCD - time)
        if (self.TripleCastCD > 0) :self.TripleCastCD = max(0,self.TripleCastCD - time)
        if (self.SwiftCastCD > 0) :self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.EnochianCD > 0) :self.EnochianCD = max(0,self.EnochianCD - time)
        if (self.ManaFrontCD > 0) :self.ManaFrontCD = max(0,self.ManaFrontCD - time)
        if (self.TransposeCD > 0) :self.TransposeCD = max(0,self.TransposeCD - time)
        if (self.AmplifierCD > 0) :self.AmplifierCD = max(0,self.AmplifierCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.LeyLinesTimer > 0) : self.LeyLinesTimer = max(0,self.LeyLinesTimer - time)
        if (self.T3Timer > 0) : self.T3Timer = max(0,self.T3Timer - time)
        if (self.AFUITimer > 0) : self.AFUITimer = max(0, self.AFUITimer-time)
        if (self.TripleCastTimer > 0) : self.TripleCastTimer = max(0, self.TripleCastTimer-time)
        if (self.SwiftCastTimer > 0) : self.SwiftCastTimer = max(0, self.SwiftCastTimer-time)
        if (self.SharpCastTimer > 0) : self.SharpCastTimer = max(0, self.SharpCastTimer-time)
        if (self.F3Timer > 0) : self.F3Timer = max(0, self.F3Timer-time)
        if (self.PotionTimer > 0) : self.PotionTimer = max(0, self.PotionTimer-time)


def BLMManaRegenCheck(Player, Enemy):   #Mana Regen Stuff
    if Player.ManaTick <= 0:
        Player.ManaTick = 3
        if Player.UmbralIceStack >= 1:
            if(Player.UmbralIceStack == 1):
                Player.Mana = min(10000, Player.Mana + 3200)
            if(Player.UmbralIceStack == 2):
                Player.Mana = min(10000, Player.Mana + 4700)
            if(Player.UmbralIceStack == 3):
                Player.Mana = min(10000, Player.Mana + 6200)