# This file contains the Player class and its implementation
from copy import deepcopy
from ffxivcalc.Jobs.PlayerEnum import JobEnum, RoleEnum
from ffxivcalc.Jobs.ActionEnum import *
from ffxivcalc.Request.etro_request import get_gearset_data

from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import EnochianEffect, ElementalEffect
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import DualCastEffect
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import SongEffect
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import EspritEffect
from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import ComboEffect


class Player:

    def TakeDamage(self, DamageAmount : int) -> None:
        """
        This function will update the HP value of the players and will kill the player if its HP goes under 0

        Args:
            DamageAmount (int): Total damage the player is taking
        """
        input(str(self.JobEnum) + " took " + str(DamageAmount))

        residual_damage = self.ShieldValue - DamageAmount
        # damage that goes through the shield (if any) will then be substracted to the HP
        # If there is still damage to do, residual_damage < 0. Otherwise it is positive
        self.HP -= max(0, -1 * residual_damage)

        if self.HP <= 0: self.TrueLock = True # Killing the player. Not allowed to raise.

    def AddAction(self, actionObject) -> None:
        """
        This function will append the spell object actionObject to the player's action list.

        actionObject (Spell) : Action we wish to append

        """
        
        self.ActionSet.append(actionObject)

    def Set_etro_gearset(self, url : str) -> None:
        """This function takes an etro url and update/sets the player's stats according to the given URL

        Args:
            url (str): etro gear set url. Can be the whole thing or just the id at the end of the url.
        """

        self.Stat = get_gearset_data(url) # Updates the stats
        

    def __init__(self, ActionSet, EffectList, Stat,Job : JobEnum):
        """
        Create the player object
        ActionSet : List[Spell] -> List of spell the player will do in the simulation
        EffectList : List[Function] -> List of all effects the player has. Can be empty.
        CurrentFight : Fight -> Reference to the fight object in which the player is.
        Stat : Dict -> Stats of the player as a dictionnary
        Job : JobEnum -> Specific job of the player
        """
        self.ActionSet = ActionSet # Known Action List
        self.EffectList = EffectList # Normally Empty, can has some effects initially
        self.RoleEnum = 0 # RoleEnum Value is set later on
        self.JobEnum = Job # JobEnum
        self.EffectCDList = [] # List of Effect for which we have to check if the have ended
        self.DOTList = [] # List of DOTs
        self.CastingSpell = []
        self.NextSpell = 0 # Index of next action in ActionSet
        self.CurrentFight = None # Reference to the fight the player is in. Set up when the player is added to a fight
        self.ManaTick = 1.5 # Starts Mana tick at this value
        self.playerID = 1 # Might not be necessary so by default 1
        self.Pet = None # Summoned Pet
        self.GCDCounter = 0 # Number of GCD done

        self.TrueLock = False   # Used to know when a player has finished all of its ActionSet
        self.NoMoreAction = False # Used to know when a player has no more actions to do. The user will have a choice to set TrueLock = True or to give anther action
        self.Casting = False    # Flag set to true if the player is casting
        self.oGCDLock = False   # If animation locked by oGCD
        self.GCDLock = False    # If have to wait for another GCD
        self.CastingLockTimer = 0 # How long we have to wait until next cast
        self.oGCDLockTimer = 0 # How long we have to wait until next oGCD
        self.GCDLockTimer = 0 # How long we have to wait until next GCD
        self.PotionTimer = 0 # Timer on the effect of potion
        self.Delay = 3 # Default time difference between AAs

        self.Mana = 10000 # Current mana. Max is 10'000
        self.HP = 2000  # Current HP
        self.MaxHP = 2000 # Starting HP
        self.ShieldValue = 0 # Value of shielding applied on the player
        self.EnemyDOT = [] # List which contains all DOT applied by the enemy on the player.
        self.TotalEnemity = 0 # Value of Enemity
        self.MagicMitigation = 1 # Current value of magic mitigation
        self.PhysicalMitigation = 1 # Current value of physical mitagation
        
        self.TotalPotency = 0 # Keeps track of total potency done
        self.TotalDamage = 0 # Keeps track of total damage done
        self.TotalMinDamage = 0 # Minimum expected damage (no crit or diret hit) 

        self.Stat = deepcopy(Stat) # Stats of the player

        self.auras = [] # List containing all Auras at the start of the fight

        self.Trait = 1  # DPS mult from trait
        self.buffList = []
        self.EffectToRemove = [] # List filled with effect to remove.
        self.EffectToAdd = [] # List that will add effect to the effectlist or effectcdlist once it has been gone through once

        self.ArcanumTimer = 0 # ArcanumTimer
        self.MeditativeBrotherhoodTimer = 0 # Meditative Brotherhood Timer
        self.OblationTimer = 0 # Oblation timer if its received
        self.TBNTimer = 0 # Timer if TBN is received
        self.CorundumTimer = 0 # Timer if corundum is given

        # Used for DPS graph and Potency/s graph

        self.DPSGraph = []
        self.PotencyGraph = []

        self.NumberDamageSpell = 0 # Number of damaging spell done, not including DOT and AA
        self.CritRateHistory = [] # History of crit rate, so we can average them at the end


        # functions for computing damage. Since the stats do not change (except MainStat), we can compute in advance
        # all functions that will not have their values changed
        # They will be computed at the begining of the simulation, they are now set at 0
        if Job != JobEnum.Pet: # Pet have these values given by the Master. So no need to set as 0
            self.f_WD = 0
            self.f_DET = 0
            self.f_TEN = 0
            self.f_SPD = 0
            self.CritRate = 0
            self.CritMult = 0
            self.DHRate = 0
            self.GCDReduction = 1 # Mult GCD reduction based on Spell Speed or Skill Speed (computed before fight)
            self.CritRateBonus = 0  # CritRateBonus
            self.DHRateBonus = 0 # DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus

        def ManaRegenCheck(Player, Enemy):  #This function is there by default
            if Player.ManaTick <= 0:
                Player.ManaTick = 3
                Player.Mana = min(10000, Player.Mana + 200)

        if Job != JobEnum.BlackMage : self.EffectCDList.append(ManaRegenCheck) # If not blackmage since they have different mana regen


        # Will now find the class and job so we can initialize the other specific fields

        # Finding Job

        match self.JobEnum:
            case JobEnum.BlackMage:
                self.RoleEnum = RoleEnum.Caster
                self.init_blackmage()
            case JobEnum.RedMage:
                self.RoleEnum = RoleEnum.Caster
                self.init_redmage()
            case JobEnum.Summoner:
                self.RoleEnum = RoleEnum.Caster
                self.init_summoner()
            case JobEnum.Scholar:
                self.RoleEnum = RoleEnum.Healer
                self.init_scholar()
            case JobEnum.WhiteMage:
                self.RoleEnum = RoleEnum.Healer
                self.init_whitemage()
            case JobEnum.Astrologian:
                self.RoleEnum = RoleEnum.Healer
                self.init_astrologian()
            case JobEnum.Sage:
                self.RoleEnum = RoleEnum.Healer
                self.init_sage()
            case JobEnum.Monk:
                self.RoleEnum = RoleEnum.Melee
                self.init_monk()
            case JobEnum.Ninja:
                self.RoleEnum = RoleEnum.Melee
                self.init_ninja()
            case JobEnum.Dragoon:
                self.RoleEnum = RoleEnum.Melee
                self.init_dragoon()
            case JobEnum.Samurai:
                self.RoleEnum = RoleEnum.Melee
                self.init_samurai()
            case JobEnum.Reaper:
                self.RoleEnum = RoleEnum.Melee
                self.init_reaper()
            case JobEnum.Machinist:
                self.RoleEnum = RoleEnum.PhysicalRanged
                self.init_machinist()
            case JobEnum.Bard:
                self.RoleEnum = RoleEnum.PhysicalRanged
                self.init_bard()
            case JobEnum.Dancer:
                self.RoleEnum = RoleEnum.PhysicalRanged
                self.init_dancer()
            case JobEnum.DarkKnight:
                self.RoleEnum = RoleEnum.Tank
                self.init_darkknight()
            case JobEnum.Gunbreaker:
                self.RoleEnum = RoleEnum.Tank
                self.init_gunbreaker()
            case JobEnum.Warrior:
                self.RoleEnum = RoleEnum.Tank
                self.init_warrior()
            case JobEnum.Paladin:
                self.RoleEnum = RoleEnum.Tank
                self.init_paladin()
            case JobEnum.Pet:
                self.RoleEnum = RoleEnum.Pet
                return # Exit the init function


                # Finding Role

        match self.RoleEnum:
            case RoleEnum.Tank:
                self.init_tank()
            case RoleEnum.Healer:
                self.init_healer()
            case RoleEnum.Caster:
                self.init_caster()
            case RoleEnum.Melee:
                self.init_melee()
            case RoleEnum.PhysicalRanged:
                self.init_physicalranged()

    # The functions under here will be called to initialize the Role and/or Job

    # update functions

    def updateTimer(self, time : float) -> None:
        """
        Updates the base timer of the player and calls the specific to the role and job update timer function
        time : float -> unit by which we update the timers
        """
        if (self.GCDLockTimer > 0) : self.GCDLockTimer = max(0, self.GCDLockTimer-time)
        if (self.oGCDLockTimer > 0) : self.oGCDLockTimer = max(0, self.oGCDLockTimer-time)
        if (self.CastingLockTimer > 0) : self.CastingLockTimer = max(0, self.CastingLockTimer-time)
        if (self.ManaTick > 0) : self.ManaTick = max(0, self.ManaTick-time)
        if (self.ArcanumTimer > 0) : self.ArcanumTimer = max(0, self.ArcanumTimer-time)
        if (self.PotionTimer > 0) : self.PotionTimer = max(0, self.PotionTimer-time)
        if (self.MeditativeBrotherhoodTimer > 0) : self.MeditativeBrotherhoodTimer = max(0, self.MeditativeBrotherhoodTimer-time)
        if (self.OblationTimer > 0) : self.OblationTimer = max(0, self.OblationTimer-time)
        if (self.TBNTimer > 0) : self.TBNTimer = max(0, self.TBNTimer-time)
        if (self.CorundumTimer > 0) : self.CorundumTimer = max(0, self.CorundumTimer-time)

        # Will now call the Role and Job update functions
        self.updateRoleTimer(self, time)
        self.updateJobTimer(self, time)
    
    def updateCD(self, time : float):
        """
        Updates the base timer of the player and calls the specific to the role and job update CD function
        time : float -> unit by which we update the timers
        """
        self.updateJobCD(self, time)
        self.updateRoleCD(self, time)

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

    # Roles

    def init_caster(self):
        #Shared ressources across casters
        
        #CD
        self.SwiftcastCD = 0
        self.LucidDreamingCD = 0
        self.SurecastCD = 0
        self.AddleCD = 0

        #Timer
        self.LucidDreamingTimer = 0

        #jobmod
        self.JobMod = 115

        #trait
        self.Trait = 1.3 #magik and mend

        #ActionEnum
        self.ClassAction = CasterActions
    
        def updateCD(self, time : float):
            if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)
            if (self.AddleCD > 0) : self.AddleCD = max(0,self.AddleCD - time)

        def updateTimer(self, time : float):
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

        self.updateRoleCD = updateCD
        self.updateRoleTimer = updateTimer

    def init_healer(self):
        #Shared ressources across casters

        #CD
        self.SurecastCD = 0
        self.RescueCD = 0
        self.SwiftcastCD = 0
        self.LucidDreamingCD = 0

        
        #Timer
        self.LucidDreamingTimer = 0

        #JobMod
        self.JobMod = 115

        #Trait
        self.Trait = 1.3 #Magik and mend

        #ActionEnum
        self.ClassAction = HealerActions
    
        def updateCD(self, time : float):
            if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.RescueCD > 0) : self.RescueCD = max(0,self.RescueCD - time)
            if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)

        def updateTimer(self, time : float):
            
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

        self.updateRoleCD = updateCD
        self.updateRoleTimer = updateTimer

    def init_melee(self):
        #Shared ressources across melees

        #self.TrueNorthStack = 2

        #CD
        self.SecondWindCD = 0 #120 sec
        self.LegSweepCD = 0 #40s 
        self.BloodbathCD = 0 #90s
        self.FeintCD = 0 #90
        self.ArmLengthCD = 0 #120s
        self.TrueNorthCD = 0 #45s, but 2 stacks

        #Stacks
        self.TrueNorthStack = 2
        
        #Trait
        self.Trait = 1

        #ActionEnum
        self.ClassAction = MeleeActions
    
        def updateCD(self, time : float):
            if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
            if (self.LegSweepCD > 0) : self.LegSweepCD = max(0,self.LegSweepCD - time)
            if (self.BloodbathCD > 0) : self.BloodbathCD = max(0,self.BloodbathCD - time)
            if (self.FeintCD > 0) : self.FeintCD = max(0,self.FeintCD - time)
            if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)
            if (self.TrueNorthCD > 0) : self.TrueNorthCD = max(0,self.TrueNorthCD - time)

        def updateTimer(self, time : float):
            pass

        self.updateRoleCD = updateCD
        self.updateRoleTimer = updateTimer

    def init_tank(self):
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

        #Timer
        self.BigMitTimer = 0
        self.RampartTimer = 0

        #ActionEnum
        self.ClassAction = TankActions
    
        def updateCD(self, time : float):
            if (self.RampartCD > 0) : self.RampartCD = max(0,self.RampartCD - time)
            if (self.LowBlowCD > 0) : self.LowBlowCD = max(0,self.LowBlowCD - time)
            if (self.ProvokeCD > 0) : self.ProvokeCD = max(0,self.ProvokeCD - time)
            if (self.InterjectCD > 0) : self.InterjectCD = max(0,self.InterjectCD - time)
            if (self.ShirkCD > 0) : self.ShirkCD = max(0,self.ShirkCD - time)
            if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)
            if (self.ReprisalCD > 0) : self.ReprisalCD = max(0,self.ReprisalCD - time)
            if (self.BigMitCD > 0) : self.BigMitCD = max(0,self.BigMitCD - time)
            if (self.TankStanceCD > 0) : self.TankStanceCD = max(0,self.TankStanceCD - time)

        def updateTimer(self, time : float):
            if (self.BigMitTimer > 0) : self.BigMitTimer = max(0,self.BigMitTimer - time)
            if (self.RampartTimer > 0) : self.RampartTimer = max(0,self.RampartTimer - time)

        self.updateRoleCD = updateCD
        self.updateRoleTimer = updateTimer

    def init_physicalranged(self):
        #Shared ressources across melees
        #CD
        self.LegGrazeCD = 0
        self.SecondWindCD = 0
        self.FootGrazeCD = 0
        self.PelotonCD = 0
        self.HeadGrazeCD = 0
        self.ArmLengthCD = 0

        #JobMod
        self.JobMod = 115

        #trait
        self.Trait = 1.2 #Common to all phys ranged

        #ActionEnum
        self.ClassAction = RangedActions
    
        def updateCD(self, time : float):
            if (self.LegGrazeCD > 0) : self.LegGrazeCD = max(0,self.LegGrazeCD - time)
            if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
            if (self.FootGrazeCD > 0) : self.FootGrazeCD = max(0,self.FootGrazeCD - time)
            if (self.PelotonCD > 0) : self.PelotonCD = max(0,self.PelotonCD - time)
            if (self.HeadGrazeCD > 0) : self.HeadGrazeCD = max(0,self.HeadGrazeCD - time)
            if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)

        def updateTimer(self, time : float):
            pass

        self.updateRoleCD = updateCD
        self.updateRoleTimer = updateTimer

    # Jobs

    def init_blackmage(self):

        self.EffectList = [EnochianEffect, ElementalEffect] # Adding effects

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
        self.SharpCast = False

        #CD
        self.TransposeCD = 0
        self.AmplifierCD = 0
        self.LeyLinesCD = 0
        self.TripleCastCD = 0
        self.SharpCastCD = 0
        self.ManafrontCD = 0
        self.ManawardCD = 0

        #Timer
        self.PolyglotTimer = 0
        self.EnochianTimer = 0
        self.LeyLinesTimer = 0
        self.Thunder3DOTTimer = 0
        self.Thunder4DOTTimer = 0

        #DOT
        self.Thunder3DOT = None
        self.Thunder4DOT = None

        #ActionEnum
        self.JobAction = BlackMageActions


        def updateCD(self, time):
            if (self.TransposeCD > 0) : self.TransposeCD = max(0,self.TransposeCD - time)
            if (self.AmplifierCD > 0) : self.AmplifierCD = max(0,self.AmplifierCD - time)
            if (self.LeyLinesCD > 0) : self.LeyLinesCD = max(0,self.LeyLinesCD - time)
            if (self.TripleCastCD > 0) : self.TripleCastCD = max(0,self.TripleCastCD - time)
            if (self.SharpCastCD > 0) : self.SharpCastCD = max(0,self.SharpCastCD - time)
            if (self.ManafrontCD > 0) : self.ManafrontCD = max(0,self.ManafrontCD - time)
            if (self.ManawardCD > 0) : self.ManawardCD = max(0,self.ManawardCD - time)

        def updateTimer(self, time):
            if (self.PolyglotTimer > 0) : self.PolyglotTimer = max(0,self.PolyglotTimer - time)
            if (self.EnochianTimer > 0) : self.EnochianTimer = max(0,self.EnochianTimer - time)
            if (self.LeyLinesTimer > 0) : self.LeyLinesTimer = max(0,self.LeyLinesTimer - time)
            if (self.Thunder3DOTTimer > 0) : self.Thunder3DOTTimer = max(0,self.Thunder3DOTTimer - time)
            if (self.Thunder4DOTTimer > 0) : self.Thunder4DOTTimer = max(0,self.Thunder4DOTTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

        def BLMManaRegenCheck(Player, Enemy):   #Mana Regen Stuff
            if Player.ManaTick <= 0:
                Player.ManaTick = 3
                if Player.ElementalGauge < 0:
                    if(Player.ElementalGauge == -1):
                        #input("adding 3200")
                        Player.Mana = min(10000, Player.Mana + 3200)
                    if(Player.ElementalGauge == -2):
                        #input("adding 4700")
                        Player.Mana = min(10000, Player.Mana + 4700)
                    if(Player.ElementalGauge == -3):
                        #input("adding 6200")
                        Player.Mana = min(10000, Player.Mana + 6200)

        self.EffectCDList.append(BLMManaRegenCheck) #Mana regen

    def init_redmage(self):

        self.EffectList = [DualCastEffect]

        #mana
        self.BlackMana = 0
        self.WhiteMana = 0
        
        #CD
        self.EmboldenCD = 0
        self.ManaficationCD = 0
        self.LucidDreamingCD = 0
        self.AccelerationCD = 0
        self.FlecheCD = 0
        self.ContreCD = 0
        self.EngagementCD = 0
        self.CorpsCD = 0
        self.MagickBarrierCD = 0

        #Timer
        self.EmboldenTimer = 0
        self.ManaficationTimer = 0

        #stack
        self.AccelerationStack = 2
        self.EngagementStack = 2
        self.CorpsStack = 2
        self.ManaStack = 0 #Used for Melee Combo finisher

        self.DualCast = False #True if DualCast cast


        #ComboAction

        self.Zwerchhau = False #If can execute
        self.Redoublement = False
        self.Verholy = False
        self.Scorch = False
        self.Resolution = False

        # Procs
        self.ExpectedVerfireProc = 0
        self.UsedVerfireProc = 0
        self.ExpectedVerstoneProc = 0
        self.UsedVerstoneProc = 0

        #ActionEnum
        self.JobAction = RedMageActions


        def updateCD(self, time : float):
            
            if (self.EmboldenCD > 0) : self.EmboldenCD = max(0,self.EmboldenCD - time)
            if (self.ManaficationCD > 0) : self.ManaficationCD = max(0,self.ManaficationCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.AccelerationCD > 0) : self.AccelerationCD = max(0,self.AccelerationCD - time)
            if (self.FlecheCD > 0) : self.FlecheCD = max(0,self.FlecheCD - time)
            if (self.ContreCD > 0) : self.ContreCD = max(0,self.ContreCD - time)
            if (self.EngagementCD > 0) : self.EngagementCD = max(0,self.EngagementCD - time)
            if (self.CorpsCD > 0) : self.CorpsCD = max(0,self.CorpsCD - time)
            if (self.MagickBarrierCD > 0) : self.MagickBarrierCD = max(0,self.MagickBarrierCD - time)


        def updateTimer(self, time : float):
            
            if (self.EmboldenTimer > 0) : self.EmboldenTimer = max(0,self.EmboldenTimer - time)
            if (self.ManaficationTimer > 0) : self.ManaficationTimer = max(0,self.ManaficationTimer - time)
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_summoner(self):
        #Gauge
        self.AetherflowGauge = 0

        #Trance
        self.FirebirdTrance = False #Birdy
        self.DreadwyrmTrance = False #Bahamut
        self.LastTranceBahamut = False #If false, next trance is bahamut. If true, next trance is phoenix

        #Primal Stacks
        self.GarudaStack = 0
        self.IfritStack = 0
        self.TitanStack = 0

        #Gems Stack (For summoning Primals)
        self.TitanGem = False
        self.GarudaGem = False
        self.IfritGem = False

        #Primal Special Attack
        self.GarudaSpecial = False
        self.IfritSpecial = False
        self.IfritSpecialCombo = False
        self.TitanSpecial = False

        #CD
        self.TranceCD = 0
        self.SearingLightCD = 0
        self.EnergyDrainCD = 0
        self.SummonCD = 0

        #buff
        self.FurtherRuin = False #Used for Ruin IV
        self.Enkindle = False
        self.Deathflare = False #Used for deathflare

        #Timer
        self.TranceTimer = 0
        self.SearingLightTimer = 0
        self.SlipstreamDOTTimer = 0
        self.SummonDOTTimer = 0

        #DOT
        self.SlipstreamDOT = None
        self.SummonDOT = None

        #Summon
        self.Summon = None

        #ActionEnum
        self.JobAction = SummonerActions

        def updateCD(self, time : float):
            
            if (self.TranceCD > 0) : self.TranceCD = max(0,self.TranceCD - time)
            if (self.SearingLightCD > 0) : self.SearingLightCD = max(0,self.SearingLightCD - time)
            if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
            if (self.SummonCD > 0) : self.SummonCD = max(0,self.SummonCD - time)


        def updateTimer(self, time : float):
            
            if (self.TranceTimer > 0) : self.TranceTimer = max(0,self.TranceTimer - time)
            if (self.SearingLightTimer > 0) : self.SearingLightTimer = max(0,self.SearingLightTimer - time)
            if (self.SlipstreamDOTTimer > 0) : self.SlipstreamDOTTimer = max(0,self.SlipstreamDOTTimer - time)
            if (self.SummonDOTTimer > 0) : self.SummonDOTTimer = max(0,self.SummonDOTTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_whitemage(self):
        #Stack
        self.LilyStack = 0
        self.BloomLily = False
        self.UsedLily = 0

        #CD
        self.LucidDreamingCD = 0
        self.AssizeCD = 0
        self.ThinAirCD = 0
        self.PresenceOfMindCD = 0
        self.BellCD = 0
        self.AquaveilCD = 0
        self.TemperanceCD = 0
        self.PlanetyIndulgenceCD = 0
        self.DivineBenisonCD = 0
        self.TetragrammatonCD = 0
        self.AsylumCD = 0
        self.BenedictionCD = 0


        #Timer
        self.DiaTimer = 0
        self.LucidDreamingTimer = 0
        self.PresenceOfMindTimer = 0
        self.LilyTimer = 40 #Initiated at 40 sec since we have 20 sec CD

        #DOT
        self.Dia = None

        #ActionEnum
        self.JobAction = WhiteMageActions


        def updateCD(self, time : float):
            
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.AssizeCD > 0) : self.AssizeCD = max(0,self.AssizeCD - time)
            if (self.ThinAirCD > 0) : self.ThinAirCD = max(0,self.ThinAirCD - time)
            if (self.PresenceOfMindCD > 0) : self.PresenceOfMindCD = max(0,self.PresenceOfMindCD - time)
            if (self.BellCD > 0) : self.BellCD = max(0,self.BellCD - time)
            if (self.AquaveilCD > 0) : self.AquaveilCD = max(0,self.AquaveilCD - time)
            if (self.TemperanceCD > 0) : self.TemperanceCD = max(0,self.TemperanceCD - time)
            if (self.PlanetyIndulgenceCD > 0) : self.PlanetyIndulgenceCD = max(0,self.PlanetyIndulgenceCD - time)
            if (self.DivineBenisonCD > 0) : self.DivineBenisonCD = max(0,self.DivineBenisonCD - time)
            if (self.TetragrammatonCD > 0) : self.TetragrammatonCD = max(0,self.TetragrammatonCD - time)
            if (self.AsylumCD > 0) : self.AsylumCD = max(0,self.AsylumCD - time)
            if (self.BenedictionCD > 0) : self.BenedictionCD = max(0,self.BenedictionCD - time)

        def updateTimer(self, time : float):
            
            if (self.DiaTimer > 0) : self.DiaTimer = max(0,self.DiaTimer - time)
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
            if (self.PresenceOfMindTimer > 0) : self.PresenceOfMindTimer = max(0,self.PresenceOfMindTimer - time)
            if (self.LilyTimer > 0) : self.LilyTimer = max(0,self.LilyTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

        def LilyCheck(Player, Enemy):
            if Player.LilyTimer <= 0:
                Player.LilyStack = min(3, Player.LilyStack + 1)
                Player.LilyTimer = 20 #Reset Timer
                
        self.EffectCDList.append(LilyCheck) #Starting with this check

    def init_scholar(self):
        #Stack
        self.AetherFlowStack = 0
        self.ConsolationStack = 0
        #CD
        self.AetherFlowCD = 0
        self.ChainStratagemCD = 0
        self.EnergyDrainCD = 0
        self.LucidDreamingCD = 0
        self.DissipationCD = 0
        self.ExpedientCD = 0
        self.ExpedientCD = 0
        self.ProtractionCD = 0
        self.RecitationCD = 0
        self.EmergencyTacticCD = 0
        self.DeploymentTacticCD = 0
        self.ExcogitationCD = 0
        self.SacredSoilCD = 0
        self.LustrateCD = 0
        self.IndomitabilityCD = 0
        self.SummonSeraphCD = 0
        self.FeyIlluminationCD = 0
        self.FeyBlessingCD = 0
        self.WhisperingDawnCD = 0
        #Timer
        self.BiolysisTimer = 0
        self.LucidDreamingTimer = 0
        self.ChainStratagemTimer = 0
        self.SummonTimer = 0
        #DOT
        self.Biolysis = None
        #Buff
        self.Recitation = True #True if we have it

        #ActionEnum
        self.JobAction = ScholarActions

        def updateCD(self, time : float):
            
            if (self.AetherFlowCD > 0) : self.AetherFlowCD = max(0,self.AetherFlowCD - time)
            if (self.ChainStratagemCD > 0) : self.ChainStratagemCD = max(0,self.ChainStratagemCD - time)
            if (self.EnergyDrainCD > 0) : self.EnergyDrainCD = max(0,self.EnergyDrainCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.DissipationCD > 0) : self.DissipationCD = max(0,self.DissipationCD - time)
            if (self.ExpedientCD > 0) : self.ExpedientCD = max(0,self.ExpedientCD - time)
            if (self.ProtractionCD > 0) : self.ProtractionCD = max(0,self.ProtractionCD - time)
            if (self.RecitationCD > 0) : self.RecitationCD = max(0,self.RecitationCD - time)
            if (self.EmergencyTacticCD > 0) : self.EmergencyTacticCD = max(0,self.EmergencyTacticCD - time)
            if (self.DeploymentTacticCD > 0) : self.DeploymentTacticCD = max(0,self.DeploymentTacticCD - time)
            if (self.ExcogitationCD > 0) : self.ExcogitationCD = max(0,self.ExcogitationCD - time)
            if (self.SacredSoilCD > 0) : self.SacredSoilCD = max(0,self.SacredSoilCD - time)
            if (self.LustrateCD > 0) : self.LustrateCD = max(0,self.LustrateCD - time)
            if (self.IndomitabilityCD > 0) : self.IndomitabilityCD = max(0,self.IndomitabilityCD - time)
            if (self.SummonSeraphCD > 0) : self.SummonSeraphCD = max(0,self.SummonSeraphCD - time)
            if (self.FeyIlluminationCD > 0) : self.FeyIlluminationCD = max(0,self.FeyIlluminationCD - time)
            if (self.FeyBlessingCD > 0) : self.FeyBlessingCD = max(0,self.FeyBlessingCD - time)
            if (self.WhisperingDawnCD > 0) : self.WhisperingDawnCD = max(0,self.WhisperingDawnCD - time)

        def updateTimer(self, time : float):
            
            if (self.BiolysisTimer > 0) : self.BiolysisTimer = max(0,self.BiolysisTimer - time)
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)
            if (self.ChainStratagemTimer > 0) : self.ChainStratagemTimer = max(0,self.ChainStratagemTimer - time)
            if (self.SummonTimer > 0) : self.SummonTimer = max(0,self.SummonTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_astrologian(self):
        #Stack
        self.DrawStack = 2
        self.EssentialDignityStack = 2
        self.CelestialIntersectionStack = 2
        #Gauge
        self.Lunar = False #Balance and Bole
        self.Solar = False #Arrow and Ewer
        self.Celestial = False #Spear and Spire
        self.HasCard = True #Assumed to True since we can just draw before. Easier for Pre Pull
        self.Redraw = False #True if we can redraw

        #Buff
        self.LordOfCrown = False

        #CD
        self.LightspeedCD = 0
        self.DivinationCD = 0
        self.MinorArcanaCD = 0
        self.DrawCD = 0
        self.MacrocosmosCD = 0
        self.ExaltationCD = 0
        self.NeutralSectCD = 0
        self.HoroscopeCD = 0
        self.CelestialIntersectionCD = 0
        self.EarthlyStarCD = 0
        self.CelestialOppositionCD = 0
        self.CollectiveCD = 0 #Collective Uncounscious
        self.SynastryCD = 0
        self.EssentialDignityCD = 0

        #timer
        self.CumbustDOTTimer = 0
        self.LightspeedTimer = 0
        self.DivinationTimer = 0
        self.BodyTimer = 0

        #DOT
        self.CumbustDOT = None

        #ActionEnum
        self.JobAction = AstrologianActions



        def updateCD(self, time : float):
            
            if (self.LightspeedCD > 0) : self.LightspeedCD = max(0,self.LightspeedCD - time)
            if (self.DivinationCD > 0) : self.DivinationCD = max(0,self.DivinationCD - time)
            if (self.MinorArcanaCD > 0) : self.MinorArcanaCD = max(0,self.MinorArcanaCD - time)
            if (self.DrawCD > 0) : self.DrawCD = max(0,self.DrawCD - time)
            if (self.MacrocosmosCD > 0) : self.MacrocosmosCD = max(0,self.MacrocosmosCD - time)
            if (self.ExaltationCD > 0) : self.ExaltationCD = max(0,self.ExaltationCD - time)
            if (self.NeutralSectCD > 0) : self.NeutralSectCD = max(0,self.NeutralSectCD - time)
            if (self.HoroscopeCD > 0) : self.HoroscopeCD = max(0,self.HoroscopeCD - time)
            if (self.CelestialIntersectionCD > 0) : self.CelestialIntersectionCD = max(0,self.CelestialIntersectionCD - time)
            if (self.EarthlyStarCD > 0) : self.EarthlyStarCD = max(0,self.EarthlyStarCD - time)
            if (self.CelestialOppositionCD > 0) : self.CelestialOppositionCD = max(0,self.CelestialOppositionCD - time)
            if (self.CollectiveCD > 0) : self.CollectiveCD = max(0,self.CollectiveCD - time)
            if (self.SynastryCD > 0) : self.SynastryCD = max(0,self.SynastryCD - time)

        def updateTimer(self, time : float):
            
            if (self.CumbustDOTTimer > 0) : self.CumbustDOTTimer = max(0,self.CumbustDOTTimer - time)
            if (self.LightspeedTimer > 0) : self.LightspeedTimer = max(0,self.LightspeedTimer - time)
            if (self.DivinationTimer > 0) : self.DivinationTimer = max(0,self.DivinationTimer - time)
            if (self.BodyTimer > 0) : self.BodyTimer = max(0,self.BodyTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_sage(self):
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
        self.AddersgallTimer = 0 #Starting at 40 since 20 sec countdown
        self.PhlegmaTimer = 0
        #DOT
        self.Eukrasian = None

        #Stack
        self.PhlegmaStack = 2
        self.AdderstingStack = 0

        #ActionEnum
        self.JobAction = SageActions


        def updateCD(self, time : float):
            
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

        def updateTimer(self, time : float):
            
            if (self.EukrasianTimer > 0) : self.EukrasianTimer = max(0,self.EukrasianTimer - time)
            if (self.AddersgallTimer > 0) : self.AddersgallTimer = max(0,self.AddersgallTimer - time)
            if (self.PhlegmaTimer > 0) : self.PhlegmaTimer = max(0,self.PhlegmaTimer - time)

        def AddersgallCheck(Player, Enemy):
            if Player.AddersgallTimer <= 0:
                Player.AddersgallStack = min(3, Player.AddersgallStack + 1)
                Player.AddersgallTimer = 0

        self.EffectCDList.append(AddersgallCheck)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_machinist(self):
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
        self.AutomatonQueenCD = 0
        self.FlamethrowerCD = 0
        self.TacticianCD = 0

        #Timer
        self.WildFireTimer = 0
        self.HyperchargeTimer = 0
        self.BioblasterDOTTimer = 0
        self.FlamethrowerDOTTimer = 0
        self.QueenStartUpTimer = 0
        self.QueenTimer = 0

        #Stacks
        self.GaussRoundStack = 3
        self.ReassembleStack = 2
        self.RicochetStack = 3
        self.WildFireStack = 0  #Used to know how many weaponskills have hit during Wildfire
        self.Reassemble = False

        #Combo Action
        self.SlugShot = False
        self.CleanShot = False

        #DOT
        self.BioblasterDOT = None
        self.FlamethrowerDOT = None

        #Queen
        self.Queen = None
        self.Overdrive = False  #Used to know if we can cast overdrive. Its set to true once the Queen is summoned and set to false when Overdrive is used
        self.QueenOnField = False

        #ActionEnum
        self.JobAction = MachinistActions

        

        def updateCD(self, time : float):
            
            if (self.ChainSawCD > 0) : self.ChainSawCD = max(0,self.ChainSawCD - time)
            if (self.AirAnchorCD > 0) : self.AirAnchorCD = max(0,self.AirAnchorCD - time)
            if (self.BarrelStabilizerCD > 0) : self.BarrelStabilizerCD = max(0,self.BarrelStabilizerCD - time)
            if (self.DrillCD > 0) : self.DrillCD = max(0,self.DrillCD - time)
            if (self.GaussRoundCD > 0) : self.GaussRoundCD = max(0,self.GaussRoundCD - time)
            if (self.WildFireCD > 0) : self.WildFireCD = max(0,self.WildFireCD - time)
            if (self.HotShotCD > 0) : self.HotShotCD = max(0,self.HotShotCD - time)
            if (self.HyperchargeCD > 0) : self.HyperchargeCD = max(0,self.HyperchargeCD - time)
            if (self.RicochetCD > 0) : self.RicochetCD = max(0,self.RicochetCD - time)
            if (self.AutomatonQueenCD > 0) : self.AutomatonQueenCD = max(0,self.AutomatonQueenCD - time)
            if (self.FlamethrowerCD > 0) : self.FlamethrowerCD = max(0,self.FlamethrowerCD - time)
            if (self.TacticianCD > 0) : self.TacticianCD = max(0,self.TacticianCD - time)

        def updateTimer(self, time : float):
            
            if (self.WildFireTimer > 0) : self.WildFireTimer = max(0,self.WildFireTimer - time)
            if (self.HyperchargeTimer > 0) : self.HyperchargeTimer = max(0,self.HyperchargeTimer - time)
            if (self.BioblasterDOTTimer > 0) : self.BioblasterDOTTimer = max(0,self.BioblasterDOTTimer - time)
            if (self.FlamethrowerDOTTimer > 0) : self.FlamethrowerDOTTimer = max(0,self.FlamethrowerDOTTimer - time)
            if (self.QueenStartUpTimer > 0) : self.QueenStartUpTimer = max(0,self.QueenStartUpTimer - time)
            if (self.QueenTimer > 0) : self.QueenTimer = max(0,self.QueenTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD
    
    def init_dancer(self):

        self.EffectList = [EspritEffect]

        #Gauge
        self.MaxFourfoldFeather = 0
        self.MaxEspritGauge = 0

        #Dancer Partner
        self.DancePartner = None


        #Used total proc
        self.UsedSilkenFlow = 0
        self.UsedSilkenSymettry = 0
        self.UsedFourfoldFeather = 0
        self.UsedThreefoldFan = 0



        #expected proc traking
        self.ExpectedSilkenSymettry = 0
        self.ExpectedSilkenFlow = 0
        self.ExpectedFourfoldFeather = 0
        self.ExpectedThreefoldFan = 0

        #buff
        self.NextDirectCrit = False #True if next 
        self.Dancing = False #True if dancing
        self.StandardFinishBuff = None
        self.TechnicalFinishBuff = None
        self.Improvising = False #True if improvising
        #Dance move
        self.Emboite = False
        self.Entrechat = False
        self.Jete = False
        self.Pirouette = False


        #AbilityReady
        self.SilkenSymettry = False
        self.SilkenFlow = False
        self.StandardFinish = False
        self.TechnicalFinish = False
        self.FlourishingFinish = False
        self.FlourishingStarfall = False
        #Flourish
        self.FlourishingSymettry = False
        self.FlourishingFlow = False
        self.ThreefoldFan = False
        self.FourfoldFan = False


        #CD
        self.StandardStepCD = 0
        self.TechnicalStepCD = 0
        self.DevilmentCD = 0
        self.FlourishCD = 0
        self.ClosedPositionCD = 0
        self.CuringWaltzCD = 0
        self.SambaCD = 0
        self.ImprovisationCD = 0

        #Timer
        self.StandardFinishTimer = 0
        self.TechnicalFinishTimer = 0
        self.DevilmentTimer = 0

        #ActionEnum
        self.JobAction = DancerActions


        def updateCD(self, time : float):
            
            if (self.StandardStepCD > 0) : self.StandardStepCD = max(0,self.StandardStepCD - time)
            if (self.TechnicalStepCD > 0) : self.TechnicalStepCD = max(0,self.TechnicalStepCD - time)
            if (self.DevilmentCD > 0) : self.DevilmentCD = max(0,self.DevilmentCD - time)
            if (self.FlourishCD > 0) : self.FlourishCD = max(0,self.FlourishCD - time)
            if (self.ClosedPositionCD > 0) : self.ClosedPositionCD = max(0,self.ClosedPositionCD - time)
            if (self.CuringWaltzCD > 0) : self.CuringWaltzCD = max(0,self.CuringWaltzCD - time)
            if (self.SambaCD > 0) : self.SambaCD = max(0,self.SambaCD - time)
            if (self.ImprovisationCD > 0) : self.ImprovisationCD = max(0,self.ImprovisationCD - time)


        def updateTimer(self, time : float):
            
            if (self.StandardFinishTimer > 0) : self.StandardFinishTimer = max(0,self.StandardFinishTimer - time)
            if (self.TechnicalFinishTimer > 0) : self.TechnicalFinishTimer = max(0,self.TechnicalFinishTimer - time)
            if (self.DevilmentTimer > 0) : self.DevilmentTimer = max(0,self.DevilmentTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_bard(self):

        self.EffectList = [SongEffect]

        #Expected Proc number
        self.ExpectedRefulgent = 0
        self.ExpectedRepertoire = 0
        self.ExpectedSoulVoiceGauge = 0
        self.ExpectedBloodLetterReduction = 0
        self.ExpectedTotalWandererRepertoire = 0
        self.ExpectedShadowbite = 0

        #Used proc
        self.UsedRefulgent = 0
        self.UsedRepertoire = 0 #Only relevant for Wanderer and pitch perfect
        self.UsedSoulVoiceGauge = 0
        self.UsedBloodLetterReduction = 0
        self.UsedRepertoireAdd = 0 #This is repertoire stacks we used more than the expected value
        self.UsedTotalWandererRepertoire = 0
        self.UsedShadowbite = 0


        #Gauge
        self.SoulVoiceGauge = 0
        self.Repertoire = 0
        self.MaximumRepertoire = 0 #Used for wanderer
        self.MaximumBloodLetterReduction = 0

        #Stack
        self.BloodLetterStack = 3


        #buff
        self.StraightShotReady = False
        self.BlastArrowReady = True
        self.ShadowbiteReady = False


        #Song
        self.MageBallad = False
        self.ArmyPaeon = False
        self.WandererMinuet = False

        #Coda
        self.MageCoda = False
        self.ArmyCoda = False
        self.WandererCoda = False


        #CD
        self.SidewinderCD = 0
        self.EmpyrealArrowCD = 0
        self.WandererMinuetCD = 0
        self.ArmyPaeonCD = 0
        self.MageBalladCD = 0
        self.BattleVoiceCD = 0
        self.BloodLetterCD = 0
        self.BarrageCD = 0
        self.RagingStrikeCD = 0
        self.TroubadourCD = 0
        self.WardenPaeanCD = 0
        self.NatureMinneCD = 0

        #Timer
        self.SongTimer = 0
        self.StormbiteDOTTimer = 0
        self.CausticbiteDOTTimer = 0
        self.BattleVoiceTimer = 0
        self.RagingStrikeTimer = 0
        self.RadiantFinaleTimer = 0

        #DOT
        self.StormbiteDOT = None
        self.CausticbiteDOT = None


        #DPSBonus
        self.RadiantFinalBuff = None

        #ActionEnum
        self.JobAction = BardActions
    
        def updateCD(self, time : float):
            
            if (self.SidewinderCD > 0) : self.SidewinderCD = max(0,self.SidewinderCD - time)
            if (self.EmpyrealArrowCD > 0) : self.EmpyrealArrowCD = max(0,self.EmpyrealArrowCD - time)
            if (self.WandererMinuetCD > 0) : self.WandererMinuetCD = max(0,self.WandererMinuetCD - time)
            if (self.ArmyPaeonCD > 0) : self.ArmyPaeonCD = max(0,self.ArmyPaeonCD - time)
            if (self.MageBalladCD > 0) : self.MageBalladCD = max(0,self.MageBalladCD - time)
            if (self.BattleVoiceCD > 0) : self.BattleVoiceCD = max(0,self.BattleVoiceCD - time)
            if (self.BloodLetterCD > 0) : self.BloodLetterCD = max(0,self.BloodLetterCD - time)
            if (self.BarrageCD > 0) : self.BarrageCD = max(0,self.BarrageCD - time)
            if (self.RagingStrikeCD > 0) : self.RagingStrikeCD = max(0,self.RagingStrikeCD - time)
            if (self.TroubadourCD > 0) : self.TroubadourCD = max(0,self.TroubadourCD - time)
            if (self.WardenPaeanCD > 0) : self.WardenPaeanCD = max(0,self.WardenPaeanCD - time)
            if (self.NatureMinneCD > 0) : self.NatureMinneCD = max(0,self.NatureMinneCD - time)

        def updateTimer(self, time : float):
            
            if (self.SongTimer > 0) : self.SongTimer = max(0,self.SongTimer - time)
            if (self.StormbiteDOTTimer > 0) : self.StormbiteDOTTimer = max(0,self.StormbiteDOTTimer - time)
            if (self.CausticbiteDOTTimer > 0) : self.CausticbiteDOTTimer = max(0,self.CausticbiteDOTTimer - time)
            if (self.BattleVoiceTimer > 0) : self.BattleVoiceTimer = max(0,self.BattleVoiceTimer - time)
            if (self.RagingStrikeTimer > 0) : self.RagingStrikeTimer = max(0,self.RagingStrikeTimer - time)
            if (self.RadiantFinaleTimer > 0) : self.RadiantFinaleTimer = max(0,self.RadiantFinaleTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_monk(self):

        self.EffectList = [ComboEffect]

        #Gauge
        self.CurrentForm = 0 #0 -> Nothing, 1 -> Opo-opo, 2 -> Raptor, 3 -> Coeurl, 4 -> Formless
        #After each execution of a relevant GCD, the form will be changed here.
        # Does action -> Changes form by Apply and adds FormChangeCheck -> Checks if any combo effect -> Effect removes itself
        # FormChangeCheck -> Changes form according to self.CurrentForm -> FormChangeCheck removes itself
        self.MasterGauge = [False,0,0,0,False]
        # This array will represent the master gauge
        # [Lunar Nadi, Chakra1, Chakra2, Chakra3, Solar Nadi]
        # For nadis, False -> closed, True -> open.
        # For chakras , 0 -> Empty, 1 -> Opo-opo, 2-> Raptor, 3-> Coeurl
        self.FormlessFistStack = 0 #Number of formless actions the player can do
        self.ExpectedChakraGate = 5 #This is a random value, so we will keep track of Expected, used value and maximum value
        self.MaxChakraGate = 5 #This is the one used to see if an action is even possible
        self.UsedChakraGate = 0 #Number of used Chakra Gates

        #Timer
        self.LeadenFistTimer = 0
        self.DisciplinedFistTimer = 0
        self.DemolishDOTTimer = 0
        self.BrotherhoodTimer = 0 #Brotherhood effectTimer
        self.RiddleOfFireTimer = 0
        self.RiddleOfWindTimer = 0
        
        #CD
        self.ThunderclapCD = 0
        self.MantraCD = 0
        self.PerfectBalanceCD = 0
        self.BrotherhoodCD = 0
        self.RiddleOfEarthCD = 0
        self.RiddleOfFireCD = 0
        self.RiddleOfWindCD = 0

        #DOT
        self.DemolishDOT = None

        #Stack
        self.ThunderclapStack = 3
        self.PerfectBalanceStack = 2
        self.RiddleOfEarthStack = 3
        self.PerfectBalanceEffectStack = 0

        #Guaranteed Crit
        self.GuaranteedCrit = False #Flag used to know if ability is a guaranteed crit

        self.UsedFormlessStack = False #Will remove effect at the end if set to true
        #JobMod
        self.JobMod = 110

        #ActionEnum
        self.JobAction = MonkActions

        def updateCD(self, time : float):
            
            if (self.ThunderclapCD > 0) : self.ThunderclapCD = max(0,self.ThunderclapCD - time)
            if (self.MantraCD > 0) : self.MantraCD = max(0,self.MantraCD - time)
            if (self.PerfectBalanceCD > 0) : self.PerfectBalanceCD = max(0,self.PerfectBalanceCD - time)
            if (self.BrotherhoodCD > 0) : self.BrotherhoodCD = max(0,self.BrotherhoodCD - time)
            if (self.RiddleOfEarthCD > 0) : self.RiddleOfEarthCD = max(0,self.RiddleOfEarthCD - time)
            if (self.RiddleOfFireCD > 0) : self.RiddleOfFireCD = max(0,self.RiddleOfFireCD - time)
            if (self.RiddleOfWindCD > 0) : self.RiddleOfWindCD = max(0,self.RiddleOfWindCD - time)


        def updateTimer(self, time : float):
            
            if (self.LeadenFistTimer  > 0) : self.LeadenFistTimer  = max(0,self.LeadenFistTimer - time)
            if (self.DisciplinedFistTimer  > 0) : self.DisciplinedFistTimer  = max(0,self.DisciplinedFistTimer - time)
            if (self.DemolishDOTTimer  > 0) : self.DemolishDOTTimer  = max(0,self.DemolishDOTTimer - time)
            if (self.BrotherhoodTimer  > 0) : self.BrotherhoodTimer  = max(0,self.BrotherhoodTimer - time)
            if (self.RiddleOfFireTimer  > 0) : self.RiddleOfFireTimer  = max(0,self.RiddleOfFireTimer - time)
            if (self.RiddleOfWindTimer  > 0) : self.RiddleOfWindTimer  = max(0,self.RiddleOfWindTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_reaper(self):
        #Gauge
        self.SoulGauge = 0
        self.ImmortalSacrificeStack = 0
        self.SoulReaverStack = 2
        self.ShroudGauge = 0
        self.LemureGauge = 0
        self.VoidShroudGauge = 0

        #Ready Effect


        #Stack
        self.SoulSliceStack = 2

        #CD
        self.SoulSliceCD = 0 #30 sec CD
        self.ArcaneCircleCD = 0 #120 sec CD
        self.GluttonyCD = 0 #60 sec CD
        self.EnshroudCD = 0 #15 sec CD
        self.HellIngressCD = 0 #20 sec CD
        self.ArcaneCrestCD = 0 # 30 sec CD


        #buff
        self.SoulSow = False #Has to be true to cast Harvest Moon
        self.EnhancedGibbet = False #Buffs Gibbet's Potency
        self.EnhancedGallows = False #Buffs Gallow's Potency

        #Timer
        self.DeathDesignTimer = 0
        self.ArcaneCircleTimer = 0 #on for 20 sec
        self.CircleOfSacrificeTimer = 5 #On for 5 sec
        self.AvatarTimer = 0 #Timer for summoning Avatar, used in Enshroud
        self.GallowsEffectTimer = 0 #Effect of Enhanced Gibbet
        self.GibbetEffectTimer = 0 #Effect of Enhanced Gallows
        self.BloodsownTimer = 0 #Timer before casting Plentiful Harvest
        self.VoidReapingTimer = 0 #timer of enhanced CrossReaping
        self.CrossReapingTimer = 0 #Timer of enhanced VoidReaping
        self.HellIngressTimer = 0 #Timer for insta-casting harpe


        self.JobMod = 115

        #ActionEnum
        self.JobAction = ReaperActions

        def updateCD(self, time : float):
            
            if (self.SoulSliceCD > 0) : self.SoulSliceCD = max(0,self.SoulSliceCD - time)
            if (self.ArcaneCircleCD > 0) : self.ArcaneCircleCD = max(0,self.ArcaneCircleCD - time)
            if (self.GluttonyCD > 0) : self.GluttonyCD = max(0,self.GluttonyCD - time)
            if (self.EnshroudCD > 0) : self.EnshroudCD = max(0,self.EnshroudCD - time)
            if (self.HellIngressCD > 0) : self.HellIngressCD = max(0,self.HellIngressCD - time)
            if (self.ArcaneCrestCD > 0) : self.ArcaneCrestCD = max(0,self.ArcaneCrestCD - time)


        def updateTimer(self, time : float):
            
            if (self.DeathDesignTimer > 0) : self.DeathDesignTimer = max(0,self.DeathDesignTimer - time)
            if (self.ArcaneCircleTimer > 0) : self.ArcaneCircleTimer = max(0,self.ArcaneCircleTimer - time)
            if (self.CircleOfSacrificeTimer > 0) : self.CircleOfSacrificeTimer = max(0,self.CircleOfSacrificeTimer - time)
            if (self.AvatarTimer > 0) : self.AvatarTimer = max(0,self.AvatarTimer - time)
            if (self.GallowsEffectTimer > 0) : self.GallowsEffectTimer = max(0,self.GallowsEffectTimer - time)
            if (self.GibbetEffectTimer > 0) : self.GibbetEffectTimer = max(0,self.GibbetEffectTimer - time)
            if (self.BloodsownTimer > 0) : self.BloodsownTimer = max(0,self.BloodsownTimer - time)
            if (self.VoidReapingTimer > 0) : self.VoidReapingTimer = max(0,self.VoidReapingTimer - time)
            if (self.CrossReapingTimer > 0) : self.CrossReapingTimer = max(0,self.CrossReapingTimer - time)
            if (self.HellIngressTimer > 0) : self.HellIngressTimer = max(0,self.HellIngressTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_samurai(self):
        #Buffs
        self.Fugetsu = False #13% DPS bonus
        self.Fuka = False #13% lest cast/recast time
        self.DirectCrit = False
        self.KaeshiHiganbana = False #True if we can cast
        self.KaeshiGoken = False #True if we can cast
        self.KaeshiSetsugekka = False #True if we can cast


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
        self.EnhancedEnpiTimer = 0
        

        #CD
        self.MeikyoCD = 0
        self.IkishotenCD = 0
        self.KaeshiCD = 0
        self.SeneiCD = 0
        self.ThirdEyeCD = 0
        self.GyotenCD = 0
        self.YatenCD = 0
        self.MeditateCD = 0
        self.KyutenCD = 0
        self.TsubamegaeshiCD = 0
        self.HagakureCD = 0
        
        #stack
        self.MeikyoStack = 2
        self.TsubamegaeshiStack = 2

        #EffectStack
        self.Meikyo = 0

        #DOT
        self.Higanbana = None

        #JobMod
        self.JobMod = 112

        #ActionEnum
        self.JobAction = SamuraiActions

        def updateCD(self, time : float):
            
            if (self.MeikyoCD > 0) : self.MeikyoCD = max(0,self.MeikyoCD - time)
            if (self.IkishotenCD > 0) : self.IkishotenCD = max(0,self.IkishotenCD - time)
            if (self.KaeshiCD > 0) : self.KaeshiCD = max(0,self.KaeshiCD - time)
            if (self.SeneiCD > 0) : self.SeneiCD = max(0,self.SeneiCD - time)
            if (self.ThirdEyeCD > 0) : self.ThirdEyeCD = max(0,self.ThirdEyeCD - time)
            if (self.GyotenCD > 0) : self.GyotenCD = max(0,self.GyotenCD - time)
            if (self.YatenCD > 0) : self.YatenCD = max(0,self.YatenCD - time)
            if (self.MeditateCD > 0) : self.MeditateCD = max(0,self.MeditateCD - time)
            if (self.KyutenCD > 0) : self.KyutenCD = max(0,self.KyutenCD - time)
            if (self.TsubamegaeshiCD > 0) : self.TsubamegaeshiCD = max(0,self.TsubamegaeshiCD - time)
            if (self.HagakureCD > 0) : self.HagakureCD = max(0,self.HagakureCD - time)
    

        def updateTimer(self, time : float):
            
            if (self.FugetsuTimer > 0) : self.FugetsuTimer = max(0,self.FugetsuTimer - time)
            if (self.FukaTimer > 0) : self.FukaTimer = max(0,self.FukaTimer - time)
            if (self.HiganbanaTimer > 0) : self.HiganbanaTimer = max(0,self.HiganbanaTimer - time)
            if (self.EnhancedEnpiTimer > 0) : self.EnhancedEnpiTimer = max(0,self.EnhancedEnpiTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_dragoon(self):
        #Special
        self.LanceMastery = False #Let us know if we are in Wheeling Thrust and FangAndClaw combo

        #Gauge
        self.DragonGauge = 0
        self.FirstmindGauge = 0
        #Stack
        self.SpineshafterStack = 2
        self.LifeSurgeStack = 2

        #Buff
        self.WheelInMotion = False
        self.FangAndClaw = False
        self.LifeOfTheDragon = False
        self.DiveReady = False
        self.DraconianFire = False
        #CD
        self.LanceChargeCD = 0
        self.BattleLitanyCD = 0
        self.DragonSightCD = 0
        self.GeirskogulCD = 0
        self.NastrondCD = 0
        self.HighJumpCD = 0
        self.SpineshafterCD = 0
        self.LifeSurgeCD = 0
        self.StardiverCD = 0
        self.DragonFireDiveCD = 0
        self.WyrmwindThrustCD = 0
        #Timer
        self.PowerSurgeTimer = 0
        self.ChaoticSpringDOTTimer = 0
        self.LanceChargeTimer = 0
        self.BattleLitanyTimer = 0
        self.DragonSightTimer = 0
        self.LifeOfTheDragonTimer = 0

        #DOT
        self.ChaoticSpringDOT = None

        #Next crit
        self.NextCrit = False

        #JobMod
        self.JobMod = 115

        #ActionEnum
        self.JobAction = DragoonActions

        def updateCD(self, time : float):
            
            if (self.LanceChargeCD > 0) : self.LanceChargeCD = max(0,self.LanceChargeCD - time)
            if (self.BattleLitanyCD > 0) : self.BattleLitanyCD = max(0,self.BattleLitanyCD - time)
            if (self.DragonSightCD > 0) : self.DragonSightCD = max(0,self.DragonSightCD - time)
            if (self.GeirskogulCD > 0) : self.GeirskogulCD = max(0,self.GeirskogulCD - time)
            if (self.NastrondCD > 0) : self.NastrondCD = max(0,self.NastrondCD - time)
            if (self.HighJumpCD > 0) : self.HighJumpCD = max(0,self.HighJumpCD - time)
            if (self.SpineshafterCD > 0) : self.SpineshafterCD = max(0,self.SpineshafterCD - time)
            if (self.LifeSurgeCD > 0) : self.LifeSurgeCD = max(0,self.LifeSurgeCD - time)
            if (self.StardiverCD > 0) : self.StardiverCD = max(0,self.StardiverCD - time)
            if (self.DragonFireDiveCD > 0) : self.DragonFireDiveCD = max(0,self.DragonFireDiveCD - time)
            if (self.WyrmwindThrustCD > 0) : self.WyrmwindThrustCD = max(0,self.WyrmwindThrustCD - time)
    

        def updateTimer(self, time : float):
            
            if (self.PowerSurgeTimer > 0) : self.PowerSurgeTimer = max(0,self.PowerSurgeTimer - time)
            if (self.ChaoticSpringDOTTimer > 0) : self.ChaoticSpringDOTTimer = max(0,self.ChaoticSpringDOTTimer - time)
            if (self.LanceChargeTimer > 0) : self.LanceChargeTimer = max(0,self.LanceChargeTimer - time)
            if (self.BattleLitanyTimer > 0) : self.BattleLitanyTimer = max(0,self.BattleLitanyTimer - time)
            if (self.DragonSightTimer > 0) : self.DragonSightTimer = max(0,self.DragonSightTimer - time)
            if (self.LifeOfTheDragonTimer > 0) : self.LifeOfTheDragonTimer = max(0,self.LifeOfTheDragonTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_ninja(self):
        #Gauge
        self.NinkiGauge = 0

        #buff
        self.Suiton = False
        self.Kassatsu = False
        self.Ten = False
        self.Chi = False
        self.Jin = False

        #Stack
        self.NinjutsuStack = 2
        self.RaijuStack = 0
        self.BunshinStack = 0

        #Ready
        self.RaijuReady = False
        self.PhantomKamaitachiReady = False
        

        #Timer
        self.HutonTimer = 0
        self.MugTimer = 0
        self.TrickAttackTimer = 0
        self.MeisuiTimer = 0
        self.KassatsuTimer = 0
        self.SuitonTimer = 0
        self.PhantomKamaitachiReadyTimer = 0
        self.TenChiJinTimer = 0
        self.DotonTimer = 0

        #CD
        self.DreamWithinADreamCD = 0
        self.MugCD = 0
        self.TrickAttackCD = 0
        self.MeisuiCD = 0
        self.NinjutsuCD = 0
        self.KassatsuCD = 0
        self.TenChiJinCD = 0
        self.BunshinCD = 0
        self.ShadeShiftCD = 0

        #Ninjutsu
        self.CurrentRitual = [] #List of currently done ritual
        self.TenChiJinRitual = [] #List of Ritual's done in TenChiJin

        #DOT
        self.DotonDOT = None

        #JobMod
        self.JobMod = 110

        #Shadow 
        self.Shadow = None #Pointer to Shadow object

        #ActionEnum
        self.JobAction = NinjaActions


        def updateCD(self, time : float):
            
            if (self.DreamWithinADreamCD > 0) : self.DreamWithinADreamCD = max(0,self.DreamWithinADreamCD - time)
            if (self.MugCD > 0) : self.MugCD = max(0,self.MugCD - time)
            if (self.TrickAttackCD > 0) : self.TrickAttackCD = max(0,self.TrickAttackCD - time)
            if (self.MeisuiCD > 0) : self.MeisuiCD = max(0,self.MeisuiCD - time)
            if (self.NinjutsuCD > 0) : self.NinjutsuCD = max(0,self.NinjutsuCD - time)
            if (self.KassatsuCD > 0) : self.KassatsuCD = max(0,self.KassatsuCD - time)
            if (self.TenChiJinCD > 0) : self.TenChiJinCD = max(0,self.TenChiJinCD - time)
            if (self.BunshinCD > 0) : self.BunshinCD = max(0,self.BunshinCD - time)
            if (self.ShadeShiftCD > 0) : self.ShadeShiftCD = max(0,self.ShadeShiftCD - time)
    

        def updateTimer(self, time : float):
            
            if (self.HutonTimer > 0) : self.HutonTimer = max(0,self.HutonTimer - time)
            if (self.MugTimer > 0) : self.MugTimer = max(0,self.MugTimer - time)
            if (self.TrickAttackTimer > 0) : self.TrickAttackTimer = max(0,self.TrickAttackTimer - time)
            if (self.MeisuiTimer > 0) : self.MeisuiTimer = max(0,self.MeisuiTimer - time)
            if (self.KassatsuTimer > 0) : self.KassatsuTimer = max(0,self.KassatsuTimer - time)
            if (self.SuitonTimer > 0) : self.SuitonTimer = max(0,self.SuitonTimer - time)
            if (self.PhantomKamaitachiReadyTimer > 0) : self.PhantomKamaitachiReadyTimer = max(0,self.PhantomKamaitachiReadyTimer - time)
            if (self.TenChiJinTimer > 0) : self.TenChiJinTimer = max(0,self.TenChiJinTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_gunbreaker(self):
        #Stack
        self.RoughDivideStack = 2
        self.AuroraStack = 2
        #Gauge
        self.PowderGauge = 0

        #ComboAction
        self.ReadyToRip = False
        self.ReadyToTear = False
        self.ReadyToGouge = False
        self.ReadyToBlast = False

        #cd
        self.GnashingFangCD = 0
        self.BlastingZoneCD = 0
        self.BloodfestCD = 0
        self.DoubleDownCD = 0
        self.SonicBreakCD = 0
        self.BowShockCD = 0
        self.RoughDivideCD = 0
        self.NoMercyCD = 0
        self.AuroraCD = 0
        self.SuperbolideCD = 0
        self.HeartOfLightCD = 0
        self.HeartOfCorundumCD = 0
        self.CamouflageCD = 0

        #Timer
        self.BowShockTimer = 0
        self.SonicBreakTimer = 0
        self.NoMercyTimer = 0
        self.HeartOfLightTimer = 0
        self.CamouflageTimer = 0

        #DOT
        self.SonicBreakDOT = None
        self.BowShowDOT = None

        #JobMod
        self.JobMod = 100

        #ActionEnum
        self.JobAction = GunbreakerActions

        def updateCD(self, time : float):
            
            if (self.GnashingFangCD > 0) : self.GnashingFangCD = max(0,self.GnashingFangCD - time)
            if (self.BlastingZoneCD > 0) : self.BlastingZoneCD = max(0,self.BlastingZoneCD - time)
            if (self.BloodfestCD > 0) : self.BloodfestCD = max(0,self.BloodfestCD - time)
            if (self.DoubleDownCD > 0) : self.DoubleDownCD = max(0,self.DoubleDownCD - time)
            if (self.SonicBreakCD > 0) : self.SonicBreakCD = max(0,self.SonicBreakCD - time)
            if (self.BowShockCD > 0) : self.BowShockCD = max(0,self.BowShockCD - time)
            if (self.RoughDivideCD > 0) : self.RoughDivideCD = max(0,self.RoughDivideCD - time)
            if (self.NoMercyCD > 0) : self.NoMercyCD = max(0,self.NoMercyCD - time)
            if (self.AuroraCD > 0) : self.AuroraCD = max(0,self.AuroraCD - time)
            if (self.SuperbolideCD > 0) : self.SuperbolideCD = max(0,self.SuperbolideCD - time)
            if (self.HeartOfLightCD > 0) : self.HeartOfLightCD = max(0,self.HeartOfLightCD - time)
            if (self.HeartOfCorundumCD > 0) : self.HeartOfCorundumCD = max(0,self.HeartOfCorundumCD - time)
            if (self.CamouflageCD > 0) : self.CamouflageCD = max(0,self.CamouflageCD - time)


        def updateTimer(self, time : float):
            
            if (self.BowShockTimer > 0) : self.BowShockTimer = max(0,self.BowShockTimer - time)
            if (self.SonicBreakTimer > 0) : self.SonicBreakTimer = max(0,self.SonicBreakTimer - time)
            if (self.NoMercyTimer > 0) : self.NoMercyTimer = max(0,self.NoMercyTimer - time)
            if (self.HeartOfLightTimer > 0) : self.HeartOfLightTimer = max(0,self.HeartOfLightTimer - time)
            if (self.CamouflageTimer > 0) : self.CamouflageTimer = max(0,self.CamouflageTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_darkknight(self):
        #Special
        self.DarksideTimer = 0          #Darkside Gauge, starts at 0 with a max duration of 60s.
        self.Blood = 0                  #Blood Gauge, starts at 0 with a max of 100 units.
        self.EsteemPointer = None

        #Stacks and Ability timers
        self.BloodWeaponStacks = 0
        self.BloodWeaponTimer = 0       #Duration of Blood Weapon buff.
        self.DeliriumStacks = 0         #Stacks of Delirium.
        self.DeliriumTimer = 0          #Duration of Delirium stacks.
        self.SaltedEarthTimer = 0       #Salted Earth duration, required to use Salt and Darkness.
        self.ShadowbringerCharges = 2   #Charges of Shadowbringer
        self.PlungeCharges = 2          #Charges of Plunge
        self.DarkArts = False           #Dark Arts Gauge, activates when TBN breaks.
        self.OblationStack = 2
        self.DarkMindTimer = 0
        self.DarkMissionaryTimer = 0
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
        self.LivingDeadCD = 0  
        self.DarkMindCD = 0
        self.DarkMissionaryCD = 0
        self.OblationCD = 0
        #DOT
        self.SaltedEarthDOT = None
        #JobMod
        self.JobMod = 105

        #ActionEnum
        self.JobAction = DarkKnightActions

        def updateCD(self, time : float):
            
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
            if (self.LivingDeadCD > 0) :self.LivingDeadCD = max(0,self.LivingDeadCD - time)
            if (self.DarkMindCD > 0) :self.DarkMindCD = max(0,self.DarkMindCD - time)
            if (self.DarkMissionaryCD > 0) :self.DarkMissionaryCD = max(0,self.DarkMissionaryCD - time)
            if (self.OblationCD > 0) :self.OblationCD = max(0,self.OblationCD - time)

        def updateTimer(self, time : float):
            

            if (self.DarksideTimer > 0) : self.DarksideTimer = max(0,self.DarksideTimer - time)
            if (self.BloodWeaponTimer > 0) : self.BloodWeaponTimer = max(0,self.BloodWeaponTimer - time)
            if (self.DeliriumTimer > 0) : self.DeliriumTimer = max(0,self.DeliriumTimer - time)
            if (self.SaltedEarthTimer > 0) : self.SaltedEarthTimer = max(0, self.SaltedEarthTimer-time)
            if (self.DarkMindTimer > 0) : self.DarkMindTimer = max(0, self.DarkMindTimer-time)
            if (self.DarkMissionaryTimer > 0) : self.DarkMissionaryTimer = max(0, self.DarkMissionaryTimer-time)
        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_paladin(self):
        #Gauge
        self.OathGauge = 100

        #Stack
        self.SwordOathStack = 0
        self.RequestACatStack = 0
        self.InterveneStack = 2

        #BIGSWORDCOMBO
        self.BladeFaith = False
        self.BladeTruth = False
        self.BladeValor = False


        #Buff
        self.RequestACat = False

        #Timer
        self.GoringDOTTimer = 0
        self.CircleScornTimer = 0
        self.ValorDOTTimer = 0
        self.FightOrFlighTimer = 0

        #DOT
        self.GoringDOT = None
        self.CircleScornDOT = None
        self.ValorDOT = None

        #CD
        self.RequestACatCD = 0
        self.CircleScornCD = 0
        self.InterveneCD = 0
        self.ExpiacionCD = 0
        self.FightOrFlightCD = 0
        self.DivineVeilCD = 0
        self.HolySheltronCD = 0
        self.CoverCD = 0
        self.InterventionCD = 0
        self.PassageOfArmsCD = 0
        self.HallowedGroundCD = 0

        #JobMod
        self.JobMod = 100

        #ActionEnum
        self.JobAction = PaladinActions

        def updateCD(self, time : float):
            
            if (self.RequestACatCD > 0) : self.RequestACatCD = max(0,self.RequestACatCD - time)
            if (self.CircleScornCD > 0) : self.CircleScornCD = max(0,self.CircleScornCD - time)
            if (self.InterveneCD > 0) : self.InterveneCD = max(0,self.InterveneCD - time)
            if (self.ExpiacionCD > 0) : self.ExpiacionCD = max(0,self.ExpiacionCD - time)
            if (self.FightOrFlightCD > 0) : self.FightOrFlightCD = max(0,self.FightOrFlightCD - time)
            if (self.HolySheltronCD > 0) : self.HolySheltronCD = max(0,self.HolySheltronCD - time)
            if (self.CoverCD > 0) : self.CoverCD = max(0,self.CoverCD - time)
            if (self.InterventionCD > 0) : self.InterventionCD = max(0,self.InterventionCD - time)
            if (self.PassageOfArmsCD > 0) : self.PassageOfArmsCD = max(0,self.PassageOfArmsCD - time)
            if (self.HallowedGroundCD > 0) : self.HallowedGroundCD = max(0,self.HallowedGroundCD - time)

        def updateTimer(self, time : float):
            
            if (self.GoringDOTTimer > 0) : self.GoringDOTTimer = max(0,self.GoringDOTTimer - time)
            if (self.CircleScornTimer > 0) : self.CircleScornTimer = max(0,self.CircleScornTimer - time)
            if (self.FightOrFlighTimer > 0) : self.FightOrFlighTimer = max(0,self.FightOrFlighTimer - time)
            if (self.ValorDOTTimer > 0) : self.ValorDOTTimer = max(0,self.ValorDOTTimer - time)


        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

        #Oath Gauge Effect
        def OathGauge(Player, Spell):
            if Spell.id == -22: #AA's DOT have id -1
                Player.OathGauge = min(100, Player.OathGauge + 5) #adding 5 Gauge each AA

        self.EffectList.append(OathGauge)

    def init_warrior(self):
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
        self.ThrillOfBattleCD = 0
        self.HolmgangCD = 0
        self.ShakeItOffCD = 0
        self.NascentFlashCD = 0
        self.BloodwhettingCD = 0
        self.EquilibriumCD = 0

        #JobMod
        self.JobMod = 105

        #ActionEnum
        self.JobAction = WarriorActions

        def updateCD(self, time : float):
            
            if (self.InfuriateCD > 0) : self.InfuriateCD = max(0,self.InfuriateCD - time)
            if (self.UpheavalCD > 0) : self.UpheavalCD = max(0,self.UpheavalCD - time)
            if (self.InnerReleaseCD > 0) : self.InnerReleaseCD = max(0,self.InnerReleaseCD - time)
            if (self.OnslaughtCD > 0) : self.OnslaughtCD = max(0,self.OnslaughtCD - time)
            if (self.ThrillOfBattleCD > 0) : self.ThrillOfBattleCD = max(0,self.ThrillOfBattleCD - time)
            if (self.HolmgangCD > 0) : self.HolmgangCD = max(0,self.HolmgangCD - time)
            if (self.ShakeItOffCD > 0) : self.ShakeItOffCD = max(0,self.ShakeItOffCD - time)
            if (self.NascentFlashCD > 0) : self.NascentFlashCD = max(0,self.NascentFlashCD - time)
            if (self.BloodwhettingCD > 0) : self.BloodwhettingCD = max(0,self.BloodwhettingCD - time)
            if (self.EquilibriumCD > 0) : self.EquilibriumCD = max(0,self.EquilibriumCD - time)
    

        def updateTimer(self, time : float):
            
            if (self.SurgingTempestTimer > 0) : self.SurgingTempestTimer = max(0,self.SurgingTempestTimer - time)
            if (self.PrimalRendTimer > 0) : self.PrimalRendTimer = max(0,self.PrimalRendTimer - time)
            if (self.NascentChaosTimer > 0) : self.NascentChaosTimer = max(0,self.NascentChaosTimer - time)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    # Blackmage helper functions

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

    # Ninja helper function

    def ResetRitual(self):
        self.CurrentRitual = []

    def AddNinki(self, amount):
        self.NinkiGauge = min(100, self.NinkiGauge + amount)

    def AddHuton(self, amount):
        self.HutonTimer = min(60, self.HutonTimer + amount)

    # Reaper helper functions

    def AddGauge(self, Amount : int):
        self.SoulGauge = min(100, self.SoulGauge + Amount)

    def AddShroud(self, Amount : int):
        self.ShroudGauge = min(100, self.ShroudGauge + Amount)


    # Monk helper functions

    def OpenChakra(self):
        self.MaxChakraGate = min(5, self.MaxChakraGate)

    def addBeastChakra(self, type):
        for i in range(1,4):
            if self.MasterGauge[i] == 0: #Means its empty so we fill it out
                self.MasterGauge[i] = type
                return
        #If get here the whole thing is already filled, so nothing happens

    def BeastChakraType(self):
        #Returns number of BeastChakra
        OpoOpo = False
        Raptor = False
        Coeurl = False

        number_chakra = 0

        for i in self.MasterGauge[1:4]:
            if not OpoOpo and i == 1: 
                OpoOpo = True
                number_chakra += 1
            elif not Raptor and i == 2:
                Raptor = True
                number_chakra += 1
            elif not Coeurl and i == 3: 
                Coeurl = True
                number_chakra += 1

        return number_chakra

    def ResetMasterGauge(self):
        self.MasterGauge[1:4] = [0,0,0] #Reset Chakra

class Pet(Player):
    """
    This class is any pet summoned by a player.
    """

    def __init__(self, Master):
        """
        Master is the player object summoning the pet.
        This is only called once and the object is reused for future need
        """
        self.Master = Master
        Master.Pet = self
        self.ClassAction = CasterActions # Just a default
        self.JobAction = SummonerActions # Won't be used

        # Jobmod
        self.JobMod = 100

        #Giving already computed values for stats
        self.f_WD = Master.f_WD
        self.f_DET = Master.f_DET
        self.f_TEN = Master.f_TEN
        self.f_SPD = Master.f_SPD
        self.CritRate = Master.CritRate
        self.CritMult = Master.CritMult
        self.DHRate = Master.DHRate
        self.GCDReduction = Master.GCDReduction
        self.CritRateBonus = self.Master.CritRateBonus  # CritRateBonus
        self.DHRateBonus = self.Master.DHRateBonus # DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus
        self.Stat = deepcopy(self.Master.Stat)
        self.ArcanumTimer = self.Master.ArcanumTimer # ArcanumTimer
        self.MeditativeBrotherhoodTimer = self.Master.MeditativeBrotherhoodTimer # Meditative Brotherhood Timer

        super().__init__([], [], deepcopy(Master.Stat), JobEnum.Pet)

        # Adding itself to the fight object
        Master.CurrentFight.AddPlayer([self])

        def updateRoleTimer(self, time):
            pass

        def updateJobTimer(self, time):
            pass

        self.updateRoleTimer = updateRoleTimer
        self.updateJobTimer = updateJobTimer

    def updateCD(self, time: float):
        pass # Since there is no reason to update the CD on the pet, we will simply pass this computation

    def ResetStat(self):
        """
        This function is called upon reusing the object to reset the stats and other attributes that could interfere. 
        """
        self.f_WD = self.Master.f_WD
        self.f_DET = self.Master.f_DET
        self.f_TEN = self.Master.f_TEN
        self.f_SPD = self.Master.f_SPD
        self.CritRate = self.Master.CritRate
        self.CritMult = self.Master.CritMult
        self.DHRate = self.Master.DHRate
        self.GCDReduction = self.Master.GCDReduction
        self.CritRateBonus = self.Master.CritRateBonus  # CritRateBonus
        self.DHRateBonus = self.Master.DHRateBonus # DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus
        self.Stat = deepcopy(self.Master.Stat)
        self.ArcanumTimer = self.Master.ArcanumTimer # ArcanumTimer
        self.MeditativeBrotherhoodTimer = self.Master.MeditativeBrotherhoodTimer # Meditative Brotherhood Timer