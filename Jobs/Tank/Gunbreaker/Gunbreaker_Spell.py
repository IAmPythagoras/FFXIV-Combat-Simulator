from Jobs.Base_Spell import buff, empty, DOTSpell
from Jobs.Tank.Tank_Spell import GunbreakerSpell
import copy
Lock = 0.75


#Requirement

def NoMercyRequirement(Player, Spell):
    return Player.NoMercyCD <= 0

def RoughDivideRequirement(Player, Enemy):
    return Player.RoughDivideStack > 0

def BowShockRequirement(Player, Spell):
    return Player.BowShockCD <= 0

def SonicBreakRequirement(Player, Spell):
    return Player.SonicBreakCD <= 0

def DoubleDownRequirement(Player, Spell):
    return Player.DoubleDownCD <= 0

def HypervelocityRequirement(Player, Spell):
    return Player.ReadyToBlast

def BloodfestRequirement(Player, Spell):
    return Player.BloodfestCD <= 0

def BlastingZoneRequirement(Player, Spell):
    return Player.BlastingZoneCD <= 0

def JugularRipRequirement(Player, Spell):
    return Player.ReadyToRip

def AbdomenTearRequirement(Player, Spell):
    return Player.ReadyToTear

def EyeGougeRequirement(Player, Spell):
    return Player.ReadyToGouge

#Apply

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
    Player.DoubleDownCD = 120

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

def KeenEdgeCombo(Player, Spell):
    if Spell.id == BrutalShell.id:
        Spell.Potency += 140
        if not (BrutalShellCombo in Player.EffectList) : Player.EffectList.append(BrutalShellCombo)
        Player.EffectToRemove.append(KeenEdgeCombo)

def BrutalShellCombo(Player, Spell):
    if Spell.id == SolidBarrel.id:
        Spell.Potency += 240
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


#Combo Action

KeenEdge = GunbreakerSpell(1, True, 2.5, 170, ApplyKeenEdge, [], 0)
BrutalShell = GunbreakerSpell(2, True, 2.5, 120, empty, [], 0)
SolidBarrel = GunbreakerSpell(3, True, 2.5, 120, empty, [], 0)

GnashingFang = GunbreakerSpell(4, True, 2.5, 360, ApplyGnashingFang, [], 1)
JugularRip = GunbreakerSpell(5, False, 0, 180, empty, [JugularRipRequirement], 0)
SavageClaw = GunbreakerSpell(6, True, 2.5, 440, ApplySavageClaw, [JugularRipRequirement], 0)
AbdomenTear = GunbreakerSpell(7, False, 0, 220, empty, [AbdomenTearRequirement], 0)
WickedTalon = GunbreakerSpell(8, True, 2.5, 520, ApplyWickedTalon, [AbdomenTearRequirement], 0)
EyeGouge = GunbreakerSpell(9, False, 0, 260, ApplyEyeGouge, [EyeGougeRequirement], 0)

BurstStrike = GunbreakerSpell(12, True, 2.5, 380, ApplyBurstStrike, [], 1)
Hypervelocity = GunbreakerSpell(13, False, 0, 180, ApplyHypervelocity,[HypervelocityRequirement], 0)

#oGCD
BlastingZone = GunbreakerSpell(10, False, 0, 700, ApplyBlastingZone, [BlastingZoneRequirement], 0)
Bloodfest = GunbreakerSpell(11, False, 0, 0, ApplyBloodfest, [BloodfestRequirement], 0)
BowShock = GunbreakerSpell(16, False, 0, 150, ApplyBowShock, [BowShockRequirement], 0)
BowShockDOT = DOTSpell(-10, 60, True)
RoughDivide = GunbreakerSpell(17, False, 0, 150, ApplyRoughDivide, [RoughDivideRequirement], 0)
NoMercy = GunbreakerSpell(18, False, 0, 0, ApplyNoMercy, [NoMercyRequirement], 0)
#GCD
DoubleDown = GunbreakerSpell(14, True, 2.5, 1200, ApplyDoubleDown, [DoubleDownRequirement], 2)
SonicBreak = GunbreakerSpell(15, True, 2.5, 300, ApplySonicBreak, [SonicBreakRequirement], 0)
SonicBreakDOT = DOTSpell(-9, 60,True)
LightningShot = GunbreakerSpell(19, True, 2.5, 150, empty, [], 0)

#buff
NoMercyBuff = buff(1.2)