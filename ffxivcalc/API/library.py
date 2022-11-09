"""
This file will contain basic function we will let the user call when importing the library or
functions callable by the API.
"""

from copy import deepcopy
import json
import math
from ffxivcalc.Jobs.PlayerEnum import JobEnum
from ffxivcalc.helperCode.helper_backend import GenerateLayoutBackend, GenerateLayoutDict, RestoreFightObject
from ffxivcalc.Fight import ComputeDamage
from ffxivcalc.Enemy import Enemy
from ffxivcalc.Jobs.Base_Spell import Spell
from ffxivcalc.Jobs.PlayerEnum import RoleEnum
#Helper function

def roundDown(x, precision):
    return math.floor(x * 10**precision)/10**precision

# library

def AverageDamageAction(Player, Potency, MultBonus, type=0):

    levelMod = 1900
    baseMain = 390  
    baseSub = 400# Level 90 LevelMod values

    JobMod = Player.JobMod # Level 90 jobmod value, specific to each job

    Player.f_WD = (Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))/100
    Player.f_DET = math.floor(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000# Determination damage
    if Player.RoleEnum == RoleEnum.Tank : Player.f_TEN = (1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000 # Tenacity damage, 1 for non-tank player
    else : Player.f_TEN = 1 # if non-tank
    Player.f_SPD = (1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000 # Used only for dots
    Player.CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000 # Crit rate in decimal
    Player.CritMult = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000 # Crit Damage multiplier
    Player.DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000 # DH rate in decimal

    return ComputeDamage(Player, Potency, Enemy(), MultBonus, type, Spell(0, False, 0, 0, 0, 0, None, []))


def CreateFightDict(PlayerList : list[JobEnum]) -> dict:
    """
    This function creates a fight dictionnary that can then be executed by the simulator. The fight's parameters will be default but
    it will create the fight with the given player list.
    PlayerList : list[JobEnum] -> Player list
    """
    return GenerateLayoutDict(PlayerList)

def CreateFightJSON(PlayerList : list[JobEnum], filename : str) -> None:
    """
    This function creates a dictionnary that the simulator can use and saves the file in a saved folder where the file is executed under the given name
    PlayerList : list[JobEnum] -> Player list
    filename : str -> name of the saved file
    """
    GenerateLayoutBackend(PlayerList, filename)

def AddPlayer(FightDict : dict, newPlayer : JobEnum) -> None:
    """
    This function will add a new player to the given Fight dictionnary. The new player will have no actions and have base stats.
    FightDict : dict -> Dictionnary with information of the fight
    newPlayer : JobEnum -> Job of the new player
    """
    jobName = JobEnum.name_for_id(newPlayer)
    if len(FightDict["data"]["PlayerList"]) == 0:
        new_id = 1
    else:
        new_id = FightDict["data"]["PlayerList"][-1]["playerID"] + 1
    # finding id of last player and adding 1 assuming they are in id order.


    newPlayerDict = {
        "JobName" : jobName,
        "playerID" : new_id,
        "stat": {
            "MainStat" : 390,
            "WD" : 0,
            "Det" : 390,
            "Ten" : 400,
            "SS" : 400,
            "Crit" : 400,
            "DH" : 400
        },
        "etro_gearset_url" : "put etro url here if you have one. Not needed",
        "Auras" : [],
        "actionLists" : [
            {
                "actionName" : "put action name here"
            }
        ]

    }

    FightDict["data"]["PlayerList"].append(newPlayerDict)

# function called by API

# GET

def GetSimulateFight(JSONFile):
    """
    This function will take the JSON file given with the API request and use other helper functions to Simulate the fight.
    JSONFile : json -> JSON file with the simulation's parameter
    """

    data = json.load(JSONFile) # Loading the file in a dictionnary

    returnData = SimulateFightAPIHelper(data)

    return json.dump(returnData,None, indent=4) # Returning the JSON file

def SimulateFightAPIHelper(FightDict : dict) -> dict:
    """
    This function can be called to simulate a fight. It requires as input the JSON file of the fight
    and it will return all the data relating to the simulation. This function will simply return the dictionnary and another function
    will return a JSON file. 
    FightDict : dict -> dictionnary holding the fight's info
    """
    with open('hey.json', "w") as write_files:
        json.dump(FightDict,write_files, indent=4) #saving file

    Event = RestoreFightObject(FightDict) # Restoring the fight object
    fightInfo = FightDict["data"]["fightInfo"] #fight information
    Event.ShowGraph = fightInfo["ShowGraph"] #Default
    Event.RequirementOn = fightInfo["RequirementOn"]
    Event.IgnoreMana = fightInfo["IgnoreMana"]

    Event.SimulateFight(0.01,fightInfo["fightDuration"], vocal=False) # Simulating the fight

    # Now every player object has the info we need. We will simply parse is and put into a dictionnary. 
    # To return as a JSON file.

    # Skeleton of the returnData
    returnData = {
        "data" : {
            "fightInfo" : {
                "fightDuration" : Event.TimeStamp,
                "maxfightDuration" : fightInfo["fightDuration"],
                "fightname" : "ayo",
                "TeamCompositionBonus" : Event.TeamCompositionBonus,
                "failedRequirementEventList" : [],
                "Success" : True,
            },
            "PlayerList" : []
        }
    }

    # Will go through every failedRequirementEvent and record them
    success = True
    for event in Event.failedRequirementList:
        
        success = success and not event.fatal # if one event was fatal success is false

        eventDict = {
            "timeStamp" : event.timeStamp,
            "playerID" : event.playerID,
            "requirementName" : event.requirementName,
            "additionalInfo" : event.additionalInfo,
            "fatal" : event.fatal
        }

        returnData["data"]["fightInfo"]["failedRequirementEventList"].append(deepcopy(eventDict))

    returnData["data"]["fightInfo"]["Success"] = success


    for player in Event.PlayerList:
        # Going through every player will create the appriopriate dictionnary to return the info and put it in
        # returnData["data"]["PlayerList"].

        playerDict = {
            "JobName" : JobEnum.name_for_id(player.JobEnum),
            "ExpectedDPS" : 0 if Event.TimeStamp == 0 else roundDown(player.TotalDamage/Event.TimeStamp,2),
            "PotencyPerSecond" :  0 if Event.TimeStamp == 0 else roundDown(player.TotalPotency/Event.TimeStamp,2),
            "TotalDamage" : player.TotalDamage,
            "TotalPotency" : player.TotalPotency,
            "numberOfGCD" : player.GCDCounter,
            "ProcInfo" : {},
            "GraphInfoDPS" : [],
            "GraphInfoPPS" : []
        } # Creating new dictionnary

        # Going through its registered DPS and PPS points

        for (x,y) in zip(player.DPSGraph, Event.timeValue):
            # DPS

            point = {
                "value" : y,
                "name" : x
            }

            playerDict["GraphInfoDPS"].append(deepcopy(point))
        
        for (x,y) in zip(player.PotencyGraph, Event.timeValue):
            # PPS

            point = {
                "value" : y,
                "name" : x
            }

            playerDict["GraphInfoPPS"].append(deepcopy(point))

        # If any job has luck will return the info regarding this luck for the rotation

        match player.JobEnum:
            case JobEnum.Bard:
                procInfo = {
                    "RefulgentArrow" : {
                        "Expected" : player.ExpectedRefulgent,
                        "Used" : player.UsedRefulgent
                    },
                    "WandererRepertoire" : {
                        "Expected" : player.ExpectedTotalWandererRepertoire,
                        "Used" : player.UsedTotalWandererRepertoire
                    },
                    "SoulVoiceGauge" : {
                        "Expected" : player.ExpectedSoulVoiceGauge,
                        "Used" : player.UsedSoulVoiceGauge
                    },
                    "BloodLetterReduction" : {
                        "Expected" : player.ExpectedBloodLetterReduction,
                        "Used" : player.UsedBloodLetterReduction
                    }
                }
                playerDict["ProcInfo"] = deepcopy(procInfo)
            case JobEnum.Dancer:
                procInfo = {
                    "SilkenSymettry" : {
                        "Expected" : player.ExpectedSilkenSymettry,
                        "Used" : player.UsedSilkenSymettry
                    },
                    "SilkenFlow" : {
                        "Expected" : player.ExpectedSilkenFlow,
                        "Used" : player.UsedSilkenFlow
                    },
                    "FourfoldFeather" : {
                        "Expected" : player.ExpectedFourfoldFeather,
                        "Used" : player.UsedFourfoldFeather
                    },
                    "ThreefoldFan" : {
                        "Expected" : player.ExpectedThreefoldFan,
                        "Used" : player.UsedThreefoldFan
                    }
                }
                playerDict["ProcInfo"] = deepcopy(procInfo)
            case JobEnum.RedMage:
                procInfo = {
                    "Verstone" : {
                        "Expected" : player.ExpectedVerstoneProc,
                        "Used" : player.UsedVerstoneProc
                    },
                    "Verfire" : {
                        "Expected" : player.ExpectedVerfireProc,
                        "Used" : player.UsedVerfireProc
                    }
                }
                playerDict["ProcInfo"] = deepcopy(procInfo)



        returnData["data"]["PlayerList"].append(deepcopy(playerDict))


    return returnData

"""
cur_dir = os.getcwd()

#the saved directory should be in that same folder

saved_dir = cur_dir + "\\saved"

saved_fight = os.listdir(saved_dir)


f = open(saved_dir + "\\" + "blackmage.json") #Opening save

data = json.load(f) #Loading json file

APIAnswer = SimulateFightAPIHelper(data)

with open(f'{"APIRequestTest"}.json', "w") as write_files:
    json.dump(APIAnswer,write_files, indent=4) #saving file

"""
# POST

    





