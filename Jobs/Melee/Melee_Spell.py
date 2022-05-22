from Jobs.Base_Spell import Spell
Lock = 0.75
class MeleeSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

#########################################
########## NINJA SPELL  #################
#########################################

class NinjaSpell(MeleeSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, Effect, Requirement,Weaponskill, Ninjutsu):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement)
        self.Weaponskill = Weaponskill
        self.Ninjutsu = Ninjutsu


#########################################
########## SAMURAI PLAYER ###############
#########################################

class SamuraiSpell(MeleeSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, Effect, Requirement, KenkiCost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement)

        self.KenkiCost = KenkiCost
        self.Requirement += [KenkiRequirement]

def KenkiRequirement(Player, Spell): #By default present in Samurai spell requirements
    return Spell.KenkiCost <= Player.KenkiGauge, -1

#########################################
########## DRAGOON PLAYER ###############
#########################################

class DragoonSpell(MeleeSpell):
    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement)

        self.Weaponskill = Weaponskill

#########################################
########## MONK SPELL ###############
#########################################

class MonkSpell(MeleeSpell):
    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill, MasterfulBlitz):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement)

        self.Weaponskill = Weaponskill
        self.MasterfulBlitz = MasterfulBlitz

#########################################
########## MONK SPELL ###############
#########################################

class ReaperSpell(MeleeSpell):
    def __init__(self, id, GCD, CastTime,RecastTime, Potency, Effect, Requirement, Weaponskill):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement)

        self.Weaponskill = Weaponskill



#Class action spell

#Requirement

def SecondWindRequirement(Player, Spell):
    return Player.SecondWindCD <= 0, Player.SecondWindCD

def LegSweepRequirement(Player, Spell):
    return Player.LegSweepCD <= 0, Player.LegSweepCD

def BloodbathRequirement(Player, Spell):
    return Player.BloodbathCD <= 0, Player.BloodbathCD

def FeintRequirement(Player, Spell):
    return Player.FeintCD <= 0, Player.FeintCD

def ArmLengthRequirement(Player, Spell):
    return Player.ArmLengthCD <= 0, Player.ArmLengthCD

def TrueNorthRequirement(Player, Spell):
    return Player.TrueNorthStack > 0, Player.TrueNorthCD

#Apply
def ApplySecondWind(Player, Enemy):
    Player.SecondWindCD = 120

def ApplyLegSweep(Player, Enemy):
    Player.LegSweepCD = 40

def ApplyBloodbath(Player, Enemy):
    Player.BloodbathCD = 90

def ApplyFeint(Player, Enemy):
    Player.FeintCD = 90

def ApplyArmLength(Player, Enemy):
    Player.ArmLengthCD = 120

def ApplyTrueNorth(Player, Enemy):
    if Player.TrueNorthStack == 2:
        Player.EffectCDList.append(TrueNorthStackCheck)
        Player.TrueNorthCD = 45
    Player.TrueNorthStack -= 1


#Check

def TrueNorthStackCheck(Player, Enemy):
    if Player.TrueNorthCD <= 0:
        if Player.TrueNorthStack == 1:
            Player.EffectToRemove.append(TrueNorthStackCheck)
        else:
            Player.TrueNorthCD = 45
        Player.TrueNorthStack += 1
#Class Action (no effect as of now)
SecondWind = MeleeSpell(0, False, Lock, 0, 0, 0, ApplySecondWind, [SecondWindRequirement])
LegSweep = MeleeSpell(0, False, Lock, 0, 0, 0, ApplyLegSweep, [LegSweepRequirement])
Bloodbath = MeleeSpell(0, False, Lock, 0, 0, 0, ApplyBloodbath, [BloodbathRequirement])
Feint = MeleeSpell(0, False, Lock, 0, 0, 0, ApplyFeint, [FeintRequirement])
ArmLength = MeleeSpell(0, False, Lock, 0, 0, 0, ApplyArmLength, [ArmLengthRequirement])
TrueNorth = MeleeSpell(0, False, Lock, 0, 0, 0, ApplyTrueNorth, [TrueNorthRequirement])