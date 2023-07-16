# This will contain all action with their IDs in the game. It will map from ids -> name or name -> ids
from enum import IntEnum
import logging
main_logging = logging.getLogger("ffxivcalc")
action_logging = main_logging.getChild("ActionEnum")

from ffxivcalc.Jobs.PlayerEnum import JobEnum, RoleEnum

class ActionEnum(IntEnum):
    # Parent enum class for all other enums. Will have
    # the two functions.

    @classmethod
    def name_for_id(cls, id : int) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def id_for_name(cls, name : str) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Caster

class CasterActions(ActionEnum):
    Swiftcast = 7561
    LucidDreaming = 7562
    Surecast = 7559
    Addle = 7560
    Sleep = 25880
    Potion = -2
    WaitAbility = 212

# BlackMage

class BlackMageActions(ActionEnum):
    Paradox = 25797
    FireI = 141
    FireII = 147
    FireIII = 152
    FireIV = 3577
    Despair = 16505
    Flare = 162
    HighFireII = 25794
    BlizzardI = 142
    BlizzardII = 25793
    BlizzardIII = 154
    BlizzardIV = 3576
    Freeze = 159
    HighBlizzardII = 25795
    UmbralSoul = 16505
    ThunderIII = 153
    ThunderIV = 7420
    Transpose = 149
    AetherialManipulation = 155
    Scathe = 156
    Manaward = 157
    Manafont = 158
    LeyLines = 3573
    Sharpcast = 3574
    BetweenTheLines = 7419
    Triplecast = 7421
    Foul = 7422
    Xenoglossy = 16507
    Amplifier = 25796


# RedMage

class RedMageActions(ActionEnum):
    Riposte = 7504
    Corps = 7506
    Verfire = 7510
    Verstone = 7511
    Zwerchhau = 7512
    Moulinet = 7513
    Vercure = 7514
    Redoublement = 7516
    Fleche = 7517
    Acceleration = 7518
    Contre = 7519
    Embolden = 7520
    Manafication = 7521
    Verraise = 7523
    Jolt = 7524
    Verthunder = 25855
    Verareo = 25856
    Impact = 16526
    Engagement = 16527
    Reprise = 16529
    MagickBarrier = 25857
    EnchantedRiposte = 7527
    EnchantedZwerchhau = 7528
    EnchantedRedoublement = 7529
    EnchantedMoulinet = 7530
    EnchantedReprise = 16528
    Resolution = 25858
    Verholy = 7526
    Verflare = 7525
    Scorch = 16530


# Summoner

class SummonerActions(ActionEnum):
    RuinIII = 3579
    RuinIV = 7426
    TryDisaster = 25826
    SearingLight = 25801
    SummonBahamut = 7427
    AstralImpulse = 25820
    AstralFlare = 25821
    Deathflare = 3582
    EnkindleBahamut = 7429
    SummonPhoenix = 25831
    FountainOfFire = 16514
    BrandOfPurgatory = 16515
    EnkindlePhoenix = 16516
    Ifrit = 25838
    Ruby = 25823
    RubyCatastrophe = 25832
    Cyclone = 25835
    Strike = 25885
    Titan = 25839
    Topaz = 25824
    TopazCatastrophe = 25833
    Mountain = 25836
    Garuda = 25840
    Emerald = 25825
    EmeraldCatastrophe = 25834
    Slipstream = 25837
    EnergyDrain = 16508
    EnergySyphon = 16510
    Fester = 181
    Painflare = 3578
    Physick = 16230
    Resurrection = 173
    Summon = 7427
    SummonEnkindle = -17

# Healer

class HealerActions(ActionEnum):
    Repose = 16560
    Esuna = 7568
    Rescue = 7571
    Swiftcast = 7561
    LucidDreaming = 7562
    Surecast = 7559
    Potion = -2
    WaitAbility = 212


# Astrologian

class AstrologianActions(ActionEnum):
    EssentialDignity = 10
    Ascend = 3603
    Lightspeed = 11
    Malefic = 25871
    Combust = 16554
    Gravity = 25872
    Draw = 3590
    Redraw = 3593
    MinorArcana = 7443
    Balance = 4401
    Bole = 4404
    Arrow = 4402
    Ewer = 4405
    Spear = 4403
    Spire = 4406
    CelestialArcanum = 4403
    LordOfCrown = 7444
    LadyOfCrown = 7445
    Astrodyne = 25870
    Divination = 16552
    NeutralSect = 16559
    EarthlyStar = 7439
    Benefic = 3594
    BeneficII = 3610
    AspectedBenefic = 2595
    Helios = 3600
    AspectedHelios = 3601
    Synastry = 3612
    CollectiveUnconscious = 3613
    CelestialOpposition = 16553
    CelestialIntersection = 16556
    Horoscope = 16557
    Exaltation = 25873
    Macrocosmos = 25874
    Microcosmos = 17


# Sage

class SageActions(ActionEnum):
    Egeiro = 24287
    Dosis = 24312
    EukrasianDosis = 24314
    Toxikon = 24316
    Dyskrasia = 24315
    Phlegma = 24313
    Kardia = 24285
    Eukrasia = 24290
    Diagnosis = 24284
    EukrasianDiagnosis = 24291
    Prognosis = 24286
    EukrasianPrognosis = 24292
    Physis = 24302
    Soteria = 24294
    Icarus = 24295
    Druochole = 24296
    Kerachole = 24298
    Ixochole = 24299
    Zoe = 24300
    Pepsis = 24301
    Taurochole = 24303
    Haima = 24305
    Rhizomata = 24309
    Holos = 24310
    Panhaima = 24311
    Krasis = 24317
    Pneuma = 24318
# Scholar

class ScholarActions(ActionEnum):
    Resurrection = 173
    Aetherflow = 166
    EnergyDrain = 167
    Adloquium = 185
    Succor = 186
    SacredSoil = 188
    Lustrate = 189
    Physick = 190
    Indomitability = 3583
    DeploymentTactic = 3585
    EmergencyTactic = 3586
    Dissipation = 3587
    Excogitation = 7434
    ChainStratagem = 7436
    Aetherpact = 7437
    WhisperingDawn = 16537
    FeyIllumination = 16538
    Recitation = 16542
    FeyBlessing = 16543
    SummonSeraph = 16545
    SummonEos = 16545
    Expedient = 25868
    Protraction = 25867
    ArtOfWar = 25866
    BroilIV = 25865
    RuinII = 17870
    Biolysis = 16540
    Consolation = 22
    Raise = 173



# Whitemage

class WhiteMageActions(ActionEnum):
    Glare = 25859
    Dia = 16532
    Holy = 25860
    AfflatusMisery = 16535
    Assize = 3571
    Cure = 120
    CureII = 135
    CureIII = 131
    Medica = 124
    MedicaII = 133
    Regen = 137
    Tetragrammaton = 3570
    Asylum = 3569
    DivineBenison = 7432
    Benediction = 140
    AfflatusSolace = 16531
    AfflatusRapture = 16534
    PresenceOfMind = 136
    ThinAir = 7430
    Temperance = 16536
    Aquaveil = 25861
    Bell = 25862
    PlenaryIndulgence = 19
    Raise = 125

# Tank

class TankActions(ActionEnum):
    Rampart = 7531
    Reprisal = 7535
    ArmLength = 7548
    LowBlow = 7540
    Provoke = 7533
    Shirk = 7537
    TankStance = 16142
    Potion = -2
    WaitAbility = 212
    Interject = 10101010


# DarkKnight

class DarkKnightActions(ActionEnum):
    Unleash = 20
    FloodOfShadow = 10
    StalwartSoul = 21
    Quietus = 5
    AbyssalDrain = 12
    HardSlash = 3617
    SyphonStrike = 3623
    Unmend = 3624
    BloodWeapon = 3625
    Souleater = 3632
    DarkMind = 3634
    ShadowWall = 3636
    LivingDead = 3638
    SaltedEarth = 3639
    Plunge = 3640
    CarveAndSpit = 3643
    Delirium = 7390
    Bloodspiller = 7392
    TheBlackestNight = 7393
    EdgeOfShadow = 16470
    DarkMissionary = 16471
    LivingShadow = 16472
    Oblation = 25754
    SaltAndDarkness = 25755
    Shadowbringer = 25757


# Gunbreaker

class GunbreakerActions(ActionEnum):
    Superbolide = 16152
    LightningShot = 16143
    RoughDivide = 16154
    NoMercy = 16138
    Bloodfest = 16164
    KeenEdge = 16137
    BrutalShell = 16139
    SolidBarrel = 16145
    BurstStrike = 16162
    GnashingFang = 16146
    SavageClaw = 16147
    WickedTalon = 16150
    JugularRip = 16156
    AbdomenTear = 16157
    EyeGouge = 16158
    Hypervelocity = 25759
    SonicBreak = 16153
    BlastingZone = 16165
    DoubleDown = 25760
    DemonSlice = 16141
    DemonSlaughter = 16149
    FatedCircle = 16163
    Nebula = 16148
    Camouflage = 16140
    HeartOfCorundum = 25758
    Aurora = 16151
    HeartOfLight = 16160
    BowShock = 16159

# Paladin

class PaladinActions(ActionEnum):
    HallowedGround = 30
    ShieldLob = 24
    Intervene = 16461
    FightOrFlight = 20
    Requiescat = 7383
    FastBlade = 9
    RiotBlade = 15
    GoringBlade = 3538
    RoyalAuthority = 3539
    Atonement = 16460
    HolySpirit = 7384
    Confiteor = 16459
    BladeOfFaith = 25748
    BladeOfTruth = 25749
    BladeOfValor = 25750
    Expiacion = 25747
    TotalEclipse = 7381
    Prominence = 16457
    CircleOfScorn = 23
    HolyCircle = 16458
    Sentinel = 17
    HolySheltron = 25746
    Intervention = 7382
    Cover = 27
    Clemency = 3541
    DivineVeil = 3540
    PassageOfArms = 7385


# Warrior

class WarriorActions(ActionEnum):
    Holmgang = 43
    Onslaught = 7386
    Infuriate = 52
    InnerRelease = 7389
    HeavySwing = 31
    Maim = 37
    StormPath = 42
    StormEye = 45
    FellCleave = 3549
    InnerChaos = 16465
    PrimalRend = 25753
    Upheaval = 7387
    Overpower = 41
    MythrilTempest = 16462
    Decimate = 3550
    ChaoticCyclone = 16463
    Orogeny = 25752
    Vengeance = 44
    ThrillOfBattle = 40
    Equilibrium = 3552
    Bloodwhetting = 25751
    NascentFlash = 16464
    ShakeItOff = 7388
    Tomahawk = 46
    
# Melee

class MeleeActions(ActionEnum):
    SecondWind = 7541
    LegSweep = 7863
    Bloodbath = 7542
    Feint = 7549
    TrueNorth = 7546
    ArmLength = 7548
    Potion = -2
    WaitAbility = 212

# Samurai

class SamuraiActions(ActionEnum):
    Hakaze = 7477
    Shifu = 7479
    Kasha = 7482
    Jinpu = 7478
    Gekko = 7481
    Yukikaze = 7480
    Fuko = 25780
    Oka = 7485
    Mangetsu = 7484
    Meikyo = 7499
    Higanbana = 7489
    TenkaGoken = 7488
    Midare = 7487
    OgiNamikiri = 25781
    KaeshiHiganbana = 16484
    KaeshiGoken = 16485
    KaeshiSetsugekka = 16486
    KaeshiNamikiri = 25782
    Shinten = 7490
    Kyuten = 7491
    Senei = 16481
    Guren = 7496
    Shoha = 16487
    ShohaII = 25779
    Ikishoten = 16482
    Meditate = 7497
    Hagakure = 7495
    Gyoten = 7492
    Yaten = 7493
    Enpi = 7486
    ThirdEye = 7498

    
# Reaper

class ReaperActions(ActionEnum):
    Slice = 24373
    WaxingSlice = 24374
    InfernalSlice = 24375
    ShadowOfDeath = 24378
    SoulSlice = 24380
    Gibbet = 24382
    Gallows = 24383
    SpinningScythe = 24376
    NightmareScythe = 24377
    WhorlOfDeath = 24379
    SoulScythe = 24381
    Guillotine = 24384
    BloodStalk = 24389
    UnveiledGibbet = 24390
    UnveiledGallows = 24391
    GrimSwathe = 24392
    Gluttony = 24393
    Soulsow = 24387
    HarvestMoon = 24388
    PlentifulHarvest = 24385
    Enshroud = 24394
    VoidReaping = 24395
    CrossReaping = 24396
    GrimReaping = 24397
    LemureSlice = 24399
    LemureScythe = 24400
    Communio = 24398
    ArcaneCrest = 24404
    ArcaneCircle = 24405
    HellIngress = 24402
    Regress = 24401
    Harpe = 24386

    
# Ninja

class NinjaActions(ActionEnum):
    SpinningEdge = 2240
    GustSlash = 2242
    AeolianEdge = 2255
    ArmorCrush = 3563
    ThrowingDagger = 2247
    ShadeShift = 2241
    DeathBlossom = 2254
    HakkeMujinsatsu = 16488
    Hide = 2245
    Mug = 2248
    TrickAttack = 2258
    Ten = 2259 # 18805 id from Kassatsu
    Chi = 2261 # 18806 id from Kassatsu
    Jin = 2263 # 18807 id from Kassatsu
    Ten2 = 18873 # Ten from TenChiJin
    Chi2 = 18877 # Chi from TenChiJin
    Jin2 = 18881 # Jin from TenChiJin
    FumaShuriken = 2265
    Katon = 2266
    Raiton = 2267
    Hyoton = 2268
    Huton = 2269
    Doton = 2270
    Suiton = 2271
    GokaMekkyaku = 16491
    HyoshoRanryu = 16492
    PhantomKamaitachi = 25774
    DreamWithinADream = 3566
    Huraijin = 25876
    Shukuchi = 2262
    HellfrogMedium = 7401
    Bhavacakra = 7402
    TenChiJin = 7403
    Bunshin = 16493
    FleetingRaiju = 25777
    ForkingRaiju = 25777
    Kassatsu = 2264
    Meisui = 16489


# Monk

class MonkActions(ActionEnum):
    BootShine = 53
    TrueStrike = 54
    Demolish = 66
    DragonKick = 74
    TwinSnakes = 61
    SnapPunch = 56
    ShadowOfTheDestroyer = 25767
    FourpointFurry = 16473
    Rockbreaker = 70
    Meditation = 3546
    TheForbiddenChakra = 3547
    Enlightenment = 16474
    PerfectBalance = 69
    ElixirField = 3545
    CelestialRevolution = 25765
    RisingPhoenix = 25768
    PhantomRush = 25769
    SixSidedStar = 16476
    FormShift = 4262
    Thunderclap = 25762
    RiddleOfEarth = 7394
    RiddleOfFire = 7395
    RiddleOfWind = 25766
    Brotherhood = 7396
    Anatman = 16475
    Mantra = 65


# Dragoon

class DragoonActions(ActionEnum):
    TrueThrust = 75
    VorpalThrust = 78
    HeavenThrust = 25771
    Disembowel = 87
    ChaoticSpring = 25772
    RaidenThrust = 16479
    FangAndClaw = 3554
    WheelingThrust = 3556
    DoomSpike = 86
    SonicThrust = 7397
    CoerthanTorment = 16477
    DraconianFury = 25770
    PiercingTalon = 90
    HighJump = 16478
    MirageDive = 7399
    SpineshatterDive = 95
    DragonFireDive = 96
    BattleLitany = 3557
    DragonSight = 7398
    LifeSurge = 83
    LanceCharge = 85
    ElusiveJump = 94
    Geirskogul = 3555
    Nastrond = 7400
    Stardiver = 16480
    WyrmwindThrust = 25773
    

# Physical Ranged

class RangedActions(ActionEnum):
    LegGraze = 7554
    FootGraze = 7553
    HeadGraze = 7551
    Peloton = 7557
    SecondWind = 7541
    ArmLength = 7548
    Potion = -2
    WaitAbility = 212


# Bard

class BardActions(ActionEnum):
    RagingStrike = 101
    Barrage = 107
    MageBallad = 114
    ArmyPaeon = 116
    RainOfDeath = 117
    BattleVoice = 118
    EmpyrealArrow = 3558
    WandererMinuet = 3559
    IronJaws = 3560
    WardenPaean = 3561
    Sidewinder = 3562
    PitchPerfect = 7404 # Assumed to be 3 stack
    Troubadour = 7405
    Causticbite = 7406
    Stormbite = 7407
    NatureMinne = 7408
    RefulgentArrow = 7409
    Shadowbite = 16494
    BurstShot = 16495
    ApexArrow = 16496 # Assumed to be 80 gauge
    Ladonsbite = 25783
    RadiantFinale = 25785
    RepellingShot = 112
    BloodLetter = 110
    BlastArrow = 25784

# Machinist

class MachinistActions(ActionEnum):
    SplitShot = 7411
    SlugShot = 7412
    ChainSaw = 25788
    Scattergun = 25768
    Hypercharge = 17209
    Tactician = 16889
    Overdrive = 16502
    Automaton = 16501
    AirAnchor = 16500
    Bioblaster = 16499
    Drill = 16498
    AutoCrossbow = 16497
    Flamethrower = 7418 # Assumed to be for 2.5s
    BarrelStabilizer = 7414
    CleanShot = 7413
    HeatBlast = 7410
    Wildfire = 2878
    Detonator = 1111111
    GaussRound = 2874
    Ricochet = 2890
    Reassemble = 2876

# Dancer

class DancerActions(ActionEnum):
    StarfallDance = 25792
    FanDanceIV = 25791
    CuringWaltz = 16015
    Improvisation = 16014
    Flourish = 16013
    Samba = 16012
    Devilment = 16011
    EnAvant = 16010
    FanDanceIII = 16009
    FanDanceII = 16008
    FanDanceI = 16007
    ClosedPosition = 16006
    SaberDance = 16005
    StandardStep = 15997
    TechnicalStep = 15998
    Bloodshower = 15996
    RisingWindmill = 15995
    Bladeshower = 15994
    Windmill = 15993
    FountainFall = 15992
    ReverseCascade = 15991
    Fountain = 15990
    Cascade = 15989
    TechnicalFinish = 16004
    StandardFinish = 16003
    ImprovisedFinish = 25789
    Ending = 18073
    Tillana = 25790
    Emboite = 15999
    Entrechat = 16000
    Jete = 16001
    Pirouette = 16002


# These are the functions we will call since they check for both cls and job_class
def name_for_id(id : int, cls : RoleEnum, job_cls : JobEnum):
    name = cls.name_for_id(id)
    if name == "Unknown": 
        name = job_cls.name_for_id(id)
    if name == "Unknown": # IF still unknown
        log_str = (
            "Unable to match ID : " + str(id) + " to an ability name in job : " + job_cls.__name__
        )
        action_logging.warning(log_str)
    return name

def id_for_name(name, cls, job_cls):
    id = cls.id_for_name(name)
    if id == -1: 
        id = job_cls.id_for_name(name)

    if id == -1 : # if still -1
        log_str = (
            "Unable to match name : " + name + " to an ability id in class : " + job_cls.__name__
        )
        
        action_logging.warning(log_str)
    return id

    