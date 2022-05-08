from Jobs.Base_Spell import DOTSpell, empty
from Jobs.Melee.Melee_Spell import DragoonSpell
import copy

#Requirement

def TrueThrustRequirement(Player, Spell):
    return not Player.DraconianFire

def WheelingThrustRequirement(Player, Spell):
    return Player.WheelInMotion

def FangAndClawRequirement(Player, Spell):
    return Player.FangAndClaw

def LanceChargeRequirement(Player, Spell):
    return Player.LanceChargeCD <= 0

def BattleLitanyRequirement(Player, Spell):
    return Player.BattleLitanyCD <= 0

def DragonSightRequirement(Player, Spell):
    return Player.DragonSightCD <= 0

def GeirskogulRequirement(Player, Spell):
    return Player.GeirskogulCD <= 0 and not Player.LifeOfTheDragon

def NastrondRequirement(Player, Spell):
    return Player.LifeOfTheDragon and Player.NastrondCD <= 0

def HighJumpRequirement(Player, Spell):
    return Player.HighJumpCD <= 0

def MirageDiveRequirement(Player, Spell):
    return Player.DiveReady

def SpineshafterRequirement(Player, Spell):
    return Player.SpineshafterStack > 0

def LifeSurgeRequirement(Player, Spell):
    return Player.LifeSurgeStack > 0

def StardiverRequirement(Player, Spell):
    return Player.StardiverCD <= 0 and Player.LifeOfTheDragon

def RaidenThrustRequirement(Player, Spell):
    return Player.DraconianFire

def WyrmwindThrustRequirement(Player, Spell):
    return Player.FirstmindGauge == 2 and Player.WyrmwindThrustCD <= 0

def DragonFireDiveRequirement(Player, Spell):
    return Player.DragonFireDiveCD <= 0

#Apply

def ApplyDragonFireDive(Player, Enemy):
    Player.DragonFireDiveCD = 120

def ApplyTrueThrust(Player, Enemy):
    if not (TrueThrustCombo in Player.EffectList) : Player.EffectList.append(TrueThrustCombo)

def ApplyWheelingThrust(Player, Enemy):
    Player.WheelInMotion = False
    
    if not Player.LanceMastery: 
        Player.FangAndClaw = True
        Player.LanceMastery = True
        Player.EffectList.append(LanceMasteryCombo)
        Player.DraconianFire = True #Conditions met
    else: 
        Player.LanceMastery = False


def ApplyFangAndClaw(Player, Enemy):
    Player.FangAndClaw = False

    if not Player.LanceMastery: 
        Player.WheelInMotion = True
        Player.LanceMastery = True
        Player.EffectList.append(LanceMasteryCombo)
        Player.DraconianFire = True #Conditions met
    else:
        Player.LanceMastery = False
def ApplyLanceCharge(Player, Enemy):
    #print("BUFFING LANCE CHARGE")
    Player.MultDPSBonus *= 1.1
    #input(Player.MultDPSBonus)
    Player.LanceChargeCD = 60
    Player.LanceChargeTimer = 20
    Player.EffectCDList.append(LanceChargeCheck)

def ApplyBattleLitany(Player, Enemy):
    Player.BattleLitanyCD = 120
    Player.BattleLitanyTimer = 15

    #Will give each person in the fight the buff

    for player in Player.CurrentFight.PlayerList:  
        player.CritRateBonus += 0.1
        #input("BUFFING CRIT : " + str(player.CritRateBonus))

    Player.EffectCDList.append(BattleLitanyCheck)

def ApplyGeirskogul(Player, Enemy):
    Player.GeirskogulCD = 30

    if Player.DragonGauge == 2 : 
        Player.LifeOfTheDragon = True
        Player.LifeOfTheDragonTimer = 30
        Player.EffectCDList.append(LifeOfTheDragonCheck)

def ApplyHighJump(Player, Enemy):
    Player.HighJumpCD = 30
    Player.DiveReady = True

def ApplyMirageDive(Player, Enemy):
    Player.DiveReady = False
    Player.DragonGauge = min(2, Player.DragonGauge + 1)

def ApplySpineshafter(Player, Enemy):
    if Player.SpineshafterStack == 2:
        Player.EffectCDList.append(SpineshafterStackCheck)
        Player.SpineshafterCD = 60
    Player.SpineshafterStack -= 1

def ApplyLifeSurge(Player, Enemy):
    if Player.LifeSurgeStack == 2:
        Player.EffectCDList.append(LifeSurgeStackCheck)
        Player.LifeSurgeCD = 45
    Player.LifeSurgeStack -= 1

    Player.NextCrit = True

def ApplyWyrmwindThrust(Player, Enemy):
    Player.FirstmindGauge = 0
    Player.WyrmwindThrustCD = 10

def ApplyNastrond(Player, Enemy):
    Player.NastrondCD = 10

def ApplyStardiver(Player, Enemy):
    Player.StardiverCD = 30

def ApplyRaidenThrust(Player, Enemy):
    Player.FirstmindGauge = min(2, Player.FirstmindGauge + 1)
    Player.DraconianFire = False

    ApplyTrueThrust(Player, Enemy) #Since considered as first of combo

#Effect

def TrueThrustCombo(Player, Spell):
    if Spell.id == Disembowel.id:
        Spell.Potency += 110

        #Gain PowerSurge, 10% damage

        if Player.PowerSurgeTimer <= 0: #Not already applied
            #print("Buffing")
            Player.MultDPSBonus *= 1.10
            #input(Player.MultDPSBonus)
            Player.EffectCDList.append(PowerSurgeCheck)
        Player.PowerSurgeTimer = 30
        #input(Player.PowerSurgeTimer)

        Player.EffectList.append(DisembowelCombo)
        Player.EffectToRemove.append(TrueThrustCombo)

    elif Spell.id == VorpalThrust.id:
        Spell.Potency += 150
        Player.EffectList.append(VorpalThrustCombo)
        Player.EffectToRemove.append(TrueThrustCombo)

def VorpalThrustCombo(Player, Spell):
    if Spell.id == HeavenThrust.id:
        Spell.Potency += 380
        Player.FangAndClaw = True
        Player.EffectToRemove.append(VorpalThrustCombo)

def DisembowelCombo(Player, Spell):
    if Spell.id == ChaoticSpring.id:
        Spell.Potency +=160
        if Player.ChaoticSpringDOT == None:
            Player.ChaoticSpringDOT = copy.deepcopy(ChaoticSpringDOT)
            Player.DOTList.append(Player.ChaoticSpringDOT)
        Player.ChaoticSpringDOTTimer = 24

        Player.WheelInMotion = True 
        Player.EffectToRemove.append(DisembowelCombo)

def LanceMasteryCombo(Player, Spell):
    if Spell.id == FangAndClaw.id or Spell.id == WheelingThrust.id:
        Spell.Potency += 100
        Player.EffectToRemove.append(LanceMasteryCombo)
    elif isinstance(Spell, DragoonSpell) and Spell.Weaponskill:
        Player.FangAndClaw = False
        Player.WheelInMotion = False
        Player.LanceMastery = False
        Player.EffectToRemove.append(LanceMasteryCombo)



#Check

def LifeOfTheDragonCheck(Player, Enemy):
    if Player.LifeOfTheDragonTimer <= 0:
        Player.EffectToRemove.append(LifeOfTheDragonCheck)
        Player.LifeOfTheDragon = False

def LifeSurgeStackCheck(Player, Enemy):
    if Player.LifeSurgeCD <= 0:
        if Player.LifeSurgeStack == 1:
            Player.EffectToRemove.append(LifeSurgeStackCheck)
        else:
            Player.LifeSurgeCD = 45
        Player.LifeSurgeStack += 1

def SpineshafterStackCheck(Player, Enemy):
    if Player.SpineshafterCD <= 0:
        if Player.SpineshafterStack == 1:
            Player.EffectToRemove.append(SpineshafterStackCheck)
        else:
            Player.SpineShifterCD = 60
        Player.SpineshafterStack += 1

def BattleLitanyCheck(Player, Enemy):
    if Player.BattleLitanyTimer <= 0:
        #input("Removing battle litany")
        for player in Player.CurrentFight.PlayerList:  player.CritRateBonus -= 0.1 #Removing buff
        Player.EffectToRemove.append(BattleLitanyCheck)

def LanceChargeCheck(Player, Enemy):
    if Player.LanceChargeTimer <= 0:
        #input("Removing lance charge")
        Player.MultDPSBonus /= 1.1
        Player.EffectToRemove.append(LanceChargeCheck)

def PowerSurgeCheck(Player, Enemy):
    #input("in check : " + str(Player.PowerSurgeTimer))
    if Player.PowerSurgeTimer <= 0:
        #input("Removing powersurge")
        Player.EffectToRemove.append(PowerSurgeCheck)
        Player.MultDPSBonus /= 1.1

#GCD
#Combo Action
TrueThrust = DragoonSpell(1, True, 2.5, 230, ApplyTrueThrust, [TrueThrustRequirement], True)
Disembowel = DragoonSpell(2, True, 2.5, 140, empty, [], True)
VorpalThrust = DragoonSpell(3, True, 2.5, 130, empty, [], True)
ChaoticSpring = DragoonSpell(4, True, 2.5, 140, empty, [], True)
ChaoticSpringDOT = DOTSpell(-22, 45)
HeavenThrust = DragoonSpell(5, True, 2.5, 100, empty, [], True)

WheelingThrust = DragoonSpell(6, True, 2.5, 300, ApplyWheelingThrust, [WheelingThrustRequirement], True )
FangAndClaw = DragoonSpell(7, True, 2.5, 300, ApplyFangAndClaw, [FangAndClawRequirement], True)
RaidenThrust = DragoonSpell(18, True, 2.5, 280, ApplyRaidenThrust, [RaidenThrustRequirement], True)
PiercingTalon = DragoonSpell(21, True, 2.5, 150, empty, [], True)

#oGCD
LanceCharge = DragoonSpell(8, False, 0, 0, ApplyLanceCharge, [LanceChargeRequirement], False)
BattleLitany = DragoonSpell(9, False, 0, 0, ApplyBattleLitany, [BattleLitanyRequirement], False)
Geirskogul = DragoonSpell(11, False, 0, 260, ApplyGeirskogul, [GeirskogulRequirement], False)
Nastrond = DragoonSpell(12, False, 0, 300, ApplyNastrond, [NastrondRequirement], False)
HighJump = DragoonSpell(13, False, 0, 400, ApplyHighJump, [HighJumpRequirement], False)
MirageDive = DragoonSpell(14, False, 0, 200, ApplyMirageDive, [MirageDiveRequirement], False)
SpineshafterDive = DragoonSpell(15, False, 0, 250, ApplySpineshafter, [SpineshafterRequirement], False)
LifeSurge = DragoonSpell(16, False, 0, 0, ApplyLifeSurge, [LifeSurgeRequirement], False)
Stardiver = DragoonSpell(17, False, 0, 620, ApplyStardiver, [StardiverRequirement], False)
WyrmwindThrust = DragoonSpell(19, False, 0, 420, ApplyWyrmwindThrust, [WyrmwindThrustRequirement], False)
DragonFireDive = DragoonSpell(20, False, 0, 300, ApplyDragonFireDive, [DragonFireDiveRequirement], False)
def DragonSight(Target):

    def DragonSightCheck(Player, Enemy):
        if Player.DragonSightTimer <= 0:
            Player.MultDPSBonus /= 1.1
            Target.MultDPSBonus /= 1.05
            Player.EffectToRemove.append(DragonSightCheck)

    def ApplyDragonSight(Player, Enemy):
        Player.DragonSightCD = 120
        Player.DragonSightTimer = 20

        Player.MultDPSBonus *= 1.1
        Target.MultDPSBonus *= 1.05
        Player.EffectCDList.append(DragonSightCheck)

    return DragoonSpell(10, False, 0, 0, ApplyDragonSight, [DragonSightRequirement], False)