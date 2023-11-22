from ffxivcalc.Jobs.Base_Spell import DOTSpell, buff, empty, buffHistory, buffPercentHistory
from ffxivcalc.Jobs.Melee.Melee_Spell import DragoonSpell
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
    else: 
        Player.LanceMastery = False


def ApplyFangAndClaw(Player, Enemy):
    Player.FangAndClaw = False

    if not Player.LanceMastery: 
        Player.WheelInMotion = True
        Player.LanceMastery = True
        Player.EffectList.append(LanceMasteryCombo)
    else:
        Player.LanceMastery = False
def ApplyLanceCharge(Player, Enemy):
    Player.LanceChargeCD = 60
    Player.LanceChargeTimer = 20
    Player.EffectCDList.append(LanceChargeCheck)
    Player.buffList.append(LanceChargeBuff)

                                     # Only doing this if SavePreBakedAction is true
    #if Player.CurrentFight.SavePreBakedAction:
    #    fight = Player.CurrentFight
    #    history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20 , LanceChargeBuff.MultDPS)
    #    Player.PercentBuffHistory.append(history)

def ApplyBattleLitany(Player, Enemy):
    Player.BattleLitanyCD = 120
    Player.BattleLitanyTimer = 15

    #Will give each person in the fight the buff
    for player in Player.CurrentFight.PlayerList:  
        player.CritRateBonus += 0.1
    Player.EffectCDList.append(BattleLitanyCheck)

                                     # Only doing this if SavePreBakedAction is true
    #if Player.CurrentFight.SavePreBakedAction:
    #    fight = Player.CurrentFight
    #    history = buffHistory(fight.TimeStamp, fight.TimeStamp + 15)
    #    fight.PlayerList[fight.PlayerIDSavePreBakedAction].BattleLitanyHistory.append(history)

def ApplyGeirskogul(Player, Enemy):
    Player.GeirskogulCD = 30

    if Player.DragonGauge == 2 : 
        Player.LifeOfTheDragon = True
        Player.LifeOfTheDragonTimer = 30
        Player.EffectCDList.append(LifeOfTheDragonCheck)
        Player.DragonGauge = 0

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
        Player.LifeSurgeCD = 40
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
            Player.buffList.append(PowerSurgeBuff)
            Player.EffectCDList.append(PowerSurgeCheck)
        Player.PowerSurgeTimer = 30
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
            Player.buffList.append(PowerSurgeBuff)
            Player.EffectCDList.append(PowerSurgeCheck)
        Player.PowerSurgeTimer = 30

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
            Player.EffectCDList.append(ChaoticSpringDOTCheck)
        else : Player.ChaoticSpringDOT.resetBuffSnapshot() # If already applied reset snapshot
        Player.ChaoticSpringDOTTimer = 24

        Player.WheelInMotion = True 
        Player.EffectToRemove.append(DisembowelCombo)

def LanceMasteryCombo(Player, Spell):
    if Spell.id == FangAndClaw.id or Spell.id == WheelingThrust.id:
        Spell.Potency += 100
        Player.EffectToRemove.append(LanceMasteryCombo)
        Player.DraconianFire = True
    elif isinstance(Spell, DragoonSpell) and Spell.Weaponskill:
        Player.FangAndClaw = False
        Player.WheelInMotion = False
        Player.LanceMastery = False
        Player.EffectToRemove.append(LanceMasteryCombo)



#Check

def ChaoticSpringDOTCheck(Player, Enemy):
    if Player.ChaoticSpringDOTTimer <= 0:
        Player.DOTList.remove(Player.ChaoticSpringDOT)
        Player.ChaoticSpringDOT = None
        Player.EffectToRemove.append(ChaoticSpringDOTCheck)


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
TrueThrust = DragoonSpell(75, True, 2.5, 230, ApplyTrueThrust, [TrueThrustRequirement], True, type = 2)
Disembowel = DragoonSpell(87, True, 2.5, 140, empty, [], True, type = 2)
VorpalThrust = DragoonSpell(78, True, 2.5, 130, empty, [], True, type = 2)
ChaoticSpring = DragoonSpell(25772, True, 2.5, 140, empty, [], True, type = 2)
ChaoticSpringDOT = DOTSpell(-22, 45, True)
HeavenThrust = DragoonSpell(25771, True, 2.5, 100, empty, [], True, type = 2)

WheelingThrust = DragoonSpell(3556, True, 2.5, 300, ApplyWheelingThrust, [WheelingThrustRequirement], True , type = 2)
FangAndClaw = DragoonSpell(3554, True, 2.5, 300, ApplyFangAndClaw, [FangAndClawRequirement], True, type = 2)
RaidenThrust = DragoonSpell(16479, True, 2.5, 280, ApplyRaidenThrust, [RaidenThrustRequirement], True, type = 2)
PiercingTalon = DragoonSpell(90, True, 2.5, 150, empty, [], True, type = 2)

#AOE combo Action
DoomSpike = DragoonSpell(86, True, 2.5, 110, ApplyDoomSpike, [], True, type = 2)
SonicThrust = DragoonSpell(7397, True, 2.5, 100, empty, [], True, type = 2)
CoerthanTorment = DragoonSpell(16477, True, 2.5, 100, empty, [], True, type = 2)
DraconianFury = DragoonSpell(25770, True, 2.5, 130, ApplyRaidenThrust, [RaidenThrustRequirement], True, type = 2) #AOE version of Raiden Thrust

#oGCD
LanceCharge = DragoonSpell(85, False, 0, 0, ApplyLanceCharge, [LanceChargeRequirement], False)
BattleLitany = DragoonSpell(3557, False, 0, 0, ApplyBattleLitany, [BattleLitanyRequirement], False)
Geirskogul = DragoonSpell(3555, False, 0, 260, ApplyGeirskogul, [GeirskogulRequirement], False)
Nastrond = DragoonSpell(7400, False, 0, 300, ApplyNastrond, [NastrondRequirement], False)
HighJump = DragoonSpell(16478, False, 0, 400, ApplyHighJump, [HighJumpRequirement], False)
MirageDive = DragoonSpell(7399, False, 0, 200, ApplyMirageDive, [MirageDiveRequirement], False)
SpineshafterDive = DragoonSpell(95, False, 0, 250, ApplySpineshafter, [SpineshafterRequirement], False)
LifeSurge = DragoonSpell(83, False, 0, 0, ApplyLifeSurge, [LifeSurgeRequirement], False)
Stardiver = DragoonSpell(16480, False, 0, 620, ApplyStardiver, [StardiverRequirement], False)
WyrmwindThrust = DragoonSpell(25773, False, 0, 420, ApplyWyrmwindThrust, [WyrmwindThrustRequirement], False)
DragonFireDive = DragoonSpell(96, False, 0, 300, ApplyDragonFireDive, [DragonFireDiveRequirement], False)

#funny oGCD
ElusiveJump = DragoonSpell(94, False, 0, 0, empty, [], 0) #No requirement, I will let a Dragoon spam this shit


#buff
RightEyeBuff = buff(1.1,name="RE")
LeftEyeBuff = buff(1.05,name="LE")
LanceChargeBuff = buff(1.1,name="Lance Charge")
PowerSurgeBuff = buff(1.1,name="Power Surge")

def DragonSight(Target):

    def DragonSightCheck(Player, Enemy):
        if Player.DragonSightTimer <= 0:
            Player.buffList.remove(RightEyeBuff)
            Target.buffList.remove(LeftEyeBuff)
            Player.EffectToRemove.append(DragonSightCheck)

    def ApplyDragonSight(Player, Enemy):
                             # Refreshing target playerID
        DragonSightSpell.TargetID = Target.playerID

        Player.DragonSightCD = 120
        Player.DragonSightTimer = 20

        Player.buffList.append(RightEyeBuff)
        Target.buffList.append(LeftEyeBuff)
        Player.EffectCDList.append(DragonSightCheck)

                                         # Only doing this if SavePreBakedAction is true
        #if Player.CurrentFight.SavePreBakedAction:
        #    fight = Player.CurrentFight
        #    history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20 , LeftEyeBuff.MultDPS)
        #    drgHistory = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20, RightEyeBuff.MultDPS) # Adding to DRG instead of chcking
        #    Target.PercentBuffHistory.append(history)
        #    Player.PercentBuffHistory.append(drgHistory)

    DragonSightSpell = DragoonSpell(7398, False, 0, 0, ApplyDragonSight, [DragonSightRequirement], False)
    DragonSightSpell.TargetID = Target.playerID
    DragonSightSpell.TargetPlayerObject = Target
    return DragonSightSpell


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