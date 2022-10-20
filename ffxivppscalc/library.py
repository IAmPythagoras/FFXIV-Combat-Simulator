"""
This file will contain basic function we will let the user call when importing the library
"""

from Jobs.PlayerEnum import JobEnum
from ffxivppscalc.UI_backend import GenerateLayoutBackend, GenerateLayoutDict

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

def AddPlayer(FightDict : dict, newPlayer : JobEnum):
    """
    This function will add a new player to the given Fight dictionnary. The new player will have no actions and have base stats.
    FightDict : dict -> Dictionnary with information of the fight
    newPlayer : JobEnum -> Job of the new player
    """
    jobName = JobEnum.name_for_id(newPlayer)

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

    FightDict["Data"]["PlayerList"].append(newPlayerDict)


    





