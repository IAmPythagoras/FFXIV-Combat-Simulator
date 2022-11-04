from ffxivcalc.Fight import Fight
from ffxivcalc.Enemy import Enemy

newEnemy = Enemy()
ShowGraph = True

newFight = Fight(newEnemy, ShowGraph) # Creating new Fight instance

from ffxivcalc.Jobs.Player import Player # Importing player class
from ffxivcalc.Jobs.PlayerEnum import JobEnum # Importing JobEnum
# Caster
Stat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "Crit" : 2397, "DH" : 1544} # Stats for RedMage

# Healer
SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "Crit" : 2351, "DH" : 436} # Stats for Scholar
WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage

# Physical Ranged
DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer

# Melee
NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon

# Tank
DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

# Caster player object
RDMPlayer = Player([], [], {}, JobEnum.RedMage)

# Healer player object
SCHPlayer = Player([], [], SCHStat, JobEnum.Scholar)
WHMPlayer = Player([], [], WHMStat, JobEnum.WhiteMage)

# Physical Ranged
DNCPlayer = Player([], [], DNCStat, JobEnum.Dancer)

# Melee
NINPlayer = Player([], [], NINStat, JobEnum.Ninja)
DRGPlayer = Player([], [], DRGStat, JobEnum.Dragoon)

# Tank
DRKPlayer = Player([], [], DRKStat, JobEnum.DarkKnight)
GNBPlayer = Player([], [], GNBStat, JobEnum.Gunbreaker)

from ffxivcalc.Jobs.Melee.Ninja.Ninja_Spell import * # Importing ninja actions
from ffxivcalc.Jobs.Melee.Dragoon.Dragoon_Spell import * # Importing dragoon actions
from ffxivcalc.Jobs.Melee.Melee_Spell import * # Importing melee actions

from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import * # Importing dancer actions
from ffxivcalc.Jobs.Ranged.Ranged_Spell import * # Importing physical ranged actions

from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import * # Importing redmage actions
from ffxivcalc.Jobs.Caster.Caster_Spell import * # Importing caster actions

from ffxivcalc.Jobs.Healer.Scholar.Scholar_Spell import * # Importing scholar actions
from ffxivcalc.Jobs.Healer.Whitemage.Whitemage_Spell import * # Importing whitemage actions
from ffxivcalc.Jobs.Healer.Healer_Spell import * # Importing healer actions

from ffxivcalc.Jobs.Tank.DarkKnight.DarkKnight_Spell import * # Importing darkknight actions
from ffxivcalc.Jobs.Tank.Gunbreaker.Gunbreaker_Spell import * # Importing gunbreaker actions
from ffxivcalc.Jobs.Tank.Tank_Spell import * # Importing tank actions

from ffxivcalc.Jobs.Base_Spell import Potion, WaitAbility

# Caster
RDMPlayer.ActionSet = [WaitAbility(15), Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Jolt, Verthunder, Fleche]

# Healer
SCHPlayer.ActionSet = [WaitAbility(18.5),Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain]
WHMPlayer.ActionSet = [WaitAbility(18.5),Glare, Dia, Glare, Glare, PresenceOfMind, Glare, Assize, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare]

# Physical Ranged 
DNCPlayer.ActionSet = [ClosedPosition(NINPlayer),StandardStep, Pirouette, Jete, WaitAbility(15), StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish]

# Melee
DRGPlayer.ActionSet = [WaitAbility(20),TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust, DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, SpineshafterDive, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust]
NINPlayer.ActionSet = [WaitAbility(10), Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju ]

# Tank 
DRKPlayer.ActionSet = [WaitAbility(16), BloodWeapon, WaitAbility(4), HardSlash, EdgeShadow, Delirium, SyphonStrike, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, Bloodspiller, SaltDarkness, EdgeShadow, SyphonStrike, Plunge, EdgeShadow]
GNBPlayer.ActionSet = [WaitAbility(20),LightningShot, KeenEdge, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BlastingZone, BowShock, DoubleDown, RoughDivide, SavageClaw, AbdomenTear, RoughDivide, WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge]


NINPlayer.Set_etro_gearset("https://etro.gg/gearset/73f9f3af-2fa1-4871-85a3-a0f6adbb5e28") # Set the Ninja's stat to be the etro gear set

newFight.AddPlayer([NINPlayer]) # Adding players to the fight

TimeUnit = 0.01 # Unit of time per frame
TimeLimit = 500 # Max running time of the simulation (time IN the simulation)

# Simulation parameters
newFight.RequirementOn = True # Will check for actions requirement
newFight.IgnoreMana = False # Will check for mana
vocal = True # Want to output data in text

#newFight.SimulateFight(TimeUnit, TimeLimit, vocal) # Simulating the fight


################################################


from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import *
from copy import deepcopy

newFire1 = deepcopy(Fire1) # Creates a new deepcopy of the fire 1 instance.

newFire1.Potency = 1000 # Changing the potency to 1000
newFire1.CastTime = 1 # Casting time in second
newFire1.RecastTime = 2.5 # 2.5 second before any other GCD actions can be done IF newFire1 is a GCD
newFire1.ManaCost = 10 # Updating mana cost
newFire1.Requirement = [] # Empty list so No requirement

def ApplynewFire1(Player, Enemy):
    Player.ElementalGauge = 3 # Setting Astral fire = 3
    
newFire1.Effect = [ApplynewFire1] # Giving new effect

newFight = Fight(newEnemy, ShowGraph) # Creating new Fight instance


BLMPlayer = Player([], [], Stat, JobEnum.BlackMage) # Creating BLM player

BLMPlayer.ActionSet = [newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1,newFire1] # Wacky action set

newFight.AddPlayer([BLMPlayer]) # Adding player to the fight


newFight.RequirementOn = True # Will check for actions requirement
newFight.IgnoreMana = False # Will check for mana
vocal = True # Want to output data in text

newFight.SimulateFight(TimeUnit, TimeLimit, vocal) # Simulating the fight
