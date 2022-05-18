from Enemy import *
from Fight import *

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
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *

Dummy = Enemy()

#Stat
BLMCRITStat = {"MainStat": 2571, "WD":120, "Det" : 1518, "Ten" : 390, "SS": 884, "Crit" : 2323, "DH" : 1037} 
BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 400, "SS": 2171, "Crit" : 715, "DH" : 1454} 
SCHStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 944, "Crit" : 2277, "DH" : 616}
RDMStat = {"MainStat": 2563, "WD":120, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2348, "DH" : 1340}
MCHStat = {"MainStat": 2572, "WD":120, "Det" : 1615, "Ten" : 400, "SS": 400, "Crit" : 2121, "DH" : 1626}
NINStat = {"MainStat": 2555, "WD":120, "Det" : 1749, "Ten" : 400, "SS": 400, "Crit" : 2283, "DH" : 1330}
DRKStat = {"MainStat": 2521, "WD":120, "Det" : 1680, "Ten" : 539, "SS": 650, "Crit" : 2343, "DH" : 976}
WARStat = {"MainStat": 2521, "WD":120, "Det" : 2130, "Ten" : 1018, "SS": 400, "Crit" : 2240, "DH" : 400}
WHMStat = {"MainStat": 2571, "WD":120, "Det" : 1830, "Ten" : 400, "SS": 489, "Crit" : 2301, "DH" : 940}
SAMStat = {"MainStat": 2563, "WD":120, "Det" : 1654, "Ten" : 400, "SS": 579, "Crit" : 2310, "DH" : 1217}
PLDStat = {"MainStat": 2502, "WD":120, "Det" : 1680, "Ten" : 527, "SS": 650, "Crit" : 2319, "DH" : 1012}
GNBStat = {"MainStat": 2517, "WD":120, "Det" : 1612, "Ten" : 527, "SS": 950, "Crit" : 2205, "DH" : 868}
ASTStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 716, "Crit" : 2277, "DH" : 844}
SMNStat = {"MainStat": 2575, "WD":120, "Det" : 1688, "Ten" : 400, "SS": 489, "Crit" : 2296, "DH" : 1289}
BRDStat = {"MainStat": 2575, "WD":120, "Det" : 1381, "Ten" : 400, "SS": 479, "Crit" : 2229, "DH" : 1662}
DNCStat = {"MainStat": 2575, "WD":120, "Det" : 1453, "Ten" : 400, "SS": 549, "Crit" : 2283, "DH" : 1477}
DRGStat = {"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235}
RPRStat ={"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235}
Event = Fight([], Dummy)

#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

BLMPlayer = BlackMage(2.5, [], [], [EnochianEffect, ElementalEffect], Event, BLMCRITStat)
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


BLMOpener = [SharpCast, WaitAbility(16.5), Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Triplecast, Despair, Manafront, Fire4, Swiftcast, LucidDreaming, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose,Fire3, Fire4, Fire4, Fire4, Despair, Xenoglossy, Transpose, Paradox]
SCHOpener = [WaitAbility(17), Potion, WaitAbility(1), Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
RDMOpener = [WaitAbility(15), Verthunder, Verareo, Swiftcast, Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, Riposte, Fleche, Zwerchhau, Contre, Redoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Verfire, Verthunder,Verfire, Verthunder,Verfire,Fleche]
MCHOpener = [Ranged_AA,WaitAbility(15), Reassemble, WaitAbility(2.25), Potion, WaitAbility(1.5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, Reassemble, WaitAbility(1), Wildfire, ChainSaw, Automaton,WaitAbility(1), Hypercharge, HeatBlast, Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet, Drill, SplitShot,GaussRound, SlugShot,Ricochet,CleanShot,GaussRound,SplitShot, SlugShot,CleanShot,SlugShot]
DRKOpener = [Melee_AA,WaitAbility(19.25), BloodWeapon, HardSlash, EdgeShadow, Delirium, SyphonStrike, Potion, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, SyphonStrike, Plunge, EdgeShadow, HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike]
WAROpener = [Melee_AA,WaitAbility(19.99), Tomahawk, Infuriate, HeavySwing, Maim, WaitAbility(1),Potion, StormEye, InnerChaos, Upheaval, InnerRelease, PrimalRend, Onslaught, FellCleave,Onslaught, FellCleave,Onslaught, FellCleave, Infuriate, InnerChaos, HeavySwing,Maim, StormPath, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, Upheaval, StormEye]
WHMOpener = [WaitAbility(17), Potion, WaitAbility(1), Glare, Dia, Glare, Glare, Swiftcast, Glare, Assize, PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare, Glare, Glare ]
SAMOpener = [Melee_AA,WaitAbility(11), Meikyo, WaitAbility(8.25), Gekko, Potion, Kasha, Ikishoten, Yukikaze,Shinten, Midare,Shinten, Kaeshi, Senei, Meikyo, Gekko, Higanbana, Kasha, OgiNamikiri, KaeshiNamikiri, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Midare, Kaeshi, Hakaze, Yukikaze, Shinten,Hakaze, Jinpu]
PLDOpener = [Melee_AA,WaitAbility(20), FastBlade, FightOrFlight, RiotBlade, GoringBlade, FastBlade, Potion, RiotBlade, CircleScorn, Intervene, RoyalAuthority, Expiacion, RequestACat, Atonement, Intervene, Atonement, Atonement, FastBlade, RiotBlade, GoringBlade, HolySpirit, HolySpirit, HolySpirit, HolySpirit, Confetti, WaitAbility(1.75),CircleScorn, BladeFaith, WaitAbility(1.75), Expiacion,BladeTruth, BladeValor ]
GNBOpener = [Melee_AA,WaitAbility(20), KeenEdge, BrutalShell, Potion, SolidBarrel, NoMercy, GnashingFang, Bloodfest, JugularRip, DoubleDown, BlastingZone, BowShock, SonicBreak, RoughDivide, SavageClaw, AbdomenTear, RoughDivide, WickedTalon, EyeGouge, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, BrutalShell, SolidBarrel, GnashingFang, JugularRip, SavageClaw, AbdomenTear, WickedTalon,BlastingZone, EyeGouge, BurstStrike, Hypervelocity ]
ASTOpener = [WaitAbility(17.5), Potion, Malefic, Lightspeed, Combust, Arcanum(BLMPlayer, "Solar"), Draw, Malefic, Arcanum(DRGPlayer, "Lunar"), Draw, Malefic, Divination, Arcanum(BRDPlayer, "Celestial"), Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic ]
SMNOpener = [WaitAbility(18.5), Ruin3, Summon, SearingLight, AstralImpulse, Potion, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Titan, Topaz, Mountain, Topaz, Mountain,Topaz, Mountain,Topaz, Mountain, Garuda, Swiftcast, Slipstream]
BRDOpener = [Ranged_AA,WaitAbility(19), Potion, Stormbite, WandererMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, IronJaws, PitchPerfect3,  EmpyrealArrow, RefulgentArrow, BloodLetter, BurstShot, BloodLetter, RefulgentArrow, BurstShot,BloodLetter, RefulgentArrow, BurstShot, RefulgentArrow,EmpyrealArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow,  ]
DNCOpener = [Melee_AA,ClosedPosition(BLMPlayer, False),WaitAbility(4.5), StandardStep, Emboite, Entrechat, WaitAbility(11.74),Potion, StandardFinish, TechnicalStep, Emboite, Entrechat, Jete, Pirouette, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Emboite, Entrechat, StandardFinish]
DRGOpener = [Melee_AA,WaitAbility(20), TrueThrust, Potion, Disembowel, LanceCharge, DragonSight(BLMPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust, DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, SpineshafterDive, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust]
NINOpener = [Melee_AA,WaitAbility(9.5),Huton, Hide, WaitAbility(2.25), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi, WaitAbility(0.7), TrickAttack, AeolianEdge, DreamWithinADream, HyoshoRanryu, Raiton, TenChiJin, Ten, Chi, Jin, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge] 
RPROpener = [Melee_AA,Soulsow, WaitAbility(13.7), Harpe, ShadowOfDeath, Potion, SoulSlice, ArcaneCircle, Gluttony, Gibbet, Gallows, PlentifulHarvest, Enshroud, VoidReaping, CrossReaping, LemureSlice, VoidReaping, CrossReaping, LemureSlice, Communio, SoulSlice, UnveiledGibbet, Gibbet, Slice, WaxingSlice, ShadowOfDeath, InfernalSlice, Slice, WaxingSlice, UnveiledGallows, Gallows, InfernalSlice, Slice]

BLMPlayer.ActionSet = BLMOpener
SCHPlayer.ActionSet = SCHOpener
RDMPlayer.ActionSet = RDMOpener
MCHPlayer.ActionSet = MCHOpener
NINPlayer.ActionSet = NINOpener
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

Event.PlayerList = [BLMPlayer, SCHPlayer, RPRPlayer, BRDPlayer ,DRKPlayer,WARPlayer,ASTPlayer,DRGPlayer] #BLMPlayer, SCHPlayer, RPRPlayer, BRDPlayer ,DRKPlayer,WARPlayer,ASTPlayer,DRGPlayer


Event.SimulateFight(0.01, 200, 20)

