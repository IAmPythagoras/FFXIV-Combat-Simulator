# This file contains the Player class and its implementation

from PlayerEnum import JobEnum, RoleEnum
from ActionEnum import *
from typing import TypeVar


# Defining types

B = TypeVar('B', bound=JobEnum.BlackMage) # Blackmage
R = TypeVar('R', bound=JobEnum.RedMage)
S = TypeVar('S', bound=JobEnum.Summoner)


class Player:

    def __init__(self, ActionSet, EffectList, CurrentFight, Stat,Job):
        """Create the player object"""
        self.ActionSet = ActionSet # Known Action List
        self.EffectList = EffectList # Normally Empty, can has some effects initially
        self.ClassEnum = 0 # RoleEnum Value is set later on
        self.JobEnum = Job # JobEnum
        self.EffectCDList = [] # List of Effect for which we have to check if the have ended
        self.DOTList = [] # List of DOTs
        self.NextSpell = 0 # Index of next action in ActionSet
        self.CurrentFight = CurrentFight # Reference to the fight the player is in
        self.ManaTick = 1.5 # Starts Mana tick at this value
        self.playerID = 0 # Might not be necessary so by default 0

        self.TrueLock = False   # Used to know when a player has finished all of its ActionSet
        self.Casting = False    # Flag set to true if the player is casting
        self.oGCDLock = False   # If animation locked by oGCD
        self.GCDLock = False    # If have to wait for another GCD
        self.CastingLockTimer = 0 # How long we have to wait until next cast
        self.oGCDLockTimer = 0 # How long we have to wait until next oGCD
        self.GCDLockTimer = 0 # How long we have to wait until next GCD
        self.PotionTimer = 0 # Timer on the effect of potion
        self.Delay = 3 # Default time difference between AAs

        self.Mana = 10000 # Starting mana
        self.HP = 1000  # Starting HP
        
        self.TotalPotency = 0 # Keeps track of total potency done
        self.TotalDamage = 0 # Keeps track of total damage done
        self.TotalMinDamage = 0 # Minimum expected damage (no crit or diret hit) 

        self.Stat = Stat # Stats of the player

        self.auras = [] # List containing all Auras at the start of the fight

        self.Trait = 1  # DPS mult from trait
        self.buffList = []
        self.GCDReduction = 1 # Mult GCD reduction based on Spell Speed or Skill Speed (computed before fight)
        self.CritRateBonus = 0  # CritRateBonus
        self.DHRateBonus = 0 # DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus
        self.EffectToRemove = [] # List filled with effect to remove.
        self.EffectToAdd = [] # List that will add effect to the effectlist or effectcdlist once it has been gone through once

        self.ArcanumTimer = 0 # ArcanumTimer
        self.MeditativeBrotherhoodTimer = 0 # Meditative Brotherhood Timer

        # Used for DPS graph and Potency/S graph

        self.DPSGraph = []
        self.PotencyGraph = []

        self.NumberDamageSpell = 0 # Number of damaging spell done, not including DOT and AA
        self.CritRateHistory = [] # History of crit rate, so we can average them at the end


        # functions for computing damage. Since the stats do not change (except MainStat), we can compute in advance
        # all functions that will not have their values changed
        # They will be computed at the begining of the simulation, they are now set at 0
        self.f_WD = 0
        self.f_DET = 0
        self.f_TEN = 0
        self.f_SPD = 0
        self.CritRate = 0
        self.CritMult = 0
        self.DHRate = 0


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
    
        def updateCD(self,time):
            if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)
            if (self.AddleCD > 0) : self.AddleCD = max(0,self.AddleCD - time)

        def updateTimer(self, time):
            super().updateTimer(time)
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

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
    
        def updateCD(self,time):
            if (self.SwiftcastCD > 0) : self.SwiftcastCD = max(0,self.SwiftcastCD - time)
            if (self.LucidDreamingCD > 0) : self.LucidDreamingCD = max(0,self.LucidDreamingCD - time)
            if (self.RescueCD > 0) : self.RescueCD = max(0,self.RescueCD - time)
            if (self.SurecastCD > 0) : self.SurecastCD = max(0,self.SurecastCD - time)

        def updateTimer(self, time):
            super().updateTimer(time)
            if (self.LucidDreamingTimer > 0) : self.LucidDreamingTimer = max(0,self.LucidDreamingTimer - time)

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
    
        def updateCD(self,time):
            if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
            if (self.LegSweepCD > 0) : self.LegSweepCD = max(0,self.LegSweepCD - time)
            if (self.BloodbathCD > 0) : self.BloodbathCD = max(0,self.BloodbathCD - time)
            if (self.FeintCD > 0) : self.FeintCD = max(0,self.FeintCD - time)
            if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)
            if (self.TrueNorthCD > 0) : self.TrueNorthCD = max(0,self.TrueNorthCD - time)

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
    
        def updateCD(self,time):
            if (self.LegGrazeCD > 0) : self.LegGrazeCD = max(0,self.LegGrazeCD - time)
            if (self.SecondWindCD > 0) : self.SecondWindCD = max(0,self.SecondWindCD - time)
            if (self.FootGrazeCD > 0) : self.FootGrazeCD = max(0,self.FootGrazeCD - time)
            if (self.PelotonCD > 0) : self.PelotonCD = max(0,self.PelotonCD - time)
            if (self.HeadGrazeCD > 0) : self.HeadGrazeCD = max(0,self.HeadGrazeCD - time)
            if (self.ArmLengthCD > 0) : self.ArmLengthCD = max(0,self.ArmLengthCD - time)

    def init_blackmage(self):
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




        def updateCD(self : B, time):
            super().updateCD(time)
            if (self.TransposeCD > 0) : self.TransposeCD = max(0,self.TransposeCD - time)
            if (self.AmplifierCD > 0) : self.AmplifierCD = max(0,self.AmplifierCD - time)
            if (self.LeyLinesCD > 0) : self.LeyLinesCD = max(0,self.LeyLinesCD - time)
            if (self.TripleCastCD > 0) : self.TripleCastCD = max(0,self.TripleCastCD - time)
            if (self.SharpCastCD > 0) : self.SharpCastCD = max(0,self.SharpCastCD - time)
            if (self.ManafrontCD > 0) : self.ManafrontCD = max(0,self.ManafrontCD - time)
            if (self.ManawardCD > 0) : self.ManawardCD = max(0,self.ManawardCD - time)

        def updateTimer(self : B, time):
            super().updateTimer(time)
            if (self.PolyglotTimer > 0) : self.PolyglotTimer = max(0,self.PolyglotTimer - time)
            if (self.EnochianTimer > 0) : self.EnochianTimer = max(0,self.EnochianTimer - time)
            if (self.LeyLinesTimer > 0) : self.LeyLinesTimer = max(0,self.LeyLinesTimer - time)
            if (self.Thunder3DOTTimer > 0) : self.Thunder3DOTTimer = max(0,self.Thunder3DOTTimer - time)
            if (self.Thunder4DOTTimer > 0) : self.Thunder4DOTTimer = max(0,self.Thunder4DOTTimer - time)


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

    # Blackmage functions

    def AddFire(self : B):
            if self.ElementalGauge >= 0 :
                self.EnochianTimer = 15 #Reset Timer
                self.ElementalGauge = min(3, self.ElementalGauge + 1)
            else: #In Ice phase, so we loose it
                self.EnochianTimer = 0
                self.ElementalGauge = 0

    def AddIce(self : B):
        if self.ElementalGauge <= 0 :
            self.EnochianTimer = 15 #Reset Timer
            self.ElementalGauge = max(-3, self.ElementalGauge - 1)
        else: #In Fire phase, so we loose it
            self.EnochianTimer = 0
            self.ElementalGauge = 0


    def init_redmage(self):
        pass

    def init_summoner(self):
        pass

    def init_whitemage(self):
        pass

    def init_scholar(self):
        pass

    def init_astrologian(self):
        pass

    def init_sage(self):
        pass

    def init_machinist(self):
        pass
    
    def init_dancer(self):
        pass

    def init_bard(self):
        pass

    def init_monk(self):
        pass

    def init_reaper(self):
        pass

    def init_samurai(self):
        pass

    def init_dragoon(self):
        pass

    def init_ninja(self):
        pass

    def init_gunbreaker(self):
        pass

    def init_darkknight(self):
        pass

    def init_paladin(self):
        pass

    def init_warrior(self):
        pass
