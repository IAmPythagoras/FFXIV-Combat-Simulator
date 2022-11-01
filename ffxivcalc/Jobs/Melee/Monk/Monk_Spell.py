from copy import deepcopy
from ffxivcalc.Jobs.Base_Spell import DOTSpell, buff, empty
from ffxivcalc.Jobs.Melee.Melee_Spell import MonkSpell
Lock = 0.75 #skill animation lock - simulating 75ms ping

#Requirements

def RaptorFormRequirement(Player, Spell):
    return Player.CurrentForm == 2 or Player.FormlessFistStack > 0, -1

def CoeurlFormRequirement(Player, Spell):
    return Player.CurrentForm == 3 or Player.FormlessFistStack > 0 , -1

def ThunderclapRequirement(Player, Spell):
    return Player.ThunderclapStack > 0, Player.ThunderclapCD

def MantraRequirement(Player, Spell):
    return Player.MantraCD <= 0, Player.MantraCD

def PerfectBalanceRequirement(Player, Spell):
    return Player.PerfectBalanceStack > 0, Player.PerfectBalanceCD

def ElixirFieldRequirement(Player, Spell):
    return Player.BeastChakraType() == 1, -1

def RisingPhoenixRequirement(Player, Spell):
    return Player.BeastChakraType() == 3, -1

def CelestialRevolutionRequirement(Player, Spell):
    return Player.BestChakraType() == 2, -1

def NadiRequirement(Player, Spell):
    return Player.MasterGauge[0] and Player.MasterGauge[4], -1

def BrotherhoodRequirement(Player, Spell):
    return Player.BrotherhoodCD <= 0, Player.BrotherhoodCD

def RiddleOfEarthRequirement(Player, Spell):
    return Player.RiddleOfEarthStack > 0, Player.RiddleOfEarthCD

def RiddleOfFireRequirement(Player, Spell):
    return Player.RiddleOfFireCD <= 0, Player.RiddleOfFireCD

def RiddleOfWindRequirement(Player, Spell):
    return Player.RiddleOfWindCD <= 0, Player.RiddleOfWindCD

def ChakraRequirement(Player, Spell):
    return Player.MaxChakraGate == 5, -1

#Apply

def ApplyFormShift(Player, Enemy):
    Player.FormlessFistStack += 1

def ApplyChakra(Player, Enemy):
    Player.UsedChakraGate += 5
    Player.MaxChakraGate = 0

def ApplyRiddleOfWind(Player, Enemy):
    Player.RiddleOfWindCD = 90
    Player.RiddleOfWindTimer = 15

def ApplyRiddleOfFire(Player, Enemy):
    Player.RiddleOfFireCD = 60
    Player.RiddleOfFireTimer = 20

    Player.EffectCDList.append(RiddleOfFireCheck)
    Player.buffList.append(RiddleOfFireBuff)

def ApplyRiddleOfEarth(Player, Enemy):
    if Player.RiddleOfEarthStack == 3:
        Player.EffectCDList.append(RiddleOfEarthStackCheck)
        Player.RiddleOfEarthCD = 30
    Player.RiddleOfEarthStack -= 1

def ApplyElixirField(Player, Enemy):
    Player.ResetMasterGauge()

    Player.MasterGauge[0] = True #Opening Lunar Nadi
    Player.FormlessFistStack += 1

def ApplyCelestialRevolution(Player, Enemy):
    Player.ResetMasterGauge()
    Player.FormlessFistStack += 1

    if Player.MasterGauge[0]: Player.MasterGauge[-1] = True #If lunar already opened open Solar
    else: Player.MasterGauge[0] = True

def ApplyRisingPhoenix(Player, Enemy):
    Player.ResetMasterGauge()

    Player.MasterGauge[-1] = True #Opening Solar Nadi
    Player.FormlessFistStack += 1

def ApplyPhantomRush(Player, Enemy):
    Player.ResetMasterGauge()
    Player.MasterGauge[0], Player.MasterGauge[-1] = False, False
    #Reset the whole Gauge
    Player.FormlessFistStack += 1

def ApplyThunderclap(Player, Enemy):
    if Player.ThunderclapStack == 3:
        Player.EffectCDList.append(ThunderclapStackCheck)
        Player.ThunderclapCD = 30
    Player.ThunderclapStack -= 1


def ApplyOpoOpo(Player, Enemy):
    FormlessStackCheck(Player)
    Player.CurrentForm = 1

def ApplyRaptor(Player, Enemy):
    FormlessStackCheck(Player)
    Player.CurrentForm = 2 #Into Raptor

def ApplyCoeurl(Player, Enemy):
    FormlessStackCheck(Player)
    Player.CurrentForm = 3 #Into Coeurl

def ApplyMantra(Player, Enemy):
    Player.MantraCD = 90

def ApplyPerfectBalance(Player, Enemy):
    if Player.PerfectBalanceStack == 2:
        Player.EffectCDList.append(PerfectBalanceStackCheck)
        Player.PerfectBalanceCD = 40
    Player.PerfectBalanceStack -= 1
    Player.PerfectBalanceEffectStack = 3
    Player.FormlessFistStack += 3
    Player.EffectList.append(PerfectBalanceEffect)

def ApplyMeditation(Player, Enemy):
    Player.MaxChakraGate += 1

def ApplyBrotherhood(Player, Enemy):
    # We will give everyone the 5% buff, and the effect that will
    # check for weaponskil/casted actions and we will assume that
    # all of them open a chakra gate

    def MeditativeBrotherhoodEffect(Target, Spell):
        if Spell.GCD:
            Player.OpenChakra() #Adds 1 chakra
            Player.ExpectedChakraGate += 0.2 #Add expected Chakra
    
    def MeditativeBrotherhoodCheck(Target, Enemy):
        if Target.MeditativeBrotherhoodTimer <= 0:
            Target.EffectList.remove(MeditativeBrotherhoodEffect)
            Target.EffectToRemove.append(MeditativeBrotherhoodCheck)
            Target.buffList.remove(BrotherhoodBuff)


    def MonkMeditativeEffect(Target, Spell):
        #This one goes on the Monk
        if Spell.GCD:
            Target.ExpectedChakraGate += 1
            Target.OpenChakra()
            
    def MonkMeditativeCheck(Target, Spell):
        if Target.MeditativeBrotherhoodTimer <= 0:
            Target.EffectList.remove(MonkMeditativeEffect)
            Target.EffectToRemove.append(MonkMeditativeCheck)
            Target.buffList.remove(BrotherhoodBuff)



    for Target in Player.CurrentFight.PlayerList:
        if Target == Player:
            #Need special effect for the Monk
            Target.EffectList.append(MonkMeditativeEffect)
            Target.EffectCDList.append(MonkMeditativeCheck)
            Target.buffList.append(BrotherhoodBuff)
        else:
            #Applying MeditativeBrotherhood to every other player
            Target.EffectList.append(MeditativeBrotherhoodEffect)
            Target.EffectCDList.append(MeditativeBrotherhoodCheck)
            Target.buffList.append(BrotherhoodBuff) #Adding buff
#Effect

def LeadenFistEffect(Player, Spell):
    if Spell.id == Bootshine.id: Spell.Potency += 100

#Check

def RiddleOfFireCheck(Player, Enemy):
    if Player.RiddleOfFireTimer <= 0:
        Player.buffList.remove(RiddleOfFireBuff)
        Player.EffectToRemove.append(RiddleOfFireCheck)

def RiddleOfEarthStackCheck(Player, Enemy):
    if Player.RiddleOfEarthCD <= 0:
        if Player.RiddleOfEarthStack == 2:
            Player.EffectToRemove.append(RiddleOfEarthStackCheck)
        else:
            Player.RiddleOfEarthCD = 30
        Player.RiddleOfEarthStack += 1

def PerfectBalanceStackCheck(Player, Enemy):
    if Player.PerfectBalanceCD <= 0:
        if Player.PerfectBalanceStack == 1:
            Player.EffectToRemove.append(PerfectBalanceStackCheck)
        else:
            Player.PerfectBalanceTimer = 40
        Player.PerfectBalanceStack += 1

def ThunderclapStackCheck(Player, Enemy):
    if Player.ThunderclapCD <= 0:
        if Player.ThunderclapStack == 2:
            Player.EffectToRemove.append(ThunderclapStackCheck)
        else:
            Player.ThunderclapTimer = 30
        Player.ThunderclapStack += 1

def DemolishDOTCheck(Player, Enemy):
    if Player.DemolishDOTTimer <= 0:
        Player.DOTList.remove(Player.DemolishDOT)
        Player.DemolishDOT = None
        Player.EffectToRemove.append(DemolishDOTCheck)

def DisciplinedFistCheck(Player, Enemy):
    if Player.DisciplinedFistTimer <= 0:
        Player.buffList.remove(DisciplinedFistBuff)
        Player.EffectToRemove.append(DisciplinedFistCheck)

def LeadenFistCheck(Player, Enemy):
    if Player.LeadenFistTimer <= 0:
        Player.EffectList.remove(LeadenFistEffect)
        Player.EffectToRemove.append(LeadenFistCheck)

#Combo Effect

def PerfectBalanceEffect(Player, Spell):
    if Spell.GCD:
        if Spell.id == Bootshine.id or Spell.id == ShadowOfTheDestroyer.id or Spell.id == DragonKick.id:
            Player.addBeastChakra(1)
            Player.PerfectBalanceEffectStack -= 1
        elif Spell.id == TrueStrike.id or Spell.id == TwinSnakes.id or Spell.id == FourpointFurry.id:
            Player.addBeastChakra(2)
            Player.PerfectBalanceEffectStack -= 1
        elif Spell.id == Demolish.id or Spell.id == SnapPunch.id or Spell.id == Rockbreaker.id:
            Player.addBeastChakra(3)
            Player.PerfectBalanceEffectStack -= 1

    if Player.PerfectBalanceEffectStack == 0:
        Player.EffectToRemove.append(PerfectBalanceEffect)

def ComboEffect(Player, Spell):
    # This effect will always be on and will check what form the player is in and use the
    # necessary effect
    if Spell.GCD:
        if Player.FormlessFistStack > 0 :#Then we are in formless, so we can do whichever

            Player.UsedFormlessStack = True

            #Opo-Opo Form
            if Spell.id == Bootshine.id or Spell.id == ShadowOfTheDestroyer.id:
                Player.GuaranteedCrit = True
            elif Spell.id == DragonKick.id:
                #Grants Leaden Fist
                if Player.LeadenFistTimer == 0: #If not already applied
                    Player.EffectList.append(LeadenFistEffect)
                    Player.EffectCDList.append(LeadenFistCheck)
                Player.LeadenFistTimer = 30

            #Raptor Form

            elif Spell.id == TrueStrike.id: #Nothing happens
                pass
            elif Spell.id == TwinSnakes.id or Spell.id == FourpointFurry.id:
                if Player.DisciplinedFistTimer == 0:
                    Player.buffList.append(DisciplinedFistBuff)
                    Player.EffectCDList.append(DisciplinedFistCheck)
                Player.DisciplinedFistTimer = 15

            #Coeurl Form

            elif Spell.id == Demolish.id:
                if Player.DemolishDOT == None:
                    Player.DemolishDOT = deepcopy(DemolishDOT)
                    Player.EffectCDList.append(DemolishDOTCheck)
                    Player.DOTList.append(Player.DemolishDOT)
                Player.DemolishDOTTimer = 18
            elif Spell.id == SnapPunch.id or Spell.id == Rockbreaker.id:
                pass #Nothing happens

        #Not formless
        elif Player.CurrentForm == 1: #Opo-Opo form
            if Spell.id == Bootshine.id or Spell.id == ShadowOfTheDestroyer.id:
                Player.GuaranteedCrit = True
            elif Spell.id == DragonKick.id:
                #Grants Leaden Fist
                if Player.LeadenFistTimer == 0: #If not already applied
                    Player.EffectList.append(LeadenFistEffect)
                    Player.EffectCDList.append(LeadenFistCheck)
                Player.LeadenFistTimer = 30
        elif Player.CurrentForm == 2 : #Raptor Form
            if Spell.id == TrueStrike.id: #Nothing happens
                pass
            elif Spell.id == TwinSnakes.id or Spell.id == FourpointFurry.id:
                if Player.DisciplinedFistTimer == 0:
                    Player.buffList.append(DisciplinedFistBuff)
                    Player.EffectCDList.append(DisciplinedFistCheck)
                Player.DisciplinedFistTimer = 15
        elif Player.CurrentForm == 3 : #Coeurl Form
            if Spell.id == Demolish.id:
                if Player.DemolishDOT == None:
                    Player.DemolishDOT = deepcopy(DemolishDOT)
                    Player.EffectCDList.append(DemolishDOTCheck)
                    Player.DOTList.append(Player.DemolishDOT)
                Player.DemolishDOTTimer = 18
            elif Spell.id == SnapPunch.id or Spell.id == Rockbreaker.id:
                pass #Nothing happens


#Other

def FormlessStackCheck(Player):
    if Player.UsedFormlessStack:
        Player.UsedFormlessStack = False
        Player.FormlessFistStack -= 1

#Opo-opo form  -> Raptor Form
Bootshine = MonkSpell(53, True, 2, 210, ApplyRaptor, [], True, False)
DragonKick = MonkSpell(74, True, 2, 320, ApplyRaptor, [], True, False)
ShadowOfTheDestroyer = MonkSpell(25767, True,2, 110, ApplyRaptor, [], True, False) #AOE of Bootshine

#Raptor form combo -> Coeurl form
TrueStrike = MonkSpell(54, True, 2, 300, ApplyCoeurl, [RaptorFormRequirement], True, False)
TwinSnakes = MonkSpell(61, True, 2, 280, ApplyCoeurl, [RaptorFormRequirement], True, False)
FourpointFurry = MonkSpell(16473, True, 2, 120, ApplyCoeurl, [RaptorFormRequirement], True, False) #AOE of Twinsnakes

#Coeurl form combo -> Opo-opo form
Demolish = MonkSpell(66, True, 2, 130, ApplyOpoOpo, [CoeurlFormRequirement], True, False)
DemolishDOT = DOTSpell(-10, 70, True)
SnapPunch = MonkSpell(56, True,2 ,310, ApplyOpoOpo, [CoeurlFormRequirement], True, False)
Rockbreaker = MonkSpell(70, True, 2, 130, ApplyOpoOpo, [CoeurlFormRequirement], True, False)

#Chakra
TheForbiddenChakra = MonkSpell(3547, False, 0, 340, ApplyChakra, [ChakraRequirement], False, False )
Enlightenment = MonkSpell(16474, False, 0, 170, ApplyChakra, [ChakraRequirement], False, False)
#Masterful Blitz
ElixirField = MonkSpell(3545, True, 2, 600, ApplyElixirField, [ElixirFieldRequirement], True, False)
CelestialRevolution = MonkSpell(25765, True, 2, 450, ApplyCelestialRevolution, [CelestialRevolutionRequirement], True, False)
RisingPhoenix = MonkSpell(25768, True, 2, 700, ApplyRisingPhoenix, [RisingPhoenixRequirement], True, False)
PhantomRush = MonkSpell(25769, True, 2, 1150, ApplyPhantomRush, [RisingPhoenixRequirement, NadiRequirement], True, False)
#Other GCD
Meditation = MonkSpell(3546, False, 0, 0, ApplyMeditation, [], False, False)
FormShift = MonkSpell(4262, True, 2, 0, ApplyFormShift, [], False, False)
SixSidedStar = MonkSpell(16476, True, 4, 550, empty, [], True, False)
#oGCD
PerfectBalance = MonkSpell(69, False, 0, 0, ApplyPerfectBalance, [PerfectBalanceRequirement], False, False)
Brotherhood = MonkSpell(7396, False, 0, 0, ApplyBrotherhood, [BrotherhoodRequirement], False, False)
RiddleOfFire = MonkSpell(7395, False, 0, 0, ApplyRiddleOfFire, [RiddleOfFireRequirement], False, False)
RiddleOfEarth = MonkSpell(7394, False, 0, 0, ApplyRiddleOfEarth, [RiddleOfEarthRequirement], False, False)
RiddleOfWind = MonkSpell(25766, False, 0, 0, ApplyRiddleOfWind, [RiddleOfWindRequirement], False, False)
#non Damage oGCD
Anatman = MonkSpell(16475, False, 0, 0, empty, [], False, False)
Thunderclap = MonkSpell(25762, False, 0, 0, ApplyThunderclap, [ThunderclapRequirement],False, False)
Mantra = MonkSpell(65, False, 0, 0, ApplyMantra, [MantraRequirement], False, False)
#Buff
DisciplinedFistBuff = buff(1.15)
BrotherhoodBuff = buff(1.05)
RiddleOfFireBuff = buff(1.15)



MonkAbility = {
53 : Bootshine,
54 : TrueStrike,
66 : Demolish,
74 : DragonKick,
61 : TwinSnakes,
56 : SnapPunch,
25767 : ShadowOfTheDestroyer,
16473 : FourpointFurry,
70 : Rockbreaker,
3546 : Meditation,
3547 : TheForbiddenChakra,
16474 : Enlightenment,
69 : PerfectBalance,
3545 : ElixirField,
25765 : CelestialRevolution,
25768 : RisingPhoenix,
25769 : PhantomRush,
16476 : SixSidedStar,
4262 : FormShift,
25762 : Thunderclap,
7394 : RiddleOfEarth,
7395 : RiddleOfFire,
25766 : RiddleOfWind,
7396 : Brotherhood,
16475 : Anatman,
65 : Mantra

}