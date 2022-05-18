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

#Class Action

#Requirement

def RampartRequirement(Player, Spell):
    return Player.RampartCD <= 0, Player.RampartCD

def LowBlowRequirement(Player, Spell):
    return Player.LowBlowCD <= 0, Player.LowBlowCD

def ProvokeRequirement(Player, Spell):
    return Player.ProvokeCD <= 0, Player.ProvokeCD

def InterjectRequirement(Player, Spell):
    return Player.InterjectCD <= 0, Player.InterjectCD

def ReprisalRequirement(Player, Spell):
    return Player.ReprisalCD <= 0, Player.ArmLengthCD

def ShirkRequirement(Player, Spell):
    return Player.ShirkCD <= 0, Player.ShirkCD

#Apply

def ApplyRampart(Player, Enemy):
    Player.RampartCD = 90

def ApplyLowBlow(Player, Enemy):
    Player.LowBlowCD = 25

def ApplyProvoke(Player, Enemy):
    Player.ProvokeCD = 30

def ApplyInterject(Player, Enemy):
    Player.InterjectCD = 30

def ApplyReprisal(Player, Enemy):
    Player.ReprisalCD = 60

def ApplyShirk(Player, Enemy):
    Player.ShirkCD = 120

#ArmLength in Melee_Spell.py
Rampart = TankSpell(0, False, Lock, 0, 0, 0, ApplyRampart, [RampartRequirement])
LowBlow = TankSpell(0, False, Lock, 0, 0, 0, ApplyLowBlow, [LowBlowRequirement])
Provoke = TankSpell(0, False, Lock, 0, 0, 0, ApplyProvoke, [ProvokeRequirement])
Interject = TankSpell(0, False, Lock, 0, 0, 0, ApplyInterject, [InterjectRequirement])
Reprisal = TankSpell(0, False, Lock, 0, 0, 0, ApplyReprisal, [ReprisalRequirement])
Shirk = TankSpell(0, False, Lock, 0, 0, 0, ApplyShirk, [ShirkRequirement])