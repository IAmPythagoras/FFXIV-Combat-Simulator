from ffxivcalc.Jobs.Base_Spell import buff, empty, DOTSpell, ManaRequirement
from ffxivcalc.Jobs.Tank.Tank_Spell import BigMitRequirement, ApplyBigMit, PaladinSpell
from ffxivcalc.helperCode.exceptions import InvalidTarget
from ffxivcalc.Jobs.Player import Shield, MitBuff
import copy
Lock = 0


#Requirement

def GoringBladeRequirement(Player, Spell):
    return Player.GoringBladeCD <= 0, Player.GoringBladeCD

def BulwarkRequirement(Player, Spell):
    return Player.BulwarkCD <= 0, Player.BulwarkCD

def FightOrFlightRequirement(Player, Spell):
    return Player.FightOrFlightCD <= 0, Player.FightOrFlightCD

def ExpiacionRequirement(Player, Spell):
    return Player.ExpiacionCD <= 0, Player.ExpiacionCD

def InterveneRequirement(Player, Spell):
    return Player.InterveneStack > 0, Player.InterveneCD

def AtonementRequirement(Player, Spell):
    return Player.SwordOathStack > 0, -1

def CircleScornRequirement(Player, Spell):
    return Player.CircleScornCD <= 0, Player.CircleScornCD

def BladeFaithRequirement(Player, Spell):
    return Player.BladeFaith, -1

def BladeTruthRequirement(Player, Spell):
    return Player.BladeTruth, -1

def BladeValorRequirement(Player, Spell):
    return Player.BladeValor, -1

def ConfettiRequirement(Player, Spell):
    return Player.RequestACat, -1

def RequestACatRequirement(Player, Spell):
    return Player.RequestACatCD <= 0, Player.RequestACatCD

def DivineVeilRequirement(Player, Spell):
    return Player.DivineVeilCD <= 0, Player.DivineVeilCD

def SheltronRequirement(Player, Spell):
    return Player.OathGauge >= 50, -1

def HolySheltronRequirement(Player, Spell):
    return Player.HolySheltronCD <= 0, Player.HolySheltronCD

def CoverRequirement(Player, Spell):
    return Player.CoverCD <= 0, Player.CoverCD

def InterventionRequirement(Player, Spell):
    return Player.InterventionCD <= 0, Player.InterventionCD

def HallowedGroundRequirement(Player, Spell):
    return Player.HallowedGroundCD <= 0, Player.HallowedGroundCD

#Apply

def ApplyHallowedGround(Player, Enemy):
    Player.HallowedGroundCD = 420

    Player.InvulnTimer = 10

def ApplyBulwark(Player, Enemy):
    Player.BulwarkCD = 90
    BulwarkMit = MitBuff(20, 10, Player)

    Player.MitBuffList.append(BulwarkMit)

def ApplyHolySheltron(Player, Enemy):
    Player.HolySheltronCD = 5
    Player.OathGauge -= 50

    
    # Gives 20% from block for 8 sec and
    # 15% mit for 4 seconds
    KnightResolveMit = MitBuff(0.85, 4, Player)
    HolySheltronMit = MitBuff(0.8, 8, Player)

    Player.MitBuffList.append(KnightResolveMit)
    Player.MitBuffList.append(HolySheltronMit)

def ApplyCover(Player, Enemy):
    Player.CoverCD = 120
    Player.OathGauge -= 50

def ApplyIntervention(Player, Enemy):
    Player.InterventionCD = 5
    Player.OathGauge -= 50

    

    

def ApplyDivineVeil(Player, Enemy):
    # For now will be assumed the buff is given as soon as its 
    # casted
    Player.DivineVeilCD = 90

    # Gives a shield to every player except the PLD
    # equal to 10% and cures every player by 400 potency

    shield_value = int(Player.MaxHP * 0.1)

    for player in Player.CurrentFight.PlayerList:
        # Giving every player that is not the PLD the divine veil shield
        if player != Player : player.ShieldList.append(Shield(shield_value, 30, player))
        

    



def ApplyTotalEclipse(Player, Enemy):
    if not (TotalEclipseCombo in Player.EffectList) : Player.EffectList.append(TotalEclipseCombo)

def ApplyFightOrFlight(Player, Enemy):
    Player.FightOrFlightTimer = 20
    Player.FightOrFlightCD = 60
    Player.buffList.append(FightOrFlightBuff)
    Player.EffectCDList.append(FightOrFlightCheck)

def ApplyExpiacion(Player, Enemy):
    Player.Mana += 10000 #Will have to double check that lol >.>
    Player.ExpacionCD = 30

def ApplyIntervene(Player, Enemy):
    if Player.InterveneStack == 2:
        Player.EffectCDList.append(InterveneStackCheck)
        Player.InterveneCD = 30
    Player.InterveneStack -= 1

def ApplyAtonement(Player, Enemy):
    Player.SwordOathStack -= 1

def ApplyCircleScorn(Player, Enemy):
    #Since DOT has 30 sec CD and 15 sec duration, we don't have to check if already applied
    Player.CircleScornCD = 30
    Player.CircleScornDOT = copy.deepcopy(CircleScornDOT)
    Player.DOTList.append(Player.CircleScornDOT)
    Player.CircleScornTimer = 15
    Player.EffectCDList.append(CircleScornDOTCheck)

def ApplyRequestACat(Player, Enemy):
    Player.RequestACatCD = 60
    Player.RequestACat = True
    Player.RequestACatStack = 4
    Player.EffectList.append(RequestACatEffect)
    Player.EffectCDList.append(RequestACatCheck)

def ApplyBladeFaith(Player, Enemy):
    Player.BladeFaith = False
    Player.BladeTruth = True

def ApplyBladeTruth(Player, Enemy):
    Player.BladeTruth = False
    Player.BladeValor = True

def ApplyBladeValor(Player, Enemy):
    Player.BladeValor = False


def ApplyConfetti(Player, Enemy):
    Player.BladeFaith = True


def ApplyFastBlade(Player, Enemy):
    if not (FastBladeCombo in Player.EffectList) : 
        Player.EffectList.append(FastBladeCombo)

def ApplyGoringBlade(Player, Enemy):
    Player.GoringBladeCD = 60 * Player.WeaponskillReduction # Cuz is weaponskill

def DivineMightEffect(Player, Spell):
    """Allows next holy spirit or holy circle to be cast immediately with increased potency.
    """
    if Spell.id == HolySpirit.id:
        Spell.Potency += 100
        Spell.CastTime = 0
        Player.EffectToRemove.append(DivineMightEffect)
    elif Spell.id == HolyCircle.id:
        Spell.Potency += 100
        Spell.CastTime = 0
        Player.EffectToRemove.append(DivineMightEffect)

def RequestACatEffect(Player, Spell):

    match Spell.id:
        case HolySpirit.id:
                             # Divine might has prio over this.
            if not DivineMightEffect in Player.EffectList:
                Spell.Potency += 300
                Spell.CastTime = 0
                Player.RequestACatStack -= 1
        case HolyCircle.id:
                             # Divine might has prio over this.
            if not DivineMightEffect in Player.EffectList:
                Spell.Potency += 170
                Spell.CastTime = 0
                Player.RequestACatStack -= 1
        case Clemency.id:
            Spell.CastTime = 0
            Player.RequestACatStack -= 1
    #Confiteor combo
        case Confetti.id | BladeFaith.id | BladeTruth.id | BladeValor.id:
            Spell.Potency += 500
            Player.RequestACatStack -= 1

    



#Combo Action

def TotalEclipseCombo(Player, Spell):
    if Spell.id == Prominence.id:
        Spell.Potency += 70
        Player.EffectToRemove.append(TotalEclipseCombo)
        # also gives Divine might
        Player.EffectList.append(DivineMightEffect)


def FastBladeCombo(Player, Spell):
    if Spell.id == RiotBlade.id:
        Spell.Potency += 160
        Player.EffectToRemove.append(FastBladeCombo)
        if not (RiotBladeCombo in Player.EffectList) : Player.EffectList.append(RiotBladeCombo)

def RiotBladeCombo(Player, Spell):
    if Spell.id == RoyalAuthority.id:
        Spell.Potency += 260
        Player.SwordOathStack += 3
        Player.EffectToRemove.append(RiotBladeCombo)
        # also gives Divine might
        Player.EffectList.append(DivineMightEffect)

    """
    Old goring blade
    elif Spell.id == GoringBlade.id:
        #Apply dot

        Player.GoringDOT = copy.deepcopy(GoringDOT)
        Player.EffectCDList.append(GoringDOTCheck)
        Player.DOTList.append(Player.GoringDOT)
        Player.ValorDOTTimer = 0 #Remove other dot if it exists
        Player.GoringDOTTimer = 21
        Spell.Potency += 150
        Player.EffectToRemove.append(RiotBladeCombo)
    """


#Check

def DivineVeilCheck(Player, Enemy):
    if Player.DivineVeilTimer <= 0:
        Player.EffectToRemove.append(DivineVeilCheck)

def RequestACatCheck(Player, Enemy):
    if Player.RequestACatStack == 0:
        Player.RequestACat = False
        Player.EffectList.remove(RequestACatEffect)
        Player.EffectToRemove.append(RequestACatCheck)
        Player.BladeFaith = True


def FightOrFlightCheck(Player, Enemy):
    if Player.FightOrFlightTimer <= 0:
        Player.buffList.remove(FightOrFlightBuff)
        Player.EffectToRemove.append(FightOrFlightCheck)

def InterveneStackCheck(Player, Enemy):
    if Player.InterveneCD <= 0:
        if Player.InterveneStack == 1:
            Player.EffectToRemove.append(InterveneStackCheck)
        else:
            Player.InterveneCD = 30
        Player.InterveneStack += 1

def CircleScornDOTCheck(Player, Enemy):
    if Player.CircleScornTimer <= 0:
        Player.DOTList.remove(Player.CircleScornDOT)
        Player.CircleScornDOT = None
        Player.EffectToRemove.append(CircleScornDOTCheck)
"""
Post 6.3
def GoringDOTCheck(Player, Enemy):
    if Player.GoringDOTTimer <= 0:
        Player.DOTList.remove(Player.GoringDOT)
        Player.EffectToRemove.append(GoringDOTCheck)
        Player.GoringDOT = None

def ValorDOTCheck(Player, Enemy):
    if Player.ValorDOTTimer <= 0:
        Player.DOTList.remove(Player.ValorDOT)
        Player.EffectToRemove.append(ValorDOTCheck)
        Player.ValorDOT = None
"""

#Combo action

FastBlade = PaladinSpell(9, True, Lock, 2.5, 200, 0, ApplyFastBlade, [], True, type = 2)
RiotBlade = PaladinSpell(15, True, Lock, 2.5, 140, 0, empty, [], True, type = 2)
RoyalAuthority = PaladinSpell(3539, True, Lock, 2.5, 140,0, empty, [], True, type = 2)
GoringBlade = PaladinSpell(3538, True, Lock, 2.5, 700, 0, ApplyGoringBlade, [GoringBladeRequirement], True, type = 2)
"""
Post 6.3 goring blade
GoringBlade = PaladinSpell(3538, True, Lock, 2.5, 100, 0, empty, [], True, type = 2)
GoringDOT = DOTSpell(-5, 65, True)
"""
#Confiteor Combo Action

Confetti = PaladinSpell(16459, True, Lock, 2.5, 420, 1000, ApplyConfetti, [ManaRequirement, ConfettiRequirement], False, type = 1) # >.>
BladeFaith = PaladinSpell(25748, True, Lock, 2.5, 220, 0, ApplyBladeFaith, [BladeFaithRequirement], False, type = 1)
BladeTruth = PaladinSpell(25749, True, Lock, 2.5, 320, 0, ApplyBladeTruth, [BladeTruthRequirement], False, type = 1)
BladeValor = PaladinSpell(25750, True, Lock, 2.5, 420, 0, ApplyBladeValor, [BladeValorRequirement], False, type = 1)
"""
Post 6.3
BladeValorDOT = DOTSpell(-11, 80, True)
"""
#GCD
HolySpirit = PaladinSpell(7384, True, 1.5, 2.5, 350, 1000, empty, [ManaRequirement], False, type = 1)
Atonement = PaladinSpell(16460, True, Lock, 2.5, 400, 0, ApplyAtonement, [AtonementRequirement], True, type = 1)
Clemency = PaladinSpell(3541, True, 1.5, 2.5, 0, 1000, empty, [ManaRequirement], False, type = 2)
ShieldLob = PaladinSpell(24, True, 0, 2.5, 100, 0, empty, [], True , type = 2)
#AOE GCD
HolyCircle = PaladinSpell(16458, True, 1.5, 2.5,100, 1000, empty, [ManaRequirement], False, type = 1)
TotalEclipse = PaladinSpell(7381, True, 0, 2.5, 100, 0, ApplyTotalEclipse, [], True, type = 2)
Prominence = PaladinSpell(16457, True, 0, 2.5, 100, 0, empty, [], True, type = 2)

#oGCD
RequestACat = PaladinSpell(7383, False, 0, Lock, 320, 0, ApplyRequestACat, [RequestACatRequirement], True) #I NEED ONE RIGHT NOW :x
CircleScorn = PaladinSpell(23, False, 0, Lock, 140, 0, ApplyCircleScorn, [CircleScornRequirement], True)
CircleScornDOT = DOTSpell(-6, 30, True)
Intervene = PaladinSpell(16461, False, 0, Lock, 150, 0, ApplyIntervene, [InterveneRequirement], True)
Expiacion = PaladinSpell(25747, False, 0, Lock, 450, 0, ApplyExpiacion, [ExpiacionRequirement], True)
FightOrFlight = PaladinSpell(20, False, 0, Lock, 0, 0, ApplyFightOrFlight, [FightOrFlightRequirement], True)

#Mitigation Actions
DivineVeil = PaladinSpell(3540, False, 0, 0, 0, 0, ApplyDivineVeil, [DivineVeilRequirement], False)
HolySheltron = PaladinSpell(25746, False, 0, 0, 0, 0, ApplyHolySheltron, [HolySheltronRequirement,SheltronRequirement], False)
Cover = PaladinSpell(27, False, 0, 0, 0, 0, ApplyCover, [SheltronRequirement, CoverRequirement], False)
HallowedGround = PaladinSpell(30, False, 0, 0, 0, 0, ApplyHallowedGround, [HallowedGroundRequirement], False)
Bulwark = PaladinSpell(11111, False, 0, 0, 0, 0, ApplyBulwark, [BulwarkRequirement], False)
Sentinel = PaladinSpell(17,False, 0, 0, 0, 0, ApplyBigMit, [BigMitRequirement], False)

def Intervention(Target):
    """This function returns a PLDSpell object corresponding to
    intervention.

    Args:
        Target (Player) : Target of the action
    
    """

    def Apply(Player, Spell):
        ApplyIntervention(Player, Spell)

        # Check if the target is valid

        if Target == Player: # Intervention cannot be used on the player itself
            raise InvalidTarget("Intervention", Player, Target, False, Target.playerID)

        # 10% for 8 sec. 10% for 4 secs and 10% (flat bonus)
        # if rampart or sentinel is up

        mit = 0.9

        if Player.BigMitTimer > 0 or Player.RampartTimer > 0:
            mit = 0.8
            # Rampart and/or Sentinel are used
        
        InterventionBuff = MitBuff(mit, 8, Target)
        KnightBuff = MitBuff(0.9, 4, Target)

        Target.MitBuffList.append(InterventionBuff)
        Target.MitBuffList.append(KnightBuff)


    Intervention = PaladinSpell(7382, False, 0, 0, 0, 0, Apply, [SheltronRequirement, InterventionRequirement], False)
    Intervention.TargetID = Target.playerID
    return Intervention




def PassageOfArms(time):
    #Function since we will be using it for a set time


    def PassageOfArmsRequirement(Player, Spell):
        return Player.PassageOfArmsCD <= 0, Player.PassageOfArmsCD

    def ApplyPassageOfArms(Player, Enemy):
        Player.PassageOfArmsCD = 120

        # Will assume every player gets 15% mit for 6 sec

        for player in Player.CurrentFight.PlayerList:
            player.MitBuffList.append(MitBuff(0.85, 5, player))


    return PaladinSpell(7385, False, time, time, 0, 0, ApplyPassageOfArms, [PassageOfArmsRequirement], False)
#buff
FightOrFlightBuff = buff(1.25,name="Fight or Flight")

PaladinAbility = {
30 : HallowedGround,
24 : ShieldLob,
16461 : Intervene,
20 : FightOrFlight,
7383 : RequestACat,
9 : FastBlade,
15 : RiotBlade,
3538 : GoringBlade,
3539 : RoyalAuthority,
16460 : Atonement,
7384 : HolySpirit,
16459 : Confetti,
25748 : BladeFaith,
25749 : BladeTruth,
25750 : BladeValor,
25747 : Expiacion,
7381 : TotalEclipse,
16457 : Prominence,
23 : CircleScorn,
16458 : HolyCircle,
17 : Sentinel,
25746 : HolySheltron,
7382 : Intervention,
27 : Cover,
3541 : Clemency,
3540 : DivineVeil,
7385 : PassageOfArms(1)
}