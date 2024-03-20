from ffxivcalc.Jobs.Base_Spell import Potion, Spell, empty
from ffxivcalc.Jobs.Melee.Melee_Spell import ArmLength
from ffxivcalc.Jobs.Player import MitBuff
from ffxivcalc.Jobs.PlayerEnum import JobEnum
Lock = 0.75



class TankSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)


#########################################
########## WARRIOR Spell  ###############
#########################################

def BeastGaugeRequirement(Player, Spell):
    RemoveBeast(Player, Spell.Cost)
    return Player.BeastGauge >= 0, -1

class WarriorSpell(TankSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, Cost, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

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

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, BloodCost, Effect, Requirement, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

        self.BloodCost = BloodCost
#########################################
########## PALADIN SKILLS  ##############
#########################################

class PaladinSpell(TankSpell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, isPhysical, type = 0):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, type = type)

        self.isPhysical = isPhysical #To know to what ability we will give FoF



#########################################
########## GUNBREAKER SKILLS  ###########
#########################################

def PowderRequirement(Player, Spell):
    Player.PowderGauge -= Spell.PowderCost
    return Player.PowderGauge >=0, 0

class GunbreakerSpell(TankSpell):

    def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, PowderCost , type = 0):
        super().__init__(id, GCD, 0, RecastTime, Potency, 0, Effect, Requirement, type = type)

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
    return Player.ReprisalCD <= 0, Player.ReprisalCD
    
def ShirkRequirement(Player, Spell):
    return Player.ShirkCD <= 0, Player.ShirkCD

def BigMitRequirement(Player, Spell):
    return Player.BigMitCD <= 0, Player.BigMitCD

def TankStanceRequirement(Player, Spell):
    return Player.TankStanceCD <= 0, Player.TankStanceCD

#Apply

def ApplyTankStance(Player, Enemy):
    if not Player.TankStanceOn:
        # Only goes in cooldown if the tank stance was already on
        Player.TankStanceOn = True
    else:
        Player.TankStanceCD = 3
        Player.TankStanceOn = False

def ApplyTurnOffTankStance(Player, Enemy):
    Player.TankStanceOn = True

def ApplyBigMit(Player, Enemy):
    Player.BigMitCD = 120
    BigMitBuff = MitBuff(0.7, 15, Player)
    Player.MitBuffList.append(BigMitBuff) # Appends buff

    # Keeps pointer to buff if Warrior
    if Player.JobEnum == JobEnum.Warrior: Player.VengeanceBuff = BigMitBuff
    elif Player.JobEnum == JobEnum.Paladin: Player.BigMitTimer = 15


def ApplyRampart(Player, Enemy):
    Player.RampartCD = 90
    RampartBuff = MitBuff(0.8, 20, Player)
    Player.MitBuffList.append(RampartBuff)
    if Player.JobEnum == JobEnum.Paladin: Player.RampartTimer = 20

def ApplyLowBlow(Player, Enemy):
    Player.LowBlowCD = 25

def ApplyProvoke(Player, Enemy):
    Player.ProvokeCD = 30
    Player.TotalEnemity = Player.CurrentFight.GetEnemityList(1)[0].TotalEnemity + 300
    # Gives enemity to the tank equal to the maximum enemity + 10.
    # The values here are arbitrary. 10 enemity corresponds to 100'000 tank damage (with tank stance on)

def ApplyInterject(Player, Enemy):
    Player.InterjectCD = 30

def ApplyReprisal(Player, Enemy):
    Player.ReprisalCD = 60
    Enemy.Reprisal = True
    Enemy.ReprisalTimer = 10





#ArmLength in Melee_Spell.py
Rampart = TankSpell(7531, False, Lock, 0, 0, 0, ApplyRampart, [RampartRequirement])
LowBlow = TankSpell(7540, False, Lock, 0, 0, 0, ApplyLowBlow, [LowBlowRequirement])
Provoke = TankSpell(7533, False, Lock, 0, 0, 0, ApplyProvoke, [ProvokeRequirement])
Interject = TankSpell(10101010, False, Lock, 0, 0, 0, ApplyInterject, [InterjectRequirement])
Reprisal = TankSpell(7535, False, Lock, 0, 0, 0, ApplyReprisal, [ReprisalRequirement])
RoyalGuard = TankSpell(16142, False, 0, 0, 0, 0, ApplyTankStance, [TankStanceRequirement]) #Turn on Tank Stance
Grit = TankSpell(3629, False, 0, 0, 0, 0, ApplyTankStance, [TankStanceRequirement])
IronWill = TankSpell(28, False, 0, 0, 0, 0, ApplyTankStance, [TankStanceRequirement])
Defiance = TankSpell(48, False, 0, 0, 0, 0, ApplyTankStance, [TankStanceRequirement])
TurnOffTankStance = TankSpell(0, False, 0, 0, 0, 0, ApplyTurnOffTankStance, [])#Turn off Tank Stance

def Shirk(Target):
    """This function is used to generate the shirk action with a customized target.

    Target (Player) : Target of the shirk.
    
    """

    def ApplyShirk(Player, Enemy):
        Player.ShirkCD = 120

        Target.TotalEnemity += Player.TotalEnemity * 0.25
        # Giving 25% of the Player's enemity to the target

        Player.TotalEnemity *= 0.75
        # Loosing 25% of the player's enemity

    custom_shirk = TankSpell(7537, False, Lock, 0, 0, 0, ApplyShirk, [ShirkRequirement])
    custom_shirk.TargetID = Target.playerID
    return custom_shirk


# Limit Break actions

LB1Timer = 1.93
LB2Timer = 3.86
LB3Timer = 3.86

TankLB1 = TankSpell(1111, False,LB1Timer, LB1Timer, 0, 0, empty, [], type=3)
TankLB2 = TankSpell(1112, False,LB2Timer, LB2Timer, 0, 0, empty, [], type=3)
TankLB3 = TankSpell(1113, False,LB3Timer, LB3Timer, 0, 0, empty, [], type=3)

TankAbility = {
10101010 : Interject,
7531 : Rampart,
7535 : Reprisal, 
7548 : ArmLength,
7540 : LowBlow,
7533 : Provoke,
7537 : Shirk,
16142 : RoyalGuard, #Gunbreaker Tank Stance
3629 : Grit, #DarkKnight Tank Stance
48 : Defiance, #Warrior Tank Stance
28 : IronWill, #Paladin Tank Stance
34590541 : Potion,
34592395 : Potion,
34594159 : Potion, 
-2 : Potion,
1111 : TankLB1,
1112 : TankLB2,
1113 : TankLB3
}