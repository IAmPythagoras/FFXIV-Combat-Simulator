import copy
import logging

main_logging = logging.getLogger("ffxivcalc")
base_spell_logging = main_logging.getChild("Base_Spell")

from ffxivcalc.Jobs.ActionEnum import name_for_id
import math
from ffxivcalc.Jobs.PlayerEnum import JobEnum
from ffxivcalc.Jobs.PlayerEnum import RoleEnum
from ffxivcalc.helperCode.requirementHandler import failedRequirementEvent
from random import random, uniform
from ffxivcalc.helperCode.helper_math import roundDown
Lock = 0.75

class FailedToCast(Exception):#Exception called if a spell fails to cast
    pass


class buff:
    """
    This class is any buff given to a player. It contains the buff's value
    """
    def __init__(self, MultDPS):
        self.MultDPS = MultDPS #DPS multiplier of the buff

class buffHistory:
    """
    This class represents an interval of time in which a buff was present.
    """

    def __init__(self, StartTime : float, EndTime : float):
        self.StartTime = StartTime
        self.EndTime = EndTime

    def isUp(self, timeStamp : float) -> bool:
        """
        This function returns weither the buff was active under the given timeStamp
        timeStamp : float -> Timestamp in secconds
        """
        return timeStamp >= self.StartTime and timeStamp <= self.EndTime
    
class buffPercentHistory(buffHistory):
    """
    This class is a buffHistory that was a percent damage bonus. This class will also hold
    the percent bonus gained from the buff.
    """

    def __init__(self, StartTime : float, EndTime : float, PercentBonus : float):
        super().__init__(StartTime, EndTime)
        self.PercentBonus = PercentBonus

    def getPercentBonus(self) -> float:
        """
        This function returns the PercentBonus of this buff
        """
        return self.PercentBonus
    
class ZIPAction:
    """
    This class holds the information of an action's damage. It will be used to efficiently and quicly compute
    many runs with random crit and DH in order to get the DPS distribution of runs. In other words, ZIPActions
    are a "pre-baked" version of the normal Spell class.
    Damage (int) : Value corresponding to the pre computed damage value of the action. Doesn't include DH and Crit damage.
    CritChange (float) : Chance for the action to crit.
    CritMultiplier (float) : Crit multiplier of the action.
    AutoCritBonus (float) : Damage bonus from crit buff when auto crit.
    DHChance (float) : Chance for the action to DH.
    AutoDHBonus (float) : Damage bonus from direct hit when auto direct hit.
    """

    def __init__(self, Damage : int, CritChance : float, CritMultiplier : float, DHChance : float, auto_crit : bool = False, auto_dh : bool = False, AutoCritBonus : float = 1, AutoDHBonus : float = 1):
        self.Damage = Damage
        self.CritChance = CritChance
        self.CritMultiplier = CritMultiplier
        self.DHChance = DHChance
        self.auto_crit = auto_crit
        self.auto_dh = auto_dh
        self.AutoCritBonus = AutoCritBonus
        self.AutoDHBonus = AutoDHBonus

    def ComputeRandomDamage(self) -> int:
        """
        This function computes random damage of an action.
        """

        CritHit = (random() <= self.CritChance)
        DirectHit = ((random() <= self.DHChance))

        UniformDamage = math.floor(self.Damage * uniform(0.95, 1.05))
        CritDamage = math.floor(UniformDamage * (1 + self.CritMultiplier if CritHit else 1) * (self.AutoCritBonus if self.auto_crit else 1))
        DHDamage = math.floor(CritDamage * (1.25 if DirectHit else 1) * (self.AutoDHBonus if self.auto_dh else 1))
        return DHDamage

class PreBakedAction:
    """
    This class is similar to ZIPAction, but it has less preprocessing than a ZIPAction does.
    A PreBakedAction only has the given buffs in memory since the Stats of the player are not assumed
    constant when computing the damage.
    IsTank : bool -> If player is a tank. In which case f_MAIN_DAMAGE is different.
    MainStatPercentageBonus : float -> PercentageBonus of the MainStat (given by comp)
    HasPotionEffect : bool -> If the Action is under the effect of a tincture. Assumed to be Grade 8 HQ
    PercentageBonus : list(float) -> Bonus multiplier of the action
    CritBonus : float -> Crit bonus of the action
    DHBonus : float -> DH Bonus of the action
    type : int -> type of the damage
    AutoCrit : bool -> If is an auto crit (true)
    AutoDH : bool -> if is an auto DH (true)
    isFromPet : bool -> True if a Pet PreBakedAction
    isGCD : bool -> True if the action is a GCD
    gcdLockTimer : float -> Time value for which the player cannot take another GCD action.
    spellDPSBuff : float -> Flat bonus applied on this action
    """

    def __init__(self, IsTank : bool, MainStatPercentageBonus : float, buffList : list,
                 TraitBonus : float, Potency : int, type : int, 
                 nonReducableStamp : float, reducableStamp : float, AutoCrit : bool = False, AutoDH : bool = False,
                 isFromPet : bool = False, isGCD : bool = False,gcdLockTimer : float = 0, spellDPSBuff : float = 1):
        self.IsTank = IsTank
        self.MainStatPercentageBonus = MainStatPercentageBonus
        #self.HasPotionEffect = HasPotionEffect
        self.buffList = buffList # This holds all buff that are not raid buffs, since those can be affected by f_SPD. So RaidBuffs are in PercentageBonus
        self.TraitBonus = TraitBonus
        self.type = type
        self.Potency = Potency
        self.gcdLockTimer = gcdLockTimer

        self.nonReducableStamp = nonReducableStamp
        self.reducableStamp = reducableStamp

        self.AutoCrit = AutoCrit
        self.AutoDH = AutoDH
        self.AutoCritBonus = 1
        self.AutoDHBonus = 1
        
        self.isFromPet = isFromPet
        self.isGCD = isGCD
        self.spellDPSBuff = spellDPSBuff

                             # These values are computed once the PreBakedAction is being looped
                             # through in SimulatePreBakedFight.
        self.CritBonus = 0
        self.DHBonus = 0
        self.PercentageBonus = []

    def resetTimeSensibleBuff(self):
        """
        This function resets the value for CritBonus, DHBonus and PercentageBonus.
        """
        self.CritBonus = 0
        self.DHBonus = 0
        self.PercentageBonus = []

    def ComputeExpectedDamage(self, f_MAIN_DMG : float, f_WD : float, f_DET : float, f_TEN : float, f_SPD : float, f_CritRate : float, f_CritMult : float, f_DH : float, DHAuto : float):
        """
        This function is called to compute the damage of the action.
        This function requires all the values computed from the stat of the player
        These values can be computed using the Fight.ComputeFunctions logic.
        This function also returns Damage without crit and DH in order to facilitate the computation
        of random action damage in ComputeRandomDamage (which is computed afterward)
        n : int -> number of time for which the PreBakedAction will compute the random damage.
        """

        f_DET_DH = math.floor((f_DET + DHAuto) * 1000 ) / 1000

        Damage = 0
        if self.type == 0: # Type 0 is direct damage
            Damage = math.floor(math.floor(math.floor(math.floor(math.floor(self.Potency * f_MAIN_DMG) * (f_DET_DH if self.AutoCrit else f_DET)) * f_TEN ) *f_WD) * self.TraitBonus) # Player.Trait is trait DPS bonus
        elif self.type == 1: # Type 1 is magical DOT
            Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(self.Potency * f_WD) * f_MAIN_DMG) * f_SPD) * f_DET) * f_TEN) * self.TraitBonus) + 1
        elif self.type == 2: # Type 2 is physical DOT
            Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(self.Potency * f_MAIN_DMG) * f_DET) * f_TEN) * f_SPD) * f_WD) * self.TraitBonus) +1
        elif self.type == 3: # Auto-attacks
            Damage = math.floor(math.floor(math.floor(self.Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD)
            Damage = math.floor(math.floor(Damage * math.floor(f_WD * (3/3) *100 )/100) * self.TraitBonus) # Player.Delay is assumed to be 3 for simplicity for now
        
        for buff in self.PercentageBonus:
            Damage = math.floor(Damage * buff)

        Damage = math.floor(Damage * self.spellDPSBuff)
        
        auto_crit_bonus = (1 + self.CritBonus * f_CritMult) if self.AutoCrit else 1# Auto_crit bonus if buffed
        auto_dh_bonus = (1 + (self.DHBonus) * 0.25) if self.AutoDH else 1# Auto_DH bonus if buffed

        ExpectedDamage = math.floor(Damage *         (1 + ( (f_CritRate + self.CritBonus) if not self.AutoCrit else 1)  * f_CritMult))
        ExpectedDamage = math.floor(ExpectedDamage * (1 + ((f_DH + self.DHBonus) if not self.AutoDH else 1) * 0.25))
        ExpectedDamage = math.floor(ExpectedDamage * auto_crit_bonus)
        ExpectedDamage = math.floor(ExpectedDamage * auto_dh_bonus)

        base_spell_logging.debug("PreBakedAction has expected damage of " + str(ExpectedDamage) + " Potency :" + str(self.Potency) +" Trait : " + str(self.TraitBonus))
        base_spell_logging.debug(str((f_MAIN_DMG, f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH)))

        return ExpectedDamage, Damage
    
    def ComputeRandomDamage(self,Damage : int, f_CritRate : float, f_CritMult : float, f_DH : float) -> int:
        """
        This function computes random damage of a PreBakedAction. It uses the Damage value precomputed in the
        ComputeExpectedDamage in order to make the computation faster.
        Damage : int -> Damage value without Crit/DH.
        Relevant player values fr Crit/DH.
        """
                             # Checking if Critical and/or DH.
        CritHit = (random() <= (f_CritRate + self.CritBonus)) or self.AutoCrit
        DirectHit = ((random() <= (f_DH + self.DHBonus))) or self.AutoDH

        auto_crit_bonus = (1 + (self.CritBonus * f_CritMult)) if self.AutoCrit else 1# Auto_crit bonus if buffed
        auto_dh_bonus = (1 + (self.DHBonus * 0.25)) if self.AutoDH else 1# Auto_DH bonus if buffed

        UniformDamage = math.floor(Damage * uniform(0.95, 1.05))
        CritDamage = math.floor(UniformDamage * (1 + f_CritMult if CritHit else 1) * (self.AutoCritBonus if self.AutoCrit else 1))
        RandomDamage = math.floor(CritDamage * (1.25 if DirectHit else 1) * (self.AutoDHBonus if self.AutoDH else 1))
        RandomDamage = math.floor(RandomDamage * auto_crit_bonus)
        RandomDamage = math.floor(RandomDamage * auto_dh_bonus)

        return RandomDamage

class Spell:
    """
    This class is any Spell, it will have some subclasses to take Job similar spell, etc.
    """
    def __init__(self, id : int, GCD : bool, CastTime : float, RecastTime : float, Potency : int, ManaCost : int, Effect, Requirement, type : int = 0, aoe_fn = None, AOEHeal = False, TargetHeal = False):
        """
        Initialization of a Spell
        id : int -> id to identify the action
        GCD : bool -> True if the action is a GCD
        CastTime : float -> Cast time of the action
        RecastTime : float -> Recast time of the action
        Potency : int -> base potency of the action
        Manacost : int -> base manacost of the action
        Effect : function -> A function called upon the execution of the action which affects the player and the enemy.
        Requirement : (function -> Bool) -> function called upon the execution to verify if the action can be executed.
        type (int) : Type of the action. The types are Spell, Weaponskill and Ability. Type = 0 is ability, type = 1 is Spell and type = 2 is Weaponskill.
        aoe_fn (function) : Function that will be called (eeeeeeh)
        AOEHeal : bool -> True if the action is an AOE healing action
        TargetHeal : bool -> True if the action is a target healing action
        """

        if aoe_fn == None:
            def f():
                pass
            self.aoe_fn = f

        self.id = id
        self.GCD = GCD #True if GCD
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.CastTime = CastTime
        self.RecastTime = RecastTime
        self.Effect = [Effect]
        self.Requirement = Requirement
        self.DPSBonus = 1
        self.TargetID = 0 #By default 0
        self.type = type 
        self.AOEHeal = AOEHeal
        self.TargetHeal = TargetHeal

    def Cast(self, player, Enemy):
        """
        This function is called by the simulator when an action is ready to begin its casting. It checks for the requirement and apply all effect
        currently in the fight that can affect the action. It will lock the player into casting mode if necessary. The action is not executed here
        and is in a way being preapred to be executed. It will be checked if the action can be done.
        player : player -> player object casting
        Enemey : Enemy -> Enemy object on which the action is done.
        """
        tempSpell = copy.deepcopy(self)
        #Creating a tempSpell which will have its values changed according that what effect
        #the player and the enemy have
        #Will apply each effect the player currently has on the spell
        if self.id != -1: #id = -1 is WaitAbility, we don't want anything with that
            for Effect in player.EffectList:
                Effect(player, tempSpell)#Changes tempSpell
            for Effect in Enemy.EffectList:
                Effect(player, tempSpell)#Changes tempSpell
        #Checks if we meet the spell requirement

        # Round casting and recasting time :

        tempSpell.CastTime = roundDown(tempSpell.CastTime, 2)
        tempSpell.RecastTime = roundDown(tempSpell.RecastTime, 2)
        #Remove all effects that have to be removed

        for remove in player.EffectToRemove:
            player.EffectList.remove(remove) #Removing effect
        for add in player.EffectToAdd:
            player.EffectList.append(add)
        
        player.EffectToRemove = [] #Empty the remove list
        player.EffectToAdd = []

        for Requirement in tempSpell.Requirement:
            ableToCast, timeLeft = Requirement(player, tempSpell)
            if(not ableToCast): #Requirements return both whether it can be casted and will take away whatever value needs to be reduced to cast
                #Will check if timeLeft is within a margin, so we will just wait for it to come
                #timeLeft is the remaining time before the spell is available

                addInfo = "" if timeLeft <= 0 else "player had to wait for or would have to wait for " + str(timeLeft) + " seconds. GCDLock " + str(player.GCDLockTimer)

                fatal =  not(timeLeft <= player.CurrentFight.waitingThreshold and timeLeft > 0) and  (player.CurrentFight.RequirementOn)  # true if stops the simulation

                newFailedRequirementEvent = failedRequirementEvent(player.CurrentFight.TimeStamp, player.playerID, Requirement.__name__, addInfo, fatal) # Recording the event
                player.CurrentFight.failedRequirementList.append(newFailedRequirementEvent) # storing the event in memory

                log_str = ("FailedRequirementEvent, " + " , Timestamp : " + str(player.CurrentFight.TimeStamp)
                + " , PlayerID : " + str(player.playerID) + " , RequirementName : " + Requirement.__name__ + " , Fatal : " + str(fatal) + " , Info : " + addInfo)

                if fatal : base_spell_logging.critical(log_str) # if fatal makes the sim crash
                else : base_spell_logging.warning(log_str) # if not fatal doesn't crash the sim
                
                if not (player.CurrentFight.RequirementOn) : return tempSpell # If we do not care about requirement simply go on.
                elif timeLeft <= player.CurrentFight.waitingThreshold and timeLeft > 0: # If we care about requirement, we check if we can wait the allocated threshold. if we can we wait for it to come off cooldown.
                    # Limit of waiting for 1 sec
                    tempSpell = WaitAbility(timeLeft + 0.01)
                    player.ActionSet.insert(player.NextSpell, tempSpell)
                    return tempSpell #Makes the character wait
                    #Might remove some stuff tho, might have to check into that (for when effects are applied)
                
                player.CurrentFight.wipe = True # otherwise we stop the simulation 
                return tempSpell
        #Will make sure CastTime is at least Lock
        if tempSpell.id > 0 and tempSpell.CastTime < Lock : tempSpell.CastTime = 0 #id < 0 are special abilities like DOT, so we do not want them to be affected by that
        return tempSpell
        #Will put casting spell in player, and do damage/effect once the casting time is over


    def CastFinal(self, player, Enemy):

        """
        This function is called when an action is ready to be casted and apply its damage and effect.
        player : player -> player object casting
        Enemy : Enemy -> Enemy object on which the action is done.
        """
        
        for Effect in self.Effect:
            Effect(player, Enemy)#Put effects on Player and/or Enemy
        #This will include substracting the mana (it has been verified before that the mana was enough)
        minDamage, Damage, Heal = 0,0,0
        if self.AOEHeal or self.TargetHeal:
            type = 1
            if self.AOEHeal:
                             # Affects all players
                for gamer in player.CurrentFight.PlayerList:
                    Heal = player.CurrentFight.ComputeHealingFunction(player, self.Potency, gamer, 1, type, self)[0]
                    #base_spell_logging.debug(
                    #    "Timestamp : " + str(player.CurrentFight.TimeStamp) + " Player " + str(gamer.playerID) + "received a healing of min value : " + str(heal[0])
                    #)
                    gamer.HP += Heal
        else:
            type = 0 #Default value for type
            if isinstance(self, Auto_Attack):
                type = 3
            elif isinstance(self, DOTSpell): #Then dot
                #We have to figure out if its a physical dot or not
                if self.isPhysical: type = 2
                else: type = 1   


            if player.CurrentFight.SavePreBakedAction:
                                # Adding to totalTimeNoFaster
                if self.GCD and self.RecastTime <= 1.5: # We check that the spellObj has recastTime lower than 1.5 and that it is not the last spell (since all those are insta cast)
                    if  player.isLastGCD(player.NextSpell): # if last GCD, add CastTime
                        player.totalTimeNoFaster += self.CastTime
                    else:        # Else adding recastTime. 
                        player.totalTimeNoFaster += self.RecastTime
                elif not self.GCD and player.isLastGCD(player.NextSpell) : 
                                # Is an oGCD
                    player.totalTimeNoFaster += self.CastTime
                elif self.GCD and (player.RoleEnum == RoleEnum.Caster) and self.type == 2: # If is a weaponskill and has Spell speed. Only needed for RDM now
                    if  player.isLastGCD(player.NextSpell): # if last GCD, add CastTime
                        player.totalTimeNoFaster += self.CastTime
                    else:        # Else adding recastTime. 
                        player.totalTimeNoFaster += self.RecastTime
                elif self.GCD and (player.RoleEnum == RoleEnum.Melee or player.RoleEnum == RoleEnum.Tank) and self.type == 1: # If is a spell and has skill speed
                    if  player.isLastGCD(player.NextSpell): # if last GCD, add CastTime
                        player.totalTimeNoFaster += self.CastTime
                    else:        # Else adding recastTime. 
                        player.totalTimeNoFaster += self.RecastTime

                                # If the action has 0 potency we skip the computation
                                # Note that this also means the action won't be added as a ZIPAction for the player.
            if self.Potency != 0 : minDamage,Damage= player.CurrentFight.ComputeDamageFunction(player, self.Potency, Enemy, self.DPSBonus, type, self, SavePreBakedAction = player.CurrentFight.SavePreBakedAction, PlayerIDSavePreBakedAction = player.playerID)    #Damage computation
            
            # move this before damage??????
            if player.JobEnum == JobEnum.Pet and self.Potency != 0: # Is a pet and action does damage

                # Updating damage and potency
                player.Master.TotalPotency+= self.Potency
                player.Master.TotalDamage += Damage
                player.Master.TotalMinDamage += minDamage

                # Updating Enemity
                if player.Master.RoleEnum == RoleEnum.Tank and player.Master.TankStanceOn:
                    # If the player is a tank and have their tank stance on
                    player.Master.TotalEnemity += Damage/1000
                    # This Enemity computation is arbitrary and is simply based on the fact that a tank with tank stance on
                    # generates 10 times the enemity of a player without tank stance.
                    # The value is made arbitrarily small in order to avoid too big numbers
                else:
                    player.Master.TotalEnemity += Damage/10000
            elif self.Potency != 0: # Is not a pet and action does damage
                # Updating damage and potency
                player.TotalPotency+= self.Potency
                player.TotalDamage += Damage
                player.TotalMinDamage += minDamage

                # Updating Enemity
                if player.RoleEnum == RoleEnum.Tank and player.TankStanceOn:
                    # If the player is a tank and have their tank stance on
                    player.TotalEnemity += Damage/1000
                    # This Enemity computation is arbitrary and is simply based on the fact that a tank with tank stance on
                    # generates 10 times the enemity of a player without tank stance.
                    # The value is made arbitrarily small in order to avoid too big numbers
                else:
                    player.TotalEnemity += Damage/10000

            Enemy.TotalPotency+= self.Potency  #Adding Potency
            Enemy.TotalDamage += Damage #Adding Damage

                                # This code starts the fight the first time a damaging action is done.
            if not (player.CurrentFight.FightStart) and Damage > 0 : 
                base_spell_logging.debug("Fight has started after the action "+name_for_id(player.CastingSpell.id,player.ClassAction, player.JobAction)+" done by player " + str(player.playerID))
                player.CurrentFight.FightStart = True
                                # Giving all players AA
                for gamer in player.CurrentFight.PlayerList:
                    if gamer.JobEnum == JobEnum.Monk: gamer.DOTList.append(copy.deepcopy(Monk_Auto))
                    elif gamer.RoleEnum == RoleEnum.Melee or gamer.JobEnum == JobEnum.Dancer or gamer.RoleEnum == RoleEnum.Tank:
                        gamer.DOTList.append(copy.deepcopy(Melee_AADOT))
                    elif gamer.RoleEnum == RoleEnum.PhysicalRanged:
                        gamer.DOTList.append(copy.deepcopy(Ranged_AADOT))

                                # Will record the starting HP of every player for graph
                for gamer in player.CurrentFight.PlayerList:
                    gamer.HPGraph[0].append(0)
                    gamer.HPGraph[1].append(gamer.HP)

                             # Will update the NextSpell of the player
        if (not (isinstance(self, DOTSpell))) : player.NextSpell+=1 # Only increase counter if action was not a DOT
                             # Checks if player has no more actions
        if (player.NextSpell == len(player.ActionSet)):
            if player.RoleEnum == RoleEnum.Pet: # If the player is a pet simply lock it
                player.TrueLock = True
            else: # Else we will call NextAction on this player before locking it
                player.NoMoreAction = True
            
        if self.GCD: player.GCDCounter += 1 # If action was a GCD, increase the counter

        if self.id > 0: # Only logs if is a player action and not a DOT
            log_str = ( "Timestamp : " + str(player.CurrentFight.TimeStamp)
            + " , Event : end_cast"
            + (" , playerID : " + str(player.playerID) if player.JobEnum != JobEnum.Pet else " , MasterID : " + str(player.Master.playerID))
            + " , CastTime : " + str(self.CastTime) + " RecastTime : " + str(self.RecastTime)
            + " , Ability : " + name_for_id(player.CastingSpell.id,player.ClassAction, player.JobAction)
            + " , SpellBonus : " + str(self.DPSBonus)
            + " , Potency : " + str(self.Potency)
            + (" , Damage : " + str(Damage) if not (self.AOEHeal or self.TargetHeal) else " , Healing : " + str(Heal)))
            
            base_spell_logging.debug(log_str)

        return self # Return the spell object. Might not be needed.

def ManaRequirement(player, Spell):
    """
    Requirement function for mana
    """
    if player.Mana >= Spell.ManaCost :
        player.Mana -= Spell.ManaCost   #ManaRequirement is the only Requirement that actually removes Ressources
        return True, -1
    return player.CurrentFight.IgnoreMana, -1 # Ignore mana is a field of the fight set to true if we ignore the mana

def empty(Player, Enemy):
    pass

def WaitAbility(time : float):
    """
    This returns an action where the player waits for a certain amount of time given
    time : float
    """
    def ApplyWaitAbility(Player, Enemy):
        pass
    WaitAction = Spell(212, False, time, time, 0, 0, ApplyWaitAbility, [])
    WaitAction.waitTime = time #Special field just for wait ability
    return WaitAction

def ApplyPotion(Player, Enemy):
    """
    Functions applies a potion and boosts the main stat of the player
    """
    Player.mainStatBonus = min(math.floor(Player.Stat["MainStat"] * 0.1),262) # Capped from grade 8 HQ tincture
    Player.Stat["MainStat"] += Player.mainStatBonus
    Player.PotionTimer = 30

    Player.EffectCDList.append(PotionCheck)

                                     # Only relevant to PreBakedAction and only does that code if true
    if Player.CurrentFight.SavePreBakedAction:
        fight = Player.CurrentFight
                                     # If prepull, make it start at 0.05
        startTime = fight.TimeStamp if fight.FightStart else -0.05
        history = buffHistory(startTime, startTime + 30)
        Player.PotionHistory.append(history)

def PrepullPotion(Player, Enemy): #If potion is prepull
    """
    If the potion is prepull
    """
    ApplyPotion(Player, Enemy)
    Player.PotionTimer = 27 #Assume we loose a bit on it
    Player.EffectToRemove.append(PrepullPotion)

def PotionCheck(Player, Enemy):
    """
    Check of potion effect
    """
    if Player.PotionTimer <= 0:
        Player.Stat["MainStat"] -= Player.mainStatBonus #Assuming we are capped
        Player.EffectCDList.remove(PotionCheck)


class DOTSpell(Spell):
    """
    This class is any DOT. The action applying a dot will append a DOT object from this class (or any subclass of DOTSpell) which will do damage over time.
    """
    #Represents DOT
    def __init__(self, id, Potency, isPhysical):
        """
        id : int -> id of the dot. Dot have negative ids
        Potency : int -> base potency of the DOT
        isPhysical : bool -> True if the dot is physical
        """
        super().__init__(id, False, 0, 0, Potency,  0, empty, [])
        #Note that here Potency is the potency of the dot, not of the ability
        self.DOTTimer = 0   #This represents the timer of the dot, and it will apply at each 3 seconds
        self.isPhysical = isPhysical #True if physical dot, false if magical dot

        #This part will keep in memory the buffs when the DOT is applied.
        self.CritBonus = 0
        self.DHBonus = 0
        self.MultBonus = []
        self.onceThroughFlag = False #This flag will be set to True once the DOT damage has been through damage computation once
        #so we can snapshot the buffs only once
        #Note that AAs do not snapshot buffs, but in the code they will still have these fields

    def CheckDOT(self, Player, Enemy, TimeUnit : float):
        """
        This function is called every time unit of the simulation and will check if a dot will be applied. A dot is applied every 3 seconds.
        If a dot has to be applied it will Cast and Castfinal itself and reset its DOTTimer to 3 seconds.
        """

        self.DOTTimer = max(0, self.DOTTimer-TimeUnit)

        if(self.DOTTimer <= 0):
            #Apply DOT
            tempSpell  = self.Cast(Player, Enemy)#Cast the DOT
            tempSpell.CastFinal(Player, Enemy)
            self.DOTTimer = 3
            
class HOTSpell(DOTSpell):
    """
    This represents a Healing Over Time effect.
    """

    def __init__(self, id, Potency):
        super().__init__(id, Potency, False)
                             # Every HOT is on only one target, hence they are targetted.
        self.TargetHeal = True


class Auto_Attack(DOTSpell):
    """
    DOTSpell subclass only for Autos since they have different potency depending on if ranged or melee.
    """
    def __init__(self, id, Ranged : bool):
        """
        Ranged : bool -> True if the auto is ranged.
        """
        if Ranged : super().__init__(id, 80, True) # Ranged AA, 80 potency
        else: super().__init__(id, 90, True) # Melee AA, 90 potency

        self.DOTTimer = 0 

class Queen_Auto(Auto_Attack):
    """
    Subclass of DOTSpell only for Machinist's queen autos
    """

    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False

class Melee_Auto(Auto_Attack):
    """
    Subclass of DOTSpell only for melee autos
    """
    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False

class Ranged_Auto(Auto_Attack):
    """
    Subclass of DOTSpell only for ranged autos
    """
    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False

class Monk_AA(Melee_Auto):
    """
    Subclass of DOTSpell only for monk autos. The reason is that it can be on a faster rate if RiddleOfWind is activated. So the DOT
    update function is overwritten and checks for that and will update the timer accordingly.
    """
    def __init__(self):
        super().__init__(-5, False)
        self.DOTTimer = 0

    def CheckDOT(self, Player, Enemy, TimeUnit):
        
        self.DOTTimer = max(0, self.DOTTimer-TimeUnit)

        if(self.DOTTimer <= 0):
            #Apply AA
            tempSpell  = self.Cast(Player, Enemy)#Cast the DOT
            tempSpell.CastFinal(Player, Enemy)
            if Player.RiddleOfWindTimer > 0 : self.DOTTimer = 1.2
            else: self.DOTTimer = 2.4

def ApplyMonk_Auto(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Monk_Auto))

def ApplyMelee_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Melee_AADOT))

def ApplyRanged_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Ranged_AADOT))

def ApplyQueen_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Queen_AADOT))

Melee_AA = Spell(-30, False, 0, 0, 0, 0, ApplyMelee_AA, [])
Ranged_AA = Spell(-30, False, 0, 0, 0, 0, ApplyRanged_AA, [])
Queen_AA = Spell(-30, False, 0, 0, 0, 0, ApplyQueen_AA, [])

Monk_Auto = Monk_AA()
Melee_AADOT = Melee_Auto(-22, False)
Ranged_AADOT = Ranged_Auto(-23, True)
Queen_AADOT = Queen_Auto(-24, False)
Potion = Spell(-2, False, 1, 1, 0, 0, ApplyPotion, [])



