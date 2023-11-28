import math
from copy import deepcopy
from ffxivcalc.helperCode.Vocal import PrintResult, SimulateRuns
from ffxivcalc.Jobs.PlayerEnum import *
from ffxivcalc.Jobs.ActionEnum import name_for_id
from ffxivcalc.Jobs.Base_Spell import ZIPAction, PreBakedAction
from ffxivcalc.helperCode.Progress import ProgressBar
from ffxivcalc.SimulationRecord.record import SimulationRecord, page
from ffxivcalc.helperCode.exceptions import playerIDNotFound

import matplotlib.pyplot as plt
import logging
from ffxivcalc.helperCode.helper_math import roundDown, isclose, roundUp
main_logging = logging.getLogger("ffxivcalc")
fight_logging = main_logging.getChild("Fight")


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

    def playerForID(self, id):
        """This function returns a reference to the player object that has the given ID in the fight.

        Args:
            id (int): id of the player we want.
        """

        for player in self.PlayerList:
            if player.playerID == id : return player

        raise playerIDNotFound
    
    def deepCopy(self):
        """This function returns a deepcopy of itself.
        We cannot use the deepcopy function alone since some issues arise.
        One such issue is that any action that targets a player will not have their target
        updated and will still target the player from the original fight (the one that is being deepcopied).
        To fix this we will look for the actions with target, get the targetID and replace these actions with the appropriate
        action that now targets the correct player.
        Note that because of how this is implemented, any fight object that has a buff given to another player must have both the caster
        and the target in its player list as if the target is not in the playerList it will not receive a valid ID.
        """
        from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import ClosedPosition
        from ffxivcalc.Jobs.Melee.Dragoon.Dragoon_Spell import DragonSight
        from ffxivcalc.Jobs.Healer.Astrologian.Astrologian_Spell import Balance, Arrow, Spear, Bole, Ewer, Spire

        dcFight = deepcopy(self)

        for player in dcFight.PlayerList:
            match player.JobEnum:
                case JobEnum.Dancer:
                    changeIndex = []
                    
                    for index,action in enumerate(player.ActionSet):
                        if action.id == 16006: # Closed Position
                            changeIndex.append((index,action.TargetPlayerObject.playerID))
                    for change in changeIndex:
                        player.ActionSet[change[0]] = ClosedPosition(dcFight.playerForID(change[1]))

                case JobEnum.Dragoon:
                    changeIndex = []
                    
                    for index,action in enumerate(player.ActionSet):
                        if action.id == 7398: # Dragoon Sight
                            changeIndex.append((index,action.TargetPlayerObject.playerID))
                    for change in changeIndex:
                        player.ActionSet[change[0]] = DragonSight(dcFight.playerForID(change[1]))
                case JobEnum.Astrologian:
                    changeIndex = []
                    
                    for index,action in enumerate(player.ActionSet):
                        if action.id >=4401 and action.id <=4406: # Arcanum
                            match action.id :
                                case 4401 : changeIndex.append((index,Balance(dcFight.playerForID(action.TargetPlayerObject.playerID))))
                                case 4402 : changeIndex.append((index,Arrow(dcFight.playerForID(action.TargetPlayerObject.playerID))))
                                case 4403 : changeIndex.append((index,Spear(dcFight.playerForID(action.TargetPlayerObject.playerID))))
                                case 4404 : changeIndex.append((index,Bole(dcFight.playerForID(action.TargetPlayerObject.playerID))))
                                case 4405 : changeIndex.append((index,Ewer(dcFight.playerForID(action.TargetPlayerObject.playerID))))
                                case 4406 : changeIndex.append((index,Spire(dcFight.playerForID(action.TargetPlayerObject.playerID))))

                    for change in changeIndex:
                        player.ActionSet[change[0]] = change[1]

        return dcFight

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
        self.MaxPotencyPlentifulHarvest = False # True will make Plentiful Harvest do max potency regardless of player.
        self.TimeUnit = 0
        self.nextID = 1 # Used to give ID to players. ID 0 is invalid

        self.simulationRecord = SimulationRecord() # Creating SimulationRecord object

                             # These values can only be eddited by manually changing the values by accessing the Fight object.
        self.SavePreBakedAction = False
        self.PlayerIDSavePreBakedAction = 0
        self.alwaysAllowConditionalAction = False # Having this value set to True will make the conditionalActions always happen for players in the fight.

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

        self.ComputeDamageFunction = ComputeDamage 
        self.ComputeHealingFunction = ComputeHeal
        self.NextActionFunction = DefaultNextActionFunction
        self.ExtractInfo = DefaultExtractInfo

    def AddPlayer(self, Players):
        for player in Players:
            player.CurrentFight = self
            self.PlayerList.append(player)
            player.playerID = self.nextID
            self.nextID += 1

    def SimulateZIPFight(self):
        """
        This function simulates the fight using the ZIPActionList of players. This will simulate a random DPS occurence
        and be used to compute a distribution.
        """

        for player in self.PlayerList:
            player_current_damage = 0
            for ZIPAction in player.ZIPActionSet:
                player_current_damage += ZIPAction.ComputeRandomDamage()
            player.ZIPDPSRun.append(round(player_current_damage/self.TimeStamp/20)*20)

    def SimulatePreBakedFight(self, Index : int, MainStat : int, f_WD : float, f_DET : float, f_TEN : float, f_SPD : float, f_CritRate : float, f_CritMult : float, f_DH : float, DHAuto : float, n : int = 1, getInfo : bool = False):
        """
        This function is called when the user wants to simulate the damage done by the pre baked actions. The player ID with
        the pre baked actions must be given. The user must also specify all the damage values computed from the stats.
        Index : int -> Index of the player with the PreBakedActions.
        n : int -> number of trial for random DPS simulation
        """
        player = self.PlayerList[Index]
        ExpectedDamage = 0
        baseMain = 390

        damageHistory = []   # This list will contain the damage of all PreBakedAction ComputeExpectedDamage used to
                             # faster compute RandomDamage

        countGCD = 0
        timeStamp = 0
        totalPotency = 0
        countGCD = 0
        #for history in player.PercentBuffHistory:
        #    fight_logging.warning(str(history))

                             # Will compute DPS
        for PreBakedAction in player.PreBakedActionSet:
                                                     # Count every GCD
            if PreBakedAction.isGCD : countGCD += 1                        
            timeStamp = PreBakedAction.timeStamp
                                         # Computing base MainStat for this action. If from pet do not get teamcomp bonus
            totalPotency += PreBakedAction.Potency
            curMainStat = MainStat * (PreBakedAction.MainStatPercentageBonus if not PreBakedAction.isFromPet else 1)

            fight_logging.debug("TimeStamp : " + str(timeStamp))
                                         # Potion
            if PreBakedAction.potionIsActive : curMainStat = math.floor(min(math.floor(curMainStat * 1.1), curMainStat + 262)) #Grade 8 HQ tincture
                                         # Any other percent bonus. Might have to remake dragoon tether since pet not affected by this buff

            for buff in PreBakedAction.buffList:
                PreBakedAction.PercentageBonus.append(buff.MultDPS)

            if PreBakedAction.IsTank : f_MAIN_DMG = (100+math.floor((curMainStat-baseMain)*156/baseMain))/100 # Tanks have a difference constant 
            else: f_MAIN_DMG = (100+math.floor((curMainStat-baseMain)*195/baseMain))/100
            ActionExpected, Damage = PreBakedAction.ComputeExpectedDamage(f_MAIN_DMG,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto) #if not actionFailsCondition else (0,0)
            ExpectedDamage += ActionExpected
            player.DamageInstanceList.append(ActionExpected)
            damageHistory.append(Damage)

                             # Will compute Random DPS
        #randomDPSRuns = []   # This list will contain all the DPS of the random runs
        #for run in range(n):
        #    CurrentDamage = 0
        #    index = 0
        #    for PreBakedAction in player.PreBakedActionSet:
        #        CurrentDamage += PreBakedAction.ComputeRandomDamage(damageHistory[index], f_CritRate,f_CritMult, f_DH)
        #        index += 1 
        #        
        #        if index == len(damageHistory) : break # Might have to break if we ommit some autos.

        #    randomDPSRuns.append(CurrentDamage/timeStamp)
                             # Sorting array so we can find the percentiles.
        #randomDPSRuns.sort()

        #Percent = int(n/100)
        #percentileRuns = {
        #    "1" :  0 if n < 100 else sum(randomDPSRuns[(Percent):(10*Percent-1)])/(len(randomDPSRuns[(Percent+1):(10*Percent-1)])),
        #    "10" : 0 if n < 100 else sum(randomDPSRuns[(10*Percent+1):(25*Percent-1)])/(len(randomDPSRuns[(10*Percent+1):(25*Percent-1)])),
        #    "25" : 0 if n < 100 else sum(randomDPSRuns[(25*Percent+1):(50*Percent-1)])/(len(randomDPSRuns[(25*Percent+1):(50*Percent-1)])),
        #    "50" : 0 if n < 100 else sum(randomDPSRuns[(50*Percent+1):(75*Percent-1)])/(len(randomDPSRuns[(50*Percent+1):(75*Percent-1)])),
        #    "75" : 0 if n < 100 else sum(randomDPSRuns[(75*Percent+1):(90*Percent-1)])/(len(randomDPSRuns[(75*Percent+1):(90*Percent-1)])),
        #    "90" : 0 if n < 100 else sum(randomDPSRuns[(90*Percent+1):(99*Percent-1)])/(len(randomDPSRuns[(90*Percent+1):(99*Percent-1)])),
        #    "99" : 0 if n < 100 else sum(randomDPSRuns[(99*Percent):])/(len(randomDPSRuns[(99*Percent):]))
        #}

        for preBakedAction in player.PreBakedActionSet: preBakedAction.resetPercentageBonus()


        fight_logging.debug("counted GCD  : " + str(countGCD))
        fight_logging.debug("previous GCD : " + str(player.GCDCounter))
        if getInfo : return round(ExpectedDamage/timeStamp,2), ExpectedDamage, timeStamp, totalPotency
        return round(ExpectedDamage/timeStamp if True else ExpectedDamage,2), {}

        


    def SimulateFight(self, TimeUnit, TimeLimit, vocal, PPSGraph : bool = True, MaxTeamBonus : bool = False, MaxPotencyPlentifulHarvest : bool = False, n = 0, showProgress : bool = True,
                      computeGraph : bool = True) -> None:

        """
        This function will Simulate the fight given the enemy and player list of this Fight
        It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
        It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
        However, no direct computation is done in this function, it simply orchestrates the whole thing

        TimeUnit : float -> unit at which the simulator will advance through time in the simulation
        TimeLimit : float -> time limit at which the simulator will stop
        vocal : bool -> True if we want to print out the results
        verbose (bool) -> True if we want the fight to record logs. The log file will be saved in the same folder the python script was executed from
        loglevel (str) -> level at which we want the logging to record.
        PPSGraph (bool) = True -> If we want the PPS graph to be next to the DPS graph
        MaaxTeamBonus (bool) = False -> If true, gives the 5% bonus regardless of team comp
        showProgress (bool) = True -> If true show fight progress bar.
        computeGraph (bool) = True -> If true will process the Graphs even if they do not show.
        """
        self.MaxPotencyPlentifulHarvest = MaxPotencyPlentifulHarvest
        self.TimeStamp = 0   # Keep track of the time
        start = False
        self.TimeUnit = TimeUnit

        self.showProgress = showProgress
        self.computeGraph = computeGraph


        self.timeValue = []  # Used for graph

        self.ComputeFunctions() # Compute all damage functions for the players


                             # Checks if every player has a least one action. If not
                             # we put True Lock
        for player in self.PlayerList:
            if len(player.ActionSet) == 0 : player.TrueLock = True

        # The first thing we will do is compute the TEAM composition DPS bonus
        # each class will give 1%
        # Tank, Healer, Caster, Ranged, Melee
        if MaxTeamBonus:
            self.TeamCompositionBonus = 1.05
        else:
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

        for Player in self.PlayerList:
            Player.Stat["MainStat"] = math.floor(Player.Stat["MainStat"] * self.TeamCompositionBonus) # Scaling %bonus on mainstat

        # Will first compute each player's GCD reduction value based on their Spell Speed and Skill Speed Value
        for Player in self.PlayerList:
            Player.SpellReduction = (1000 - math.floor(130 * (Player.Stat["SS"]-400) / 1900))/1000
            Player.WeaponskillReduction = (1000 - math.floor(130 * (Player.Stat["SkS"]-400) / 1900))/1000
            Player.EffectList.append(GCDReductionEffect)
                                         # Computing AA delay
            Player.currentDelay = math.floor(math.floor(int(Player.baseDelay * 1000 ) * (100 - Player.Haste)/100)/10)/100

        fight_logging.debug("Starting simulation with TeamCompositionBonus = " + str(self.TeamCompositionBonus))
        fight_logging.debug("Parameters are -> RequirementOn : " + str(self.RequirementOn) + ", IgnoreMana : " + str(self.IgnoreMana))
        if self.showProgress:
            pB = ProgressBar.init(int(TimeLimit/TimeUnit), "Progress Of Fight (maxTime)")
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
                            if player.CastingSpell.id > 0 and player.JobEnum != JobEnum.Pet:
                                log_str = ( "Timestamp : " + str(self.TimeStamp)
                                + " , Event : begin_cast_GCD"
                                + " , playerID : " + str(player.playerID)
                                + " , Ability : " + name_for_id(player.CastingSpell.id,player.ClassAction, player.JobAction) )

                                fight_logging.debug(log_str)

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
                            player.oGCDLock = True
                            player.oGCDLockTimer = player.CastingSpell.CastTime

                            if player.CastingSpell.id > 0 and player.JobEnum != JobEnum.Pet:
                                log_str = ( "Timestamp : " + str(self.TimeStamp)
                                + " , Event : begin_cast_oGCD"
                                + " , playerID : " + str(player.playerID)
                                + " , Ability : " + name_for_id(player.CastingSpell.id,player.ClassAction, player.JobAction) )
                                
                                fight_logging.debug(log_str)
                

            if self.Enemy.hasEventList and start :
                # Only goes through the Enemy's EventList if the fight has started AND if the Enemy has an event list
                if not self.Enemy.IsCasting:
                    # If the enemy is not casting
                    self.Enemy.EventList[self.Enemy.EventNumber].begin_cast(self.Enemy) # Begins the casting of the next event

                self.Enemy.UpdateTimer(TimeUnit) # Updating the Enemy's timers

                        # We will now update any timer each player and the enemy has
            for player in self.PlayerList:
                player.updateTimer(TimeUnit)
                player.updateCD(TimeUnit)
                player.updateLock() # Update the lock on the player to see if the player's state changes
                                    # Castfinal is being called in player.updateLock() if it applies.

            # Updating shield timer and healing buff timer of all players
            for player in self.PlayerList:
                for shield in player.ShieldList: shield.UpdateTimer(TimeUnit) # Update shield timer
                for buff in player.ReceivedHealBuffList : buff.UpdateTimer(TimeUnit) # Update buff on received heal timer
                for buff in player.GivenHealBuffList : buff.UpdateTimer(TimeUnit) # Update buff on given heal timer
                for buff in player.MitBuffList : buff.UpdateTimer(TimeUnit) # Update Mit buff timer
                    
            for player in self.PlayerList:
                # Loops through the playerList
                # And calls every function in the player.EffectCDList
                # These functions will check if an effect should be terminated
                for CDCheck in player.EffectCDList:
                    CDCheck(player, self.Enemy)

                for remove in player.EffectToRemove:
                    # Loops through all effect that have been classified as terminated and removes them from the EffectCDList
                    player.EffectCDList.remove(remove) # Removing relevant spell
                    fight_logging.debug("Removing Check function : " + remove.__name__ + " TimeStamp : " + str(self.TimeStamp))
                for add in player.EffectToAdd:
                    # Adds any function to EffectCDList that should be added
                    player.EffectCDList.append(add)

                # Resets the list containing functions to be removed and added
                player.EffectToRemove = []
                player.EffectToAdd = []

            
            for player in self.PlayerList:
                             # Recomputing recastTime if new Haste has been added.
                             # Note that I am not certain if this goes here or in CastFinal.
                             # Having the recomputeRecastLock here means that as soon as a haste buff is applied
                             # it recomptes the recast lock based on the haste change. recomputeRecastLock()
                             # changes the aaDelay, current AATimer and the current recast lock but it does NOT
                             # recompute the current casting timer. This is because if you APPLY a haste buff it is either
                             # a GCD effect or an oGCD, meaning when you apply the casting timer should always be 0.
                             # And when the haste buff gets removed I BELIEVE that it does not affect the CURRENT casting
                             # but it will affect the recast. Hence why we do not recompute the casting timer (at least I think it works like that).
                if player.hasteHasChanged: 
                    player.recomputeRecastLock(isSpell=(player.RoleEnum == RoleEnum.Caster))
                for DOT in player.DOTList:
                    DOT.CheckDOT(player,self.Enemy, TimeUnit)


            if self.wipe: # If we detect that wipe has been set to true we stop the simulation. This for now only happens if a failedRequirement is fatal
                break


            for player in self.PlayerList:
                # Will go through all player and check if they have no more actions set to true. 
                # If so we will call the NextAction function
                if player.NoMoreAction:
                    # NextActionFunction is by default nothing and only returns True.
                    # But this function can be customized by the user to fit any use of it they might need
                    player.TrueLock = self.NextActionFunction(self, player)
                    if not player.TrueLock : 
                        player.NoMoreAction = False
                        player.NoMoreActionLog = True
                        log_str = "Player ID " + str(player.playerID) + " has received other actions to do, Timestamp : " + str(self.TimeStamp)
                        fight_logging.debug(log_str)
                    elif player.NoMoreActionLog:
                        player.NoMoreActionLog = False # We want this log to only happen once everytime the player has no more actions
                        log_str = "Player ID " + str(player.playerID) + " has no more actions, Timestamp : " + str(self.TimeStamp)
                        fight_logging.debug(log_str)


            CheckFinalLock = True
            for player in self.PlayerList:
                # Goes through every player and checks if they are done. If everyone has nothing to do the fight finishes
                CheckFinalLock = player.TrueLock and CheckFinalLock # If all player's TrueLock is true, then CheckFinalLock will be True
                

            if CheckFinalLock: 
                log_str = "Simulation has succesfully finished."
                fight_logging.debug(log_str)
                break
            
            
            if start:
                # If the fight has started, will sample DPS values at certain time.
                # The fight starts as soon as one player does damage.
                # The finished time is based on when the fight starts and not when the simulation starts.
                # If the simulation finishes before the fight starts there will be no damage done.
                if self.TimeStamp >= 1 and (isclose(self.TimeStamp%1, 0.25) or isclose(self.TimeStamp%1, 0.5) or isclose(self.TimeStamp%1, 0.75) or isclose(self.TimeStamp%1, 0)):# last thing is to ensure no division by zero and also to have no spike at the begining
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
            self.TimeStamp = round(self.TimeStamp,2) # Round it for cleaner value
            if vocal and self.FightStart and self.showProgress: next(pB)

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

        result_str = ""

        if self.wipe:
            # If the simulation ran into a problem caused by a failed requirement.
            result_str = "The simulation ran into a problem. You can disable requirements by setting its value to 'False' in the JSON file.\n" + "=================\n"
            for t in self.failedRequirementList: # Printing the failed requirement if it was fatal
                if t.fatal : 
                    result_str += (
                        "Failed Fatal Requirement : " + t.requirementName + " Timestamp : " + str(t.timeStamp)
                        )
                             # Recording final HP value of players
        for gamer in self.PlayerList:
            gamer.HPGraph[0].append(self.TimeStamp)
            gamer.HPGraph[1].append(gamer.HP)

        # Printing the results if vocal is true.
        if vocal and self.TimeStamp < TimeLimit: pB.complete()
        fig2 = None
        if n > 0 and vocal : fig2 = SimulateRuns(self, n)
        if computeGraph : result, fig = PrintResult(self, self.TimeStamp, self.timeValue, PPSGraph=PPSGraph)
        else : result, fig = "", None
        if vocal:
            print(result) 
            #plt.show()

        
        return result, fig, fig2
            
    def ComputeFunctions(self) -> None:
        """
        This function computes all relevant values needed to compute damage from potency using the stats of each player
        self : Fight -> Fight for which we want to compute the values (for all its players)
        """

        fight_logging.debug("Initializing damage values for all players.")

        for Player in self.PlayerList:
            levelMod = 1900
            baseMain = 390  
            baseSub = 400# Level 90 LevelMod values

            JobMod = Player.JobMod # Level 90 jobmod value, specific to each job

            Player.f_WD = (Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))/100 # Necessary to check if its not 0 since etro only returns the damage multiplier.
            Player.f_DET = math.floor(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000# Determination damage
            if Player.RoleEnum == RoleEnum.Tank : Player.f_TEN = (1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000 # Tenacity damage, 1 for non-tank player
            else : Player.f_TEN = 1 # if non-tank
            Player.f_SPD = (1000+math.floor(130*((Player.Stat["SS"] if Player.RoleEnum == RoleEnum.Caster or Player.RoleEnum == RoleEnum.Healer else Player.Stat["SkS"])-baseSub)/levelMod))/1000 # Used only for dots
            Player.CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000 # Crit rate in decimal
            Player.CritMult = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000 # Crit Damage multiplier
            Player.DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000 # DH rate in decimal
            Player.DHAuto = math.floor(140*(Player.Stat["DH"]-baseSub)/levelMod)/1000 # DH bonus when auto crit/DH
                             # I was using baseMain for DHAuto, but I think that might be wrong based on what
                             # is in the tankcalc gear sheet. I have not yet confirmed which is the correct one to use.
            
            log_str = ("ID : " + str(Player.playerID) + " , Job : " + JobEnum.name_for_id(Player.JobEnum) 
            + " , f_WD : " + str(Player.f_WD) 
            + " , f_DET : " + str(Player.f_DET) 
            + " , f_TEN : " + str(Player.f_TEN) 
            + " , f_SPD : " + str(Player.f_SPD) 
            + " , f_CritRate : " + str(Player.CritRate) 
            + " , f_CritMult : " + str(Player.CritMult)
            + " , f_DHRate : " + str(Player.DHRate)  
            + ", f_DHAuto : " + str(Player.DHAuto))

            fight_logging.debug(log_str)

# HELPER FUNCTIONS UNDER

# GCDReduction Effect

def GCDReductionEffect(Player, Spell) -> None:
    """
    Computes the GCD reduction according to the SkillSpeed or the SpellSpeed of the player
    Player : player -> Player object
    Spell : Spell -> Spell object affected by the effect
    """

    if Spell.type == 1: # Spell
        Spell.CastTime = math.floor(math.floor(math.floor((int(Spell.CastTime * 1000 ) * Player.SpellReduction)) * (100 - Player.Haste)/100)/10)/100  if Spell.CastTime > 0 else 0
        Spell.RecastTime = math.floor(math.floor(math.floor((int(Spell.RecastTime * 1000 ) * Player.SpellReduction)) * (100 - Player.Haste)/100)/10)/100
        if Spell.RecastTime < 1.5 and Spell.RecastTime > 0 : Spell.RecastTime = 1.5 # A GCD cannot go under 1.5 sec
    elif Spell.type == 2: # Weaponskill
        Spell.CastTime = math.floor(math.floor(math.floor((int(Spell.CastTime * 1000 ) * Player.WeaponskillReduction)) * (100 - Player.Haste)/100)/10)/100 if Spell.CastTime > 0 else 0
        Spell.RecastTime = math.floor(math.floor(math.floor((int(Spell.RecastTime * 1000 ) * Player.WeaponskillReduction)) * (100 - Player.Haste)/100)/10)/100
        if Spell.RecastTime < 1.5 and Spell.RecastTime > 0 : Spell.RecastTime = 1.5 # A GCD cannot go under 1.5 sec

# Compute Damage
def ComputeDamage(Player, Potency, Enemy, SpellBonus, type, spellObj, SavePreBakedAction : bool = False, PlayerIDSavePreBakedAction : int = 1) -> float:

    """
    This function computes the damage from a given potency.
    Player : player -> player object doing the damage
    Potency : int -> potency value
    Enemy : Enemy -> Enemy object taking the damage
    SpellBonus : float -> Multiplying value to the final damage coming from the action itself
    type : int -> type of the action. 0 is Direct Damage, 1 is magical DOT, 2 is physical DOT and 3 is autos
    spellObj : Spell -> Object of the spell being casted
    SavePreBakedAction : bool -> If we want the simulator to save the PreBakedAction to the player's list. False by default.
    PlayerIDSavePreBakedAction : int -> ID of the player for which we want to record the PreBakedActions.
    """

                             # Creating page object to record action
    thisPage = page()
    thisPage.setPlayerID(Player.playerID)
    Player.CurrentFight.simulationRecord.addPage(thisPage)
    thisPage.setName(name_for_id(spellObj.id, Player.ClassAction, Player.JobAction))
    thisPage.setPotency(Potency)
    thisPage.setTimeStamp(Player.CurrentFight.TimeStamp)

    # Checking if under pot for record (only if not DOT)
    if Player.PotionTimer > 0 and (type != 1 and type != 2): thisPage.setHasPotion()

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
    isPet = (Player.JobEnum == JobEnum.Pet)
    isTank = Player.RoleEnum == RoleEnum.Tank or (isPet and Player.Master.RoleEnum == RoleEnum.Tank)
    MainStat = Player.Stat["MainStat"]
    # Computing values used throughout all computations
    if isTank : f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*156/baseMain))/100 # Tanks have a difference constant 
    else: f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*195/baseMain))/100
    # These values are all already computed since they do not change
    f_WD = Player.f_WD
    f_DET = Player.f_DET
    f_TEN = Player.f_TEN
    f_SPD = Player.f_SPD
    CritRate = (Player.CritRate)
    CritMult = Player.CritMult
    DHRate = Player.DHRate
    CritRateBonus = Player.CritRateBonus
    DHRateBonus = Player.DHRateBonus # Saving value for later use if necessary
    f_DET_DH = math.floor((f_DET + Player.DHAuto) * 1000 ) / 1000

                             # Check if DOT. If not we take current buffs.
                             # If is a dot we take snapshotted buffs.
    if (type == 0 or type == 3) or not spellObj.onceThroughFlag:
        if round(Player.CritRateBonus,2) > 0 : thisPage.addCritBuffList(("Other", Player.CritRateBonus))
        if round(Player.DHRateBonus,2) > 0 : thisPage.addDHBuffList(("Other", Player.DHRateBonus))

        if Enemy.ChainStratagem: 
            CritRateBonus += 0.1    # If ChainStratagem is active, increase crit rate
            thisPage.addCritBuffList(("CS", 0.1))

        if Enemy.WanderingMinuet: 
            CritRateBonus += 0.02 # If WanderingMinuet is active, increase crit rate
            thisPage.addCritBuffList(("WM", 0.02))

        if Enemy.ArmyPaeon: 
            DHRateBonus += 0.03 # If WanderingMinuet is active, increase crit rate
            thisPage.addDHBuffList(("AP", 0.03))

        if Enemy.BattleVoice: 
            DHRateBonus += 0.2 # If BattleVoice is active, increase DHRate
            thisPage.addDHBuffList(("BV", 0.2))
    else:
                             # If dot and has gone through once (so has snapshotted buff) we use them
                             # This only considers Crit,DH and Pot snapshot
        DHRateBonus = spellObj.DHBonus
        if round(DHRateBonus, 2) > 0 : thisPage.addDHBuffList(("DOTSnapshot", DHRateBonus))
        CritRateBonus = spellObj.CritBonus
        if round(CritRateBonus, 2) > 0 : thisPage.addCritBuffList(("DOTSnapshot", CritRateBonus))

                             # Checking if ChainStratagem clips since ground DOT do not clip
                             # Debuff
        if spellObj.isGround and Enemy.ChainStratagem:
            CritRateBonus += 0.1    # If ChainStratagem is active, increase crit rate
            thisPage.addCritBuffList(("CS", 0.1))
        
        if spellObj.potSnapshot : 
                             # We have to recompute f_AP.
            if Player.PotionTimer <= 0 :
                             # If a potion is already applied f_MAIN_DMG won't change so we skip
                             # So we only change f_MAIN_DMG when the potion is no longer active
                             # on the player but the DOT has it snapshotted.
                mainStatBonus = min(int(MainStat * 0.1), 262)
                if isTank : f_MAIN_DMG = (100+math.floor(((MainStat+mainStatBonus)-baseMain)*156/baseMain))/100 # Tanks have a difference constant 
                else: f_MAIN_DMG = (100+math.floor(((MainStat+mainStatBonus)-baseMain)*195/baseMain))/100
            thisPage.setHasPotion()
        elif not spellObj.potSnapshot and Player.PotionTimer > 0:
                             # If not snapshot Potion BUT potion is currently applied
                             # We have to recalculate f_MAIN_DMG using the lower
                             # MainStatvalue
            if isTank : f_MAIN_DMG = (100+math.floor(((MainStat-Player.mainStatBonus)-baseMain)*156/baseMain))/100 # Tanks have a difference constant 
            else: f_MAIN_DMG = (100+math.floor(((MainStat-Player.mainStatBonus)-baseMain)*195/baseMain))/100
    DHRate += DHRateBonus# Adding Bonus
    CritRate += CritRateBonus# Adding bonus

    # We will check if the ability is an assured crit and/ord DH, in which case we will have to buff the damage
    # Depending on the buffs the player is currently receiving

    auto_crit = False
    auto_DH = False

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
            fight_logging.debug("Inner Release Stack : " + str(Player.InnerReleaseStack))        # Primal Rend                                     # Fell Cleave                                    # Inner Chaos
            if (Player.NextSpell < len(Player.ActionSet)) and (Player.ActionSet[Player.NextSpell].id == 25753 or (Player.ActionSet[Player.NextSpell].id == 3549 and Player.InnerReleaseStack > 0) or Player.ActionSet[Player.NextSpell].id == 16465):
                CritRate = 1# If inner release weaponskill
                DHRate = 1
                             # Remove stack if fell cleave
                if Player.ActionSet[Player.NextSpell].id == 3549 : Player.InnerReleaseStack -= 1
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

    if type == 0: fight_logging.debug(str((Player.Stat["MainStat"],f_MAIN_DMG, f_WD, f_DET, f_TEN, f_SPD, CritRate, CritMult, DHRate)))


    if type == 0: # Type 0 is direct damage
        #Damage = Potency * f_MAIN_DMG * f_DET * f_TEN  *f_WD * Player.Trait
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG) * (f_DET_DH if auto_crit and auto_DH else f_DET)) * f_TEN ) *f_WD) * Player.Trait) # Player.Trait is trait DPS bonus
        Damage = math.floor(Damage * SpellBonus)
        Player.NumberDamageSpell += 1
        Player.CritRateHistory += [CritRate]
    elif type == 1 : # Type 1 is magical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_WD) * f_MAIN_DMG) * f_SPD) * f_DET) * f_TEN) * Player.Trait) + 1
        
        if not spellObj.onceThroughFlag:# If we haven't gotten through with this DOT once, we have to snapshot the buffs


            spellObj.DHBonus = DHRateBonus # Adding Bonus
                             # Adding Crit bonus but removing ChainStratagem if groundDOT since
                             # Chain Strat is a debuff.
            spellObj.CritBonus = CritRateBonus - (0.1 if spellObj.isGround and Enemy.ChainStratagem else 0)
            spellObj.potSnapshot = Player.PotionTimer > 0 # Checking Potion

            for buffs in Player.buffList: 
                             # Adding buff to DOT only if not (ground and debuff) since ground DOT
                             # do not snapshot debuff.
                if not (spellObj.isGround and buffs.isDebuff) : spellObj.MultBonus += [buffs] 
            for buffs in Enemy.buffList:
                             # Adding buff to DOT only if not (ground and debuff) since ground DOT
                             # do not snapshot debuff.
                if not (spellObj.isGround and buffs.isDebuff) : spellObj.MultBonus += [buffs] 

            # Now the DOT has completely snapshot all possible buff. So we save those
            # and never come back here

            spellObj.onceThroughFlag = True # set flag to True, so never snapshot again

    elif type == 2: # Physical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG) * f_DET) * f_TEN) * f_SPD) * f_WD) * Player.Trait) +1
    
        if not spellObj.onceThroughFlag:# If we haven't gotten through with this DOT once, we have to snapshot the buffs

            spellObj.DHBonus = DHRateBonus # Adding DH Bonus
                             # Adding Crit bonus but removing ChainStratagem if groundDOT since
                             # Chain Strat is a debuff.
            spellObj.CritBonus = CritRateBonus - (0.1 if spellObj.isGround and Enemy.ChainStratagem else 0)
            spellObj.potSnapshot = Player.PotionTimer > 0 # Checking Potion

            for buffs in Player.buffList: 
                             # Adding buff to DOT only if not (ground and debuff) since ground DOT
                             # do not snapshot debuff.
                if not (spellObj.isGround and buffs.isDebuff) : spellObj.MultBonus += [buffs] 
            for buffs in Enemy.buffList:
                             # Adding buff to DOT only if not (ground and debuff) since ground DOT
                             # do not snapshot debuff.
                if not (spellObj.isGround and buffs.isDebuff) : spellObj.MultBonus += [buffs] 

            # Now the DOT has completely snapshot all possible buff. So we save those
            # and never come back here

            spellObj.onceThroughFlag = True # set flag to True, so never snapshot again

    elif type == 3: # Auto-attacks
        Damage = math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG) * f_DET) * f_TEN) * f_SPD)
        Damage = math.floor(math.floor(Damage * math.floor(f_WD * (Player.baseDelay/3) *100 )/100) * Player.Trait)
    # Now applying buffs

    if type == 0 or type == 3 or not spellObj.onceThroughFlag: # If Action or AA, then we apply the current buffs
        for buffs in Player.buffList: 
            Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all buffs
            thisPage.addPercentBuff(buffs)
        for buffs in Enemy.buffList:
            Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all buffs
            thisPage.addPercentBuff(buffs)
    else: # if type is 1 or 2, then its a DOT, so we have to use the snapshotted buffs
        for buffs in spellObj.MultBonus:
            Damage = math.floor(Damage * buffs.MultDPS)
            thisPage.addPercentBuff(buffs)
                             # If DOT is a ground DOT we have to add buffs that are debuff
        if spellObj.isGround:
            for buffs in Player.buffList: 
                if buffs.isDebuff:
                    Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all debuffs
                    thisPage.addPercentBuff(buffs)
            for buffs in Enemy.buffList:
                if buffs.isDebuff:
                    Damage = math.floor(Damage * buffs.MultDPS) # Multiplying all debuffs
                    thisPage.addPercentBuff(buffs)


    if SavePreBakedAction and (Player.playerID == PlayerIDSavePreBakedAction or (isPet and Player.Master.playerID == PlayerIDSavePreBakedAction)): 
        """
        If that is set to true we will record all we need and will not compute the rest.
        We will check if the action is a GCD with recast time of lesser or equal to 1.5s since the GCD
        cannot go lower. The total time will be remembered and substracted from the total time that is reduceable from more SpS.
        """
                             # Snapshotting all buff on that action.
        buffList = []
        potActive = False
        if type == 0 or type == 3 or not spellObj.onceThroughFlag:
                             # if AA or action take all curent buff/debuff
            for buff in Player.buffList:
                buffList.append(buff)
            for buff in Enemy.buffList:
                buffList.append(buff)

            potActive = Player.PotionTimer > 0 or (isPet and Player.Master.PotionTimer > 0)

        else:
                             # If is DOT we take the snapshotted buffs + debuff if ground
            for buff in spellObj.MultBonus:
                buffList.append(buff)
                             # If DOT is a ground DOT we have to add buffs that are debuff
            if spellObj.isGround:
                for buff in Player.buffList: 
                    if buff.isDebuff: buffList.append(buff)
                for buff in Enemy.buffList:
                    if buff.isDebuff: buffList.append(buff)

            potActive = spellObj.potSnapshot

        if auto_crit and auto_DH : fight_logging.debug("Auto Crit/DH prebaked")
        elif auto_crit : fight_logging.debug("Auto Crit prebaked")

        nonReducableStamp = 0 if not Player.CurrentFight.FightStart else Player.totalTimeNoFaster
        reducableStamp = 0 if not Player.CurrentFight.FightStart else Player.CurrentFight.TimeStamp - Player.totalTimeNoFaster

        gcdLockTimer = max(spellObj.notRoundRecastTime, spellObj.notRoundCastTime) if spellObj.GCD  and (Player.RoleEnum != RoleEnum.Pet) and max(spellObj.notRoundRecastTime, spellObj.notRoundCastTime) > 1.5 else 0
        if spellObj.GCD and (Player.RoleEnum == RoleEnum.Melee or Player.RoleEnum == RoleEnum.Tank) and spellObj.type == 1 : gcdLockTimer = 0
        elif spellObj.GCD and (Player.RoleEnum == RoleEnum.Caster) and spellObj.type == 2 : gcdLockTimer = 0
        
        newPreBaked = PreBakedAction(isTank, Player.CurrentFight.TeamCompositionBonus,buffList, Player.Trait, Potency, type,Player.CurrentFight.TimeStamp if Player.CurrentFight.FightStart else 0, nonReducableStamp + (0 if type == 0 else reducableStamp), 
                                     reducableStamp if type == 0 else 0 ,AutoCrit=auto_crit, AutoDH=auto_DH, isFromPet=isPet, isGCD=spellObj.GCD,gcdLockTimer=gcdLockTimer,spellDPSBuff=SpellBonus, isConditionalAction=spellObj.conditionalAction)
                             # Giving dh and crit bonus
        newPreBaked.CritBonus = CritRateBonus
        newPreBaked.DHBonus = DHRateBonus
        newPreBaked.potionIsActive = potActive
                             # have to specific if is wildfire
        if spellObj.id == -2878 : newPreBaked.isWildfire = True

        (Player if not isPet else Player.Master).PreBakedActionSet.append(newPreBaked)
        
        return Potency, Potency        # Exit the function since we are not interested in the immediate damage value. Still return potency as to not break the fight's duration.


    if spellObj.id == -2878: #If wildfire it cannot crit or DH, so we remove it
        non_crit_dh_expected, dh_crit_expected = Damage, Damage # Non crit expected damage, expected damage with crit
        (Player if Player.JobEnum != JobEnum.Pet else Player.Master).ZIPActionSet.append(ZIPAction(Damage, 0, CritMult, 0))
        thisPage.setDamage(dh_crit_expected)
        return non_crit_dh_expected , dh_crit_expected

    
    if auto_crit and auto_DH: # If both 
        fight_logging.debug("Auto Crit/DH")
        auto_crit_bonus = (1 + CritRateBonus * CritMult) # Auto_crit bonus if buffed
        fight_logging.debug("CritRate : " + str(CritRateBonus) + " autocritbonus : " + str(auto_crit_bonus))
        auto_dh_bonus = (1 + DHRateBonus * 0.25) # Auto_DH bonus if buffed
        fight_logging.debug("DHRateBonus : " + str(DHRateBonus) + " autodhbonus : " + str(auto_dh_bonus))
        non_crit_dh_expected, dh_crit_expected =  0, math.floor(math.floor(Damage * (1 + CritMult) ) * (1.25)) 
        (Player if Player.JobEnum != JobEnum.Pet else Player.Master).ZIPActionSet.append(ZIPAction(Damage, 1, CritMult, 1, auto_crit=True, auto_dh=True, AutoCritBonus=auto_crit_bonus, AutoDHBonus=auto_dh_bonus))
        Damage = math.floor(math.floor(dh_crit_expected * auto_crit_bonus) * auto_dh_bonus)
        thisPage.setDamage(Damage)
        thisPage.setAutoCrit(True)
        thisPage.setAutoDH(True)
        return 0, Damage
    elif auto_crit: # If sure to crit, add crit to min expected damage
        fight_logging.debug("Auto Crit")
        auto_crit_bonus = (1 + CritRateBonus * CritMult) # Auto_crit bonus if buffed
        non_crit_dh_expected, dh_crit_expected = ( 0, 
                                                   math.floor(math.floor(Damage * (1 + CritMult) ) * (1 + (DHRate * 0.25))) )# If we have auto crit, we return full damage
        (Player if Player.JobEnum != JobEnum.Pet else Player.Master).ZIPActionSet.append(ZIPAction(Damage, 1, CritMult, DHRate, auto_crit=True, AutoCritBonus=auto_crit_bonus ))
        Damage = math.floor(dh_crit_expected * auto_crit_bonus) 
        thisPage.setDamage(Damage)
        thisPage.setAutoCrit(True)
        return 0, Damage
    else:# No auto_crit or auto_DH
        non_crit_dh_expected, dh_crit_expected = 0, math.floor(math.floor(Damage * (1 + (CritRate * CritMult)) ) * (1 + (DHRate * 0.25))) # Non crit expected damage, expected damage with crit
        (Player if Player.JobEnum != JobEnum.Pet else Player.Master).ZIPActionSet.append(ZIPAction(Damage, CritRate, CritMult, DHRate))
        Damage = dh_crit_expected
        thisPage.setDamage(Damage)
        return 0 , Damage

# Compute Healing
def ComputeHeal(Player, Potency, Target, SpellBonus, type, spellObj) -> float:
    """This function computes and returns the healing done by an action.

    Args:
        Player (Player): Player casting the action
        Potency (int): Potency of the heal
        Target (Player): Target of the healing
        SpellBonus (float): Bonus of the spell
        type (int): Type of the action. type = 1 is Direct Heal, Type = 2 is DOT heal
        spellObj (Spell): Object corresponding to the action being casted
    """
    baseMain = 390  


    if Player.JobEnum == JobEnum.Pet: MainStat = Player.Stat["MainStat"] # Summons do not receive bonus
    else: MainStat = math.floor(Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus) # Scaling %bonus on mainstat
    # Computing values used throughout all computations
    f_MAIN_heal = (100+math.floor((MainStat-baseMain)*304/baseMain))/100
    # These values are all already computed since they do not change
    f_WD = Player.f_WD
    f_DET = Player.f_DET
    f_TEN = Player.f_TEN
    f_SPD = Player.f_SPD
    CritRate = Player.CritRate
    CritMult = Player.CritMult
    
    # WARNING
    # THESE CONSTANTS ARE PROBABLY WRONG. I HAVE NOT VERIFIED AND AM SIMPLY USING THOSE IN ORDER TO TEST THE CODE.
    
    if type == 1: # Direct Heal
        H_1 = math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_heal * f_DET) * f_DET) * f_TEN) * f_WD ) * Player.Trait)
        H_1_min = math.floor(H_1 * 97/100) # Minimal healing done
        H_1_expected_crit = math.floor(H_1 * (1 + round((CritRate * CritMult), 3))) # Expected healing done
        # All buff the Player is giving
        for HealingBuff in Player.GivenHealBuffList:
            H_1_min = math.floor(H_1_min * HealingBuff.PercentBuff)
            H_1_expected_crit = math.floor(H_1_expected_crit * HealingBuff.PercentBuff)
        # All buff the target is receiving
        for HealingBuff in Target.ReceivedHealBuffList:
            H_1_min = math.floor(H_1_min * HealingBuff.PercentBuff)
            H_1_expected_crit = math.floor(H_1_expected_crit * HealingBuff.PercentBuff)

        return H_1_min, H_1_expected_crit 
    if type == 2: # DOT heal
        H_1 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_heal * f_DET) * f_DET) * f_TEN)  * f_SPD)* f_WD ) * Player.Trait)
        H_1_min = math.floor(H_1 * 97/100) # Minimal healing done
        H_1_expected_crit = math.floor(H_1 * (1 + round((CritRate * CritMult), 3))) # Expected healing done

        # If this is the first time the DOT is used. Will snapshot all buffs for later application of the heal.

        if not spellObj.onceThroughFlag:
            spellObj.onceThroughFlag = True
            # If this DOT has never been through. We take note of what buffs
            for HealingBuff in Player.GivenHealBuffList:
                spellObj.MultBonus.append(HealingBuff.PercentBuff)
            # All buff the target is receiving
            for HealingBuff in Target.ReceivedHealBuffList:
                spellObj.MultBonus.append(HealingBuff.PercentBuff)

        for buff in spellObj.MultBonus:
            # Applying all buff saved. buff here is the percent bonus in float
            H_1_min = math.floor(H_1_min * buff)
            H_1_expected_crit = math.floor(H_1_expected_crit * buff)

        return H_1_min, H_1_expected_crit
