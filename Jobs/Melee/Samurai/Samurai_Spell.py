#########################################
########## SAMURAI PLAYER ###############
#########################################

from Jobs.Melee.Melee_Spell import SamuraiSpell
from Jobs.Base_Spell import DOTSpell, buff, empty
import math
import copy
Lock = 0
#Special
def AddKenki(Player, Add):
    Player.KenkiGauge = min(100, Player.KenkiGauge + Add)
    #print("Kenki Gauge : " + str(Player.KenkiGauge))


#Requirement

def KenkiRequirement(Player, Spell): #By default present in Samurai spell requirements
    return Spell.KenkiCost <= Player.KenkiGauge, -1

def MeikyoRequirement(Player, Spell):
    return Player.MeikyoStack > 0, Player.MeikyoCD

def IkishotenRequirement(Player, Spell):
    return Player.IkishotenCD <= 0, Player.IkishotenCD

def KaeshiRequirement(Player, Spell):
    return Player.KaeshiCD <= 0, Player.KaeshiCD

def SeneiRequirement(Player, Spell):
    return Player.SeneiCD <= 0, Player.SeneiCD

def OgiNamikiriRequirement(Player, Spell):
    return Player.OgiNamikiriReady, -1

def KaeshiNamikiriRequirement(Player, Spell):
    return Player.KaeshiNamikiriReady, -1

def ShohaRequirement(Player, Spell):
    return Player.MeditationGauge == 3, -1

def MidareRequirement(Player, Spell):
    return Player.Setsu and Player.Ka and Player.Getsu, -1 #need all of them

def TenkaGokenRequirement(Player, Spell): #Need 2 
    i = 0
    if Player.Setsu : i +=1
    if Player.Ka : i+=1
    if Player.Getsu : i +=1
    return i == 2, -1

def HiganbanaRequirement(Player, Spell):#Need 1
    i = 0
    if Player.Setsu : i +=1
    if Player.Ka : i+=1
    if Player.Getsu : i +=1
    return i == 1, -1

def ThirdEyeRequirement(Player, Spell):
    return Player.ThirdEyeCD <= 0, Player.ThirdEyeCD

def GyotenRequirement(Player, Spell):
    return Player.GyotenCD <= 0, Player.GyotenCD

def YatenRequirement(Player, Spell):
    return Player.YatenCD <= 0, Player.YatenCD

def HagakureRequirement(Player, Spell):
    return Player.HagakureCD <= 0, Player.HagakureCD

def TsubamegaeshiRequirement(Player, Spell):
    return Player.TsubamegaeshiStack > 0, Player.TsubamegaeshiCD

def KaeshiHiganbanaRequirement(Player, Spell):
    return Player.KaeshiHiganbana, -1

def KaeshiGokenRequirement(Player, Spell):
    return Player.KaeshiGoken, -1

def KaeshiSetsugekkaRequirement(Player, Spell):
    return Player.KaeshiSetsugekka, -1

#Apply

def ApplyTsubamegaeshi(Player, Enemy):
    Player.KaeshiHiganbana , Player.KaeshiGoken, Player.KaeshiSetsugekka = False,False,False #Reseting values
    if Player.TsubamegaeshiStack == 2:
        Player.EffectCDList.append(TsubamegaeshiStackCheck)
        Player.TsubamegaeshiCD = 60
    Player.TsubamegaeshiStack -= 1

def ApplyHagakure(Player, Enemy):
    i = 0
    if Player.Setsu : i +=1
    if Player.Ka : i+=1
    if Player.Getsu : i +=1

    AddKenki(Player, i * 10)
    Player.Setsu, Player.Ka, Player.Getsu = False, False, False #Reseting

def ApplyYaten(Player, Enemy):
    Player.YatenCD = 10
    if not (YatenEffect in Player.EffectList) : 
        Player.EffectList.append(YatenEffect)
        Player.EffectCDList.append(YatenCheck)
    Player.EnhancedEnpiTimer = 15

def ApplyGyoten(Player, Enemy):
    Player.GyotenCD = 10

def Add10Kenki(Player, Enemy):
    AddKenki(Player, 10)

def ApplyTenkaGoken(Player, Enemy):
    Player.KaeshiGoken = True
    Player.EffectList.append(TsubamegaeshiCheck)
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1) #Adding meditation stack
    Player.Setsu, Player.Ka, Player.Getsu = False, False, False #Reseting

def ApplyThirdEye(Player, Enemy):
    Player.ThirdEyeCD = 15
    #We will assume it gives us 10 Kenki
    AddKenki(Player, 10)

def ApplyFuko(Player, Enemy):
    AddKenki(Player, 10)
    if not (FukoCombo in Player.EffectList) : Player.EffectList.append(FukoCombo)

def ApplyHakaze(Player, Enemy):
    AddKenki(Player, 5)
    if not (HakazeEffect in Player.EffectList) : Player.EffectList.append(HakazeEffect)

def ApplyJinpu(Player, Enemy):
    if not (JinpuEffect in Player.EffectList) : Player.EffectList.append(JinpuEffect)

def ApplyShifu(Player, Enemy):
    if not (ShifuEffect in Player.EffectList) : Player.EffectList.append(ShifuEffect)

def ApplyMeikyo(Player, Enemy):
    if Player.MeikyoStack == 2:
        Player.EffectCDList.append(MeikyoStackCheck)
        Player.MeikyoCD = 55
    Player.MeikyoStack -= 1
    Player.EffectList.append(MeikyoEffect)
    Player.EffectCDList.append(MeikyoCheck) #Could be a problem if do it before finishing 3 weaponskills
    Player.Meikyo = 3


def ApplyIkishoten(Player, Enemy):
    AddKenki(Player, 50)
    Player.IkishotenCD = 120
    Player.OgiNamikiriReady = True

def ApplyMidare(Player, Enemy):
    Player.KaeshiSetsugekka = True
    Player.EffectList.append(TsubamegaeshiCheck)
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1)
    Player.DirectCrit = True
    Player.Setsu, Player.Ka, Player.Getsu = False, False, False #Reseting

def ApplyKaeshi(Player, Enemy):
    Player.DirectCrit = True
    ApplyTsubamegaeshi(Player, Enemy) #Also sets flag to false

def ApplyKaeshiHiganbana(Player, Enemy):
    Player.DirectCrit = True
    ApplyTsubamegaeshi(Player, Enemy) #Also sets flag to false
    if Player.Higanbana == None:
        Player.Higanbana = copy.deepcopy(HiganbanaDOT)
        Player.DOTList.append(Player.Higanbana)
    Player.HiganbanaTimer = 45 #Adding dot

def ApplyKaeshiGoken(Player, Enemy):
    Player.DirectCrit = True
    ApplyTsubamegaeshi(Player, Enemy) #Also sets flag to false


def ApplySenei(Player, Enemy):
    Player.SeneiCD = 120
    Player.KenkiGauge -= 25

def ApplyHiganbana(Player, Enemy):
    Player.KaeshiHiganbana = True
    Player.EffectList.append(TsubamegaeshiCheck)
    if Player.Higanbana == None:
        Player.Higanbana = copy.deepcopy(HiganbanaDOT)
        Player.DOTList.append(Player.Higanbana)
    Player.HiganbanaTimer = 45
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1)
    Player.Setsu, Player.Ka, Player.Getsu = False, False, False #Reseting

def ApplyOgiNamikiri(Player, Enemy):
    #print("hey")
    Player.KaeshiNamikiriReady = True
    Player.OgiNamikiriReady = False
    Player.DirectCrit = True
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1)

def ApplyKaeshiNamikiri(Player, Enemy):
    Player.KaeshiNamikiriReady = False
    Player.DirectCrit = True

def ApplyShoha(Player, Enemy):
    Player.MeditationGauge = 0

def ApplyShinten(Player, Enemy):
    Player.KenkiGauge -= 25

def ApplyKaeshiGoken(Player, Enemy):
    ApplyTsubamegaeshi(Player, Enemy)

#Combo Action Effect

def FukoCombo(Player, Spell):
    if Spell.id == Mangetsu.id:
        Spell.Potency += 20
        Player.FugetsuTimer = 40
        Player.Getsu = True
    elif Spell.id == Oka.id:
        Spell.Potency += 20
        Player.FukaTimer = 40
        Player.Ka = True

def HakazeEffect(Player, Spell):
    if Spell.id == Jinpu.id:
        Player.FugetsuTimer = 40
        AddKenki(Player, 5)
        Spell.Potency += 160
        if not Player.Fugetsu:
            Player.Fugetsu = True
            Player.buffList.append(HakazeBuff)
            Player.EffectCDList.append(FugetsuCheck)
            Player.EffectToRemove.append(HakazeEffect)
    elif Spell.id == Shifu.id:
        Spell.Potency += 160
        if not (FukaEffect in Player.EffectList) : Player.EffectList.append(FukaEffect)
        if not (FukaCheck in Player.EffectCDList) : Player.EffectCDList.append(FukaCheck)
        Player.FukaTimer = 40
        AddKenki(Player, 5)
        Player.EffectToRemove.append(HakazeEffect)
    elif Spell.id == Yukikaze.id:
        Spell.Potency += 180
        AddKenki(Player, 15)
        Player.Setsu = True
        Player.EffectToRemove.append(HakazeEffect)


def ShifuEffect(Player, Spell):
    if Spell.id == Kasha.id:
        Spell.Potency += 210
        AddKenki(Player, 10)
        Player.Ka = True
        Player.EffectToRemove.append(ShifuEffect)

def JinpuEffect(Player, Spell):
    if Spell.id == Gekko.id: 
        Spell.Potency +=210
        AddKenki(Player, 10)
        Player.Getsu = True
        Player.EffectToRemove.append(JinpuEffect)

def FukaEffect(Player, Spell):
    Spell.CastTime *= 0.87
    Spell.RecastTime *= 0.87

def MeikyoEffect(Player, Spell):
    if Spell.id == Gekko.id: 
        Spell.Potency +=210
        AddKenki(Player, 10)
        Player.Getsu = True
        Player.Meikyo -= 1
    elif Spell.id == Kasha.id:
        Spell.Potency += 210
        AddKenki(Player, 10)
        Player.Ka = True
        Player.Meikyo -= 1
    elif Spell.id == Jinpu.id:
        Player.FugetsuTimer = 40
        AddKenki(Player, 5)
        Spell.Potency += 160
        if not Player.Fugetsu:
            Player.Fugetsu = True
            Player.MultDPSBonus *= 1.13
            Player.EffectCDList.append(FugetsuCheck)
        Player.Meikyo -= 1
    elif Spell.id == Shifu.id:
        Spell.Potency += 160
        if not (FukaEffect in Player.EffectList) : Player.EffectList.append(FukaEffect)
        if not (FukaCheck in Player.EffectCDList) : Player.EffectCDList.append(FukaCheck)
        Player.FukaTimer = 40
        AddKenki(Player, 5)
        Player.Meikyo -= 1
    elif Spell.id == Yukikaze.id:
        Spell.Potency += 180
        AddKenki(Player, 15)
        Player.Setsu = True
        Player.Meikyo -= 1

#Effect

def TsubamegaeshiCheck(Player, Spell):
    #This effect will remove the ability to do Tsubamegaeshi if the next spell after a Iaijutsu is not a Kaeshi
    if Spell.GCD:
        if Player.KaeshiHiganbana:
            if Spell.id != KaeshiHiganbana.id: Player.KaeshiHiganbana = False
        elif Player.KaeshiGoken:
            if Spell.id != KaeshiGoken.id: Player.KaeshiGoken = False
        elif Player.KaeshiSetsugekka:
            if Spell.id != KaeshiSetsugekka.id: Player.KaeshiSetsugekka = False

        Player.EffectToRemove.append(TsubamegaeshiCheck)

def YatenEffect(Player, Spell):
    if Spell.id == Enpi.id:
        Spell.Potency += 160
        Player.EnhancedEnpiTimer = 0 #End effect
    
#Effect Check

def YatenCheck(Player, Enemy):
    if Player.EnhancedEnpiTimer <= 0:
        Player.EffectList.remove(YatenEffect)
        Player.EffectToRemove.append(YatenCheck)

def FukaCheck(Player, Enemy):
    if Player.FukaTimer <= 0:
        Player.EffectList.remove(FukaEffect)
        Player.EffectToRemove.append(FukaCheck)

def FugetsuCheck(Player, Enemy):
    if Player.FugetsuTimer <= 0:
        Player.Fugetsu = False
        Player.buffList.remove(HakazeBuff)
        Player.EffectToRemove.append(FugetsuCheck)

def HiganbanaCheck(Player, Enemy):
    if Player.HiganbanaTimer <= 0:
        Player.DOTList.remove(Player.Higanbana)
        Player.Higanbana = None
        Player.EffectToRemove.append(HiganbanaCheck)

def MeikyoCheck(Player, Enemy):
    if Player.Meikyo == 0:
        Player.EffectList.remove(MeikyoEffect)
        Player.EffectToRemove.append(MeikyoCheck)

#Stack Check

def TsubamegaeshiStackCheck(Player, Enemy):
    if Player.TsubamegaeshiCD <= 0:
        if Player.TsubamegaeshiStack == 1:
            Player.EffectToRemove.append(TsubamegaeshiStackCheck)
        else:
            Player.TsubamegaeshiCD = 60
        Player.TsubamegaeshiStack += 1

def MeikyoStackCheck(Player, Enemy):
    if Player.MeikyoCD <= 0:
        if Player.MeikyoStack == 1:
            Player.EffectToRemove.append(MeikyoStackCheck)
        else:
            Player.MeikyoCD = 55
        Player.MeikyoStack +=1


#GCD
OgiNamikiri = SamuraiSpell(1, True, 1.8, 2.5, 800, ApplyOgiNamikiri, [OgiNamikiriRequirement], 0)
KaeshiNamikiri = SamuraiSpell(2, True, 1.3, 1, 800, ApplyKaeshiNamikiri, [KaeshiNamikiriRequirement], 0)
Enpi = SamuraiSpell(3, True, 0, 1.5, 100, Add10Kenki, [], 0)

#Iaijutsu
Higanbana = SamuraiSpell(4, True, 1.3, 2.5, 200, ApplyHiganbana, [HiganbanaRequirement], 0)
HiganbanaDOT = DOTSpell(-1, 60, True)
TenkaGoken = SamuraiSpell(5, True, 1.3, 2.5, 280, ApplyTenkaGoken, [TenkaGokenRequirement], 0)
Midare = SamuraiSpell(6, True, 1.3, 2.5, 640, ApplyMidare, [MidareRequirement], 0)

#Kaeshi
KaeshiHiganbana = SamuraiSpell(7, True, 0, 2.5, 200, ApplyKaeshiHiganbana, [KaeshiHiganbanaRequirement,TsubamegaeshiRequirement], 0)
KaeshiGoken = SamuraiSpell(8, True, 0, 2.5, 280, ApplyKaeshiGoken, [KaeshiGokenRequirement,TsubamegaeshiRequirement], 0)
KaeshiSetsugekka = SamuraiSpell(9, True, 0, 2.5, 640, ApplyKaeshi, [KaeshiSetsugekkaRequirement,TsubamegaeshiRequirement], 0)

#Combo Actions
Hakaze = SamuraiSpell(10, True, Lock, 2.5, 200, ApplyHakaze, [], 0 )
Jinpu = SamuraiSpell(11, True, Lock, 2.5, 120, ApplyJinpu, [], 0)
Gekko = SamuraiSpell(12, True, Lock, 2.5, 170, empty, [], 0)
Shifu = SamuraiSpell(13, True, Lock, 2.5, 120, empty, [], 0)
Kasha = SamuraiSpell(14, True, Lock, 2.5, 170, empty, [], 0)
Yukikaze = SamuraiSpell(15, True, Lock, 2.5, 120, empty, [], 0)

#AOE Combo Action
Fuko = SamuraiSpell(16, True, 0, 2.5, 100, ApplyFuko, [], 0 )
Mangetsu = SamuraiSpell(17, True, 0, 2.5, 100, empty, [], 0)
Oka = SamuraiSpell(18, True, 0, 2.5, 100, empty, [], 0)

#oGCD
Meikyo = SamuraiSpell(19, False, Lock, Lock, 0, ApplyMeikyo, [MeikyoRequirement], 0)
Ikishoten = SamuraiSpell(20, False, Lock, Lock, 0, ApplyIkishoten, [IkishotenRequirement], 0)
Shoha = SamuraiSpell(21, False, Lock, Lock, 520, ApplyShoha, [ShohaRequirement], 0)
Shoha2 = SamuraiSpell(22, False, Lock, Lock, 200, ApplyShoha, [ShohaRequirement], 0) #AOEVersion of Shoha
ThirdEye = SamuraiSpell(23, False, 0, 0, 0, ApplyThirdEye, [ThirdEyeRequirement], 0)
Hagakure = SamuraiSpell(24, False, 0, 0, 0, ApplyHagakure, [HagakureRequirement], 0)

#Kenki Action
Senei = SamuraiSpell(25, False, Lock, 2.5, 800, ApplySenei, [SeneiRequirement], 25)
Guren = SamuraiSpell(26, False, 0, 0, 500, ApplySenei, [SeneiRequirement], 25) #AOE version of Senei
Shinten = SamuraiSpell(27, False, Lock, 1, 250, ApplyShinten, [], 25)
Gyoten = SamuraiSpell(28, False, 0, 0, 100, ApplyGyoten,[GyotenRequirement],10 )
Yaten = SamuraiSpell(29, False, 0, 0, 100, ApplyYaten, [YatenRequirement], 10)
Kyuten = SamuraiSpell(30, False, 0, 0, 110, empty, [], 25)
#buff
HakazeBuff = buff(1.13)

def Meditate(time):
    #This function will return a Samurai Spell object that will correspond to a Meditate of the specified amount of time
    def MeditateRequirement(Player, Spell):
        return Player.MeditateCD <= 0 and time < 15 and time > 0, Player.MedidateCD

    def ApplyMedidate(Player, Spell):
        #Medidate generates 10 kenki each 3 sec, so we will divide time by 3, and add that much kenki
        AddKenki(Player, 10 * math.floor(time/3))
        Player.MedidateCD = 60

    return SamuraiSpell(31, False, time, time, 0, ApplyMedidate, [MeditateRequirement], 0)

SamuraiAbility = {}