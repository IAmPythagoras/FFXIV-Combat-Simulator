#########################################
########## MACHINIST SPELL  #############
#########################################
from Jobs.Base_Spell import empty, WaitAbility
from Jobs.Ranged.Machinist.Machinist_Player import Queen
from Jobs.Ranged.Ranged_Spell import MachinistSpell

Lock = 0.75

#Special

def AddGauge(Player, Battery, Heat):
    Player.BatteryGauge = min(100, Player.BatteryGauge + Battery)
    Player.HeatGauge = min(100, Player.HeatGauge + Heat)

def RemoveGauge(Player, Battery, Heat):
    Player.BatteryGauge = max(0, Player.BatteryGauge - Battery)
    Player.HeatGauge = max(0, Player.HeatGauge - Heat)
#Requirement

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
    return Player.GaussRoundStack > 0, -1

def RicochetRequirement(Player, Spell):
    return Player.RicochetStack > 0, -1

def DrillRequirement(Player, Spell):
    return Player.DrillCD <= 0, Player.DrillCD

def OverdriveRequirement(Player, Spell):
    return Player.Overdrive, -1

def ChainSawRequirement(Player, Spell):
    return Player.ChainSawCD <= 0, Player.ChainSawCD

def AutomatonRequirement(Player, Spell):
    return (not Player.Overdrive) and Player.BatteryGauge >= 50, -1

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
    if isinstance(Spell, MachinistSpell) and Spell.Weaponskill : Player.WildFireStack +=1

def HyperchargeEffect(Player, Spell):
    if Spell.Weaponskill : Spell.Potency += 20

#Combo Actions effect

def SplitShotEffect(Player, Spell):
    if Spell.id == 5:

        Spell.Potency =+ 160
        Player.EffectToRemove.append(SplitShotEffect)

def SlugShotEffect(Player, Spell):
    if Spell.id == 6:

        Spell.Potency += 250
        Player.EffectToRemove.append(SlugShotEffect)


#Check

def WildFireCheck(Player, Enemy):
    if Player.WildFireTimer <= 0:

        WildFireOff = MachinistSpell(1, False, 0, 0, 200 * Player.WildFireStack, 0, empty, [], False)
        #Temporary Spell that will be put in front of the Queue
        Player.ActionSet.insert(Player.NextSpell+1, WildFireOff) #Insert in queue, will be instantly executed
        Player.WildFireStack = 0
        Player.EffectList.remove(WildFireEffect)
        Player.EffectToRemove.append(WildFireCheck)

def HyperchargeCheck(Player, Enemy):
    if Player.HyperchargeTimer <= 0:
        #print("Hypercharge went off at : " + str(Player.CurrentFight.TimeStamp))
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

def QueenCheck(Player, Enemy):#This will be called on the queen
    if Player.Timer <= 0: 
        Player.Master.Overdrive = False
        Player.ActionSet.insert(Player.NextSpell+1,Bunker)
        Player.ActionSet.insert(Player.NextSpell+2,Collider)
        Player.EffectToRemove.append(QueenCheck)

Wildfire = MachinistSpell(0, False, 0, Lock, 0, 0, ApplyWildFire, [WildFireRequirement], False)
AirAnchor = MachinistSpell(2, True, 0, 2.5, 580, 0, ApplyAirAnchor, [AirAnchorRequirement], True)
BarrelStabilizer = MachinistSpell(3, False, 0, Lock, 0, 0, ApplyBarrelStabilizer, [BarrelStabilizerRequirement], False)
HeatBlast = MachinistSpell(7, True, Lock, 1.5, 180, 0, ApplyHeatBlast, [], True)
Hypercharge = MachinistSpell(8, False, 0, Lock, 0, 0, ApplyHypercharge, [HyperchargeRequirement], False)
Reassemble = MachinistSpell(9, False, 0, Lock, 0, 0, ApplyReassemble, [ReassembleRequirement], False)
GaussRound = MachinistSpell(10, False, 0, Lock, 120, 0, ApplyGaussRound, [GaussRoundRequirement], False)
Ricochet = MachinistSpell(11, False, 0, Lock, 120, 0, ApplyRicochet, [RicochetRequirement], False)
Drill = MachinistSpell(12, True, 0, 2.5, 580, 0, ApplyDrill, [DrillRequirement], True)
ChainSaw = MachinistSpell(17, True, 0, 2.5, 580, 0, ApplyChainSaw, [ChainSawRequirement], True)
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
Bunker = MachinistSpell(15, True, 0, 2.5, 680, 0, empty, [], False)   #Triggered by Overdrive
Collider = MachinistSpell(16, True, 0 , 2.5, 780, 0, ApplyCollider, [], False)  #Spell Queen will cast