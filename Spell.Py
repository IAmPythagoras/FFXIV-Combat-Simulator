import copy
from Player import *





class FailedToCast(Exception):#Exception called if a spell fails to cast
    pass

class Spell:
    #This class is any Spell, it will have some subclasses to take Job similar spell, etc.

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        self.id = id
        self.GCD = GCD #True if GCD
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.CastTime = CastTime
        self.RecastTime = RecastTime
        self.Effect = Effect
        self.Requirement = Requirement

    def Cast(self, player, Enemy):
        #This function will cast the spell given by the Fight, it will apply whatever effects it has and do its potency

        tempSpell = copy.deepcopy(self)
        #Creating a tempSpell which will have its values changed according that what effect
        #the player and the enemy have

        #Will apply each effect the player currently has on the spell
        #print("Effect List : " + str(player.EffectList))
        for Effect in player.EffectList:
            Effect(player, tempSpell)#Changes tempSpell
        for Effect in Enemy.EffectList:
            Effect(Enemy, tempSpell)#Changes tempSpell
        #Checks if we meet the spell requirement

        for Requirement in tempSpell.Requirement:
            if(not Requirement(player, tempSpell)) : #Requirements return both whether it can be casted and will take away whatever value needs to be reduced to cast
                print("Failed to cast the spell : " + str(self.id))
                print("The Requirement that failed was : " + str(Requirement.__name__))
                raise FailedToCast("Failed to cast the spell")
        return tempSpell

        #Will put casting spell in player, and do damage/effect once the casting time is over


    def CastFinal(self, player, Enemy):
        #print("##################################")
        #print("Potency of spell: " + str(self.Potency))
        #print("Spell has finally been cast: " + str(self.id))

        self.Effect(player, Enemy)#Put effects on Player and/or Enemy
        #This will include substracting the mana (it has been verified before that the mana was enough)
        
        #print("Current MP: " + str(player.Mana))
        #print("Current Blood: " + str(player.Blood))

        player.TotalPotency+= self.Potency
        Enemy.TotalPotency+= self.Potency  #Doing Damage

        #Will update the NextSpell of the player

        if (not (isinstance(self, DOTSpell))) : player.NextSpell+=1
        if (player.NextSpell == len(player.ActionSet)):#Checks if no more spell to do
            player.TrueLock = True

        return self

class DOTSpell(Spell):
    #Represents DOT
    def __init__(self, id, Potency):
        super().__init__(id, False, 0, 0, Potency,  0, empty, [empty])
        #Note that here Potency is the potency of the dot, not of the ability
        self.DOTTimer = 0   #This represents the timer of the dot, and it will apply at each 3 seconds
    def CheckDOT(self, Player, Enemy, TimeUnit):
        #print("The dot Timer is :  " + str(self.DOTTimer))
        if(self.DOTTimer <= 0):
            #Apply DOT
            tempSpell  = self.Cast(Player, Enemy)#Cast the DOT
            tempSpell.CastFinal(Player, Enemy)
            self.DOTTimer = 3
        else:
            self.DOTTimer = max(0, self.DOTTimer-TimeUnit)
#Function to generate Waiting
def WaitAbility(time):
    return Spell(-1, True, time, time, 0, 0, empty, [])

class BLMSpell(Spell):
    #This class will be all BlackMage Ability
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, IsFire, IsIce, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)#Calls constructor of Spell

        #BLM specific part

        self.IsFire = IsFire
        self.IsIce = IsIce

#The following will be all relevant Black Mage spell, requirement check, effect, etc.

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

def SwiftCastRequirement(Player, Spell):
    return Player.SwiftCastCD <= 0

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
    if (Player.AstralFireStack >= 1 or Player.UmbralIceStack >= 1) : Spell.Potency*=1.2

def TripleCastEffect(Player,Spell):
    if (not Spell.CastTime == 0) and (Spell.GCD):
        #print("Applied TripleCastEffect on : " + str(Spell.id))
        Spell.CastTime=0
        Player.TripleCastStack-=1

def SwiftCastEffect(Player, Spell):
    if (not Spell.CastTime == 0):
        Spell.CastTime=0
        Player.SwiftCastStack = 0

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


def PotionEffect(Player, Spell):
    Spell.Potency *= 1.1


#Function that will check if an effect has ended

def CheckLeyLines(Player,Enemy):
    if(Player.LeyLinesTimer <= 0):
        Player.EffectList.remove(LeyLinesEffect)
        Player.EffectCDList.remove(CheckLeyLines)
        Player.LeyLinesTimer = 0
        return CheckLeyLines

def Thunder3DotCheck(Player,Enemy):
    if(Player.T3Timer <= 0):
        Player.DOTList.remove(T3DOT)
        Player.EffectCDList.remove(Thunder3DotCheck)
        Player.T3Timer = 0

def AFUICheck(Player,Enemy):
    
    if(Player.AFUITimer <= 0):
        #print("LOST AFUI ============================")
        Player.AFUITimer = 0
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0
        Player.EffectCDList.remove(AFUICheck)

# def EnochianLostCheck(Player,Enemy):

#     if(Player.AFUITimer == 0):
#         Player.EffectList.remove(EnochianEffect)
#         Player.EffectCDList.remove(EnochianLostCheck)
#         Player.Enochian = False

def SwiftCastCheck(Player, Enemy):
    if (Player.SwiftCastTimer <= 0 or Player.SwiftCastStack == 0):
        Player.SwiftCastTimer = 0
        Player.SwiftCastStack = 0
        Player.EffectList.remove(SwiftCastEffect)
        Player.EffectCDList.remove(SwiftCastCheck)

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
        #print("Potion Effect out =========================================================================================")

#Applying Effect of Spell

def empty(Player, Enemy):#If no effect
    return True

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

# def ApplyEnochian(Player,Enemy):
#     Player.EnochianCD = 30
#     if not Player.Enochian : #Only add effect is
#         #print('added enochian')
#         Player.EffectList.append(EnochianEffect)
#         Player.EffectCDList.append(EnochianLostCheck)
#         Player.Enochian = True

def ApplySwiftCast(Player,Enemy):
    Player.SwiftCastCD = 60
    Player.SwiftCastStack = 1
    Player.SwiftCastTimer = 15
    Player.EffectList.append(SwiftCastEffect)
    Player.EffectCDList.append(SwiftCastCheck)

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
    if (not (T3DOT in Player.DOTList) ): Player.DOTList.append(T3DOT)
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

def ApplyPotion(Player, Enemy):
    Player.PotionTimer = 30
    Player.EffectList.append(PotionEffect)
    Player.EffectCDList.append(CheckPotion)


def GiveF3Prock(Player, Enemy):
    Player.EffectList.append(F3ProckEffect)

#Special Effect of Spells when casted

def DespairCast(Player, Enemy):
    Player.Mana = 0
    ResetAFUITimer(Player, Enemy)


#List of Black Mage Spell

GCD = 2.33
LONGGCD = 3.27
F1 = BLMSpell(1, True, GCD, GCD, 180, 800, True, False, AddAstralFire1, [ManaRequirement])
#F2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, empty, ManaCheck)#Will not used, so whatever
F3 = BLMSpell(2, True, LONGGCD, GCD, 240, 2000, True, False, AddAstralFire3, [ManaRequirement])
F4 = BLMSpell(3, True, 2.61, GCD, 300, 800, True, False, empty, [ManaRequirement, AstralFireRequirement, EnoughTimeRequirement])
Despair = BLMSpell(4, True, 2.8, GCD, 340, 800, True, False, AddAstralFire1, [ManaRequirement, AstralFireRequirement, EnoughTimeRequirement])

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

#Eno = BLMSpell(11, False, 0.5, 0, 0, 0, False, False, ApplyEnochian, [EnochianRequirement])    #Removed since no longer necessary in Endwalker
Swift = BLMSpell(12, False, 0.5, 0, 0, 0, False, False, ApplySwiftCast, [SwiftCastRequirement])
Triple = BLMSpell(13, False, 0.5, 0, 0, 0, False, False, ApplyTripleCast, [TripleCastRequirement])
Sharp = BLMSpell(14, False, 0.5, 0, 0, 0, False, False, ApplySharpCast, [SharpCastRequirement])
Ley = BLMSpell(15, False, 0.5, 0, 0, 0, False, False, ApplyLeyLines, [LeyLinesRequirement])
Transpo = BLMSpell(16, False, 0, 0, 0, 0, False, False, ApplyTranspose, [TransposeRequirement])
Mana = BLMSpell(17, False, 0.5, 0, 0, 0, False, False, ApplyManaFront, [ManaFrontRequirement])

#EndWalker Spell

Para = BLMSpell(18, True, GCD, GCD, 500, 1600, False, False, ApplyParadox, [ManaRequirement])
Amp = BLMSpell(19, False, 0.5, 0, 0, 0, False, False, ApplyAmplifier, [AmplifierRequirement])

#Potions

Potion = BLMSpell(20, False, 0.5, 0, 0, 0, False, False, ApplyPotion, [])


#Special Effects

B3Starter = BLMSpell(6, True, LONGGCD, GCD, 0, 0, False, True, ApplyBlizzard3, [])
F3Starter = BLMSpell(2, True, LONGGCD, GCD, 0, 0, True, False, AddAstralFire3, [ManaRequirement])
PolyglotStarter = BLMSpell(21, False, 0, 0, 0, 0, False, False, AddPolyglot, [])
Thunder3Starter = BLMSpell(22, False, 0, 0, 0, 0, False, False, ApplyThunder3, [])
F3ProckStarter = BLMSpell(23, False, 0, 0, 0, 0, False, False, GiveF3Prock, [])

#########################################
########## DARK KNIGHT SKILLS ###########
#########################################

class DRKSkill(Spell):
    #A class for Dark Knight Skills containing all the relevant weaponskills/spells, cooldowns,
    #as well as their effects and requirements. For now does not consider out of combo actions.

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, BloodCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.BloodCost = BloodCost

def DarksideEffect(Player, Spell):
    if Player.DarksideTimer > 0:
        Spell.Potency *= 1.10

#Requirements for each Skill and Ability.

def BloodRequirement(Player, Spell):
    #print("Delirium stacks: "+ str(Player.DeliriumStacks))
    if Player.DeliriumStacks > 0 and (Spell.id == 4 or Spell.id == 5):
        Spell.BloodCost = 0
        Player.DeliriumStacks -= 1
        return True
    elif Player.Blood >= 50:
        Player.Blood -= 50
        return True
    return False

def EdgeShadowRequirement(Player, Spell):
    if Player.EdgeShadowCD <= 0 :
        if Player.DarkArts:
            Spell.ManaCost = 0
            Player.DarkArts = False
            return True
        elif Player.Mana >= Spell.ManaCost:
            Player.Mana -= Spell.ManaCost
            return True
    return False

def BloodWeaponRequirement(Player, Spell):
    if Player.BloodWeaponCD <= 0: return True
    return False

def DeliriumRequirement(Player, Spell):
    if Player.DeliriumCD <= 0: return True
    return False

def CarveSpitRequirement(Player, Spell):
    if Player.CarveSpitCD <= 0: return True
    return False

def AbyssalDrainRequirement(Player, Spell):
    if Player.AbyssalDrainCD <= 0: return True
    return False

def SaltedEarthRequirement(Player, Spell):
    if Player.SaltedEarthCD <= 0: return True
    return False

def SaltDarknessRequirement(Player, Spell):
    if Player.SaltedEarthTimer > 0: return True
    return False

def ShadowbringerRequirement(Player, Spell):
    if Player.DarksideTimer > 0 and Player.ShadowbringerCharges > 0: return True
    return False

def PlungeRequirement(Player, Spell):
    if Player.PlungeCharges > 0: return True
    return False

def TBNRequirement(Player, Spell):
    if Player.Mana >= Spell.ManaCost:
        Player.Mana -= Spell.ManaCost
        return True
    return False

#Effect functions that persist after action use

def BloodWeaponEffect(Player, Spell):
    #print("Blood Weapon active")
    if Spell.GCD:
        Player.Mana = min(Player.Mana + 600, 10000)
        Player.Blood = min(100, Player.Blood + 10)

def DeliriumEffect(Player, Spell):
    #print("Delirium active")
    if Spell.id == 4:
        Player.Mana = min(Player.Mana + 200, 10000)
    elif Spell.id == 5:
        Player.Mana = min(Player.Mana + 500, 10000)
    if Player.DeliriumStacks == 0:
        Player.EffectList.remove(DeliriumEffect)

def HardSlashEffect(Player, Spell):
    if Spell.id == 2:
        Multiplier = Spell.Potency/120
        BonusDmg = 140 * Multiplier
        Spell.Potency += BonusDmg
        Player.Mana = min(Player.Mana + 600, 10000)
    if (Spell.id == 2) or (Spell.id == 3) or (Spell.id == 1):
        Player.EffectList.remove(HardSlashEffect)

def SyphonStrikeEffect(Player, Spell):
    if Spell.id == 3:
        Multiplier = Spell.Potency/120
        BonusDmg = 220 * Multiplier
        Spell.Potency += BonusDmg
        Player.Blood = min(100, Player.Blood + 20)
    if (Spell.id == 2) or (Spell.id == 3) or (Spell.id == 1):
        Player.EffectList.remove(SyphonStrikeEffect)

#Cooldown checks to remove effect and restore charges

def BloodWeaponCheck(Player, Spell):
    if Player.BloodWeaponTimer <= 0:
        Player.BloodWeaponTimer = 0
        Player.EffectList.remove(BloodWeaponEffect)
        Player.EffectCDList.remove(BloodWeaponCheck)

def DeliriumCheck(Player, Spell):
    if Player.DeliriumTimer <= 0 or Player.DeliriumStacks == 0:
        Player.EffectList.remove(DeliriumEffect)
        Player.EffectCDList.remove(DeliriumCheck)

def SaltedEarthCheck(Player, Spell):
    if Player.SaltedEarthTimer <= 0:
        Player.DOTList.remove(SaltedEarthDOT)
        Player.SaltedEarthTimer = 0
        Player.EffectCDList.remove(SaltedEarthCheck)

def CheckShadowbringerCharge(Player, Enemy):
    if Player.ShadowbringerCD <= 0:
        if Player.ShadowbringerCharges == 0:
            Player.ShadowbringerCD = 30
        if Player.ShadowbringerCharges == 1:
            Player.EffectCDList.remove(CheckShadowbringerCharge)
        Player.ShadowbringerCharges +=1

def CheckPlungeCharge(Player, Enemy):
    if Player.PlungeCD <= 0:
        if Player.PlungeCharges == 0:
            Player.PlungeCD = 30
        if Player.PlungeCharges == 1:
            Player.EffectCDList.remove(CheckPlungeCharge)
        Player.PlungeCharges +=1


#Apply effects that happen upon action use

def ApplyHardSlashEffect(Player, Spell):
    Player.EffectList.append(HardSlashEffect)

def ApplySyphonEffect(Player, Spell):
    Player.EffectList.append(SyphonStrikeEffect)

def ApplyBloodWeaponEffect(Player, Spell):
    Player.BloodWeaponCD = 60                     
    Player.EffectList.append(BloodWeaponEffect)
    Player.BloodWeaponTimer = 10.7                  #The extra 0.7s is due to a quirk of this buff's timing.
    Player.EffectCDList.append(BloodWeaponCheck)

def ApplyDeliriumEffect(Player, Spell):
    Player.DeliriumCD = 60
    Player.EffectList.append(DeliriumEffect)
    Player.DeliriumStacks = 3
    Player.DeliriumTimer = 30 
    Player.EffectCDList.append(DeliriumCheck)

def ApplyEdgeShadowEffect(Player, Spell):
    Player.DarksideTimer = min(60, Player.DarksideTimer + 30)
    Player.EdgeShadowCD = 1

def ApplyCarveSpitEffect(Player, Spell):
    Player.CarveSpitCD = 60
    Player.AbyssalDrainCD = 60
    Player.Mana = min(Player.Mana + 600, 10000)

def ApplyAbyssalDrainEffect(Player, Spell):
    Player.AbyssalDrainCD = 60
    Player.CarveSpitCD = 60

def ApplySaltedEarth(Player, Spell):
    Player.SaltedEarthCD = 90
    Player.SaltedEarthTimer = 15
    Player.DOTList.append(SaltedEarthDOT)

def ApplySaltDarknessEffect(Player, Spell):
    Player.SaltDarknessCD = 15

def SpendShadowbringer(Player, Spell):
    if Player.ShadowbringerCharges == 2 :
        Player.ShadowbringerCD = 60
    Player.ShadowbringerCharges -= 1
    Player.EffectCDList.append(CheckShadowbringerCharge)

def SummonLivingShadow(Player, Spell):
    Actions = [PDelay, PAbyssalDrain, PPlunge, PQuietus, PShadowbringer, PEdgeShadow, PBloodspiller, PCarveSpit]
    Pet = Esteem(2.36,Actions,[],[],Player.CurrentFight)
    Player.CurrentFight.PlayerList.append(Pet)
    Player.EsteemPointer = Pet
    #print("Esteem enters the battlefield.")

def SpendPlunge(Player,Spell):
    if Player.PlungeCharges == 2 :
        Player.PlungeCD = 30
    Player.PlungeCharges -= 1
    Player.EffectCDList.append(CheckPlungeCharge)

def ApplyDarkArts(Player, Spell):
    Player.DarkArts = True


#List of Weaponskills and Spells used by a Dark Knight Player.
DRKGCD = 2.41           #GCD speed
Lock = 0.75             #Fixed value for animation lock.

HardSlash = DRKSkill(1, True, Lock, DRKGCD, 170, 0, 0, ApplyHardSlashEffect, [])
SyphonStrike = DRKSkill(2, True, Lock, DRKGCD, 120, 0, 0, ApplySyphonEffect, [])
Souleater = DRKSkill(3, True, Lock, DRKGCD, 120, 0, 0, empty, [])
Bloodspiller = DRKSkill(4, True, Lock, DRKGCD, 500, 0, 50, empty, [BloodRequirement])
Quietus = DRKSkill(5, True, Lock, DRKGCD, 200, 0, 50, empty, [BloodRequirement])
Unmend = DRKSkill(6, True, Lock, 2.50, 150, 0, 0, empty, [])

#List of Buffs used by a Dark Knight Player.

BloodWeapon = DRKSkill(7, False, Lock, 0, 0, 0, 0, ApplyBloodWeaponEffect, [BloodWeaponRequirement])
Delirium = DRKSkill(8, False, Lock, 0, 0, 0, 0, ApplyDeliriumEffect, [DeliriumRequirement])

#List of Abilities used by a Dark Knight Player.

EdgeShadow = DRKSkill(9, False, Lock, 0, 460, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
FloodShadow = DRKSkill(10, False, Lock, 0, 160, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
CarveSpit = DRKSkill(11, False, Lock, 0, 510, 0, 0, ApplyCarveSpitEffect, [CarveSpitRequirement])
AbyssalDrain = DRKSkill(12, False, Lock, 0, 150, 0, 0, ApplyAbyssalDrainEffect, [AbyssalDrainRequirement])
SaltedEarth = DRKSkill(13, False, Lock, 0, 50, 0, 0, ApplySaltedEarth, [SaltedEarthRequirement]) #Ground target DOT, ticks once upon placement.
SaltedEarthDOT = DOTSpell(14, 50)
SaltDarkness = DRKSkill(15, False, Lock, 0, 500, 0, 0, empty, [SaltDarknessRequirement])
Shadowbringer = DRKSkill(16, False, Lock, 0, 600, 0, 0, SpendShadowbringer, [ShadowbringerRequirement])
LivingShadow = DRKSkill(17, False, Lock, 0, 0, 0, 50, SummonLivingShadow, [BloodRequirement])
Plunge = DRKSkill(18, False, Lock, 0, 150, 0, 0, SpendPlunge, [PlungeRequirement])

TBN = DRKSkill(27, False, Lock, 0, 0, 3000, 0, ApplyDarkArts, [TBNRequirement])     #Simply makes the next EdgeShadow free for now.

#List of Abilities performed by Living Shadow.

PAbyssalDrain = DRKSkill(19, True, 0.5, 2.36, 300, 0, 0, empty, [])
PPlunge = DRKSkill(20, True, 0.5, 2.36, 300, 0, 0, empty, [])
PQuietus = DRKSkill(21, True, 0.5, 2.36, 300, 0, 0, empty, [])
PShadowbringer = DRKSkill(22, True, 0.5, 2.36, 450, 0, 0, empty, [])
PEdgeShadow = DRKSkill(23, True, 0.5, 2.36, 300, 0, 0, empty, [])
PBloodspiller = DRKSkill(24, True, 0.5, 2.36, 300, 0, 0, empty, [])
PCarveSpit = DRKSkill(25, True, 0.5, 2.36, 300, 0, 0, empty, [])
PDelay = DRKSkill(26, True, 0, 4.50, 0, 0, 0, empty, [])    #6s animation before it starts attacking.


#print("feelsbad for drk man")