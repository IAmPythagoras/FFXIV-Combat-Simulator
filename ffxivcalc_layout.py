from ffxivcalc.Enemy import Enemy, MagicRaidWide, PhysicalRaidWide, WaitEvent, TankBuster
from ffxivcalc.Fight import Fight
from ffxivcalc.Jobs.Player import Player
from ffxivcalc.Jobs.PlayerEnum import *
from copy import deepcopy
from ffxivcalc.helperCode.helper_backend import timeCheck

from ffxivcalc.Jobs.Base_Spell import WaitAbility, Potion, conditionalAction
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
BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390} # Stats for BlackMage
#BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1530, 'Ten': 400, 'SS': 2521, 'SkS': 400, 'Crit': 851, 'DH': 1331, 'Piety': 390}
#BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1277, 'Ten': 400, 'SS': 1292, 'SkS': 400, 'Crit': 2514, 'DH': 1150, 'Piety': 390}
RDMStat = {"MainStat": 3378, "WD": 132, "Det": 1601, "Ten": 400, "SS": 502, "SkS": 400, "Crit": 2514, "DH": 1616} # Stats for RedMage
RDMStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 538, 'SkS': 400, 'Crit': 2514, 'DH': 1580, 'Piety': 390}
SMNStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1342, 'Ten': 400, 'SS': 1411, 'SkS': 400, 'Crit': 2284, 'DH': 1196, 'Piety': 390} # Stats for Summoner

# Healer
SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1412, 'SkS': 400, 'Crit': 2306, 'DH': 440, 'Piety': 390} # Stats for Scholar
WHMStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for WhiteMage
ASTStat =  {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for Astrologian
SGEStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 954, 'SkS': 400, 'Crit': 2502, 'DH': 724, 'Piety': 390} # Stats for Sage

# Physical Ranged
MCHStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2557, 'DH': 1432, 'Piety': 390} # Stats for Machinist
MCHStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390}
BRDStat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2598, 'DH': 1252, 'Piety': 390} # Stats for Bard
DNCStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390} # Stats for Dancer
#DNCStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390}

# Melee
NINStat = {"MainStat": 3378, "WD":132, "Det" : 1697, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2554, "DH" : 1582} # Stats for Ninja
SAMStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1164, 'Ten': 400, 'SS': 400, 'SkS': 1513, 'Crit': 2282, 'DH': 1274, 'Piety': 390} # Stats for Samurai
#SAMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1325, 'Ten': 400, 'SS': 400, 'SkS': 1059, 'Crit': 2647, 'DH': 1202, 'Piety': 390}
DRGStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1726, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1540, 'Piety': 390} # Stats for Dragoon
MNKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1464, 'Ten': 400, 'SS': 400, 'SkS': 889, 'Crit': 2606, 'DH': 1274, 'Piety': 390} # Stats for Monk
MNKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1289, 'Ten': 400, 'SS': 400, 'SkS': 830, 'Crit': 2628, 'DH': 1458, 'Piety': 390}
RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1870, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2567, 'DH': 1360, 'Piety': 390} # Stats for Reaper

# Tank {'MainStat': 3338, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 671, 'Crit': 2627, 'DH': 904}
DRKStat =  {'MainStat': 3338, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 591, 'Crit': 2627, 'DH': 976, 'Piety': 390} # Stats for DarkKnight
WARStat =   {'MainStat': 3338, 'WD': 132, 'Det': 2023, 'Ten': 529, 'SS': 400, 'SkS': 948, 'Crit': 2481, 'DH': 652, 'Piety': 390}
PLDStat = {'MainStat': 3328, 'WD': 132, 'Det': 2182, 'Ten': 529, 'SS': 400, 'SkS': 400, 'Crit': 2576, 'DH': 940, 'Piety': 390} # Stats for Paladin
#GNBStat = {"MainStat": 3338, "WD":132, "Det" : 1901, "Ten" : 529, "SS": 400, "SkS" : 708, "Crit" : 2627, "DH" : 868} # Stats for Gunbreaker
GNBStat = {'MainStat': 3338, 'WD': 132, 'Det': 1944, 'Ten': 529, 'SS': 400, 'SkS': 1462, 'Crit': 2262, 'DH': 436, 'Piety': 390}
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
BLMOpener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
             Manafront, WaitAbility(1),Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
             Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
             Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]

SMNOpener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]

RDMOpener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
             Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, 
             Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, 
             Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]

# Healer
SCHOpener = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, WaitAbility(1), ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, 
            Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Biolysis, Broil, Broil,
			Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil]
WHMOpener = [Glare, ThinAir, Dia, Glare, WaitAbility(1), PresenceOfMind, Glare, Glare, Glare, Glare, Glare, ThinAir, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]
ASTOpener = [Malefic, Lightspeed, Combust, Malefic, Malefic, Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, 
            Malefic, Malefic,Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,
            Malefic, Malefic, Malefic]
SGEOpener = [Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Phlegma, Phlegma, Dosis, Dosis, Dosis, Dosis, Dosis, 
            Dosis, Dosis, Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, 
            Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]


# Physical Ranged 
BRDOpener = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]#,MageBallad, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, ArmyPaeon, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]
MCHOpener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
			Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
			HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
			GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]
#DNCOpener = [StandardStep, Pirouette, Jete, WaitAbility(15), StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish]
DNCOpener = [StandardStep, Pirouette, Jete, WaitAbility(15), StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]

# Melee
SAMOpener = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha]
DRGOpener = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
			LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
			HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
			Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
			Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
			Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive, RaidenThrust, WyrmwindThrust, VorpalThrust, Nastrond, HeavenThrust,
			FangAndClaw, WheelingThrust]

MNKOpener = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra, RisingPhoenix, RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, RisingPhoenix, TheForbiddenChakra, DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish, DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes, RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine, TwinSnakes, DragonKick, DragonKick, DragonKick, DragonKick ]
NINOpener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju, FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
RPROpener = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows, SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon ]

# Tank 
DRKOpener = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
            HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
			SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
			Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
			Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash ]

#DRKOpener = [HardSlash, SyphonStrike, Souleater,conditionalAction(HardSlash, timeCheck(5)), HardSlash]
#DRKOpener = [HardSlash]
#WAROpener = [HeavySwing, Infuriate, Maim, Potion, StormEye, InnerRelease, InnerChaos, Upheaval, Onslaught, PrimalRend, Infuriate, InnerChaos, Onslaught, FellCleave, FellCleave, HeavySwing, Maim, StormPath,FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, FellCleave, FellCleave]
WAROpener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]
#FastWAr = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Maim,Upheaval, StormPath, HeavySwing, InnerRelease, PrimalRend, FellCleave, FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, Maim, StormPath]

PLDOpener = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
GNBOpener = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown, RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, BrutalShell, NoMercy, RoughDivide, GnashingFang, JugularRip, DoubleDown, BlastingZone, RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel]

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

PlayerList = [PLDPlayer]

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

findBiS = False

__logger__ = logging.getLogger("ffxivcalc") # root logger
level = logging.DEBUG if not findBiS else logging.WARNING
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
__logger__.setLevel(level=level) # __logger__ = logging.getLogger("ffxivcalc") 

if not findBiS:
    Event.SimulateFight(time_unit, TimeLimit, vocal, n=500000, PPSGraph=False, MaxTeamBonus=False) # Simulating fight
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
    #foodSpace = [HD, BE, DB, BG]
    foodSpace = [HD,BE, CW, CC]

    Crit = 0
    DH = 1
    Det = 2
    Ten = 5
    materiaSpace = [Crit, DH, Det]
    optimal, random = BiSSolver(Event, GearSpace,materiaSpace, foodSpace,PercentileToOpt=["exp"], randomIteration=100, mendSpellSpeed=True,minSPDValue=400,maxSPDValue=700, useNewAlgo=True, 
                                oversaturationIterationsPreGear=1, oversaturationIterationsPostGear=1,findOptMateriaGearBF=True,swapDHDetBeforeSpeed=True)

if False:
    from ffxivcalc.GearSolver.Solver import computeDamageValue, getGearDPSValue, materiaBisSolverV3
    from ffxivcalc.GearSolver.Gear import MateriaGenerator, GearSet, Food, ImportGear
    matGen = MateriaGenerator(18, 36)

    raidFood = Food({"Crit" : [103, 0.1], "SkS" : [62, 0.1]}, "Baba Ghanoush")

    #data = ImportGear("StrikingGear.json")
    Crit = 0
    DH = 1
    Det = 2
    SS = 3
    SkS = 4
    """
    Weapon = data["WEAPON"][0]
    Weapon.AddMateria(matGen.GenerateMateria(4))
    Weapon.AddMateria(matGen.GenerateMateria(4))

    Head = data["HEAD"][0]
    Head.AddMateria(matGen.GenerateMateria(4))
    Head.AddMateria(matGen.GenerateMateria(1))

    Body = data["BODY"][0]
    Body.AddMateria(matGen.GenerateMateria(4))
    Body.AddMateria(matGen.GenerateMateria(4))

    Hand = data["HANDS"][0]
    Hand.AddMateria(matGen.GenerateMateria(4))
    Hand.AddMateria(matGen.GenerateMateria(1))

    Leg = data["LEGS"][1]
    Leg.AddMateria(matGen.GenerateMateria(4))
    Leg.AddMateria(matGen.GenerateMateria(4))

    Feet = data["FEET"][0]
    Feet.AddMateria(matGen.GenerateMateria(4))
    Feet.AddMateria(matGen.GenerateMateria(4))

    Ear = data["EARRINGS"][1]
    Ear.AddMateria(matGen.GenerateMateria(0))
    Ear.AddMateria(matGen.GenerateMateria(0))

    Neck = data["NECKLACE"][1]
    Neck.AddMateria(matGen.GenerateMateria(4))
    Neck.AddMateria(matGen.GenerateMateria(4))

    Bracelet = data["BRACELETS"][0]
    Bracelet.AddMateria(matGen.GenerateMateria(4))
    Bracelet.AddMateria(matGen.GenerateMateria(4))

    Lring = data["LRING"][0]
    Lring.AddMateria(matGen.GenerateMateria(4))
    Lring.AddMateria(matGen.GenerateMateria(4))

    ring = data["RING"][0]
    ring.AddMateria(matGen.GenerateMateria(4))
    ring.AddMateria(matGen.GenerateMateria(4))
    """

    gSet = GearSet()
    gSet.IsTank = False
    """
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
    """

    getGearDPSValue(Event, gSet, 0, n=0)