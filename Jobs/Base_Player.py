class Player:

    #This class will contain any relevant information to the player. It will be the mother of all other Player

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        self.GCDTimer = GCDTimer    #How long a GCD is
        self.ActionSet = ActionSet  #Known Action List
        self.EffectList = EffectList    #Normally Empty, can has some effects initially
        self.PrePullSet = PrePullSet    #Prepull action list
        self.EffectCDList = [ManaRegenCheck]       #List of Effect for which we have to check if the have ended
        self.DOTList = []
        self.NextSpell = 0
        self.CastingSpell = []
        self.CurrentFight = CurrentFight
        self.ManaTick = 1.5 #Starts Mana tick at this value

        self.TrueLock = False   #Used to know when a player has finished all of its ActionSet
        self.Casting = False    #used to know if an action is possible
        self.oGCDLock = False   #If animation locked by oGCD
        self.GCDLock = False    #If have to wait for another GCD
        self.CastingLockTimer = 0
        self.oGCDLockTimer = 0
        self.GCDLockTimer = 0
        self.PotionTimer = 0

        self.Mana = 10000 #Starting mana
        self.HP = 1000  #Could be changed
        
        self.TotalPotency = 0
        self.TotalDamage = 0    

        self.Stat = Stat #Stats of the player

        self.MultDPSBonus = 1   #Mult bonus for DPS (Ex: BLM.MultDPSBonus = 1.3 * 1.2 -> Enochian * Magik and Mend)
        self.GCDReduction = 1 #Mult GCD reduction based on Spell Speed or Skill Speed (computed before fight)

        self.EffectToRemove = []

        self.ArcanumTimer = 0 #ArcanumTimer

        #Used for DPS graph and Potency/S graph

        self.DPSGraph = []
        self.PotencyGraph = []





    def updateTimer(self, time):
        #input("Update called at : " + str(self.CurrentFight.TimeStamp))
        if (self.GCDLockTimer > 0) : self.GCDLockTimer = max(0, self.GCDLockTimer-time)
        if (self.oGCDLockTimer > 0) : self.oGCDLockTimer = max(0, self.oGCDLockTimer-time)
        if (self.CastingLockTimer > 0) : self.CastingLockTimer = max(0, self.CastingLockTimer-time)
        if (self.ManaTick > 0) : self.ManaTick = max(0, self.ManaTick-time)
        if (self.ArcanumTimer > 0) : self.ArcanumTimer = max(0, self.ArcanumTimer-time)

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









