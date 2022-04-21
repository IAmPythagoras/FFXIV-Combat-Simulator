from Jobs.Base_Spell import Spell
Lock = 0.75
class HealerSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)



def SwiftCastRequirement(Player, Spell):
    return Player.SwiftCastCD <= 0

def ApplySwiftCast(Player, Enemy):
    Player.SwiftCastCD = 60
    Player.EffectList.append(SwiftCastEffect)

def SwiftCastEffect(Player, Spell):
    if Spell.GCD and Spell.CastTime != 0: 
        Spell.CastTime = 0
        Player.EffectToRemove.append(SwiftCastEffect)

SwiftCast = HealerSpell(1, False,0, Lock, 0, 0, ApplySwiftCast, [SwiftCastRequirement])


#########################################
########## SCHOLAR SPELL  ###############
#########################################

class ScholarSpell(HealerSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


#########################################
########## WHITEMAGE SPELL ##############
#########################################


class WhitemageSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)
