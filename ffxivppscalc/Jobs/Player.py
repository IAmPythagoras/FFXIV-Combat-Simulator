# This file contains the Player class and its implementation

from PlayerEnum import JobEnum, RoleEnum


class Player:

    def __init__(self, ActionSet, EffectList, CurrentFight, Stat, Role, Job):
        """Create the player object"""
        self.ActionSet = ActionSet # Known Action List
        self.EffectList = EffectList # Normally Empty, can has some effects initially
        self.ClassEnum = Role # RoleEnum
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

        # Finding Role

        match self.RoleEnum:
            case RoleEnum.Tank:
                pass
            case RoleEnum.Healer:
                pass
            case RoleEnum.Caster:
                pass
            case RoleEnum.Melee:
                pass
            case RoleEnum.PhysicalRanged:
                pass

        # Finding Job

        match self.JobEnum:
            case JobEnum.BlackMage:
                self.init_blackmage()
            case JobEnum.RedMage:
                self.init_redmage()
            case JobEnum.Summoner:
                self.init_summoner()
            case JobEnum.Scholar:
                self.init_scholar()
            case JobEnum.WhiteMage:
                self.init_whitemage()
            case JobEnum.Astrologian:
                self.init_astrologian()
            case JobEnum.Sage:
                self.init_sage()
            case JobEnum.Monk:
                self.init_monk()
            case JobEnum.Ninja:
                self.init_ninja()
            case JobEnum.Dragoon:
                self.init_dragoon()
            case JobEnum.Samurai:
                self.init_samurai()
            case JobEnum.Reaper:
                self.init_reaper()
            case JobEnum.Machinist:
                self.init_machinist()
            case JobEnum.Bard:
                self.init_bard()
            case JobEnum.Dancer:
                self.init_dancer()
            case JobEnum.DarkKnight:
                self.init_darkknight()
            case JobEnum.Gunbreaker:
                self.init_gunbreaker()
            case JobEnum.Warrior:
                self.init_warrior()
            case JobEnum.Paladin:
                self.init_paladin()



    # The functions under here will be called to initialize the Role and/or Job

    def init_blackmage(self):
        pass
    
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
