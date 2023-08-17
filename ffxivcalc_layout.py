from ffxivcalc.Enemy import Enemy, MagicRaidWide, PhysicalRaidWide, WaitEvent, TankBuster
from ffxivcalc.Fight import Fight
from ffxivcalc.Jobs.Player import Player
from ffxivcalc.Jobs.PlayerEnum import *
from copy import deepcopy

from ffxivcalc.Jobs.Base_Spell import WaitAbility, Potion
from ffxivcalc.Jobs.Caster.Caster_Spell import *
from ffxivcalc.Jobs.Melee.Melee_Spell import *
from ffxivcalc.Jobs.Ranged.Ranged_Spell import *
from ffxivcalc.Jobs.Healer.Healer_Spell import *
from ffxivcalc.Jobs.Tank.Tank_Spell import *

#CASTER
from ffxivcalc.Jobs.Caster.Summoner.Summoner_Spell import *
from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import * 
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import *

#HEALER
from ffxivcalc.Jobs.Healer.Sage.Sage_Spell import *
from ffxivcalc.Jobs.Healer.Scholar.Scholar_Spell import *
from ffxivcalc.Jobs.Healer.Whitemage.Whitemage_Spell import *
from ffxivcalc.Jobs.Healer.Astrologian.Astrologian_Spell import *

#RANGED
from ffxivcalc.Jobs.Ranged.Machinist.Machinist_Spell import *
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import *
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import *

#TANK
from ffxivcalc.Jobs.Tank.Gunbreaker.Gunbreaker_Spell import *
from ffxivcalc.Jobs.Tank.DarkKnight.DarkKnight_Spell import *
from ffxivcalc.Jobs.Tank.Warrior.Warrior_Spell import *
from ffxivcalc.Jobs.Tank.Paladin.Paladin_Spell import *

#MELEE
from ffxivcalc.Jobs.Melee.Samurai.Samurai_Spell import *
from ffxivcalc.Jobs.Melee.Ninja.Ninja_Spell import *
from ffxivcalc.Jobs.Melee.Dragoon.Dragoon_Spell import *
from ffxivcalc.Jobs.Melee.Reaper.Reaper_Spell import *
from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import *


# This part of the code will execute whatever rotation is written here. It will be called from TUI.

Dummy = Enemy()
Event = Fight(Dummy, False)

# ===============================================================================================
# You don't need to to worry about anything above this point

# Stat Sheet
# Enter your own stats here. The default is the 6.2 Savage BiS found on the Balance. The default Tenacity for non-tank is 400.
# These stats must include the bonus stats food gives.

# Caster
#BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1493, 'Ten': 400, 'SS': 824, 'SkS': 400, 'Crit': 2514, 'DH': 1402} # Stats for BlackMage
#BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1534, 'Ten': 400, 'SS': 886, 'SkS': 400, 'Crit': 2519, 'DH': 1294}
#BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1529, 'Ten': 400, 'SS': 824, 'SkS': 400, 'Crit': 2514, 'DH': 1294}
BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1246, 'Ten': 400, 'SS': 814, 'SkS': 400, 'Crit': 2509, 'DH': 1644}

#RDMStat = {"MainStat": 3378, "WD": 132, "Det": 1601, "Ten": 400, "SS": 502, "SkS": 400, "Crit": 2514, "DH": 1616} # Stats for RedMage
RDMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1673, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1544}
#RDMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1637, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1580}
RDMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1529, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1688}

SMNStat = {'MainStat': 3378, 'WD': 132, 'Det': 1534, 'Ten': 400, 'SS': 591, 'SkS': 400, 'Crit': 2555, 'DH': 1544} # Stats for Summoner
SMNStat = {'MainStat': 3378, 'WD': 132, 'Det': 1462, 'Ten': 400, 'SS': 591, 'SkS': 400, 'Crit': 2555, 'DH': 1616}
SMNStat = {'MainStat': 3378, 'WD': 132, 'Det': 1565, 'Ten': 400, 'SS': 538, 'SkS': 400, 'Crit': 2514, 'DH': 1616}
# Healer
SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 990, 'SkS': 400, 'Crit': 2502, 'DH': 688, 'Piety': 400} # Stats for Scholar
SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 918, 'SkS': 400, 'Crit': 2502, 'DH': 760, 'Piety': 400}
SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 954, 'SkS': 400, 'Crit': 2502, 'DH': 724, 'Piety': 400}
#SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2155, 'Ten': 400, 'SS': 810, 'SkS': 400, 'Crit': 2502, 'DH': 760, 'Piety': 400}
#SCHStat = {'MainStat': 3369, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1350, 'SkS': 400, 'Crit': 2430, 'DH': 400, 'Piety': 400}
#SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2155, 'Ten': 400, 'SS': 903, 'SkS': 400, 'Crit': 2409, 'DH': 760, 'Piety': 390}


WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "SkS" : 400, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage
ASTStat = {"MainStat": 2949, "WD":126, "Det" : 1659, "Ten" : 400, "SS": 1473, "SkS" : 400, "Crit" : 2280, "DH" : 436} # Stats for Astrologian
SGEStat = {"MainStat": 2928, "WD":126, "Det" : 1859, "Ten" : 400, "SS": 827, "SkS" : 400, "Crit" : 2312, "DH" : 1012} # Stats for Sage

# Physical Ranged
MCHStat = {"MainStat": 2937, "WD":126, "Det" : 1598, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2389, "DH" : 1592} # Stats for Machinist
BRDStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 400, "SkS" : 536, "Crit" : 2387, "DH" : 1340} # Stats for Bard
DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 400, "SkS" : 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer

# Melee
NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
SAMStat = {"MainStat": 2937, "WD":126, "Det" : 1571, "Ten" : 400, "SS": 400, "SkS" : 508, "Crit" : 2446, "DH" : 1459} # Stats for Samurai


DRGStat = {"MainStat": 3378, "WD":132, "Det" : 1870, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2567, "DH" : 1396} # Stats for Dragoon
#DRGStat = {'MainStat': 3378, 'WD': 132, 'Det': 1671, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2510, 'DH': 1652}

MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 400, "SkS" : 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1870, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1396} # Stats for Reaper
#RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1726, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1540}
#RPStat =   {'MainStat': 3378, 'WD': 132, 'Det': 1654, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2603, 'DH': 1468}
#RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1762, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1504}


# Tank {'MainStat': 3378, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 671, 'Crit': 2627, 'DH': 904}
DRKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 671, 'Crit': 2627, 'DH': 904} # Stats for DarkKnight
DRKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 924, 'Crit': 2447, 'DH': 832}
DRKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1772, 'Ten': 713, 'SS': 400, 'SkS': 780, 'Crit': 2662, 'DH': 796}
DRKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1916, 'Ten': 713, 'SS': 400, 'SkS': 888, 'Crit': 2662, 'DH': 544}

WARStat = {'MainStat': 3378, 'WD': 132, 'Det': 2182, 'Ten': 529, 'SS': 400, 'SkS': 400, 'Crit': 2576, 'DH': 940}
#WARStat = {'MainStat': 3378, 'WD': 132, 'Det': 1870, 'Ten': 400, 'SS': 400, 'SkS': 832, 'Crit': 2567, 'DH': 964}
#WARStat = {'MainStat': 3378, 'WD': 132, 'Det': 2019, 'Ten': 713, 'SS': 400, 'SkS': 970, 'Crit': 2585, 'DH': 436}

PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

#DRKStat =  {
#"MainStat" : 450,
#"WD" : 0,
#"Det" : 390,
#"Ten" : 400,
#"SS" : 400,
#"SkS" : 400,
#"Crit" : -70,
#"DH" : 400
#}  

# ===============================================================================================

# Here the player objects are being initialized. You do not need to change anything here.
# Note that if you want to simulate with two players of the same Jobs you will need to create another Player Object here.
# You can simply copy the objet's __init__ and change the name. 

# Caster player object
BLMPlayer = Player([], [], BLMStat, JobEnum.BlackMage)
RDMPlayer = Player([], [], RDMStat, JobEnum.RedMage)
SMNPlayer = Player([], [], SMNStat, JobEnum.Summoner)

# Healer player object
SCHPlayer = Player([], [], SCHStat, JobEnum.Scholar)
WHMPlayer = Player([], [], WHMStat, JobEnum.WhiteMage)
SGEPlayer = Player([], [], SGEStat, JobEnum.Sage)
ASTPlayer = Player([], [], ASTStat, JobEnum.Astrologian)

# Physical Ranged
MCHPlayer = Player([], [], MCHStat, JobEnum.Machinist)
BRDPlayer = Player([], [], BRDStat, JobEnum.Bard)
DNCPlayer = Player([], [], DNCStat, JobEnum.Dancer)

# Melee
NINPlayer = Player([], [], NINStat, JobEnum.Ninja)
SAMPlayer = Player([], [], SAMStat, JobEnum.Samurai)
DRGPlayer = Player([], [], DRGStat, JobEnum.Dragoon)
RPRPlayer = Player([], [], RPRStat, JobEnum.Reaper)
MNKPlayer = Player([], [], MNKStat, JobEnum.Monk)

# Tank
DRKPlayer = Player([], [], DRKStat, JobEnum.DarkKnight)
WARPlayer = Player([], [], WARStat, JobEnum.Warrior)
PLDPlayer = Player([], [], PLDStat, JobEnum.Paladin)
GNBPlayer = Player([], [], GNBStat, JobEnum.Gunbreaker)


# You can also use the Player.Set_etro_gearset(url : str) function to set up stats

#BLMPlayer.Set_etro_gearset(url)

# ===============================================================================================

# Here you can enter the action list you want the simulator to simulate. If you want to simulate a BlackMage go to the respective list, in that case you would write in BLMOpener\
# Note that this action list also includes the prepull. The simulator will start at soon as one of the player character does damage. So coordinate your different player with WaitAbility() so
# they all start at the same time.
# Note that if you are simulating with more than 1 per job you will need to create a new list of actions.

# Caster
BLMOpener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, SharpCast, Swiftcast, Despair, Manafront, Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, Blizzard3, Blizzard4,Paradox, SharpCast, Fire3, Fire4, Fire4, Thunder3, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]
SMNOpener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]
RDMOpener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]

# Healer
SCHOpener = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, WaitAbility(0), WaitAbility(0.25), EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
WHMOpener = [Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]
ASTOpener = [Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic]
SGEOpener = []

# Physical Ranged 
BRDOpener = []
MCHOpener = []
DNCOpener = []

# Melee
SAMOpener = []
DRGOpener = [TrueThrust, Disembowel, LanceCharge, DragonSight(RDMPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust, DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, SpineshafterDive, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust]
MNKOpener = []
NINOpener = []
RPROpener = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows, SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon ]

# Tank 
DRKOpener = [BloodWeapon, TBN(DRKPlayer), Potion, HardSlash, EdgeShadow, Delirium, SyphonStrike, Souleater, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, Bloodspiller, SaltDarkness, EdgeShadow, SyphonStrike, Plunge, EdgeShadow, HardSlash, SyphonStrike, Souleater]
#DRKOpener = [HardSlash]
#WAROpener = [HeavySwing, Infuriate, Maim, Potion, StormEye, InnerRelease, InnerChaos, Upheaval, Onslaught, PrimalRend, Infuriate, InnerChaos, Onslaught, FellCleave, FellCleave, HeavySwing, Maim, StormPath,FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, FellCleave, FellCleave]
WAROpener = [HeavySwing, Infuriate, Maim, WaitAbility(0.75), Potion, StormEye, InnerRelease, Upheaval, InnerChaos, Onslaught, FellCleave, Onslaught, PrimalRend, FellCleave, Onslaught, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, InnerChaos, HeavySwing, Upheaval, Maim, StormEye, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormEye, FellCleave, InnerRelease, Onslaught, FellCleave, FellCleave, PrimalRend, FellCleave, FellCleave, HeavySwing, Maim, StormEye, HeavySwing, Maim, StormEye, HeavySwing, Maim]
PLDOpener = []
GNBOpener = []

# ===============================================================================================

# Here we are linking the earlier created action list to the player object. You should not have to change anything here except if you are trying to simulate
# with more than 1 player per job. In which case you will need to link the earlier created object and the earlier created action list.

# Caster
BLMPlayer.ActionSet = BLMOpener
RDMPlayer.ActionSet = RDMOpener
SMNPlayer.ActionSet = SMNOpener

# Healer
SCHPlayer.ActionSet = SCHOpener
WHMPlayer.ActionSet = WHMOpener
ASTPlayer.ActionSet = ASTOpener
SGEPlayer.ActionSet = SGEOpener

# Physical Ranged
MCHPlayer.ActionSet = MCHOpener
BRDPlayer.ActionSet = BRDOpener
DNCPlayer.ActionSet = DNCOpener

# Melee
NINPlayer.ActionSet = NINOpener
SAMPlayer.ActionSet = SAMOpener
DRGPlayer.ActionSet = DRGOpener
RPRPlayer.ActionSet = RPROpener
MNKPlayer.ActionSet = MNKOpener

#Tank
DRKPlayer.ActionSet = DRKOpener
WARPlayer.ActionSet = WAROpener
PLDPlayer.ActionSet = PLDOpener
GNBPlayer.ActionSet = GNBOpener

# ===============================================================================================

# Here you will put into this list all the players you wish to simulate.
# Note that the limit is not 8, you can put as much as you want.
# Furthemore the simulator will compute the bonus 5% if it applies.
# So if you want to simulate the BlackMage and a RedMage, you would do: 
# PlayerList = [BLMPlayer, RDMPlayer]

PlayerList = [SCHPlayer]

Event.AddPlayer(PlayerList)

# ===============================================================================================

# Here you can change the final parameters to the simulation

TimeLimit = 500 # Time limit for the simulation in seconds. It will stop once this time has been reached (in simulation time)
time_unit = 0.01 # Time unit or frame of the simulation. Smallest step the simulator will take between each iterations. It is advised to not change this value
ShowGraph = False # Parameter to show (or not) the graph generated by the simulator.
RequirementOn = False # Parameter that will enable or disable the requirement check for all actions. If False the simulator will not check if an action can be done
IgnoreMana = True # True if want to ignore mana
vocal = True # True if want to view results

Event.RequirementOn = RequirementOn
Event.ShowGraph = ShowGraph
Event.IgnoreMana = IgnoreMana

findBiS = True

__logger__ = logging.getLogger("ffxivcalc") # root logger
level = logging.DEBUG if not findBiS else logging.WARNING
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
__logger__.setLevel(level=level) # __logger__ = logging.getLogger("ffxivcalc") 

if not findBiS:
    #Event.SimulateFight(time_unit, TimeLimit, vocal, n=0, PPSGraph=False, MaxTeamBonus=False) # Simulating fight
    pass

# ===============================================================================================


if findBiS:
    from ffxivcalc.GearSolver.Gear import ImportGear, Food
    from ffxivcalc.GearSolver.Solver import BiSSolver, getBaseStat, getGearDPSValue

    GearSpace = ImportGear("HealingGear.json")

    HD = Food({"DH" : [103, 0.1], "Det" : [62, 0.1]}, "Honeyed Dragonfruit")
    DB = Food({"SkS" : [103, 0.1], "DH" : [62, 0.1]}, "Dragonfruit Blend")
    BG = Food({"Crit" : [103, 0.1], "SkS" : [62, 0.1]}, "Baba Ghanoush")
    BE = Food({"Det" : [103, 0.1], "Crit" : [62, 0.1]}, "Baked Eggplant")
    CW = Food({"SS" : [103, 0.1], "DH" : [62, 0.1]}, "Caviar Sandwich")
    CC = Food({"Crit" : [103, 0.1], "SS" : [62, 0.1]}, "Caviar Canapes")
    MB = Food({"Ten" : [103, 0.1], "Det" : [62, 0.1]}, "Marinated Broccoflower")
    BS =  Food({"Det" : [103, 0.1], "Ten" : [62, 0.1]}, "Broccoflower Stew")
    foodSpace = [CC]

    Crit = 0
    DH = 1
    Det = 2
    Ten = 5
    materiaSpace = [Crit, DH, Det]
    optimal, random = BiSSolver(Event, GearSpace,materiaSpace, foodSpace,PercentileToOpt=["exp"], randomIteration=100, mendSpellSpeed=True,minSPDValue=0,maxSPDValue=1500, useNewAlgo=True, 
                                oversaturationIterationsPreGear=1, oversaturationIterationsPostGear=1,findOptMateriaGearBF=True)

if False:
    from ffxivcalc.GearSolver.Solver import computeDamageValue, getGearDPSValue
    from ffxivcalc.GearSolver.Gear import MateriaGenerator, GearSet, Food, ImportGear
    matGen = MateriaGenerator(18, 36)
    raidFood = Food({"Crit" : [103, 0.1], "SS" : [62, 0.1]}, "Caviar Canapes")

    data = ImportGear("HealingGear.json")
    Crit = 0
    DH = 1
    Det = 2
    SS = 3
    SkS = 4
    Weapon = data["WEAPON"][0]
    #Weapon.AddMateria(matGen.GenerateMateria(3))
    #Weapon.AddMateria(matGen.GenerateMateria(3))

    Head = data["HEAD"][1]
    Head.AddMateria(matGen.GenerateMateria(0))
    #Head.AddMateria(matGen.GenerateMateria(3))

    Body = data["BODY"][0]
    #Body.AddMateria(matGen.GenerateMateria(3))
    #Body.AddMateria(matGen.GenerateMateria(3))

    Hand = data["HANDS"][1]
    #Hand.AddMateria(matGen.GenerateMateria(3))
    #Hand.AddMateria(matGen.GenerateMateria(3))

    Leg = data["LEGS"][1]
    Leg.AddMateria(matGen.GenerateMateria(1))
    Leg.AddMateria(matGen.GenerateMateria(1))

    Feet = data["FEET"][0]
    Feet.AddMateria(matGen.GenerateMateria(1))
    Feet.AddMateria(matGen.GenerateMateria(1))

    Ear = data["EARRINGS"][1]
    Ear.AddMateria(matGen.GenerateMateria(0))
    Ear.AddMateria(matGen.GenerateMateria(0))

    Neck = data["NECKLACE"][0]
    Neck.AddMateria(matGen.GenerateMateria(0))
    Neck.AddMateria(matGen.GenerateMateria(0))

    Bracelet = data["BRACELETS"][0]
    Bracelet.AddMateria(matGen.GenerateMateria(1))
    Bracelet.AddMateria(matGen.GenerateMateria(1))
    #Bracelet.forceAddMateria(matGen.GenerateMateria(2))

    Lring = data["LRING"][1]
    Lring.AddMateria(matGen.GenerateMateria(1))
    Lring.AddMateria(matGen.GenerateMateria(1))
    #Lring.forceAddMateria(matGen.GenerateMateria(2))

    ring = data["RING"][0]
    ring.AddMateria(matGen.GenerateMateria(1))
    ring.AddMateria(matGen.GenerateMateria(1))

    gSet = GearSet()
    gSet.AddGear(Weapon)
    gSet.AddGear(Head)
    gSet.AddGear(Body)
    gSet.AddGear(Hand)
    gSet.AddGear(Leg)
    gSet.AddGear(Feet)
    gSet.AddGear(Ear)
    gSet.AddGear(Neck)
    gSet.AddGear(Bracelet)
    gSet.AddGear(Lring)
    gSet.AddGear(ring)
    gSet.addFood(raidFood)

    print(gSet.getMateriaTypeLimit(3, matGen))

    getGearDPSValue(Event, gSet, 0, n=0)