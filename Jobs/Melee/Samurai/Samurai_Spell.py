#########################################
########## SAMURAI PLAYER ###############
#########################################

from Jobs.Melee.Melee_Spell import SamuraiSpell
from Jobs.Base_Spell import DOTSpell, buff, empty
Lock = 0.75
import copy
#Special
def AddKenki(Player, Add):
    Player.KenkiGauge = min(100, Player.KenkiGauge + Add)
    #print("Kenki Gauge : " + str(Player.KenkiGauge))


#Requirement

def KenkiRequirement(Player, Spell): #By default present in Samurai spell requirements
    return Spell.KenkiCost <= Player.KenkiGauge

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
    return Player.Setsu and Player.Ka and Player.Getsu, -1

def HiganbanaRequirement(Player, Spell):
    i = 0
    if Player.Setsu : i +=1
    if Player.Ka : i+=1
    if Player.Getsu : i +=1
    return i == 1, -1

#Apply

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
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1)
    Player.DirectCrit = True
    Player.Setsu, Player.Ka, Player.Getsu = False, False, False

def ApplyKaeshi(Player, Enemy):
    Player.DirectCrit = True
    Player.KaeshiCD = 60

def ApplySenei(Player, Enemy):
    Player.SeneiCD = 120
    Player.KenkiGauge -= 25

def ApplyHiganbana(Player, Enemy):
    if Player.Higanbana != None:
        Player.Higanbana = copy.deepcopy(HiganbanaDOT)
        Player.DOTList.append(Player.Higanbana)
    Player.HiganbanaTimer = 45
    Player.MeditationGauge = min(3, Player.MeditationGauge + 1)


    if Player.Setsu : Player.Setsu = False
    if Player.Ka : Player.Ka = False
    if Player.Getsu : Player.Getsu = False

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

#Combo Action Effect

def HakazeEffect(Player, Spell):
    if Spell.id == Jinpu.id:
        Player.FugetsuTimer = 40
        AddKenki(Player, 5)
        Spell.Potency += 160
        if not Player.Fugetsu:
            Player.Fugetsu = True
            Player.buffList.append(HakazaBuff)
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

    
#Effect Check

def FukaCheck(Player, Enemy):
    if Player.FukaTimer <= 0:
        Player.EffectList.remove(FukaEffect)
        Player.EffectToRemove.append(FukaCheck)


def FugetsuCheck(Player, Enemy):
    if Player.FugetsuTimer <= 0:
        Player.Fugetsu = False
        Player.buffList.remove(HakazaBuff)
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

def MeikyoStackCheck(Player, Enemy):
    if Player.MeikyoCD <= 0:
        if Player.MeikyoStack == 1:
            Player.MeikyoStack +=1
            Player.EffectToRemove.append(MeikyoStackCheck)
        else:
            Player.MeikyoStack +=1
            Player.MeikyoCD = 55

#GCD
Midare = SamuraiSpell(9, True, 1.3, 2.5, 600, ApplyMidare, [MidareRequirement], 0)
Kaeshi = SamuraiSpell(10, True, 1.3, 2.5, 600, ApplyKaeshi, [], 0)
OgiNamikiri = SamuraiSpell(13, True, 1.8, 2.5, 800, ApplyOgiNamikiri, [OgiNamikiriRequirement], 0)
KaeshiNamikiri = SamuraiSpell(14, True, 1.3, 1, 800, ApplyKaeshiNamikiri, [KaeshiNamikiriRequirement], 0)

#Combo Actions
Hakaze = SamuraiSpell(1, True, Lock, 2.5, 200, ApplyHakaze, [], 0 )
Jinpu = SamuraiSpell(2, True, Lock, 2.5, 120, ApplyJinpu, [], 0)
Gekko = SamuraiSpell(3, True, Lock, 2.5, 170, empty, [], 0)
Shifu = SamuraiSpell(4, True, Lock, 2.5, 120, empty, [], 0)
Kasha = SamuraiSpell(5, True, Lock, 2.5, 170, empty, [], 0)
Yukikaze = SamuraiSpell(6, True, Lock, 2.5, 120, empty, [], 0)


#oGCD
Meikyo = SamuraiSpell(7, False, Lock, Lock, 0, ApplyMeikyo, [MeikyoRequirement], 0)
Ikishoten = SamuraiSpell(8, False, Lock, Lock, 0, ApplyIkishoten, [IkishotenRequirement], 0)
Senei = SamuraiSpell(11, False, Lock, 2.5, 800, ApplySenei, [SeneiRequirement], 25)
Shoha = SamuraiSpell(15, False, Lock, Lock, 500, ApplyShoha, [ShohaRequirement], 0)
Shinten = SamuraiSpell(16, False, Lock, 1, 250, ApplyShinten, [], 25)
#DOT
Higanbana = SamuraiSpell(12, True, 1.3, 2.5, 200, ApplyHiganbana, [HiganbanaRequirement], 0)
HiganbanaDOT = DOTSpell(-1, 60, True)

#buff
HakazaBuff = buff(1.13)