from Jobs.Base_Spell import Spell, Auto_Attack
Lock = 0.75



class TankSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)


#########################################
########## WARRIOR Spell  ###############
#########################################

def BeastGaugeRequirement(Player, Spell):
    RemoveBeast(Player, Spell.Cost)
    return Player.BeastGauge >= 0, -1

class WarriorSpell(TankSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, Cost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.Requirement += [BeastGaugeRequirement] 
        self.Cost = Cost

def RemoveBeast(Player, Gauge):
    Player.BeastGauge -= Gauge #Caanot go under 0 cuz verify if enough gauge


#########################################
########## DARK KNIGHT SKILLS ###########
#########################################

class DRKSkill(TankSpell):
    #A class for Dark Knight Skills containing all the relevant weaponskills/spells, cooldowns,
    #as well as their effects and requirements. For now does not consider out of combo actions.

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, BloodCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.BloodCost = BloodCost
#########################################
########## PALADIN SKILLS  ##############
#########################################

class PaladinSpell(TankSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)



#########################################
########## GUNBREAKER SKILLS  ###########
#########################################

def PowderRequirement(Player, Spell):
    Player.PowderGauge -= Spell.PowderCost
    return Player.PowderGauge >=0, 0

class GunbreakerSpell(TankSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, PowderCost ):
        super().__init__(id, GCD, 0.75, RecastTime, Potency, 0, Effect, Requirement)

        self.PowderCost = PowderCost
        self.Requirement += [PowderRequirement]
