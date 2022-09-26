from ffxivppscalc.Jobs.Base_Spell import buff, empty, DOTSpell
from ffxivppscalc.Jobs.Tank.Tank_Spell import BigMit, GunbreakerSpell
import copy
Lock = 0.75


#Requirement

def CamouflageRequirement(Player, Spell):
    return Player.CamouflageCD <= 0, Player.CamouflageCD

def NoMercyRequirement(Player, Spell):
    return Player.NoMercyCD <= 0, Player.NoMercyCD

def RoughDivideRequirement(Player, Enemy):
    return Player.RoughDivideStack > 0, Player.RoughDivideCD

def BowShockRequirement(Player, Spell):
    return Player.BowShockCD <= 0, Player.BowShockCD

def SonicBreakRequirement(Player, Spell):
    return Player.SonicBreakCD <= 0, Player.SonicBreakCD

def DoubleDownRequirement(Player, Spell):
    return Player.DoubleDownCD <= 0, Player.DoubleDownCD

def HypervelocityRequirement(Player, Spell):
    return Player.ReadyToBlast, -1

def BloodfestRequirement(Player, Spell):
    return Player.BloodfestCD <= 0, Player.BloodfestCD

def BlastingZoneRequirement(Player, Spell):
    return Player.BlastingZoneCD <= 0, Player.BlastingZoneCD

def JugularRipRequirement(Player, Spell):
    return Player.ReadyToRip, -1

def AbdomenTearRequirement(Player, Spell):
    return Player.ReadyToTear, -1

def EyeGougeRequirement(Player, Spell):
    return Player.ReadyToGouge, -1

def AuroraRequirement(Player, Spell):
    return Player.AuroraStack > 0, Player.AuroraCD

def SuperbolideRequirement(Player, Spell):
    return Player.SuperbolideCD <= 0, Player.SuperbolideCD

def HeartOfLightRequirement(Player, Spell):
    return Player.HeartOfLightCD <= 0, Player.HeartOfLightCD

def HeartOfCorundumRequirement(Player, Spell):
    return Player.HeartOfCorundumCD <= 0, Player.HeartOfCorundumCD

#Apply

def ApplyCamouflage(Player, Enemy):
    Player.CamouflageCD = 90

def ApplyDemonSlice(Player, Enemy):
    if not (DemonSliceCombo in Player.EffectList) : Player.EffectList.append(DemonSliceCombo)

def ApplyHeartOfCorundum(Player, Enemy):
    Player.HeartOfCorundumCD = 25

def ApplyHeartOfLight(Player, Enemy):
    Player.HeartOfLightCD = 90

def ApplySuperbolide(Player, Enemy):
    Player.SuperbolideCD = 360

def ApplyAurora(Player, Enemy):
    if Player.AuroraStack == 2:
        Player.EffectCDList.append(AuroraStackCheck)
        Player.AuroraCD = 60
    Player.AuroraStack -= 1

def ApplyNoMercy(Player, Enemy):
    Player.buffList.append(NoMercyBuff)
    Player.NoMercyTimer = 20
    Player.NoMercyCD = 60
    Player.EffectCDList.append(NoMercyCheck)

def ApplyRoughDivide(Player, Enemy):
    if Player.RoughDivideStack == 2:
        Player.EffectCDList.append(RoughDivideStackCheck)
        Player.RoughDivideCD = 30
    Player.RoughDivideStack -= 1

def ApplyBowShock(Player, Enemy):
    Player.BowShockCD = 60
    Player.BowShockTimer = 15
    Player.BowShockDOT = copy.deepcopy(BowShockDOT)
    Player.DOTList.append(Player.BowShockDOT)
    Player.EffectCDList.append(BowShockDOTCheck)

def ApplySonicBreak(Player, Enemy):
    Player.SonicBreakCD = 60
    Player.SonicBreakTimer = 30
    Player.SonicBreakDOT = copy.deepcopy(SonicBreakDOT)
    Player.DOTList.append(Player.SonicBreakDOT)
    Player.EffectCDList.append(SonicBreakDOTCheck)

def ApplyDoubleDown(Player, Enemy):
    Player.DoubleDownCD = 60

def ApplyHypervelocity(Player, Enemy):
    Player.ReadyToBurst = False

def ApplyBurstStrike(Player, Enemy):
    Player.ReadyToBlast = True

def ApplyBloodfest(Player, Enemy):
    Player.PowderGauge = 3
    Player.BloodfestCD = 90

def ApplyBlastingZone(Player, Enemy):
    Player.BlastingZoneCD = 30

def ApplyKeenEdge(Player, Enemy):
    if not (KeenEdgeCombo in Player.EffectList) : Player.EffectList.append(KeenEdgeCombo)

def ApplyGnashingFang(Player, Enemy):
    Player.ReadyToRip = True
    Player.GnashingFangCD = 30

def ApplySavageClaw(Player, Enemy):
    Player.ReadyToRip = False
    Player.ReadyToTear = True

def ApplyWickedTalon(Player, Enemy):
    Player.ReadyToTear = False
    Player.ReadyToGouge = True

def ApplyEyeGouge(Player, Enemy):
    Player.ReadyToGauge = False

#Combo Effect

def DemonSliceCombo(Player, Spell):
    if Spell.id == DemonSlaughter.id:
        Spell.Potency += 60
        Player.PowderGauge = min(3, Player.PowderGauge + 1)
        Player.EffectToRemove.append(DemonSliceCombo)

def KeenEdgeCombo(Player, Spell):
    if Spell.id == BrutalShell.id:
        Spell.Potency += 140
        if not (BrutalShellCombo in Player.EffectList) : Player.EffectList.append(BrutalShellCombo)
        Player.EffectToRemove.append(KeenEdgeCombo)

def BrutalShellCombo(Player, Spell):
    if Spell.id == SolidBarrel.id:
        Spell.Potency += 220
        Player.PowderGauge = min(3, Player.PowderGauge + 1)
        Player.EffectToRemove.append(BrutalShellCombo)


#Check

def NoMercyCheck(Player, Enemy):
    if Player.NoMercyTimer <= 0:
        Player.buffList.remove(NoMercyBuff)
        Player.EffectToRemove.append(NoMercyCheck)

def BowShockDOTCheck(Player, Enemy):
    if Player.BowShockTimer <= 0:
        Player.DOTList.remove(Player.BowShockDOT)
        Player.BowShockDOT = None
        Player.EffectToRemove.append(BowShockDOTCheck)

def SonicBreakDOTCheck(Player, Enemy):
    if Player.SonicBreakTimer <= 0:
        Player.DOTList.remove(Player.SonicBreakDOT)
        Player.SonicBreakDOT = None
        Player.EffectToRemove.append(SonicBreakDOTCheck)

def RoughDivideStackCheck(Player, Enemy):
    if Player.RoughDivideCD <= 0:
        if Player.RoughDivideStack == 1:
            Player.EffectToRemove.append(RoughDivideStackCheck)
        else:
            Player.RoughDivideCD = 30
        Player.RoughDivideStack +=1

def AuroraStackCheck(Player, Enemy):
    if Player.AuroraCD <= 0:
        if Player.AuroraStack == 1:
            Player.EffectToRemove.append(AuroraStackCheck)
        else:
            Player.AuroraCD = 30
        Player.AuroraStack +=1


#Combo Action

KeenEdge = GunbreakerSpell(16137, True, 2.5, 170, ApplyKeenEdge, [], 0)
BrutalShell = GunbreakerSpell(16139, True, 2.5, 130, empty, [], 0)
SolidBarrel = GunbreakerSpell(16145, True, 2.5, 140, empty, [], 0)

GnashingFang = GunbreakerSpell(16146, True, 2.5, 380, ApplyGnashingFang, [], 1)
JugularRip = GunbreakerSpell(16156, False, 0, 200, empty, [JugularRipRequirement], 0)
SavageClaw = GunbreakerSpell(16147, True, 2.5, 460, ApplySavageClaw, [JugularRipRequirement], 0)
AbdomenTear = GunbreakerSpell(16157, False, 0, 240, empty, [AbdomenTearRequirement], 0)
WickedTalon = GunbreakerSpell(16150, True, 2.5, 540, ApplyWickedTalon, [AbdomenTearRequirement], 0)
EyeGouge = GunbreakerSpell(16158, False, 0, 280, ApplyEyeGouge, [EyeGougeRequirement], 0)

BurstStrike = GunbreakerSpell(16162, True, 2.5, 380, ApplyBurstStrike, [], 1)
Hypervelocity = GunbreakerSpell(25759, False, 0, 180, ApplyHypervelocity,[HypervelocityRequirement], 0)

#oGCD
BlastingZone = GunbreakerSpell(16165, False, 0, 720, ApplyBlastingZone, [BlastingZoneRequirement], 0)
Bloodfest = GunbreakerSpell(16164, False, 0, 0, ApplyBloodfest, [BloodfestRequirement], 0)
BowShock = GunbreakerSpell(16159, False, 0, 150, ApplyBowShock, [BowShockRequirement], 0)
BowShockDOT = DOTSpell(-10, 60, True)
RoughDivide = GunbreakerSpell(16154, False, 0, 150, ApplyRoughDivide, [RoughDivideRequirement], 0)
NoMercy = GunbreakerSpell(16138, False, 0, 0, ApplyNoMercy, [NoMercyRequirement], 0)
#GCD
DoubleDown = GunbreakerSpell(25760, True, 2.5, 1200, ApplyDoubleDown, [DoubleDownRequirement], 2)
SonicBreak = GunbreakerSpell(16153, True, 2.5, 300, ApplySonicBreak, [SonicBreakRequirement], 0)
SonicBreakDOT = DOTSpell(-9, 60,True)
LightningShot = GunbreakerSpell(16143, True, 2.5, 150, empty, [], 0)
#AOE GCD
FatedCircle = GunbreakerSpell(16163, True, 2.5, 290, empty, [], 1)
DemonSlice = GunbreakerSpell(16141, True, 2.5, 100, ApplyDemonSlice, [], 0)
DemonSlaughter = GunbreakerSpell(16149, True, 2.5, 100, empty, [], 1)


#Mit
Aurora = GunbreakerSpell(16151, False, 0, 0, ApplyAurora, [AuroraRequirement], 0)
Superbolide = GunbreakerSpell(16152, False, 0, 0, ApplySuperbolide, [SuperbolideRequirement], 0)
HeartOfLight = GunbreakerSpell(16160, False, 0, 0, ApplyHeartOfLight, [HeartOfLightRequirement], 0)
HeartOfCorundum = GunbreakerSpell(25758, False, 0, 0, ApplyHeartOfCorundum, [HeartOfCorundumRequirement], 0)
Camouflage = GunbreakerSpell(16140, False, 0, 0, ApplyCamouflage, [CamouflageRequirement], 0)
#buff
NoMercyBuff = buff(1.2)

GunbreakerAbility = {
16152 : Superbolide,
16143 : LightningShot,
16154 : RoughDivide,
16138 : NoMercy,
16164 : Bloodfest,
16137 : KeenEdge,
16139 : BrutalShell,
16145 : SolidBarrel,
16162 : BurstStrike,
16146 : GnashingFang,
16147 : SavageClaw,
16150 : WickedTalon,
16156 : JugularRip,
16157 : AbdomenTear,
16158 : EyeGouge,
25759 : Hypervelocity,
16153 : SonicBreak,
16165 : BlastingZone,
25760 : DoubleDown,
16141 : DemonSlice,
16149 : DemonSlaughter,
16163 : FatedCircle,
16148 : BigMit,
16140 : Camouflage,
25758 : HeartOfCorundum,
16151 : Aurora,
16160 : HeartOfLight,
16159 : BowShock
}