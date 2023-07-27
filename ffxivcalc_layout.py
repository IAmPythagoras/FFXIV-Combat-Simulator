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
BLMStat = {'MainStat': 3371, 'WD': 132, 'Det': 1493, 'Ten': 400, 'SS': 841, 'SkS': 400, 'Crit': 2492, 'DH': 1402} # Stats for BlackMage
RDMStat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "SkS" : 400, "Crit" : 2397, "DH" : 1544} # Stats for RedMage
SMNStat = {"MainStat": 2948, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 544, "SkS" : 400, "Crit" : 2436, "DH" : 1544} # Stats for Summoner

# Healer
SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "SkS" : 400, "Crit" : 2351, "DH" : 436} # Stats for Scholar
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
DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon
MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 400, "SkS" : 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
RPRStat = {"MainStat": 2946, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2462, "DH" : 1577} # Stats for Reaper

# Tank
DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "SkS" : 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
WARStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "SkS" : 400, "Crit" : 2377, "DH" : 1012} # Stats for Warrior
PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

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
SMNOpener = [Summon, Deathflare, Enkindle,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3,Ruin3]
RDMOpener = []

# Healer
SCHOpener = [WaitAbility(2),Broil,Biolysis, Broil, Swiftcast, ChainStratagem, Broil, Broil ]
WHMOpener = [Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]
ASTOpener = [Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic]
SGEOpener = []

# Physical Ranged 
BRDOpener = []
MCHOpener = []
DNCOpener = []

# Melee
SAMOpener = []
DRGOpener = []
MNKOpener = []
NINOpener = []
RPROpener = [SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice,SoulSlice]

# Tank 
DRKOpener = [BloodWeapon, TBN(DRKPlayer), Potion, HardSlash, EdgeShadow, Delirium, SyphonStrike, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, Bloodspiller, SaltDarkness, EdgeShadow, SyphonStrike, Plunge, EdgeShadow]
WAROpener = [TankStance, Provoke,Holmgang ,Maim, Maim, Maim, Maim, Maim, Maim, Maim, Maim]
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

PlayerList = [BLMPlayer]

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

__logger__ = logging.getLogger("ffxivcalc") # root logger
level = logging.WARNING
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
__logger__.setLevel(level=level) # __logger__ = logging.getLogger("ffxivcalc") 

#Event.SimulateFight(time_unit, TimeLimit, vocal, n=0, PPSGraph=False) # Simulating fight

# ===============================================================================================

from ffxivcalc.GearSolver.Gear import ImportGear, Food
from ffxivcalc.GearSolver.Solver import BiSSolver, getBaseStat, getGearDPSValue
import matplotlib.pyplot as plt
GearSpace = ImportGear("BLMSet.json")

HD = Food({"DH" : [103, 0.1], "Det" : [62, 0.1]}, "Honeyed Dragonfruit")
BE = Food({"Det" : [103, 0.1], "Crit" : [62, 0.1]}, "Baked Eggplant")
CW = Food({"SS" : [103, 0.1], "DH" : [62, 0.1]}, "Caviar Sandwich")
CC = Food({"Crit" : [103, 0.1], "SS" : [62, 0.1]}, "Caviar Canapes")
#optimal, random = BiSSolver(Event, GearSpace,[3,0,1,2] , [BE, HD, CW, CC],PercentileToOpt=["exp"], randomIteration=100, maxSPDValue=900, useNewAlgo=True, oversaturationLimit=0)


if True :
    from ffxivcalc.GearSolver.Solver import computeDamageValue, getGearDPSValue
    from ffxivcalc.GearSolver.Gear import MateriaGenerator, GearSet, Food
    matGen = MateriaGenerator(18, 36)
    foodDict = {"Crit" : [63, 0.1], "Det" : [103, 0.1]}
    raidFood = Food(foodDict, "Baked Eggplant")

    data = ImportGear("GearTest.json")
    Crit = 0
    DH = 1
    Det = 2
    SS = 3
    Weapon = data["WEAPON"][0]
    Weapon.AddMateria(matGen.GenerateMateria(1))
    Weapon.AddMateria(matGen.GenerateMateria(1))

    Head = data["HEAD"][1]
    Head.AddMateria(matGen.GenerateMateria(2))
    Head.AddMateria(matGen.GenerateMateria(3))
    Body = data["BODY"][1]
    Body.AddMateria(matGen.GenerateMateria(1))
    Body.AddMateria(matGen.GenerateMateria(1))
    Hand = data["HANDS"][0]
    Hand.AddMateria(matGen.GenerateMateria(1))
    Hand.AddMateria(matGen.GenerateMateria(1))

    Leg = data["LEGS"][0]
    Leg.AddMateria(matGen.GenerateMateria(0))
    Leg.AddMateria(matGen.GenerateMateria(0))

    Feet = data["FEET"][1]
    Feet.AddMateria(matGen.GenerateMateria(0))
    Feet.AddMateria(matGen.GenerateMateria(2))

    Ear = data["EARRINGS"][0]
    Ear.AddMateria(matGen.GenerateMateria(1))
    Ear.AddMateria(matGen.GenerateMateria(1))

    Neck = data["NECKLACE"][1]
    Neck.AddMateria(matGen.GenerateMateria(1))
    Neck.AddMateria(matGen.GenerateMateria(1))

    Bracelet = data["BRACELETS"][0]
    Bracelet.AddMateria(matGen.GenerateMateria(1))
    Bracelet.AddMateria(matGen.GenerateMateria(1))

    Lring = data["LRING"][0]
    Lring.AddMateria(matGen.GenerateMateria(1))
    Lring.AddMateria(matGen.GenerateMateria(1))

    ring = data["RING"][0]
    ring.AddMateria(matGen.GenerateMateria(0))
    ring.AddMateria(matGen.GenerateMateria(0))

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
    gSet.addFood(CC)


    getGearDPSValue(Event, gSet, 0,n=10000000)