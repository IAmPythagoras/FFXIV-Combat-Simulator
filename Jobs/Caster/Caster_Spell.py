
from Jobs.Base_Spell import Spell
from Jobs.Caster.Blackmage.BlackMage_Player import BlackMage
Lock = 0.75
class CasterSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)



def SwiftCastRequirement(Player, Spell):
    return Player.SwiftCastCD <= 0

def LucidDreamingRequirement(Player, Spell):
    return Player.LucidDreamingCD <= 0

def ApplyLucidDreaming(Player, Enemy):
    Player.LucidDreamingCD = 60
    Player.LucidDreamingTimer = 21
    Player.EffectCDList.append(LucidDreamingCheck)

def ApplySwiftCast(Player, Enemy):
    Player.SwiftCastCD = 60
    Player.EffectList.append(SwiftCastEffect)

def SwiftCastEffect(Player, Spell):
    if Spell.GCD and Spell.CastTime > Lock:  #If GCD and not already insta cast
        Spell.CastTime = Lock
        Player.EffectToRemove.append(SwiftCastEffect)

def LucidDreamingCheck(Player, Enemy):
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


SwiftCast = CasterSpell(1, False,0, Lock, 0, 0, ApplySwiftCast, [SwiftCastRequirement])
LucidDreaming = CasterSpell(2, False, Lock,0,0, 0, ApplyLucidDreaming, [LucidDreamingRequirement])


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




