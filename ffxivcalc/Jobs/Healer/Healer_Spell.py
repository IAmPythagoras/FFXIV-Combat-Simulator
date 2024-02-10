from ffxivcalc.Jobs.Base_Spell import ManaRequirement, Potion, Spell, empty
from ffxivcalc.Jobs.Caster.Caster_Spell import LucidDreaming, Surecast, Swiftcast
Lock = 0.75
class HealerSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0, AOEHeal = False):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type, AOEHeal = AOEHeal)


#########################################
########## SCHOLAR SPELL  ###############
#########################################

class ScholarSpell(HealerSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0, AOEHeal = False):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type, AOEHeal = AOEHeal)


#########################################
########## WHITEMAGE SPELL ##############
#########################################


class WhitemageSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0, AOEHeal = False):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type, AOEHeal = AOEHeal)

#########################################
########## ASTROLOGIAN SPELL ############
#########################################


class AstrologianSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0, AOEHeal = False):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type, AOEHeal = AOEHeal)

#########################################
##########     SAGE   SPELL   ###########
#########################################


class SageSpell(HealerSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0, AOEHeal = False):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type, AOEHeal = AOEHeal)



#Class Action spell

#Requirement
def RescueRequirement(Player, Spell):
    return Player.RescueCD <= 0, Player.RescueCD

#Apply

def ApplyRescue(Player, Enemy):
    Player.RescueCD = 120

#Swiftcast, Surecast and LucidDreaming are in Caster_Spell.py
Repose = HealerSpell(16560, True, 2.5, 2.5, 0, 600, empty, [ManaRequirement])
Esuna = HealerSpell(7568, True, 1, 2.5, 0, 400, empty, [ManaRequirement])
Rescue = HealerSpell(7571, False, 0, 0, 0, 0, ApplyRescue, [RescueRequirement])

# Limit Break actions

LB1Timer = 4.10
LB2Timer = 7.13
LB3Timer = 10.10

HealerLB1 = HealerSpell(1111, False,LB1Timer, LB1Timer, 0, 0, empty, [])
HealerLB2 = HealerSpell(1112, False,LB2Timer, LB2Timer, 0, 0, empty, [])
HealerLB3 = HealerSpell(1113, False,LB3Timer, LB3Timer, 0, 0, empty, [])

HealerAbility = {
16560 : Repose,
7568 : Esuna,
7571 : Rescue,
7561 : Swiftcast,
7562 : LucidDreaming,
7559 : Surecast,
34590545 : Potion,
34592399 : Potion, 
-2 : Potion,
1111 : HealerLB1,
1112 : HealerLB2,
1113 : HealerLB3
}