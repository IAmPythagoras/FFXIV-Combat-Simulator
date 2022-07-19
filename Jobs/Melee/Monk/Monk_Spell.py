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


# Maps Ability IDs from FFlogs to Skill objects
# Not exhaustive: If an ability is missing, check log for id and add it into the mapping.
# Using strings for now until MNK implementation. This is just for documentation.
MonkAbility = {
    3: 'Sprint',
    53: 'Bootshine',
    54: 'True Strike',
    56: 'Snap Punch',
    61: 'Twin Snakes',
    66: 'Demolish',
    69: 'Perfect Balance',
    74: 'Dragon Kick',
    202: 'Final Heaven',
    3545: 'Elixir Field',
    3546: 'Meditation',
    3547: 'the Forbidden Chakra',
    4262: 'Form Shift',
    7394: 'Riddle of Earth',
    7395: 'Riddle of Fire',
    7396: 'Brotherhood',
    7548: "Arm's Length",
    7549: 'Feint',
    16476: 'Six-sided Star',
    25762: 'Thunderclap',
    25766: 'Riddle of Wind',
    25768: 'Rising Phoenix',
    25769: 'Phantom Rush',
    34590541: 'Medicated',   # This is assumed to be strength pot grade 6
}