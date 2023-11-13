from ffxivcalc.Jobs.Base_Spell import DOTSpell, WaitAbility, buff, empty, buffPercentHistory
from ffxivcalc.Jobs.Melee.Melee_Spell import NinjaSpell
import copy

from ffxivcalc.Jobs.Player import Pet

Lock = 0.5


#Requirement

def ShadeShiftRequirement(Player, Spell):
    return Player.ShadeShiftCD <= 0, Player.ShadeShiftCD

def PhantomKamaitachiRequirement(Player, Spell):
    return Player.PhantomKamaitachiReady, -1

def BunshinRequirement(Player, Spell):
    return Player.BunshinCD <=0 and Player.NinkiGauge >= 50, Player.BunshinCD

def TenRequirement(Player, Spell):
    if Player.Ten :
        Player.Ten = False
        return True, -1
    return False, -1

def ChiRequirement(Player, Spell):
    return Player.Chi, -1

def JinRequirement(Player, Spell):
    return Player.Jin, -1

def TenChiJinRequirement(Player, Spell):
    return Player.TenChiJinCD <= 0 and not Player.Kassatsu, Player.TenChiJinCD

def KassatsuOnRequirement(Player, Spell):
    return Player.Kassatsu, -1

def KassatsuRequirement(Player, Spell):
    return Player.KassatsuCD <= 0, Player.KassatsuCD

def NinjutsuRequirement(Player, Spell):
    return Player.NinjutsuStack > 0 or Player.Kassatsu or len(Player.CurrentRitual) > 0, Player.NinjutsuCD

def FleetingRaijuRequirement(Player, Spell):
    return Player.RaijuStack > 0, -1

def MeisuiRequirement(Player, Spell):
    return Player.Suiton and Player.MeisuiCD <= 0, -1

def BhavacakraRequirement(Player, Spell):
    return Player.NinkiGauge >= 50, -1

def TrickAttackRequirement(Player, Spell):
    return Player.Suiton and Player.TrickAttackCD <= 0, -1

def MugRequirement(Player, Spell):
    return Player.MugCD <= 0, Player.MugCD

def DreamWithinADreamRequirement(Player, Spell):
    return Player.DreamWithinADreamCD <= 0, Player.DreamWithinADreamCD

def TenChiJinOnRequirement(Player, Spell): #TenChiJin Ninjutsu
    return Player.TenChiJinTimer > 0, -1

#Ninjutsu Requirement

def FumaShurikenRequirement(Player, Spell):
    return Player.CurrentRitual == [0] or Player.CurrentRitual == [1] or Player.CurrentRitual == [2], -1

def RaitonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,1] or Player.CurrentRitual == [2,1], -1

def KatonRequirement(Player, Spell):
    return Player.CurrentRitual == [1,0] or Player.CurrentRitual == [2,0], -1

def HyotonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,2] or Player.CurrentRitual == [1,2], -1

def HutonRequirement(Player, Spell):
    return Player.CurrentRitual == [2,1,0] or Player.CurrentRitual == [1,2,0], -1

def DotonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,2,1] or Player.CurrentRitual == [2,0,1], -1

def SuitonRequirement(Player, Spell):
    return Player.CurrentRitual == [0,1,2] or Player.CurrentRitual == [1,0,2], -1


#Apply

def ApplyDeathBlossom(Player, Enemy):
    if not (DeathBlossomCombo in Player.EffectList) : Player.EffectList.append(DeathBlossomCombo)
    Player.AddNinki(5)

def ApplyShadeShift(Player, Enemy):
    Player.ShadeShiftCD = 120

def ApplyDoton(Player, Enemy):
    Player.ResetRitual()
    Player.DotonTimer = 18
    Player.DotonDOT = copy.deepcopy(DotonDOT)
    Player.DOTList.append(Player.DotonDOT)
    Player.EffectCDList.append(DotonCheck)

def ApplyTen(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(0) #0 is a Ten

def ApplyChi(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(1) #1 is a Chi

def ApplyJin(Player, Enemy):
    ApplyNinjutsu(Player, Enemy)
    Player.CurrentRitual.append(2) #2 is a Jin

def ApplyHide(Player, Enemy):
    Player.NinjutsuStack = 2
    if Player.NinjutsuCD > 0:
        Player.EffectCDList.remove(NinjutsuStackCheck)
        Player.NinjutsuCD = 0

def ApplyPhantomKamaitachi(Player, Enemy):

    if Player.Pet == None: #If no Shadow, we will create a new one
        Player.Pet = Pet(Player) # Creating an object
        Player.Pet.ActionSet.append(WaitAbility(0.01)) #Adding an action so program does not crash

    Player.PhantomKamaitachiReady = False
    #Will give Action to the Shadow
    Shadow = Player.Pet
    Shadow.TrueLock = False #Delocking the shadow
    Shadow.ActionSet.insert(Shadow.NextSpell + 1, PhantomKamaitachiShadow) #Adding the spell
    Player.AddHuton(10)
    Player.AddNinki(10)

def ApplyBunshin(Player, Enemy):
    Player.AddNinki(-50)
    Player.BunshinCD = 90
    Player.BunshinStack = 5

    if Player.Pet == None: #If no Shadow, we will create a new one
        Player.Pet = Pet(Player) # Creating an object
        Player.Pet.ActionSet.append(WaitAbility(0.01)) #Adding an action so program does not crash
    else:
        Player.Pet.ResetStat() # Reseting stat on the summon

    Player.EffectList.append(BunshinEffect)
    Player.PhantomKamaitachiReady = True
    Player.PhantomKamaitachiReadyTimer = 45
    Player.EffectCDList.append(PhantomKamaitachiCheck)

def ApplyTenChiJin(Player, Enemy):
    Player.TenChiJinCD = 120
    Player.TenChiJinTimer = 6
    Player.EffectCDList.append(TenChiJinCheck)
    Player.EffectList.append(TenChiJinEffect)

def ApplyKassatsu(Player, Enemy):
    Player.KassatsuTimer = 15
    Player.KassatsuCD = 60
    Player.Kassatsu = True
    Player.EffectList.append(KassatsuEffect)
    Player.EffectCDList.append(KassatsuCheck)

def ApplyHyoshoRanryu(Player, Enemy):
    Player.ResetRitual()

def ApplySuiton(Player, Enemy):
    Player.Suiton = True
    if not SuitonCheck in Player.EffectCDList : Player.EffectCDList.append(SuitonCheck)
    Player.SuitonTimer = 20
    Player.ResetRitual() #Even if in TenChiJin, does not matter

def ApplyHuton(Player, Enemy):
    Player.HutonTimer = 60
    if not (HutonEffect in Player.EffectList):
        Player.EffectList.append(HutonEffect)
    if not (HutonCheck in Player.EffectCDList):
        Player.Haste += 15
        Player.hasteChangeValue = 15
        Player.hasteHasChanged = True
        Player.EffectCDList.append(HutonCheck)
    Player.ResetRitual() #Even if in TenChiJin, does not matter

def ApplyRaiton(Player, Enemy):
    if Player.RaijuStack == 0: Player.EffectList.append(RaitonEffect) #will loose all if weaponskill is done
    Player.RaijuStack = min(3, Player.RaijuStack + 1)
    Player.ResetRitual() #Even if in TenChiJin, does not matter

def ApplyNinjutsu(Player, Enemy):
    if len(Player.CurrentRitual) == 0 and not Player.Kassatsu: #If we are not already in a ritual
        if Player.NinjutsuStack == 2:
            Player.EffectCDList.append(NinjutsuStackCheck)
            Player.NinjutsuCD = 20
        Player.NinjutsuStack -= 1

def ApplyThrowingDagger(Player, Enemy):
    Player.AddNinki(5)

def ApplyFleetingRaiju(Player, Enemy):
    Player.RaijuReady = False
    Player.RaijuStack -= 1
    Player.AddNinki(5)
    

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
    Player.TrickAttackCD = 60
    Player.TrickAttackTimer = 15
    Player.EffectCDList.append(TrickAttackCheck)
    Player.buffList.append(TrickAttackBuff)
    Player.Suiton = False

                             # Only relevant to PreBakedAction and only does that code if true. Also checking if the PreBakedAction player is this ninja
    #if Player.CurrentFight.SavePreBakedAction and Player == Player.CurrentFight.PlayerList[Player.CurrentFight.PlayerIDSavePreBakedAction]:
    #    fight = Player.CurrentFight
    #    history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 15, TrickAttackBuff.MultDPS)
    #    history.isTrickAttack = True
    #    fight.PlayerList[fight.PlayerIDSavePreBakedAction].PercentBuffHistory.append(history)

def ApplyMug(Player, Enemy):
    Player.MugCD = 120
    Player.MugTimer = 20
    Player.AddNinki(40)
    Player.EffectCDList.append(MugCheck)
    Enemy.buffList.append(MugBuff)

    # Only relevant to PreBakedAction and only does that code if true
    #if Player.CurrentFight.SavePreBakedAction:
    #    fight = Player.CurrentFight
    #    history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20, MugBuff.MultDPS)
    #    fight.PlayerList[fight.PlayerIDSavePreBakedAction].PercentBuffHistory.append(history)

def ApplyHuraijin(Player, Enemy):
    Player.HutonTimer = 60

def ApplyDreamWithinADream(Player, Enemy):
    Player.DreamWithinADreamCD = 60

def ApplySpinningEdge(Player, Enemy):
    ##input(Player.EffectList)
    Player.AddNinki(5)
    
    if not (SpinningEdgeCombo in Player.EffectList): Player.EffectList.append(SpinningEdgeCombo)


#Effect

def DeathBlossomCombo(Player, Spell):
    if Spell.id == HakkeMujinsatsu.id:
        Spell.Potency += 30
        Player.AddHuton(10)
        Player.AddNinki(5)
        Player.EffectToRemove.append(DeathBlossomCombo)

def TenChiJinEffect(Player, Spell):
    if Spell.id == Ten2.id or Spell.id == Chi2.id or Spell.id == Jin2.id: #If not one of these spells, we simply stop

        if Spell.id == Ten2.id:
            Player.TenChiJinRitual += [0] #Ten is 0
        elif Spell.id == Chi2.id:
            Player.TenChiJinRitual += [1] #Chi is 1
        elif Spell.id == Jin2.id:
            Player.TenChiJinRitual += [2] #Jin is 2

        #We will now check how we change the action

        if len(Player.TenChiJinRitual) == 1: #We will execute FumaShuriken
            Spell.Potency += FumaShuriken.Potency #Giving Potency as a bonus in case some other effect gave flat potency (shouldn't be the case for Ninja)
            #No notable effect to give
        elif len(Player.TenChiJinRitual) == 2:

            if Player.TenChiJinRitual == [0,1] or Player.TenChiJinRitual == [2,1]: # Raiton : Ten -> Chi or Jin -> Chi
                Spell.Potency += Raiton.Potency
                Spell.Effect = Raiton.Effect
            elif Player.TenChiJinRitual == [0, 2] or Player.TenChiJinRitual == [1,2]: # hyoton : Ten -> Jin or Chi -> Jin
                Spell.Potency += Hyoton.Potency
                #No notable effect to give
            elif Player.TenChiJinRitual == [1,0] or Player.TenChiJinRitual == [2,0]: # Katon : Chi -> Ten or Jin -> Ten
                Spell.Potency += Katon.Potency
                #No notable effect to give
            #Else, we change nothing and its going to bunny lol
        
        elif len(Player.TenChiJinRitual) == 3:

            if Player.TenChiJinRitual == [0,1,2] or Player.TenChiJinRitual == [1,0,2]: # Suiton : Ten -> Chi -> Jin or Chi -> Ten -> Jin
                Spell.Potency += Suiton.Potency
                Spell.Effect = Suiton.Effect
                Spell.RecastTime += 0.5
            elif Player.TenChiJinRitual == [2,1,0] or Player.TenChiJinRitual == [1,2,0]: # Huton : Jin -> Chi -> Ten or Chi -> Jin -> Ten
                Spell.Potency = 0
                Spell.Effect = Huton.Effect
            elif Player.TenChiJinRitual == [0,2,1] or Player.TenChiJinRitual == [2,0,1]: # Doton : Ten -> Jin -> Chi or Jin -> Ten -> Chi
                Spell.Potency = 0
                Spell.Effect = Doton.Effect

            #Since last possible Ninjutsu, we will set TenChiJin Timer to 0.01 so it terminates
            Player.TenChiJinTimer = 0.01
            Player.TenChiJinRitual = [] #Reseting TenChiJin Ritual
            #input("Finishing")
            #Effect will be removed in Check

            


    elif not (isinstance(Spell, DOTSpell)): #If not a DOTSpell
        Player.TenChiJinTimer = 0


def HutonEffect(Player, Spell):
    pass
        # Why did I do that? Left for future me to figure out
    #if isinstance(Spell, NinjaSpell) and Spell.Weaponskill and Spell.GCD : Spell.RecastTime *= 0.85

def BunshinEffect(Player, Spell):
    if isinstance(Spell, NinjaSpell) and Spell.Weaponskill and Spell.id != PhantomKamaitachi.id: #We don't want Kamataichi to have bunshin effect
        #Will give Action to the Shadow
        Shadow = Player.Pet
        Shadow.TrueLock = False #Delocking the shadow
        Shadow.ActionSet.insert(Shadow.NextSpell + 1, NinjaSpell(35, False, 0, 1, 160, empty, [], True, False)) #Adding the spell
        Player.BunshinStack -= 1
        Player.AddNinki(5)
        if Player.BunshinStack == 0:
            Player.EffectToRemove.append(BunshinEffect)

def KassatsuEffect(Player, Spell):
    if isinstance(Spell, NinjaSpell) and Spell.Ninjutsu:
        Spell.DPSBonus = 1.3
        Player.KassatsuTimer = 0

def RaitonEffect(Player, Spell):
    if Spell.GCD and (Spell.Weaponskill or Player.RaijuStack == 0) and (Spell.id != FleetingRaiju.id and Spell.id != PhantomKamaitachi.id):
        Player.RaijuStack = 0
        Player.EffectToRemove.append(RaitonEffect)

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

def DotonCheck(Player, Enemy):
    if Player.DotonTimer <= 0:
        Player.DOTList.remove(Player.DotonDOT)
        Player.DotonDOT = None
        Player.EffectToRemove.append(DotonCheck)

def HutonCheck(Player, Enemy):
    if Player.HutonTimer <= 0:
        Player.EffectList.remove(HutonEffect)
        Player.EffectToRemove.append(HutonCheck)
        Player.Haste -= 15
        Player.hasteChangeValue = -15
        Player.hasteHasChanged = True

def PhantomKamaitachiCheck(Player, Enemy):
    if not Player.PhantomKamaitachiReady or Player.PhantomKamaitachiReadyTimer <= 0:
        Player.PhantomKamaitachiReady = False
        Player.PhantomKamaitachiReadyTimer = 0
        Player.EffectToRemove.append(PhantomKamaitachiCheck)

def SuitonCheck(Player, Enemy):
    if not Player.Suiton or Player.SuitonTimer <= 0:
        Player.EffectToRemove.append(SuitonCheck)
        Player.SuitonTimer = 0
        Player.Suiton = False

def KassatsuCheck(Player, Enemy):
    if Player.KassatsuTimer <= 0:
        Player.EffectList.remove(KassatsuEffect)
        Player.EffectToRemove.append(KassatsuCheck)
        Player.Kassatsu = False

def NinjutsuStackCheck(Player, Enemy):
    if Player.NinjutsuCD <= 0:
        if Player.NinjutsuStack == 1:
            Player.EffectToRemove.append(NinjutsuStackCheck)
        else:
            Player.NinjutsuCD = 20
        Player.NinjutsuStack +=1

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

def TenChiJinCheck(Player, Enemy):
    if Player.TenChiJinTimer <= 0:
        Player.EffectList.remove(TenChiJinEffect)
        Player.EffectToRemove.append(TenChiJinCheck)



#GCD
SpinningEdge = NinjaSpell(2240, True, Lock, 2.5, 220, ApplySpinningEdge, [], True, False, type = 2)
GustSlash = NinjaSpell(2242, True, Lock, 2.5, 160, empty, [], True, False, type = 2)
AeolianEdge = NinjaSpell(2255, True, Lock, 2.5, 200, empty, [], True, False, type = 2)
ArmorCrush = NinjaSpell(3563, True, Lock, 2.5, 200, empty, [], True, False, type = 2)
Huraijin = NinjaSpell(25876, True, Lock, 2.5, 200, ApplyHuraijin, [], True, False, type = 2)
FleetingRaiju = NinjaSpell(25777, True, Lock, 2.5, 560, ApplyFleetingRaiju, [FleetingRaijuRequirement], True, False, type = 2)
ThrowingDagger = NinjaSpell(2247, True, Lock, 2.5, 120, ApplyThrowingDagger, [], True, False, type = 2)
PhantomKamaitachi = NinjaSpell(25774, True, Lock, 2.5, 0, ApplyPhantomKamaitachi, [PhantomKamaitachiRequirement], True, False, type = 2)
PhantomKamaitachiShadow = NinjaSpell(8, False, 0, 0, 600, empty, [], False, False) #Action done by the shadow
DeathBlossom = NinjaSpell(2254, True, Lock, 2.5, 100, ApplyDeathBlossom, [],True, False, type = 2)
HakkeMujinsatsu = NinjaSpell(16488, True, Lock, 2.5, 100, empty, [], True, False, type = 2)

#Ninjutsu
FumaShuriken = NinjaSpell(2265, True, Lock,1.5, 450, ApplyHyoshoRanryu, [FumaShurikenRequirement], False, True) #Same effect as HyoshoRanruy, since only reset Player.CurrentRitual list
Raiton = NinjaSpell(2267, True, Lock,1.5, 650, ApplyRaiton, [RaitonRequirement], False, True )
Huton = NinjaSpell(2269, True, Lock,1.5, 0, ApplyHuton, [HutonRequirement], False, True)
Suiton = NinjaSpell(2271, True, Lock,1.5, 500, ApplySuiton, [SuitonRequirement], False, True)
Hyoton = NinjaSpell(2268, True, Lock, 1.5, 350, ApplyHyoshoRanryu, [HyotonRequirement], False, True)
HyoshoRanryu = NinjaSpell(16492, True, Lock,1.5, 1300, ApplyHyoshoRanryu, [HyotonRequirement, KassatsuOnRequirement], False, True)
Katon = NinjaSpell(2266, True, Lock, 1.5, 350, ApplyHyoshoRanryu, [KatonRequirement], False, True)
GokaMekkyaku = NinjaSpell(16491, True, Lock, 1.5, 600, ApplyHyoshoRanryu, [KatonRequirement, KassatsuOnRequirement], False, True)
Doton = NinjaSpell(2270, True, Lock, 1.5, 0, ApplyDoton, [DotonRequirement], False, True)
DotonDOT = DOTSpell(-33, 80, True)

#Ritual
Ten = NinjaSpell(2259, True, 0, 0.5, 0, ApplyTen, [NinjutsuRequirement], False, False)
Chi = NinjaSpell(2261, True, 0, 0.5, 0, ApplyChi, [NinjutsuRequirement], False, False)
Jin = NinjaSpell(2263, True, 0, 0.5, 0, ApplyJin, [NinjutsuRequirement], False, False)

#TenChiJin
TenChiJin = NinjaSpell(7403, False, Lock, 0, 0, ApplyTenChiJin, [TenChiJinRequirement], False, False)
#TenChiJin will trigger the TenChiJinEffect. The actions we can take will be different from the Ninjutsu
Ten2 = NinjaSpell(18873, True, Lock, 1, 0, empty, [TenChiJinOnRequirement], False, True)
Chi2 = NinjaSpell(18877, True, Lock, 1, 0, empty, [TenChiJinOnRequirement], False, True)
Jin2 = NinjaSpell(18881, True, Lock, 1, 0, empty, [TenChiJinOnRequirement], False, True) 
#These Ninjutsu are only to be used in TenChiJin
#Their potency/apply will be changed according to what spell should be casted

#oGCD
DreamWithinADream = NinjaSpell(3566, False, Lock, 0, 3*150, ApplyDreamWithinADream, [DreamWithinADreamRequirement], False, False)
Mug = NinjaSpell(2248, False, Lock, 0, 150, ApplyMug, [MugRequirement], False, False)
TrickAttack = NinjaSpell(2258, False, Lock, 0, 400, ApplyTrickAttack, [TrickAttackRequirement], False, False)
Bhavacakra = NinjaSpell(7402, False, Lock, 0, 350, ApplyBhavacakra, [BhavacakraRequirement], False, False)
Meisui = NinjaSpell(16489, False, Lock, 0, 0, ApplyMeisui, [MeisuiRequirement], False, False)
Kassatsu = NinjaSpell(2264, False, Lock, 0, 0, ApplyKassatsu,[KassatsuRequirement], False, False)
Bunshin = NinjaSpell(16493, False, Lock, 0, 0, ApplyBunshin, [BunshinRequirement], False, False)
Hide = NinjaSpell(2245, True, 0, 0, 0, ApplyHide, [], False, False)
ShadeShift = NinjaSpell(2241, False, Lock, 0, 0, ApplyShadeShift, [ShadeShiftRequirement], False, False)
HellfrogMedium = NinjaSpell(7401, False, Lock, 0, 160, ApplyBhavacakra, [BhavacakraRequirement], False, False)
#buff
MugBuff = buff(1.05,name="Mug")
TrickAttackBuff = buff(1.1,name="Trick Attack")


NinjaAbility = {
2240 : SpinningEdge,
2242 : GustSlash,
2255 : AeolianEdge,
3563 : ArmorCrush,
2247 : ThrowingDagger,
2241 : ShadeShift,
2254 : DeathBlossom,
16488 : HakkeMujinsatsu,
2245 : Hide,
2248 : Mug,
2258 : TrickAttack,
2259 : Ten,
2261 : Chi,
2263 : Jin,
2265 : FumaShuriken,
2266 : Katon,
2267 : Raiton,
2268 : Hyoton,
2269 : Huton,
2270 : Doton,
2271 : Suiton,
16491 : GokaMekkyaku,
16492: HyoshoRanryu,
25774 : PhantomKamaitachi,
#25776 : Hollow Nozuchi,
3566 : DreamWithinADream,
25876 : Huraijin,
2264 : Kassatsu,
2262 : WaitAbility(0.5), #Shukuchi,
7401 : HellfrogMedium,
7402 : Bhavacakra,
7403 : TenChiJin,
16489 : Meisui,
16493 : Bunshin,
25777 : FleetingRaiju,
25778 : FleetingRaiju,
18805 : Ten,
18806 : Chi,
18807 : Jin,
18873 : Ten2,
18877 : Chi2,
18881 : Jin2
}
