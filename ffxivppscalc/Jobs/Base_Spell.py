import copy

from Fight import ComputeDamage
import math
from Jobs.PlayerEnum import JobEnum
from Jobs.PlayerEnum import RoleEnum
from requirementHandler import failedRequirementEvent
Lock = 0.75

class FailedToCast(Exception):#Exception called if a spell fails to cast
    pass


class buff:
    """
    This class is any buff given to a player. It contains the buff's value
    """
    def __init__(self, MultDPS):
        self.MultDPS = MultDPS #DPS multiplier of the buff


class Spell:
    """
    This class is any Spell, it will have some subclasses to take Job similar spell, etc.
    """
    def __init__(self, id : int, GCD : bool, CastTime : float, RecastTime : float, Potency : int, ManaCost : int, Effect, Requirement):
        """
        Initialization of a Spell
        id : int -> id to identify the action
        GCD : bool -> True if the action is a GCD
        CastTime : float -> Cast time of the action
        RecastTime : float -> Recast time of the action
        Potency : int -> base potency of the action
        Manacost : int -> base manacost of the action
        Effect : function -> A function called upon the execution of the action which affects the player and the enemy.
        Requirement : function -> Bool -> function called upon the execution to verify if the action can be executed.

        """
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

                addInfo = "" if timeLeft <= 0 else "player had to wait for " + str(timeLeft) + " seconds."

                fatal = not (timeLeft <= player.CurrentFight.waitingThreshold and timeLeft > 0 or (player.CurrentFight.RequirementOn) ) # true if stops the simulation

                newFailedRequirementEvent = failedRequirementEvent(player.CurrentFight.TimeStamp, player.playerID, Requirement.__name__, addInfo, fatal) # Recording the event
                player.CurrentFight.failedRequirementList.append(newFailedRequirementEvent) # storing the event in memory
                
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
        if tempSpell.id > 0 and tempSpell.CastTime < Lock : tempSpell.CastTime = 0.5 #id < 0 are special abilities like DOT, so we do not want them to be affected by that
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

        type = 0 #Default value for type
        if isinstance(self, Auto_Attack):
            type = 3
        elif isinstance(self, DOTSpell): #Then dot
            #We have to figure out if its a physical dot or not
            if self.isPhysical: type = 2
            else: type = 1   

        
        if self.Potency != 0 : minDamage,Damage= ComputeDamage(player, self.Potency, Enemy, self.DPSBonus, type, self)    #Damage computation
        else: minDamage, Damage = 0,0

        

        if player.JobEnum == JobEnum.Pet:
            player.Master.TotalPotency+= self.Potency
            player.Master.TotalDamage += Damage
            player.Master.TotalMinDamage += minDamage
        else:
            player.TotalPotency+= self.Potency
            player.TotalDamage += Damage
            player.TotalMinDamage += minDamage
        
        Enemy.TotalPotency+= self.Potency  #Adding Potency
        Enemy.TotalDamage += Damage #Adding Damage


        if not (player.CurrentFight.FightStart) and Damage > 0 : 
            player.CurrentFight.FightStart = True

            #Giving all players AA

            for gamer in player.CurrentFight.PlayerList:
                if gamer.JobEnum == JobEnum.Monk: gamer.DOTList.append(copy.deepcopy(Monk_Auto))
                elif gamer.RoleEnum == RoleEnum.Melee or gamer.JobEnum == JobEnum.Dancer or gamer.RoleEnum == RoleEnum.Tank:
                    gamer.DOTList.append(copy.deepcopy(Melee_AADOT))
                elif gamer.RoleEnum == RoleEnum.PhysicalRanged:
                    gamer.DOTList.append(copy.deepcopy(Ranged_AADOT))


        #Will update the NextSpell of the player

        if (not (isinstance(self, DOTSpell))) : player.NextSpell+=1
        if (player.NextSpell == len(player.ActionSet)):#Checks if no more spell to do
            player.TrueLock = True

        if self.GCD: player.GCDCounter += 1

        return self

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
    Player.Stat["MainStat"] = min(math.floor(Player.Stat["MainStat"] * 1.1), Player.Stat["MainStat"] + 223) #Grade 7 HQ tincture
    Player.PotionTimer = 30

    Player.EffectCDList.append(PotionCheck)

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
        Player.Stat["MainStat"] -= 223 #Assuming we are capped
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
        if(self.DOTTimer <= 0):
            #Apply DOT
            tempSpell  = self.Cast(Player, Enemy)#Cast the DOT
            tempSpell.CastFinal(Player, Enemy)
            self.DOTTimer = 3
        else:
            self.DOTTimer = max(0, self.DOTTimer-TimeUnit)


class Auto_Attack(DOTSpell):
    """
    DOTSpell subclass only for Autos since they have different potency depending on if ranged or melee.
    """
    def __init__(self, id, Ranged : bool):
        """
        Ranged : bool -> True if the auto is ranged.
        """
        if Ranged : super().__init__(id, 100, True) # Ranged AA
        else: super().__init__(id, 110, True) # Melee AA

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



