from Jobs.Base_Spell import DOTSpell, buff, empty
from Jobs.Melee.Melee_Spell import Bloodbath, DragoonSpell, SecondWind
import copy

#Requirement

def TrueThrustRequirement(Player, Spell):
    return not Player.DraconianFire, -1

def WheelingThrustRequirement(Player, Spell):
    return Player.WheelInMotion, -1

def FangAndClawRequirement(Player, Spell):
    return Player.FangAndClaw, -1

def LanceChargeRequirement(Player, Spell):
    return Player.LanceChargeCD <= 0, Player.LanceChargeCD

def BattleLitanyRequirement(Player, Spell):
    return Player.BattleLitanyCD <= 0, Player.BattleLitanyCD

def DragonSightRequirement(Player, Spell):
    return Player.DragonSightCD <= 0, Player.DragonSightCD

def GeirskogulRequirement(Player, Spell):
    return Player.GeirskogulCD <= 0 and not Player.LifeOfTheDragon, Player.GeirskogulCD

def NastrondRequirement(Player, Spell):
    return Player.LifeOfTheDragon and Player.NastrondCD <= 0, Player.NastrondCD

def HighJumpRequirement(Player, Spell):
    return Player.HighJumpCD <= 0, Player.HighJumpCD

def MirageDiveRequirement(Player, Spell):
    return Player.DiveReady, -1

def SpineshafterRequirement(Player, Spell):
    return Player.SpineshafterStack > 0, Player.SpineshafterCD

def LifeSurgeRequirement(Player, Spell):
    return Player.LifeSurgeStack > 0, Player.LifeSurgeCD

def StardiverRequirement(Player, Spell):
    return Player.StardiverCD <= 0 and Player.LifeOfTheDragon, Player.StardiverCD

def RaidenThrustRequirement(Player, Spell):
    return Player.DraconianFire, -1

def WyrmwindThrustRequirement(Player, Spell):
    return Player.FirstmindGauge == 2 and Player.WyrmwindThrustCD <= 0, -1

def DragonFireDiveRequirement(Player, Spell):
    return Player.DragonFireDiveCD <= 0, Player.DragonFireDiveCD

#Apply

def ApplyDoomSpike(Player, Enemy):
    if not (DoomSpikeCombo in Player.EffectList ): Player.EffectList.append(DoomSpikeCombo)

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
    Player.buffList.append(LanceChargeBuff)
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

def DoomSpikeCombo(Player, Spell):
    if Spell.id == SonicThrust.id:
        Spell.Potency += 20
            #Gain PowerSurge, 10% damage

        if Player.PowerSurgeTimer <= 0: #Not already applied
            #print("Buffing")
            Player.buffList.append(PowerSurgeBuff)
            #input(Player.MultDPSBonus)
            Player.EffectCDList.append(PowerSurgeCheck)
        Player.PowerSurgeTimer = 30
        #input(Player.PowerSurgeTimer)
        Player.EffectList.append(SonicThrustCombo)
        Player.EffectToRemove.append(DoomSpikeCombo)

def SonicThrustCombo(Player, Spell):
    if Spell.id == CoerthanTorment.id:
        Spell.Potency += 50
        Player.DraconianFire = True
        Player.EffectToRemove.append(SonicThrustCombo)



def TrueThrustCombo(Player, Spell):
    if Spell.id == Disembowel.id:
        Spell.Potency += 110

        #Gain PowerSurge, 10% damage

        if Player.PowerSurgeTimer <= 0: #Not already applied
            #print("Buffing")
            Player.buffList.append(PowerSurgeBuff)
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
        Player.buffList.remove(LanceChargeBuff)
        Player.EffectToRemove.append(LanceChargeCheck)

def PowerSurgeCheck(Player, Enemy):
    #input("in check : " + str(Player.PowerSurgeTimer))
    if Player.PowerSurgeTimer <= 0:
        #input("Removing powersurge")
        Player.EffectToRemove.append(PowerSurgeCheck)
        Player.buffList.remove(PowerSurgeBuff)

#GCD
#Combo Action
TrueThrust = DragoonSpell(1, True, 2.5, 230, ApplyTrueThrust, [TrueThrustRequirement], True)
Disembowel = DragoonSpell(2, True, 2.5, 140, empty, [], True)
VorpalThrust = DragoonSpell(3, True, 2.5, 130, empty, [], True)
ChaoticSpring = DragoonSpell(4, True, 2.5, 140, empty, [], True)
ChaoticSpringDOT = DOTSpell(-22, 45, True)
HeavenThrust = DragoonSpell(5, True, 2.5, 100, empty, [], True)

WheelingThrust = DragoonSpell(6, True, 2.5, 300, ApplyWheelingThrust, [WheelingThrustRequirement], True )
FangAndClaw = DragoonSpell(7, True, 2.5, 300, ApplyFangAndClaw, [FangAndClawRequirement], True)
RaidenThrust = DragoonSpell(8, True, 2.5, 280, ApplyRaidenThrust, [RaidenThrustRequirement], True)
PiercingTalon = DragoonSpell(9, True, 2.5, 150, empty, [], True)

#AOE combo Action
DoomSpike = DragoonSpell(10, True, 2.5, 110, ApplyDoomSpike, [], True)
SonicThrust = DragoonSpell(11, True, 2.5, 100, empty, [], True)
CoerthanTorment = DragoonSpell(12, True, 2.5, 100, empty, [], True)
DraconianFury = DragoonSpell(13, True, 2.5, 130, ApplyRaidenThrust, [RaidenThrustRequirement], True) #AOE version of Raiden Thrust

#oGCD
LanceCharge = DragoonSpell(14, False, 0, 0, ApplyLanceCharge, [LanceChargeRequirement], False)
BattleLitany = DragoonSpell(15, False, 0, 0, ApplyBattleLitany, [BattleLitanyRequirement], False)
Geirskogul = DragoonSpell(16, False, 0, 260, ApplyGeirskogul, [GeirskogulRequirement], False)
Nastrond = DragoonSpell(17, False, 0, 300, ApplyNastrond, [NastrondRequirement], False)
HighJump = DragoonSpell(18, False, 0, 400, ApplyHighJump, [HighJumpRequirement], False)
MirageDive = DragoonSpell(19, False, 0, 200, ApplyMirageDive, [MirageDiveRequirement], False)
SpineshafterDive = DragoonSpell(20, False, 0, 250, ApplySpineshafter, [SpineshafterRequirement], False)
LifeSurge = DragoonSpell(21, False, 0, 0, ApplyLifeSurge, [LifeSurgeRequirement], False)
Stardiver = DragoonSpell(22, False, 0, 620, ApplyStardiver, [StardiverRequirement], False)
WyrmwindThrust = DragoonSpell(23, False, 0, 420, ApplyWyrmwindThrust, [WyrmwindThrustRequirement], False)
DragonFireDive = DragoonSpell(24, False, 0, 300, ApplyDragonFireDive, [DragonFireDiveRequirement], False)

#funny oGCD
ElusiveJump = DragoonSpell(25, False, 0, 0, empty, [], 0) #No requirement, I will let a Dragoon spam this shit


#buff
RightEyeBuff = buff(1.1)
LeftEyeBuff = buff(1.05)
LanceChargeBuff = buff(1.1)
PowerSurgeBuff = buff(1.1)

def DragonSight(Target):

    def DragonSightCheck(Player, Enemy):
        if Player.DragonSightTimer <= 0:
            Player.buffList.remove(RightEyeBuff)
            Target.buffList.remove(LeftEyeBuff)
            Player.EffectToRemove.append(DragonSightCheck)

    def ApplyDragonSight(Player, Enemy):
        Player.DragonSightCD = 120
        Player.DragonSightTimer = 20

        Player.buffList.append(RightEyeBuff)
        Target.buffList.append(LeftEyeBuff)
        Player.EffectCDList.append(DragonSightCheck)

    return DragoonSpell(26, False, 0, 0, ApplyDragonSight, [DragonSightRequirement], False)


DragoonAbility = {
75 : TrueThrust,
78 : VorpalThrust,
25771 : HeavenThrust,
87 : Disembowel,
25772 : ChaoticSpring,
16479 : RaidenThrust,
3554 : FangAndClaw,
3556 : WheelingThrust,
86 : DoomSpike,
7397 : SonicThrust,
16477 : CoerthanTorment,
25770 : DraconianFury,
90 : PiercingTalon,
16478 : HighJump,
7399 : MirageDive,
95 : SpineshafterDive,
96 : DragonFireDive,
3557 : BattleLitany,
7398 : DragonSight,
83 : LifeSurge,
85 : LanceCharge,
94 : ElusiveJump,
3555 : Geirskogul,
7400 : Nastrond,
16480 : Stardiver,
25773 : WyrmwindThrust
}