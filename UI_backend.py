import copy
import json
import os
from Jobs.Melee.Monk.Monk_Spell import ComboEffect

from Jobs.Melee.Ninja.Ninja_Spell import ApplyHuton
from Jobs.Melee.Samurai.Samurai_Spell import MeikyoCheck, MeikyoEffect, MeikyoStackCheck


from Jobs.Ranged.Dancer.Dancer_Spell import EspritEffect
from Jobs.Ranged.Bard.Bard_Spell import SongEffect
from Jobs.Tank.DarkKnight.DarkKnight_Spell import BloodWeaponCheck, BloodWeaponEffect
from Jobs.Tank.Warrior.Warrior_Spell import SurgingTempestEffect
from Jobs.Caster.Redmage.Redmage_Spell import DualCastEffect
from Jobs.Caster.Blackmage.BlackMage_Spell import ElementalEffect, EnochianEffect

from Fight import Fight
from Enemy import Enemy
from FFLogsAPIRequest import getAbilityList, lookup_abilityID
from Jobs.Base_Spell import PrepullPotion, WaitAbility

#CASTER
from Jobs.Caster.Summoner.Summoner_Player import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *
#HEALER
from Jobs.Healer.Sage.Sage_Player import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *
#RANGED
from Jobs.Ranged.Machinist.Machinist_Player import *
from Jobs.Ranged.Bard.Bard_Player import *
from Jobs.Ranged.Dancer.Dancer_Player import *
#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import *
from Jobs.Tank.DarkKnight.DarkKnight_Player import *
from Jobs.Tank.Warrior.Warrior_Player import *
from Jobs.Tank.Paladin.Paladin_Player import *
#MELEE
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *
from Jobs.Melee.Monk.Monk_Player import *

#This file will take care of request by TUI.py and return whatever needs to be returned

# ============================================================================================

# These are the stats that will be used when importing from FFLogs. Make sure to change them accordingly

# Caster
BLMStat = {"MainStat": 2945, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 840, "Crit" : 2386, "DH" : 1307} # Stats for BlackMage
RDMStat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "Crit" : 2397, "DH" : 1544} # Stats for RedMage
SMNStat = {"MainStat": 2948, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 544, "Crit" : 2436, "DH" : 1544} # Stats for Summoner

# Healer
SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "Crit" : 2351, "DH" : 436} # Stats for Scholar
WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage
ASTStat = {"MainStat": 2949, "WD":126, "Det" : 1659, "Ten" : 400, "SS": 1473, "Crit" : 2280, "DH" : 436} # Stats for Astrologian
SGEStat = {"MainStat": 2928, "WD":126, "Det" : 1859, "Ten" : 400, "SS": 827, "Crit" : 2312, "DH" : 1012} # Stats for Sage

# Physical Ranged
MCHStat = {"MainStat": 2937, "WD":126, "Det" : 1598, "Ten" : 400, "SS": 400, "Crit" : 2389, "DH" : 1592} # Stats for Machinist
BRDStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Bard
DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer

# Melee
NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
SAMStat = {"MainStat": 2937, "WD":126, "Det" : 1571, "Ten" : 400, "SS": 508, "Crit" : 2446, "DH" : 1459} # Stats for Samurai
DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon
MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
RPRStat = {"MainStat": 2946, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Reaper

# Tank
DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
WARStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for Warrior
PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

# ============================================================================================

def ImportFightBackend(fightID,fightNumber):

    Event = Fight([], Enemy(), False) #Creating event

    action_dict, player_dict = getAbilityList(fightID, fightNumber) #getting ability List
    
    for playerID in player_dict:

        player_dict[playerID]["job_object"].ActionSet = action_dict[playerID]
        player_dict[playerID]["job_object"].CurrentFight = Event
        job_name = player_dict[playerID]["job"] #getting job name

        if job_name == "Sage" : player_dict[playerID]["job_object"].Stat = SGEStat
        elif job_name == "Scholar" : player_dict[playerID]["job_object"].Stat = SCHStat
        elif job_name == "WhiteMage" : player_dict[playerID]["job_object"].Stat = WHMStat
        elif job_name == "Astrologian" : player_dict[playerID]["job_object"].Stat = ASTStat
        elif job_name == "Warrior" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(WARStat)
        elif job_name == "DarkKnight" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRKStat)
            player_dict[playerID]["job_object"].EffectList = [BloodWeaponEffect] #Assuming we pre pull it
            player_dict[playerID]["job_object"].EffectCDList = [BloodWeaponCheck]
        elif job_name == "Paladin" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(PLDStat)
            player_dict[playerID]["job_object"].EffectList = [OathGauge]
        elif job_name == "Gunbreaker" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(GNBStat)
        #Caster
        elif job_name == "BlackMage" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(BLMStat)
            player_dict[playerID]["job_object"].EffectList = [EnochianEffect, ElementalEffect]
        elif job_name == "RedMage" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(RDMStat)
            player_dict[playerID]["job_object"].EffectList = [DualCastEffect]
        elif job_name == "Summoner" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(SMNStat)
        #Ranged
        elif job_name == "Dancer" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(DNCStat)
            player_dict[playerID]["job_object"].EffectList = [EspritEffect]
        elif job_name == "Machinist" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(MCHStat)
        elif job_name == "Bard" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(BRDStat)
            player_dict[playerID]["job_object"].EffectList = [SongEffect]
        #melee
        elif job_name == "Reaper" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(RPRStat)
        elif job_name == "Monk" :              
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(MNKStat)

        elif job_name == "Dragoon" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRGStat)
        elif job_name == "Ninja" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(NINStat)
        elif job_name == "Samurai" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(SAMStat)

        Event.PlayerList.append(player_dict[playerID]["job_object"])

    Event.RequirementOn = False #By default making false

    Event.SimulateFight(0.01, 1000, 0)

    return Event


def AskInput(range):
    #This function will ask a numerical value to the user where range is the number of options
    #The inputs are assumed to be numerically ordered and starting at 1 and finishing at (range)
    user_input = input("Enter a number to select that option : ")

    while True:
        if int(user_input) >= 1 and int(user_input) <= range: #if input is valid
            return user_input
        else : #Non-valid input
            user_input = input("This is not a valid input. Please enter a valid number : ")



def SaveFight(Event, countdown, fightDuration, saveName):
    #This function will save a fight into memory.

    #The file will be saved as a JSON format

    PlayerListDict = []
    PlayerIDList = [] #list of all player IDs so we don't have duplicates

    for Player in Event.PlayerList:
        #Going through all players in the Event
        PlayerDict = {} #Empty dictionnary

        if isinstance(Player, BlackMage) : PlayerDict["JobName"] = "BlackMage"
        elif isinstance(Player, Redmage) : PlayerDict["JobName"] = "RedMage"
        elif isinstance(Player, DarkKnight) : PlayerDict["JobName"] = "DarkKnight"
        elif isinstance(Player, Warrior) : PlayerDict["JobName"] = "Warrior"
        elif isinstance(Player, Paladin) : PlayerDict["JobName"] = "Paladin"
        elif isinstance(Player, Gunbreaker) : PlayerDict["JobName"] = "Gunbreaker"
        elif isinstance(Player, Machinist) : PlayerDict["JobName"] = "Machinist"
        elif isinstance(Player, Samurai) : PlayerDict["JobName"] = "Samurai"
        elif isinstance(Player, Ninja) : PlayerDict["JobName"] = "Ninja"
        elif isinstance(Player, Scholar) : PlayerDict["JobName"] = "Scholar"
        elif isinstance(Player, Whitemage) : PlayerDict["JobName"] = "WhiteMage"
        elif isinstance(Player, Astrologian) : PlayerDict["JobName"] = "Astrologian"
        elif isinstance(Player, Sage) : PlayerDict["JobName"] = "Sage"
        elif isinstance(Player, Summoner) : PlayerDict["JobName"] = "Summoner"
        elif isinstance(Player, Dragoon) : PlayerDict["JobName"] = "Dragoon"
        elif isinstance(Player, Reaper) : PlayerDict["JobName"] = "Reaper"
        elif isinstance(Player, Bard) : PlayerDict["JobName"] = "Bard"
        elif isinstance(Player, Dancer): PlayerDict["JobName"] = "Dancer"
        elif isinstance(Player, Monk): PlayerDict["JobName"] = "Monk"


        while Player.playerID in PlayerIDList:
            Player.playerID += 1

        PlayerDict["playerID"] = Player.playerID

        PlayerIDList += [Player.playerID]

        PlayerDict["stat"] = Player.Stat
        actionList = []

        PlayerDict["Auras"] = copy.deepcopy(Player.auras)

        for action in Player.ActionSet:
            actionDict = {}
            #Special case for WaitAbility
            if action.id == 212 : #WaitAbility
                if action.waitTime != 0:
                    actionDict["actionID"] = 212
                    actionDict["sourceID"] = Player.playerID
                    actionDict["targetID"] = 0 #id 0 is by default the main enemy
                    actionDict["isGCD"] = False
                    actionDict["waitTime"] = action.waitTime

                    actionList.append(copy.deepcopy(actionDict))#adding to dict
            else: #Normal ability
                actionDict["actionID"] = action.id 
                actionDict["sourceID"] = Player.playerID
                actionDict["targetID"] = action.TargetID #id 0 is by default the main enemy
                actionDict["isGCD"] = action.GCD

                actionList.append(copy.deepcopy(actionDict))#adding to dict

        PlayerDict["actionList"] = copy.deepcopy(actionList)

        PlayerListDict.append(copy.deepcopy(PlayerDict))

    


    data = {"data" : {
                "fightInfo" : {
                    "countdownValue" : countdown,
                    "fightDuration" : fightDuration,
                    "time_unit" : 0.01,
                    "ShowGraph" : Event.ShowGraph,
                    "RequirementOn" : Event.RequirementOn
                },
                "PlayerList" : PlayerListDict
    }}
    save_dir = os.getcwd() + "\\saved"
    with open(save_dir + "\\" + saveName + ".json", "w") as write_files:
        json.dump(data,write_files, indent=4) #saving file



def SimulateFightBackend(file_name):
    #Will read the fight in memory and transform it into an Event we can simulate
    #The memory will contain a file with a Job name and a list of actionID that we will transform into
    #an event.

    #the name of the save file will always be "save.json"

    f = open(file_name) #Opening save

    data = json.load(f) #Loading json file

    #The file is formated like so 
    #   {
    #	"data" : {
    #		"PlayerList": [
    #		{
    #			"JobName" : "Blackmage",
    #           "playerID" : "1",
    #			"actionList" : [
    #			{
    #				"actionID" : "12",
    #				"actionName" : "Fire4",
    #               "sourceID" : "1",
    #               "targetID" : "63"
    #			},
    #           ...
    #			]
    #		},
    #       ...
    #		]
    #	}

    #So we will go through the PlayerList and then through all the actionList

    PlayerList = data["data"]["PlayerList"] #Player List
    fightInfo = data["data"]["fightInfo"] #fight information

    if len(PlayerList) > 1 : #If there is more than 1 player we will ask if we wish to simulate all or only 1
        print(
            "This save file has more than one player character : " + "\n" + 
            "1- Simulate only one player character" + "\n" + 
            "2- Simulate all the player character at the same time" + "\n" + 
            "====================================================="
            )

        user_input = AskInput(2)

        if user_input == "1" : #want to only simulate one player
            print(
                "=====================================================" + "\n" + 
                "List of player in this save file : "
            )
            n_player = len(PlayerList)
            for i in range(n_player):
                print(str(i + 1) + " -> " + PlayerList[i]["JobName"])
            
            print("Select which player character you wish to simulate.")

            user_input = AskInput(n_player)

            PlayerList = [PlayerList[int(user_input) - 1]] #Only taking what we are interested in

    #We will now go through all actionID and transform into an abilityList

    print("Restoring save file into Event object...")
    PlayerActionList = {} #Dictionnary containing all player with their action

    closed_position = False
    dance_partner_flag = False
    dance_partner = None
    dancer = None

    for player in PlayerList: #Going through all player in PlayerList and creating JobObject
        #Will check what job the player is so we can create a player object of the relevant job

        job_name = player["JobName"]
        job_object = None
        #Healer
        if job_name == "Sage" : job_object = Sage(2.5, [], [], [], None, {})
        elif job_name == "Scholar" : job_object = Scholar(2.5, [], [], [], None, {})
        elif job_name == "WhiteMage" : job_object = Whitemage(2.5, [], [], [], None, {})
        elif job_name == "Astrologian" : job_object = Astrologian(2.5, [], [], [], None, {})
        #Tank
        elif job_name == "Warrior" : job_object = Warrior(2.5, [], [], [SurgingTempestEffect], None, {})
        elif job_name == "DarkKnight" : job_object = DarkKnight(2.5, [], [], [], None, {})
        elif job_name == "Paladin" : job_object = Paladin(2.5, [], [], [OathGauge], None, {})
        elif job_name == "Gunbreaker" : job_object = Gunbreaker(2.5, [], [], [], None, {})
        #Caster
        elif job_name == "BlackMage" : job_object = BlackMage(2.5, [], [], [EnochianEffect, ElementalEffect], None, {})
        elif job_name == "RedMage" : job_object = Redmage(2.5, [], [], [DualCastEffect], None, {})
        elif job_name == "Summoner" : job_object = Summoner(2.5, [], [], [], None, {})
        #Ranged
        elif job_name == "Dancer" : job_object = Dancer(2.5, [], [], [EspritEffect], None, {})
        elif job_name == "Machinist" : job_object = Machinist(2.5, [], [], [], None, {})
        elif job_name == "Bard" : job_object = Bard(2.5, [], [], [SongEffect], None, {})
        #melee
        elif job_name == "Reaper" : job_object = Reaper(2.5, [], [], [], None, {})
        elif job_name == "Monk" : job_object = Monk(2.5, [], [], [ComboEffect], None, {})
        elif job_name == "Dragoon" : job_object = Dragoon(2.5, [], [], [], None, {})
        elif job_name == "Ninja" : job_object = Ninja(2.5, [], [], [], None, {})
        elif job_name == "Samurai" : job_object = Samurai(2.5, [], [], [], None, {})
        

        job_object.playerID = player["playerID"] #Giving the playerID

        PlayerActionList[str(job_object.playerID)] = {"job" : job_name, "job_object" : job_object, "actionList" : player["actionList"], "actionObject" : []} #Adding new Key accessible by IDs

        #Giving player object the stat dictionnary

        PlayerActionList[str(job_object.playerID)]["job_object"].Stat = player["stat"] #Copies dictionnary

        #We can access the information using the player's id

        #We will then check for Auras and do the appropriate effect

        for aura in player["Auras"]: #Going through all buffs in the player
            #We will look for a selection of buffs that are important. We will assume
            #the optimal scenario. So if we use a potion, we will assume its right before the fight begins
            
            job_object.auras += [aura] #Adding aura. Used for when restoring a fight using a saved file.
            
            if aura == "SharpCast":
                #SharpCast for BLM.
                job_object.SharpCast = True
            elif aura == "Soulsow":
                job_object.Soulsow = True
            elif aura == "Medicated":
                #Potion
                job_object.EffectCDList.append(PrepullPotion) #Adding this effect that will automatically apply the potion
                #on the first go through of the sim
            elif aura == "Meikyo Shisui":
                job_object.EffectCDList.append(MeikyoStackCheck)
                job_object.MeikyoCD = 46
                job_object.MeikyoStack -= 1
                job_object.EffectList.append(MeikyoEffect)
                job_object.EffectCDList.append(MeikyoCheck) #Could be a problem if do it before finishing 3 weaponskills
                job_object.Meikyo = 3
            elif aura == "Mudra":
                #Will also assume huton has been done
                ApplyHuton(job_object, None) #Giving Huton
                job_object.HutonTimer = 53 #Assuming some loss
                #If mudra is detected, we will assume we have casted it for Suiton
                job_object.CurrentRitual = [0,1,2]
            elif aura == "Eukrasia":
                job_object.Eukrasia = True
            elif aura == "Standard Step":
                #Assuming Dancer did 2 step
                job_object.Emboite = True
                job_object.Entrechat = True
                job_object.StandardFinish = True
            elif aura == "ClosedPosition":
                if dance_partner_flag:
                    job_object.DancePartner = dance_partner
                else:
                    closed_position = True
                    dancer = job_object
            elif aura == "Dance partner":
                if closed_position:
                    dancer.DancePartner = job_object
                else:
                    dance_partner_flag = True
                    dance_partner = job_object


    #Will now go through every player and give them an ActionList


    for playerID in PlayerActionList:

        for action in PlayerActionList[playerID]["actionList"]:

            if int(action["actionID"]) == 212 : 
                #WaitAbility. WaitAbility has a special field where the waited time is specified
                actionObject = WaitAbility(action["waitTime"])
            else: actionObject = lookup_abilityID(action["actionID"],action["targetID"], action["sourceID"],PlayerActionList) #Getting action object

            PlayerActionList[playerID]["actionObject"] += [actionObject]

        #We will now create the event

    Dummy = Enemy()
    Event = Fight([], Dummy, False)

    for playerID in PlayerActionList:
        PlayerActionList[playerID]["job_object"].ActionSet = PlayerActionList[playerID]["actionObject"] #Linking player object and action list
        Event.PlayerList.append(PlayerActionList[playerID]["job_object"]) #Adding job_object to Event
        PlayerActionList[playerID]["job_object"].CurrentFight = Event


    Event.ShowGraph = fightInfo["ShowGraph"] #Default
    Event.RequirementOn = fightInfo["RequirementOn"]
    Event.SimulateFight(0.01,fightInfo["fightDuration"], fightInfo["countdownValue"]) #Simulates the fight


    print(
        "========================================="
        )
    input("Press any key to return to the Main menu : ")


def MergeFightBackEnd(child_fight, parent_fight, parent_name):
    #This will merge the two fights.

    
    child = open(child_fight) #Opening save
    parent = open(parent_fight)
    data_child = json.load(child) #Loading json file
    data_parent = json.load(parent) #Loading json file

    #We will simply put Player list of data_child into player_list of parent

    data_parent["data"]["PlayerList"] += data_child["data"]["PlayerList"]

    save_dir = os.getcwd() + "\\saved"
    with open(save_dir + "\\" + parent_name, "w") as write_files:
        json.dump(data_parent,write_files, indent=4) #saving file