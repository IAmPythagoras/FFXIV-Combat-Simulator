
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
        #self.CastingTarget = []
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



        #Used for DPS graph and Potency/S graph

        self.DPSGraph = []
        self.PotencyGraph = []





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

#########################################
########## BLACK MAGE PLAYER ############
#########################################

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

        #print("Player now " + str(Player.Mana) + " mana  ")
        #print("player has : " + str(Player.UmbralIceStack))

#########################################
########## DARK KNIGHT PLAYER ###########
#########################################

class DarkKnight(Player):
    #A class for Dark Knight Players containing all effects and cooldowns relevant to the job.

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Special
        self.DarksideTimer = 0          #Darkside Gauge, starts at 0 with a max duration of 60s.
        self.Blood = 0                  #Blood Gauge, starts at 0 with a max of 100 units.
        self.EsteemPointer = None

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
        self.EdgeShadowCD = 0           #1s     Shares a CD with FloodShadow.
        self.CarveSpitCD = 0            #60s    Shares a CD with AbyssalDrain.
        self.AbyssalDrainCD = 0         #60s    Shares a CD with CarveSpit.
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

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight,Master):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight,Master.Stat)

        self.Blood = 0
        self.Master = Master

    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        

#########################################
########## NINJA PLAYER #################
#########################################


class Ninja(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        
        #Gauge
        self.HutonGauge = 60 #Assumes we start with 60 sec of Huton
        self.NinkiGauge = 0 #Starts with 0

        #oGCD Cooldown
        self.TenChiJinCd = 0    #120 sec
        self.DreamWithinADreamCd = 0 #60 sec
        self.KassatsuCd = 0 #60 sec
        self.MeisuiCd = 0 #120 sec
        self.MugCd = 0 #120 sec
        self.TrickAttackCd = 0 #60 sec
        self.BunshinCd = 0

        #effectTimer
        self.TenChiJinTimer = 0
        self.KassatsuTimer = 0
        self.MeisuiTimer = 0
        self.TrickAttackTimer = 0

        #Ninjutsu Stacks
        self.NinjutsuStack = 2
        self.NinjutsuCd = 0

        #Raiton Stacks
        self.RaitonStacks = 0
        self.RaitonStacksTimer = 0

        #Suiton
        self.SuitonTimer = 0

        #Bunshin
        self.BunshinStacks = 0
        self.BunshinTimer = 0
        self.KamaitachiTimer = 0

    def updateCD(self, time):
        if (self.TenChiJinCd > 0) : self.TenChiJinCd = max(0,self.TenChiJinCd - time)
        if (self.DreamWithinADreamCd > 0) : self.DreamWithinADreamCd = max(0,self.DreamWithinADreamCd - time)
        if (self.KassatsuCd > 0) : self.KassatsuCd = max(0,self.KassatsuCd - time)
        if (self.MeisuiCd > 0) : self.MeisuiCd = max(0,self.MeisuiCd - time)
        if (self.MugCd > 0) : self.MugCd = max(0,self.MugCd - time)
        if (self.TrickAttackCd > 0) : self.TrickAttackCd = max(0,self.TrickAttackCd - time)

    def updateTimer(self, time):
        super().updateTimer(time)

        if (self.TenChiJinTimer > 0) : self.TenChiJinTimer = max(0,self.TenChiJinTimer - time)
        if (self.KassatsuTimer > 0) : self.KassatsuTimer = max(0,self.KassatsuTimer - time)
        if (self.MeisuiTimer > 0) : self.MeisuiTimer = max(0,self.MeisuiTimer - time)
        if (self.HutonGauge > 0) : self.HutonGauge = max(0,self.HutonGauge - time)
        if (self.RaitonStacksTimer > 0) : self.RaitonStacksTimer = max(0,self.RaitonStacksTimer - time)
        if (self.SuitonTimer > 0) : self.SuitonTimer = max(0,self.SuitonTimer - time)
        if (self.BunshinTimer > 0) : self.BunshinTimer = max(0,self.BunshinTimer - time)
        if (self.KamaitachiTimer > 0) : self.KamaitachiTimer = max(0,self.KamaitachiTimer - time)


#########################################
########## SCHOLAR PLAYER ###############
#########################################

class Scholar(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        self.AetherFlowStack = 0

        self.AetherFlowCD = 0
        self.ChainStratagemCD = 0
        self.EnergyDrainCD = 0
        self.SwiftCastCD = 0
        self.LucidDreamingCD = 0
        self.DissipationCD = 0

        self.BiolysisTimer = 0
        self.Biolysis = None

        self.LucidDreamingTimer = 0
        self.ChainStratagemTimer = 0


    def updateCD(self, time):
        if (self.AetherFlowCD > 0) : self.AetherFlowCD = max(0,self.AetherFlowCD - time)
        if (self.ChainStratagemCD > 0) : self.ChainStratagemCD = max(0,self.ChainStratagemCD - time)
        if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.BiolysisTimer > 0) : self.BiolysisTimer = max(0,self.BiolysisTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.ChainStratagemTimer > 0) : self.ChainStratagemTimer = max(0,self.ChainStratagemTimer - time)


#########################################
########## WHITEMAGE PLAYER #############
#########################################

class Whitemage(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)



        #CD
        self.SwiftCastCD = 0
        self.LucidDreamingCD = 0
        self.AssizeCD = 0
        self.ThinAirCD = 0
        self.PresenceOfMindCD = 0


        #Timer
        self.DiaTimer = 0
        self.LucidDreamingTimer = 0
        self.PresenceOfMindTimer = 0

        #DOT
        self.Dia = None

    def updateCD(self, time):
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.AssizeCD > 0) : self.AssizeCD = max(0,self.AssizeCD - time)
        if (self.ThinAirCD > 0) : self.ThinAirCD = max(0,self.ThinAirCD - time)
        if (self.PresenceOfMindCD > 0) : self.PresenceOfMindCD = max(0,self.PresenceOfMindCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.DiaTimer > 0) : self.DiaTimer = max(0,self.DiaTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
        if (self.PresenceOfMindTimer > 0) : self.PresenceOfMindTimer = max(0,self.PresenceOfMindTimer - time)


#########################################
########## REDMAGE PLAYER ###############
#########################################

class Redmage(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        self.BlackMana = 0
        self.WhiteMana = 0
        
        #CD
        self.EmboldenCD = 0
        self.ManaficationCD = 0
        self.SwiftCastCD = 0
        self.LucidDreamingCD = 0
        self.AccelerationCD = 0
        self.FlecheCD = 0
        self.ContreCD = 0
        self.EngagementCD = 0
        self.CorpsCD = 0

        #Timer
        self.EmboldenTimer = 0
        self.ManaficationTimer = 0
        #self.SwiftCastTimer = 0
        self.LucidDreamingTimer = 0
        #self.AccelerationTimer = 0

        #stack
        self.AccelerationStack = 2
        self.EngagementStack = 2
        self.CorpsStack = 2

        self.DualCast = False #True if DualCast cast


        #ComboAction

        self.Zwerchhau = False #If can execute
        self.Redoublement = False
        self.Verholy = False
        self.Scorch = False
        self.Resolution = False

        self.MultDPSBonus = 1.3 #magik and mend

    def updateCD(self, time):
        if (self.EmboldenCD > 0) : self.AetherFlowCD = max(0,self.EmboldenCD - time)
        if (self.ManaficationCD > 0) : self.ManaficationCD = max(0,self.ManaficationCD - time)
        if (self.SwiftCastCD > 0) : self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
        if (self.AccelerationCD > 0) : self.AccelerationCD = max(0,self.AccelerationCD - time)
        if (self.FlecheCD > 0) : self.FlecheCD = max(0,self.FlecheCD - time)
        if (self.ContreCD > 0) : self.ContreCD = max(0,self.ContreCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.EmboldenTimer > 0) : self.EmboldenTimer = max(0,self.EmboldenTimer - time)
        if (self.ManaficationTimer > 0) : self.ManaficationTimer = max(0,self.ManaficationTimer - time)
        if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)


#########################################
########## MACHINIST PLAYER #############
#########################################


class Machinist(Player):
    
    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.BatteryGauge = 0
        self.HeatGauge = 0


        #CD
        self.ChainSawCD = 0
        self.AirAnchorCD = 0
        self.BarrelStabilizerCD = 0
        self.DrillCD = 0
        self.WildFireCD = 0
        self.GaussRoundCD = 0
        self.ReassembleCD = 0
        self.HotShotCD = 0
        self.HyperchargeCD = 0
        self.RicochetCD = 0
        self.AutomatedQueenCD = 0

        #Timer
        self.WildFireTimer = 0
        self.HyperchargeTimer = 0

        #Stacks
        self.GaussRoundStack = 3
        self.ReassembleStack = 2
        self.RicochetStack = 3
        self.WildFireStack = 0  #Used to know how many weaponskills have hit during Wildfire
        self.Reassemble = False

        #Combo Action
        self.SlugShot = False
        self.CleanShot = False

        #Queen
        self.Queen = None
        self.Overdrive = False  #Used to know if we can cast overdrive. Its set to true once the Queen is summoned and set to false when Overdrive is used
        self.QueenOnField = False

        self.MultDPSBonus = 1.2

        

    def updateCD(self, time):
        if (self.ChainSawCD > 0) : self.ChainSawCD = max(0,self.ChainSawCD - time)
        if (self.AirAnchorCD > 0) : self.AirAnchorCD = max(0,self.AirAnchorCD - time)
        if (self.BarrelStabilizerCD > 0) : self.BarrelStabilizerCD = max(0,self.BarrelStabilizerCD - time)
        if (self.DrillCD > 0) : self.DrillCD = max(0,self.DrillCD - time)
        if (self.GaussRoundCD > 0) : self.GaussRoundCD = max(0,self.GaussRoundCD - time)
        if (self.WildFireCD > 0) : self.WildFireCD = max(0,self.WildFireCD - time)
        if (self.HotShotCD > 0) : self.HotShotCD = max(0,self.HotShotCD - time)
        if (self.HyperchargeCD > 0) : self.HyperchargeCD = max(0,self.HyperchargeCD - time)
        if (self.RicochetCD > 0) : self.RicochetCD = max(0,self.RicochetCD - time)
        if (self.AutomatedQueenCD > 0) : self.AutomatedQueenCD = max(0,self.AutomatedQueenCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.WildFireTimer > 0) : self.WildFireTimer = max(0,self.WildFireTimer - time)
        if (self.HyperchargeTimer > 0) : self.HyperchargeTimer = max(0,self.HyperchargeTimer - time)


#Queen Player

class Queen(Player):

    def __init__(self, Machinist, Timer):
        super().__init__(Machinist.GCDTimer, [], [], [], Machinist.CurrentFight, Machinist.Stat)


        self.Master = Machinist

        self.Timer = Timer
        self.Master.Queen = self  #Giving the Queen's pointer to the Machinist
        self.Master.CurrentFight.PlayerList.append(self)
        self.MultDPSBonus = 1.2


    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.Timer > 0) : self.Timer = max(0,self.Timer - time)


#########################################
########## WARRIOR PLAYER ###############
#########################################


class Warrior(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buffs
        self.SurgingTempest = False #If surging tempest is on, set to true

        #Gauge
        self.BeastGauge = 0

        #Stack
        self.InnerReleaseStack = 0
        self.NoBeastCostStack = 0
        self.OnslaughtStack = 3
        self.InfuriateStack = 2

        #Timer
        self.SurgingTempestTimer = 0
        self.PrimalRendTimer = 0
        self.NascentChaosTimer = 0

        #CD
        self.InfuriateCD = 0
        self.UpheavalCD = 0
        self.InnerReleaseCD = 0
        self.OnslaughtCD = 0

    def updateCD(self, time):
        if (self.InfuriateCD > 0) : self.InfuriateCD = max(0,self.InfuriateCD - time)
        if (self.UpheavalCD > 0) : self.UpheavalCD = max(0,self.UpheavalCD - time)
        if (self.InnerReleaseCD > 0) : self.InnerReleaseCD = max(0,self.InnerReleaseCD - time)
        if (self.OnslaughtCD > 0) : self.OnslaughtCD = max(0,self.OnslaughtCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.SurgingTempestTimer > 0) : self.SurgingTempestTimer = max(0,self.SurgingTempestTimer - time)
        if (self.PrimalRendTimer > 0) : self.PrimalRendTimer = max(0,self.PrimalRendTimer - time)
        if (self.NascentChaosTimer > 0) : self.NascentChaosTimer = max(0,self.NascentChaosTimer - time)




#########################################
########## SAMURAI PLAYER ###############
#########################################


class Samurai(Player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Buffs
        self.Fugetsu = False #13% DPS bonus
        self.Fuka = False #13% lest cast/recast time
        self.DirectCrit = False

        #Gauge
        self.KenkiGauge = 0
        self.Setsu = False
        self.Ka = False
        self.Getsu = False
        self.MeditationGauge = 0
        
        #Ready
        self.OgiNamikiriReady = False
        self.KaeshiNamikiriReady = False

        #Timer
        self.FugetsuTimer = 0
        self.FukaTimer = 0
        self.HiganbanaTimer = 0
        

        #CD
        self.MeikyoCD = 0
        self.IkishotenCD = 0
        self.KaeshiCD = 0
        self.SeneiCD = 0
        
        #stack
        self.MeikyoStack = 2

        #EffectStack
        self.Meikyo = 0

        #DOT
        self.Higanbana = None

    def updateCD(self, time):
        if (self.MeikyoCD > 0) : self.MeikyoCD = max(0,self.MeikyoCD - time)
        if (self.IkishotenCD > 0) : self.IkishotenCD = max(0,self.IkishotenCD - time)
        if (self.KaeshiCD > 0) : self.KaeshiCD = max(0,self.KaeshiCD - time)
        if (self.SeneiCD > 0) : self.SeneiCD = max(0,self.SeneiCD - time)
 

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.FugetsuTimer > 0) : self.FugetsuTimer = max(0,self.FugetsuTimer - time)
        if (self.FukaTimer > 0) : self.FukaTimer = max(0,self.FukaTimer - time)
        if (self.HiganbanaTimer > 0) : self.HiganbanaTimer = max(0,self.HiganbanaTimer - time)