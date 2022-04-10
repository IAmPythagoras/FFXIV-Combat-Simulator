import copy

from Player import *
from Fight import ComputeDamage



def AddFlatBonus(Potency, CurrentPotency, Bonus):

    Mult = CurrentPotency/Potency

    Bonus *= Mult

    return Bonus + CurrentPotency




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
        self.Effect = [Effect]
        self.Requirement = Requirement
        self.DPSBonus = 1

    def Cast(self, player, Enemy):
        #This function will cast the spell given by the Fight, it will apply whatever effects it has and do its potency

        tempSpell = copy.deepcopy(self)
        #Creating a tempSpell which will have its values changed according that what effect
        #the player and the enemy have
        #print("Status of DualCast : " + str(player.DualCast))
        #Will apply each effect the player currently has on the spell
        #print("Effect List : " + str(player.EffectList))
        for Effect in player.EffectList:
            Effect(player, tempSpell)#Changes tempSpell
        for Effect in Enemy.EffectList:
            Effect(player, tempSpell)#Changes tempSpell
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

        
        for Effect in self.Effect:
            Effect(player, Enemy)#Put effects on Player and/or Enemy
        #This will include substracting the mana (it has been verified before that the mana was enough)
        
        #print("Current MP: " + str(player.Mana))
        #print("Current Blood: " + str(player.Blood))
        Damage = ComputeDamage(player, self.Potency, Enemy.Bonus, self.DPSBonus)    #Damage computation

        if isinstance(player, Queen) or isinstance(player, Esteem):
            player.Master.TotalPotency+= self.Potency
            player.Master.TotalDamage += Damage
        else:
            player.TotalPotency+= self.Potency
            player.TotalDamage += Damage
        
        Enemy.TotalPotency+= self.Potency  #Adding Potency
        Enemy.TotalDamage += Damage #Adding Damage


        #Will update the NextSpell of the player

        if (not (isinstance(self, DOTSpell))) : player.NextSpell+=1
        if (player.NextSpell == len(player.ActionSet)):#Checks if no more spell to do
            player.TrueLock = True

        return self

class DOTSpell(Spell):
    #Represents DOT
    def __init__(self, id, Potency):
        super().__init__(id, False, 0, 0, Potency,  0, empty, [])
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
    if (Player.AstralFireStack >= 1 or Player.UmbralIceStack >= 1) : Spell.Potency*=1

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
        Player.Stat["MainStat"] /= 1.1 #Reset MainStat
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
    Player.EffectList.insert(0,SwiftCastEffect)
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

def ApplyPotion(Player, Enemy):
    Player.PotionTimer = 30
    Player.Stat["MainStat"] *= 1.1
    Player.EffectList.insert(0,PotionEffect)
    Player.EffectCDList.append(CheckPotion)


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

Potion = BLMSpell(-2, False, 0.5, 0, 0, 0, False, False, ApplyPotion, [])


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
    Pet = Esteem(2.5,Actions,[],[],Player.CurrentFight,Player)
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

#########################################
########## NINJA PLAYER #################
#########################################

class NinjaSpell(Spell):

    def __init__(self, id, WeaponSkill, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)
        self.WeaponSkill = WeaponSkill


#Requirement
def TenChiJinRequirement(Player, Spell):
    return Player.TenChiJinCd <= 0

def BunshinRequirement(Player, Spell):
    return Player.BunshinCd <= 0

def MeisuiRequirement(Player, Spell):
    return Player.MeisuiCd <= 0 and Player.SuitonTimer > 0

def NinkiRequirement(Player, Spell):
    return Player.NinkiGauge >= 50

def DWDRequirement(Player, Spell):
    return Player.DreamWithinADreamCd <= 0

def RaijuRequirement(Player, Spell):
    return Player.RaitonStacks > 0

def HyoshoRequirement(Player, Spell):
    return Player.KassatsuTimer > 0

def SuitonRequirement(Player, Spell):
    return Player.SuitonTimer > 0

def NinjutsuRequirement(Player, Spell):
    return Player.NinjutsuStack > 0

def TrickAttackRequirement(Player, Spell):
    return Player.TrickAttackCd <= 0

def MugRequirement(Player, Spell):
    return Player.MugCd <= 0

def KassatsuRequirement(Player, Spell):
    return Player.KassatsuCd <= 0

#Apply
def ApplyHide(Player, Enemy): Player.NinjutsuStack = 2

def ApplyTenChiJin(Player, Enemy):
    Player.TenChiJinCd = 120
    ApplyRaiton(Player, Enemy)
    ApplySuiton(Player, Enemy)
    Player.NinjutsuStack += 2 #Reduced by 1 in ApplyRaiton() and ApplySuiton()

def ApplyBunshin(Player, Enemy):
    Player.BunshinStacks = 5
    Player.BunshinTimer = 30
    Player.KamaitachiTimer = 45
    Player.NinkiGauge = max(0, Player.NinkiGauge - 50)
    Player.EffectList.insert(0, BunshinEffect)   #Insert so first effect

def ApplyMeisui(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 50)
    Player.MeisuiCd = 120
    Player.MeisuiTimer = 30
    Player.SuitonTimer = 0
    Player.EffectList.append(MeisuiEffect)

def ApplyBhavacakra(Player, Enemy):
    Player.NinkiGauge = max(0, Player.NinkiGauge - 50)

def ApplyDWD(Player, Enemy):
    Player.DreamWithinADreamCd = 60

def ApplySuiton(Player, Enemy):
    Player.SuitonTimer = 20
    Player.NinjutsuStack-=1
    

def ApplyRaiton(Player, Enemy):
    Player.RaitonStacks = min(3, Player.RaitonStacks+1)
    Player.RaitonStacksTimer = 30
    Player.NinjutsuStack -=1 #Assumed to only come here if stacks is positive (so never negative)
    if not (RaitonStacksEffect in Player.EffectList): Player.EffectList.append(RaitonStacksEffect)

def ApplyKassatsu(Player, Enemy):
    Player.KassatsuCd = 60
    Player.KassatsuTimer = 15

def ApplySpinningEdge(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 5)
    Player.EffectList.append(SpinningEdgeEffect)

def ApplyGustSlash(Player, Enemy):
    Player.EffectList.append(GustSlashEffect)

def ApplyArmorCrush(Player, Enemy):
    Player.HutonGauge = min(60, Player.HutonGauge + 30)

def ApplyTrickAttack(Player, Enemy):
    Player.TrickAttackCd = 60
    Enemy.Bonus *= 1.05
    #Set up a timer for the Enemy on trick attack
    Enemy.EffectList.append(TrickAttackEffect)

def ApplyMug(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 40)
    Player.MugCd = 120

def ApplyKassatsu(Player, Enemy):
    Player.KassatsuTimer = 15

def ApplyRaiju(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 5)

def ApplyKamaitachi(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 10)

def NinjutsuTimerEffect(Player, Enemy):
    if(Player.NinjutsuStack != 2):
        if(Player.NinjutsuCd <= 0):
            Player.NinjutsuStack+=1
            if (Player.NinjutsuStack == 1):
                Player.NinjutsuCd = 20


#Effect

def BunshinEffect(Player, Spell):

    if isinstance(Spell,NinjaSpell) and (Spell.WeaponSkill):
        #It will be assumed that each ability are melee, so simply adding the flat bonus of 160 potency, it will be pushed onto the array, so first

        Spell.Potency += 160
        Player.BunshinStacks -=1
        Player.NinkiGauge = min(100, Player.NinkiGauge + 5)
    
    if (Player.BunshinStacks == 0) or (Player.BunshinTimer <= 0):
        Player.EffectList.remove(BunshinEffect)
        Player.BunshinTimer = 0




def MeisuiEffect(Player, Spell):

    if(Player.MeisuiTimer <= 0):
        Player.EffectList.remove(MeisuiEffect)
    elif(Spell.id == 12):
        Spell.Potency = AddFlatBonus(Bhavacakra.Potency, Spell.Potency, 100)


def RaitonStacksEffect(Player, Spell):
    #Might be lost depending on what spell is cast, so must check for that
    if (Spell.id == 0) or (Spell.id == 1) or (Spell.id == 2) or (Spell.id == 3) or Player.RaitonStacksTimer <= 0 or Player.RaitonStacks == 0:#Remove if skill or timer out or stacks empty
        Player.RaitonStacks = 0
        Player.RaitonStacksTimer = 0
        Player.EffectList.remove(RaitonStacksEffect)


def TrickAttackEffect(Player, Spell):
    if(Player.TrickAttackTimer <= 0): 
        Player.CurrentFight.Enemy.EffectList.remove(TrickAttackEffect)
        Player.CurrentFight.Enemy.Bonus /= 1.05

def SpinningEdgeEffect(Player, Spell):
    if (Spell.id == 1):
        Spell.Potency = AddFlatBonus(140, Spell.Potency, 160)
        Player.NinkiGauge = min(100, Player.NinkiGauge + 5)
        Player.EffectList.remove(SpinningEdgeEffect)

def GustSlashEffect(Player,Spell):
    if (Spell.id == 2):
        Spell.Potency = AddFlatBonus(180, Spell.Potency, 220)
        Player.NinkiGauge = min(100, Player.NinkiGauge + 15)
        Player.EffectList.remove(GustSlashEffect)
    elif(Spell.id == 3):
        Spell.Potency  = AddFlatBonus(180, Spell.Potency, 200)
        Player.NinkiGauge = min(100, Player.NinkiGauge + 15)
        Player.EffectList.remove(GustSlashEffect)

def AutoEffect(Player, Spell):
    Player.DOTList.append(Autos)
    Player.EffectList.remove(AutoEffect)






#Ability
NinjaGCD = 2.5

#1-2-3 Combo
SpinningEdge = NinjaSpell(0, True, True, 0, NinjaGCD,  200, 0, ApplySpinningEdge, [])
GustSlash = NinjaSpell(1, True,True, 0, NinjaGCD, 140, 0, ApplyGustSlash, [])
AeolianEdge = NinjaSpell(2, True,True, 0, NinjaGCD, 180, 0, empty, [])
ArmorCrush = NinjaSpell(3, True,True, 0, NinjaGCD, 180, 0, ApplyArmorCrush, [])

#oGCD
TrickAttack = NinjaSpell(4, False,False, Lock, 0, 400, 0, ApplyTrickAttack, [TrickAttackRequirement])
Mug = NinjaSpell(5, False,False, Lock, 0, 150, 0, ApplyMug, [MugRequirement])
Kassatsu = NinjaSpell(6, False,False, Lock, 0, 0, 0, ApplyKassatsu, [KassatsuRequirement])
DWD = NinjaSpell(11, False,False, Lock, 0, 450, 0, ApplyDWD, [DWDRequirement]) #Dream Within a Dream
Bhavacakra = NinjaSpell(12, False,False, Lock, 0, 400,0, ApplyBhavacakra, [NinkiRequirement])
Meisui = NinjaSpell(13, False,False, Lock, 0, 0, 0, ApplyMeisui, [MeisuiRequirement])
#test = NinjaSpell(id, WS, GCD, CT, RT, PO, MANA, E, R)
#Ninjutsu
#Only implementing those we will realistically use
Raiton = NinjaSpell(7, False,True, 2*Lock, NinjaGCD + 2*Lock, 650,0, ApplyRaiton, [NinjutsuRequirement])
Suiton = NinjaSpell(8, False,True,2*Lock, NinjaGCD + 2*Lock, 500,0, ApplySuiton, [NinjutsuRequirement])
Hyosho = NinjaSpell(9, False,True,2*Lock, NinjaGCD + 2*Lock, 1200,0, empty, []) #HyoshoRequirement
TenChiJin = NinjaSpell(15, False, False, 4*Lock, 0, 450 + 650 + 500, 0,ApplyTenChiJin, [TenChiJinRequirement])
#Tenchijin will be assumed to be Ten-Chi-Jin (since optimal)

#Raiju
Raiju = NinjaSpell(10, True,True, Lock, NinjaGCD, 560, 0, ApplyRaiju, [RaijuRequirement])

#Bunshin
Bunshin = NinjaSpell(14, False, False, Lock, 0, 0, 0, ApplyBunshin, [BunshinRequirement, NinkiRequirement])
Kamaitachi = NinjaSpell(15, False, True, 0, NinjaGCD, 550, 0, ApplyKamaitachi, [])

class NinjaDOT(DOTSpell):

    def __init__(self,id, Potency):
        super().__init__(id, Potency)
        #Note that here Potency is the potency of the dot, not of the ability
        self.DOTTimer = 0   #This represents the timer of the dot, and it will apply at each 3 seconds
        self.WeaponSkill = False

#Autos
Autos = NinjaDOT(-1, 100)

#Special
Hide = NinjaSpell(16, False, False, 0, 0, 0, 0, ApplyHide, [])





#########################################
########## SCHOLAR PLAYER ###############
#########################################

ScholarGCD = 2.5
ScholarCast = 1.5

class ScholarSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)
        
        
def ApplyBiolysis(Player, Enemy):
    if (not (Player.Biolysis in Player.DOTList)):
        Player.Biolysis = copy.deepcopy(BiolysisDOT)
        Player.DOTList.append(Player.Biolysis)
        Player.EffectCDList.append(CheckBiolysis)
    Player.BiolysisTimer = 30

def ApplyAetherflow(Player, Enemy):
    Player.Mana = min(10000, Player.Mana + 2000)
    Player.AetherFlowStack = 3
    Player.AetherFlowCD = 60

def ApplyChainStratagem(Player, Enemy):
    Player.ChainStratagemCD = 120
    Player.ChainStratagemTimer = 15
    Enemy.ChainStratagem = True
    Player.EffectCDList.append(CheckChainStratagem)

def ApplyEnergyDrain(Player, Enemy):
    Player.EnergyDrainCD = 1
    Player.AetherFlowStack -= 1

def ApplyDissipation(Player, Enemy):
    Player.DissipationCD = 180
    Player.AetherFlowStack = 3
#====================================

def AetherflowRequirement(Player, Spell):
    return Player.AetherFlowCD <= 0

def ChainStratagemRequirement(Player, Spell):
    return Player.ChainStratagemCD <= 0

def AetherStackRequirement(Player, Spell):
    return Player.AetherFlowStack > 0

def DissipationRequirement(Player, Spell):
    return Player.DissipationCD <= 0
#====================================

def CheckChainStratagem(Player, Enemy):
    if Player.ChainStratagemTimer <= 0:
        Player.ChainStratagemTimer = 0
        Enemy.ChainStratagem = False
        Player.EffectCDList.remove(CheckChainStratagem)

def CheckBiolysis(Player, Enemy):
    if Player.BiolysisTimer <= 0 : 
        Player.DOTList.remove(Player.Biolysis)
        Player.Biolysis = None
        Player.EffectCDList.remove(CheckBiolysis)

Broil = ScholarSpell(1, True, ScholarCast, ScholarGCD, 295,  400, empty, [ManaRequirement])
Ruin = ScholarSpell(2, True, 0, ScholarGCD, 220,  400, empty, [ManaRequirement])
Biolysis = ScholarSpell(3, True, 0, ScholarGCD, 0, 400, ApplyBiolysis, [ManaRequirement])
BiolysisDOT = DOTSpell(4, 70)
Aetherflow = ScholarSpell(5, False, 0, Lock, 0, 0, ApplyAetherflow, [AetherflowRequirement])
Dissipation = ScholarSpell(8, False, 0, Lock, 0, 0, ApplyDissipation, [DissipationRequirement])
ChainStratagem = ScholarSpell(6, False, 0, Lock, 0, 0, ApplyChainStratagem, [ChainStratagemRequirement])
EnergyDrain = ScholarSpell(7, False, 0, Lock, 100, 0, ApplyEnergyDrain, [AetherStackRequirement])

#########################################
########## REDMAGE PLAYER ###############
#########################################


class RedmageSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, BlackCost, WhiteCost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.BlackCost = BlackCost
        self.WhiteCost = WhiteCost
#Special

def Addmana(Player, WhiteMana, BlackMana):
    Player.WhiteMana = min(100, Player.WhiteMana + WhiteMana)
    Player.BlackMana = min(100, Player.BlackMana + BlackMana)

def Removemana(Player, WhiteMana, BlackMana):
    Player.WhiteMana = max(0, Player.WhiteMana - WhiteMana)
    Player.BlackMana = max(0, Player.BlackMana - BlackMana)

#Requirement
def RDMManaRequirement(Player, Spell):
    return Spell.ManaCost <= Player.Mana and Spell.BlackCost <= Player.BlackMana and Spell.WhiteCost <= Player.WhiteMana

def ManaficationRequirement(Player, Spell):
    return Player.ManaficationCD <= 0

def EmboldenRequirement(Player, Spell):
    return Player.EmboldenCD <= 0

def AccelerationRequirement(Player, Spell):
    return Player.AccelerationStack >= 1

def FlecheRequirement(Player, Spell):
    return Player.FlecheCD <= 0

def ContreRequirement(Player, Spell):
    return Player.ContreCD <= 0

def EngagementRequirement(Player, Spell):
    return Player.EngagementStack > 0

def CorpsRequirement(Player, Spell):
    return Player.CorpsStack > 0

#Combo Action Requirements

def ZwerchhauRequirement(Player, Spell):
    return Player.Zwerchhau

def RedoublementRequirement(Player, Spell):
    return Player.Redoublement

def VerholyRequirement(Player, Spell):
    return Player.Verholy

def ScorchRequirement(Player, Spell):
    return Player.Scorch

def ResolutionRequirement(Player, Spell):
    return Player.Resolution



#Apply

def ApplyJolt(Player, Enemy):
    Addmana(Player, 2, 2)

def ApplyVerfire(Player, Enemy):
    Addmana(Player, 0, 5)

def ApplyVerstone(Player,Enemy):
    Addmana(Player, 5, 0)

def ApplyVerareao(Player, Enemy):
    Addmana(Player, 6, 0)

def ApplyVerthunder(Player, Enemy):
    Addmana(Player, 0, 6)

def ApplyManafication(Player, Enemy):
    Player.ManaficationStack = 6
    Player.ManaficationCD = 110
    Player.EffectList.insert(0,ManaficationEffect)
    Addmana(Player, 50, 50)

def ApplyEmbolden(Player, Enemy):
    Enemy.Bonus *= 1.05 #5% DPS boost for everyone. I put buff on Boss, but could put it on every other player
    Player.EmboldenTimer = 20
    Player.EmboldenCD = 120
    Player.EffectCDList.append(EmboldenCheck)

def ApplyAcceleration(Player, Enemy):
    if Player.AccelerationStack == 2:
         Player.AccelerationCD = 55
         Player.EffectCDList.append(AccelerationStackCheck)
    Player.EffectList.insert(0,AccelerationEffect)
    Player.AccelerationStack -= 1

def ApplyFleche(Player, Enemy):
    Player.FlecheCD = 25

def ApplyContre(Player, Enemy):
    Player.ContreCD = 35

def ApplyEngagement(Player, Enemy):
    if Player.EngagementStack == 2:
        Player.EngagementCD = 35
        Player.EffectCDList.append(EngagementStackCheck)
    Player.EngagementStack -= 1

def ApplyCorps(Player, Enemy):
    if Player.CorpsStack == 2:
        Player.CorpsCD = 35
        Player.EffectCDList.append(CorpsStackCheck)
    Player.CorpsStack -= 1




#Combo Action Apply

def ApplyRiposte(Player, Enemy):
    Removemana(Player, 20, 20)
    Player.Zwerchhau = True

def ApplyZwerchhau(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.Redoublement = True
    Player.Zwerchhau = False

def ApplyRedoublement(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.Verholy = True
    Player.Redoublement = False

def ApplyVerholy(Player, Enemy):
    Addmana(Player, 11, 0)
    Player.Scorch = True
    Player.Verholy = False

def ApplyScorch(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = True
    Player.Scorch = False

def ApplyResolution(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = False


#Effect

def DualCastEffect(Player, Spell):
    if Spell.CastTime != 0 and  Spell.GCD and Spell.id != -1:   #Want to make sure the spell will affect Dualcast, id != -1 is to make sure this is not WaitAbility
        #print("Spell satisfies DualCast")
        #print("Spell is : " + str(Spell.id))
        #print("CastTime : " + str(Spell.CastTime))
        if Player.DualCast:
            Spell.CastTime = 0 #Insta cast half of the spells, will be put by default for RedMage
            Player.DualCast = False #Remove Dualcast
        else: Player.DualCast = True    #Give Dual cast

def ManaficationEffect(Player, Spell):
    if Spell.GCD : #Only affect if GCD
        Player.ManaficationStack -= 1
        Spell.DPSBonus *= 1.05 #5% boost on magic damage
        if Player.ManaficationStack == 0: Player.EffectList.remove(ManaficationEffect)  #If no stack remove it

def AccelerationEffect(Player, Spell):
    if Spell.id == 3 and not (SwiftCastEffect in Player.EffectList): 
        Spell.CastTime = 0    #Will have to cast how this interacts with Dual cast
        Player.EffectList.remove(AccelerationEffect)

#Check

def EmboldenCheck(Player, Enemy):
    if Player.EmboldenTimer <= 0:
        Player.EmboldenTimer = 0
        Enemy.Bonus /= 1.05 #Removing 5% dps increase
        Player.EffectCDList.remove(EmboldenCheck)

def AccelerationStackCheck(Player, Enemy):
    if Player.AccelerationCD <= 0:
        Player.AccelerationStack += 1

        if Player.AccelerationStack == 2:
            Player.EffectCDList.remove(AccelerationStackCheck)
        else:
            Player.AccelerationCD = 55

def EngagementStackCheck(Player, Enemy):
    if Player.EngagementCD <= 0:
        Player.EngagementStack += 1

        if Player.EngagementStack == 2:
            Player.EffectCDList.remove(EngagementStackCheck)
        else:
            Player.EngagementCD = 35

def CorpsStackCheck(Player, Enemy):
    if Player.CorpsCD <= 0:
        Player.CorpsStack += 1

        if Player.CorpsStack == 2:
            Player.EffectCDList.remove(CorpsStackCheck)
        else:
            Player.CorpsCD = 35

Jolt = RedmageSpell(0, True, 2, 2.5,310, 200, ApplyJolt, [RDMManaRequirement], 0, 0 )
Verfire = RedmageSpell(1, True, 2, 2.5, 330, 200, ApplyVerfire, [RDMManaRequirement], 0, 0)
Verstone = RedmageSpell(2, True, 2, 2.5, 330, 200, ApplyVerstone, [RDMManaRequirement], 0, 0)
Verthunder = RedmageSpell(3, True, 5, 2.5, 380, 300, ApplyVerthunder, [RDMManaRequirement], 0, 0)
Verareo = RedmageSpell(3, True, 5, 2.5, 380, 300, ApplyVerareao, [RDMManaRequirement], 0, 0)

#All melee actions are assumed to be enchanted
#Combo actions
Riposte = RedmageSpell(4, True, 0, 1.5, 220, 0, ApplyRiposte, [RDMManaRequirement], 20,20)
Zwerchhau = RedmageSpell(5, True, 0, 1.5, 290, 0, ApplyZwerchhau, [RDMManaRequirement, ZwerchhauRequirement], 15, 15)
Redoublement = RedmageSpell(6, True, 0, 2.5, 470, 0, ApplyRedoublement, [RDMManaRequirement, RedoublementRequirement], 15, 15)
Verholy = RedmageSpell(7, True, 0, 2.5, 580, 400, ApplyVerholy, [RDMManaRequirement, VerholyRequirement], 0, 0)
Scorch = RedmageSpell(8, True, 0, 2.5, 680, 400, ApplyScorch, [RDMManaRequirement, ScorchRequirement], 0, 0)
Resolution = RedmageSpell(9, True, 0, 2.5, 750, 400, ApplyResolution, [RDMManaRequirement, ResolutionRequirement], 0, 0)

#For now combo action cannot be cancelled by doing something else

Manafication = RedmageSpell(10, False, 0, Lock, 0, 0, ApplyManafication, [ManaficationRequirement], 0, 0)
Embolden = RedmageSpell(11, False, 0, Lock, 0, 0, ApplyEmbolden, [EmboldenRequirement], 0, 0)
Acceleration = RedmageSpell(12, False, 0, Lock, 0, 0, ApplyAcceleration, [AccelerationRequirement], 0, 0)

Fleche = RedmageSpell(13, False, 0, Lock, 460, 0, ApplyFleche, [FlecheRequirement], 0, 0)
Contre = RedmageSpell(14, False, 0, Lock, 360, 0, ApplyContre, [ContreRequirement], 0, 0)
Engagement = RedmageSpell(15, False, 0, Lock, 180, 0, ApplyEngagement, [EngagementRequirement], 0, 0)
Corps = RedmageSpell(16, False, 0, Lock, 130, 0, ApplyCorps, [CorpsRequirement], 0, 0)

#########################################
########## MACHINIST SPELL  #############
#########################################


class MachinistSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, WeaponSkill):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.WeaponSkill = WeaponSkill #Boolean Variable

#Special

def AddGauge(Player, Battery, Heat):
    Player.BatteryGauge = min(100, Player.BatteryGauge + Battery)
    Player.HeatGauge = min(100, Player.HeatGauge + Heat)

def RemoveGauge(Player, Battery, Heat):
    Player.BatteryGauge = max(0, Player.BatteryGauge - Battery)
    Player.HeatGauge = max(0, Player.HeatGauge - Heat)
#Requirement

def WildFireRequirement(Player, Spell):
    return Player.WildFireCD <= 0

def AirAnchorRequirement(Player, Spell):
    return Player.AirAnchorCD <= 0

def BarrelStabilizerRequirement(Player, Spell):
    return Player.BarrelStabilizerCD <= 0

def HyperchargeRequirement(Player, Spell):
    return Player.HyperchargeCD <= 0 and Player.HeatGauge >= 50

def ReassembleRequirement(Player, Spell):
    return Player.ReassembleStack > 0

def GaussRoundRequirement(Player, Spell):
    return Player.GaussRoundStack > 0

def RicochetRequirement(Player, Spell):
    return Player.RicochetStack > 0

def DrillRequirement(Player, Spell):
    return Player.DrillCD <= 0

def OverdriveRequirement(Player, Spell):
    return Player.Overdrive

def ChainSawRequirement(Player, Spell):
    return Player.ChainSawCD <= 0

def AutomatonRequirement(Player, Spell):
    return (not Player.Overdrive) and Player.BatteryGauge >= 50

#Apply

def ApplyWildFire(Player, Enemy):
    Player.WildFireCD = 120
    Player.WildFireTimer = 10
    Player.EffectList.append(WildFireEffect)
    Player.EffectCDList.append(WildFireCheck)

def ApplyAirAnchor(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.AirAnchorCD = 40

def ApplyBarrelStabilizer(Player, Enemy):
    AddGauge(Player, 0, 50)
    Player.BarrelStabilizerCD = 120

def ApplyHeatBlast(Player, Enemy):
    Player.GaussRoundCD = max(0, Player.GaussRoundCD - 15)
    Player.RicochetCD = max(0, Player.RicochetCD - 15)

def ApplyHypercharge(Player, Enemy):
    Player.HyperchargeTimer = 8
    Player.HyperchargeCD = 10
    RemoveGauge(Player, 0, 50)#cost
    Player.EffectList.append(HyperchargeEffect)
    Player.EffectCDList.append(HyperchargeCheck)

def ApplyReassemble(Player, Enemy):
    if Player.ReassembleStack == 2:
        Player.EffectCDList.append(ReassembleStackCheck)
        Player.ReassembleCD = 55
    Player.ReassembleStack -= 1
    Player.Reassemble = True
    
def ApplyGaussRound(Player, Enemy):
    if Player.GaussRoundStack == 3:
        Player.EffectCDList.append(GaussRoundStackCheck)
        Player.GaussRoundCD = 30
    Player.GaussRoundStack -= 1

def ApplyRicochet(Player, Enemy):
    if Player.RicochetStack == 3:
        Player.EffectCDList.append(RicochetStackCheck)
        Player.RicochetCD = 30
    Player.RicochetStack -= 1

def ApplyDrill(Player, Enemy):
    Player.DrillCD = 20

def ApplyOverdrive(Player, Enemy):
    Player.Overdrive = False
    Player.Queen.ActionSet.insert(0,Collider)
    Player.Queen.ActionSet.insert(0,Bunker)

def ApplyChainSaw(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.ChainSawCD = 60

def ApplyAutomaton(Player, Enemy):
    Player.AutomatonQueenCD = 6
    RemoveGauge(Player, 50, 0)
    if Player.Queen == None : Queen(Player, 10)#Creating new queen
    #Will have to depend on battery Gauge
    #Timer is set at 10 so we can have 2 GCD to do finisher move if reaches before
    Player.Queen.EffectCDList.append(QueenCheck)
    Player.Queen.ActionSet.append(WaitAbility(10.5))

def ApplyCollider(Queen, Enemy):#Called on queen
    Queen.Master.QueenOnField = False

#Combo Actions

def ApplySplitShot(Player, Enemy):
    AddGauge(Player, 0, 5)
    Player.EffectList.append(SplitShotEffect)

def ApplySlugShot(Player, Enemy):
    AddGauge(Player, 0, 5)
    Player.EffectList.append(SlugShotEffect)

def ApplyCleanShot(Player, Enemy):
    AddGauge(Player, 10, 5)

#Effect

def WildFireEffect(Player, Spell):
    if isinstance(Spell, MachinistSpell) and Spell.WeaponSkill : Player.WildFireStack +=1

def HyperchargeEffect(Player, Spell):
    if Spell.WeaponSkill : Spell.Potency += 20

#Combo Actions effect

def SplitShotEffect(Player, Spell):
    if Spell.id == 5:

        Spell.Potency =+ 160
        Player.EffectList.remove(SplitShotEffect)

def SlugShotEffect(Player, Spell):
    if Spell.id == 6:

        Spell.Potency += 250
        Player.EffectList.remove(SlugShotEffect)


#Check

def WildFireCheck(Player, Enemy):
    if Player.WildFireTimer <= 0:

        WildFireOff = MachinistSpell(1, False, 0, 0, 150 * Player.WildFireStack, 0, empty, [], False)
        #Temporary Spell that will be put in front of the Queue
        Player.ActionSet.insert(Player.NextSpell+1, WildFireOff) #Insert in queue, will be instantly executed
        Player.WildFireStack = 0
        Player.EffectList.remove(WildFireEffect)
        Player.EffectCDList.remove(WildFireCheck)

def HyperchargeCheck(Player, Enemy):
    if Player.HyperchargeTimer <= 0:
        print("Hypercharge went off at : " + str(Player.CurrentFight.TimeStamp))
        Player.EffectList.remove(HyperchargeEffect)
        Player.EffectCDList.remove(HyperchargeCheck)

def ReassembleStackCheck(Player, Enemy):
    if Player.ReassembleCD <= 0:
        if Player.ReassembleStack == 1:
            Player.EffectCDList.remove(ReassembleStackCheck)
        else:
            Player.ReassembleCD = 55
        Player.ReassembleStack +=1

def GaussRoundStackCheck(Player, Enemy):
    if Player.GaussRoundCD <= 0:
        if Player.GaussRoundStack == 2:
            Player.EffectCDList.remove(GaussRoundStackCheck)
        else:
            Player.GaussRoundCD = 30
        Player.GaussRoundStack +=1

def RicochetStackCheck(Player, Enemy):
    if Player.RicochetCD <= 0:
        if Player.RicochetStack == 2:
            Player.EffectCDList.remove(RicochetStackCheck)
        else:
            Player.RicochetCD = 30
        Player.RicochetStack +=1

def QueenCheck(Player, Enemy):#This will be called on the queen
    if Player.Timer <= 0: 
        Player.Master.Overdrive = False
        Player.ActionSet.insert(Player.NextSpell+1,Bunker)
        Player.ActionSet.insert(Player.NextSpell+2,Collider)
        Player.EffectCDList.remove(QueenCheck)

Wildfire = MachinistSpell(0, False, 0, Lock, 0, 0, ApplyWildFire, [WildFireRequirement], False)
AirAnchor = MachinistSpell(2, True, 0, 2.5, 570, 0, ApplyAirAnchor, [AirAnchorRequirement], True)
BarrelStabilizer = MachinistSpell(3, False, 0, Lock, 0, 0, ApplyBarrelStabilizer, [BarrelStabilizerRequirement], False)
HeatBlast = MachinistSpell(7, True, Lock, 1.5, 170, 0, ApplyHeatBlast, [], True)
Hypercharge = MachinistSpell(8, False, 0, Lock, 0, 0, ApplyHypercharge, [HyperchargeRequirement], False)
Reassemble = MachinistSpell(9, False, 0, Lock, 0, 0, ApplyReassemble, [ReassembleRequirement], False)
GaussRound = MachinistSpell(10, False, 0, Lock, 120, 0, ApplyGaussRound, [GaussRoundRequirement], False)
Ricochet = MachinistSpell(11, False, 0, Lock, 120, 0, ApplyRicochet, [RicochetRequirement], False)
Drill = MachinistSpell(12, True, 0, 2.5, 570, 0, ApplyDrill, [DrillRequirement], True)
ChainSaw = MachinistSpell(17, True, 0, 2.5, 570, 0, ApplyChainSaw, [ChainSawRequirement], True)
#Combo Action

SplitShot = MachinistSpell(4, True, Lock, 2.5, 200, 0, ApplySplitShot, [], True)
SlugShot = MachinistSpell(5, True, Lock, 2.5, 120, 0, ApplySlugShot, [], True )
CleanShot = MachinistSpell(6, True, Lock, 2.5, 110, 0, ApplyCleanShot, [], True)


#Queen's Ability

#These abilities will write into the Queen's ability list.
#If they are not done the queen will do them automatically
Automaton = MachinistSpell(14, False, 0, Lock, 0, 0, ApplyAutomaton, [AutomatonRequirement], False)
Overdrive = MachinistSpell(13, False, 0, Lock, 0, 0, ApplyOverdrive, [OverdriveRequirement], False)
#These will be casted by the machinist, so they have no damage. Their only effect is to add into Queen's Queue
Bunker = MachinistSpell(15, True, 0, 2.5, 650, 0, empty, [], False)   #Triggered by Overdrive
Collider = MachinistSpell(16, True, 0 , 2.5, 750, 0, ApplyCollider, [], False)  #Spell Queen will cast



#########################################
########## WARRIOR Spell  ###############
#########################################

def BeastGaugeRequirement(Player, Spell):
    RemoveBeast(Player, Spell.Cost)
    return Player.BeastGauge >= 0

class WarriorSpell(Spell):

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement, Cost):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

        self.Requirement += [BeastGaugeRequirement] 
        self.Cost = Cost

#Special

def AddBeast(Player, Gauge):
    Player.BeastGauge = min(100, Player.BeastGauge + Gauge)

def RemoveBeast(Player, Gauge):
    Player.BeastGauge -= Gauge #Caanot go under 0 cuz verify if enough gauge

#Requirement

def UpheavalRequirement(Player, Spell):
    return Player.UpheavalCD == 0

def OnslaughtRequirement(Player, Spell):
    return Player.OnslaughtStack >= 1

def InfuriateRequirement(Player, Spell):
    return Player.InfuriateStack >= 1

def InnerReleaseRequirement(Player, Spell):
    return Player.InnerReleaseCD == 0

def PrimalRendRequirement(Player, Spell):
    return Player.PrimalRendTimer > 0

def FellCleaveRequirement(Player, Spell):
    return Player.BeastGauge >= 50

def InnerChaosRequirement(Player, Spell):
    return Player.NascentChaosTimer > 0

#Apply

def ApplyHeavySwing(Player, Enemy):
    if not (HeavySwingEffect in Player.EffectList) : Player.EffectList.append(HeavySwingEffect)

def ApplyMaim(Player, Enemy):
    if not (MaimEffect in Player.EffectList) : Player.EffectList.append(MaimEffect)
    AddBeast(Player, 10)

def ApplyStormEye(Player, Enemy):
    Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 30)
    AddBeast(Player, 10)

def ApplyStormPath(Player, Enemy):
    AddBeast(Player, 20)

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
    Player.InnerReleaseStack += 1 #To allow for Direct Crit
    Player.PrimalRendTimer = 0

def ApplyInnerChaos(Player, Enemy):
    Player.InnerReleaseStack += 1
    Player.InfuriateCD = max(0, Player.InfuriateCD - 5)
    Player.NascentChaosTimer = 0

#Effect

def InnerReleaseEffect(Player, Spell):
    if isinstance(Spell, WarriorSpell) and Spell.Cost != 0:
        Player.NoBeastCostStack -= 1
        Spell.Cost = 0
        if Player.NoBeastCostStack == 0: Player.EffectList.remove(InnerReleaseEffect)

def SurgingTempestEffect(Player, Spell):
    if Player.SurgingTempestTimer > 0 : 
        Player.MultDPSBonus *= 1.1
        Player.EffectCDList.append(SurgingTempestCheck)
        Player.EffectList.remove(SurgingTempestEffect)

#Combo Action

def HeavySwingEffect(Player, Spell):
    if Spell.id == 2:
        Spell.Potency += 150
        Player.EffectList.remove(HeavySwingEffect)

def MaimEffect(Player, Spell):
    if Spell.id == 3 or Spell.id == 11:
        Spell.Potency += 280
        Player.EffectList.remove(MaimEffect)


#Check

def SurgingTempestCheck(Player, Enemy):
    if Player.SurgingTempestTimer <= 0: 
        Player.MultDPSBonus /= 1.1
        Player.EffectList.append(SurgingTempestEffect)
        Player.EffectCDList.remove(SurgingTempestCheck)

def OnslaughtStackCheck(Player, Enemy):
    if Player.OnslaughtCD <= 0:
        if Player.OnslaughtStack == 2:
            Player.EffectCDList.remove(OnslaughtStackCheck)
        else:
            Player.OnslaughtCD = 30
        Player.OnslaughtStack += 1

def InfuriateStackCheck(Player, Enemy):
    if Player.InfuriateCD <= 0:
        if Player.InfuriateStack == 1:
            Player.EffectCDList.remove(InfuriateStackCheck)
        else:
            Player.InfuriateCD = 30
        Player.InfuriateStack += 1
    

#Combo Action
HeavySwing = WarriorSpell(1, True, Lock, 2.5, 200, 0, ApplyHeavySwing, [],0)
Maim = WarriorSpell(2, True, Lock, 2.5, 130, 0, ApplyMaim, [],0)
StormEye = WarriorSpell(3, True, Lock, 2.5, 120, 0, ApplyStormEye, [],0)
StormPath = WarriorSpell(11, True, Lock, 2.5, 120, 0, ApplyStormPath, [], 0)
#Missing Storm's path

#oGCD
Upheaval = WarriorSpell(4, False, Lock, 0, 350, 0, ApplyUpheaval, [UpheavalRequirement],0)
Onslaught = WarriorSpell(5, False, Lock, 0, 150, 0, ApplyOnslaught, [OnslaughtRequirement],0)
Infuriate = WarriorSpell(6, False, Lock, 0, 0, 0, ApplyInfuriate, [InfuriateRequirement],0)
InnerRelease = WarriorSpell(7, False, Lock, 0, 0, 0, ApplyInnerRelease, [InnerReleaseRequirement],0)


#GCD
PrimalRend = WarriorSpell(8, True, Lock, 2.5, 700, 0, ApplyPrimalRend, [PrimalRendRequirement],0)
FellCleave = WarriorSpell(9, True, Lock, 2.5, 460, 0, empty, [],50)
InnerChaos = WarriorSpell(10, True, Lock, 2.5, 650,0, ApplyInnerChaos, [InnerChaosRequirement], 50)
Tomahawk = WarriorSpell(12, True, Lock, 2.5, 150, 0, empty, [], 0)


#########################################
########## WHITEMAGE PLAYER #############
#########################################


class WhitemageSpell(Spell):
    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement)

#Requirement

def PresenceOfMindRequirement(Player, Spell):
    return Player.PresenceOfMindCD <= 0

def AssizeRequirement(Player, Spell):
    return Player.AssizeCD <= 0

def ThinAirRequirement(Player, Spell):
    return Player.ThinAirCD <= 0

#Apply

def ApplyDia(Player, Enemy):
    Player.DiaTimer = 30

    if (Player.Dia == None) : 
        Player.Dia = copy.deepcopy(DiaDOT)
        Player.EffectCDList.append(CheckDia)
        Player.DOTList.append(Player.Dia)

def ApplyAssize(Player, Enemy):
    Player.Mana = min(10000, Player.Mana + 500)
    Player.AssizeCD = 45

def ApplyThinAir(Player, Enemy):
    Player.ThinAirCD = 60
    Player.EffectList.append(ThinAirEffect)

def ApplyPresenceOfMind(Player, Enemy):
    Player.PresenceOfMindCD = 120
    Player.PresenceOfMindTimer = 15
    Player.EffectList.append(PresenceOfMindEffect)
    Player.EffectCDList.append(CheckPresenceOfMind)

#Effect

def ThinAirEffect(Player, Spell):
    Spell.ManaCost = 0
    Player.EffectList.remove(ThinAirEffect)

def PresenceOfMindEffect(Player, Spell):
    Spell.CastTime *= 0.8
    Spell.RecastTime *= 0.8

#Check

def CheckDia(Player, Enemy):
    if Player.DiaTimer <= 0:
        Player.DOTList.remove(Player.Dia)
        Player.Dia = None
        Player.EffectCDList.remove(CheckDia)

def CheckPresenceOfMind(Player, Enemy):
    if Player.PresenceOfMindTimer <= 0:
        Player.EffectList.remove(PresenceOfMindEffect)
        Player.EffectCDList.remove(CheckPresenceOfMind)



#GCD
Glare = WhitemageSpell(0, True, 1.5, 2.5, 310, 400, empty, [])
Dia = WhitemageSpell(1, True, Lock, 2.5, 0, 400, ApplyDia, [])
DiaDOT = DOTSpell(5, 60)

#OGCD
Assize = WhitemageSpell(2, False, Lock, Lock, 400, 0, ApplyAssize, [AssizeRequirement])
ThinAir = WhitemageSpell(3, False, Lock, Lock, 0, 0, ApplyThinAir, [ThinAirRequirement])
PresenceOfMind = WhitemageSpell(4, False, Lock, Lock, 0, 0, ApplyPresenceOfMind, [PresenceOfMindRequirement])