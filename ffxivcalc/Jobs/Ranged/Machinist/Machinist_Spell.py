#########################################
########## MACHINIST SPELL  #############
#########################################


import copy
from ffxivcalc.Jobs.Base_Spell import DOTSpell, Queen_AA, empty, WaitAbility
from ffxivcalc.Jobs.Ranged.Ranged_Spell import MachinistSpell
from ffxivcalc.Jobs.Player import Pet

Lock = 0

#Special

def AddGauge(Player, Battery, Heat):
    Player.BatteryGauge = min(100, Player.BatteryGauge + Battery)
    Player.HeatGauge = min(100, Player.HeatGauge + Heat)

def RemoveGauge(Player, Battery, Heat):
    Player.BatteryGauge = max(0, Player.BatteryGauge - Battery)
    Player.HeatGauge = max(0, Player.HeatGauge - Heat)

#Requirement

def DetonatorRequirement(Player, Spell):
    return Player.WildFireTimer > 0, -1

def DismantleRequirement(Player, Spell):
    return Player.DismantleCD <= 0, Player.DismantleCD

def OverheatedRequirement(Player, Spell):
    return Player.HyperchargeStack > 0, -1 #True if Overheated

def WildFireRequirement(Player, Spell):
    return Player.WildFireCD <= 0, Player.WildFireCD

def AirAnchorRequirement(Player, Spell):
    return Player.AirAnchorCD <= 0, Player.AirAnchorCD

def BarrelStabilizerRequirement(Player, Spell):
    return Player.BarrelStabilizerCD <= 0, Player.BarrelStabilizerCD

def HyperchargeRequirement(Player, Spell):
    return Player.HyperchargeCD <= 0 and Player.HeatGauge >= 50, -1

def ReassembleRequirement(Player, Spell):
    return Player.ReassembleStack > 0, -1

def GaussRoundRequirement(Player, Spell):
    return Player.GaussRoundStack > 0, Player.GaussRoundCD

def RicochetRequirement(Player, Spell):
    return Player.RicochetStack > 0, Player.RicochetCD

def DrillRequirement(Player, Spell):
    return Player.DrillCD <= 0, Player.DrillCD

def OverdriveRequirement(Player, Spell):
    return Player.Overdrive, -1

def ChainSawRequirement(Player, Spell):
    return Player.ChainSawCD <= 0, Player.ChainSawCD

def AutomatonRequirement(Player, Spell):
    return (not Player.Overdrive) and Player.BatteryGauge >= 50, -1

def TacticianRequirement(Player, Spell):
    return Player.TacticianCD <= 0, Player.TacticianCD

#Apply

def ApplyDetonator(Player, Spell):
    Player.WildFireTimer = 0

def ApplyDismantle(Player, Enemy):
    Player.DismantleCD = 120

def ApplyTactician(Player, Enemy):
    Player.TacticianCD = 90

def ApplyScattergun(Player, Enemy):
    AddGauge(Player, 0, 10)

def ApplyBioblaster(Player, Enemy):
    ApplyDrill(Player, Enemy)
    if Player.BioblasterDOT == None:
        Player.BioblasterDOT = copy.deepcopy(BioblasterDOT)
        Player.DOTList.append(Player.BioblasterDOT)
        Player.BioblasterDOTTimer = 15
        Player.EffectCDList.append(BioblasterDOTCheck)
    Player.BioblasterDOTTimer = 15

def ApplyWildFire(Player, Enemy):
    Player.WildFireCD = 120
    Player.WildFireTimer = 10
    Player.EffectList.append(WildFireEffect)
    Player.EffectCDList.append(WildFireCheck)

def ApplyAirAnchor(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.AirAnchorCD = 40 * Player.WeaponskillReduction

def ApplyBarrelStabilizer(Player, Enemy):
    AddGauge(Player, 0, 50)
    Player.BarrelStabilizerCD = 120

def ApplyHeatBlast(Player, Enemy):
    Player.GaussRoundCD = max(0, Player.GaussRoundCD - 15)
    Player.RicochetCD = max(0, Player.RicochetCD - 15)

def ApplyHypercharge(Player, Enemy):
    Player.HyperchargeStack = 5
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
    Player.DrillCD = 20 * Player.WeaponskillReduction

def ApplyOverdrive(Player, Enemy):
    Player.Overdrive = False
    Player.Queen.ActionSet.insert(0,Collider)
    Player.Queen.ActionSet.insert(0,Bunker)

def ApplyChainSaw(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.ChainSawCD = 60 * Player.WeaponskillReduction

def ApplyAutomaton(Player, Enemy):
    Player.QueenStartUpTimer = 5
    Player.EffectCDList.append(QueenStartUpCheck)

def SummonQueen(Player, Enemy):
    #input("SummoningQueen at : " + str(Player.CurrentFight.TimeStamp))
    Player.AutomatonQueenCD = 6

    QueenTimer = (Player.BatteryGauge - 50)/5 + 10 #Queen timer by linearly extrapolating 10 sec base + extra battery Gauge
    #Queen Timer = (ExtraBatteryGauge) / BatteryPerSec - StartUpTimer + BaseTimer = Battery/5 - 5 + 10
    Player.BatteryGauge = 0
    if Player.Queen == None : Player.Queen = Pet(Player)#Creating new queen
    else: Player.Queen.ResetStat() # Reseting stat on the summon
    Player.QueenTimer = QueenTimer - 3 # Setting Queen Timer, gives last 3 seconds to perform finisher moves
    #Will have to depend on battery Gauge
    #Timer is set at 10 so we can have 2 GCD to do finisher move if reaches before
    Player.EffectCDList.append(QueenCheck)
    Player.Queen.ActionSet.append(Queen_AA)
    Player.Queen.ActionSet.append(WaitAbility(QueenTimer - 3)) #Gives 3 last sec to do finishing move
    Player.Queen.TrueLock = False #Delocking the queen if she was in a locked state, would happen is resummoned

def ApplyCollider(Queen, Enemy):#Called on queen
    Queen.Master.QueenOnField = False

#Combo Actions

def ApplySplitShot(Player, Enemy):
    AddGauge(Player, 0, 5)
    if not (SplitShotEffect in Player.EffectList) : Player.EffectList.append(SplitShotEffect)

def ApplySlugShot(Player, Enemy):
    pass

def ApplyCleanShot(Player, Enemy):
    pass

#Effect

def WildFireEffect(Player, Spell):
    if isinstance(Spell, MachinistSpell) and Spell.Weaponskill : Player.WildFireStack = min(6, Player.WildFireStack + 1) # Max of 6

def HyperchargeEffect(Player, Spell):
    if isinstance(Spell, MachinistSpell) and Spell.Weaponskill : 
        Spell.Potency += 20
        Player.RemoveHyperchargeStack = True

#Combo Actions effect

def SplitShotEffect(Player, Spell):
    if Spell.id == SlugShot.id:

        Spell.Potency += 180
        Player.EffectToRemove.append(SplitShotEffect)
        if not (SlugShotEffect in Player.EffectList) : Player.EffectList.append(SlugShotEffect)
        AddGauge(Player, 0, 5)

def SlugShotEffect(Player, Spell):
    if Spell.id == CleanShot.id:

        Spell.Potency += 260
        Player.EffectToRemove.append(SlugShotEffect)
        AddGauge(Player, 10, 5)


#Check

def QueenStartUpCheck(Player, Enemy):
    if Player.QueenStartUpTimer <= 0:
        SummonQueen(Player, Enemy) #Waits for 5 sec then summons the queen
        Player.EffectToRemove.append(QueenStartUpCheck)

def FlamethrowerDOTCheck(Player, Enemy):
    if Player.FlamethrowerDOTTimer <= 0:
        Player.DOTList.remove(Player.FlamethrowerDOT)
        Player.FlamethrowerDOT = None
        Player.EffectToRemove.append(FlamethrowerDOTCheck)

def BioblasterDOTCheck(Player, Enemy):
    if Player.BioblasterDOTTimer <= 0:
        Player.DOTList.remove(Player.BioblasterDOT)
        Player.BioblasterDOT = None
        Player.EffectToRemove.append(BioblasterDOTCheck)

def WildFireCheck(Player, Enemy):
    if Player.WildFireTimer <= 0:
        WildFireOff = MachinistSpell(2878, False, 0, 0, 240 * Player.WildFireStack, 0, empty, [], False)
        # Gives same ID as wildfire action so it shows in the log file
        #Temporary Spell that will be put in front of the Queue
        Player.ActionSet.insert(Player.NextSpell+1, WildFireOff) #Insert in queue, will be instantly executed
        Player.EffectList.remove(WildFireEffect)
        Player.EffectToRemove.append(WildFireCheck)
        Player.WildFireStack = 0

def HyperchargeCheck(Player, Enemy):

    if Player.RemoveHyperchargeStack:
        Player.RemoveHyperchargeStack = False
        Player.HyperchargeStack -= 1

    if Player.HyperchargeStack == 0:
        Player.EffectList.remove(HyperchargeEffect)
        Player.EffectToRemove.append(HyperchargeCheck)

def ReassembleStackCheck(Player, Enemy):
    if Player.ReassembleCD <= 0:
        if Player.ReassembleStack == 1:
            Player.EffectToRemove.append(ReassembleStackCheck)
        else:
            Player.ReassembleCD = 55
        Player.ReassembleStack +=1

def GaussRoundStackCheck(Player, Enemy):
    if Player.GaussRoundCD <= 0:
        if Player.GaussRoundStack == 2:
            Player.EffectToRemove.append(GaussRoundStackCheck)
        else:
            Player.GaussRoundCD = 30
        Player.GaussRoundStack +=1

def RicochetStackCheck(Player, Enemy):
    if Player.RicochetCD <= 0:
        if Player.RicochetStack == 2:
            Player.EffectToRemove.append(RicochetStackCheck)
        else:
            Player.RicochetCD = 30
        Player.RicochetStack +=1

def QueenCheck(Player, Enemy): # This will turn the queen off and make her perform the finisher moves
    if Player.QueenTimer <= 0: 
        Player.Overdrive = False
        Player.Queen.TrueLock = False #Delocking the Queen so she can perform these two abilities
        Player.Queen.ActionSet.insert(Player.NextSpell+1,Bunker)
        Player.Queen.ActionSet.insert(Player.NextSpell+2,Collider)
        Player.EffectToRemove.append(QueenCheck)
        Player.Queen.EffectCDList.append(QueenAACheck)


def QueenAACheck(Player, Enemy):
    if Player.TrueLock:#This function will be called on the Queen once it has finished Collider, it will get rid of AA's
        #It checks for when the Queen is done
        Player.DOTList = [] #Reset DOTList
        Player.EffectToRemove.append(QueenAACheck)




Dismantle = MachinistSpell(111111, False, 0, 0, 0, 0, ApplyDismantle, [DismantleRequirement], False)
Wildfire = MachinistSpell(2878, False, 0, Lock, 0, 0, ApplyWildFire, [WildFireRequirement], False)
Detonator = MachinistSpell(1111111, False, 0, 0, 0, 0, ApplyDetonator, [DetonatorRequirement], False)
AirAnchor = MachinistSpell(16500, True, 0, 2.5, 600, 0, ApplyAirAnchor, [AirAnchorRequirement], True, type = 2)
BarrelStabilizer = MachinistSpell(7414, False, 0, Lock, 0, 0, ApplyBarrelStabilizer, [BarrelStabilizerRequirement], False)
HeatBlast = MachinistSpell(7410, True, Lock, 1.5, 200, 0, ApplyHeatBlast, [OverheatedRequirement], True, type = 2)
Hypercharge = MachinistSpell(17209, False, 0, Lock, 0, 0, ApplyHypercharge, [HyperchargeRequirement], False)
Reassemble = MachinistSpell(2876, False, 0, Lock, 0, 0, ApplyReassemble, [ReassembleRequirement], False)
GaussRound = MachinistSpell(2874, False, 0, Lock, 130, 0, ApplyGaussRound, [GaussRoundRequirement], False)
Ricochet = MachinistSpell(2890, False, 0, Lock, 130, 0, ApplyRicochet, [RicochetRequirement], False)
Drill = MachinistSpell(16498, True, 0, 2.5, 600, 0, ApplyDrill, [DrillRequirement], True, type = 2)
ChainSaw = MachinistSpell(25788, True, 0, 2.5, 600, 0, ApplyChainSaw, [ChainSawRequirement], True, type = 2)
Tactician = MachinistSpell(16889, False, 0, 0, 0, 0, ApplyTactician, [TacticianRequirement], False)
#Combo Action

SplitShot = MachinistSpell(7411, True, Lock, 2.5, 200, 0, ApplySplitShot, [], True, type = 2)
SlugShot = MachinistSpell(7412, True, Lock, 2.5, 120, 0, ApplySlugShot, [], True , type = 2)
CleanShot = MachinistSpell(7413, True, Lock, 2.5, 120, 0, ApplyCleanShot, [], True, type = 2)


#AOE GCD
AutoCrossbow = MachinistSpell(16497, True, 0, 1.5, 140, 0, empty, [OverheatedRequirement], True, type = 2)
Scattergun = MachinistSpell(25768, True, 0, 2.5, 150, 0, ApplyScattergun, [], True, type = 2)
Bioblaster = MachinistSpell(16499, True, 0, 0, 50, 0, ApplyBioblaster, [DrillRequirement], True, type = 2) #Shares CD with Drill
BioblasterDOT = DOTSpell(-2, 50, True)
FlamethrowerDOT = DOTSpell(-3, 80, True)
def Flamethrower(time):
    #This function will apply a dot for the specified duration, and lock the player for this duration



    def FlamethrowerRequirement(Player, Spell):
        return time > 10 and Player.FlamethrowerCD <= 0, Player.FlamethrowerCD

    def ApplyFlamethrower(Player, Enemy):
        Player.FlamethrowerCD = 60
        Player.FlamethrowerDOTTimer = time
        Player.FlamethrowerDOT = copy.deepcopy(FlamethrowerDOT)
        Player.DOTList.append(Player.FlamethrowerDOT)
        Player.EffectCDList.append(FlamethrowerDOTCheck)

    return MachinistSpell(7418, True, time, time, 0, 0, ApplyFlamethrower, [FlamethrowerRequirement], False)

#Queen's Ability

#These abilities will write into the Queen's ability list.
#If they are not done the queen will do them automatically
Automaton = MachinistSpell(16501, False, 0, Lock, 0, 0, ApplyAutomaton, [], False)
Overdrive = MachinistSpell(16502, False, 0, Lock, 0, 0, ApplyOverdrive, [], False)
#These will be casted by the machinist, so they have no damage. Their only effect is to add into Queen's Queue
Bunker = MachinistSpell(15, True, 0, 2.5, 680, 0, ApplyCollider, [], False)   #Triggered by Overdrive
Collider = MachinistSpell(16, True, 0 , 2.5, 780, 0, ApplyCollider, [], False)  #Spell Queen will cast

MachinistAbility = {
7411 : SplitShot, 
7412 : SlugShot, 
25788 : ChainSaw,
25768 : Scattergun, 
17209 : Hypercharge, 
16889 : Tactician, 
16502 : Overdrive, 
16501 : Automaton,
16500 : AirAnchor, 
16499 : Bioblaster, 
16498 : Drill,
16497 : AutoCrossbow, 
7418 : Flamethrower(2.5), 
7414 : BarrelStabilizer, 
7413 : CleanShot, 
7410 : HeatBlast, 
2878 : Wildfire,
1111111 : Detonator,
2874 : GaussRound, 
2890 : Ricochet,
2876 : Reassemble
}
