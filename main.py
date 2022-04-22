from Enemy import *
from Fight import *

from Jobs.Base_Spell import WaitAbility, Potion
#CASTER
from Jobs.Caster.Caster_Spell import SwiftCast
from Jobs.Caster.Blackmage.BlackMage_Spell import * 
from Jobs.Caster.Redmage.Redmage_Spell import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *

#HEALER
from Jobs.Healer.Scholar.Scholar_Spell import *
from Jobs.Healer.Whitemage.Whitemage_Spell import *
from Jobs.Healer.Astrologian.Astrologian_Spell import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *

#RANGED
from Jobs.Ranged.Machinist.Machinist_Spell import *
from Jobs.Ranged.Machinist.Machinist_Player import *

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
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *

Dummy = Enemy()

#Stat
BLMCRITStat = {"MainStat": 2571, "WD":120, "Det" : 1518, "Ten" : 390, "SS": 884, "Crit" : 2323, "DH" : 1037} 
BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 390, "SS": 2171, "Crit" : 715, "DH" : 1454} 
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


Event = Fight([], Dummy)

#DRKPlayer = DarkKnight(2.41, DRKAction, [], [DarksideEffect], Event)

BLMPlayer = BlackMage(2.5, [], [], [AstralFire, UmbralIce,UmbralHeartEffect], Event, BLMCRITStat)
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

BLMOpener = [Sharp, WaitAbility(16.5), F3, T3, F4, Triple, F4, Potion, F4, Amp, Ley, F4, Triple, Despair, Mana, F4, SwiftCast, Despair, Transpo, Para, Xeno, T3, F3, F4, F4, F4, Despair, Xeno, Transpo, Para]
SCHOpener = [WaitAbility(17), Potion, WaitAbility(1), Broil, Biolysis, Aetherflow, Broil, SwiftCast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
RDMOpener = [WaitAbility(15), Verthunder, Verareo, SwiftCast, Acceleration, Verthunder, Potion, Verthunder, Embolden, Manafication, Riposte, Fleche, Zwerchhau, Contre, Redoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Verfire, Verthunder,Verfire, Verthunder,Verfire,Fleche]
MCHOpener = [WaitAbility(15), Reassemble, WaitAbility(2.25), Potion, WaitAbility(1.5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, Reassemble, WaitAbility(1), Wildfire, ChainSaw, Automaton,WaitAbility(1), Hypercharge, HeatBlast, Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet,HeatBlast,GaussRound,HeatBlast,Ricochet, Drill, SplitShot,GaussRound, SlugShot,Ricochet,CleanShot,GaussRound,SplitShot, SlugShot,CleanShot,SlugShot]
NINOpener = [WaitAbility(18.5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, AeolianEdge, WaitAbility(1.75), TrickAttack, Kamaitachi, Hyosho, Raiton, TenChiJin, Meisui, Raiju, Bhavacakra,Raiju, Bhavacakra, SpinningEdge, Raiton, Raiju]
DRKOpener = [WaitAbility(19.25), BloodWeapon, HardSlash, EdgeShadow, Delirium, SyphonStrike, Potion, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, SyphonStrike, Plunge, EdgeShadow, HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike, Souleater,HardSlash, SyphonStrike]
WAROpener = [WaitAbility(20), Tomahawk, Infuriate, HeavySwing, Maim, WaitAbility(1),Potion, StormEye, InnerChaos, Upheaval, InnerRelease, PrimalRend, Onslaught, FellCleave,Onslaught, FellCleave,Onslaught, FellCleave, Infuriate, InnerChaos, HeavySwing,Maim, StormPath, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, Upheaval, StormEye]
WHMOpener = [WaitAbility(17), Potion, WaitAbility(1), Glare, Dia, Glare, Glare, SwiftCast, Glare, Assize, PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare, Glare, Glare ]
SAMOpener = [WaitAbility(11), Meikyo, WaitAbility(8.25), Gekko, Potion, Kasha, Ikishoten, Yukikaze,Shinten, Midare,Shinten, Kaeshi, Senei, Meikyo, Gekko, Higanbana, Kasha, OgiNamikiri, KaeshiNamikiri, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Midare, Kaeshi, Hakaze, Yukikaze, Shinten,Hakaze, Jinpu]
PLDOpener = [WaitAbility(20), FastBlade, FightOrFlight, RiotBlade, GoringBlade, FastBlade, Potion, RiotBlade, CircleScorn, Intervene, RoyalAuthority, Expiacion, RequestACat, Atonement, Intervene, Atonement, Atonement, FastBlade, RiotBlade, GoringBlade, HolySpirit, HolySpirit, HolySpirit, HolySpirit, Confetti, WaitAbility(1.75),CircleScorn, BladeFaith, WaitAbility(1.75), Expiacion,BladeTruth, BladeValor ]
GNBOpener = [WaitAbility(20), KeenEdge, BrutalShell, Potion, SolidBarrel, NoMercy, GnashingFang, Bloodfest, JugularRip, DoubleDown, BlastingZone, BowShock, SonicBreak, RoughDivide, SavageClaw, AbdomenTear, RoughDivide, WickedTalon, EyeGouge, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, BrutalShell, SolidBarrel, GnashingFang, JugularRip, SavageClaw, AbdomenTear, WickedTalon,BlastingZone, EyeGouge, BurstStrike, Hypervelocity ]
ASTOpener = [WaitAbility(17.5), Potion, Malefic, Lightspeed, Combust, Arcanum(WHMPlayer, "Solar"), Draw, Malefic, Arcanum(WHMPlayer, "Lunar"), Draw, Malefic, Divination, Arcanum(WHMPlayer, "Celestial"), Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic ]


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

#NinjaPlayer = Ninja(2.5, NINAction, [], [AutoEffect, NinjutsuTimerEffect], Event)
Event.PlayerList = [BLMPlayer, SCHPlayer, RDMPlayer, MCHPlayer ,DRKPlayer,WARPlayer,ASTPlayer,SAMPlayer] #BLMPlayer, SCHPlayer, RDMPlayer, MCHPlayer ,DRKPlayer,WARPlayer,ASTPlayer,SAMPlayer
Event.SimulateFight(0.01, 100, 20)

