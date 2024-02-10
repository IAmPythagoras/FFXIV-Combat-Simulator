#########################################
########## SCHOLAR PLAYER ###############
#########################################

from ffxivcalc.Jobs.Healer.Healer_Spell import ScholarSpell
from ffxivcalc.Jobs.Player import HealingBuff, MitBuff

from ffxivcalc.Jobs.Base_Spell import DOTSpell, empty, ManaRequirement, buffHistory
import copy
Lock = 0.75

def AetherflowRequirement(Player, Spell):
    return Player.AetherFlowCD <= 0, Player.AetherFlowCD

def ChainStratagemRequirement(Player, Spell):
    return Player.ChainStratagemCD <= 0, Player.ChainStratagemCD

def AetherStackRequirement(Player, Spell):
    return Player.AetherFlowStack > 0, -1

def DissipationRequirement(Player, Spell):
    return Player.DissipationCD <= 0 and Player.SummonTimer <= 0, Player.DissipationCD #Cannot use while summoned

def ExpedientRequirement(Player, Spell):
    return Player.ExpedientCD <= 0, Player.ExpedientCD

def ProtractionRequirement(Player, Spell):
    return Player.ProtractionCD <= 0, Player.ProtractionCD

def RecitationRequirement(Player, Spell):
    return Player.RecitationCD <= 0, Player.RecitationCD

def EmergencyTacticRequirement(Player, Spell):
    return Player.EmergencyTacticCD <= 0, Player.EmergencyTacticCD

def DeploymentTacticRequirement(Player, Spell):
    return Player.DeploymentTacticCD <= 0, Player.DeploymentTacticCD

def IndomitabilityRequirement(Player, Spell):
    return Player.IndomitabilityCD <= 0, Player.IndomitabilityCD

def LustrateRequirement(Player, Spell):
    return Player.LustrateCD <= 0, Player.LustrateCD

def SacredSoilRequirement(Player, Spell):
    return Player.SacredSoilCD <= 0, Player.SacredSoilCD

def ExcogitationRequirement(Player, Spell):
    return Player.ExcogitationCD <= 0, Player.ExcogitationCD

def AdloquiumRequirement(Player, Spell):
    if Player.Recitation:
        return True, -1 #if we have it
    else:
        return ManaRequirement(Player, Spell) #Else return ManaRequirement

def AetherHealRequirement(Player, Spell):
    return Player.AetherFlowStack > 0 or Player.Recitation, -1

def SummonSeraphRequirement(Player, Spell):
    return Player.SummonSeraphCD <= 0, Player.SummonSeraphCD

def ConsolationRequirement(Player, Spell):
    return Player.ConsolationStack > 0, -1

def FeyBlessingRequirement(Player, Spell):
    return Player.FeyBlessingCD <= 0, Player.FeyBlessingCD

def FeyIlluminationRequirement(Player, Spell):
    return Player.FeyIlluminationCD <= 0, Player.FeyIlluminationCD

def WhisperingDawnRequirement(Player, Spell):
    return Player.WhisperingDawnCD <= 0, Player.WhisperingDawnCD

#====================================

def ApplyFeyBlessing(Player, Enemy):
    Player.FeyBlessingCD = 60

def ApplyFeyIllumination(Player, Enemy):
    Player.FeyIlluminationCD = 120

    for player in Player.CurrentFight.PlayerList:
        player.AddHealingBuff(HealingBuff(1.1, 20, player, GivenHealBuff=False, BuffName="FeyIllumination"))
        player.AddMitBuff(MitBuff(0.95, 20, player, MagicMit=True, BuffName="FeyIllumination"))

def ApplyWhisperingDawn(Player, Enemy):
    Player.WhisperingDawnCD = 60

def Apply(Player, Enemy):
    Player.CD = 0
    Player.AetherFlowStack -= 1

def ApplyConsolation(Player, Enemy):
    Player.ConsolationStack -= 1

def ApplySummonSeraph(Player, Enemy):
    Player.SummonTimer = 22
    Player.SummonSeraphCD = 120
    Player.ConsolationStack = 2

def ApplyIndomitability(Player, Enemy):
    Player.IndomitabilityCD = 30
    if Player.Recitation : Player.Recitation = False
    else: Player.AetherFlowStack -= 1

def ApplyLustrate(Player, Enemy):
    Player.LustrateCD = 1
    Player.AetherFlowStack -= 1

def ApplySacredSoil(Player, Enemy):
    Player.SacredSoilCD = 30
    Player.AetherFlowStack -= 1

    for player in Player.CurrentFight.PlayerList:
        player.AddMitBuff(MitBuff(0.9, 15, player, BuffName="SacredSoil"))

def ApplyExcogitation(Player, Enemy):
    Player.ExcogitationCD = 45
    if Player.Recitation : Player.Recitation = False
    else: Player.AetherFlowStack -= 1

def ApplyAdloquium(Player, Enemy):
    if Player.Recitation : Player.Recitation = False

def ApplyExpedient(Player, Enemy):
    Player.ExpedientCD = 120

    for player in Player.CurrentFight.PlayerList:
        player.AddMitBuff(MitBuff(0.9, 20, player, BuffName="Expedient"))

def ApplyProtraction(Player, Enemy):
    Player.ProtractionCD = 60

def ApplyRecitation(Player, Enemy):
    Player.RecitationCD = 90
    Player.Recitation = True

def ApplyEmergencyTactic(Player, Enemy):
    Player.EmergencyTacticCD = 15

def ApplyDeploymentTactic(Player, Enemy):
    Player.DeploymentTacticCD = 90
        
def ApplyBiolysis(Player, Enemy):
    if (not (Player.Biolysis in Player.DOTList)):
        Player.Biolysis = copy.deepcopy(BiolysisDOT)
        Player.DOTList.append(Player.Biolysis)
        Player.EffectCDList.append(CheckBiolysis)
    else : Player.Biolysis.resetBuffSnapshot() # If already applied reset snapshot
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

                                     # Only doing this if SavePreBakedAction is true
    #if Player.CurrentFight.SavePreBakedAction:
    #    fight = Player.CurrentFight
    #    history = buffHistory(fight.TimeStamp, fight.TimeStamp + 15)
    #    fight.PlayerList[fight.PlayerIDSavePreBakedAction].ChainStratagemHistory.append(history)

def ApplyEnergyDrain(Player, Enemy):
    Player.EnergyDrainCD = 1
    Player.AetherFlowStack -= 1

def ApplyDissipation(Player, Enemy):
    Player.DissipationCD = 180
    Player.AetherFlowStack = 3
    Player.GivenHealBuffList.append(HealingBuff(1.2, 30, Player, BuffName="Dissipation"))

#===================================

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




#DamageGCD
Broil = ScholarSpell(25865, True, 1.5, 2.5, 295,  400, empty, [ManaRequirement], type = 1)
Ruin = ScholarSpell(17870, True, 0, 2.5, 220,  300, empty, [ManaRequirement], type = 1)
Biolysis = ScholarSpell(16540, True, 0, 2.5, 0, 300, ApplyBiolysis, [ManaRequirement], type = 1)
BiolysisDOT = DOTSpell(-4, 70, False)
ArtOfWar = ScholarSpell(25866, True, 0, 2.5, 165, 400, empty, [ManaRequirement], type = 1)#AOE

#HealGCD
Succor = ScholarSpell(186, True, 2, 2.5, 200, 1000, ApplyAdloquium, [AdloquiumRequirement], type = 1) ##This action has apply and requirement because of recitation. 160% shield
Adloquium = ScholarSpell(185, True, 2, 2.5, 300, 1000, ApplyAdloquium, [AdloquiumRequirement], type = 1) #This action has apply and requirement because of recitation. 180% shield
Physick = ScholarSpell(190, True, 1.5, 2.5, 450, 400, empty, [ManaRequirement], type = 1)
SummonEos = ScholarSpell(29, True, 1.5, 2.5, 0, 200, empty, [ManaRequirement], type = 1)
Resurrection = ScholarSpell(173, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])
#Damage oGCD
ChainStratagem = ScholarSpell(7436, False, 0, Lock, 0, 0, ApplyChainStratagem, [ChainStratagemRequirement])
EnergyDrain = ScholarSpell(167, False, 0, Lock, 100, 0, ApplyEnergyDrain, [AetherStackRequirement])
Aetherflow = ScholarSpell(166, False, 0, Lock, 0, 0, ApplyAetherflow, [AetherflowRequirement])
Dissipation = ScholarSpell(3587, False, 0, Lock, 0, 0, ApplyDissipation, [DissipationRequirement])
#Heal oGCD
Expedient = ScholarSpell(25868, False, 0, 0, 0, 0, ApplyExpedient, [ExpedientRequirement])
Protraction = ScholarSpell(25867, False, 0, 0, 0, 0, ApplyProtraction, [ProtractionRequirement])
Recitation = ScholarSpell(16542, False, 0, 0, 0, 0, ApplyRecitation, [RecitationRequirement])
EmergencyTactic = ScholarSpell(3586, False, 0, 0, 0, 0, ApplyEmergencyTactic, [EmergencyTacticRequirement])
DeploymentTactic = ScholarSpell(3585, False, 0, 0, 0, 0, ApplyDeploymentTactic, [DeploymentTacticRequirement])

#AetherFlow Heal spell
Excogitation = ScholarSpell(7434, False, 0, 0, 0, 0, ApplyExcogitation, [ExcogitationRequirement,AetherHealRequirement]) #Can be used by recitation
SacredSoil = ScholarSpell(188, False, 0, 0, 0, 0, ApplySacredSoil, [SacredSoilRequirement,AetherflowRequirement])
Lustrate = ScholarSpell(189, False, 0, 0, 600, 0, ApplyLustrate, [LustrateRequirement,AetherflowRequirement])
Indomitability = ScholarSpell(3583, False, 0, 0, 400, 0, ApplyIndomitability, [IndomitabilityRequirement,AetherHealRequirement], AOEHeal=True)#Can be used by recitation

#Fey Healing
Consolation = ScholarSpell(16546, False, 0, 0, 0, 0, ApplyConsolation, [ConsolationRequirement])
SummonSeraph = ScholarSpell(16545, False, 0, 0, 250, 0, ApplySummonSeraph, [SummonSeraphRequirement], AOEHeal=True) # 100% shield
FeyBlessing = ScholarSpell(16543, False, 0, 0, 320, 0, ApplyFeyBlessing, [FeyBlessingRequirement], AOEHeal=True)
Aetherpact = ScholarSpell(7437, False, 0, 0, 0, 0, empty, []) #No requirement, since 3 sec cd, so not really worth it imo
DissolveUnion = ScholarSpell(7869, False, 0, 0, 0, 0, empty, [])
FeyIllumination = ScholarSpell(16538, False, 0, 0, 0, 0, ApplyFeyIllumination, [FeyIlluminationRequirement])
WhisperingDawn = ScholarSpell(16537, False, 0, 0, 0, 0, ApplyWhisperingDawn, [WhisperingDawnRequirement])

ScholarAbility = {
166 : Aetherflow, 
167 : EnergyDrain, 
185 : Adloquium,  
186 : Succor, 
188 : SacredSoil, 
189 : Lustrate, 
190 : Physick, 
3583 : Indomitability, 
3585 : DeploymentTactic, 
3586 : EmergencyTactic,
3587 : Dissipation, 
7434 : Excogitation, 
7436 : ChainStratagem, 
7437 : Aetherpact, 
16537 : WhisperingDawn, 
16538 : FeyIllumination, 
16542 : Recitation, 
16543 : FeyBlessing, 
16545 : SummonSeraph,
17215 : SummonEos, 
25868 : Expedient, 
25867 : Protraction, 
25866 : ArtOfWar, 
25865 : Broil, 
17870 : Ruin, 
16540 : Biolysis,
16546 : Consolation,
173 : Resurrection,
7869 : DissolveUnion
}