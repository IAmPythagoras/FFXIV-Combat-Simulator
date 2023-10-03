from ffxivcalc.Jobs.Base_Spell import ManaRequirement, Potion, Spell, empty
from ffxivcalc.Jobs.PlayerEnum import JobEnum
Lock = 0
class CasterSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)


#########################################
########## BLACKMAGE SPELL ##############
#########################################
class BLMSpell(CasterSpell):
    #This class will be all BlackMage Ability
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, IsFire, IsIce, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)#Calls constructor of Spell

        #BLM specific part

        self.IsFire = IsFire
        self.IsIce = IsIce

#########################################
########## REDMAGE SPELL ################
#########################################


class RedmageSpell(CasterSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, BlackCost, WhiteCost, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

        self.BlackCost = BlackCost
        self.WhiteCost = WhiteCost

#########################################
########## SUMMONER SPELL ###############
#########################################


class SummonerSpell(CasterSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)


#Class Action

#Requirement

def SwiftcastRequirement(Player, Spell):
    return Player.SwiftcastCD <= 0, Player.SwiftcastCD

def LucidDreamingRequirement(Player, Spell):
    #if Player.LucidDreamingCD > 0: input("LUCID IS OUT OF SYNC BY : " + str(Player.LucidDreamingCD))
    #return Player.LucidDreamingCD <= 0, Player.LucidDreamingCD
    return True, -1

def SurecastRequirement(Player, Spell):
    return Player.SurecastCD <= 0, Player.SurecastCD

def AddleRequirement(Player, Spell):
    return Player.AddleCD <= 0, Player.AddleCD

#Apply

def ApplyLucidDreaming(Player, Enemy):
    Player.LucidDreamingCD = 60
    Player.LucidDreamingTimer = 21
    Player.EffectCDList.append(LucidDreamingCheck)


    # The order of insta cast usage for blackmage is SwiftCast -> TripleCast
    # The order for redmage is Acceleration -> Dualcast -> Swiftcast.
    # For purpose of simplicity, the order of these for RDM might not always be like that in sim. For example,
    # if execute Jolt -> Acc -> Swift : The usage will be Acc -> Swift -> Dual.
    # That is because Acc is insert(0), Swift is insert(1) and dual is index 0 at the start.
    # However if execute Jolt -> Swift -> Acc, then the correct use of Acc -> Dual -> Swift will happen.

def ApplySwiftcast(Player, Enemy):
    Player.SwiftcastCD = 60
                             # Inserting in index 1 in order to have it go after ElementalEffect for blm and dualcast effect for rdm.
    Player.EffectList.insert(1,SwiftcastEffect)

def ApplySurecast(Player, Enemy):
    Player.SurecastCD = 120

def ApplyAddle(Player, Enemy):
    Player.AddleCD = 90
    Enemy.Addle = True
    Enemy.AddleTimer = 10


#Effect

def SwiftcastEffect(Player, Spell):
    if Spell.GCD and Spell.CastTime >= Lock and not (Player.JobEnum == JobEnum.BlackMage and Spell.id == 152 and Player.F3Proc):  #If GCD and not already insta cast and not F3 Proc when casting F3
        Spell.CastTime = Lock
        Player.EffectToRemove.append(SwiftcastEffect)

#Check

def LucidDreamingCheck(Player, Enemy):
    #input("got in")
    if (int(Player.LucidDreamingTimer * 100)/100)%3 == 0 and Player.LucidDreamingTimer != 21:
        #if on a tic and not equal to 21
        #input("got in")

        if Player.JobEnum == JobEnum.BlackMage:
            #We have to check if in firephase, in which case no mana regen
            if Player.ElementalGauge <= 0: #If in ice phase
                #input("Adding mana")
                Player.Mana = min(10000, Player.Mana + 550)
        else:
            #Then any other player
            Player.Mana = min(10000, Player.Mana + 550)

        #Check if we are done
        if Player.LucidDreamingTimer <= 0:
            Player.EffectToRemove.append(LucidDreamingCheck)

#Class Action
Swiftcast = CasterSpell(7561, False,0, Lock, 0, 0, ApplySwiftcast, [SwiftcastRequirement])
LucidDreaming = CasterSpell(7562, False, Lock,0,0, 0, ApplyLucidDreaming, [LucidDreamingRequirement])
Surecast = CasterSpell(7559, False, Lock, 0, 0, 0, ApplySurecast, [SurecastRequirement])
Addle = CasterSpell(7560, False, Lock, 0, 0, 0, ApplyAddle, [AddleRequirement])
Sleep = CasterSpell(25880, True, 2.5, 2.5, 0, 800, empty, [ManaRequirement])

CasterAbility = {
7561 : Swiftcast, 
7562 : LucidDreaming,  
7559 : Surecast, 
7560 : Addle, 
25880 : Sleep,
34590544 : Potion, #Grade 6
34592398 : Potion, # Grade 7
-2 : Potion
}