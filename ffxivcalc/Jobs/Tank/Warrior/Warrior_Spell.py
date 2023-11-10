#########################################
########## WARRIOR Spell  ###############
#########################################

from ffxivcalc.Jobs.Base_Spell import buff, empty
from ffxivcalc.Jobs.Tank.Tank_Spell import BigMitRequirement, ApplyBigMit, WarriorSpell
from ffxivcalc.Jobs.Player import Shield, MitBuff
Lock = 0.75

def BeastGaugeRequirement(Player, Spell):
    RemoveBeast(Player, Spell.Cost)
    return Player.BeastGauge >= 0, -1

#Special

def AddBeast(Player, Gauge):
    Player.BeastGauge = min(100, Player.BeastGauge + Gauge)

def RemoveBeast(Player, Gauge):
    Player.BeastGauge -= Gauge #Caanot go under 0 cuz verify if enough gauge

#Requirement

def UpheavalRequirement(Player, Spell):
    return Player.UpheavalCD <= 0, Player.UpheavalCD

def OnslaughtRequirement(Player, Spell):
    return Player.OnslaughtStack >= 1, Player.OnslaughtCD

def InfuriateRequirement(Player, Spell):
    return Player.InfuriateStack >= 1, Player.InfuriateCD

def InnerReleaseRequirement(Player, Spell):
    return Player.InnerReleaseCD <= 0, Player.InnerReleaseCD

def PrimalRendRequirement(Player, Spell):
    return Player.PrimalRendTimer > 0, -1

def FellCleaveRequirement(Player, Spell):
    return Player.BeastGauge >= 50, -1

def InnerChaosRequirement(Player, Spell):
    return Player.NascentChaosTimer > 0, -1

def ThrillOfBattleRequirement(Player, Spell):
    return Player.ThrillOfBattleCD <= 0, Player.ThrillOfBattleCD

def HolmgangRequirement(Player, Spell):
    return Player.HolmgangCD <= 0, Player.HolmgangCD

def ShakeItOffRequirement(Player, Spell):
    return Player.ShakeItOffCD <= 0, Player.ShakeItOffCD

def NascentFlashRequirement(Player, Spell):
    return Player.NascentFlashCD <= 0, Player.NascentFlashCD

def BloodwhettingRequirement(Player, Spell):
    return Player.BloodwhettingCD <= 0, Player.BloodwhettingCD

def EquilibriumRequirement(Player, Spell):
    return Player.EquilibriumCD <= 0, Player.EquilibriumCD

#Apply

def ApplyEquilibrium(Player, Enemy):
    Player.EquilibriumCD = 60

    # 1200 potency healing

def ApplyBloodwhetting(Player, Enemy):
    Player.BloodwhettingCD = 25
    BloodwhettingBuff = MitBuff(0.9, 8, Player)
    StemFlowBuff = MitBuff(0.9, 4, Player)
    Player.MitBuffList.append(BloodwhettingBuff)
    Player.MitBuffList.append(StemFlowBuff)

    Player.BloodwhettingBuff = BloodwhettingBuff


def ApplyNascentFlash(Player, Enemy):
    Player.NascentFlashCD = 25

def ApplyShakeItOff(Player, Enemy):
    Player.ShakeItOffCD = 90

    # Gives a shield equal to 15% of max HP + 2% per Thrill, Vengeance and bloodwhetting
    shield_percent = 0.15

    if Player.VengeanceBuff != None: 
        Player.VengeanceBuff.Timer = 0
        Player.VengeanceBuff = None
        shield_percent += 0.02
    if Player.BloodwhettingBuff != None:
        Player.BloodwhettingBuff.Timer = 0
        Player.BloodwhettingBuff = None
        shield_percent += 0.02
    if Player.ThrillOfBattleTimer > 0:
        Player.ThrillOfBattleTimer = 0
        shield_percent += 0.02
    
    # Removing mit if the timer is bigger than 0 and giving an extra 2%

    shield_value = (Player.MaxHP * shield_percent)

    for player in Player.CurrentFight.PlayerList:
        player.ShieldList.append(Shield(shield_value, 15, player))

    # Also does 300 potency healing


def ApplyHolmgang(Player, Enemy):
    Player.HolmgangCD = 240

    Player.InvulnTimer = 10

def ApplyThrillOfBattle(Player, Enemy):
    Player.ThrillOfBattleCD = 90

    # Increases max HP by 20%
    HPReceive = Player.MaxHP * 0.2
    Player.MaxHP *= 1.2
    Player.ApplyHeal(HPReceive)
    Player.ThrillOfBattleTimer = 10

    Player.EffectCDList.append(ThrillOfBattleCheck)

def ApplyOverpower(Player, Enemy):
    if not (OverpowerCombo in Player.EffectList) : Player.EffectList.append(OverpowerCombo)

def ApplyHeavySwing(Player, Enemy):
    if not (HeavySwingEffect in Player.EffectList) : Player.EffectList.append(HeavySwingEffect)

def ApplyMaim(Player, Enemy):
    pass

def ApplyStormEye(Player, Enemy):
    pass

def ApplyStormPath(Player, Enemy):
    pass

def ApplyUpheaval(Player, Enemy):
    Player.UpheavalCD = 30

def ApplyOnslaught(Player, Enemy):
    if Player.OnslaughtStack == 3:
        #Then we have to add check
        Player.EffectCDList.append(OnslaughtStackCheck)
        Player.OnslaughtCD = 30
    Player.OnslaughtStack -= 1

def ApplyInfuriate(Player, Enemy):
    AddBeast(Player, 50)
    if Player.InfuriateStack == 2:
        Player.EffectCDList.append(InfuriateStackCheck)

    Player.InfuriateStack -= 1
    Player.NascentChaosTimer = 30

def ApplyInnerRelease(Player, Enemy):
    Player.EffectList.append(InnerReleaseEffect)
    Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 10)
    Player.PrimalRendTimer = 30 #Primal rend ready
    Player.InnerReleaseStack = 3
    Player.NoBeastCostStack = 3
    Player.InnerReleaseCD = 60

def ApplyPrimalRend(Player, Enemy):
    Player.PrimalRendTimer = 0

def ApplyInnerChaos(Player, Enemy):
    Player.InfuriateCD = max(0, Player.InfuriateCD - 5)
    Player.NascentChaosTimer = 0

#Effect

def InnerReleaseEffect(Player, Spell):
    if Spell.id == FellCleave.id:
        Player.NoBeastCostStack -= 1
        Spell.Cost = 0
        if Player.NoBeastCostStack == 0: 
            Player.EffectToRemove.append(InnerReleaseEffect)

def SurgingTempestEffect(Player, Spell):
    if Player.SurgingTempestTimer > 0 : 
        Player.buffList.append(SurgingTempestBuff)
        Player.EffectCDList.append(SurgingTempestCheck)
        Player.EffectToRemove.append(SurgingTempestEffect)

#Combo Action

def OverpowerCombo(Player, Spell):
    if Spell.id == MythrilTempest.id:
        Spell.Potency += 50
        Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 30)
        Player.EffectToRemove.append(OverpowerCombo)

def HeavySwingEffect(Player, Spell):
    if Spell.id == Maim.id:
        Spell.Potency += 150
        Player.EffectToRemove.append(HeavySwingEffect)
        if not (MaimEffect in Player.EffectList) : Player.EffectList.append(MaimEffect)
        AddBeast(Player, 10)


def MaimEffect(Player, Spell):
    if Spell.id == StormEye.id:
        Spell.Potency += 280
        if Player.SurgingTempestTimer <= 0:
            Player.EffectCDList.append(SurgingTempestCheck)
            Player.buffList.append(SurgingTempestBuff)
        Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 30)
        AddBeast(Player, 10)
        Player.EffectToRemove.append(MaimEffect)
    elif Spell.id == StormPath.id:
        Spell.Potency += 280
        AddBeast(Player, 20)
        Player.EffectToRemove.append(MaimEffect)

#Check


def ThrillOfBattleCheck(Player, Enemy):
    if Player.ThrillOfBattleTimer <= 0:
        Player.EffectToRemove.append(ThrillOfBattleCheck)

        Player.MaxHP /= 1.2 # Reducing maxHP
        Player.HP = min(Player.HP, Player.MaxHP)

def SurgingTempestCheck(Player, Enemy):
    if Player.SurgingTempestTimer <= 0: 
        Player.buffList.remove(SurgingTempestBuff)
        Player.EffectList.append(SurgingTempestEffect)
        Player.EffectToRemove.append(SurgingTempestCheck)

def OnslaughtStackCheck(Player, Enemy):
    if Player.OnslaughtCD <= 0:
        if Player.OnslaughtStack == 2:
            Player.EffectToRemove.append(OnslaughtStackCheck)
        else:
            Player.OnslaughtCD = 30
        Player.OnslaughtStack += 1

def InfuriateStackCheck(Player, Enemy):
    if Player.InfuriateCD <= 0:
        if Player.InfuriateStack == 1:
            Player.EffectToRemove.append(InfuriateStackCheck)
        else:
            Player.InfuriateCD = 30
        Player.InfuriateStack += 1
    

#Combo Action
HeavySwing = WarriorSpell(31, True, Lock, 2.5, 200, 0, ApplyHeavySwing, [],0, type = 2)
Maim = WarriorSpell(37, True, Lock, 2.5, 150, 0, ApplyMaim, [],0, type = 2)
StormEye = WarriorSpell(45, True, Lock, 2.5, 160, 0, ApplyStormEye, [],0, type = 2)
StormPath = WarriorSpell(42, True, Lock, 2.5, 160, 0, ApplyStormPath, [], 0, type = 2)
#Missing Storm's path

#oGCD
Upheaval = WarriorSpell(7387, False, Lock, 0, 400, 0, ApplyUpheaval, [UpheavalRequirement],0)
Onslaught = WarriorSpell(7386, False, Lock, 0, 150, 0, ApplyOnslaught, [OnslaughtRequirement],0)
Infuriate = WarriorSpell(52, False, Lock, 0, 0, 0, ApplyInfuriate, [InfuriateRequirement],0)
InnerRelease = WarriorSpell(7389, False, Lock, 0, 0, 0, ApplyInnerRelease, [InnerReleaseRequirement],0)


#GCD
PrimalRend = WarriorSpell(25753, True, Lock, 2.5, 700, 0, ApplyPrimalRend, [PrimalRendRequirement],0, type = 2)
FellCleave = WarriorSpell(3549, True, Lock, 2.5, 520, 0, empty, [],50, type = 2)
InnerChaos = WarriorSpell(16465, True, Lock, 2.5, 660,0, ApplyInnerChaos, [InnerChaosRequirement], 50, type = 2)
Tomahawk = WarriorSpell(46, True, Lock, 2.5, 150, 0, empty, [], 0, type = 2)

#AOE GCD
Overpower = WarriorSpell(41,True, 0, 2.5, 110, 0 , ApplyOverpower, [], 0 , type = 2)
MythrilTempest = WarriorSpell(16462, True, 0, 2.5, 100, 0, empty, [], 0, type = 2)
Decimate = WarriorSpell(3550, True, 0, 2.5, 200, 0, empty, [], 50, type = 2)
ChaoticCyclone = WarriorSpell(16463, True, Lock, 2.5, 320,0, ApplyInnerChaos, [InnerChaosRequirement], 50, type = 2) #AOE Version of Inner chaos
#AOE oGCD
Orogeny = WarriorSpell(25752, False, Lock, 0, 150, 0, ApplyUpheaval, [UpheavalRequirement],0) #AOE Version of Upheaval
#Mit
ThrillOfBattle = WarriorSpell(40, False, 0, 0, 0, 0, ApplyThrillOfBattle, [ThrillOfBattleRequirement], 0)
Holmgang = WarriorSpell(43, False, 0, 0, 0, 0, ApplyHolmgang, [HolmgangRequirement], 0)
ShakeItOff = WarriorSpell(7388, False, 0, 0, 0, 0, ApplyShakeItOff, [ShakeItOffRequirement], 0)
Bloodwhetting = WarriorSpell(25751, False, 0, 0, 0, 0, ApplyBloodwhetting, [BloodwhettingRequirement], 0)
Equilibrium = WarriorSpell(3552, False, 0, 0, 0, 0, ApplyEquilibrium, [EquilibriumRequirement], 0)
Vengeance = WarriorSpell(44, False, 0, 0, 0, 0, ApplyBigMit,[BigMitRequirement], 0)

def NascentFlash(Target):
    """This function returns a WARSpell object of Nascent Flash
    with target whatever target has been given

    Args:
        Target (Player) : Target of the action
    
    """

    def NascentGlintCheck(Player, Enemy):
        if Player.NascentFlashTimer <= 4:
            Player.MagicMitigation /= 0.9
            Player.PhysicalMitigation  /= 0.9
            Player.EffectToRemove.append(NascentGlintCheck)

    def NascentFlashCheck(Player, Enemy):
        if Player.NascentFlashTimer <= 0:
            Player.MagicMitigation /= 0.9
            Player.PhysicalMitigation  /= 0.9
            Player.EffectToRemove.append(NascentFlashCheck)

    def ApplySpell(Player, Enemy):
        ApplyNascentFlash(Player, Enemy)
        # Gives 10% for 8 sec and an add. 10% for 4 sec
        Target.MagicMitigation *= 0.9 * 0.9
        Target.PhysicalMitigation *= 0.9 * 0.9

        Target.EffectCDList.append(NascentFlashCheck)
        Target.EffectCDList.append(NascentGlintCheck)

    NascentFlash = WarriorSpell(16464, False, 0, 0, 0, 0, ApplySpell, [NascentFlashRequirement], 0)
    NascentFlash.TargetID = Target.playerID
    return NascentFlash





#buff
SurgingTempestBuff = buff(1.1,name="Surging Tempest")

WarriorAbility = {
43 : Holmgang,
7386 : Onslaught,
52 : Infuriate,
7389 : InnerRelease,
31 : HeavySwing,
37 : Maim,
42 : StormPath,
45 : StormEye,
3549 : FellCleave,
16465 : InnerChaos,
25753 : PrimalRend,
7387 : Upheaval,
41 : Overpower,
16462 : MythrilTempest,
3550 : Decimate,
16463 : ChaoticCyclone,
25752 : Orogeny,
44 : Vengeance,
40 : ThrillOfBattle,
3552 : Equilibrium,
25751 : Bloodwhetting,
16464 : NascentFlash,
7388 : ShakeItOff,
46 : Tomahawk
}