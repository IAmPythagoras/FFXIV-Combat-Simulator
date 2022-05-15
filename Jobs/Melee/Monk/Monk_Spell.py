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
    return Player.PerfectBalance > 0 or Player.TrueStrike or Player.TwinSnakes or Player.FourPointFury

def RaptorFormRequirement(Player, Spell):
    return Player.PerfectBalance > 0 or Player.Bootshine or Player.ArmOfTheDestroyer or Player.DragonKick or Player.ShadowOfTheDestroyer

