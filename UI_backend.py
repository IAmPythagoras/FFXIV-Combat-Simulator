import copy
import json
import os


from Jobs.Ranged.Dancer.Dancer_Spell import EspritEffect
from Jobs.Ranged.Bard.Bard_Spell import SongEffect
from Jobs.Tank.DarkKnight.DarkKnight_Spell import BloodWeaponCheck, BloodWeaponEffect
from Jobs.Tank.Warrior.Warrior_Spell import SurgingTempestEffect
from Jobs.Caster.Redmage.Redmage_Spell import DualCastEffect
from Jobs.Caster.Blackmage.BlackMage_Spell import ElementalEffect, EnochianEffect

from Fight import Fight
from Enemy import Enemy
from FFLogsAPIRequest import getAbilityList, lookup_abilityID
from Jobs.Base_Spell import Melee_AA, Ranged_AA, WaitAbility

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

BLMCRITStat = {"MainStat": 2571, "WD":120, "Det" : 1752, "Ten" : 390, "SS": 758, "Crit" : 2287, "DH" : 965} 
BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1422, "Ten" : 400, "SS": 2171, "Crit" : 715, "DH" : 1454} 
SCHStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 944, "Crit" : 2277, "DH" : 616}
RDMStat = {"MainStat": 2563, "WD":120, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2348, "DH" : 1340}
MCHStat = {"MainStat": 2572, "WD":120, "Det" : 1615, "Ten" : 400, "SS": 400, "Crit" : 2121, "DH" : 1626}
NINStat = {"MainStat": 2555, "WD":120, "Det" : 1749, "Ten" : 400, "SS": 400, "Crit" : 2283, "DH" : 1330}
DRKStat = {"MainStat": 2521, "WD":120, "Det" : 1680, "Ten" : 539, "SS": 650, "Crit" : 2343, "DH" : 976}
WARStat = {"MainStat": 2521, "WD":120, "Det" : 2130, "Ten" : 1018, "SS": 400, "Crit" : 2240, "DH" : 400}
WHMStat = {"MainStat": 2571, "WD":120, "Det" : 1830, "Ten" : 400, "SS": 489, "Crit" : 2301, "DH" : 940}
SAMStat = {"MainStat": 2563, "WD":120, "Det" : 1654, "Ten" : 400, "SS": 579, "Crit" : 2310, "DH" : 1217}
PLDStat = {"MainStat": 2502, "WD":120, "Det" : 1680, "Ten" : 527, "SS": 650, "Crit" : 2319, "DH" : 1012}
GNBStat = {"MainStat": 2517, "WD":120, "Det" : 1612, "Ten" : 527, "SS": 950, "Crit" : 2205, "DH" : 868}
ASTStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 716, "Crit" : 2277, "DH" : 844}
SMNStat = {"MainStat": 2575, "WD":120, "Det" : 1688, "Ten" : 400, "SS": 489, "Crit" : 2296, "DH" : 1289}
BRDStat = {"MainStat": 2575, "WD":120, "Det" : 1381, "Ten" : 400, "SS": 479, "Crit" : 2229, "DH" : 1662}
DNCStat = {"MainStat": 2575, "WD":120, "Det" : 1453, "Ten" : 400, "SS": 549, "Crit" : 2283, "DH" : 1477}
DRGStat = {"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235}
RPRStat ={"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235}
SGEStat ={"MainStat": 2563, "WD":120, "Det" : 1953, "Ten" : 400, "SS": 656, "Crit" : 2244, "DH" : 904}

def ImportFightBackend(fightID,fightNumber):

    Event = Fight([], Enemy(), False) #Creating event

    action_dict, player_dict = getAbilityList(fightID, fightNumber) #getting 

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
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        elif job_name == "DarkKnight" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRKStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
            player_dict[playerID]["job_object"].EffectList = [BloodWeaponEffect] #Assuming we pre pull it
            player_dict[playerID]["job_object"].EffectCDList = [BloodWeaponCheck]
        elif job_name == "Paladin" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(PLDStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
            player_dict[playerID]["job_object"].EffectList = [OathGauge]
        elif job_name == "Gunbreaker" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(GNBStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
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
            player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
        elif job_name == "Machinist" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(MCHStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
        elif job_name == "Bard" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(BRDStat)
            player_dict[playerID]["job_object"].EffectList = [SongEffect]
            player_dict[playerID]["job_object"].ActionSet.insert(0, Ranged_AA)
        #melee
        elif job_name == "Reaper" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(RPRStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        elif job_name == "Monk" :  pass #Not yet Implemented
        elif job_name == "Dragoon" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(DRGStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        elif job_name == "Ninja" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(NINStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)
        elif job_name == "Samurai" : 
            player_dict[playerID]["job_object"].Stat = copy.deepcopy(SAMStat)
            player_dict[playerID]["job_object"].ActionSet.insert(0, Melee_AA)

        Event.PlayerList.append(player_dict[playerID]["job_object"])

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

        PlayerDict["playerID"] = Player.playerID
        PlayerDict["stat"] = Player.Stat
        actionList = []

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
                    "fightDuration" : fightDuration
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
        elif job_name == "Monk" : job_object = Machinist(2.5, [], [], [], None, {}) #Monk is not yet implemented
        elif job_name == "Dragoon" : job_object = Dragoon(2.5, [], [], [], None, {})
        elif job_name == "Ninja" : job_object = Ninja(2.5, [], [], [], None, {})
        elif job_name == "Samurai" : job_object = Samurai(2.5, [], [], [], None, {})
        
        if isinstance(job_object, (Tank, Melee, Dancer)): job_object.ActionSet.insert(0, Melee_AA) #If needs AA
        elif isinstance(job_object, Ranged) and (not isinstance(job_object, Dancer)) : job_object.ActionSet.insert(0, Ranged_AA) #If needs ranged AA

        job_object.playerID = player["playerID"] #Giving the playerID

        PlayerActionList[str(player["playerID"])] = {"job" : job_name, "job_object" : job_object, "actionList" : player["actionList"], "actionObject" : []} #Adding new Key accessible by IDs

        #Giving player object the stat dictionnary

        PlayerActionList[str(player["playerID"])]["job_object"].Stat = player["stat"] #Copies dictionnary

        #We can access the information using the player's id


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


    Event.ShowGraph = True #Default
    Event.SimulateFight(0.01,fightInfo["fightDuration"], fightInfo["countdownValue"]) #Simulates the fight


    print(
        "========================================="
        )
    input("Press any key to return to the Main menu : ")
