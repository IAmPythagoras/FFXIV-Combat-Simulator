from Jobs.Base_Spell import ManaRequirement, Spell, empty
from Jobs.Caster.Caster_Spell import LucidDreaming, Surecast, Swiftcast
Lock = 0.75
class HealerSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


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

#########################################
########## ASTROLOGIAN SPELL ############
#########################################


class AstrologianSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

#########################################
##########     SAGE   SPELL   ###########
#########################################


class SageSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)



#Class Action spell

#Requirement
def RescueRequirement(Player, Spell):
    return Player.RescueCD <= 0, Player.RescueCD

#Apply

def ApplyRescue(Player, Enemy):
    Player.RescueCD = 120

#Swiftcast, Surecast and LucidDreaming are in Caster_Spell.py
Repose = HealerSpell(0, True, 2.5, 2.5, 0, 600, empty, [ManaRequirement])
Esuna = HealerSpell(0, True, 1, 2.5, 0, 0, 400, [ManaRequirement])
Rescue = HealerSpell(0, False, 0, 0, 0, 0, ApplyRescue, [RescueRequirement])
Raise = HealerSpell(0, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])
HealerAbility = {
16560 : Repose,
7568 : Esuna,
7571 : Rescue,
7561 : Swiftcast,
7562 : LucidDreaming,
7559 : Surecast,
173 : Raise, #Scholar Raise
3603 : Raise, #Astro raise
24287 : Raise, #sage raise
125 : Raise #whitemage raise
}