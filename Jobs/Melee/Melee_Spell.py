from Jobs.Base_Spell import Spell
Lock = 0.75
class MeleeSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

#########################################
########## NINJA SPELL  #################
#########################################

class NinjaSpell(MeleeSpell):

    def __init__(self, id, WeaponSkill, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)
        self.WeaponSkill = WeaponSkill


#########################################
########## SAMURAI PLAYER ###############
#########################################

class SamuraiSpell(MeleeSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, Effect, Requirement, KenkiCost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement)

        self.KenkiCost = KenkiCost
        self.Requirement += [KenkiRequirement]

def KenkiRequirement(Player, Spell): #By default present in Samurai spell requirements
    return Spell.KenkiCost <= Player.KenkiGauge

#########################################
########## DRAGOON PLAYER ###############
#########################################

class DragoonSpell(MeleeSpell):
    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement)

        self.Weaponskill = Weaponskill