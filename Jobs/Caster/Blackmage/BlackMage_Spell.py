from Jobs.Caster.Caster_Spell import BLMSpell
from Jobs.Base_Spell import DOTSpell, empty, ManaRequirement

import copy
Lock = 0.75

#Requirement
def AmplifierRequirement(Player, Spell):
    return Player.AmplifierCD <= 0

# def EnochianOnRequirement(player, Spell):
#     return player.Enochian

def ManaRequirement(player, Spell):
    if player.Mana >= Spell.ManaCost :
        player.Mana -= Spell.ManaCost   #ManaRequirement is the only Requirement that actually removes Ressources
        return True
    return False

def AstralFireRequirement(player, Spell):
    return player.AstralFireStack >= 1

def UmbralIceRequirement(Player, Spell):
    return Player.UmbralIceStack >= 1

def PolyglotRequirement(Player, Spell):
    return Player.PolyglotStack >= 1

def FireSpellRequirement(Player, Spell):
    return Player.AstralFireStack >=1

def IceSpellRequirement(Player, Spell):
    return Player.UmbralIceStack >=1

def LeyLinesRequirement(Player, Spell):
    return Player.LeyLinesCD <= 0

def TripleCastRequirement(Player, Spell):
    return Player.TripleCastCharges > 0

def SharpCastRequirement(Player, Spell):
    return Player.SharpCastCharges > 0

# def EnochianRequirement(Player, Spell):
#     return (Player.EnochianCD == 0) and ((Player.AstralFireStack >= 1) or (Player.UmbralIceStack >= 1))

def ManaFrontRequirement(Player, Spell):
    return (Player.ManaFrontCD <= 0)

def TransposeRequirement(Player, Spell):
    return (Player.TransposeCD <= 0)

def ParadoxRequirement(Player, Spell):
    return Player.Paradox

def EnoughTimeRequirement(Player, Spell):
    return Player.AFUITimer >= Spell.CastTime

#Effect of spells
def AstralFire(Player, Spell):

    if(not isinstance(Spell, BLMSpell)) : return False

    Stack = Player.AstralFireStack

    if (Spell.IsFire):
        if(Stack == 1): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.4#Update Damage
        elif(Stack == 2): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.6#Update Damage
        elif (Stack == 3): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.8#Update Damage
    elif (Spell.IsIce):
        if(Stack == 1): 
            Spell.Potency*=0.9#Update Damage
            Spell.ManaCost*=0.5
        elif(Stack == 2): 
            Spell.Potency*=0.8#Update Damage
            Spell.ManaCost*=0.25
        elif (Stack == 3): 
            Spell.Potency*=0.7#Update Damage
            Spell.ManaCost*=0
            Spell.CastTime*=0.5

def UmbralIce(Player, Spell):
    if(not isinstance(Spell, BLMSpell)) : return False
    Stack = Player.UmbralIceStack
    if(Spell.IsIce):
        if (Stack == 1):
            Spell.ManaCost *= 0.75
        elif (Stack == 2):
            Spell.ManaCost *= 0.5
        elif (Stack == 3):
            Spell.ManaCost = 0
    elif(Spell.IsFire):
        if (Stack == 1):
            Spell.ManaCost *= 0.5
            Spell.Potency *= 0.9
        elif (Stack == 2):
            Spell.ManaCost *= 0.25
            Spell.Potency *= 0.8
        elif (Stack == 3):
            Spell.ManaCost = 0
            Spell.CastTime *= 0.5
            Spell.Potency *= 0.7
    elif(Spell.id == 18 and Stack >= 1): #Paradox
        Spell.ManaCost = 0
        Spell.CastTime = 0

def LeyLinesEffect(Player, Spell):
    Spell.CastTime*=0.85
    Spell.RecastTime*=0.85

def EnochianEffect(Player, Spell):
    if (Player.AstralFireStack >= 1 or Player.UmbralIceStack >= 1) : Spell.Potency*=1

def TripleCastEffect(Player,Spell):
    if (not Spell.CastTime == 0) and (Spell.GCD):
        #print("Applied TripleCastEffect on : " + str(Spell.id))
        Spell.CastTime=0
        Player.TripleCastStack-=1

def SharpCastEffect(Player,Spell):

    if(Spell.id == 8):#Id 0 is T3
        Player.T3Prock = 1
        Player.SharpCastStack = 0
        Player.EffectList.append(T3ProckEffect)
        Player.SharpCastGoThroughOnce = False
    elif(Spell.id == 1 or (Spell.id == 18 and Player.AstralFireStack >= 1)): #Fire 1
        Player.F3Prock == 1
        Player.SharpCastStack = 0
        Player.EffectList.append(F3ProckEffect)
        Player.SharpCastGoThroughOnce = False

def T3ProckEffect(Player, Spell):

    if(Spell.id == 8 and Player.T3Prock == 1 and Player.SharpCastGoThroughOnce):
        Spell.CastTime = 0
        Spell.ManaCost = 0
        Player.T3Prock = 0

        #Finding Multiplying bonus so far

        Mult = Spell.Potency/50 #40 is based potency of Thunder 3

        NewBonus = 350 * Mult #To find new bonus

        Spell.Potency += NewBonus

        Player.EffectList.remove(T3ProckEffect)
        
    Player.SharpCastGoThroughOnce = True
def F3ProckEffect(Player, Spell):

    if (Spell.id == 2 and Player.SharpCastGoThroughOnce):
        Spell.CastTime = 0
        Spell.ManaCost = 0
        Player.EffectList.remove(F3ProckEffect)

    Player.SharpCastGoThroughOnce = True

def UmbralHeartEffect(Player, Spell):
    if (not (isinstance(Spell, BLMSpell))) : return False
    if(Player.UmbralHeartStack >= 1 and Spell.IsFire and Player.AstralFireStack >= 1):
        if(Spell.id != 5):
            Spell.ManaCost/=2
            Player.UmbralHeartStack-=1
    elif(Player.UmbralHeartStack <= 0):
        Player.UmbralHeartStack = 0
        Player.EffectList.remove(UmbralHeartEffect)


def PotionEffect(Player, Spell):    #This effect is only so it can be seen
    pass


#Function that will check if an effect has ended

def CheckLeyLines(Player,Enemy):
    if(Player.LeyLinesTimer <= 0):
        Player.EffectList.remove(LeyLinesEffect)
        Player.EffectCDList.remove(CheckLeyLines)
        Player.LeyLinesTimer = 0
        return CheckLeyLines

def Thunder3DotCheck(Player,Enemy):
    if(Player.T3Timer <= 0):
        Player.DOTList.remove(Player.T3)
        Player.EffectCDList.remove(Thunder3DotCheck)
        Player.T3Timer = 0

def AFUICheck(Player,Enemy):
    
    if(Player.AFUITimer <= 0):
        #print("LOST AFUI ============================")
        Player.AFUITimer = 0
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0
        Player.EffectCDList.remove(AFUICheck)

def TripleCastCheck(Player, Enemy):
    if (Player.TripleCastTimer <= 0 or Player.TripleCastStack == 0):
        #print("Removed Tripe")
        Player.TripleCastTimer = 0
        Player.TripleCastStack = 0
        Player.EffectList.remove(TripleCastEffect)
        Player.EffectCDList.remove(TripleCastCheck)

def SharpCastCheck(Player, Enemy):
    if (Player.SharpCastTimer <= 0 or Player.SharpCastStack == 0) : 
        Player.SharpCastStack = 0
        Player.SharpCastTimer = 0
        Player.EffectList.remove(SharpCastEffect)
        Player.EffectCDList.remove(SharpCastCheck)

def CheckSharpCast(Player, Enemy):

    if Player.SharpCastCD <= 0:
        if Player.SharpCastCharges == 0:
            Player.SharpCastCD = 30
        elif Player.SharpCastCharges == 1:
            Player.EffectCDList.remove(CheckSharpCast)
        Player.SharpCastCharges +=1

def CheckTripleCastCharges(Player, Enemy):
    if Player.TripleCastCD <= 0:
        if Player.TripleCastCharges == 0:
            Player.TripleCastCD = 60
        elif Player.SharpCastCharges == 1:
            Player.EffectCDList.remove(CheckTripleCastCharges)
        Player.TripleCastCharges += 1

def CheckPotion(Player, Enemy):

    if(Player.PotionTimer <= 0): 
        Player.EffectList.remove(PotionEffect)
        Player.EffectCDList.remove(CheckPotion)
        Player.Stat["MainStat"] /= 1.1 #Reset MainStat
        #print("Potion Effect out =========================================================================================")

#Applying Effect of Spell

def ResetAFUITimer(Player, Enemy):
    Player.AFUITimer = 15

def AddAstralFire1(Player, Enemy):#Adds one Astral Fire

    if(Player.AstralFireStack >=0 and Player.UmbralIceStack == 0):
        Player.AstralFireStack = min(3, Player.AstralFireStack + 1)
        if Player.AFUITimer <= 0: Player.EffectCDList.append(AFUICheck)
        Player.AFUITimer = 15
    elif (Player.AstralFireStack == 0 and Player.UmbralIceStack >=1):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0
        Player.AFUITimer = 0

def AddAstralFire3(Player, Enemy):#Astral Fire 3
    Player.AstralFireStack = 3
    Player.UmbralIceStack = 0
    if Player.AFUITimer <= 0: Player.EffectCDList.append(AFUICheck)
    Player.AFUITimer = 15

def AddUmbralIce3(Player, Enemy):#Add Umbral Ice 3
    Player.UmbralIceStack = 3
    Player.AstralFireStack = 0
    if Player.AFUITimer <= 0: Player.EffectCDList.append(AFUICheck)
    Player.AFUITimer = 15

def ApplyTripleCast(Player,Enemy):
    if Player.TripleCastCharges == 2 : Player.TripleCastCD = 60
    Player.TripleCastCharges -= 1
    Player.TripleCastStack = 3
    Player.TripleCastTimer = 15
    if (not (TripleCastEffect in Player.EffectList) ): Player.EffectList.append(TripleCastEffect)
    if (not (TripleCastCheck in Player.EffectCDList) ) : Player.EffectCDList.append(TripleCastCheck)
    if (not (CheckTripleCastCharges in Player.EffectCDList) ) : Player.EffectCDList.append(CheckTripleCastCharges)

def ApplyLeyLines(Player,Enemy):
    Player.LeyLinesCD = 120
    Player.LeyLinesTimer = 30
    Player.EffectList.append(LeyLinesEffect)
    Player.EffectCDList.append(CheckLeyLines)

def ApplySharpCast(Player,Enemy):
    if Player.SharpCastCharges == 2 : Player.SharpCastCD = 30
    Player.SharpCastStack = 1
    Player.SharpCastCharges -= 1
    Player.SharpCastTimer = 30
    Player.EffectCDList.append(CheckSharpCast)  #To check charges
    Player.EffectCDList.append(SharpCastCheck)  #To check if to remove effect
    Player.EffectList.append(SharpCastEffect)

def ApplyManaFront(Player,Enemy):
    Player.ManaFrontCD = 180
    Player.Mana = min(10000, Player.Mana + 3000)
    #Add mana

def ApplyBlizzard4(Player,Enemy):
    Player.UmbralHeartStack = 3
    Player.EffectList.append(UmbralHeartEffect)
    Player.Paradox = True

def ApplyThunder3(Player,Enemy):
    if (not (Player.T3 in Player.DOTList) ): 
        Player.T3 = copy.deepcopy(T3DOT)
        Player.DOTList.append(Player.T3)
    if (not (Thunder3DotCheck in Player.EffectCDList) ): Player.EffectCDList.append(Thunder3DotCheck)
    Player.T3Timer = 30

def ApplyTranspose(Player, Enemy):
    
    if(Player.UmbralIceStack >= 1):
        Player.UmbralIceStack = 0
        Player.AstralFireStack = 1
    elif(Player.AstralFireStack >= 1):
        Player.UmbralIceStack = 1
        Player.AstralFireStack = 0

    Player.TransposeCD = 5

def ApplyPolyglot(Player, Enemy):
    Player.PolyglotStack -= 1

def ApplyParadox(Player, Enemy):
    Player.Paradox = False
    if(Player.UmbralIceStack >= 1):
        ResetAFUITimer(Player, Enemy)
        Player.UmbralIceStack = min(3, Player.UmbralIceStack + 1)
    elif(Player.AstralFireStack >= 1):
        ResetAFUITimer(Player, Enemy)


def AddPolyglot(Player, Enemy):
    Player.PolyglotStack = min(2, Player.PolyglotStack + 1)


def ApplyAmplifier(Player, Enemy):
    Player.PolyglotStack = min(2, Player.PolyglotStack + 1)
    Player.AmplifierCD = 120

def ApplyBlizzard3(Player, Enemy):
    if(Player.AstralFireStack == 3) : Player.Paradox = True
    AddUmbralIce3(Player, Enemy)


def GiveF3Prock(Player, Enemy):
    Player.EffectList.append(F3ProckEffect)

#Special Effect of Spells when casted

def DespairCast(Player, Enemy):
    Player.Mana = 0
    ResetAFUITimer(Player, Enemy)


#List of Black Mage Spell

GCD = 2.50
LONGGCD = 3.50
F1 = BLMSpell(1, True, GCD, GCD, 180, 800, True, False, AddAstralFire1, [ManaRequirement])
#F2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, empty, ManaCheck)#Will not used, so whatever
F3 = BLMSpell(2, True, LONGGCD, GCD, 240, 2000, True, False, AddAstralFire3, [ManaRequirement])
F4 = BLMSpell(3, True, 2.8, GCD, 300, 800, True, False, empty, [ManaRequirement, AstralFireRequirement, EnoughTimeRequirement])
Despair = BLMSpell(4, True, 3.0, GCD, 340, 800, True, False, AddAstralFire1, [ManaRequirement, AstralFireRequirement, EnoughTimeRequirement])

#Ice Spell
#B1 = BLMSpell(5, True, 2.19, 2.19, 180, 400, False, True, AddUmbralIce1, ManaCheck)#Not used so whatever
#B2 = BLMAbility(6, True, 2.17, 2.17, 140, 200, False, True, empty, ManaCheck)#AOE so not used
B3 = BLMSpell(6, True, LONGGCD, GCD, 240, 800, False, True, ApplyBlizzard3, [ManaRequirement])
B4 = BLMSpell(7, True, GCD, GCD, 300, 800, False, True, ApplyBlizzard4, [ManaRequirement, UmbralIceRequirement, EnoughTimeRequirement])

#DOT

T3 = BLMSpell(8, True, GCD, GCD, 50, 400, False, False, ApplyThunder3, [ManaRequirement])
T3DOT = DOTSpell(9, 35)
#Special Damage Spell

Xeno = BLMSpell(10, True, 0.7, GCD, 660, 0, False, False, ApplyPolyglot, [PolyglotRequirement])

#Boosting Ability

Triple = BLMSpell(13, False, 0.5, 0, 0, 0, False, False, ApplyTripleCast, [TripleCastRequirement])
Sharp = BLMSpell(14, False, 0.5, 0, 0, 0, False, False, ApplySharpCast, [SharpCastRequirement])
Ley = BLMSpell(15, False, 0.5, 0, 0, 0, False, False, ApplyLeyLines, [LeyLinesRequirement])
Transpo = BLMSpell(16, False, 0, 0, 0, 0, False, False, ApplyTranspose, [TransposeRequirement])
Mana = BLMSpell(17, False, 0.5, 0, 0, 0, False, False, ApplyManaFront, [ManaFrontRequirement])

#EndWalker Spell

Para = BLMSpell(18, True, GCD, GCD, 500, 1600, False, False, ApplyParadox, [ManaRequirement])
Amp = BLMSpell(19, False, 0.5, 0, 0, 0, False, False, ApplyAmplifier, [AmplifierRequirement])
