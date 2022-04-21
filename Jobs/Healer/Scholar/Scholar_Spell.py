#########################################
########## SCHOLAR PLAYER ###############
#########################################

from Jobs.Healer.Healer_Spell import ScholarSpell

from Jobs.Base_Spell import DOTSpell, empty, ManaRequirement
import copy
Lock = 0.75

ScholarGCD = 2.5
ScholarCast = 1.5
        
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
        Player.EffectToRemove.append(CheckChainStratagem)

def CheckBiolysis(Player, Enemy):
    if Player.BiolysisTimer <= 0 : 
        Player.DOTList.remove(Player.Biolysis)
        Player.Biolysis = None
        Player.EffectToRemove.append(CheckBiolysis)

Broil = ScholarSpell(1, True, ScholarCast, ScholarGCD, 295,  400, empty, [ManaRequirement])
Ruin = ScholarSpell(2, True, 0, ScholarGCD, 220,  300, empty, [ManaRequirement])
Biolysis = ScholarSpell(3, True, 0, ScholarGCD, 0, 300, ApplyBiolysis, [ManaRequirement])
BiolysisDOT = DOTSpell(4, 70)
Aetherflow = ScholarSpell(5, False, 0, Lock, 0, 0, ApplyAetherflow, [AetherflowRequirement])
Dissipation = ScholarSpell(8, False, 0, Lock, 0, 0, ApplyDissipation, [DissipationRequirement])
ChainStratagem = ScholarSpell(6, False, 0, Lock, 0, 0, ApplyChainStratagem, [ChainStratagemRequirement])
EnergyDrain = ScholarSpell(7, False, 0, Lock, 100, 0, ApplyEnergyDrain, [AetherStackRequirement])