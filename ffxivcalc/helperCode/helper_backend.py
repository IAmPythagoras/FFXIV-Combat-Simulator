import copy
import json
import logging
main_logging = logging.getLogger("ffxivcalc")
helper_logging = main_logging.getChild("Helper")
from pathlib import Path
import math

from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import ComboEffect
from ffxivcalc.Jobs.Melee.Ninja.Ninja_Spell import ApplyHuton
from ffxivcalc.Jobs.Melee.Samurai.Samurai_Spell import MeikyoCheck, MeikyoEffect, MeikyoStackCheck
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import EspritEffect
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import SongEffect
from ffxivcalc.Jobs.Tank.DarkKnight.DarkKnight_Spell import BloodWeaponCheck, BloodWeaponEffect
from ffxivcalc.Jobs.Tank.Warrior.Warrior_Spell import SurgingTempestEffect
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import DualCastEffect
from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import ElementalEffect, EnochianEffect

from ffxivcalc.Fight import Fight
from ffxivcalc.Enemy import Enemy
from ffxivcalc.Request.FFLogsAPIRequest import getAbilityList, lookup_abilityID
from ffxivcalc.Jobs.Base_Spell import PrepullPotion, WaitAbility
from ffxivcalc.Jobs.Player import Player
from ffxivcalc.Jobs.PlayerEnum import *

from ffxivcalc.Jobs.ActionEnum import name_for_id, id_for_name # importing helper functions
from ffxivcalc.Request.etro_request import get_gearset_data


letters = "abcdefghijklmnopqrstuvwyxz" # Used to make sure the input is only numbers

#This file will take care of request by TUI.py and return whatever needs to be returned

# ============================================================================================

# These are the stats that will be used when importing from FFLogs. Make sure to change them accordingly

# Caster
BLMStat = {"MainStat": 2945, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 840, "SkS" : 400,  "Crit" : 2386, "DH" : 1307} # Stats for BlackMage
RDMStat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "SkS" : 400, "Crit" : 2397, "DH" : 1544} # Stats for RedMage
SMNStat = {"MainStat": 2948, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 544, "SkS" : 400, "Crit" : 2436, "DH" : 1544} # Stats for Summoner

# Healer
SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "SkS" : 400, "Crit" : 2351, "DH" : 436} # Stats for Scholar
WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "SkS" : 400, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage
ASTStat = {"MainStat": 2949, "WD":126, "Det" : 1659, "Ten" : 400, "SS": 1473, "SkS" : 400, "Crit" : 2280, "DH" : 436} # Stats for Astrologian
SGEStat = {"MainStat": 2928, "WD":126, "Det" : 1859, "Ten" : 400, "SS": 827, "SkS" : 400, "Crit" : 2312, "DH" : 1012} # Stats for Sage

# Physical Ranged
MCHStat = {"MainStat": 2937, "WD":126, "Det" : 1598, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2389, "DH" : 1592} # Stats for Machinist
BRDStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 400, "SkS" : 536, "Crit" : 2387, "DH" : 1340} # Stats for Bard
DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 400, "SkS" : 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer

# Melee
NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
SAMStat = {"MainStat": 2937, "WD":126, "Det" : 1571, "Ten" : 400, "SS": 400, "SkS" : 508, "Crit" : 2446, "DH" : 1459} # Stats for Samurai
DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon
MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 400, "SkS" : 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
RPRStat = {"MainStat": 2946, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "SkS" : 400, "Crit" : 2462, "DH" : 1577} # Stats for Reaper

# Tank
DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "SkS" : 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
WARStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "SkS" : 400, "Crit" : 2377, "DH" : 1012} # Stats for Warrior
PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 400, "SkS" : 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

# ============================================================================================

def ImportFightBackend(fightID,fightNumber):

    Event = Fight(Enemy(), False) #Creating event
    helper_logging.debug("Constructing Event object from FFLogs link.")
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

    return Event


def AskInput(range):
    #This function will ask a numerical value to the user where range is the number of options
    #The inputs are assumed to be numerically ordered and starting at 1 and finishing at (range)
    user_input = input("Enter a number to select that option : ")

    while True:

        has_letter = False

        for letter in user_input:
            if letter.lower() in letters: has_letter = True

        if user_input == "" or has_letter: 
            has_letter = False
            user_input = input("This is not a valid input. Please enter a valid number : ")
        elif int(user_input) >= 1 and int(user_input) <= range: #if input is valid
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


        PlayerDict["JobName"] = JobEnum.name_for_id(Player.JobEnum)

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
                    actionDict["actionName"] = name_for_id(action.id,Player.ClassAction, Player.JobAction)
                    actionDict["waitTime"] = action.waitTime

                    actionList.append(copy.deepcopy(actionDict))#adding to dict
            else: #Normal ability
                actionDict["actionName"] = name_for_id(action.id,Player.ClassAction, Player.JobAction)
                actionDict["TargetID"] = action.TargetID 

                actionList.append(copy.deepcopy(actionDict))#adding to dict

        PlayerDict["actionList"] = copy.deepcopy(actionList)
        PlayerDict["etro_gearset_url"] = "Put a URL here if you want. The code will only overwirte the stats if it detects an etro url."

        PlayerListDict.append(copy.deepcopy(PlayerDict))

    EnemyList = []
    for EnemyID in Event.EnemyDict:
        EnemyList.append({"EnemyID" : EnemyID})

    

    data = {"data" : {
                "fightInfo" : {
                    "countdownValue" : countdown,
                    "fightDuration" : fightDuration,
                    "time_unit" : 0.01,
                    "ShowGraph" : Event.ShowGraph,
                    "RequirementOn" : Event.RequirementOn,
                    "IgnoreMana" : Event.IgnoreMana

                },
                "EnemyList" : EnemyList,
                "PlayerList" : PlayerListDict
    }}
    save_dir: Path = Path.cwd() / 'saved'
    with open(save_dir / f'{saveName}.json', "w") as write_files:
        json.dump(data,write_files, indent=4) #saving file

def RestoreFightObject(data : dict, name : str = ""):
    """
    This takes a FightDict dictionnary and converts it back into an Event object.
    data : dict -> dictionnary with the fight's data
    """

    helper_logging.debug("Restoring saved file " + name + " into Event object.")

    
    PlayerActionList = {} #Dictionnary containing all player with their action

    closed_position = False
    dance_partner_flag = False
    dance_partner = None
    dancer = None

    for player in data["data"]["PlayerList"]: #Going through all player in PlayerList and creating JobObject
        #Will check what job the player is so we can create a player object of the relevant job
        
        job_name = player["JobName"]
        job_object = None
        #Healer
        if job_name == "Sage" : job_object = Player([], [],{}, JobEnum.Sage)
        elif job_name == "Scholar" : job_object = Player([], [], {}, JobEnum.Scholar)
        elif job_name == "WhiteMage" : job_object = Player([], [], {}, JobEnum.WhiteMage)
        elif job_name == "Astrologian" : job_object = Player([], [], {}, JobEnum.Astrologian)
        #Tank
        elif job_name == "Warrior" : job_object = Player([], [SurgingTempestEffect],  {}, JobEnum.Warrior)
        elif job_name == "DarkKnight" : job_object = Player([], [],  {}, JobEnum.DarkKnight)
        elif job_name == "Paladin" : job_object = Player([], [], {}, JobEnum.Paladin)
        elif job_name == "Gunbreaker" : job_object = Player([], [],  {}, JobEnum.Gunbreaker)
        #Caster
        elif job_name == "BlackMage" : job_object = Player([], [EnochianEffect, ElementalEffect],  {}, JobEnum.BlackMage)
        elif job_name == "RedMage" : job_object = Player([], [DualCastEffect],  {}, JobEnum.RedMage)
        elif job_name == "Summoner" : job_object = Player([], [],  {}, JobEnum.Summoner)
        #Ranged
        elif job_name == "Dancer" : job_object = Player([], [EspritEffect],  {}, JobEnum.Dancer)
        elif job_name == "Machinist" : job_object = Player([], [],  {}, JobEnum.Machinist)
        elif job_name == "Bard" : job_object = Player([], [SongEffect],  {}, JobEnum.Bard)
        #melee
        elif job_name == "Reaper" : job_object = Player([], [],  {}, JobEnum.Reaper)
        elif job_name == "Monk" : job_object = Player([], [ComboEffect],  {}, JobEnum.Monk)
        elif job_name == "Dragoon" : job_object = Player([], [],  {}, JobEnum.Dragoon)
        elif job_name == "Ninja" : job_object = Player([], [],  {}, JobEnum.Ninja)
        elif job_name == "Samurai" : job_object = Player([], [],  {}, JobEnum.Samurai)
        

        job_object.playerID = player["playerID"] #Giving the playerID
        helper_logging.debug("Creating job object : " + job_name + " for playerID : " + str(player["playerID"]))

        PlayerActionList[str(job_object.playerID)] = {"job" : job_name, "job_object" : job_object, "actionList" : player["actionList"], "actionObject" : []} #Adding new Key accessible by IDs

        #Giving player object the stat dictionnary
        
        # Will check if the player is given an etro url.

        etro_url = player["etro_gearset_url"]
        if "etro.gg/gearset/" in etro_url:
            job_object.Stat = get_gearset_data(etro_url)

            # Since etro now returns only the weapon damage multiplier, we have to find the the original WD.
            job_object.f_WD = PlayerActionList[str(job_object.playerID)]["job_object"].Stat["WD"]/100 # Mult bonus we already know.
            
            baseMain = 390
            JobMod = job_object.JobMod # Level 90 jobmod value, specific to each job
            job_object.Stat["WD"] -= math.floor((baseMain * JobMod) /1000)
            

        else :
            PlayerActionList[str(job_object.playerID)]["job_object"].Stat = player["stat"]
        # If detects an etro url copies the stats. Otherwise takes the stats from the file
        #We can access the information using the player's id
        #We will then check for Auras and do the appropriate effect
        
        # Logging the stat of the player
        logging.debug("Player id " + str(job_object.playerID) + " has stats : " + str(job_object.Stat))

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

        player_obj = PlayerActionList[playerID]["job_object"] # Getting job object so we can have access to the ActionEnum of the class

        for action in PlayerActionList[playerID]["actionList"]:
            actionID = id_for_name(action["actionName"], player_obj.ClassAction, player_obj.JobAction) # Getting id from name

            if int(actionID) == 212 : 
                #WaitAbility. WaitAbility has a special field where the waited time is specified
                actionObject = WaitAbility(action["waitTime"])
            else: 
                actionObject = lookup_abilityID(actionID,action["TargetID"], playerID,PlayerActionList) #Getting action object

                actionObject = copy.deepcopy(actionObject)
                actionObject.TargetID = action["TargetID"] # Letting the action know who its target is

            PlayerActionList[playerID]["actionObject"] += [actionObject]

        #We will now create the event

    EnemyDict = {}

    for EnemyID in data["data"]["EnemyList"]:
        EnemyDict[EnemyID] = Enemy()

    Event = Fight(EnemyDict, False)

    for playerID in PlayerActionList:
        PlayerActionList[playerID]["job_object"].ActionSet = PlayerActionList[playerID]["actionObject"] #Linking player object and action list
        Event.AddPlayer([PlayerActionList[playerID]["job_object"]]) #Adding job_object to Event


    return Event

def SimulateFightBackend(file_name : str):
    """
    This function takes a file_name and opens the given file name assuming it is located in the saved folder.
    file_name : str -> name of the saved file.
    """

    f = open(file_name) #Opening save

    data = json.load(f) #Loading json file
    PlayerList = data["data"]["PlayerList"]

    if len(PlayerList) > 1 : #If there is more than 1 player we will ask if we wish to simulate all or only 1
        print(
            "This save file has more than one player character : " + "\n" + 
            "1- Simulate only one player character" + "\n" + 
            "2- Simulate all the player characters at the same time" + "\n" + 
            "====================================================="
            )

        user_input = AskInput(2)

        if user_input == "1" : #want to only simulate one player
            print(
                "=====================================================" + "\n" + 
                "List of players in this save file : "
            )
            n_player = len(PlayerList)
            for i in range(n_player):
                print(str(i + 1) + " -> " + PlayerList[i]["JobName"])
            
            print("Select which player character you wish to simulate.")

            user_input = AskInput(n_player)

            PlayerList = [PlayerList[int(user_input) - 1]] #Only taking what we are interested in

    #We will now go through all actionID and transform into an abilityList

    print("Restoring save file into Event object...")

    Event = RestoreFightObject(data, name=file_name)

    fightInfo = data["data"]["fightInfo"] #fight information
    Event.ShowGraph = fightInfo["ShowGraph"] #Default
    Event.RequirementOn = fightInfo["RequirementOn"]
    Event.IgnoreMana = fightInfo["IgnoreMana"]
    
    Event.SimulateFight(0.01,fightInfo["fightDuration"], vocal=True) #Simulates the fight


    print(
        "========================================="
        )
    input("Press any key to return to the Main menu : ")

def MergeFightBackEnd(child_fight, parent_fight, parent_name):
    """DEPRECIATED"""
    #This will merge the two fights.

    
    child = open(child_fight) #Opening save
    parent = open(parent_fight)
    data_child = json.load(child) #Loading json file
    data_parent = json.load(parent) #Loading json file

    #We will simply put Player list of data_child into player_list of parent

    data_parent["data"]["PlayerList"] += data_child["data"]["PlayerList"]

    save_dir: Path = Path.cwd() / "saved"
    with open(save_dir / parent_name, "w") as write_files:
        json.dump(data_parent,write_files, indent=4) #saving file

def GenerateLayoutBackend(player_list,namefile):
    # This function will generate a JSON file with nothng written inside which can be edited by the user
    # directly. It requires as input a player_list which is a list of PlayerEnum to know which player
    # the user wants in the fight

    data = GenerateLayoutDict(player_list)
    
    save_dir: Path = Path.cwd() / 'saved'
    with open(save_dir / f'{namefile}.json', "w") as write_files:
        json.dump(data,write_files, indent=4) # saving file
   
def GenerateLayoutDict(player_list):
    """
    This function generates a dictionnary that the simulator can use to simulate the fight
    """

    data = {
        "data":
        { 
            "fightInfo"  : {
                "fightDuration" : 500,
                "time_unit" : 0.01,
                "ShowGraph" : True,
                "RequirementOn" : True,
                "IgnoreMana" : False
            },
            "EnemyList" : [{"EnemyID" : 0}],
            "PlayerList" : []
            }
    }

    stat_dict = {
            "MainStat" : 390,
            "WD" : 0,
            "Det" : 390,
            "Ten" : 400,
            "SS" : 400,
            "SkS" : 400,
            "Crit" : 400,
            "DH" : 400
        }

    # Will not fill the PlayerList
    id = 100

    for player in player_list:
        # player is a JobEnum

        player_dict = {
            "JobName" : JobEnum.name_for_id(player),
            "playerID" : id,
            "stat" : stat_dict,
            "etro_gearset_url":  "Put a URL here if you want. The code will only overwirte the stats if it detects an etro url.",
            "Auras" : [],
            "actionList" : [
                {"actionName": "putNameHere", "TargetID" : "putTargetIDHere"}
            ]
        }

        data["data"]["PlayerList"].append(copy.deepcopy(player_dict))

        id+=1

    return data