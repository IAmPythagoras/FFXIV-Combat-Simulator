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
BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 824, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390} # Stats for BlackMage
RDMStat = {"MainStat": 3378, "WD": 132, "Det": 1601, "Ten": 400, "SS": 502, "SkS": 400, "Crit": 2514, "DH": 1616} # Stats for RedMage
SMNStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1342, 'Ten': 400, 'SS': 1411, 'SkS': 400, 'Crit': 2284, 'DH': 1196, 'Piety': 390} # Stats for Summoner

# Healer
SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2306, 'DH': 440, 'Piety': 390} # Stats for Scholar
WHMStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for WhiteMage
ASTStat =  {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for Astrologian
SGEStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 954, 'SkS': 400, 'Crit': 2502, 'DH': 724, 'Piety': 390} # Stats for Sage

# Physical Ranged
MCHStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2557, 'DH': 1432, 'Piety': 390} # Stats for Machinist
BRDStat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2598, 'DH': 1252, 'Piety': 390} # Stats for Bard
DNCStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390} # Stats for Dancer

# Melee
NINStat = {'MainStat': 3378, 'WD': 132, 'Det': 1666, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2595, 'DH': 1258, 'Piety': 390} # Stats for Ninja
SAMStat =  {'MainStat': 3367, 'WD': 132, 'Det': 1248, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2587, 'DH': 1422, 'Piety': 390} # Stats for Samurai
DRGStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1726, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1540, 'Piety': 390} # Stats for Dragoon
MNKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1464, 'Ten': 400, 'SS': 400, 'SkS': 889, 'Crit': 2606, 'DH': 1274, 'Piety': 390} # Stats for Monk
RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1870, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2567, 'DH': 1360, 'Piety': 390} # Stats for Reaper

DRKStat = {'MainStat': 3338, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 591, 'Crit': 2627, 'DH': 976, 'Piety': 390} # Stats for DarkKnight
WARStat = {'MainStat': 3338, 'WD': 132, 'Det': 2023, 'Ten': 529, 'SS': 400, 'SkS': 400, 'Crit': 2481, 'DH': 652, 'Piety': 390} # Stats for Warrior
PLDStat = {'MainStat': 3328, 'WD': 132, 'Det': 2182, 'Ten': 529, 'SS': 400, 'SkS': 400, 'Crit': 2540, 'DH': 976, 'Piety': 390}# Stats for Paladin
GNBStat = {'MainStat': 3338, 'WD': 132, 'Det': 1944, 'Ten': 529, 'SS': 400, 'SkS': 1462, 'Crit': 2262, 'DH': 436, 'Piety': 390}# Stats for Gunbreaker

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
BLMOpener = [SharpCast, Fire3, Thunder3, Fire4, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
             Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
             Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
             Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]

SMNOpener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]
RDMOpener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
             Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, 
             Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, 
             Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]


# Healer
SCHOpener = [Ruin, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
WHMOpener = [Glare, ThinAir, Dia, Glare, WaitAbility(1), PresenceOfMind, Glare, Glare, Glare, Glare, Glare, ThinAir, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]
ASTOpener = [Malefic, Lightspeed, Combust, Malefic, Malefic, Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, 
            Malefic, Malefic,Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,
            Malefic, Malefic, Malefic]
SGEOpener = [Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Phlegma, Phlegma, Dosis, Dosis, Dosis, Dosis, Dosis, 
            Dosis, Dosis, Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, 
            Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]


# Physical Ranged 
BRDOpener = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, WaitAbility(40)]#,MageBallad, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, ArmyPaeon, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]
MCHOpener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
			Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
			HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
			GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]
DNCOpener = [ClosedPosition(MCHPlayer),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
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
NINOpener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju, FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
RPROpener = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows, SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon]

# Tank 
DRKOpener = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
            HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
			SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
			Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
			Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash ]

WAROpener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
             FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
             HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
             FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]
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

PlayerList = [BRDPlayer]

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

findBiS = False # Set to True if want to find BiS instead.

__logger__ = logging.getLogger("ffxivcalc") # root logger
level = logging.DEBUG if not findBiS else logging.WARNING
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
__logger__.setLevel(level=level) 

if True:
    from ffxivcalc.helperCode.helper_backend import RestoreFightObject
    from save import save
    Event = RestoreFightObject(save)
    Event.RequirementOn = False
    Event.ShowGraph = False
    Event.IgnoreMana = True
    Event.SimulateFight(time_unit, TimeLimit, vocal, n=0, PPSGraph=False, MaxTeamBonus=False)

if False:#not findBiS:
    from ffxivcalc.helperCode.helper_backend import SaveFight
    print(Event.PlayerList[0].computeTimeStamp())
    Event.SimulateFight(time_unit, TimeLimit, vocal, n=0, PPSGraph=False, MaxTeamBonus=False) # Simulating fight
    if False : Event.simulationRecord.saveRecord()
    pass

# ===============================================================================================


if findBiS:
    from ffxivcalc.GearSolver.Gear import ImportGear, Food
    from ffxivcalc.GearSolver.Solver import BiSSolver, getBaseStat, getGearDPSValue

    GearSpace = ImportGear("BLMSet.json")

    HD = Food({"DH" : [103, 0.1], "Det" : [62, 0.1]}, "Honeyed Dragonfruit")
    DB = Food({"SkS" : [103, 0.1], "DH" : [62, 0.1]}, "Dragonfruit Blend")
    BG = Food({"Crit" : [103, 0.1], "SkS" : [62, 0.1]}, "Baba Ghanoush")
    BE = Food({"Det" : [103, 0.1], "Crit" : [62, 0.1]}, "Baked Eggplant")
    CW = Food({"SS" : [103, 0.1], "DH" : [62, 0.1]}, "Caviar Sandwich")
    CC = Food({"Crit" : [103, 0.1], "SS" : [62, 0.1]}, "Caviar Canapes")
    MB = Food({"Ten" : [103, 0.1], "Det" : [62, 0.1]}, "Marinated Broccoflower")
    BS =  Food({"Det" : [103, 0.1], "Ten" : [62, 0.1]}, "Broccoflower Stew")
    #foodSpace = [CC, CW, BE, HD]
    foodSpace = [BE]

    Crit = 0
    DH = 1
    Det = 2
    Ten = 5
    materiaSpace = [Crit, DH, Det]
    optimal, random, text = BiSSolver(Event, GearSpace,materiaSpace, foodSpace,PercentileToOpt=["exp"], randomIteration=100, mendSpellSpeed=True,minSPDValue=800,maxSPDValue=900, useNewAlgo=True, 
                                oversaturationIterationsPreGear=1, oversaturationIterationsPostGear=1,findOptMateriaGearBF=True,swapDHDetBeforeSpeed=True, minPiety=0)
    
# Sample code for importing fight from FFlogs
if False:
    from ffxivcalc.helperCode.helper_backend import RestoreFightObject
    from ffxivcalc.Request.FFLogs_api import getSingleFightData

    data = getSingleFightData("", "", "YbDaH9C6dNVJAh8T",
                          "67", showProgress=True)
    RestoreFightObject(data)

#if False:
#    from ffxivcalc.GearSolver.Gear import GearSet
#    from ffxivcalc.GearSolver.Solver import getGearDPSValue
#    print(getGearDPSValue(Event, GearSet(), 0, 1))