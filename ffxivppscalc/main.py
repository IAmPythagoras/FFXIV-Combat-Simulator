from Enemy import *
from Fight import *
import copy

from Jobs.Base_Spell import Melee_AA, Ranged_AA, WaitAbility, Potion
from Jobs.Caster.Caster_Spell import Swiftcast, LucidDreaming

#CASTER
from Jobs.Caster.Summoner.Summoner_Spell import *
from Jobs.Caster.Blackmage.BlackMage_Spell import * 
from Jobs.Caster.Redmage.Redmage_Spell import *
from Jobs.Caster.Summoner.Summoner_Player import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *

#HEALER
from Jobs.Healer.Sage.Sage_Spell import *
from Jobs.Healer.Scholar.Scholar_Spell import *
from Jobs.Healer.Whitemage.Whitemage_Spell import *
from Jobs.Healer.Astrologian.Astrologian_Spell import *
from Jobs.Healer.Sage.Sage_Player import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *

#RANGED
from Jobs.Ranged.Machinist.Machinist_Spell import *
from Jobs.Ranged.Bard.Bard_Spell import *
from Jobs.Ranged.Dancer.Dancer_Spell import *
from Jobs.Ranged.Machinist.Machinist_Player import *
from Jobs.Ranged.Bard.Bard_Player import *
from Jobs.Ranged.Dancer.Dancer_Player import *

#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Spell import *
from Jobs.Tank.DarkKnight.DarkKnight_Spell import *
from Jobs.Tank.Warrior.Warrior_Spell import *
from Jobs.Tank.Paladin.Paladin_Spell import *
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import *
from Jobs.Tank.DarkKnight.DarkKnight_Player import *
from Jobs.Tank.Warrior.Warrior_Player import *
from Jobs.Tank.Paladin.Paladin_Player import *

#MELEE
from Jobs.Melee.Samurai.Samurai_Spell import *
from Jobs.Melee.Ninja.Ninja_Spell import *
from Jobs.Melee.Dragoon.Dragoon_Spell import *
from Jobs.Melee.Reaper.Reaper_Spell import *
from Jobs.Melee.Monk.Monk_Spell import *
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *
from Jobs.Melee.Monk.Monk_Player import *


from FFLogsAPIRequest import getAbilityList
from UI_backend import BLMStat, SaveFight

Dummy = Enemy()

#Stat
# Caster
BLMStat = {"MainStat": 2945, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 840, "Crit" : 2386, "DH" : 1307} # Stats for BlackMage
RDMStat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "Crit" : 2397, "DH" : 1544} # Stats for RedMage
SMNStat = {"MainStat": 2948, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 544, "Crit" : 2436, "DH" : 1544} # Stats for Summoner

# Healer
SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "Crit" : 2351, "DH" : 436} # Stats for Scholar
WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage
ASTStat = {"MainStat": 2949, "WD":126, "Det" : 1659, "Ten" : 400, "SS": 1473, "Crit" : 2280, "DH" : 436} # Stats for Astrologian
SGEStat = {"MainStat": 2928, "WD":126, "Det" : 1859, "Ten" : 400, "SS": 827, "Crit" : 2312, "DH" : 1012} # Stats for Sage

# Physical Ranged
MCHStat = {"MainStat": 2937, "WD":126, "Det" : 1598, "Ten" : 400, "SS": 400, "Crit" : 2389, "DH" : 1592} # Stats for Machinist
BRDStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Bard
DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer

# Melee
NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
SAMStat = {"MainStat": 2937, "WD":126, "Det" : 1571, "Ten" : 400, "SS": 508, "Crit" : 2446, "DH" : 1459} # Stats for Samurai
DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon
MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
RPRStat = {"MainStat": 2946, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Reaper

# Tank
DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
WARStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for Warrior
PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

Event = Fight([], Dummy, False)

#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

BLMPlayer = BlackMage(2.5, [], [], [EnochianEffect, ElementalEffect], Event, BLMStat)
SCHPlayer = Scholar(2.5, [], [], [], Event, SCHStat)
RDMPlayer = Redmage(2.5, [], [], [DualCastEffect], Event, RDMStat)
MCHPlayer = Machinist(2.5, [], [], [], Event, MCHStat)
NINPlayer = Ninja(2.5, [], [], [], Event, NINStat)
DRKPlayer = DarkKnight(2.5, [], [], [], Event, DRKStat)
WARPlayer = Warrior(2.5, [], [], [SurgingTempestEffect], Event, WARStat)
WHMPlayer = Whitemage(2.5, [], [], [], Event, WHMStat)
SAMPlayer = Samurai(2.5, [], [], [], Event, SAMStat)
PLDPlayer = Paladin(2.5, [], [], [], Event, PLDStat)
GNBPlayer = Gunbreaker(2.5, [], [], [], Event, GNBStat)
ASTPlayer = Astrologian(2.5, [], [], [], Event, ASTStat)
SMNPlayer = Summoner(2.5, [], [], [], Event, SMNStat)
BRDPlayer = Bard(2.5, [], [], [SongEffect], Event, BRDStat)
DNCPlayer = Dancer(2.5, [], [], [EspritEffect], Event, DNCStat)
DRGPlayer = Dragoon(2.5, [], [], [], Event, DRGStat)
RPRPlayer = Reaper(2.5, [], [], [], Event, RPRStat)
MNKPlayer = Monk(2.5, [], [], [ComboEffect,FormlessStackCheck], Event, MNKStat)


PLDPlayer2 = Paladin(2.5, [], [], [], Event, PLDStat)
PLDPlayer3 = Paladin(2.5, [], [], [], Event, PLDStat)

BLMOpener = [SharpCast, WaitAbility(16.5), Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Triplecast, Despair, Manafront, Fire4, Swiftcast, LucidDreaming, Despair, Transpose, SharpCast, Paradox, Xenoglossy, Thunder3,Transpose,Fire3, Fire4, Fire4, Fire4, Despair, Xenoglossy, Transpose, Paradox]
SCHOpener = [WaitAbility(17), Potion, WaitAbility(1), Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
RDMOpener = [WaitAbility(15), Verthunder, Verareo, Swiftcast, Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Verfire, Verthunder,Verfire, Verthunder,Verfire,Fleche]
DRKOpener = [Melee_AA,WaitAbility(19.25), BloodWeapon, HardSlash, EdgeShadow, Delirium, SyphonStrike, Potion, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, SyphonStrike, Plunge, EdgeShadow, HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike]
WAROpener = [Melee_AA,WaitAbility(19.99), Tomahawk, Infuriate, HeavySwing, Maim, WaitAbility(1),Potion, StormEye, InnerChaos, Upheaval, InnerRelease, PrimalRend, Onslaught, FellCleave,Onslaught, FellCleave,Onslaught, FellCleave, Infuriate, InnerChaos, HeavySwing,Maim, StormPath, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, Upheaval, StormEye]
WHMOpener = [WaitAbility(17), Potion, WaitAbility(1), Glare, Dia, Glare, Glare, Swiftcast, Glare, Assize, PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare, Glare, Glare ]
SAMOpener = [Melee_AA,WaitAbility(11), Meikyo, WaitAbility(8.5), Gekko, Potion, Kasha, Ikishoten, Yukikaze, Midare, Senei, KaeshiSetsugekka, Meikyo, Gekko, Shinten, Higanbana, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Gekko, Gyoten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka]
PLDOpener = [Melee_AA,WaitAbility(20), FastBlade, FightOrFlight, RiotBlade, GoringBlade, FastBlade, Potion, RiotBlade, CircleScorn, Intervene, RoyalAuthority, Expiacion, RequestACat, Atonement, Intervene, Atonement, Atonement, FastBlade, RiotBlade, GoringBlade, HolySpirit, HolySpirit, HolySpirit, HolySpirit, Confetti, WaitAbility(1.75),CircleScorn, BladeFaith, WaitAbility(1.75), Expiacion,BladeTruth, BladeValor ]
GNBOpener = [Melee_AA,WaitAbility(20), KeenEdge, BrutalShell, Potion, SolidBarrel, NoMercy, GnashingFang, Bloodfest, JugularRip, DoubleDown, BlastingZone, BowShock, SonicBreak, RoughDivide, SavageClaw, AbdomenTear, RoughDivide, WickedTalon, EyeGouge, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, BrutalShell, SolidBarrel, GnashingFang, JugularRip, SavageClaw, AbdomenTear, WickedTalon,BlastingZone, EyeGouge, BurstStrike, Hypervelocity ]
ASTOpener = [WaitAbility(17.5), Potion, Malefic, Lightspeed, Combust, Arcanum(NINPlayer, "Solar"), Draw, Malefic, Arcanum(DRGPlayer, "Lunar"), Draw, Malefic, Divination, Arcanum(BRDPlayer, "Celestial"), Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic ]
SMNOpener = [WaitAbility(18.5), Ruin3, Summon, SearingLight, AstralImpulse, Potion, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Titan, Topaz, Mountain, Topaz, Mountain,Topaz, Mountain,Topaz, Mountain, Garuda, Swiftcast, Slipstream]
RPROpener = [Melee_AA,Soulsow, WaitAbility(13.7), Harpe, ShadowOfDeath, Potion, SoulSlice, ArcaneCircle, Gluttony, Gibbet, Gallows, PlentifulHarvest, Enshroud, VoidReaping, CrossReaping, LemureSlice, VoidReaping, CrossReaping, LemureSlice, Communio, SoulSlice, UnveiledGibbet, Gibbet, Slice, WaxingSlice, ShadowOfDeath, InfernalSlice, Slice, WaxingSlice, UnveiledGallows, Gallows, InfernalSlice, Slice]
DRGOpener = [Melee_AA,WaitAbility(20), TrueThrust, Potion, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust, DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, SpineshafterDive, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust]
BRDOpener = [WaitAbility(19.5), Potion, Stormbite, WandererMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, BurstShot, RadiantFinale, BattleVoice, BurstShot, Sidewinder,RefulgentArrow, Barrage, RefulgentArrow, BurstShot, RefulgentArrow, EmpyrealArrow, IronJaws]
DNCOpener = [ClosedPosition(NINPlayer, False),WaitAbility(4.5), StandardStep, Emboite, Entrechat, WaitAbility(11.74),Potion, StandardFinish, TechnicalStep, Emboite, Entrechat, Jete, Pirouette, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Emboite, Entrechat, StandardFinish]
MCHOpener = [Ranged_AA,WaitAbility(15), Reassemble, WaitAbility(2.25), Potion, WaitAbility(1.5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, Reassemble, WaitAbility(1), Wildfire, ChainSaw, Automaton,WaitAbility(1), Hypercharge, HeatBlast, Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet, Drill]
#MNKOpener = [WaitAbility(18), FormShift, Give_Monk_Auto,DragonKick, Potion, TwinSnakes, WaitAbility(1), RiddleOfFire, Demolish, TheForbiddenChakra, Bootshine, Brotherhood, WaitAbility(1), PerfectBalance, DragonKick, RiddleOfWind, Bootshine, DragonKick, ElixirField, Bootshine, PerfectBalance, TwinSnakes, DragonKick, Demolish, RisingPhoenix]
#MNKOpener2 = [WaitAbility(15), FormShift, WaitAbility(3), Potion, Give_Monk_Auto, TwinSnakes, WaitAbility(1), RiddleOfFire, Demolish, TheForbiddenChakra, DragonKick, Brotherhood, PerfectBalance, Bootshine, RiddleOfWind, TrueStrike, SnapPunch, RisingPhoenix, DragonKick, PerfectBalance, TwinSnakes, Bootshine, Demolish, RisingPhoenix]
#BLMPlayer.ActionSet = getAbilityList(client_id, client_secret)
BLMPlayer.ActionSet = BLMOpener
SCHPlayer.ActionSet = SCHOpener
RDMPlayer.ActionSet = RDMOpener
MCHPlayer.ActionSet = MCHOpener
#NINPlayer.ActionSet = NINOpener
DRKPlayer.ActionSet = DRKOpener
WARPlayer.ActionSet = WAROpener
WHMPlayer.ActionSet = WHMOpener
SAMPlayer.ActionSet = SAMOpener
PLDPlayer.ActionSet = PLDOpener
GNBPlayer.ActionSet = GNBOpener
ASTPlayer.ActionSet = ASTOpener
SMNPlayer.ActionSet = SMNOpener
BRDPlayer.ActionSet = BRDOpener
DNCPlayer.ActionSet = DNCOpener
DRGPlayer.ActionSet = DRGOpener
RPRPlayer.ActionSet = RPROpener
#MNKPlayer.ActionSet = MNKOpener2
Event.PlayerList = [] #BLMPlayer, SCHPlayer, RPRPlayer, BRDPlayer ,DRKPlayer,WARPlayer,ASTPlayer,DRGPlayer
Event.ShowGraph = True
#Event.SimulateFight(0.01, 1000, 20)

fightID = 'KVgxmW9fC26qhNGt'
fightNumber = '16'
action_dict, player_dict = getAbilityList(fightID, fightNumber)

for playerID in player_dict:
    player_dict[playerID]["job_object"].ActionSet = action_dict[playerID]
    player_dict[playerID]["job_object"].CurrentFight = Event
    job_name = player_dict[playerID]["job"] #getting job name

    if job_name == "Sage" : player_dict[playerID]["job_object"].Stat = SGEStat
    elif job_name == "Scholar" : player_dict[playerID]["job_object"].Stat = SCHStat
    elif job_name == "WhiteMage" : player_dict[playerID]["job_object"].Stat = WHMStat
    elif job_name == "Astrologian" : player_dict[playerID]["job_object"].Stat = ASTStat
    elif job_name == "Warrior" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(WARStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
    elif job_name == "DarkKnight" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRKStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        player_dict[playerID]["job_object"].EffectList = [BloodWeaponEffect] #Assuming we pre pull it
        player_dict[playerID]["job_object"].EffectCDList = [BloodWeaponCheck]
    elif job_name == "Paladin" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(PLDStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        player_dict[playerID]["job_object"].EffectList = [OathGauge]
    elif job_name == "Gunbreaker" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(GNBStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
    #Caster
    elif job_name == "BlackMage" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(BLMStat)
        player_dict[playerID]["job_object"].EffectList = [EnochianEffect, ElementalEffect]
    elif job_name == "RedMage" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(RDMStat)
        player_dict[playerID]["job_object"].EffectList = [DualCastEffect]
    elif job_name == "Summoner" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(SMNStat)
    #Ranged
    elif job_name == "Dancer" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(DNCStat)
        player_dict[playerID]["job_object"].EffectList = [EspritEffect]
        player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
    elif job_name == "Machinist" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(MCHStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
    elif job_name == "Bard" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(BRDStat)
        player_dict[playerID]["job_object"].EffectList = [SongEffect]
        player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
    #melee
    elif job_name == "Reaper" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(RPRStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
    elif job_name == "Monk" :  pass #Not yet Implemented
    elif job_name == "Dragoon" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRGStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
    elif job_name == "Ninja" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(NINStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
    elif job_name == "Samurai" : 
        player_dict[playerID]["job_object"].Stat = copy.deepcopy(SAMStat)
        player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)

    Event.PlayerList.append(player_dict[playerID]["job_object"])

Event.ShowGraph = True
Event.RequirementOn = False
print("Starting simulator")
Event.SimulateFight(0.01, 1000, 0)

