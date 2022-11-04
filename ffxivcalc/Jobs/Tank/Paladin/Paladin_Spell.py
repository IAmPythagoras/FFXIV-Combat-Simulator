from ffxivcalc.Jobs.Base_Spell import buff, empty, DOTSpell, ManaRequirement
from ffxivcalc.Jobs.Tank.Tank_Spell import BigMit, PaladinSpell
import copy
Lock = 0


#Requirement

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


def ApplyHolySheltron(Player, Enemy):
    Player.HolySheltronCD = 5
    Player.OathGauge -= 50

def ApplyCover(Player, Enemy):
    Player.CoverCD = 120
    Player.OathGauge -= 50

def ApplyIntervention(Player, Enemy):
    Player.InterventionCD = 5
    Player.OathGauge -= 50

def ApplyDivineVeil(Player, Enemy):
    Player.DivineVeilCD = 90

def ApplyTotalEclipse(Player, Enemy):
    if not (TotalEclipseCombo in Player.EffectList) : Player.EffectList.append(TotalEclipseCombo)

def ApplyFightOrFlight(Player, Enemy):
    Player.FightOrFlightTimer = 25
    Player.FightOrFlightCD = 60
    Player.EffectList.append(FightOrFlightEffect)
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
    #Since DOT has 30 sec CD and 15 sec duration, we don't have to check
    Player.CircleScornDOT = copy.deepcopy(CircleScornDOT)
    Player.DOTList.append(Player.CircleScornDOT)
    Player.CircleScornTimer = 15
    Player.EffectCDList.append(CircleScornDOTCheck)

def ApplyRequestACat(Player, Enemy):
    Player.RequestACatCD = 60
    Player.RequestACat = True
    Player.RequestACatStack = 5
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
    Player.GoringDOTTimer = 0   #Remove GoringBladeDOT
    Player.ValorDOT = copy.deepcopy(BladeValorDOT)
    Player.DOTList.append(Player.ValorDOT)
    Player.ValorDOTTimer = 21
    Player.EffectCDList.append(ValorDOTCheck)


def ApplyConfetti(Player, Enemy):
    Player.RequestACatStack = 0
    Player.RequestACatStack = False
    Player.BladeFaith = True

#Combo Action

def ApplyFastBlade(Player, Enemy):
    if not (FastBladeCombo in Player.EffectList) : 
        Player.EffectList.append(FastBladeCombo)


#Effect

def TotalEclipseCombo(Player, Spell):
    if Spell.id == Prominence.id:
        Spell.Potency += 70
        Player.EffectToRemove.append(TotalEclipseCombo)

def FightOrFlightEffect(Player, Spell):
    if Spell.isPhysical or isinstance(Spell, DOTSpell):
        Spell.DPSBonus *= FightOrFlightBuff.MultDPS #Giving bonus to the spell if it is physical

def RequestACatEffect(Player, Spell):
    if Spell.id == HolySpirit.id:
        Spell.Potency += 300
        Spell.CastTime = 0
        Player.RequestACatStack -= 1
    elif Spell.id == HolyCircle.id:
        Spell.Potency += 170
        Spell.CastTime = 0
        Player.RequestACatStack -= 1
    elif Spell.id == Clemency.id:
        Spell.CastTime = 0
        Player.RequestACatStack -= 1



#Combo Action

def FastBladeCombo(Player, Spell):
    if Spell.id == RiotBlade.id:
        Spell.Potency += 130
        Player.EffectToRemove.append(FastBladeCombo)
        Player.EffectList.append(RiotBladeCombo)

def RiotBladeCombo(Player, Spell):
    if Spell.id == RoyalAuthority.id:
        Spell.Potency += 290
        Player.SwordOathStack += 3
        Player.EffectToRemove.append(RiotBladeCombo)
    elif Spell.id == GoringBlade.id:
        #Apply dot

        Player.GoringDOT = copy.deepcopy(GoringDOT)
        Player.EffectCDList.append(GoringDOTCheck)
        Player.DOTList.append(Player.GoringDOT)
        Player.ValorDOTTimer = 0 #Remove other dot if it exists
        Player.GoringDOTTimer = 21
        Spell.Potency += 150
        Player.EffectToRemove.append(RiotBladeCombo)


#Check

def RequestACatCheck(Player, Enemy):
    if Player.RequestACatStack == 0:
        Player.RequestACat = False
        Player.EffectList.remove(RequestACatEffect)
        Player.EffectToRemove.append(RequestACatCheck)
        Player.BladeFaith = True

def FightOrFlightCheck(Player, Enemy):
    if Player.FightOrFlighTimer <= 0:
        Player.EffectList.remove(FightOrFlightEffect)
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


#Combo action

FastBlade = PaladinSpell(9, True, Lock, 2.5, 200, 0, ApplyFastBlade, [], True)
RiotBlade = PaladinSpell(15, True, Lock, 2.5, 170, 0, empty, [], True)
RoyalAuthority = PaladinSpell(3539, True, Lock, 2.5, 130,0, empty, [], True)
GoringBlade = PaladinSpell(3538, True, Lock, 2.5, 100, 0, empty, [], True)
GoringDOT = DOTSpell(-5, 65, True)

#Confiteor Combo Action

Confetti = PaladinSpell(16459, True, Lock, 2.5, 1000, 1000, ApplyConfetti, [ManaRequirement, ConfettiRequirement], False) # >.>
BladeFaith = PaladinSpell(25748, True, Lock, 2.5, 480, 0, ApplyBladeFaith, [BladeFaithRequirement], False)
BladeTruth = PaladinSpell(25749, True, Lock, 2.5, 560, 0, ApplyBladeTruth, [BladeTruthRequirement], False)
BladeValor = PaladinSpell(25750, True, Lock, 2.5, 620, 0, ApplyBladeValor, [BladeValorRequirement], False)
BladeValorDOT = DOTSpell(-11, 80, True)

#GCD
HolySpirit = PaladinSpell(7384, True, 1.5, 2.5, 300, 1000, empty, [ManaRequirement], False)
Atonement = PaladinSpell(16460, True, Lock, 2.5, 420, 0, ApplyAtonement, [AtonementRequirement], True)
Clemency = PaladinSpell(3541, True, 1.5, 2.5, 0, 1000, empty, [ManaRequirement], False)
ShieldLob = PaladinSpell(24, True, 0, 2.5, 100, 0, empty, [], True )
#AOE GCD
HolyCircle = PaladinSpell(16458, True, 1.5, 2.5,130, 1000, empty, [ManaRequirement], False)
TotalEclipse = PaladinSpell(7381, True, 0, 2.5, 100, 0, ApplyTotalEclipse, [], True)
Prominence = PaladinSpell(16457, True, 0, 2.5, 100, 0, empty, [], True)

#oGCD
RequestACat = PaladinSpell(7383, False, 0, Lock, 400, 0, ApplyRequestACat, [RequestACatRequirement], True) #I NEED ONE RIGHT NOW :x
CircleScorn = PaladinSpell(23, False, 0, Lock, 100, 0, ApplyCircleScorn, [CircleScornRequirement], True)
CircleScornDOT = DOTSpell(-6, 30, True)
Intervene = PaladinSpell(16461, False, 0, Lock, 150, 0, ApplyIntervene, [InterveneRequirement], True)
Expiacion = PaladinSpell(25747, False, 0, Lock, 420, 0, ApplyExpiacion, [ExpiacionRequirement], True)
FightOrFlight = PaladinSpell(20, False, 0, Lock, 0, 0, ApplyFightOrFlight, [FightOrFlightRequirement], True)

#Mitigation Actions
DivineVeil = PaladinSpell(3540, False, 0, 0, 0, 0, ApplyDivineVeil, [DivineVeilRequirement], False)
HolySheltron = PaladinSpell(25746, False, 0, 0, 0, 0, ApplyHolySheltron, [HolySheltronRequirement,SheltronRequirement], False)
Cover = PaladinSpell(27, False, 0, 0, 0, 0, ApplyCover, [SheltronRequirement, CoverRequirement], False)
HallowedGround = PaladinSpell(30, False, 0, 0, 0, 0, ApplyHallowedGround, [HallowedGroundRequirement], False)
Intervention = PaladinSpell(7382, False, 0, 0, 0, 0, ApplyIntervention, [SheltronRequirement, InterventionRequirement], False)
def PassageOfArms(time):
    #Function since we will be using it for a set time
    def PassageOfArmsRequirement(Player, Spell):
        return Player.PassageOfArmsCD <= 0, Player.PassageOfArmsCD

    def ApplyPassageOfArms(Player, Enemy):
        Player.PassageOfArmsCD = 120

    return PaladinSpell(7385, False, time, time, 0, 0, ApplyPassageOfArms, [PassageOfArmsRequirement], False)
#buff
FightOrFlightBuff = buff(1.25)

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
17 : BigMit,
25746 : HolySheltron,
7382 : Intervention,
27 : Cover,
3541 : Clemency,
3540 : DivineVeil,
7385 : PassageOfArms(1)
}