from ffxivcalc.Jobs.Base_Spell import Potion, Spell, empty
from ffxivcalc.Jobs.Melee.Melee_Spell import ArmLength, SecondWind
Lock = 0
class RangedSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)


#########################################
########## MACHINIST SPELL  #############
#########################################


class MachinistSpell(RangedSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, WeaponSkill, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

        self.Weaponskill = WeaponSkill #Boolean Variable


#########################################
#######    BARD    SPELL    #############
#########################################


class BardSpell(RangedSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill, type = 0):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement, type = type)

        self.Weaponskill = Weaponskill

#########################################
#########  DANCER    SPELL    ###########
#########################################


class DancerSpell(RangedSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill, type = 0):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement, type = type)
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

# Limit Break actions

LB1Timer = 5.10
LB2Timer = 6.10
LB3Timer = 8.20

RangedLB1 = RangedSpell(1111, False,LB1Timer, LB1Timer, 0, 0, empty, [], type=3)
RangedLB2 = RangedSpell(1112, False,LB2Timer, LB2Timer, 0, 0, empty, [], type=3)
RangedLB3 = RangedSpell(1113, False,LB3Timer, LB3Timer, 0, 0, empty, [], type=3)

RangedAbility = {
7554 : LegGraze,
7553 : FootGraze,
7551: HeadGraze,
7557 : Peloton,
7541 : SecondWind,
7548 : ArmLength,
34590542 : Potion,
34592396 : Potion,
-2 : Potion,
1111 : RangedLB1,
1112 : RangedLB2,
1113 : RangedLB3
}