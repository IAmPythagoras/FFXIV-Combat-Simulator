from Jobs.Base_Spell import Spell
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

        self.WeaponSkill = WeaponSkill #Boolean Variable


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
