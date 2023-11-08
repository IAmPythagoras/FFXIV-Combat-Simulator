from ffxivcalc.Jobs.Base_Spell import buff, empty, buffHistory, buffPercentHistory
from ffxivcalc.Jobs.Ranged.Ranged_Spell import DancerSpell
import copy
#Requirement

def SambaRequirement(Player, Spell):
    return Player.SambaCD <= 0, Player.SambaCD

def CuringWaltzRequirement(Player, Spell):
    return Player.CuringWaltzCD <= 0, Player.CuringWaltzCD

def StandardStepRequirement(Player, Spell):
    return Player.StandardStepCD <= 0, Player.StandardStepCD

def DanceRequirement(Player, Spell):
    return Player.Dancing, -1

def StandardFinishRequirement(Player, Spell):
    #Will check how many step we have
    #Not done in apply since we want to acces the spell easily

    Player.StandardFinishBuff = copy.deepcopy(StandardFinishBuff)
    step = 0
    if Player.Emboite : step +=1
    if Player.Entrechat : step +=1
    if Player.Jete : step +=1
    if Player.Pirouette : step +=1

    if step == 1:
        Spell.Potency += 180
        Player.StandardFinishBuff.MultDPS = 1.02
    elif step > 1:
        Spell.Potency += 360
        Player.StandardFinishBuff.MultDPS = 1.05

    return Player.StandardFinish, -1
        
def TechnicalFinishRequirement(Player, Spell):
    #Will check how many step we have
    #Not done in apply since we want to acces the spell easily

    Player.TechnicalFinishBuff = copy.deepcopy(TechnicalFinishBuff)
    step = 0
    if Player.Emboite : step +=1
    if Player.Entrechat : step +=1
    if Player.Jete : step +=1
    if Player.Pirouette : step +=1

    if step == 1 :
        Spell.Potency += 190
        Player.TechnicalFinishBuff.MultDPS = 1.01
    elif step == 2 :
        Spell.Potency += 370
        Player.TechnicalFinishBuff.MultDPS = 1.02
    elif step == 3 :
        Spell.Potency += 550
        Player.TechnicalFinishBuff.MultDPS = 1.03
    elif step == 4 :
        Spell.Potency += 850
        Player.TechnicalFinishBuff.MultDPS = 1.05

    return Player.TechnicalFinish, -1

def TechnicalStepRequirement(Player, Spell):
    return Player.TechnicalStepCD <= 0, Player.TechnicalStepCD

def DevilmentRequirement(Player, Spell):
    return Player.DevilmentCD <= 0, Player.DevilmentCD

def TillanaRequirement(Player, Spell):
    return Player.FlourishingFinish, -1

def StarfallDanceRequirement(Player, Spell):
    return Player.FlourishingStarfall, -1

def FlourishRequirement(Player, Spell):
    return Player.FlourishCD <= 0, Player.FlourishCD

def FanDance4Requirement(Player, Spell):
    return Player.FourfoldFan, -1

def FanDance3Requirement(Player, Spell):
    return Player.ThreefoldFan, -1

def FanDance1Requirement(Player, Spell):
    return Player.MaxFourfoldFeather > 0, -1

def FountainFallRequirement(Player, Spell):
    return Player.SilkenFlow or Player.FlourishingFlow, -1

def ReverseCascadeRequirement(Player, Spell):
    return Player.SilkenSymettry or Player.FlourishingSymettry, -1

def SaberDanceRequirement(Player, Spell):
    return Player.MaxEspritGauge >= 50, -1

def ClosedPositionRequirement(Player, Spell):
    return Player.ClosedPositionCD <= 0, Player.ClosedPositionCD

def ImprovisedFinishRequirement(Player, Spell):
    return Player.Improvising, -1

#Apply

def ApplySamba(Player, Enemy):
    Player.SambaCD = 90

def ApplyImprovisedFinish(Player, Enemy):
    Player.Improvising = False

def ApplyCuringWaltz(Player, Enemy):
    Player.CuringWaltzCD = 60

def ApplyWindmill(Player, Enemy):
    if not (WindmillCombo in Player.EffectList) : Player.EffectList.append(WindmillCombo)

def ApplyCascade(Player, Enemy):
    #Cascade has 50% chance to grant SikenSymettry, so we will keep track of the expected number we should have
    Player.ExpectedSilkenSymettry += 0.5 #adding to expected
    Player.SilkenSymettry = True    #Assuming it is true

    #Adding Combo Action
    if not (CascadeComboEffect in Player.EffectList) : Player.EffectList.append(CascadeComboEffect)


def ApplyStandardStep(Player, Enemy):
    Player.Dancing = True
    Player.StandardStepCD = 30
    Player.StandardFinish = True #Ready StandardFinish

def ApplyStandardFinish(Player, Enemy):
    #The MultBonus has already been computed from Requirement, so we just apply it to the dancer
    #and the dance partner

    #The check will be done on the dancer only
    if Player.StandardFinishTimer <= 0: 
        Player.EffectCDList.append(StandardFinishCheck)
        Player.buffList.append(Player.StandardFinishBuff) #Bonus DPS
        if Player.DancePartner != None : Player.DancePartner.buffList.append(Player.StandardFinishBuff) #Dance Partner Bonus
    
    Player.StandardFinishTimer = 60

    Player.Emboite = False
    Player.Entrechat = False
    Player.Jete = False
    Player.Pirouette = False
    #Reseting Dance move

def ApplyTechnicalStep(Player, Enemy):
    Player.Dancing = True
    Player.TechnicalStepCD = 120
    Player.TechnicalFinish = True #Ready TechnicalFinish

def ApplyTechnicalFinish(Player, Enemy):
    #The MultBonus has already been computed from Requirement, so we just apply it to the dancer
    #and the dance partner

    #The check will be done on the dancer only
    Player.EffectCDList.append(TechnicalFinishCheck)
    Enemy.buffList.append(Player.TechnicalFinishBuff) #Since party wide, applies on enemy


    Player.TechnicalFinishTimer = 20
    Player.Emboite = False
    Player.Entrechat = False
    Player.Jete = False
    Player.Pirouette = False
    #Reseting Dance move

    Player.FlourishingFinish = True #Enables Tillana

                                     # Only doing this if SavePreBakedAction is true
    #if Player.CurrentFight.SavePreBakedAction:
    #    fight = Player.CurrentFight
    #    history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20 , Player.TechnicalFinishBuff.MultDPS)
    #    fight.PlayerList[fight.PlayerIDSavePreBakedAction].PercentBuffHistory.append(history)

def ApplyEmboite(Player, Enemy):
    Player.Emboite = True

def ApplyEntrechat(Player, Enemy):
    Player.Entrechat = True

def ApplyJete(Player, Enemy):
    Player.Jete = True

def ApplyPirouette(Player, Enemy):
    Player.Pirouette = True

def ApplyDevilment(Player, Enemy):
    Player.FlourishingStarfall = True #Enables StarfallDance

    Player.DevilmentTimer = 20
    Player.DevilmentCD = 120
    #Give buff

    Player.CritRateBonus += 0.2
    Player.DHRateBonus += 0.2

    if Player.DancePartner != None : 
        Player.DancePartner.CritRateBonus += 0.2
        Player.DancePartner.DHRateBonus += 0.2

    Player.EffectCDList.append(DevilmentCheck)

    dancePartnerIsSavePreBaked = False if Player.DancePartner == None else Player.CurrentFight.PlayerIDSavePreBakedAction == Player.DancePartner.playerID

                                     # Only doing this if SavePreBakedAction is true
    if Player.CurrentFight.SavePreBakedAction and (Player.CurrentFight.PlayerIDSavePreBakedAction == Player.playerID or dancePartnerIsSavePreBaked):
        fight = Player.CurrentFight
        history = buffHistory(fight.TimeStamp, fight.TimeStamp + 20)
        fight.PlayerList[fight.PlayerIDSavePreBakedAction].DevilmentHistory.append(history)

def ApplyTillana(Player, Enemy):
    Player.FlourishingFinish = False 
    #We have to apply or reapply StandardFinish with a bonus of 5%, so reset, set bonus to 5% and apply
    if Player.StandardFinishBuff != None : Player.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
    if Player.DancePartner != None : Player.DancePartner.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
    
    if Player.StandardFinishBuff == None : Player.StandardFinishBuff = copy.deepcopy(StandardFinishBuff)
    Player.StandardFinishBuff.MultDPS = 1.05

    Player.StandardFinishTimer = 0 # Have to set to 0 so ApplyStandardFinish appends the buff to player buff list.

    ApplyStandardFinish(Player, Enemy) #Will give StandardFinish with a bonus of 5%

def ApplyStarfallDance(Player, Enemy):
    Player.NextDirectCrit = True
    Player.FlourishingStarfall = False

def ApplyFlourish(Player, Enemy):
    Player.FlourishCD = 60
    Player.FlourishingSymettry = True
    Player.FlourishingFlow = True
    Player.ThreefoldFan = True
    Player.FourfoldFan = True
    Player.ExpectedThreefoldFan +=1

def ApplyFanDance4(Player, Enemy):
    Player.FourfoldFan = False

def ApplyFanDance3(Player, Enemy):
    Player.ThreefoldFan = False
    Player.UsedThreefoldFan += 1

def ApplyFanDance1(Player, Enemy):
    Player.ThreefoldFan = True #Assume it happend
    Player.ExpectedThreefoldFan += 0.5 #add to expected

    Player.MaxFourfoldFeather -= 1
    Player.UsedFourfoldFeather += 1

def ApplyFountainFall(Player, Enemy):
    Player.MaxFourfoldFeather = min(4, Player.MaxFourfoldFeather + 1)
    Player.ExpectedFourfoldFeather += 0.5
    #Stats
    if not Player.FlourishingFlow: #If not from flourish
        Player.SilkenFlow = False
        Player.UsedSilkenFlow += 1
    else: #From flourish
        Player.FlourishingFlow = False #Not RNG

def ApplyReverseCascade(Player, Enemy):

    Player.MaxFourfoldFeather = min(4, Player.MaxFourfoldFeather + 1) 
    Player.ExpectedFourfoldFeather += 0.5 #Create
    if not Player.FlourishingSymettry: #Then its by SilkenSymettry
        Player.UsedSilkenSymettry += 1 #Need
        Player.SilkenSymettry = False
    else:
        Player.FlourishingSymettry = False
        #Since Flourish isn't RNG, this one does not keep track of anything

def ApplySaberDance(Player, Enemy):
    Player.MaxEspritGauge -= 50

def ApplyEnding(Player, Enemy):
    if Player.StandardFinishTimer > 0: #Remove StandardFinish
        Player.DancePartner.buffList.remove(Player.StandardFinishBuff)
    if Player.DevilmentTimer > 0: #Remove Devilment
        Player.DancePartner.CritRateBonus -= 0.2
        Player.DancePartner.DHRateBonus -= 0.2

    Player.DancePartner = None #Removing DancePartner

#Effect

def WindmillCombo(Player, Spell):
    if Spell.id == Bladeshower.id:
        Spell.Potency += 40
        Spell.Effect = Fountain.Effect #Giving Effect since we have made the combo

def EspritEffect(Player, Spell):
    if Spell.id == Fountain.id or Spell.id == FountainFall.id or Spell.id == Cascade.id or Spell.id == ReverseCascade.id:
        Player.MaxEspritGauge = min(100, Player.MaxEspritGauge + 5)

def CascadeComboEffect(Player, Spell):
    if Spell.id == Fountain.id:
        Spell.Potency += 180
        
        Player.ExpectedSilkenFlow += 0.5
        Player.SilkenFlow = True
        Player.EffectToRemove.append(CascadeComboEffect)

#Check

def DevilmentCheck(Player, Enemy):
    if Player.DevilmentTimer <= 0:
        Player.CritRateBonus -= 0.2
        Player.DHRateBonus -= 0.2
        if Player.DancePartner != None : 
            Player.DancePartner.CritRateBonus -= 0.2
            Player.DancePartner.DHRateBonus -= 0.2
        Player.EffectToRemove.append(DevilmentCheck)

def StandardFinishCheck(Player, Enemy):
    if Player.StandardFinishTimer <= 0:
        Player.buffList.remove(Player.StandardFinishBuff)
        if Player.DancePartner != None : Player.DancePartner.buffList.remove(Player.StandardFinishBuff)
        Player.EffectToRemove.append(StandardFinishCheck)
        Player.StandardFinishBuff = None

def TechnicalFinishCheck(Player, Enemy):
    if Player.TechnicalFinishTimer <= 0:
        Enemy.buffList.remove(Player.TechnicalFinishBuff)
        Player.EffectToRemove.append(TechnicalFinishCheck)
        Player.TechnicalFinishBuff = None


#GCD
StarfallDance = DancerSpell(25792, True, 2.5, 600, ApplyStarfallDance, [StarfallDanceRequirement], True, type = 2)
#ComboAction
Cascade = DancerSpell(15989, True, 2.5, 220,ApplyCascade, [], True, type = 2)
Fountain = DancerSpell(15990, True, 2.5, 100, empty, [], True, type = 2)
FountainFall = DancerSpell(15992, True, 2.5, 340, ApplyFountainFall, [FountainFallRequirement], True, type = 2)
ReverseCascade = DancerSpell(15991, True, 2.5, 280, ApplyReverseCascade, [ReverseCascadeRequirement], True, type = 2)
SaberDance = DancerSpell(16005, True, 2.5, 480, ApplySaberDance, [SaberDanceRequirement], True, type = 2)
#AOE Combo action
Windmill = DancerSpell(15993, True, 2.5, 100, ApplyWindmill, [], True , type = 2) #AOE Version of Cascade
RisingWindmill = DancerSpell(15995, True, 2.5, 140, ApplyReverseCascade, [ReverseCascadeRequirement], True, type = 2) #AOE version of Reverse Cascade
Bladeshower = DancerSpell(15994, True, 2.5, 100, empty, [], True, type = 2)
Bloodshower = DancerSpell(15996, True, 2.5, 180, ApplyFountainFall, [FountainFallRequirement], True, type = 2)
#Dance
StandardStep = DancerSpell(15997, True, 1.5, 0, ApplyStandardStep, [StandardStepRequirement], True, type = 2)
StandardFinish = DancerSpell(16003, True, 1.5, 360, ApplyStandardFinish, [StandardFinishRequirement], True, type = 2)
TechnicalStep = DancerSpell(15998, True, 1.5, 0, ApplyTechnicalStep, [TechnicalStepRequirement], True, type = 2)
TechnicalFinish = DancerSpell(16004, True, 1.5, 350, ApplyTechnicalFinish, [TechnicalFinishRequirement], True, type = 2)

def Improvisation(time): #Function, since we need to know for how long we are doing it

    def ImprovisationRequirement(Player, Spell):
        return Player.ImprovisationCD <= 0, Player.ImprovisationCD

    def ApplyImprovisation(Player, Enemy):
        Player.ImprovisationCD = 0
        Player.Improvising = True
    
    return DancerSpell(16014, True, time, time, ApplyImprovisation, [ImprovisationRequirement], False)

ImprovisedFinish = DancerSpell(25789, True, 1.5, 0, ApplyImprovisedFinish, [ImprovisedFinishRequirement], False)
Tillana = DancerSpell(25790, True, 1.5, 360, ApplyTillana, [TillanaRequirement], True, type = 2)
#Dance Move
Emboite = DancerSpell(15999, True, 1, 0, ApplyEmboite, [DanceRequirement], True)
Entrechat = DancerSpell(16000, True, 1, 0, ApplyEntrechat, [DanceRequirement], True)
Jete = DancerSpell(16001, True, 1, 0, ApplyJete, [DanceRequirement], True)
Pirouette = DancerSpell(16002, True, 1, 0, ApplyPirouette, [DanceRequirement], True)


#oGCD
Devilment = DancerSpell(16011, False, 0, 0, ApplyDevilment, [DevilmentRequirement], False)
Flourish = DancerSpell(16013, False, 0, 0, ApplyFlourish, [FlourishRequirement], False)
FanDance4 = DancerSpell(25791, False, 0, 300, ApplyFanDance4, [FanDance4Requirement], False)
FanDance3 = DancerSpell(16009, False, 0, 200, ApplyFanDance3, [FanDance3Requirement], False)
FanDance2 = DancerSpell(16008, False, 0, 100, ApplyFanDance1, [FanDance1Requirement], False) #AOE Version of FanDance1
FanDance1 = DancerSpell(16007, False, 0, 150, ApplyFanDance1, [FanDance1Requirement], False)
EnAvant = DancerSpell(16010, False, 0, 0, empty, [], False) #No requirement, spam that shit
CuringWaltz = DancerSpell(16015, False, 0, 0, ApplyCuringWaltz, [CuringWaltzRequirement], False)
Samba = DancerSpell(16012, False, 0, 0, ApplySamba, [SambaRequirement], False)
#buff
TechnicalFinishBuff = buff(1,name="Technical Finish") #We will adapt the buff depending on number of steps at casting
StandardFinishBuff = buff(1,name="Standard Finish") #We will adapt the buff depending on number of steps at casting

#Dance Partner
Ending = DancerSpell(18073, False, 0, 0, ApplyEnding, [], False)

def ClosedPosition(Partner, InFight="True"):

    def ApplyClosedPosition(Player, Enemy):
        if InFight : Player.ClosedPositionCD = 30 #Only update CD if in Fight, since we can dance partner before begins
        
        Player.DancePartner = Partner #New Partner
        if Player.StandardFinishTimer > 0: #Add StandardFinish
            Player.DancePartner.buffList.append(Player.StandardFinishBuff)
        if Player.DevilmentTimer > 0: #Add Devilment
            Player.DancePartner.CritRateBonus += 0.2
            Player.DancePartner.DHRateBonus += 0.2


        #Will have to switch buff
    ClosedPositionSpell = DancerSpell(16006, False, 0, 0, ApplyClosedPosition, [ClosedPositionRequirement], False)
    ClosedPositionSpell.TargetID = Partner.playerID
    return ClosedPositionSpell

DancerAbility = {
25792 : StarfallDance, 
25791 : FanDance4, 
16015 : CuringWaltz, 
16014 : Improvisation(2), 
16013 : Flourish, 
16012 : Samba, 
16011 : Devilment, 
16010 : EnAvant, 
16009 : FanDance3, 
16008 : FanDance2, 
16007 : FanDance1, 
16006 : ClosedPosition, 
16005 : SaberDance, 
15997 : StandardStep, 
15998 : TechnicalStep,
15996 : Bloodshower, 
15995 : RisingWindmill, 
15994 : Bladeshower, 
15993 : Windmill, 
15992 : FountainFall, 
15991 : ReverseCascade, 
15990 : Fountain, 
15989 : Cascade, 
16004 : TechnicalFinish, 
16193 : TechnicalFinish, 
16194 : TechnicalFinish, 
16195 : TechnicalFinish,
16196 : TechnicalFinish,
16003 : StandardFinish, 
25789 : ImprovisedFinish , 
18073 : Ending, 
25790 : Tillana, 
15999 : Emboite, 
16000 : Entrechat, 
16001 : Jete, 
16002 : Pirouette 
}