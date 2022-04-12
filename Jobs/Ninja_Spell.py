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
    Enemy.Bonus *= 1.1
    Player.TrickAttackTimer = 15
    Player.EffectCDList.append(TrickAttackEffect)

def ApplyMug(Player, Enemy):
    Player.NinkiGauge = min(100, Player.NinkiGauge + 40)
    Player.MugCd = 120
    Player.MultDPSBonus *= 1.05
    Player.MugTimer = 20
    Player.EffectCDList.append(MugCheck)

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


def TrickAttackEffect(Player, Enemy):
    if(Player.TrickAttackTimer <= 0): 
        Player.EffectCDList.remove(TrickAttackEffect)
        Enemy.Bonus /= 1.1

def SpinningEdgeEffect(Player, Spell):
    if (Spell.id == 1):
        Spell.Potency = AddFlatBonus(140, Spell.Potency, 160)
        Player.NinkiGauge = min(100, Player.NinkiGauge + 5)
        Player.EffectList.remove(SpinningEdgeEffect)

def GustSlashEffect(Player,Spell):
    if (Spell.id == 2):
        Spell.Potency += 260
        Player.NinkiGauge = min(100, Player.NinkiGauge + 15)
        Player.EffectList.remove(GustSlashEffect)
    elif(Spell.id == 3):
        Spell.Potency += 240
        Player.NinkiGauge = min(100, Player.NinkiGauge + 15)
        Player.EffectList.remove(GustSlashEffect)

def AutoEffect(Player, Spell):
    Player.DOTList.append(Autos)
    Player.EffectList.remove(AutoEffect)



#Check

def MugCheck(Player, Enemy):
    if Player.MugTimer <= 0:
        Player.MultDPSBonus /= 1.05
        Player.EffectCDList.remove(MugCheck)


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
Bhavacakra = NinjaSpell(12, False,False, Lock, 0, 350,0, ApplyBhavacakra, [NinkiRequirement])
Meisui = NinjaSpell(13, False,False, Lock, 0, 0, 0, ApplyMeisui, [MeisuiRequirement])
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
Kamaitachi = NinjaSpell(15, False, True, 0, NinjaGCD, 600, 0, ApplyKamaitachi, [])

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