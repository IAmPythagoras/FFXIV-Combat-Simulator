from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import NinjaSpell
from Jobs.Melee.Ninja.Ninja_Spell import ArmorCrush
Lock = 0.75


#Requirement

def FleetingRaijuRequirement(Player, Spell):
    return Player.RaijuReady

def MeisuiRequirement(Player, Spell):
    return Player.Suiton and Player.MeisuiCD <= 0

def BhavacakraRequirement(Player, Spell):
    return Player.NinkiGauge >= 50

def TrickAttackRequirement(Player, Spell):
    return Player.TrickAttackCD <= 0

def MugRequirement(Player, Spell):
    return Player.MugCD <= 0

def DreamWithinADreamRequirement(Player, Spell):
    return Player.DreamWithinADreamCD <= 0

#Apply

def ApplyFleetingRaiju(Player, Enemy):
    Player.RaijuReady = False

def ApplyMeisui(Player, Enemy):
    Player.Suiton = False
    Player.AddNinki(50)
    Player.MeisuiCD = 120
    Player.MeisuiTimer = 30
    Player.EffectList.append(MeisuiEffect)
    Player.EffectCDList.append(MeisuiCheck)

def ApplyBhavacakra(Player, Enemy):
    Player.AddNinki(-50)

def ApplyTrickAttack(Player, Enemy):
    Player.buffList.append(TrickAttackBuff)
    Player.TrickAttackCD = 60
    Player.TrickAttackTimer = 15
    Player.EffectCDList.append(TrickAttackCheck)

def ApplyMug(Player, Enemy):
    Enemy.buffList.append(MugBuff)
    Player.MugCD = 120
    Player.MugTimer = 20
    Player.AddNinki(40)
    Player.EffectCDList.append(MugCheck)

def ApplyHuraijin(Player, Enemy):
    Player.HutonTimer = 60

def ApplyDreamWithinADream(Player, Enemy):
    Player.DreamWithinADreamCD = 60

def ApplySpinningEdge(Player, Enemy):
    Player.AddNinki(5)
    
    if not (SpinningEdgeCombo in Player.EffectList): Player.EffectList.append(SpinningEdgeCombo)


#Effect

def MeisuiEffect(Player, Spell):
    if Spell.id == Bhavacakra.id:
        Spell.Potency += 150

def SpinningEdgeCombo(Player, Spell):
    if Spell.id == GustSlash.id:
        Spell.Potency += 160
        Player.AddNinki(5)
        Player.EffectToRemove.append(SpinningEdgeCombo)
        if not (GustSlashCombo in Player.EffectList) : Player.EffectList.append(GustSlashCombo)

def GustSlashCombo(Player, Spell):
    if Spell.id == AeolianEdge.id:
        Spell.Potency += 240
        Player.AddNinki(15)
        Player.EffectToRemove.append(GustSlashCombo)
    elif Spell.id == ArmorCrush.id:
        Spell.Potency += 220
        Player.AddNinki(15)
        Player.AddHuton(30)
        Player.EffectToRemove.append(GustSlashCombo)


#Check

def MeisuiCheck(Player, Enemy):
    if Player.MeisuiTimer <= 0:
        Player.EffectList.remove(MeisuiEffect)
        Player.EffectToRemove.append(MeisuiCheck)

def TrickAttackCheck(Player, Enemy):
    if Player.TrickAttackTimer <= 0:
        Player.buffList.remove(TrickAttackBuff)
        Player.EffectToRemove.append(TrickAttackCheck)

def MugCheck(Player, Enemy):
    if Player.MugTimer <= 0:
        Enemy.buffList.remove(MugBuff)
        Player.EffectToRemove.append(MugCheck)



#GCD
SpinningEdge = NinjaSpell(1, True, Lock, 2.5, 220, ApplySpinningEdge, [], True )
GustSlash = NinjaSpell(2, True, Lock, 2.5, 160, empty, [], True)
AeolianEdge = NinjaSpell(3, True, Lock, 2.5, 200, empty, [], True)
ArmorCrush = NinjaSpell(4, True, Lock, 2.5, 200, empty, [], True)
Huraijin = NinjaSpell(6, True, Lock, 2.5, 200, ApplyHuraijin, [], True)
FleetingRaiju = NinjaSpell(11, True, Lock, 2.5, 560, ApplyFleetingRaiju, [FleetingRaijuRequirement], True)

#oGCD
DreamWithinADream = NinjaSpell(5, False, Lock, 0, 3*150, ApplyDreamWithinADream, [DreamWithinADreamRequirement], False)
Mug = NinjaSpell(7, False, Lock, 0, 150, ApplyMug, [MugRequirement], True)
TrickAttack = NinjaSpell(8, False, Lock, 0, 400, ApplyTrickAttack, [TrickAttackRequirement], False)
Bhavacakra = NinjaSpell(9, False, Lock, 0, 350, ApplyBhavacakra, [BhavacakraRequirement], False)
Meisui = NinjaSpell(10, False, Lock, 0, 0, ApplyMeisui, [MeisuiRequirement], False)


#buff
MugBuff = buff(1.05)
TrickAttackBuff = buff(1.1)