from Jobs.Base_Spell import ManaRequirement, Potion, Spell, empty
from Jobs.Caster.Blackmage.BlackMage_Player import BlackMage
Lock = 0
class CasterSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


#########################################
########## BLACKMAGE SPELL ##############
#########################################
class BLMSpell(CasterSpell):
    #This class will be all BlackMage Ability
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, IsFire, IsIce, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)#Calls constructor of Spell

        #BLM specific part

        self.IsFire = IsFire
        self.IsIce = IsIce

#########################################
########## REDMAGE SPELL ################
#########################################


class RedmageSpell(CasterSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, BlackCost, WhiteCost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.BlackCost = BlackCost
        self.WhiteCost = WhiteCost

#########################################
########## SUMMONER SPELL ###############
#########################################


class SummonerSpell(CasterSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


#Class Action

#Requirement

def SwiftcastRequirement(Player, Spell):
    return Player.SwiftcastCD <= 0, Player.SwiftcastCD

def LucidDreamingRequirement(Player, Spell):
    return Player.LucidDreamingCD <= 0, Player.LucidDreamingCD

def SurecastRequirement(Player, Spell):
    return Player.SurecastCD <= 0, Player.SurecastCD

def AddleRequirement(Player, Spell):
    return Player.AddleCD <= 0, Player.AddleCD

#Apply

def ApplyLucidDreaming(Player, Enemy):
    Player.LucidDreamingCD = 60
    Player.LucidDreamingTimer = 21
    Player.EffectCDList.append(LucidDreamingCheck)

def ApplySwiftcast(Player, Enemy):
    Player.SwiftcastCD = 60
    Player.EffectList.insert(0,SwiftcastEffect)

def ApplySurecast(Player, Enemy):
    Player.SurecastCD = 120

def ApplyAddle(Player, Enemy):
    Player.AddleCD = 90


#Effect

def SwiftcastEffect(Player, Spell):
    if Spell.GCD and Spell.CastTime > Lock:  #If GCD and not already insta cast
        Spell.CastTime = Lock
        Player.EffectToRemove.append(SwiftcastEffect)

#Check

def LucidDreamingCheck(Player, Enemy):
    #input("got in")
    if (int(Player.LucidDreamingTimer * 100)/100)%3 == 0 and Player.LucidDreamingTimer != 21:
        #if on a tic and not equal to 21
        #input("got in")

        if isinstance(Player, BlackMage):
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
Swiftcast = CasterSpell(1001, False,0, Lock, 0, 0, ApplySwiftcast, [SwiftcastRequirement])
LucidDreaming = CasterSpell(1002, False, Lock,0,0, 0, ApplyLucidDreaming, [LucidDreamingRequirement])
Surecast = CasterSpell(1003, False, Lock, 0, 0, 0, ApplySurecast, [SurecastRequirement])
Addle = CasterSpell(1004, False, Lock, 0, 0, 0, ApplyAddle, [AddleRequirement])
Sleep = CasterSpell(1005, True, 2.5, 2.5, 0, 800, empty, [ManaRequirement])

CasterAbility = {
7561 : Swiftcast, 
7562 : LucidDreaming,  
7559 : Surecast, 
7560 : Addle, 
25880 : Sleep,
34590544 : Potion
}