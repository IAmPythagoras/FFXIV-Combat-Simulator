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