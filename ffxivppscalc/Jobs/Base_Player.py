class Player:

    #This class will contain any relevant information to the player. It will be the mother of all other Player

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        self.GCDTimer = GCDTimer    #How long a GCD is
        self.ActionSet = ActionSet  #Known Action List
        self.EffectList = EffectList    #Normally Empty, can has some effects initially
        self.PrePullSet = PrePullSet    #Prepull action list
        self.EffectCDList = []       #List of Effect for which we have to check if the have ended
        self.DOTList = []
        self.NextSpell = 0
        #self.CastingSpell = []
        self.CurrentFight = CurrentFight
        self.ManaTick = 1.5 #Starts Mana tick at this value
        self.playerID = 0 #Might not be necessary so by default 0

        self.TrueLock = False   #Used to know when a player has finished all of its ActionSet
        self.Casting = False    #used to know if an action is possible
        self.oGCDLock = False   #If animation locked by oGCD
        self.GCDLock = False    #If have to wait for another GCD
        self.CastingLockTimer = 0
        self.oGCDLockTimer = 0
        self.GCDLockTimer = 0
        self.PotionTimer = 0
        self.Delay = 3

        self.Mana = 10000 #Starting mana
        self.HP = 1000  #Could be changed
        
        self.TotalPotency = 0
        self.TotalDamage = 0   
        self.TotalMinDamage = 0 #Minimum expected damage (no crit or diret hit) 

        self.Stat = Stat #Stats of the player

        self.auras = [] # List containing all Auras at the start of the fight

        self.Trait = 1  #DPS mult from trait
        self.buffList = []
        self.GCDReduction = 1 #Mult GCD reduction based on Spell Speed or Skill Speed (computed before fight)
        self.CritRateBonus = 0  #CritRateBonus
        self.DHRateBonus = 0 #DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus
        self.EffectToRemove = []
        self.EffectToAdd = [] #List that will add effect to the effectlist or effectcdlist once it has been gone through once

        self.ArcanumTimer = 0 #ArcanumTimer
        self.MeditativeBrotherhoodTimer = 0 #Meditative Brotherhood Timer

        #Used for DPS graph and Potency/S graph

        self.DPSGraph = []
        self.PotencyGraph = []

        self.NumberDamageSpell = 0 #Number of damaging spell done, not including DOT and AA
        self.CritRateHistory = [] #History of crit rate, so we can average them at the end


        #functions for computing damage. Since the stats do not change (except MainStat), we can compute in advance
        #all functions that will not have their values changed
        #They will be computed at the begining of the simulation, they are now set at 0
        self.f_WD = 0
        self.f_DET = 0
        self.f_TEN = 0
        self.f_SPD = 0
        self.CritRate = 0
        self.CritMult = 0
        self.DHRate = 0


    def updateTimer(self, time):
        if (self.GCDLockTimer > 0) : self.GCDLockTimer = max(0, self.GCDLockTimer-time)
        if (self.oGCDLockTimer > 0) : self.oGCDLockTimer = max(0, self.oGCDLockTimer-time)
        if (self.CastingLockTimer > 0) : self.CastingLockTimer = max(0, self.CastingLockTimer-time)
        if (self.ManaTick > 0) : self.ManaTick = max(0, self.ManaTick-time)
        if (self.ArcanumTimer > 0) : self.ArcanumTimer = max(0, self.ArcanumTimer-time)
        if (self.PotionTimer > 0) : self.PotionTimer = max(0, self.PotionTimer-time)
        if (self.MeditativeBrotherhoodTimer > 0) : self.MeditativeBrotherhoodTimer = max(0, self.MeditativeBrotherhoodTimer-time)

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









