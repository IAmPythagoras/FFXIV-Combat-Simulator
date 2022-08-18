from Jobs.Base_Spell import buff, empty
from Jobs.Ranged.Ranged_Spell import DancerSpell
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

    if Player.StandardFinishBuff != None : Player.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
    if Player.DancePartner != None and Player.StandardFinishBuff != None : Player.DancePartner.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
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

    if Player.TechnicalFinishBuff != None : Player.CurrentFight.Enemy.buffList.remove(Player.TechnicalFinishBuff)#Reset DPSBonus
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
    return Player.Improvising

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
    if Player.StandardFinishTimer == 0: Player.EffectCDList.append(StandardFinishCheck)
    Player.StandardFinishTimer = 60
    Player.buffList.append(Player.StandardFinishBuff) #Bonus DPS
    if Player.DancePartner != None : Player.DancePartner.buffList.append(Player.StandardFinishBuff) #Dance Partner Bonus

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

    Player.TechnicalFinishTimer = 20
    Enemy.buffList.append(Player.TechnicalFinishBuff) #Since party wide, applies on enemy

    Player.Emboite = False
    Player.Entrechat = False
    Player.Jete = False
    Player.Pirouette = False
    #Reseting Dance move

    Player.FlourishingFinish = True #Enables Tillana

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

def ApplyTillana(Player, Enemy):
    Player.FlourishingFinish = False 
    #We have to apply or reapply StandardFinish with a bonus of 5%, so reset, set bonus to 5% and apply
    print(Player.StandardFinishBuff)
    if Player.StandardFinishBuff != None : Player.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
    if Player.DancePartner != None : Player.DancePartner.buffList.remove(Player.StandardFinishBuff) #Reset DPSBonus
    Player.StandardFinishBuff.MultDPS = 1.05
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
        Player.DancePartner.CritRateBonus -= 0.2
        Player.DancePartner.DHRateBonus -= 0.2
        Player.EffectToRemove.append(DevilmentCheck)

def StandardFinishCheck(Player, Enemy):
    if Player.StandardFinishTimer <= 0:
        Player.buffList.remove(Player.StandardFinishBuff)
        if Player.DancePartner != None : Player.DancePartner.buffList.remove(Player.StandardFinishBuff)
        Player.EffectToRemove.append(StandardFinishCheck)

def TechnicalFinishCheck(Player, Enemy):
    if Player.TechnicalFinishTimer <= 0:
        Enemy.buffList.remove(Player.TechnicalFinishBuff)
        Player.EffectToRemove.append(TechnicalFinishCheck)


#GCD
StarfallDance = DancerSpell(1, True, 2.5, 600, ApplyStarfallDance, [StarfallDanceRequirement], True)
#ComboAction
Cascade = DancerSpell(2, True, 2.5, 220,ApplyCascade, [], True)
Fountain = DancerSpell(3, True, 2.5, 100, empty, [], True)
FountainFall = DancerSpell(4, True, 2.5, 340, ApplyFountainFall, [FountainFallRequirement], True)
ReverseCascade = DancerSpell(5, True, 2.5, 280, ApplyReverseCascade, [ReverseCascadeRequirement], True)
SaberDance = DancerSpell(6, True, 2.5, 480, ApplySaberDance, [SaberDanceRequirement], True)
#AOE Combo action
Windmill = DancerSpell(7, True, 2.5, 100, ApplyWindmill, [], True ) #AOE Version of Cascade
RisingWindmill = DancerSpell(8, True, 2.5, 140, ApplyReverseCascade, [ReverseCascadeRequirement], True) #AOE version of Reverse Cascade
Bladeshower = DancerSpell(9, True, 2.5, 100, empty, [], True)
Bloodshower = DancerSpell(10, True, 2.5, 180, ApplyFountainFall, [FountainFallRequirement], True)
#Dance
StandardStep = DancerSpell(11, True, 1.5, 0, ApplyStandardStep, [StandardStepRequirement], True)
StandardFinish = DancerSpell(12, True, 1.5, 360, ApplyStandardFinish, [StandardFinishRequirement], True)
TechnicalStep = DancerSpell(13, True, 1.5, 0, ApplyTechnicalStep, [TechnicalStepRequirement], True)
TechnicalFinish = DancerSpell(14, True, 1.5, 350, ApplyTechnicalFinish, [TechnicalFinishRequirement], True)

def Improvisation(time): #Function, since we need to know for how long we are doing it

    def ImprovisationRequirement(Player, Spell):
        return Player.ImprovisationCD <= 0, Player.ImprovisationCD

    def ApplyImprovisation(Player, Enemy):
        Player.ImprovisationCD = 0
        Player.Improvising = True
    
    return DancerSpell(15, True, time, time, ApplyImprovisation, [ImprovisationRequirement], False)

ImprovisedFinish = DancerSpell(16, True, 1.5, 0, ApplyImprovisedFinish, [ImprovisedFinishRequirement], False)
Tillana = DancerSpell(17, True, 1.5, 360, ApplyTillana, [TillanaRequirement], True)
#Dance Move
Emboite = DancerSpell(18, True, 1, 0, ApplyEmboite, [DanceRequirement], True)
Entrechat = DancerSpell(19, True, 1, 0, ApplyEntrechat, [DanceRequirement], True)
Jete = DancerSpell(20, True, 1, 0, ApplyJete, [DanceRequirement], True)
Pirouette = DancerSpell(21, True, 1, 0, ApplyPirouette, [DanceRequirement], True)


#oGCD
Devilment = DancerSpell(22, False, 0, 0, ApplyDevilment, [DevilmentRequirement], False)
Flourish = DancerSpell(23, False, 0, 0, ApplyFlourish, [FlourishRequirement], False)
FanDance4 = DancerSpell(24, False, 0, 300, ApplyFanDance4, [FanDance4Requirement], False)
FanDance3 = DancerSpell(25, False, 0, 200, ApplyFanDance3, [FanDance3Requirement], False)
FanDance2 = DancerSpell(26, False, 0, 100, ApplyFanDance1, [FanDance1Requirement], False) #AOE Version of FanDance1
FanDance1 = DancerSpell(27, False, 0, 150, ApplyFanDance1, [FanDance1Requirement], False)
EnAvant = DancerSpell(28, False, 0, 0, empty, [], False) #No requirement, spam that shit
CuringWaltz = DancerSpell(29, False, 0, 0, ApplyCuringWaltz, [CuringWaltzRequirement], False)
Samba = DancerSpell(30, False, 0, 0, ApplySamba, [SambaRequirement], False)
#buff
TechnicalFinishBuff = buff(1) #We will adapt the buff depending on number of steps at casting
StandardFinishBuff = buff(1) #We will adapt the buff depending on number of steps at casting

#Dance Partner
Ending = DancerSpell(32, False, 0, 0, ApplyEnding, [], False)

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
    ClosedPositionSpell = DancerSpell(33, False, 0, 0, ApplyClosedPosition, [ClosedPositionRequirement], False)
    ClosedPositionSpell.TargetID = Partner.playerID
    return ClosedPositionSpell

DancerAbility = {
25792 : StarfallDance, 
25791 : FanDance4, 
16015 : CuringWaltz, 
16014 : Improvisation, 
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