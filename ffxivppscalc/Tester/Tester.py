"""
This file will contain code for a tester we can use to test the simulator and make sure everything works accordingly

The test will check for those things and make sure they are of the correct values:

- End time
- Total potency done

This list will be expanded


"""
import json

from ffxivppscalc.UI_backend import RestoreFightObject


class Tester:
    """
    This class will contain code for the Tester object which will be created to test the simulator.
    """

    def __init__(self, filename):
        """
        filename : str -> name of the file containing the tester's information
        """
        self.filename = filename 


    def Test(self):
        """
        This function will test with all the given tests in the file and will report on the success and fails.
        """

        f = open(self.filename) #Opening save
        data = json.load(f)

        for test in data["data"]["FightList"]:
            # Will iterate through every fight in the saved file and test them.
            f_test = open(test["Fight"]) # Opening saved file for the test
            data_test = json.load(f_test) # loading data

            Event = RestoreFightObject(data_test) # Restoring into Event object

            fightInfo = data_test["data"]["fightInfo"] #fight information
            Event.ShowGraph = data_test["ShowGraph"] #Default
            Event.RequirementOn = fightInfo["RequirementOn"]
            Event.IgnoreMana = fightInfo["IgnoreMana"]
            
            Event.SimulateFight(0.01,fightInfo["fightDuration"], vocal=True) #Simulates the fight

            

