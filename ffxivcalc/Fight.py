import math
from ffxivcalc.helperCode.Vocal import PrintResult
from ffxivcalc.Jobs.PlayerEnum import *

from copy import deepcopy


class NoMoreAction(Exception):# Exception called if a spell fails to cast
    pass

class Fight:
    """
    
    This class will be the environment in which the fight happens. It will hold a list of players, an enemy, etc.
    It will be called upon for when we want to start the simulation

    """

    def GetEnemityList(self, range : int):
        """Returns a list of players in order of greather enemity to lowest enemity. The length of the
        returned list is equal to range.

        range (int) : Number of players we want
        
        """


        sorted_list = sorted(self.PlayerList, key=lambda Player : Player.TotalEnemity, reverse=True)
        # This returns a sorted list of the PlayerList with respect to their TotalEnemity
        # This could be optimized. But for now we will reocompute this sorted list every time.

        return sorted_list[0:range] # Returns the number of targets we are interested in

    def __init__(self, Enemy, ShowGraph):
        self.Enemy = Enemy
        Enemy.CurrentFight = self
        self.ShowGraph = ShowGraph
        self.TimeStamp = 0
        self.TeamCompositionBonus = 1
        self.FirstHit = False # False until the first damaging action is done
        self.RequirementOn = True # By default True
        self.FightStart = False # If Fight is started
        self.IgnoreMana = True # If true we ignore mana in the simulation
        self.timeValue = [] # Array holding all sampling time for the DPS and PPS
        self.failedRequirementList = [] # List holding all failedRequirementEvent object for the fight.
        self.waitingThreshold = 1 # number of seconds we are willing to wait for. By default 1
        self.wipe = False # Will be set to True in case we are stopping the simulation.
        self.PlayerList = [] # Empty player list
        # functions

        def DefaultNextActionFunction(Fight, Player) -> bool:
            """
            The default function does not add any other actions and hence just returns True to lock the player.
            """
            return True

        def DefaultExtractInfo(Fight) -> None:
            """
            This function is called every frame of the simulation and can be used to extract whatever information from it we want.
            By default it does nothing.
            Note that the function cannot return any value, and so it must save all wanted data in some other variable or file.
            """
            pass

        self.ComputeDamageFunction = ComputeDamage # This would let someone overwrite this function.
        self.NextActionFunction = DefaultNextActionFunction
        self.ExtractInfo = DefaultExtractInfo

    def AddPlayer(self, Players):

        for player in Players:
            player.CurrentFight = self
            self.PlayerList.append(player)

    def SimulateFight(self, TimeUnit, TimeLimit, vocal) -> None:

        """
        This function will Simulate the fight given the enemy and player list of this Fight
        It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
        It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
        However, no direct computation is done in this function, it simply orchestrates the whole thing

        TimeUnit : float -> unit at which the simulator will advance through time in the simulation
        TimeLimit : float -> time limit at which the simulator will stop
        vocal : bool -> True if we want to print out the results
        """

        self.TimeStamp = 0   # Keep track of the time
        start = False

        self.timeValue = []  # Used for graph

        self.ComputeFunctions() # Compute all damage functions for the players


        # The first thing we will do is compute the TEAM composition DPS bonus
        # each class will give 1%
        # Tank, Healer, Caster, Ranged, Melee
        hasMelee = False
        hasCaster = False
        hasRanged = False
        hasTank = False
        hasHealer = False
        for player in self.PlayerList:
            if player.RoleEnum == RoleEnum.Melee : hasMelee = True
            elif player.RoleEnum == RoleEnum.PhysicalRanged : hasCaster = True
            elif player.RoleEnum == RoleEnum.Caster : hasRanged = True
            elif player.RoleEnum == RoleEnum.Healer : hasTank = True
            elif player.RoleEnum == RoleEnum.Tank : hasHealer = True

        if len(self.PlayerList) == 1 : self.TeamCompositionBonus = 1 # If only one player, there is not bonus
        else:
            if hasMelee: self.TeamCompositionBonus += 0.01
            if hasCaster: self.TeamCompositionBonus += 0.01
            if hasRanged: self.TeamCompositionBonus += 0.01
            if hasTank: self.TeamCompositionBonus += 0.01
            if hasHealer: self.TeamCompositionBonus += 0.01

        # Will first compute each player's GCD reduction value based on their Spell Speed or Skill Speed Value

        for Player in self.PlayerList:
            Player.GCDReduction = (1000 - (130 * (Player.Stat["SS"]-400) / 1900))/1000
            Player.EffectList.append(GCDReductionEffect)

        while(self.TimeStamp <= TimeLimit):

            for player in self.PlayerList:
                # if player.ActionSet[player.NextSpell] == None : player.TrueLock = True # Locking the player if None
                # Will first Check if the NextSpell is a GCD or not
                if(not player.TrueLock):# If it is we do nothing
                    if (player.ActionSet[player.NextSpell].GCD):
                        # Is a GCD
                        # Have to check if the player can cast the spell
                        # So check if Animation Lock, if Casting or if GCDLock
                        if(not (player.oGCDLock or player.GCDLock or player.Casting)):

                            player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)# Cast the spell
                            # Locking the player
                            # print(Player.CastingSpell.CastTime)
                            # input(Player.CastingSpell.RecastTime)
                            player.Casting = True
                            player.CastingLockTimer = player.CastingSpell.CastTime
                            player.GCDLock = True
                            player.GCDLockTimer = player.CastingSpell.RecastTime
                            player.CastingTarget = self.Enemy
                        # Else we do nothing since doing the nextspell is not currently possible


                    else:
                        # Is an oGCD
                        # print("Spell with id : " + str(player.ActionSet[player.NextSpell].id))
                        # input("is being casted at : " + str(self.TimeStamp))
                        
                        if(not (player.oGCDLock or player.Casting)):
                            # Then we can cast the oGCD
                            player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)
                            player.Casting = True
                            player.CastingLockTimer = player.CastingSpell.CastTime
                            player.CastingTarget = self.Enemy
                            #player.CastingSpell.CastFinal(player, self.Enemy)
                            player.oGCDLock = True
                            player.oGCDLockTimer = player.CastingSpell.CastTime
                            # print("oGCD with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(self.TimeStamp) )
            

            if self.Enemy.hasEventList and start :
                # Only goes through the Enemy's EventList if the fight has started AND if the Enemy has an event list
                if not self.Enemy.IsCasting:
                    # If the enemy is not casting
                    self.Enemy.EventList[self.Enemy.EventNumber].begin_cast(self.Enemy) # Begins the casting of the next event

                self.Enemy.UpdateTimer(TimeUnit) # Updating the Enemy's timers

            # Updating shield timer of all players
            for player in self.PlayerList:
                for shield in player.ShieldList: shield.UpdateTimer(TimeUnit)

            # Updating and casting DOT if needed
            for player in self.PlayerList:
                for DOT in player.DOTList:
                    DOT.CheckDOT(player,self.Enemy, TimeUnit)


                    
            for player in self.PlayerList:
                # Loops through the playerList
                # And calls every function in the player.EffectCDList
                # These functions will check if an effect should be terminated
                for CDCheck in player.EffectCDList:
                    CDCheck(player, self.Enemy)

                for remove in player.EffectToRemove:
                    # Loops through all effect that have been classified as terminated and removes them from the EffectCDList
                    player.EffectCDList.remove(remove) # Removing relevant spell
                for add in player.EffectToAdd:
                    # Adds any function to EffectCDList that should be added
                    player.EffectCDList.append(add)

                # Resets the list containing functions to be removed and added
                player.EffectToRemove = []
                player.EffectToAdd = []
            


            # We will now update any timer each player and the enemy has
            for player in self.PlayerList:
                player.updateTimer(TimeUnit)
                player.updateCD(TimeUnit)
                player.updateLock() # Update the lock on the player to see if the player's state changes

            if self.wipe: # If we detect that wipe has been set to true we stop the simulation. This for now only happens if a failedRequirement is fatal
                break


            for player in self.PlayerList:
                # Will go through all player and check if they have no more actions set to true. 
                # If so we will call the NextAction function
                if player.NoMoreAction:
                    # NextActionFunction is by default nothing and only returns True.
                    # But this function can be customized by the user to fit any use of it they might need
                    player.TrueLock = self.NextActionFunction(self, player)
                    if not player.TrueLock : player.NoMoreAction = False


            CheckFinalLock = True
            for player in self.PlayerList:
                # Goes through every player and checks if they are done. If everyone has nothing to do the fight finishes
                CheckFinalLock = player.TrueLock and CheckFinalLock # If all player's TrueLock is true, then CheckFinalLock will be True

            if CheckFinalLock: 
                if vocal : print("The Fight finishes at: " + str(self.TimeStamp))
                break
            
            
            if start:
                # If the fight has started, will sample DPS values at certain time.
                # The fight starts as soon as one player does damage.
                # The finished time is based on when the fight starts and not when the simulation starts.
                # If the simulation finishes before the fight starts there will be no damage done.
                if self.TimeStamp >= 3 and (isclose(self.TimeStamp%1, 0.25) or isclose(self.TimeStamp%1, 0.5) or isclose(self.TimeStamp%1, 0.75) or isclose(self.TimeStamp%1, 0)):# last thing is to ensure no division by zero and also to have no spike at the begining
                    # Samples DPS every frame of the simulation.
                    # If it becomes a problem if fights are too long, could limit rate of sampling.
                    self.timeValue+= [self.TimeStamp]
                    for Player in self.PlayerList:
                        Player.DPSGraph += [round(Player.TotalDamage/self.TimeStamp, 2)] # Rounding the value to 2 digits
                        Player.PotencyGraph += [round(Player.TotalPotency/self.TimeStamp, 2)]

            # Calling information extracting method
            self.ExtractInfo(self)

            # update self.TimeStamp
            self.TimeStamp += TimeUnit
            self.TimeStamp = round(self.TimeStamp, 2) # Round it for cleaner value

            if self.FightStart and not start:
                self.TimeStamp = 0
                start = True


        # Post fight computations

        remove = []

        for i in range(len(self.PlayerList)):  
            # Removing all instance of clones/summons from the fight. The DPS done has already been given to their master.
            player = self.PlayerList[i] 
            if player.JobEnum == JobEnum.Pet:
                remove += [i]

        k = 0
        for i in remove:
            self.PlayerList.pop(i-k)
            k+=1

        for t in self.failedRequirementList: # Printing the failed requirement if it was fatal
            if t.fatal : 
                print("The first failed fatal requirement was : " + t.requirementName)
                print("It happened at : " + str(t.timeStamp))

        # Printing the results if vocal is true.
        if vocal : PrintResult(self, self.TimeStamp, self.timeValue)
            


    def ComputeFunctions(self) -> None:
        """
        This function computes all relevant values needed to compute damage from potency using the stats of each player
        self : Fight -> Fight for which we want to compute the values (for all its players)
        """

        for Player in self.PlayerList:
            levelMod = 1900
            baseMain = 390  
            baseSub = 400# Level 90 LevelMod values

            JobMod = Player.JobMod # Level 90 jobmod value, specific to each job

            Player.f_WD = (Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))/100
            Player.f_DET = math.floor(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000# Determination damage
            if Player.RoleEnum == RoleEnum.Tank : Player.f_TEN = (1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000 # Tenacity damage, 1 for non-tank player
            else : Player.f_TEN = 1 # if non-tank
            Player.f_SPD = (1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000 # Used only for dots
            Player.CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000 # Crit rate in decimal
            Player.CritMult = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000 # Crit Damage multiplier
            Player.DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000 # DH rate in decimal

# HELPER FUNCTIONS UNDER

# GCDReduction Effect
def GCDReductionEffect(Player, Spell) -> None:
    """
    Computes the GCD reduction according to the SkillSpeed or the SpellSpeed of the player
    Player : player -> Player object
    Spell : Spell -> Spell object affected by the effect
    """
    if Spell.GCD:
        Spell.CastTime *= Player.GCDReduction
        Spell.RecastTime *= Player.GCDReduction

def ComputeDamage(Player, Potency, Enemy, SpellBonus, type, spellObj):

    """
    This function computes the damage from a given potency.
    Player : player -> player object doing the damage
    Potency : int -> potency value
    Enemy : Enemy -> Enemy object taking the damage
    SpellBonus : float -> Multiplying value to the final damage coming from the action itself
    type : int -> type of the action. 0 is Direct Damage, 1 is magical DOT, 2 is physical DOT and 3 is autos
    spellObj : Spell -> Object of the spell being casted

    """

    # The type input signifies what type of damage we are dealing with, since the computation will chance according to what
    # type of damage it is

    # type = 0 (Direct Damage), type = 1 (magical DOT), type = 2(physical DOT), type = 3 (Auto-attacks)

    # All relevant formulas were taken from https://finalfantasy.fandom.com/wiki/Final_Fantasy_XIV_attributes#Damage_and_healing_formulae ,
    # were given to me by javaJake#0001 on discord or were taken from the Allagan Studies discord server.
    # The formulas on the website assume a random function that will randomise the ouput. We instead compute the expected outcome.
    # Also thanks to whoever did the DPS computation code on the black mage gear comparison sheet : https://docs.google.com/spreadsheets/d/1t3EYSOPuMceqCFrU4WAbzSd4gbYi-J7YeMB36dNmaWM/edit# gid=654212594
    # It helped me a lot to understand better the DPS computation of this game
    # Also, note that this function is still in development, and so some of these formulas might be a bit off. Use at your own risk.
    # This function will compute the DPS given the stats of a player

    # These computations should be up to date with Endwalker.

    baseMain = 390  

    Enemy = Player.CurrentFight.Enemy # Enemy targetted


    if Player.JobEnum == JobEnum.Pet: MainStat = Player.Stat["MainStat"] # Summons do not receive bonus
    else: MainStat = math.floor(Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus) # Scaling %bonus on mainstat
    # Computing values used throughout all computations
    if Player.RoleEnum == RoleEnum.Tank : f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*156/baseMain))/100 # Tanks have a difference constant 
    else: f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*195/baseMain))/100
    # These values are all already computed since they do not change
    f_WD = Player.f_WD
    f_DET = Player.f_DET
    f_TEN = Player.f_TEN
    f_SPD = Player.f_SPD
    CritRate = (Player.CritRate)
    CritMult = Player.CritMult
    DHRate = Player.DHRate

    if Enemy.ChainStratagem: CritRate += 0.1    # If ChainStratagem is active, increase crit rate

    if Enemy.WanderingMinuet: CritRate += 0.02 # If WanderingMinuet is active, increase crit rate

    if Enemy.BattleVoice: DHRate += 0.2 # If BattleVoice is active, increase DHRate


    DHRate += Player.DHRateBonus # Adding Bonus
    CritRate += Player.CritRateBonus # Adding bonus

    # We will check if the ability is an assured crit and/ord DH, in which case we will have to buff the damage
    # Depending on the buffs the player is currently receiving

    auto_crit = False
    auto_DH = False
    CritRateBonus = CritRate # Saving value for later use if necessary
    DHRateBonus = DHRate # Saving value for later use if necessary

    if type == 0: # Making sure its not an AA or DOT
        if Player.JobEnum == JobEnum.Machinist: 
            # Then if machinist, has to check if direct crit guarantee
            if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].Weaponskill:    # Checks if reassemble is on and if its a weapon skill
                CritRate = 1
                DHRate = 1
                Player.Reassemble = False # Uses Reassemble    
                auto_crit = True
                auto_DH = True   
        elif Player.JobEnum == JobEnum.Warrior:
            if Player.InnerReleaseStack >= 1 and (Player.NextSpell < len(Player.ActionSet)) and (Player.ActionSet[Player.NextSpell].id == 9 or Player.ActionSet[Player.NextSpell].id == 8 or Player.ActionSet[Player.NextSpell].id == 10):
                CritRate = 1# If inner release weaponskill
                DHRate = 1
                Player.InnerReleaseStack -= 1
                auto_crit = True
                auto_DH = True
        elif Player.JobEnum == JobEnum.Samurai:
            if Player.DirectCrit:
                CritRate = 1
                DHRate = 1
                Player.DirectCrit = False
                auto_crit = True
                auto_DH = True
        elif Player.JobEnum == JobEnum.Dancer:
            if Player.NextDirectCrit:
                CritRate = 1
                DHRate = 1
                Player.NextDirectCrit = False
                auto_crit = True
                auto_DH = True
        elif Player.JobEnum == JobEnum.Dragoon:
            if Player.NextCrit and Player.ActionSet[Player.NextSpell].Weaponskill: # If next crit and weaponskill
                CritRate = 1
                Player.NextCrit = False
                auto_crit = True
        elif Player.JobEnum == JobEnum.Monk:
            if Player.GuaranteedCrit and Player.ActionSet[Player.NextSpell].Weaponskill:
                CritRate = 1
                Player.GuaranteedCrit = False
                auto_crit = True

    if type == 0: # Type 0 is direct damage
        Damage = math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN ) *f_WD) * Player.Trait) # Player.Trait is trait DPS bonus
        Damage = math.floor(Damage * SpellBonus)
        Player.NumberDamageSpell += 1
        Player.CritRateHistory += [CritRate]
    elif type == 1 : # Type 1 is magical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_WD) * f_MAIN_DMG) * f_SPD) * f_DET) * f_TEN) * Player.Trait) + 1
        
        if not spellObj.onceThroughFlag:# If we haven't gotten through with this DOT once, we have to snapshot the buffs

            if Enemy.ChainStratagem: spellObj.CritBonus += 0.1    # If ChainStratagem is active, increase crit rate
            if Enemy.WanderingMinuet: spellObj.CritBonus += 0.02 # If WanderingMinuet is active, increase crit rate
            if Enemy.BattleVoice: spellObj.DHBonus += 0.2 # If WanderingMinuet is active, increase DHRate
            spellObj.DHBonus += Player.DHRateBonus # Adding Bonus
            spellObj.CritBonus += Player.CritRateBonus # Adding bonus

            for buffs in Player.buffList: 
                spellObj.MultBonus += [buffs] # Adding buff to DOT
            for buffs in Enemy.buffList:
                spellObj.MultBonus += [buffs] # Adding buff to DOT

            # Now the DOT has completely snapshot all possible buff. So we save those
            # and never come back here

            spellObj.onceThroughFlag = True # set flag to True, so never snapshot again

    elif type == 2: # Physical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD) * f_WD) * Player.Trait) +1
    
        if not spellObj.onceThroughFlag:# If we haven't gotten through with this DOT once, we have to snapshot the buffs

            if Enemy.ChainStratagem: spellObj.CritBonus += 0.1    # If ChainStratagem is active, increase crit rate
            if Enemy.WanderingMinuet: spellObj.CritBonus += 0.02 # If WanderingMinuet is active, increase crit rate
            if Enemy.BattleVoice: spellObj.DHBonus += 0.2 # If WanderingMinuet is active, increase DHRate
            spellObj.DHBonus += Player.DHRateBonus # Adding Bonus
            spellObj.CritBonus += Player.CritRateBonus # Adding bonus

            for buffs in Player.buffList: 
                spellObj.MultBonus += [buffs] # Adding buff to DOT
            for buffs in Enemy.buffList:
                spellObj.MultBonus += [buffs] # Adding buff to DOT

            # Now the DOT has completely snapshot all possible buff. So we save those
            # and never come back here

            spellObj.onceThroughFlag = True # set flag to True, so never snapshot again

    elif type == 3: # Auto-attacks
        Damage = math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD)
        Damage = math.floor(math.floor(Damage * math.floor(f_WD * (Player.Delay/3) *100 )/100) * Player.Trait)
    # Now applying buffs

    if type == 0 or type == 3: # If Action or AA, then we apply the current buffs
        for buffs in Player.buffList: 
            Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all buffs
        for buffs in Enemy.buffList:
            Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all buffs
    else: # if type is 1 or 2, then its a DOT, so we have to use the snapshotted buffs
        for buffs in spellObj.MultBonus:
            Damage = math.floor(Damage * buffs.MultDPS)

    if spellObj.id == -2878: #If wildfire it cannot crit or DH, so we remove it
        non_crit_dh_expected, dh_crit_expected = Damage, Damage # Non crit expected damage, expected damage with crit
        return non_crit_dh_expected , dh_crit_expected

    
    if auto_crit and auto_DH: # If both 
        auto_crit_bonus = (1 + roundDown(CritRateBonus * CritMult, 3)) # Auto_crit bonus if buffed
        auto_dh_bonus = (1 + roundDown(DHRateBonus * 0.25, 2)) # Auto_DH bonus if buffed
        non_crit_dh_expected, dh_crit_expected = math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2)))
        return math.floor(math.floor(non_crit_dh_expected * auto_crit_bonus) * auto_dh_bonus), math.floor(math.floor(dh_crit_expected * auto_crit_bonus) * auto_dh_bonus)
    elif auto_crit: # If sure to crit, add crit to min expected damage
        auto_crit_bonus = (1 + roundDown(CritRateBonus * CritMult, 3)) # Auto_crit bonus if buffed
        non_crit_dh_expected, dh_crit_expected = math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2))) # If we have auto crit, we return full damage
        return math.floor(non_crit_dh_expected * auto_crit_bonus), math.floor(dh_crit_expected * auto_crit_bonus) 
    else:# No auto_crit or auto_DH
        non_crit_dh_expected, dh_crit_expected = math.floor(Damage * ( 1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2))) # Non crit expected damage, expected damage with crit
        return non_crit_dh_expected , dh_crit_expected



def isclose(a, b, rel_tol=1e-09, abs_tol=0.0): # Helper function to compare float
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def roundDown(x, precision):
    return math.floor(x * 10**precision)/10**precision
    # Imagine not having a built in function to rounddown floats :x
