from Jobs.Base_Spell import Potion, Spell
from Jobs.Melee.Melee_Spell import ArmLength, SecondWind
Lock = 0.75
class RangedSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


#########################################
########## MACHINIST SPELL  #############
#########################################


class MachinistSpell(RangedSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, WeaponSkill):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.Weaponskill = WeaponSkill #Boolean Variable


#########################################
#######    BARD    SPELL    #############
#########################################


class BardSpell(RangedSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement)

        self.Weaponskill = Weaponskill

#########################################
#########  DANCER    SPELL    ###########
#########################################


class DancerSpell(RangedSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement)
        self.Weaponskill = Weaponskill


#Class Action

#Requirement

def LegGrazeRequirement(Player, Spell):
    return Player.LegGrazeCD <= 0, Player.LegGrazeCD

def FootGrazeRequirement(Player, Spell):
    return Player.FootGrazeCD <= 0, Player.FootGrazeCD

def PelotonRequirement(Player, Spell):
    return Player.PelotonCD <= 0, Player.PelotonCD

def HeadGrazeRequirement(Player, Spell):
    return Player.HeadGrazeCD <= 0, Player.HeadGrazeCD

#Apply

def ApplyLegGraze(Player, Spell):
    Player.LegGrazeCD = 30

def ApplyFootGraze(Player, Spell):
    Player.FootGrazeCD = 30

def ApplyPeloton(Player, Spell):
    Player.PelotonCD = 5

def ApplyHeadGraze(Player, Spell):
    Player.HeadGrazeCD = 30


#ArmLength and SecondWind are in Melee_Spell.py
LegGraze = RangedSpell(0, False, Lock, 0, 0, 0, ApplyLegGraze, [LegGrazeRequirement])
FootGraze = RangedSpell(0, False, Lock, 0, 0, 0, ApplyFootGraze, [FootGrazeRequirement])
Peloton = RangedSpell(0, False, Lock, 0, 0, 0, ApplyPeloton, [PelotonRequirement])
HeadGraze = RangedSpell(0, False, Lock, 0, 0, 0, ApplyHeadGraze, [HeadGrazeRequirement])

RangedAbility = {
7554 : LegGraze,
7553 : FootGraze,
7551: HeadGraze,
7557 : Peloton,
7541 : SecondWind,
7548 : ArmLength,
34590542 : Potion
}