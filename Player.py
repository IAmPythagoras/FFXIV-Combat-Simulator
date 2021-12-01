class Player:

    #This class will contain any relevant information to the player. It will be the mother of all other Player

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight):
        self.GCDTimer = GCDTimer    #How long a GCD is
        self.ActionSet = ActionSet  #Known Action List
        self.EffectList = EffectList    #Normally Empty, can has some effects initially
        self.PrePullSet = PrePullSet    #Prepull action list
        self.EffectCDList = []          #List of Effect for which we have to check if the have ended
        self.EffectCDList = [ManaRegenCheck]
        self.DOTList = []
        self.NextSpell = 0
        self.CastingSpell = []
        self.CastingTarget = []
        self.CurrentFight = CurrentFight
        self.ManaTick = 3

        self.TrueLock = False   #Used to know when a player has finished all of its ActionSet
        self.Casting = False    #used to know if an action is possible
        self.oGCDLock = False   #If animation locked by oGCD
        self.GCDLock = False    #If have to wait for another GCD
        self.CastingLockTimer = 0
        self.oGCDLockTimer = 0
        self.GCDLockTimer = 0

        self.Mana = 10000
        self.HP = 1000  #Could be changed
        
        self.TotalPotency = 0

    def updateTimer(self, time):
        #print("Updated Timer : " + str(self.oGCDLockTimer))
        #print(str(self.GCDLock) + str(self.oGCDLock) + str(self.Casting))
        if (self.GCDLockTimer > 0) : self.GCDLockTimer = max(0, self.GCDLockTimer-time)
        if (self.oGCDLockTimer > 0) : self.oGCDLockTimer = max(0, self.oGCDLockTimer-time)
        if (self.CastingLockTimer > 0) : self.CastingLockTimer = max(0, self.CastingLockTimer-time)
        if (self.ManaTick > 0) : self.ManaTick = max(0, self.ManaTick-time)

    def updateLock(self):
        if (self.GCDLockTimer <= 0):
            self.GCDLockTimer = 0
            self.GCDLock = False
        
        if (self.oGCDLockTimer <= 0):
            self.oGCDLockTimer = 0
            self.oGCDLock = False
        
        if(self.Casting and self.CastingLockTimer <=0):
            self.CastingSpell.CastFinal(self, self.CastingTarget)

        if (self.CastingLockTimer <= 0):
            self.CastingLockTimer = 0
            self.Casting = False

def ManaRegenCheck(Player, Enemy):  #This function is there by default
    if Player.ManaTick <= 0:
        Player.ManaTick = 3
        Player.Mana = min(10000, Player.Mana + 200)


class BlackMage(Player):
    #This class will be blackmage object and will be the one used to simulate a black mage

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight)
        self.EffectCDList = [BLMManaRegenCheck]
        #Prock
        self.T3Prock = False
        self.F3Prock = False
        self.Paradox = False
        self.Enochian = False

        #Ability Effect Stack
        self.SharpCastStack = 0
        self.TripleCastStack = 0
        self.SwiftCastStack = 0
        self.AstralFireStack = 0
        self.UmbralIceStack = 0
        self.PolyglotStack = 0
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

        #Ability CD
        self.LeyLinesCD = 0
        self.SharpCastCD = 0
        self.TripleCastCD = 0
        self.SwiftCastCD = 0
        self.EnochianCD = 0
        self.ManaFrontCD = 0
        self.TransposeCD = 0
        self.AmplifierCD = 0
    
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

        #print("Player now " + str(Player.Mana) + " mana  ")
        #print("player has : " + str(Player.UmbralIceStack))

#########################################
########## DARK KNIGHT PLAYER ###########
#########################################

class DarkKnight(Player):
    #A class for Dark Knight Players containing all effects and cooldowns relevant to the job.

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight)

        #Special
        self.DarksideTimer = 0          #Darkside Gauge, starts at 0 with a max duration of 60s.
        self.Blood = 0                  #Blood Gauge, starts at 0 with a max of 100 units.

        #Stacks and Ability timers
        self.BloodWeaponTimer = 0       #Duration of Blood Weapon buff.
        self.DeliriumStacks = 0         #Stacks of Delirium.
        self.DeliriumTimer = 0          #Duration of Delirium stacks.
        self.SaltedEarthTimer = 0       #Salted Earth duration, required to use Salt and Darkness.
        self.ShadowbringerCharges = 2   #Charges of Shadowbringer
        self.PlungeCharges = 2          #Charges of Plunge
        self.DarkArts = False           #Dark Arts Gauge, activates when TBN breaks.

        #Cooldowns for all abilities, starting at 0 and adjusted by Apply.

        self.BloodWeaponCD = 0          #60s
        self.DeliriumCD = 0             #60s
        self.EdgeShadowCD = 0           #2s     Shares a CD with Flood.
        self.CarveSpitCD = 0            #60s
        self.AbyssalDrainCD = 0         #60s
        self.SaltedEarthCD = 0          #90s
        self.SaltDarknessCD = 0         #15s
        self.ShadowbringerCD = 0        #60s charge
        self.LivingShadowCD = 0         #120s
        self.PlungeCD = 0               #30s charge
        
    def updateCD(self, time):
        if (self.BloodWeaponCD > 0) : self.BloodWeaponCD = max(0,self.BloodWeaponCD - time)
        if (self.DeliriumCD > 0) :self.DeliriumCD = max(0,self.DeliriumCD - time)
        if (self.EdgeShadowCD > 0) :self.EdgeShadowCD = max(0,self.EdgeShadowCD - time)
        if (self.CarveSpitCD > 0) :self.CarveSpitCD = max(0,self.CarveSpitCD - time)
        if (self.AbyssalDrainCD > 0) :self.AbyssalDrainCD = max(0,self.AbyssalDrainCD - time)
        if (self.SaltedEarthCD > 0) :self.SaltedEarthCD = max(0,self.SaltedEarthCD - time)
        if (self.SaltDarknessCD > 0) :self.SaltDarknessCD = max(0,self.SaltDarknessCD - time)
        if (self.ShadowbringerCD > 0) :self.ShadowbringerCD = max(0,self.ShadowbringerCD - time)
        if (self.LivingShadowCD > 0) :self.LivingShadowCD = max(0,self.LivingShadowCD - time)
        if (self.PlungeCD > 0) :self.PlungeCD = max(0,self.PlungeCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)

        if (self.DarksideTimer > 0) : self.DarksideTimer = max(0,self.DarksideTimer - time)
        if (self.BloodWeaponTimer > 0) : self.BloodWeaponTimer = max(0,self.BloodWeaponTimer - time)
        if (self.DeliriumTimer > 0) : self.DeliriumTimer = max(0,self.DeliriumTimer - time)
        if (self.SaltedEarthTimer > 0) : self.SaltedEarthTimer = max(0, self.SaltedEarthTimer-time)


class Esteem(Player):
    #A class for Living Shadow pet, summoned by Living Shadow.

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight)

        self.Blood = 0

    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        

