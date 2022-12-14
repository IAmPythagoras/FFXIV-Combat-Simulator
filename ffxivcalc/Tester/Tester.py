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
from ffxivcalc.helperCode.helper_backend import RestoreFightObject


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
    save_dir: Path = Path.cwd() / 'ffxivcalc' /'Tester'
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
        self.filename = Path.cwd() / filename 
        self.fightResults = [] # Empty list that will be filled with all the fight results


    def Test(self):
        """
        This function will test with all the given tests in the file and will report on the success and fails.
        """

        self.fightResults = [] # Reseting the list
        f = open(self.filename / "test_layout.json" ) #Opening save
        #input(self.filename)
        data = json.load(f)

        for test in data["data"]["FightList"]:
            # Will iterate through every fight in the saved file and test them.
            file = self.filename / test["Fight"]
            f_test = open(file) # Opening saved file for the test
            data_test = json.load(f_test) # loading data

            
            # Restoring into Event object
            Event_Req = RestoreFightObject(data_test, name=test["Fight"]) # Requirement on
            Event = RestoreFightObject(data_test, name=test["Fight"]) # No requirements
            
            Event.ShowGraph = False
            Event.RequirementOn = False
            Event.IgnoreMana = True
            
            Event.SimulateFight(0.01,500, vocal=False) # Simulate the fight with no requirements

            Event_Req.ShowGraph = False
            Event_Req.RequirementOn = True
            Event_Req.IgnoreMana = True

            Event_Req.SimulateFight(0.01,500, vocal=False) # Simulates the fight with requirements

            failedReq = 0
            for event in Event_Req.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
                if event.fatal : failedReq += 1

            result = {
                "TestName" : test["TestName"],
                "EndTime" : Event.TimeStamp,
                "ExpectedEndTime" : test["ExpectedResult"]["EndTime"],
                "EqualTime" : isclose(Event.TimeStamp,float(test["ExpectedResult"]["EndTime"])),
                "FailedRequirement" : failedReq == 0,
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
        total_passed = 0
        for test in self.fightResults:
            passed = True
            print("Result(s) for test : " + str(test["TestName"]))
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

            if not test["FailedRequirement"]:
                passed = False
                print("This fight did not pass requirement.")

            
            if passed : 
                total_passed += 1
                print("Passed!")

            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++") # Making space for next test

        print("Passed " + str(total_passed) + "/" + str(len(self.fightResults)) + " test(s)." )


if __name__ == "__main__":
    Tester("test_layout.json").Test()

    



            

