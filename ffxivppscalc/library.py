"""
This file will contain basic function we will let the user call when importing the library or
functions callable by the API.
"""

from copy import deepcopy
import json
import math
import os
from Jobs.PlayerEnum import JobEnum
from UI_backend import GenerateLayoutBackend, GenerateLayoutDict, RestoreFightObject

#Helper function

def roundDown(x, precision):
    return math.floor(x * 10**precision)/10**precision

# library

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

def SimulateFightAPI(FightDict : dict) -> dict:
    """
    This function can be called to simulate a fight. It requires as input the JSON file of the fight
    and it will return all the data relating to the simulation. This function will simply return the dictionnary and another function
    will return a JSON file. 
    FightDict : dict -> dictionnary holding the fight's info
    """

    Event = RestoreFightObject(FightDict) # Restoring the fight object

    fightInfo = FightDict["data"]["fightInfo"] #fight information
    Event.ShowGraph = fightInfo["ShowGraph"] #Default
    Event.RequirementOn = fightInfo["RequirementOn"]

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


cur_dir = os.getcwd()

#the saved directory should be in that same folder

saved_dir = cur_dir + "\\saved"

saved_fight = os.listdir(saved_dir)


f = open(saved_dir + "\\" + "blackmage.json") #Opening save

data = json.load(f) #Loading json file

print(SimulateFightAPI(data))


# POST

    





