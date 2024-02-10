from ffxivcalc.Jobs.Base_Spell import Potion, Spell, empty
Lock = 0
class MeleeSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

#########################################
########## NINJA SPELL  #################
#########################################

class NinjaSpell(MeleeSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, Effect, Requirement,Weaponskill, Ninjutsu, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement, type = type)
        self.Weaponskill = Weaponskill
        self.Ninjutsu = Ninjutsu


#########################################
########## SAMURAI PLAYER ###############
#########################################

class SamuraiSpell(MeleeSpell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, Effect, Requirement, KenkiCost, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement, type = type)

        self.KenkiCost = KenkiCost
        self.Requirement += [KenkiRequirement]

def KenkiRequirement(Player, Spell): #By default present in Samurai spell requirements
    #input("Current Gauge is " + str(Player.KenkiGauge - Spell.KenkiCost))
    return Spell.KenkiCost <= Player.KenkiGauge, -1

#########################################
########## DRAGOON PLAYER ###############
#########################################

class DragoonSpell(MeleeSpell):
    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill, type = 0):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement, type = type)

        self.Weaponskill = Weaponskill

#########################################
########## MONK SPELL ###############
#########################################

class MonkSpell(MeleeSpell):
    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill, MasterfulBlitz, type = 0):
        super().__init__(id, GCD, Lock, RecastTime, Potency, 0, Effect, Requirement, type = type)

        self.Weaponskill = Weaponskill
        self.MasterfulBlitz = MasterfulBlitz

#########################################
########## MONK SPELL ###############
#########################################

class ReaperSpell(MeleeSpell):
    def __init__(self, id, GCD, CastTime,RecastTime, Potency, Effect, Requirement, Weaponskill, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, 0, Effect, Requirement, type = type)

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
    Enemy.Feint = True
    Enemy.FeintTimer = 10

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
SecondWind = MeleeSpell(7541, False, Lock, 0, 0, 0, ApplySecondWind, [SecondWindRequirement])
LegSweep = MeleeSpell(7863, False, Lock, 0, 0, 0, ApplyLegSweep, [LegSweepRequirement])
Bloodbath = MeleeSpell(7542, False, Lock, 0, 0, 0, ApplyBloodbath, [BloodbathRequirement])
Feint = MeleeSpell(7549, False, Lock, 0, 0, 0, ApplyFeint, [FeintRequirement])
ArmLength = MeleeSpell(7548, False, Lock, 0, 0, 0, ApplyArmLength, [ArmLengthRequirement])
TrueNorth = MeleeSpell(7546, False, Lock, 0, 0, 0, ApplyTrueNorth, [TrueNorthRequirement])

# Limit Break actions

LB1Timer = 5.86
LB2Timer = 6.86
LB3Timer = 8.20

MeleeLB1 = MeleeSpell(1111, False,LB1Timer, LB1Timer, 0, 0, empty, [])
MeleeLB2 = MeleeSpell(1112, False,LB2Timer, LB2Timer, 0, 0, empty, [])
MeleeLB3 = MeleeSpell(1113, False,LB3Timer, LB3Timer, 0, 0, empty, [])


MeleeAbility = {
7541 : SecondWind,
7863 : LegSweep,
7542 : Bloodbath,
7549 : Feint,
7546 : TrueNorth,
7548 : ArmLength,
34590541 : Potion,  #STR
34590542 : Potion,   #DEX,
34592395 : Potion, # STR 7
34592396 : Potion, # DEX 7
-2 : Potion,
1111 : MeleeLB1,
1112 : MeleeLB2,
1113 : MeleeLB3
}