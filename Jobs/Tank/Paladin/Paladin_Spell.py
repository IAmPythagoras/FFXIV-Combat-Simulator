from Jobs.Base_Spell import buff, empty, DOTSpell, ManaRequirement
from Jobs.Tank.Paladin.Paladin_Player import Paladin
from Jobs.Tank.Tank_Spell import PaladinSpell
import copy
Lock = 0.5


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

#Apply

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
    if not (FastBladeCombo in Player.EffectList) : Player.EffectList.append(FastBladeCombo)


#Effect

def FightOrFlightEffect(Player, Spell):
    if Spell.isPhysical or isinstance(Spell, DOTSpell):
        Spell.DPSBonus *= FightOrFlightBuff.MultDPS #Giving bonus to the spell if it is physical

def RequestACatEffect(Player, Spell):
    if Spell.id == HolySpirit.id:
        Spell.Potency += 270
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
        if Player.GoringDOT == None:
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
        Player.EffectToRemove(ValorDOTCheck)
        Player.ValorDOT = None


#Combo action

FastBlade = PaladinSpell(1, True, Lock, 2.5, 200, 0, ApplyFastBlade, [], True)
RiotBlade = PaladinSpell(2, True, Lock, 2.5, 170, 0, empty, [], True)
RoyalAuthority = PaladinSpell(3, True, Lock, 2.5, 130,0, empty, [], True)
GoringBlade = PaladinSpell(4, True, Lock, 2.5, 100, 0, empty, [], True)
GoringDOT = DOTSpell(-5, 65, True)

#Confiteor Combo Action

Confetti = PaladinSpell(5, True, Lock, 2.5, 900, 1000, ApplyConfetti, [ManaRequirement, ConfettiRequirement], False) # >.>
BladeFaith = PaladinSpell(6, True, Lock, 2.5, 420, 0, ApplyBladeFaith, [BladeFaithRequirement], False)
BladeTruth = PaladinSpell(7, True, Lock, 2.5, 500, 0, ApplyBladeTruth, [BladeTruthRequirement], False)
BladeValor = PaladinSpell(8, True, Lock, 2.5, 580, 0, ApplyBladeValor, [BladeValorRequirement], False)
BladeValorDOT = DOTSpell(-11, 80, True)
#GCD
HolySpirit = PaladinSpell(9, True, 1.5, 2.5, 270, 1000, empty, [ManaRequirement], False)
Atonement = PaladinSpell(10, True, Lock, 2.5, 420, 0, ApplyAtonement, [AtonementRequirement], True)

#oGCD
RequestACat = PaladinSpell(11, False, 0, Lock, 400, 0, ApplyRequestACat, [RequestACatRequirement], True) #I NEED ONE RIGHT NOW :x
CircleScorn = PaladinSpell(12, False, 0, Lock, 100, 0, ApplyCircleScorn, [CircleScornRequirement], True)
CircleScornDOT = DOTSpell(-6, 30, True)
Intervene = PaladinSpell(13, False, 0, Lock, 150, 0, ApplyIntervene, [InterveneRequirement], True)
Expiacion = PaladinSpell(14, False, 0, Lock, 340, 0, ApplyExpiacion, [ExpiacionRequirement], True)
FightOrFlight = PaladinSpell(15, False, 0, Lock, 0, 0, ApplyFightOrFlight, [FightOrFlightRequirement], True)

#buff
FightOrFlightBuff = buff(1.25)