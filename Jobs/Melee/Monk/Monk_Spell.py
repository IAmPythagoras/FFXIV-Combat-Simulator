from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import MonkSpell
from Jobs.Melee.Monk.Monk_Player import Monk
Lock = 0.75 #skill animation lock - simulating 75ms ping

#Requirements

def ForbiddenChakraRequirement(Player, Spell):
    return Player.FifthChakra == -1

def ElixerFieldRequirement(Player, Spell):  #must use three of the same form skills and grants lunar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 3 or Player.RaptorSkillUsed == 3 or Player.CoeurlSkillUsed == 3

def RisingPhoenixRequirement(Player, Spell):    #must use three different form skills is aoe and unlocks solar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 1 and Player.RaptorSkillUsed == 1 and Player.CoeurlSkillUsed == 1

def CelestialRevolutionRequirement(Player, Spell):    #must use 2 gcds if same form and last is different form skills is aoe and unlocks solar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 2 and Player.RaptorSkillUsed == 1 \
                                        or Player.OpoOpoSkillUsed == 2 and Player.CoeurlSkillUsed == 1 \
                                            or Player.RaptorSkillUsed == 2 and Player.OpoOpoSkillUsed == 1 \
                                                or Player.RaptorSkillUsed == 2 and Player.CoeurlSkillUsed == 1 \
                                                    or Player.CoeurlSkillUsed == 2 and Player.RaptorSkillUsed == 1 \
                                                        or Player.CoeurlSkillUsed == 2 and Player.OpoOpoSkillUsed == 1

def PhantomRushRequirement(Player, Spell):    #must use three different form skills is aoe and unlocks solar nadi
    return Player.SolarNadi == -1 and Player.LunarNadi == -1
                                    
def CoeurlFormRequirement(Player, Spell):
    return Player.PerfectBalance > 0 or [Player.TrueStrike, Player.TwinSnakes, Player.FourPointFury]

def RaptorFormRequirement(Player, Spell):
    return Player.PerfectBalance > 0 or [Player.Bootshine, Player.ArmOfTheDestroyer, Player.DragonKick, Player.ShadowOfTheDestroyer]

#Effect
def BootshineOpoOpoFormBonus(Player, Spell):
    if Spell.id == Bootshine.id and Player.OpoOpoForm == True:
        Player.NextCrit = True

def LeadenFist(Player, Spell):
    if Spell.id == DragonKick.id:
        Bootshine.Potency += 310
        Player.buffList.Append() 

def ApplyRaptorForm(Player, Spell):
    Player.OpoOpoSkillUsed += 1
    Player.RaptorForm = True

def ApplyCoeurlForm(Player, Spell):
    Player.RaptorSkillUsed += 1
    Player.RaptorForm = True

#GCD
# def __init__(self, id, GCD, RecastTime, Potency, Effect, Requirement, Weaponskill):
Bootshine = MonkSpell(1, True, Lock, 2, 210, [BootshineOpoOpoFormBonus, LeadenFist, ApplyRaptorForm], [], True)
TrueStrike = MonkSpell(2, True, Lock, 2, 300, ApplyCoeurlForm, RaptorFormRequirement, True)
SnapPunch = MonkSpell(3, True, Lock, 2, 310, )