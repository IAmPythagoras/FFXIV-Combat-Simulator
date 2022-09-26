# This will contain all action with their IDs in the game. It will map from ids -> name or name -> ids
from enum import IntEnum # Importing enums

# Caster

class CasterActions(IntEnum):
    Swiftcast = 7561
    LucidDreaming = 7562
    Surecast = 7559
    Addle = 7560
    Sleep = 25880
    Potion = -2

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# BlackMage

class BlackMageActions(IntEnum):
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
    Xeoglossy = 16507
    Amplifier = 25796

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# RedMage

class RedMageActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Summoner

class SummonerActions(IntEnum):
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
    AOEFountainOfFire = 16515
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Healer

class HealerActions(IntEnum):
    Repose = 16560
    Esuna = 7568
    Rescue = 7571
    Swiftcast = 7561
    LucidDreaming = 7562
    Surecast = 7559
    Potion = -2

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Astrologian

class AstrologianActions(IntEnum):
    Malefic = 25871
    Combust = 16554
    Gravity = 25872
    Draw = 3590
    Redraw = 3593
    MinorArcana = 7443
    SolarArcanum = 4401
    LunarArcanum = 4402
    CelestialArcanum = 4403
    LordOfCrown = 7444
    LadyOfCrown = 7445
    Astrodyne = 25870
    Divination = 16552
    NeutralSect = 16559
    EarthlyStar = 7439
    Benefic = 3594
    BeneficII = 3610
    AspectedBenific = 2595
    Helios = 3600
    AspectedHelios = 3601
    Synastry = 3612
    Collective = 3613
    CelestialOpposition = 16553
    CelestialIntersection = 16556
    Horoscope = 16557
    Exaltation = 25783
    Macrocosmos = 25874


    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Sage

class SageActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Scholar

class ScholarActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown


# Whitemage

class WhiteMageActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Tank

class TankActions(IntEnum):
    Rampart = 7531
    Reprisal = 7535
    ArmLength = 7548
    LowBlow = 7540
    Provoke = 7533
    Shirk = 7537
    TankStance = 16142
    Potion = -2

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# DarkKnight

class DarkKnightActions(IntEnum):
    HardSlah = 3617
    SyphoneStrike = 3623
    Unmend = 3624
    BloodWeapon = 3625
    Souleater = 3632
    DarkMind = 3634
    ShadowWall = 3636
    LivingDead = 3638
    SaltedEarth = 3639
    Plunge = 3640
    CarveSpit = 3643
    Delirium = 7390
    Bloodspiller = 7392
    TBN = 7393 # The Blackest Night
    EdgeOfShadow = 16470
    DarkMissionary = 16471
    LivingShadow = 16472
    Oblation = 25754
    SaltAndDarkness = 25755
    Shadowbringer = 25757

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Gunbreaker

class GunbreakerActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Paladin

class PaladinActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown'

# Warrior

class WarriorActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown
    
# Melee

class MeleeActions(IntEnum):
    SecondWind = 7541
    LegSweep = 7863
    Bloodbath = 7542
    Feint = 7549
    TrueNorth = 7546
    ArmLength = 7548
    Potion = -2

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Samurai

class SamuraiActions(IntEnum):
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

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown
    
# Reaper

class ReaperActions(IntEnum):
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
    SoulScyte = 24381
    Guillotine = 24384
    BloodStalk = 24389
    UnveiledGibbet = 24390
    UnveiledGallows = 24391
    GrimSwath = 24392
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
    ArcanaCrest = 24404
    ArcaneCircle = 24405
    HellIngress = 24402
    Regress = 24401
    Harpe = 24386

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown
    
# Ninja

class NinjaActions(IntEnum):
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
    ForkingRaiju = 25778

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Monk

class MonkActions(IntEnum):
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
    Brotherhood = 7396
    Anatman = 16475
    Mantra = 65

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# Dragoon

class DragoonActions(IntEnum):
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
    SpineshafterDive = 95
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
    
    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown


