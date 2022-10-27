"""
This file will contain code for a tester we can use to test the simulator and make sure everything works accordingly

The test will check for those things and make sure they are of the correct values:

- End time
- Total potency done

This list will be expanded


"""
from copy import deepcopy
import json
from pathlib import Path
from UI_backend import RestoreFightObject


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def GenerateTestLayout(num_test : int):
    layout = {
        "data" :{
            "FightList" : [{
                "TestName" : "EnterName",
                "Fight" : "put name of save file",
                "ExpectedResult" : {
                    "EndTime" : "Endtime here",
                    "Put playerId here" : {"ExpectedTotalPotency" : "Put expected potency here"}
                }
            }] * num_test
        }
    }
    save_dir: Path = Path.cwd() / 'ffxivppscalc' /'Tester'
    saveName = "test_layout"
    with open(save_dir / f'{saveName}.json', "w") as write_files:
        json.dump(layout,write_files, indent=4) #saving file

class Tester:
    """
    This class will contain code for the Tester object which will be created to test the simulator.
    """

    def __init__(self, filename):
        """
        filename : str -> name of the file containing the tester's information
        """
        self.filename = Path.cwd() / 'ffxivppscalc' / 'Tester' / filename 
        self.fightResults = [] # Empty list that will be filled with all the fight results


    def Test(self):
        """
        This function will test with all the given tests in the file and will report on the success and fails.
        """

        self.fightResults = [] # Reseting the list
        f = open(self.filename) #Opening save
        data = json.load(f)

        for test in data["data"]["FightList"]:
            # Will iterate through every fight in the saved file and test them.
            file = Path.cwd() / 'ffxivppscalc' / 'Tester' / test["Fight"]
            f_test = open(file) # Opening saved file for the test
            data_test = json.load(f_test) # loading data

            Event = RestoreFightObject(data_test) # Restoring into Event object

            fightInfo = data_test["data"]["fightInfo"] #fight information
            Event.ShowGraph = fightInfo["ShowGraph"] #Default
            Event.RequirementOn = fightInfo["RequirementOn"]
            Event.IgnoreMana = fightInfo["IgnoreMana"]
            
            Event.SimulateFight(0.01,fightInfo["fightDuration"], vocal=False) #Simulates the fight

            result = {
                "TestName" : test["TestName"],
                "EndTime" : Event.TimeStamp,
                "ExpectedEndTime" : test["ExpectedResult"]["EndTime"],
                "EqualTime" : isclose(Event.TimeStamp,float(test["ExpectedResult"]["EndTime"])),
                "PlayerList" : []
            }

            for player in Event.PlayerList:
                player_result = {
                    "playerID" : player.playerID,
                    "TotalPotency" : player.TotalPotency,
                    "ExpectedTotalPotency" : test["ExpectedResult"][str(player.playerID)]["ExpectedTotalPotency"],
                    "EqualPotency" : int(player.TotalPotency) == int(test["ExpectedResult"][str(player.playerID)]["ExpectedTotalPotency"])
                }

                result["PlayerList"].append(deepcopy(player_result))
        
            self.fightResults.append(deepcopy(result))

        # Will now print out the results:

        for test in self.fightResults:
            passed = True
            print("Result for test : " + str(test["TestName"]))
            for player_result in test["PlayerList"]:
                
                if not player_result["EqualPotency"]: # Checking for equal potency
                    passed = False
                    print(
                        "Player with id " + str(player_result["playerID"]) + " did not pass potency test." + 
                        "\nTotal potency : " + str(player_result["TotalPotency"]) + " | Expected : " + str(player_result["ExpectedTotalPotency"])
                         )

            if not test["EqualTime"] : # Checking for equal end time
                passed = False
                print(
                        "This fight did not pass the end time test." + 
                        "\nEnd time : " + str(test["EndTime"]) + " | Expected : " + str(test["ExpectedEndTime"])
                         )
            
            if passed : print("Passed!")

            print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n") # Making space for next test




if __name__ == "__main__":
    x = Tester("test_layout.json")
    x.Test()
    #GenerateTestLayout(19)



            

