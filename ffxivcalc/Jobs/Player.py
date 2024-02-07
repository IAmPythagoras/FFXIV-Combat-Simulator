# This file contains the Player class and its implementation
from copy import deepcopy
from ffxivcalc.Jobs.PlayerEnum import JobEnum, RoleEnum
from ffxivcalc.Jobs.ActionEnum import *
from ffxivcalc.Request.etro_request import get_gearset_data

from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import EnochianEffectCheck, ElementalEffect
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import DualCastEffect
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import SongEffect
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import EspritEffect
from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import ComboEffect
from ffxivcalc.helperCode.exceptions import InvalidMitigation
from ffxivcalc.helperCode.helper_math import roundDown
from math import floor
import logging

main_logging = logging.getLogger("ffxivcalc")
player_logging = main_logging.getChild("Player")

class MitBuff:
    """This class represents a mitigation buff given to a player. This object
    also keeps track of the timer of such a buff.

    Returns:
        PercentMit (float) : Percent damage taken of the mitigation. So if 30% mit, PercentMit = 0.7
        Timer (float) : Timer of the mit
        Player (Player) : Player on which the mit is applied
        MagicMit (bool) : If the Mit is only for magic damage
        PhysicalMit (bool) : If the mit is only for physical damage.
        BuffName (str) : Name of the buff
    """

    def __init__(self, PercentMit : float, Timer : float, Player, MagicMit = False, PhysicalMit = False, BuffName = ""):
        self.PercentMit = PercentMit
        self.Timer = Timer
        self.Player = Player

        self.MagicMit = MagicMit
        self.PhysicalMit = PhysicalMit

        self.BuffName = BuffName

        # Checks for invalid input and raises error in both cases
        if self.MagicMit and self.PhysicalMit : raise InvalidMitigation()
        elif self.PercentMit <=0 or self.PercentMit >= 1: raise InvalidMitigation(InvalidRange=True, PercentMit=self.PercentMit)

        # If mitigation for both physical and magical will have TrueMit set to true.
        if not MagicMit and not PhysicalMit: self.TrueMit = True
        else :
            self.TrueMit = False

        

    def UpdateTimer(self, time : float):
        """Update the timer of the buff and removes itself if timer reaches 0.

        Args:
            time (float): time unit by which we update the timer
        """

        self.Timer -= time

        if self.Timer <= 0:
            self.Player.MitBuffList.remove(self)

class HealingBuff:
    """This class represents a buff for healing. It has a percent bonus and also
    a timer. Once the timer has reached 0 the buff removes itself.

    Returns:
        PercentBuff (float): Percent healing buff
        Timer (float) : Timer of the buff until end of its effect
        Player (Player) : Player on which the buff is applied
        GivenHealBuff (bool) : True if this buff buffs given healing instead of received healing.
        BuffName (str) : name of the buff. Only used for logging.
    """

    def __init__(self, PercentBuff : float, Timer : float, Player, GivenHealBuff = True, BuffName : str =""):
        self.PercentBuff = PercentBuff
        self.Timer = Timer
        self.Player = Player
        self.GivenHealBuff = GivenHealBuff
        self.BuffName = BuffName

    def UpdateTimer(self, time : float) -> None:
        """Update a buff's timer value. If the timer reaches 0 removes the shield from the player.

        Args:
            time (float): time value by which we update the shield's timer
        """

        self.Timer -= time

        if self.Timer <= 0: # Remove itself if time is 0
            player_logging.debug("TimeStamp : " + str(self.Player.CurrentFight.TimeStamp) + "Removing " + self.BuffName + " from player " + str(self.Player.playerID))
            if self.GivenHealBuff : self.Player.GivenHealBuffList.remove(self) # Removes from GivenHeal list
            else : self.Player.ReceivedHealBuffList.remove(self) # Remves from received heal list

class Shield:
    """This class represents a shield. It will take damage before the main HP of a player
    is reduced. A shield will remove itself if its time limit is reached.

    Attributes:
        ShieldAmount (int) : Amount of the shield
        Timer (float) : Timer of the shield
        Player (Player) : Player on which the shield is applied
    """

    def __init__(self, ShieldAmount : int, Timer: float, Player, ShieldName = ""):
        self.ShieldAmont = ShieldAmount
        self.Timer = Timer
        self.Player = Player
        self.ShieldName = ShieldName

    def UpdateTimer(self, time : float) -> None:
        """Update a shield's timer value. If the timer reaches 0 removes the shield from the player.

        Args:
            time (float): time value by which we update the shield's timer
        """

        self.Timer -= time

        if self.Timer <= 0:
            self.Player.ShieldList.remove(self) # Remove itself if time is 0

class Player:
    """
    This class represents all players in the simulation. Objects of this class contain vital information relative to what a player
    is.

    Attribute:
        ActionSet : List[Spell] -> List of spell the player will do in the simulation
        EffectList : List[Function] -> List of all effects the player has. Can be empty.
        CurrentFight : Fight -> Reference to the fight object in which the player is.
        Stat : Dict -> Stats of the player as a dictionnary
        Job : JobEnum -> Specific job of the player
    """

    def setStat(self, newStat : dict):
        """
        This function sets the given stat dict as the stat of the player. It does a deepcopy if the newStat
        dictionnary to avoid any issues.
        newStat : dict -> New stats dictionnary.
        """
        self.Stat = deepcopy(newStat)

    def recomputeRecastLock(self, isSpell : bool):
        """
        This function is called if a Haste change has been detected. This will recompute the gcdLock of the player.
        We only recompute the GCD Lock. Note that this is no longer valid, see function declaration for comment.
        isSpell : bool -> True if the value to use is SpellReduction. For simplicity, this value will be figured out based on the 
                          job of the player.
        """

                            # Leaving some of the code as comment in case.
                            # But found that haste buffs only affect the next GCD, meaning we do not have to recompute
                            # current lock timer. This also means we only have to update the currentDelay for AA.
                            # Note that this function is currently being called as soon as a change happens (before DOTs are applied)
                            # and it could be moved to being only called when AAs are applied IF there was a haste change.
                            # I will leave everything here regardless for now.

                             # Do not worry about CastingLockTimer since it will be 0 at this point. NOT TRUE
                             # ANYMORE WILL HAVE TO WORK ON THAT
        #self.GCDLockTimer = floor(floor(int(self.GCDLockTimer * 1000 ) * (100 - self.hasteChangeValue)/100)/10)/100
        #player_logging.debug("Haste change has been detected. New GCDLockTimer : " + str(self.GCDLockTimer))

                             # Only update this if player has AA. Which means if autoPointer is not None
        if self.autoPointer:
                             # Auto haste buff are multiplicative. Furthermore, since only Monk has
                             # two haste buffs and the other one is just auto haste buff we can only
                             # worry about the current haste and the autoHaste amount and multiply both.
            aaMultHaste = int((100-self.Haste) * (100-self.autoHaste)/100)
                             # Recomputing AA delay lock
                             # rounding on self.delay * 1000 on the integer is needed as otherwise it sometimes
                             # creates issues with floating points. Ex : 2.01 * 1000 = 2009.9999... which when
                             # int() = 2009
            self.currentDelay = floor(floor(int(round(self.baseDelay * 1000,0)) * (aaMultHaste)/100)/10)/100
            player_logging.debug("Haste change detected. New delay : " + str(self.currentDelay) + " aaMultHaste : " + str(aaMultHaste))
                             # Updating the AA Timer
            #self.autoPointer.DOTTimer = floor(floor(int(self.autoPointer.DOTTimer * 1000 ) * (100 - self.hasteChangeValue)/100)/10)/100

        self.hasteHasChanged = False
        self.hasteChangeValue = 0

    def AddHealingBuff(self, buff : HealingBuff, GivenHealBuff = True, stackable = False):
        """
        This function appends a HealingBuff object to the player's ReceivedHealBuffList or GivenHealBuffList.
        If an identical non-stackable effect is found. It simply reset the time on the buff.
        buff : Healing buff object
        GivenHealBuff : bool -> If the healing buff is on given heals rather than received heals
        stackable : bool -> True of the buff is stackable
        """

        if GivenHealBuff and not stackable and (buff.BuffName in self.GivenHealBuffNameList):
                             # The buff is non-stackable and already applied. So we reset the timer.
            for AppliedBuff in self.GivenHealBuffList:
                if AppliedBuff.BuffName == buff.BuffName:
                    AppliedBuff.Timer = buff.Timer
                    return
        elif not GivenHealBuff and not stackable and (buff.BuffName in self.ReceivedHealBuffNameList):
                             # The buff is non-stackable and already applied. So we reset the timer.
            for AppliedBuff in self.ReceivedHealBuffList:
                if AppliedBuff.BuffName == buff.BuffName:
                    AppliedBuff.Timer = buff.Timer
                    return
                             # Else we simply append the buff
        if GivenHealBuff: 
            self.GivenHealBuffList.append(buff)
            self.GivenHealBuffNameList.append(buff.BuffName)
        else:
            self.ReceivedHealBuffList.append(buff)
            self.ReceivedHealBuffNameList.append(buff.BuffName)

    def AddMitBuff(self, buff : MitBuff, stackable = False):
        """
        This function appends a MitBuff object to the player's MitBuffList. If a mit is non-stackable
        it will simply reset the timer of the buff in the case where it is already applied.
        buff : MitBuff -> MitBuff object to append
        stackable : bool -> true if the buff is stackable
        """

        if not stackable and buff.BuffName in self.MitBuffNameList:
                             # Buff is already applied and non-stackable
            for MitBuff in self.MitBuffList:
                if MitBuff.BuffName == buff.BuffName:
                    MitBuff.Timer = buff.Timer
                    return
                
        self.MitBuffList.append(buff)
        self.MitBuffNameList.append(buff.BuffName)
        
    def AddShield(self, shield : Shield, stackable = False):
        """
        This function appends a shield to the player's ShieldList. If the shield is already applied
        and non-stackable then it will simply reset the shield
        shield : Shield -> Shield object to append
        stackable : bool -> True of the shield is stackable.
        """

        if not stackable and shield.ShieldName in self.ShieldNameList:
            for Shield in self.ShieldList:
                if Shield.ShieldName == shield.ShieldName:
                    Shield.Timer = shield.Timer
                    Shield.ShieldAmount = shield.ShieldAmont
                    return
        
        self.ShieldList.append(shield)
        self.ShieldNameList.append(shield.ShieldName)
        
    def ApplyHeal(self, HealingAmount : int) -> None:
        """This function will update the HP according to
        the healing received.

        Args:
            HealingAmount (int) : Total amount of healing given to the player.
        
        """

        self.HP = min(self.HP + HealingAmount, self.MaxHP)

    def TakeDamage(self, DamageAmount : int, MagicDamage : bool) -> None:
        """
        This function will update the HP value of the players and will kill the player if its HP goes under 0

        Args:
            DamageAmount (int): Total damage the player is taking
            MagicDamage (bool) : True if the damage is magical. False if physical.
        """

        # Will first check if the player is a tank with their invuln on

        if self.RoleEnum == RoleEnum.Tank and self.InvulnTimer > 0 and (self.JobEnum == JobEnum.Gunbreaker or self.JobEnum == JobEnum.Paladin):
            # If is paladin or gnb with invuln on, then takes 0 damage
                return # We exit this function since they take no damage

        residual_damage = -1 * DamageAmount

        # Will compute the residual damage after shields have been applied

        for shield in self.ShieldList:
            residual_damage += shield.ShieldAmount

            if residual_damage > 0:
                # If residal damage is bigger than 0, then the shield has taken the full amount of the damage.
                # If such is the case the amount of remaining shield is the value of residual_damage

                shield.ShieldAmount = residual_damage
                return # Exit the function since all the damage has been taken care of
            elif residual_damage == 0 :
                # If the shield had exact damage
                shield.Player.ShieldList.remove(shield) # Remove shield from the player
                return # Exit the function since all the damage has been taken care of

        # If we get here then there is still residual damage that will affect the player's HP.
        # Damage that goes through the shield (if any) will then be substracted to the HP
        # If there is still damage to do, residual_damage < 0. Otherwise it is positive

        damage = -1 * residual_damage

        # Will now apply every mitigation the player has

        for MitBuff in self.MitBuffList:
            if MitBuff.TrueMit :
                # If true mit
                damage = int(damage * MitBuff.PercentMit)
            elif MitBuff.MagicMit and MagicDamage:
                # If the damage is magical and the mit is magical
                damage = int(damage * MitBuff.PercentMit)
            elif MitBuff.PhysicalMit and not MagicDamage:
                # If the damage is physical and the mit is physical
                damage = int(damage * MitBuff.PercentMit)

        # Take damage and record it
        self.HP -= max(0, damage)
        self.HPGraph[0].append(self.CurrentFight.TimeStamp)
        self.HPGraph[1].append(self.HP)
        player_logging.debug(
            "Timestamp : " + str(self.CurrentFight.TimeStamp) + "-> ID " + str(self.playerID) + " took " + str(damage) + ("Magical" if MagicDamage else "Physical") + "damage. Current HP : " + str(self.HP)
        )

        
        if self.HP <= 0:
            if self.RoleEnum == RoleEnum.Tank and self.InvulnTimer > 0 and (self.JobEnum == JobEnum.Warrior or self.JobEnum == JobEnum.DarkKnight):
                # If Warrior or DarkKnight with invuln
                self.HP = 1
            else : 
                player_logging.debug(
                    "ID " + str(self.playerID) + " died as a result of the above damage. The overkill is " + str(self.HP * -1)
                )
                self.TrueLock = True # Killing the player. Not allowed to raise.

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
        
    def isLastGCD(self, ActionIndex : int) -> bool:
        """
        This function returns weither the provided ActionIndex is the last GCD of the ActionSet of the player.
        ActionIndex : int -> Index of the action in the list ActionSet
        """

        for index in range(ActionIndex+1, len(self.ActionSet)):
            if self.ActionSet[index].GCD : return False
        return True
    
    def setBasedWeaponDelay(self, newDelay : float) -> None:
        """This function sets the value of the Delay for AA. By default has a value of 3.

        Args:
            newDelay (float): Value of the day in seconds.
        """
        self.baseDelay = newDelay

    def computeActionReduction(self) -> None:
        """
        This function computes SpellReduction and WeaponSkillReduction ratio and sets those values at the
        appropriate fields.
        """
        self.SpellReduction = (1000 - floor(130 * (self.Stat["SS"]-400) / 1900))/1000
        self.WeaponskillReduction = (1000 - floor(130 * (self.Stat["SkS"]-400) / 1900))/1000

    def computeActionTimer(self, Spell) -> None:

        """
        This function computes the new CastTime and RecastTime of the Spell given the player's current Haste and SpS/SkS value.

        Spell (Spell) -> Spell object to alter the CastTime and RecastTime
        """
        if Spell.type == 1: # Spell
            Spell.CastTime = floor(floor(floor((int(Spell.CastTime * 1000 ) * self.SpellReduction)) * (100 - self.Haste)/100)/10)/100  if Spell.CastTime > 0 else 0
            Spell.RecastTime =floor(floor(floor((int(Spell.RecastTime * 1000 ) * self.SpellReduction)) * (100 - self.Haste)/100)/10)/100
            if Spell.RecastTime < 1.5 and Spell.RecastTime > 0 : Spell.RecastTime = 1.5 # A GCD cannot go under 1.5 sec
        elif Spell.type == 2: # Weaponskill
            Spell.CastTime = floor(floor(floor((int(Spell.CastTime * 1000 ) * self.WeaponskillReduction)) * (100 - self.Haste)/100)/10)/100 if Spell.CastTime > 0 else 0
            Spell.RecastTime = floor(floor(floor((int(Spell.RecastTime * 1000 ) * self.WeaponskillReduction)) * (100 - self.Haste)/100)/10)/100
            if Spell.RecastTime < 1.5 and Spell.RecastTime > 0 : Spell.RecastTime = 1.5 # A GCD cannot go under 1.5 sec

    def computeTimeStamp(self) -> dict:
        """
        This function computes the final time stamp of the player given its current ActionSet and SpS/SkS value.
        The result could be a bit off for players with haste buff as this is meant as an approximation.
        It will also return how long is left until the next GCD after the last action is casted. In other words it returns how long
        the player will have to wait to execute another GCD.
        This function assumes that haste actions are always applied (if a combo is required)

        Return :
        dict -> {currentTimeStamp : float, untilNextGCD : float}
        """
                             # Computes the reduction ratios
        self.computeActionReduction()
                             # Initializes timeStamp and finalLockTimer and other relevants timer
        curTimeStamp = 0
        curDOTTimer = 0
        curBuffTimer = 0
        finalGCDLockTimer = 0
                             # hasteBuffList contains list of [startTime,EndTime,hasteAmount] to know when to apply haste buffs
                             # Note that this is a BIG ESTIMATE of the actual time since we do not modify the GCD
                             # as the oGCD is happening.
        hasteBuffTimeIntervalList = []
        hasteBuffIndexList = [] # -> This list contains the index of all haste actions done by the player.
                                # We check to see if one is made. When a haste action is made hasteBuffTimeIntervalList
                                # will be added an entry that will let us know when it should finish
        
                                # Will look what Haste action is possible from the player
        possibleHasteActionId = []
        hasteAmount = 0
        hasteBuffTimer = 0

                                 # If the job is blackmage we check for insta cast such as triplecast, swiftcast
                                 # and keep track of what state the player is in since it affects cast times.
                                 # It is not negligeable. We will assume a stack of triplecast is used right away
                                 # (same for swiftcast) and do not check if the casted action is insta cast (which wouldn't use the stack)
                                 # We also do not keep track of the different level of fire/ice and only assume full stack. This of course adds error, but will be smaller than without
                                 # this whole thing.
        isBLM = self.JobEnum == JobEnum.BlackMage
        inAstralFire = False
        inUmbralIce = False
        tripleCastStack = 0
        hasSwiftCast = False

                                 # If is a RedMage we keep track of swiftcast, acceleration and dual cast
        isRDM = self.JobEnum == JobEnum.RedMage
        hasDualCast = False
        hasAcceleration = False
        gcdCastDetectionLimit = 1.7 # Actions with cast times under that treshold will give dualcast

                                 # If is a Summoner we keept track of swiftcast
        isSMN = self.JobEnum == JobEnum.Summoner
        


        # Monk can be ommited since the player object of monk is
        # initialized with haste of 20.
        # And we assume max haste from bard (even if this results in worst estimate)
        # This could be made better in future versions.
        # Also assumes Astrologian always gets haste buff from Astrodyne
        # TODO -> Fix Bard estimate with army paeon
        match self.JobEnum:
            case JobEnum.BlackMage : # Leylines
                possibleHasteActionId.append(3573)
                hasteAmount = 15
                hasteBuffTimer = 30
            case JobEnum.WhiteMage : # Presence of Mind
                possibleHasteActionId.append(136)
                hasteAmount = 20
                hasteBuffTimer = 15
            case JobEnum.Samurai : # Shifu
                possibleHasteActionId.append(7479)
                hasteAmount = 13
                hasteBuffTimer = 40
            case JobEnum.Bard : # Army Paeon
                possibleHasteActionId.append(116)
                hasteAmount = 20
                hasteBuffTimer = 45 # This could be a mistake. TODO FIX THIS
            case JobEnum.Astrologian : # Astrodyne
                possibleHasteActionId.append(25870)
                hasteAmount = 10
                hasteBuffTimer = 15
            case JobEnum.Ninja : # 
                possibleHasteActionId.append(2269)
                possibleHasteActionId.append(25876)
                possibleHasteActionId.append(3563)
                hasteAmount = 15
                hasteBuffTimer = 60 # Since Huton give 60 we assume the best case

                             # This is simply for optimization so we only check once
        checkForHasteAction = len(possibleHasteActionId) != 0
        hasHasteAction = False


                             # Will check for DOTs and will track an estimate of remaining time on the DOT
                             # We proceed similarly to hasteBuff and look for what class has DOTs
        possibleDOTActionId = []
        dotTimer = 0 
                             # We only consider DOTs that are 'running' and ignore SMN Garuda DOT, GNB DOT,
                             # DRK puddle, etc. But we take 
                             # buffs that have to be reapplied like on RPR
        match self.JobEnum:
            case JobEnum.BlackMage : # T3/T4
                possibleDOTActionId.append(153)
                possibleDOTActionId.append(7420)
                dotTimer = 30
            case JobEnum.WhiteMage : # Dia
                possibleDOTActionId.append(16532)
                dotTimer = 30
            case JobEnum.Scholar : # Biolysis
                possibleDOTActionId.append(16540)
                dotTimer = 30
            case JobEnum.Astrologian : # Combust
                possibleDOTActionId.append(16554)
                dotTimer = 30
            case JobEnum.Sage : # Eukrasian Dosis
                possibleDOTActionId.append(24314)
                dotTimer = 30
            case JobEnum.Dragoon : # Chaotic Spring
                possibleDOTActionId.append(25772)
                dotTimer = 24
            case JobEnum.Monk : # Demolish
                possibleDOTActionId.append(66)
                dotTimer = 18
            case JobEnum.Samurai : # Higanbana
                possibleDOTActionId.append(16484)
                possibleDOTActionId.append(7489)
                dotTimer = 60
            case JobEnum.Bard : # Only tracks the highest DOT timer and allows iron jaws to reset
                                # both of them
                possibleDOTActionId.append(7406)
                possibleDOTActionId.append(7407)
                possibleDOTActionId.append(3560)
                dotTimer = 45
        checkForDOTAction = len(possibleDOTActionId) != 0

                             # Will also check for the running buffs timer
                             # Done similarly to DOT and hasteBuff
        possibleBuffActionId = []
        buffTimer = 0

        match self.JobEnum:
            case JobEnum.Reaper : # Death Design
                possibleBuffActionId.append(24378)
                possibleBuffActionId.append(24379)
                buffTimer = 30
            case JobEnum.Samurai : # Only tracks fugetsu
                possibleBuffActionId.append(7478)
                buffTimer = 40
            case JobEnum.Dragoon : # Powersurge
                possibleBuffActionId.append(87)
                buffTimer = 30
            case JobEnum.Monk : # Twin snakes
                possibleBuffActionId.append(61)
                buffTimer = 15
            case JobEnum.DarkKnight : # Darkside
                possibleBuffActionId.append(10)
                possibleBuffActionId.append(16470)
                buffTimer = 30
            case JobEnum.Warrior :
                possibleBuffActionId.append(16462)
                possibleBuffActionId.append(16470)
                possibleBuffActionId.append(7389)
                buffTimer = 30        

        checkForBuffAction = len(possibleBuffActionId) != 0

                             # gcdIndexList contains the index of all actions done by the player that are GCD.
        gcdIndexList = []    
        firstIndexDamage = 0
        foundFirstDamage = False
        
                            
                             # Need to find first action that actually damages. Usually a GCD but should check
                             # and will look for haste actions
        for index,action in enumerate(self.ActionSet):

            if checkForHasteAction and action.id in possibleHasteActionId:
                             # Found haste action. Will append to index
                hasteBuffIndexList.append(index)
                hasHasteAction = True

            if (not foundFirstDamage) and (action.Potency > 0 or action.id in possibleDOTActionId):
                foundFirstDamage = True
                             # Found first damaging action
                             # Add to timestamp and will check for GCD clipping
                spellObj = deepcopy(action)
                self.computeActionTimer(spellObj)
                             # Adding estimated value
                curTimeStamp += max(0,spellObj.RecastTime - spellObj.CastTime)
                             # Saving first index
                firstIndexDamage = index
                             # This is an edge case where there is only one GCD casted followed by some oGCD.
                             # Since it will not be put into gcdIndexList we initialize the value of finalGCDLockTimer
                             # To what is left in it.
                if action.GCD : finalGCDLockTimer = max(0,spellObj.RecastTime - spellObj.CastTime)
                if action.id in possibleDOTActionId : curDOTTimer = dotTimer - max(0,spellObj.RecastTime-spellObj.CastTime)

                if isBLM:
                             # if is a BLM we check if the action isFire or isIce if any
                    if spellObj.IsFire : inAstralFire = True
                    elif spellObj.IsIce : inUmbralIce = True

                if isRDM :
                             # To detect if dualcast is added we check if the spell has a casttime higher then 2.2 . If such is true
                             # then it wasn't affected by a previous dualcast, acceleration or a previous dualcast
                    if spellObj.CastTime > gcdCastDetectionLimit:
                        hasDualCast = True

                             # Do not check for buff since buff actions can never be the first GCD and are always
                             # 2nd or 3rd action.

                             # Populating gcdIndexList. Skips first damage instance
        for index in range(firstIndexDamage+1,len(self.ActionSet)):
            action = self.ActionSet[index]
            if action.GCD : gcdIndexList.append(index)
            

                             # If first haste action is done between the first GCD and 2nd it will be detected here
        if hasHasteAction and (hasteBuffIndexList[0] < gcdIndexList[0]):
                hasteBuffIndexList.pop(0) # Remove this haste index

                hasteBuffTimeIntervalList.append([curTimeStamp,curTimeStamp + hasteBuffTimer, hasteAmount])
                hasHasteAction = len(hasteBuffIndexList) != 0

                             # Initialize curTimeStamp according to first done oGCDs?

        if len(gcdIndexList) == 0 : 
                             # No (other) GCD(s) performed, so compute using only oGCD
            for index in range(firstIndexDamage+1,len(self.ActionSet)):
                action = self.ActionSet[index]
                curTimeStamp += self.ActionSet[index].RecastTime
                             # Since no other GCD remove oGCD cast time from the lock timer
                finalGCDLockTimer -= self.ActionSet[index].RecastTime
            return {"currentTimeStamp" : round(curTimeStamp,2), "untilNextGCD" : round(max(0,finalGCDLockTimer),2),"dotTimer" : 0, "buffTimer" : 0}

        
        lastGCDIndex = gcdIndexList[-1]
        for listIndex,gcdIndex in enumerate(gcdIndexList):
            hasteBonus = 0 # Always reset haste bonus
            if gcdIndex == lastGCDIndex:
                             # Last GCD. So simply compute how long is left in the GCD
                             # Making deep copy to not affect anything
                spellObj = deepcopy(self.ActionSet[gcdIndex])

                             # Checking for haste
                for hasteInterval in hasteBuffTimeIntervalList:
                    if curTimeStamp >= hasteInterval[0] and curTimeStamp <= hasteInterval[1]:
                        hasteBonus = hasteInterval[2]
                        break

                             # Compute spellObj cast/recast time
                self.Haste += hasteBonus
                self.computeActionTimer(spellObj)
                self.Haste -= hasteBonus

                if isBLM:
                    if inAstralFire and spellObj.IsIce or inUmbralIce and spellObj.IsFire:
                             # reduce casttime
                            spellObj.CastTime = max(round(spellObj.CastTime/2,2),1.5)

                             # Check for swiftcast/Triplecast
                    if spellObj.CastTime > 0.1:
                        if hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False
                        elif tripleCastStack > 0:
                            spellObj.CastTime = 0
                            tripleCastStack -= 1
                elif isRDM:
                    if spellObj.CastTime > 0.1 and spellObj.type == 1:
                        if hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False
                        elif hasAcceleration:
                            spellObj.CastTime = 0
                            hasAcceleration = False
                        elif hasDualCast:
                            spellObj.CastTime = 0
                            hasDualCast = False
                elif isSMN:
                    if spellObj.CastTime > 0.1 and hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False

                             # Adding CastTime only since last GCD
                curTimeStamp += spellObj.CastTime
                        
                gcdLockTimer = max(0,spellObj.RecastTime - spellObj.CastTime)
                curDOTTimer = max(0,curDOTTimer-spellObj.CastTime) # Removing until end of GCD
                curBuffTimer = max(0,curBuffTimer-spellObj.CastTime) # Removing until end of GCD


                             # if last action is buff update curBuffTimer
                if checkForBuffAction and spellObj.id in possibleBuffActionId:
                             # A dot is detected. Update buff timer and removing the time lost until the end of the GCD
                    curBuffTimer = buffTimer
                             # if last action is DOT update curDOTTimer
                elif checkForDOTAction and spellObj.id in possibleDOTActionId:
                             # A dot is detected. Update DOT timer and removing the time lost until the end of the GCD
                    curDOTTimer = dotTimer

                for ogcdIndex in range(lastGCDIndex+1,len(self.ActionSet)):
                    gcdLockTimer -= self.ActionSet[ogcdIndex].RecastTime
                    curDOTTimer = max(0,curDOTTimer-self.ActionSet[ogcdIndex].RecastTime) # Removing until end of GCD
                    curBuffTimer = max(0,curBuffTimer-self.ActionSet[ogcdIndex].RecastTime) # Removing until end of GCD

                             # If there is risks of clipping gcdLockTimer will be negative.
                             # So we substract gcdLockTimer from curTimeStamp (min(gcdLockTimer,0))
                             # Could be interesting to add 'Risk of Clipping between GCD X and GCD Y'
                curTimeStamp -= min(0,gcdLockTimer)
                finalGCDLockTimer = gcdLockTimer
            else:
                             # Check if this GCD or if there are oGCD between the next GCD that have HASTE effects
                if hasHasteAction and (hasteBuffIndexList[0] >= gcdIndex and hasteBuffIndexList[0] < gcdIndexList[listIndex+1]):
                    hasteBuffIndexList.pop(0) # Remove this haste index

                    hasteBuffTimeIntervalList.append([curTimeStamp,curTimeStamp + hasteBuffTimer, hasteAmount])
                    hasHasteAction = len(hasteBuffIndexList) != 0

                             # Making deep copy to not affect anything
                spellObj = deepcopy(self.ActionSet[gcdIndex])

                             # Checking if this action has an haste effect onto it.
                             # If it does we have to add haste to the player and remove it afterward.
                             
                
                for hasteInterval in hasteBuffTimeIntervalList:
                    if curTimeStamp >= hasteInterval[0] and curTimeStamp <= hasteInterval[1]:
                        hasteBonus = hasteInterval[2]
                        break

                             # Compute spellObj cast/recast time
                self.Haste += hasteBonus
                self.computeActionTimer(spellObj)
                self.Haste -= hasteBonus

                             # Checking if BLM in which case we add some effects is it applies 
                if isBLM:
                    if inAstralFire and spellObj.IsIce or inUmbralIce and spellObj.IsFire:
                             # reduce casttime
                            spellObj.CastTime = max(round(spellObj.CastTime/2,2),1.5)

                             # Check for swiftcast/Triplecast only if spell isn't already insta cast
                    if spellObj.CastTime > 0.1:
                        if hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False
                        elif tripleCastStack > 0:
                            spellObj.CastTime = 0
                            tripleCastStack -= 1
                elif isRDM:
                             # Check for swiftcast/dualcast/acceleration only if spell isn't already insta cast and is spell
                    if spellObj.CastTime > 0.1 and spellObj.type == 1:
                        if hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False
                        elif hasAcceleration:
                            spellObj.CastTime = 0
                            hasAcceleration = False
                        elif hasDualCast:
                            spellObj.CastTime = 0
                            hasDualCast = False
                elif isSMN:
                    if spellObj.CastTime > 0.1 and hasSwiftCast:
                            spellObj.CastTime = 0
                            hasSwiftCast = False

                             # Checking for if action is a DOT action. DOTs are only GCD so
                             # we only check with spellObj
                if checkForDOTAction and spellObj.id in possibleDOTActionId:
                             # A dot is detected. Update DOT timer and removing the time lost until the end of the GCD
                    curDOTTimer = dotTimer - max(0,spellObj.RecastTime - spellObj.CastTime)
                else : curDOTTimer = max(0,curDOTTimer-max(spellObj.RecastTime,spellObj.CastTime)) # Removing until end of GCD


                             # Checking for if action is a buff action. Buff actions are only on GCD
                             # so we can check spellObj only
                if checkForBuffAction and spellObj.id in possibleBuffActionId:
                             # A dot is detected. Update buff timer and removing the time lost until the end of the GCD
                    curBuffTimer = buffTimer - max(0,spellObj.RecastTime - spellObj.CastTime)
                else : curBuffTimer = max(0,curBuffTimer-max(spellObj.RecastTime,spellObj.CastTime)) # Removing until end of GCD

                curTimeStamp += max(spellObj.RecastTime, spellObj.CastTime)
                
                             # Adding estimated value 
                gcdLockTimer = max(0,spellObj.RecastTime - spellObj.CastTime)
                             # Will check if any potential clipping until next GCD
                             # Adding up all oGCD actions between both GCD.


                for ogcdIndex in range(gcdIndex+1,gcdIndexList[listIndex+1]):
                    gcdLockTimer -= self.ActionSet[ogcdIndex].RecastTime

                             # If isBLM we check if the oGCD action is 'transpose' which will affect the state
                             # We also check for triplecast/swiftcast
                    if isBLM : 
                        if self.ActionSet[ogcdIndex].id == 149 :
                            if inUmbralIce : 
                                inUmbralIce = False
                                inAstralFire = True
                            elif inAstralFire:
                                inUmbralIce = True
                                inAstralFire = False
                        elif self.ActionSet[ogcdIndex].id == 7561:
                            hasSwiftCast = True
                        elif self.ActionSet[ogcdIndex].id == 7421:
                            tripleCastStack = 3
                    elif isRDM:
                        if self.ActionSet[ogcdIndex].id == 7561:
                            hasSwiftCast = True
                        elif self.ActionSet[ogcdIndex].id == 7518:
                            hasAcceleration = True
                    elif isSMN:
                        if self.ActionSet[ogcdIndex].id == 7561:
                            hasSwiftCast = True


                             # If there is risks of clipping gcdLockTimer will be negative.
                             # So we substract gcdLockTimer from curTimeStamp (min(gcdLockTimer,0))
                             # Could be interesting to add 'Risk of Clipping between GCD X and GCD Y'
                curTimeStamp -= min(0,gcdLockTimer)
                if gcdLockTimer < 0: # if gcdLockTimer was exceeded then we have to remove to other timer
                    curDOTTimer = max(0,curDOTTimer+min(0,gcdLockTimer))
                    curBuffTimer = max(0,curBuffTimer+min(0,gcdLockTimer))

                                             # Last thing we check if BLM changes state or if RDM gets dualcast
                if isBLM:
                    if not inAstralFire and not inUmbralIce: # Not in any
                        if  spellObj.IsFire : inAstralFire = True
                        elif spellObj.IsIce : inUmbralIce = True
                    if inUmbralIce : 
                             # The only two actions that can make a BLM go from ice -> fire are F3 and transpose (is an oGCD) so we only check for those two.
                             # to see if we are now in fire. If the action 'IsIce' or not 'IsFire' and not 'IsIce' then we stay in ice.
                             # Else we loose both fire and ice
                        if spellObj.IsIce or (not spellObj.IsFire and not spellObj.IsIce):
                            pass
                        elif spellObj.id == 152:
                            inUmbralIce = False
                            inAstralFire = True
                        else :
                            inUmbralIce = False
                            inAstralFire = False # Might not be required, but is a way to make sure.
                    if inAstralFire:
                             # The only two actions that can make a BLM go from fire -> ice are B3 and transpose (is an oGCD) so we only check for those two.
                             # to see if we are now in ice. If the action 'IsFire' or not 'IsFire' and not 'IsIce' then we stay in fire.
                             # Else we loose both fire and ice
                        if spellObj.IsFire or (not spellObj.IsFire and not spellObj.IsIce):
                            pass
                        elif spellObj.id == 154:
                            inUmbralIce = True
                            inAstralFire = False
                        else :
                            inUmbralIce = False
                            inAstralFire = False # Might not be required, but is a way to make sure.
                             # Check if we give dualcast
                elif isRDM :
                    if spellObj.CastTime > gcdCastDetectionLimit:
                        hasDualCast = True

        return {"currentTimeStamp" : round(curTimeStamp,2), "untilNextGCD" : round(finalGCDLockTimer,2), "dotTimer" : round(curDOTTimer,2), "buffTimer" : round(curBuffTimer,2),
                "detectedInFire" : inAstralFire, "detectedInIce" : inUmbralIce, "dualCast" : hasDualCast}


    def __init__(self, ActionSet, EffectList, Stat,Job : JobEnum):

        self.ActionSet = ActionSet # Known Action List
        self.ZIPActionSet = [] # List of ZIPActions of the player
        self.ZIPDPSRun = [] # List containing all ZIP runs' DPS
        self.ZIPRunPercentile = {} # Percentiles of ZIPRuns
        self.PreBakedActionSet = [] # Contains all PreBakedActions of the player
        self.DPSBar = {} # Dict containing the count of DPS occurence of the ZIPActions
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
        self.PlayerName = "" # Can be used to give the player a name that will be displayed in the final graph and result.
        self.mainStatBonus = 0 # Used to remember the stat gained from pots.
        self.totalTimeNoFaster = 0 # total time in seconds that cannot be made faster by having more SpS or SkS. Used for PreBakedActions.

        # Buff History
        # These are used for PreBakedAction in order to know if chaning f_SPD changes what action is under what buff
        self.ChainStratagemHistory = []
        self.BattleLitanyHistory = []
        self.WanderingMinuetHistory = []
        self.BattleVoiceHistory = []
        self.DevilmentHistory = []
        self.PotionHistory = []
        self.PercentBuffHistory = []



        self.TrueLock = False   # Used to know when a player has finished all of its ActionSet
        self.NoMoreActionLog = True # Used to know if we have logged that the player has no more actions.
        self.NoMoreAction = False # Used to know when a player has no more actions to do. The user will have a choice to set TrueLock = True or to give anther action
        self.Casting = False    # Flag set to true if the player is casting
        self.oGCDLock = False   # If animation locked by oGCD
        self.GCDLock = False    # If have to wait for another GCD
        self.CastingLockTimer = 0 # How long we have to wait until next cast
        self.oGCDLockTimer = 0 # How long we have to wait until next oGCD
        self.GCDLockTimer = 0 # How long we have to wait until next GCD
        self.PotionTimer = 0 # Timer on the effect of potion
        self.baseDelay = 3 # Default time difference between AAs
        self.currentDelay = 3 # current Delay to be applied to AAs. Differs from baseDelay with Haste.
        self.autoPointer = None # Pointer to the player's AA DOT.
        self.Haste = 0 # Total Haste value of the player.
        self.autoHaste = 0 # Haste amount for AA only. This is only really relevant for monk Riddle Of Wind.
        self.hasteHasChanged = False # Flag to know if haste has changed. This is needed to recompute recast time.
        self.hasteChangeValue = 0 # Value for which haste has changed. Can be negative or positive.

        self.Mana = 10000 # Current mana. Max is 10'000
        self.HP = 2000  # Current HP
        self.MaxHP = 2000 # Starting HP
        self.ShieldList = [] # List of all shields currently applied on the player. Shield prio is lowest index to highest index
        self.ShieldNameList = [] # List of all shields' name currently applied on the player
        self.EnemyDOT = [] # List which contains all DOT applied by the enemy on the player.
        self.TotalEnemity = 0 # Value of Enemity
        self.MagicMitigation = 1 # Current value of magic mitigation
        self.PhysicalMitigation = 1 # Current value of physical mitagation
        
        self.TotalPotency = 0 # Keeps track of total potency done
        self.TotalDamage = 0 # Keeps track of total damage done
        self.TotalMinDamage = 0 # Minimum expected damage (no crit or diret hit) 
        self.DamageInstanceList = [] # Used to remember damage instance for debugging. Usually unused

        self.Stat = deepcopy(Stat) # Stats of the player
        self.baseMainStat = self.Stat["MainStat"] # copy of main stat base. used for pet

        self.auras = [] # List containing all Auras at the start of the fight

        self.Trait = 1  # DPS mult from trait
        self.buffList = [] # List of all damage buff on the player
        self.MitBuffList = [] # List of all MitBuff on the player
        self.MitBuffNameList = [] # List of all the MitBuff's name on the player
        self.ReceivedHealBuffList = [] # List of all healing buff on the player. Buffs incoming heals
        self.ReceivedHealBuffNameList = [] # List of all healing buff's name on the player. 
        self.GivenHealBuffList = [] # List of all healing buff on the player. Buffs given heal.
        self.GivenHealBuffNameList = [] # List of all healing buff's name on the player. 
        self.EffectToRemove = [] # List filled with effect to remove.
        self.EffectToAdd = [] # List that will add effect to the effectlist or effectcdlist once it has been gone through once

        self.ArcanumTimer = 0 # ArcanumTimer
        self.ArcanumBuff = None # Arcanum buff given to the player if any
        self.MeditativeBrotherhoodTimer = 0 # Meditative Brotherhood Timer
        self.OblationTimer = 0 # Oblation timer if its received
        self.CorundumTimer = 0 # Timer if corundum is given
        self.NascentFlashTimer = 0 # Timer if Nascent flash is given
        self.InterventionTimer = 0 # Timer if Intervention is given
        self.InterventionBuff = False # True if a given intervention is buffed
        # Used for DPS graph and Potency/s graph

        self.DPSGraph = []
        self.PotencyGraph = []
        self.HPGraph = [[],[]]

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
            self.DHAuto = 0
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
        Note that some of these update have round(_,2). This is because those are cyclic timer and a slight deviation
        can add up to a non-negligeable deviation by the end. The other timers are not cyclic and so them having a +-0.01 accuracy 
        isn't a big deal (for now). The timer of DOTs are also updated with a round(_,2)
        time : float -> unit by which we update the timers
        """
        if (self.GCDLockTimer > 0) : self.GCDLockTimer = round(max(0, self.GCDLockTimer-time),2)
        if (self.oGCDLockTimer > 0) : self.oGCDLockTimer = round(max(0, self.oGCDLockTimer-time),2)
        if (self.CastingLockTimer > 0) : self.CastingLockTimer = round(max(0, self.CastingLockTimer-time),2)
        if (self.ManaTick > 0) : self.ManaTick = round(max(0, self.ManaTick-time),2)
        if (self.ArcanumTimer > 0) : self.ArcanumTimer = max(0, self.ArcanumTimer-time)
        if (self.PotionTimer > 0) : self.PotionTimer = max(0, self.PotionTimer-time)
        if (self.MeditativeBrotherhoodTimer > 0) : self.MeditativeBrotherhoodTimer = max(0, self.MeditativeBrotherhoodTimer-time)
        if (self.OblationTimer > 0) : self.OblationTimer = max(0, self.OblationTimer-time)
        if (self.CorundumTimer > 0) : self.CorundumTimer = max(0, self.CorundumTimer-time)
        if (self.NascentFlashTimer > 0) : self.NascentFlashTimer = max(0, self.NascentFlashTimer-time)
        if (self.InterventionTimer > 0) : self.InterventionTimer = max(0, self.InterventionTimer-time)

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
        if (self.GCDLockTimer < self.CurrentFight.TimeUnit):
            self.GCDLockTimer = 0
            self.GCDLock = False
        
        if (self.oGCDLockTimer < self.CurrentFight.TimeUnit):
            self.oGCDLockTimer = 0
            self.oGCDLock = False
        
        if(self.Casting and self.CastingLockTimer < self.CurrentFight.TimeUnit):
            self.CastingSpell.CastFinal(self, self.CastingTarget)

        if (self.CastingLockTimer < self.CurrentFight.TimeUnit):
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
        self.InvulnTimer = 0

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
            if (self.InvulnTimer > 0) : self.InvulnTimer = max(0,self.InvulnTimer - time)

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

        self.EffectList = [ElementalEffect] # Adding effects
        self.EffectCDList = [EnochianEffectCheck]

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
        self.Fire3Proc = False
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
        self.PlenaryIndulgenceCD = 0
        self.DivineBenisonCD = 0
        self.TetragrammatonCD = 0
        self.AsylumCD = 0
        self.BenedictionCD = 0


        #Timer
        self.DiaTimer = 0
        self.LucidDreamingTimer = 0
        self.PresenceOfMindTimer = 0
        self.LilyTimer = 0

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
            if (self.PlenaryIndulgenceCD > 0) : self.PlenaryIndulgenceCD = max(0,self.PlenaryIndulgenceCD - time)
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

        def LilyTimerStartCheck(Player, Enemy):
            if Player.CurrentFight.FightStart:
                Player.EffectCDList.append(LilyCheck)
                Player.EffectToRemove.append(LilyTimerStartCheck)
                Player.LilyTimer = 20

        def LilyCheck(Player, Enemy):
            if Player.LilyTimer <= 0:
                Player.LilyStack = min(3, Player.LilyStack + 1)
                Player.LilyTimer = 20 #Reset Timer
                
        self.EffectCDList.append(LilyTimerStartCheck) #Starting with this check

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
        self.CollectiveUnconsciousCD = 0 #CollectiveUnconscious Uncounscious
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
            if (self.CollectiveUnconsciousCD > 0) : self.CollectiveUnconsciousCD = max(0,self.CollectiveUnconsciousCD - time)
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
        self.AddersgallTimer = 0 
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


        def applyAddersgallCheck(Player, Enemy):
            if Player.CurrentFight.FightStart:
                Player.EffectToRemove.append(applyAddersgallCheck)
                Player.EffectCDList.append(AddersgallCheck)
                Player.AddersgallTimer = 20

        def AddersgallCheck(Player, Enemy):
            if Player.AddersgallTimer <= 0:
                Player.AddersgallStack = min(3, Player.AddersgallStack + 1)
                Player.AddersgallTimer = 20

        self.EffectCDList.append(applyAddersgallCheck)

        # update functions
        self.updateJobTimer = updateTimer
        self.updateJobCD = updateCD

    def init_machinist(self):
        #Special
        self.RemoveHyperchargeStack = False # Used to know when to remove a hypercharge stack

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
        self.DismantleCD = 0

        #Timer
        self.WildFireTimer = 0
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
        self.HyperchargeStack = 0

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
            if (self.DismantleCD > 0) : self.DismantleCD = max(0,self.DismantleCD - time)

        def updateTimer(self, time : float):
            
            if (self.WildFireTimer > 0) : self.WildFireTimer = max(0,self.WildFireTimer - time)
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
        self.WanderingMinuet = False

        #Coda
        self.MageCoda = False
        self.ArmyCoda = False
        self.WandererCoda = False


        #CD
        self.SidewinderCD = 0
        self.EmpyrealArrowCD = 0
        self.WanderingMinuetCD = 0
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
        self.RadiantFinaleBuff = None

        #ActionEnum
        self.JobAction = BardActions
    
        def updateCD(self, time : float):
            
            if (self.SidewinderCD > 0) : self.SidewinderCD = max(0,self.SidewinderCD - time)
            if (self.EmpyrealArrowCD > 0) : self.EmpyrealArrowCD = max(0,self.EmpyrealArrowCD - time)
            if (self.WanderingMinuetCD > 0) : self.WanderingMinuetCD = max(0,self.WanderingMinuetCD - time)
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
        self.ExpectedChakraGate = 0 #This is a random value, so we will keep track of Expected, used value and maximum value
        self.MaxChakraGate = 0 #This is the one used to see if an action is even possible
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

        # Haste given from trait
        self.Haste = 20

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
        self.Soulsow = False

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

        # buff History
        self.TrickAttackHistory = []

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
            if (self.DotonTimer > 0) : self.DotonTimer = max(0,self.DotonTimer - time)

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
        self.BowShockDOT = None

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
        #self.GoringDOTTimer = 0
        self.CircleScornTimer = 0
        #self.ValorDOTTimer = 0
        self.FightOrFlightTimer = 0
        self.HolySheltronTimer = 0
        self.PassageOfArmsTimer = 0
        self.DivineVeilTimer = 0

        #DOT
        #self.GoringDOT = None
        self.CircleScornDOT = None
        #self.ValorDOT = None

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
        self.BulwarkCD = 0
        self.GoringBladeCD = 0

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
            if (self.BulwarkCD > 0) : self.BulwarkCD = max(0,self.BulwarkCD - time)
            if (self.GoringBladeCD > 0) : self.GoringBladeCD = max(0,self.GoringBladeCD - time)

        def updateTimer(self, time : float):
            
            #if (self.GoringDOTTimer > 0) : self.GoringDOTTimer = max(0,self.GoringDOTTimer - time)
            if (self.CircleScornTimer > 0) : self.CircleScornTimer = max(0,self.CircleScornTimer - time)
            if (self.FightOrFlightTimer > 0) : self.FightOrFlightTimer = max(0,self.FightOrFlightTimer - time)
            #if (self.ValorDOTTimer > 0) : self.ValorDOTTimer = max(0,self.ValorDOTTimer - time)
            if (self.HolySheltronTimer > 0) : self.HolySheltronTimer = max(0,self.HolySheltronTimer - time)
            if (self.PassageOfArmsTimer > 0) : self.PassageOfArmsTimer = max(0,self.PassageOfArmsTimer - time)
            if (self.DivineVeilTimer > 0) : self.DivineVeilTimer = max(0,self.DivineVeilTimer - time)


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
        
        # Current mit
        self.VengeanceBuff = None
        self.BloodwhettingBuff = None
        # Need to know which buff is up when casting shake it off

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
        self.ThrillOfBattleTimer = 0

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
            if (self.ThrillOfBattleTimer > 0) : self.ThrillOfBattleTimer = max(0,self.ThrillOfBattleTimer - time)

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

    # Summoner helpder function

    def resetPrimalEffect(self) -> None:
        """This function resets the effects gained from summoning a primal.
        This function is called before summoning a new primal.
        """
        self.TitanStack = 0
        self.TitanSpecial = False
        self.IfritStack = 0
        self.IfritSpecial = False
        self.IfritSpecialCombo = False
        self.GarudaStack = 0
        self.GarudaSpecial = False

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
        self.MaxChakraGate = min(5, self.MaxChakraGate+1)

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
        self.ClassAction = Master.ClassAction 
        self.JobAction = Master.JobAction 

        # Jobmod
        self.JobMod = 100

        #Giving already computed values for stats
                             # Recomputing f_WD since it is affected by JobMod
        self.f_WD = (Master.Stat["WD"]+floor(390*self.JobMod/1000))/100
        self.f_DET = Master.f_DET
        self.f_TEN = Master.f_TEN
        self.f_SPD = Master.f_SPD
        self.CritRate = Master.CritRate
        self.CritMult = Master.CritMult
        self.DHRate = Master.DHRate
        self.DHAuto = 0
        self.GCDReduction = Master.GCDReduction
        self.CritRateBonus = self.Master.CritRateBonus  # CritRateBonus
        self.DHRateBonus = self.Master.DHRateBonus # DHRate Bonus Very usefull for dancer personnal and dance partner crit/DH rate bonus
        self.Stat = deepcopy(self.Master.Stat)
        self.ArcanumTimer = self.Master.ArcanumTimer # ArcanumTimer
        self.MeditativeBrotherhoodTimer = self.Master.MeditativeBrotherhoodTimer # Meditative Brotherhood Timer

                             # Pets do not have the 5% comp bonus, so we take baseMain stat and then check if potion
        self.Stat["MainStat"] = Master.baseMainStat
        if Master.PotionTimer > 0 : self.Stat["MainStat"] += min(int(self.Stat["MainStat"] * 0.1), 262)

        player_logging.debug("New Pet Created : " + str(self.Stat))

        super().__init__([], [], deepcopy(Master.Stat), JobEnum.Pet)
        self.Stat["MainStat"] = Master.baseMainStat + (min(floor(Master.baseMainStat * 0.1),262) if Master.PotionTimer > 0 else 0)
                             # Giving same playerID as Master
        self.playerID = Master.playerID

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
        self.f_WD = (self.Master.Stat["WD"]+floor(390*self.JobMod/1000))/100
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

                             # Pets do not have the 5% comp bonus, so we take baseMain stat and then check if potion
        self.Stat["MainStat"] = self.Master.baseMainStat
        if self.Master.PotionTimer > 0 : self.Stat["MainStat"] += min(int(self.Stat["MainStat"] * 0.1), 262)

        self.ArcanumTimer = self.Master.ArcanumTimer # ArcanumTimer
        self.MeditativeBrotherhoodTimer = self.Master.MeditativeBrotherhoodTimer # Meditative Brotherhood Timer