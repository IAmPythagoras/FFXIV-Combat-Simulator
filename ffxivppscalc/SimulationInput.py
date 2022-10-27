import os

from Enemy import Enemy
from Fight import Fight
from Jobs.Player import Player
from Jobs.PlayerEnum import *
from copy import deepcopy

from Jobs.Base_Spell import WaitAbility, Potion
from Jobs.Caster.Caster_Spell import *
from Jobs.Melee.Melee_Spell import *
from Jobs.Ranged.Ranged_Spell import *
from Jobs.Healer.Healer_Spell import *
from Jobs.Tank.Tank_Spell import *

#CASTER
from Jobs.Caster.Summoner.Summoner_Spell import *
from Jobs.Caster.Blackmage.BlackMage_Spell import * 
from Jobs.Caster.Redmage.Redmage_Spell import *

#HEALER
from Jobs.Healer.Sage.Sage_Spell import *
from Jobs.Healer.Scholar.Scholar_Spell import *
from Jobs.Healer.Whitemage.Whitemage_Spell import *
from Jobs.Healer.Astrologian.Astrologian_Spell import *

#RANGED
from Jobs.Ranged.Machinist.Machinist_Spell import *
from Jobs.Ranged.Bard.Bard_Spell import *
from Jobs.Ranged.Dancer.Dancer_Spell import *

#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Spell import *
from Jobs.Tank.DarkKnight.DarkKnight_Spell import *
from Jobs.Tank.Warrior.Warrior_Spell import *
from Jobs.Tank.Paladin.Paladin_Spell import *

#MELEE
from Jobs.Melee.Samurai.Samurai_Spell import *
from Jobs.Melee.Ninja.Ninja_Spell import *
from Jobs.Melee.Dragoon.Dragoon_Spell import *
from Jobs.Melee.Reaper.Reaper_Spell import *
from Jobs.Melee.Monk.Monk_Spell import *

from UI_backend import SaveFight

def ExecuteMemoryCode(SaveFight_check):
    # This part of the code will execute whatever rotation is written here. It will be called from TUI.

    Dummy = Enemy()
    Event = Fight([], Dummy, False)


    # ===============================================================================================
    # You don't need to to worry about anything above this point

    # Stat Sheet
    # Enter your own stats here. The default is the 6.2 Savage BiS found on the Balance. The default Tenacity for non-tank is 400.
    # These stats must include the bonus stats food gives.

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

    # ===============================================================================================

    # Here the player objects are being initialized. You do not need to change anything here.
    # Note that if you want to simulate with two players of the same Jobs you will need to create another Player Object here.
    # You can simply copy the objet's __init__ and change the name. 

    # Caster player object
    BLMPlayer = Player([], [EnochianEffect, ElementalEffect], Event, deepcopy(BLMStat), JobEnum.BlackMage)
    RDMPlayer = Player([], [DualCastEffect], Event, deepcopy(RDMStat), JobEnum.RedMage)
    SMNPlayer = Player([], [], Event, deepcopy(SMNStat), JobEnum.Summoner)

    # Healer player object
    SCHPlayer = Player([], [], Event, deepcopy(SCHStat), JobEnum.Scholar)
    WHMPlayer = Player([], [], Event, deepcopy(WHMStat), JobEnum.WhiteMage)
    SGEPlayer = Player([], [], Event, deepcopy(SGEStat), JobEnum.Sage)
    ASTPlayer = Player([], [], Event, deepcopy(ASTStat), JobEnum.Astrologian)

    # Physical Ranged
    MCHPlayer = Player([], [], Event, deepcopy(MCHStat), JobEnum.Machinist)
    BRDPlayer = Player([], [SongEffect], Event, deepcopy(BRDStat), JobEnum.Bard)
    DNCPlayer = Player([], [EspritEffect], Event, deepcopy(DNCStat), JobEnum.Dancer)
    
    # Melee
    NINPlayer = Player([], [], Event, deepcopy(NINStat), JobEnum.Ninja)
    SAMPlayer = Player([], [], Event, deepcopy(SAMStat), JobEnum.Samurai)
    DRGPlayer = Player([], [], Event, deepcopy(DRGStat), JobEnum.Dragoon)
    RPRPlayer = Player([], [], Event, deepcopy(RPRStat), JobEnum.Reaper)
    MNKPlayer = Player([], [ComboEffect], Event, deepcopy(MNKStat), JobEnum.Monk)

    # Tank
    DRKPlayer = Player([], [], Event, deepcopy(DRKStat), JobEnum.DarkKnight)
    WARPlayer = Player([], [SurgingTempestEffect], Event, deepcopy(WARStat), JobEnum.Warrior)
    PLDPlayer = Player([], [], Event, deepcopy(PLDStat), JobEnum.Paladin)
    GNBPlayer = Player([], [], Event, deepcopy(GNBStat), JobEnum.Gunbreaker)


    # ===============================================================================================

    # Here you can enter the action list you want the simulator to simulate. If you want to simulate a BlackMage go to the respective list, in that case you would write in BLMOpener\
    # Note that this action list also includes the prepull. The simulator will start at soon as one of the player character does damage. So coordinate your different player with WaitAbility() so
    # they all start at the same time.
    # Note that if you are simulating with more than 1 per job you will need to create a new list of actions.

    # Caster
    BLMOpener = []
    SMNOpener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan]
    RDMOpener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Jolt, Verthunder, Fleche]
    
    # Healer
    SCHOpener = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain]
    WHMOpener = [Glare, Dia, Glare, Glare, PresenceOfMind, Glare, Assize, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare]
    ASTOpener = [Malefic, Lightspeed, Combust, Malefic, Malefic, Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic ]
    SGEOpener = [Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Phlegma, Phlegma, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]

    # Physical Ranged 
    BRDOpener = [Stormbite, WandererMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, IronJaws, PitchPerfect3, WaitAbility(50)]
    MCHOpener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton, WaitAbility(2),Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, WaitAbility(60)]
    DNCOpener = [StandardStep, Pirouette, Jete, WaitAbility(15), StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish]

    # Melee
    SAMOpener = [Meikyo, WaitAbility(9), Gekko, Kasha, Ikishoten, Yukikaze, Midare, Senei, KaeshiSetsugekka, Meikyo, Gekko, Shinten, Higanbana,Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Gekko, Gyoten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka ]
    DRGOpener = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust, DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, SpineshafterDive, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, WaitAbility(50)]
    MNKOpener = [FormShift, DragonKick, TwinSnakes, RiddleOfFire, Demolish, TheForbiddenChakra, Bootshine, Brotherhood, PerfectBalance, DragonKick, RiddleOfWind, Bootshine, DragonKick, ElixirField, Bootshine, PerfectBalance, TwinSnakes, DragonKick, Demolish, RisingPhoenix]
    NINOpener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju ]
    RPROpener = [Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, PlentifulHarvest, Enshroud, VoidReaping, CrossReaping, LemureSlice, VoidReaping, CrossReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet]

    # Tank 
    DRKOpener = [BloodWeapon, WaitAbility(4), HardSlash, EdgeShadow, Delirium, SyphonStrike, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, Bloodspiller, SaltDarkness, EdgeShadow, SyphonStrike, Plunge, EdgeShadow]
    WAROpener = [Tomahawk, Infuriate, HeavySwing, Maim, StormEye, InnerRelease, InnerChaos, Upheaval, Onslaught, PrimalRend, Infuriate, InnerChaos, Onslaught, FellCleave, Onslaught, FellCleave, FellCleave, HeavySwing, Maim, StormPath, FellCleave, Infuriate, InnerChaos]
    PLDOpener = [HolySpirit, FastBlade, FightOrFlight, RiotBlade, GoringBlade, FastBlade, RiotBlade, CircleScorn, Expiacion, RoyalAuthority, Intervene, RequestACat, Atonement, Intervene, Atonement, Atonement, FastBlade, RiotBlade, GoringBlade, HolySpirit, HolySpirit, HolySpirit, HolySpirit, Confetti,BladeFaith, BladeTruth, BladeValor, WaitAbility(50) ]
    GNBOpener = [LightningShot, KeenEdge, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BlastingZone, BowShock, DoubleDown, RoughDivide, SavageClaw, AbdomenTear, RoughDivide, WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, WaitAbility(50)]


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
 
    Event.PlayerList = PlayerList

    # ===============================================================================================

    # Here you can change the final parameters to the simulation

    TimeLimit = 500 # Time limit for the simulation in seconds. It will stop once this time has been reached (in simulation time)
    time_unit = 0.01 # Time unit or frame of the simulation. Smallest step the simulator will take between each iterations. It is advised to not change this value
    ShowGraph = False # Parameter to show (or not) the graph generated by the simulator.
    RequirementOn = True # Parameter that will enable or disable the requirement check for all actions. If False the simulator
                         # will not check if an action can be done

    # ===============================================================================================

    if SaveFight_check: #If we wish to save the fight

        os.system('CLS') #clearing HUD

        print(
        "===================== SAVE FIGHT IN CODE ====================="
        )
        filename = input("Enter the name you wish to save the fight as : ")

        SaveFight(Event, 0, TimeLimit, filename)
    else:
        Event.RequirementOn = RequirementOn
        Event.ShowGraph = ShowGraph
        Event.SimulateFight(time_unit, TimeLimit, vocal=True)
        print("=========================================================")
        input("Press any key to go back to the main")

