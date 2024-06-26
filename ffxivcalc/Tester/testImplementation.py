"""
This file will contain the test code of every test.

It also contains the code for the testSuite class

A testSuite is a compilation of different tests that are testing a similar thing.

EX : A Blackmage testSuite, etc.

"""
from ffxivcalc.helperCode.Progress import ProgressBar

from math import floor
from ffxivcalc.Fight import Fight
from ffxivcalc.Jobs.Player import Player
from ffxivcalc.Jobs.PlayerEnum import *
from ffxivcalc.Enemy import Enemy


from ffxivcalc.Jobs.Base_Spell import WaitAbility, Potion, conditionalAction
from ffxivcalc.Jobs.Caster.Caster_Spell import *
from ffxivcalc.Jobs.Melee.Melee_Spell import *
from ffxivcalc.Jobs.Ranged.Ranged_Spell import *
from ffxivcalc.Jobs.Healer.Healer_Spell import *
from ffxivcalc.Jobs.Tank.Tank_Spell import *

#CASTER
from ffxivcalc.Jobs.Caster.Summoner.Summoner_Spell import *
from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import * 
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import *

#HEALER
from ffxivcalc.Jobs.Healer.Sage.Sage_Spell import *
from ffxivcalc.Jobs.Healer.Scholar.Scholar_Spell import *
from ffxivcalc.Jobs.Healer.Whitemage.Whitemage_Spell import *
from ffxivcalc.Jobs.Healer.Astrologian.Astrologian_Spell import *

#RANGED
from ffxivcalc.Jobs.Ranged.Machinist.Machinist_Spell import *
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import *
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import *

#TANK
from ffxivcalc.Jobs.Tank.Gunbreaker.Gunbreaker_Spell import *
from ffxivcalc.Jobs.Tank.DarkKnight.DarkKnight_Spell import *
from ffxivcalc.Jobs.Tank.Warrior.Warrior_Spell import *
from ffxivcalc.Jobs.Tank.Paladin.Paladin_Spell import *

#MELEE
from ffxivcalc.Jobs.Melee.Samurai.Samurai_Spell import *
from ffxivcalc.Jobs.Melee.Ninja.Ninja_Spell import *
from ffxivcalc.Jobs.Melee.Dragoon.Dragoon_Spell import *
from ffxivcalc.Jobs.Melee.Reaper.Reaper_Spell import *
from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import *

import logging
from ffxivcalc.Request.FFLogs_api import FFLogClientV2
from ffxivcalc.Jobs import ActionEnum
from ffxivcalc.Request.FFLogs_api import FFLogClientV2, get_fflog_events_dataframe
from ffxivcalc.Request.ffxivcalcViewTranslator import ffxiv_sim_view
from ffxivcalc.helperCode.helper_backend import RestoreFightObject
from random import randint, seed, sample

main_logging = logging.getLogger("ffxivcalc")
test_logging = main_logging.getChild("Testing")

base_stat = {
        "MainStat" : 450,
        "WD" : 0,
        "Det" : 390,
        "Ten" : 400,
        "SS" : 400,
        "SkS" : 400,
        "Crit" : 400,
        "DH" : 400,
        "Piety" : 390
    }       
        
class hitBuff:
    def __init__(self, buff : float, isCrit : bool = True):
        self.buff = buff
        self.isCrit = isCrit


class test:
    """
    This class represents a single test case of a test suite.
    testName (str) : name of this test
    testFunction (function -> T) : code that will execute the test. This contains the test's logic. It can return any type as long as all the return statements are within a list.
    validationFunction (function -> Bool) : this function will receive as input the result of testFunction, it contains the code that will
                                            compare the test's results to expected results. This function must accept what testFunction returns
                                            and must return a boolean value with a list of expected values.
    """

    def __init__(self, testName : str, testFunction , validationFunction ) -> None:
        self.testName = testName
        self.testFunction = testFunction
        self.validationFunction = validationFunction

    def executeTest(self) -> bool:
        """This function executes the test. The results of the test are written in the log file.
            It also returns a boolean relating to weither the test was successful
        """
        test_logging.debug("Executing test -> " + self.testName)
        try:
            testResults = self.testFunction()
        except Exception as Error:
            test_logging.error("A '" + Error.__class__.__name__ + "' was catched when executing " + self.testName + ". \nError message : " + repr(Error)+"")   
            return False
        validation, expected = self.validationFunction(testResults)

        if not validation: test_logging.error(self.testName + " failed. testResults : " + str(testResults) + " expected results : " + str(expected))    
        return validation
    
class testSuite:
    """This class represents a suite of tests.
    testSuiteName (str) : Name of the test suite
    """

    def __init__(self,testSuiteName : str) -> None:
        self.testSuiteName = testSuiteName
        self.testList = []

    def addTest(self, newTest : test) -> None:
        """This function adds a test to this test suite.

        Args:
            newTest (test): new test to be added.
        """
        self.testList.append(newTest)

    def executeTestSuite(self) -> (bool, int):
        """This function executes all test in order of insertion into the testList.
        It returns a tuple which corresponds to (passed?, how many test failed).
        """
        test_logging.debug("Executing test suite -> " + self.testSuiteName)
        success = True
        numFailed = 0
        x = len(self.testList)
        for test in self.testList: 
            curTest = test.executeTest()
            if not curTest : numFailed += 1
            success = success and curTest

        if not success : test_logging.error("Testsuite " + self.testSuiteName + " had at least one fail test. See above.")
        else : test_logging.debug(self.testSuiteName + " completed without errors.")
        return success, numFailed


######################################
#       Blackmage testSuite          #
######################################

def generateBLMTestSuite() -> testSuite:

    blmTestSuite = testSuite("Blackmage test suite")

    # Opener requirement, end time and potency test 1

    def blmTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, Triplecast, Manafront,
                    Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def blmTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 86.07, 9349]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    blmtest1 = test("Opener requirement, end time and potency 1", blmTest1TestFunction, blmTest1ValidationFunction)
    blmTestSuite.addTest(blmtest1)

    # Opener requirement, end time and potency test 2
                
    def blmTest2TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HighFire, HighFire, HighFire, Flare, HighBlizzard, Freeze, Thunder4, HighFire, Amplifier, HighFire, HighFire, Flare, Flare, 
                    HighBlizzard, Freeze, Foul, Swiftcast, Transpose, HighFire, Triplecast, Flare, Flare, Manafront, Flare]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def blmTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 48.45, 5348]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    blmtest2 = test("Opener requirement, end time and potency 2", blmTest2TestFunction, blmTest2ValidationFunction)
    blmTestSuite.addTest(blmtest2)

    # Mana test 1

    def blmTest3TestFunction() -> None:
        """This test checks the mana regen during ui 1 and confirms ui 1
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Despair, Transpose, WaitAbility(3)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana,player.ElementalGauge]

    def blmTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3200, -1]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1]

        return passed, expected

    blmtest3 = test("Testing mana tic and umbral ice phase 1",blmTest3TestFunction,blmTest3ValidationFunction)
    blmTestSuite.addTest(blmtest3)

    # Mana test 2

    def blmTest4TestFunction() -> None:
        """This test checks the mana regen during ui 2 and confirms ui 2
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Despair, Transpose, Paradox,WaitAbility(3)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana,player.ElementalGauge]

    def blmTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [4700,-2]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1]

        return passed, expected

    blmtest4 = test("Testing mana tic and umbral ice phase 2",blmTest4TestFunction,blmTest4ValidationFunction)
    blmTestSuite.addTest(blmtest4)

    # Mana test 3

    def blmTest5TestFunction() -> None:
        """This tests mana regen under ui 3 and confirms ui 3
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Despair, Blizzard3,WaitAbility(3.1)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana,player.ElementalGauge]

    def blmTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [6200,-3]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1]

        return passed, expected

    blmtest5 = test("Testing mana tic and umbral ice phase 3",blmTest5TestFunction,blmTest5ValidationFunction)
    blmTestSuite.addTest(blmtest5)

    # Mana test 4

    def blmTest6TestFunction() -> None:
        """This will test the mana regeneration in astral fire
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Despair, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana,player.ElementalGauge]

    def blmTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,3]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1]

        return passed, expected

    blmtest6 = test("Testing mana tic in astral fire phase",blmTest6TestFunction,blmTest6ValidationFunction)
    blmTestSuite.addTest(blmtest6)


    # Transpose test

    def blmTest7TestFunction() -> None:
        """This tests that tranpose goes to UI 1 if astral fire
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Transpose]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [-1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest7 = test("Tranpose in AF goes to UI 1",blmTest7TestFunction,blmTest7ValidationFunction)
    blmTestSuite.addTest(blmtest7)

    # Transpose test UI to AF 1

    def blmTest8TestFunction() -> None:
        """This tests that tranpose goes to AF 1 if in UI
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Transpose]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest8 = test("Tranpose in UI goes to AF 1",blmTest8TestFunction,blmTest8ValidationFunction)
    blmTestSuite.addTest(blmtest8)

    # Double transpose test from UI

    def blmTest8TestFunction() -> None:
        """This tests that tranpose goes to UI 1 if double tranpose from UI 
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Transpose, WaitAbility(5), Transpose]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [-1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest8 = test("Double transpose start in UI",blmTest8TestFunction,blmTest8ValidationFunction)
    blmTestSuite.addTest(blmtest8)

    # Double transpose test from AF

    def blmTest9TestFunction() -> None:
        """This tests that tranpose goes to AF 1 if double transpose from AF
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Transpose, WaitAbility(5), Transpose]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest9 = test("Double transpose start in AF",blmTest9TestFunction,blmTest9ValidationFunction)
    blmTestSuite.addTest(blmtest9)

    # Transpose from nothing

    def blmTest10TestFunction() -> None:
        """This tests that tranpose does nothing if not in AF or UI
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Scathe, Transpose]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest10 = test("Transpose not in UI or AF",blmTest10TestFunction,blmTest10ValidationFunction)
    blmTestSuite.addTest(blmtest10)

    # Loosing UI after 15 seconds

    def blmTest11TestFunction() -> None:
        """This tests that UI is lost after 15 seconds of doing nothing
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest11 = test("Loosing UI after 15 seconds",blmTest11TestFunction,blmTest11ValidationFunction)
    blmTestSuite.addTest(blmtest11)

    # Loosing UI after 15 seconds

    def blmTest15TestFunction() -> None:
        """This tests that AF is lost after 15 seconds of doing nothing
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3,WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.ElementalGauge]

    def blmTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest15 = test("Loosing AF after 15 seconds",blmTest15TestFunction,blmTest15ValidationFunction)
    blmTestSuite.addTest(blmtest15)

    # Checking enochian timer resets

    def blmTest12TestFunction() -> None:
        """This tests that enochian is reset
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,WaitAbility(12.00), Blizzard1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EnochianTimer]

    def blmTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [15]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest12 = test("Enochian timer reset",blmTest12TestFunction,blmTest12ValidationFunction)
    blmTestSuite.addTest(blmtest12)

    # Gaining PolyglotStack after 30 seconds under enochian and testing umbral soul

    def blmTest13TestFunction() -> None:
        """This tests that polyglot stacks are gained after 30 seconds of enochian and testing umbral soul
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,WaitAbility(10), UmbralSoul, WaitAbility(10), UmbralSoul,UmbralSoul, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.PolyglotStack, player.ElementalGauge, player.UmbralHearts]

    def blmTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1, -3, 3]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1] and expected[2] == testResults[2]

        return passed, expected

    blmtest13 = test("Gaining PolyglotStack after 30 seconds in enochian and testing umbral soul",blmTest13TestFunction,blmTest13ValidationFunction)
    blmTestSuite.addTest(blmtest13)

    # Testing mana usage 1

    def blmTest14TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,Blizzard4, Fire3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana]

    def blmTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [10000]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest14 = test("Mana usage test 1",blmTest14TestFunction,blmTest14ValidationFunction)
    blmTestSuite.addTest(blmtest14)

    # Testing mana usage 2

    def blmTest16TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,Blizzard4, Fire3, Fire4, Fire4, Fire4]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana]

    def blmTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [7600]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest16 = test("Mana usage test 2",blmTest16TestFunction,blmTest16ValidationFunction)
    blmTestSuite.addTest(blmtest16)

    # Testing mana usage 3

    def blmTest17TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,Blizzard4, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana]

    def blmTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2800]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest17 = test("Mana usage test 3",blmTest17TestFunction,blmTest17ValidationFunction)
    blmTestSuite.addTest(blmtest17)

    # Testing mana usage 4

    def blmTest18TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3,Blizzard4, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana, player.EnochianTimer]

    def blmTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,15]

        passed = expected[0] == testResults[0] and expected[1] == testResults[1]

        return passed, expected

    blmtest18 = test("Mana usage test 4",blmTest18TestFunction,blmTest18ValidationFunction)
    blmTestSuite.addTest(blmtest18)

    # Testing mana usage 5

    def blmTest19TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [HighBlizzard, Freeze, HighFire, HighFire, HighFire]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana]

    def blmTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [7000]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest19 = test("Mana usage test 5",blmTest19TestFunction,blmTest19ValidationFunction)
    blmTestSuite.addTest(blmtest19)

    # Testing mana usage 6

    def blmTest20TestFunction() -> None:
        """This tests the final mana at the end of a rotation
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [HighBlizzard, Freeze, HighFire, HighFire, HighFire, Flare, Flare]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana]

    def blmTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest20 = test("Mana usage test 6",blmTest20TestFunction,blmTest20ValidationFunction)
    blmTestSuite.addTest(blmtest20)

    # Triplecast/swiftcast test and interaction with insta cast spell 1

    def blmTest21TestFunction() -> None:
        """Triplecast/swiftcast test and interaction with insta cast spell 1
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Fire3, Triplecast, Fire4, Fire4, Swiftcast, Fire4]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TripleCastStack]

    def blmTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest21 = test("Triplecast/swiftcast test and interaction with insta cast spell 1",blmTest21TestFunction,blmTest21ValidationFunction)
    blmTestSuite.addTest(blmtest21)

    # Triplecast/swiftcast test and interaction with insta cast spell 2

    def blmTest22TestFunction() -> None:
        """Triplecast/swiftcast test and interaction with insta cast spell 2
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Fire3, Triplecast, Fire4, Fire4, Triplecast, Fire4]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TripleCastStack]

    def blmTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest22 = test("Triplecast/swiftcast test and interaction with insta cast spell 2",blmTest22TestFunction,blmTest22ValidationFunction)
    blmTestSuite.addTest(blmtest22)

    # Triplecast/swiftcast test and interaction with insta cast spell 3

    def blmTest23TestFunction() -> None:
        """Triplecast/swiftcast test and interaction with insta cast spell 3
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Fire3, SharpCast, Amplifier, Fire1, Triplecast, Fire4, Xenoglossy, Fire4, Fire3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TripleCastStack]

    def blmTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest23 = test("Triplecast/swiftcast test and interaction with insta cast spell 3",blmTest23TestFunction,blmTest23ValidationFunction)
    blmTestSuite.addTest(blmtest23)

    # Triplecast/swiftcast test and interaction with insta cast spell 4

    def blmTest24TestFunction() -> None:
        """Triplecast/swiftcast test and interaction with insta cast spell 4
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Blizzard3, Fire3, SharpCast, Amplifier, Thunder3, Triplecast, Fire4, Xenoglossy, Fire4, Thunder3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TripleCastStack]

    def blmTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest24 = test("Triplecast/swiftcast test and interaction with insta cast spell 4",blmTest24TestFunction,blmTest24ValidationFunction)
    blmTestSuite.addTest(blmtest24)

    # Triplecast/swiftcast test and interaction with insta cast spell 4

    def blmTest25TestFunction() -> None:
        """Triplecast/swiftcast test and interaction with insta cast spell 4
        """
        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = base_stat
        actionSet = [Fire3, Blizzard3, Swiftcast, Paradox]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = False

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [SwiftcastEffect in player.EffectList]

    def blmTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        passed = expected[0] == testResults[0]

        return passed, expected

    blmtest25 = test("Triplecast/swiftcast test and interaction with insta cast spell 5",blmTest25TestFunction,blmTest25ValidationFunction)
    blmTestSuite.addTest(blmtest25)

    return blmTestSuite

######################################
#         Redmage testSuite          #
######################################

def generateRDMTestSuite() -> testSuite:

    rdmTestSuite = testSuite("Redmage test suite")

    # Opener requirement, end time and potency test 1

    def rdmTest1TestFunction() -> None:
        """This test will try the opener of a redmage. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Swiftcast, Acceleration, Verthunder, Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
                    Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verfire, Verthunder, Verstone, Verareo, Jolt, 
                    Verthunder, Fleche]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def rdmTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 32.49, 8730]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest1 = test("Opener requirement, end time and potency 1", rdmTest1TestFunction, rdmTest1ValidationFunction)
    rdmTestSuite.addTest(rdmtest1)

    # Dual cast test 1

    def rdmTest2TestFunction() -> None:
        """This test will make sure dual cast works as intented
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt, Verthunder, Jolt, Swiftcast, Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast]

    def rdmTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest2 = test("Dual cast test 1", rdmTest2TestFunction, rdmTest2ValidationFunction)
    rdmTestSuite.addTest(rdmtest2)

    # Dual cast test 2

    def rdmTest3TestFunction() -> None:
        """This test will make sure dual cast works as intented. WIth swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt, Verthunder, Jolt, Swiftcast, Verthunder, Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast, SwiftcastEffect in player.EffectList]

    def rdmTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest3 = test("Dual cast test 2", rdmTest3TestFunction, rdmTest3ValidationFunction)
    rdmTestSuite.addTest(rdmtest3)

    # Dual cast test 3

    def rdmTest4TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Swiftcast, Acceleration, Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast, SwiftcastEffect in player.EffectList, AccelerationEffect in player.EffectList]

    def rdmTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest4 = test("Dual cast test 3", rdmTest4TestFunction, rdmTest4ValidationFunction)
    rdmTestSuite.addTest(rdmtest4)

    # Dual cast test 4

    def rdmTest5TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Swiftcast, Acceleration, Verthunder, Verareo]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast, SwiftcastEffect in player.EffectList, AccelerationEffect in player.EffectList]

    def rdmTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest5 = test("Dual cast test 4", rdmTest5TestFunction, rdmTest5ValidationFunction)
    rdmTestSuite.addTest(rdmtest5)

    # Dual cast test 5

    def rdmTest6TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt,Swiftcast, Acceleration, Verthunder, Verareo]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast, SwiftcastEffect in player.EffectList, AccelerationEffect in player.EffectList]

    def rdmTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest6 = test("Dual cast test 5", rdmTest6TestFunction, rdmTest6ValidationFunction)
    rdmTestSuite.addTest(rdmtest6)

    # Dual cast test 6

    def rdmTest7TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt,Swiftcast, Acceleration, Verthunder, Verareo, Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DualCast, SwiftcastEffect in player.EffectList, AccelerationEffect in player.EffectList]

    def rdmTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest7 = test("Dual cast test 6", rdmTest7TestFunction, rdmTest7ValidationFunction)
    rdmTestSuite.addTest(rdmtest7)

    # Black/White mana generation/usage test 1

    def rdmTest8TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt, Verthunder, Verfire, Verareo]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [8, 13]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest8 = test("Black/White mana generation/usage test 1", rdmTest8TestFunction, rdmTest8ValidationFunction)
    rdmTestSuite.addTest(rdmtest8)

    # Black/White mana generation/usage test 2

    def rdmTest9TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jolt, Jolt, Jolt, Jolt, Jolt]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [10,10]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest9 = test("Black/White mana generation/usage test 2", rdmTest9TestFunction, rdmTest9ValidationFunction)
    rdmTestSuite.addTest(rdmtest9)

    # Black/White mana generation/usage test 3

    def rdmTest10TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Verfire, Verthunder, Verstone, Verareo, Manafication]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [67,67]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest10 = test("Black/White mana generation/usage test 3", rdmTest10TestFunction, rdmTest10ValidationFunction)
    rdmTestSuite.addTest(rdmtest10)

    # Black/White mana generation/usage test 4

    def rdmTest11TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Verfire, Verthunder, Verstone, Verareo, Manafication, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Verflare, Scorch, Resolution, EnchantedReprise]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [20, 31]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest11 = test("Black/White mana generation/usage test 4", rdmTest11TestFunction, rdmTest11ValidationFunction)
    rdmTestSuite.addTest(rdmtest11)

    # Black/White mana generation/usage test 5

    def rdmTest12TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Verfire, Verthunder, Verstone, Verareo, Manafication, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Verholy, Scorch, Resolution, EnchantedReprise]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [31, 20]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest12 = test("Black/White mana generation/usage test 5", rdmTest12TestFunction, rdmTest12ValidationFunction)
    rdmTestSuite.addTest(rdmtest12)

    # Black/White mana generation/usage test 6

    def rdmTest13TestFunction() -> None:
        """This test will make sure dual cast works as intented. With acceleration and swiftcast
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 502, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Manafication, Manafication, Verthunder, Verareo]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WhiteMana, player.BlackMana]

    def rdmTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [100,100]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rdmtest13 = test("Black/White mana generation/usage test 6", rdmTest13TestFunction, rdmTest13ValidationFunction)
    rdmTestSuite.addTest(rdmtest13)

    return rdmTestSuite


######################################
#         Summoner testSuite         #
######################################

def generateSMNTestSuite() -> testSuite:

    smnTestSuite = testSuite("Summoner test suite")

    # Opener requirement, end time and potency test 1

    def smnTest1TestFunction() -> None:
        """This test will try the opener of a redmage. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, 
                    AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def smnTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 80.21, 9530]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest1 = test("Opener requirement, end time and potency 1", smnTest1TestFunction, smnTest1ValidationFunction)
    smnTestSuite.addTest(smntest1)

    # Opener requirement, end time and potency test 2

    def smnTest2TestFunction() -> None:
        """This test will try the opener of a redmage. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, 
                    AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, 
                    Ifrit, Ruby, Ruby, Cyclone, Strike, Ruin4, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def smnTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 105.91, 14510]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest2 = test("Opener requirement, end time and potency 2", smnTest2TestFunction, smnTest2ValidationFunction)
    smnTestSuite.addTest(smntest2)

    # Summon test 1

    def smnTest3TestFunction() -> None:
        """This test checks the total potency done by Bahamut when summoned and makes sure he dissapears after the given time duration.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, Enkindle, Deathflare, WaitAbility(15), Ruin3]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        pet = player.Pet
        return [player.TotalPotency, pet.TrueLock]

    def smnTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3320, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest3 = test("Summon test 1 - Bahamut", smnTest3TestFunction, smnTest3ValidationFunction)
    smnTestSuite.addTest(smntest3)

    # Summon test 2

    def smnTest4TestFunction() -> None:
        """This test checks the total potency done by Phoenix when summoned and makes sure he dissapears after the given time duration.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, Enkindle, Deathflare, WaitAbility(15), Ruin3, WaitAbility(60), Summon, Enkindle, WaitAbility(15)]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        pet = player.Pet
        return [player.TotalPotency, pet.TrueLock]

    def smnTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3320 + 1300 + 240*5, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest4 = test("Summon test 2 - Phoenix", smnTest4TestFunction, smnTest4ValidationFunction)
    smnTestSuite.addTest(smntest4)

    # Searing Light Test

    def smnTest5TestFunction() -> None:
        """This tests if Searing light works correctly.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [SearingLight, WaitAbility(15)]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [SearingLightbuff in Dummy.buffList]

    def smnTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest5 = test("Searing Light test 1", smnTest5TestFunction, smnTest5ValidationFunction)
    smnTestSuite.addTest(smntest5)

    # Searing Light Test 2

    def smnTest6TestFunction() -> None:
        """This tests if Searing light works correctly.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [SearingLight, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [SearingLightbuff in Dummy.buffList]

    def smnTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest6 = test("Searing Light test 2", smnTest6TestFunction, smnTest6ValidationFunction)
    smnTestSuite.addTest(smntest6)

    # Testing summoning Garuda

    def smnTest7TestFunction() -> None:
        """Testing Garuda
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Summon, WaitAbility(15), Garuda, Emerald, Swiftcast, Emerald, Slipstream]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.GarudaStack, player.GarudaSpecial, player.CastingSpell.CastTime]

    def smnTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2, False, 0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest7 = test("Primal test 1 - Garuda", smnTest7TestFunction, smnTest7ValidationFunction)
    smnTestSuite.addTest(smntest7)

    # Testing summoning Garuda interupted by ifrit

    def smnTest8TestFunction() -> None:
        """Testing Garuda interupted by ifrit
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Summon, WaitAbility(15), Garuda, Emerald, Swiftcast, Emerald, Ifrit, Ruby, Cyclone]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.GarudaStack, player.GarudaSpecial, player.IfritStack, player.IfritSpecial, player.IfritSpecialCombo]

    def smnTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False, 1, False, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest8 = test("Primal test 2 - Garuda/Ifrit", smnTest8TestFunction, smnTest8ValidationFunction)
    smnTestSuite.addTest(smntest8)

    # Testing summoning Garuda interupted by ifrit

    def smnTest9TestFunction() -> None:
        """Testing Ifrit interupted by Titan
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Summon, WaitAbility(15), Ifrit, Cyclone, Ruby, Ruby, Titan, Topaz, Mountain, Topaz]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.IfritStack, player.IfritSpecial, player.IfritSpecialCombo, player.IfritGem, player.TitanGem, player.TitanStack, player.TitanSpecial ]

    def smnTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,False, False, False, False, 2, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest9 = test("Primal test 3 - Ifrit/Titan", smnTest9TestFunction, smnTest9ValidationFunction)
    smnTestSuite.addTest(smntest9)

    # RuinIV test

    def smnTest10TestFunction() -> None:
        """Making sure RuinIV is used up
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [EnergyDrainSMN]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.FurtherRuin]

    def smnTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest10 = test("FurtherRuin test 1", smnTest10TestFunction, smnTest10ValidationFunction)
    smnTestSuite.addTest(smntest10)

    # RuinIV test 2

    def smnTest11TestFunction() -> None:
        """Making sure RuinIV is used up
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 544, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [EnergyDrainSMN, Ruin4]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.FurtherRuin]

    def smnTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    smntest11 = test("FurtherRuin test 2", smnTest11TestFunction, smnTest11ValidationFunction)
    smnTestSuite.addTest(smntest11)

    return smnTestSuite

######################################
#          Scholar testSuite         #
######################################

def generateSCHTestSuite() -> testSuite:

    schTestSuite = testSuite("Scholar test suite")

    # Opener requirement, end time and potency test 1

    def schTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Dissipation, Broil, EnergyDrain, 
                    Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def schTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 36.95, 6020]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest1 = test("Opener requirement, end time and potency 1", schTest1TestFunction, schTest1ValidationFunction)
    schTestSuite.addTest(schtest1)

    # AetherStack test 1

    def schTest2TestFunction() -> None:
        """Testing Aetherstack
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Aetherflow, EnergyDrain, EnergyDrain]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AetherFlowStack]

    def schTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest2 = test("Aetherstack test 1", schTest2TestFunction, schTest2ValidationFunction)
    schTestSuite.addTest(schtest2)

    # AetherStack test 2

    def schTest3TestFunction() -> None:
        """Testing Aetherstack 2
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Aetherflow, EnergyDrain, EnergyDrain, Dissipation]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AetherFlowStack]

    def schTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest3 = test("Aetherstack test 2", schTest3TestFunction, schTest3ValidationFunction)
    schTestSuite.addTest(schtest3)

    # AetherStack test 3

    def schTest4TestFunction() -> None:
        """Testing Aetherstack 3
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Aetherflow, EnergyDrain, EnergyDrain, Dissipation, EnergyDrain, EnergyDrain, EnergyDrain]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AetherFlowStack]

    def schTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest4 = test("Aetherstack test 3", schTest4TestFunction, schTest4ValidationFunction)
    schTestSuite.addTest(schtest4)

    # AetherStack test 4

    def schTest5TestFunction() -> None:
        """Testing Aetherstack 4
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Aetherflow, EnergyDrain, EnergyDrain, Dissipation, EnergyDrain, EnergyDrain, EnergyDrain]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AetherFlowStack]

    def schTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest5 = test("Aetherstack test 4", schTest5TestFunction, schTest5ValidationFunction)
    schTestSuite.addTest(schtest5)

    # AetherStack test 5

    def schTest6TestFunction() -> None:
        """Testing Aetherstack 5
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dissipation, EnergyDrain, EnergyDrain]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AetherFlowStack]

    def schTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest6 = test("Aetherstack test 6", schTest6TestFunction, schTest6ValidationFunction)
    schTestSuite.addTest(schtest6)

    # Chain Stratagem test
    def schTest7TestFunction() -> None:
        """Testing Chain Stratagem
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [ChainStratagem, WaitAbility(5)]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.ChainStratagem]

    def schTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest7 = test("Chain Stratagem test 1", schTest7TestFunction, schTest7ValidationFunction)
    schTestSuite.addTest(schtest7)

    # Chain Stratagem test
    def schTest8TestFunction() -> None:
        """Testing Chain Stratagem
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [ChainStratagem, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.ChainStratagem]

    def schTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    schtest8 = test("Chain Stratagem test 2", schTest8TestFunction, schTest8ValidationFunction)
    schTestSuite.addTest(schtest8)

    return schTestSuite

######################################
#          Whitemage testSuite       #
######################################

def generateWHMTestSuite() -> testSuite:

    whmTestSuite = testSuite("Whitemage test suite")

    # Opener requirement, end time and potency test 1

    def whmTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare, Dia, Glare, Glare, PresenceOfMind, Glare, Assize, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare
                    , Glare, Glare, Glare, Glare, Glare ]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def whmTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 37.29, 6330]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest1 = test("Opener requirement, end time and potency 1", whmTest1TestFunction, whmTest1ValidationFunction)
    whmTestSuite.addTest(whmtest1)

    # Thin air test

    def whmTest2TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [ThinAir,Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.ManaCost]

    def whmTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest2 = test("Thin air test 1", whmTest2TestFunction, whmTest2ValidationFunction)
    whmTestSuite.addTest(whmtest2)

    # Thin air test 2

    def whmTest3TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [ThinAir,Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.ManaCost]

    def whmTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest3 = test("Thin air test 2", whmTest3TestFunction, whmTest3ValidationFunction)
    whmTestSuite.addTest(whmtest3)

    # Thin air test 3

    def whmTest4TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [ThinAir,Assize, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.ManaCost]

    def whmTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest4 = test("Thin air test 3", whmTest4TestFunction, whmTest4ValidationFunction)
    whmTestSuite.addTest(whmtest4)

    # PoM test

    def whmTest5TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [PresenceOfMind, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Haste, PresenceOfMindEffect in player.EffectList ]

    def whmTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [20, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest5 = test("Presence of Mind test 1", whmTest5TestFunction, whmTest5ValidationFunction)
    whmTestSuite.addTest(whmtest5)\

    # PoM test 2

    def whmTest6TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [PresenceOfMind, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Haste, PresenceOfMindEffect in player.EffectList ]

    def whmTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest6 = test("Presence of Mind test 2", whmTest6TestFunction, whmTest6ValidationFunction)
    whmTestSuite.addTest(whmtest6)

    # Lily Test

    def whmTest7TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare,WaitAbility(40.02)]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.LilyStack, player.UsedLily, player.BloomLily]

    def whmTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2, 0, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest7 = test("Lily generation/usage test 1", whmTest7TestFunction, whmTest7ValidationFunction)
    whmTestSuite.addTest(whmtest7)

    # Lily Test

    def whmTest8TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare,WaitAbility(60.06)]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.LilyStack, player.UsedLily, player.BloomLily]

    def whmTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3, 0, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest8 = test("Lily generation/usage test 2", whmTest8TestFunction, whmTest8ValidationFunction)
    whmTestSuite.addTest(whmtest8)

    # Lily Test 3

    def whmTest9TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare,WaitAbility(60), AfflatusRapture, AfflatusSolace, WaitAbility(20)]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.LilyStack, player.UsedLily, player.BloomLily]

    def whmTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2, 2, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest9 = test("Lily generation/usage test 3", whmTest9TestFunction, whmTest9ValidationFunction)
    whmTestSuite.addTest(whmtest9)

    # Lily Test 4

    def whmTest10TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare,WaitAbility(60), AfflatusRapture, AfflatusSolace, WaitAbility(20), AfflatusRapture]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.LilyStack, player.UsedLily, player.BloomLily]

    def whmTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1, 3, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest10 = test("Lily generation/usage test 4", whmTest10TestFunction, whmTest10ValidationFunction)
    whmTestSuite.addTest(whmtest10)

    # Lily Test 5

    def whmTest11TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 839, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Glare,WaitAbility(60), AfflatusRapture, AfflatusSolace, WaitAbility(20), AfflatusRapture, AfflatusMisery, AfflatusSolace]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.LilyStack, player.UsedLily, player.BloomLily]

    def whmTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 1, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    whmtest11 = test("Lily generation/usage test 5", whmTest11TestFunction, whmTest11ValidationFunction)
    whmTestSuite.addTest(whmtest11)

    return whmTestSuite

######################################
#          Astrologian testSuite     #
######################################

def generateASTTestSuite() -> testSuite:

    astTestSuite = testSuite("Astrologian test suite")

    # Opener requirement, end time and potency test 1

    def astTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw, WaitAbility(30),Malefic, Lightspeed, Combust, Arcanum(NINPlayer, "Lunar", True), Draw, Malefic,Arcanum(NINPlayer, "Solar", True), Draw, Malefic,Arcanum(NINPlayer, "Celestial", True), 
                    Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, 
                    Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, 
                    Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,Combust, WaitAbility(30)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def astTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 95.72, 8350]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest1 = test("Opener requirement, end time and potency 1", astTest1TestFunction, astTest1ValidationFunction)
    astTestSuite.addTest(asttest1)

    # Arcana test

    def astTest2TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw,Arcanum(NINPlayer, "Solar", True), Arcanum(NINPlayer, "Lunar", True),Draw]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, len(NINPlayer.buffList), player.HasCard]

    def astTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False, 1, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest2 = test("Arcana test 1", astTest2TestFunction, astTest2ValidationFunction)
    astTestSuite.addTest(asttest2)

    # Arcana test 2

    def astTest3TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True), Arcanum(NINPlayer, "Lunar", True), Arcanum(NINPlayer, "Lunar", True)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, len(NINPlayer.buffList), ]

    def astTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False,1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest3 = test("Arcana test 2", astTest3TestFunction, astTest3ValidationFunction)
    astTestSuite.addTest(asttest3)

    # Arcana test 3

    def astTest4TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True), Arcanum(NINPlayer, "Lunar", True), Arcanum(NINPlayer, "Celestial", True), WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, len(NINPlayer.buffList)]

    def astTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, True,0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest4 = test("Arcana test 3", astTest4TestFunction, astTest4ValidationFunction)
    astTestSuite.addTest(asttest4)

    # Arcana test 4

    def astTest5TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Astrodyne]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, BodyEffect in player.EffectList]

    def astTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest5 = test("Arcana test 4 - Astrodyne", astTest5TestFunction, astTest5ValidationFunction)
    astTestSuite.addTest(asttest5)

    # Arcana test 5

    def astTest6TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Solar", True),Astrodyne]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, BodyEffect in player.EffectList, len(NINPlayer.buffList)]

    def astTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False, False,1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest6 = test("Arcana test 5 - Astrodyne", astTest6TestFunction, astTest6ValidationFunction)
    astTestSuite.addTest(asttest6)

    # Arcana test 6

    def astTest7TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Astrodyne]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, BodyEffect in player.EffectList]

    def astTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest7 = test("Arcana test 6 - Astrodyne", astTest7TestFunction, astTest7ValidationFunction)
    astTestSuite.addTest(asttest7)

    # Arcana test 7

    def astTest8TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Arcanum(NINPlayer, "Celestial", True),Astrodyne]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, BodyEffect in player.EffectList,AstrodyneBuff in player.buffList]

    def astTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False, True, True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest8 = test("Arcana test 7 - Astrodyne", astTest8TestFunction, astTest8ValidationFunction)
    astTestSuite.addTest(asttest8)

    # Arcana test 8

    def astTest9TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Arcanum(NINPlayer, "Celestial", True),Astrodyne,
                    Arcanum(NINPlayer, "Solar", True), WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Solar, player.Lunar, player.Celestial, BodyEffect in player.EffectList,AstrodyneBuff in player.buffList]

    def astTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, False, False, False, False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest9 = test("Arcana test 8 - Astrodyne", astTest9TestFunction, astTest9ValidationFunction)
    astTestSuite.addTest(asttest9)

    # Lightspeed

    def astTest10TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1473, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Lightspeed, Malefic, Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime]

    def astTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest10 = test("Lightspeed test 1", astTest10TestFunction, astTest10ValidationFunction)
    astTestSuite.addTest(asttest10)

    # Lightspeed 2

    def astTest11TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Lightspeed, Malefic, Malefic, WaitAbility(12.52), Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime]

    def astTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.5]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest11 = test("Lightspeed test 2", astTest11TestFunction, astTest11ValidationFunction)
    astTestSuite.addTest(asttest11)

    # Draw/Redrawtest

    def astTest12TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.HasCard, player.Redraw, player.DrawStack]

    def astTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, 1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest12 = test("Draw/Redraw test 1", astTest12TestFunction, astTest12ValidationFunction)
    astTestSuite.addTest(asttest12)

    # Draw/Redrawtest 2

    def astTest13TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw, Redraw]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.HasCard, player.Redraw, player.DrawStack]

    def astTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, False, 1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest13 = test("Draw/Redraw test 2", astTest13TestFunction, astTest13ValidationFunction)
    astTestSuite.addTest(asttest13)

    # Draw/Redrawtest 3

    def astTest14TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw, Redraw, Arcanum(NINPlayer, "Solar", True)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.HasCard, player.Redraw, player.DrawStack]

    def astTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, 1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest14 = test("Draw/Redraw test 3", astTest14TestFunction, astTest14ValidationFunction)
    astTestSuite.addTest(asttest14)

    # Draw/Redrawtest 4

    def astTest15TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw, Redraw, Arcanum( NINPlayer,"Solar", True), Draw]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.HasCard, player.Redraw, player.DrawStack]

    def astTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, 0]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest15 = test("Draw/Redraw test 4", astTest15TestFunction, astTest15ValidationFunction)
    astTestSuite.addTest(asttest15)

    # Draw/Redrawtest 5

    def astTest16TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Draw, Redraw, Arcanum( NINPlayer,"Solar", True), Draw, Arcanum( NINPlayer,"Lunar", True), WaitAbility(30)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.HasCard, player.Redraw, player.DrawStack]

    def astTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
                                # Note that Redraw is still true. However this won't affect anything
                                # since Redraw does not do anything since the solver does not check
                                # if a specific card was drawn. It simply checks if a card was drawn
                                # for arcanum requirement. So redraw effectively does nothing here.
        expected = [False, True, 1]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest16 = test("Draw/Redraw test 5", astTest16TestFunction, astTest16ValidationFunction)
    astTestSuite.addTest(asttest16)

    # Divination test 1

    def astTest17TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Divination, Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DivinationBuff in Dummy.buffList]

    def astTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
                                # Note that Redraw is still true. However this won't affect anything
                                # since Redraw does not do anything since the solver does not check
                                # if a specific card was drawn. It simply checks if a card was drawn
                                # for arcanum requirement. So redraw effectively does nothing here.
        expected = [True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest17 = test("Divination test 1", astTest17TestFunction, astTest17ValidationFunction)
    astTestSuite.addTest(asttest17)

    # Divination test 1

    def astTest17TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Divination, Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DivinationBuff in Dummy.buffList]

    def astTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
                                # Note that Redraw is still true. However this won't affect anything
                                # since Redraw does not do anything since the solver does not check
                                # if a specific card was drawn. It simply checks if a card was drawn
                                # for arcanum requirement. So redraw effectively does nothing here.
        expected = [True]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest17 = test("Divination test 1", astTest17TestFunction, astTest17ValidationFunction)
    astTestSuite.addTest(asttest17)

    # Divination test 2

    def astTest18TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([WaitAbility(1)], [], Stat, JobEnum.Ninja)

        actionSet = [Divination, Malefic, WaitAbility(15)]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DivinationBuff in Dummy.buffList]

    def astTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
                                # Note that Redraw is still true. However this won't affect anything
                                # since Redraw does not do anything since the solver does not check
                                # if a specific card was drawn. It simply checks if a card was drawn
                                # for arcanum requirement. So redraw effectively does nothing here.
        expected = [False]    

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    asttest18 = test("Divination test 2", astTest18TestFunction, astTest18ValidationFunction)
    astTestSuite.addTest(asttest18)

    return astTestSuite

######################################
#            Sage testSuite          #
######################################

def generateSGETestSuite() -> testSuite:

    sgeTestSuite = testSuite("Sage test suite")

    # Opener requirement, end time and potency test 1

    def sgeTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, Eukrasia, EukrasianDosis, Dosis,Dosis, Phlegma, Phlegma, Dosis, Pneuma, Dosis, Dosis,
                    Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis,Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def sgeTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 51.39, 8000]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest1 = test("Opener requirement, end time and potency 1", sgeTest1TestFunction, sgeTest1ValidationFunction)
    sgeTestSuite.addTest(sgetest1)

    # Addersgall test 1

    def sgeTest2TestFunction() -> None:
        """Tests Addersgall
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AddersgallStack]

    def sgeTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3]   # TODO Check that?

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest2 = test("Addersgall test 1", sgeTest2TestFunction, sgeTest2ValidationFunction)
    sgeTestSuite.addTest(sgetest2)

    # Addersgall test 2

    def sgeTest3TestFunction() -> None:
        """Tests Addersgall
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, WaitAbility(20.02), WaitAbility(20.02), Rhizomata]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AddersgallStack]

    def sgeTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest3 = test("Addersgall test 2", sgeTest3TestFunction, sgeTest3ValidationFunction)
    sgeTestSuite.addTest(sgetest3)

    # Addersgall test 3

    def sgeTest4TestFunction() -> None:
        """Tests Addersgall
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, WaitAbility(20.02), WaitAbility(20.02), Rhizomata,WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AddersgallStack]

    def sgeTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest4 = test("Addersgall test 3", sgeTest4TestFunction, sgeTest4ValidationFunction)
    sgeTestSuite.addTest(sgetest4)

    # Addersgall test 4

    def sgeTest5TestFunction() -> None:
        """Tests Addersgall
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, WaitAbility(20.02), WaitAbility(20.02), Rhizomata,WaitAbility(20.02), Taurochole, Ixochole]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AddersgallStack]

    def sgeTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest5 = test("Addersgall test 4", sgeTest5TestFunction, sgeTest5ValidationFunction)
    sgeTestSuite.addTest(sgetest5)

    # Addersgall test 5

    def sgeTest6TestFunction() -> None:
        """Tests Addersgall
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, WaitAbility(20.02), WaitAbility(20.02), Rhizomata,WaitAbility(20.02), Taurochole, Ixochole, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AddersgallStack]

    def sgeTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest6 = test("Addersgall test 5", sgeTest6TestFunction, sgeTest6ValidationFunction)
    sgeTestSuite.addTest(sgetest6)

    # Addersting test 1

    def sgeTest7TestFunction() -> None:
        """Tests Addersting
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AdderstingStack]

    def sgeTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest7 = test("Addersting test 1", sgeTest7TestFunction, sgeTest7ValidationFunction)
    sgeTestSuite.addTest(sgetest7)

    # Addersting test 2

    def sgeTest8TestFunction() -> None:
        """Tests Addersting
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, Dosis, Eukrasia, EukrasianDiagnosis, Diagnosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AdderstingStack]

    def sgeTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest8 = test("Addersting test 2", sgeTest8TestFunction, sgeTest8ValidationFunction)
    sgeTestSuite.addTest(sgetest8)

    # Addersting test 3

    def sgeTest9TestFunction() -> None:
        """Tests Addersting
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, Dosis, Eukrasia, EukrasianDiagnosis, Diagnosis, Haima, Toxikon]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AdderstingStack]

    def sgeTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest9 = test("Addersting test 3", sgeTest9TestFunction, sgeTest9ValidationFunction)
    sgeTestSuite.addTest(sgetest9)

    # Addersting test 4

    def sgeTest10TestFunction() -> None:
        """Tests Addersting
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 827, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Dosis, Dosis, Eukrasia, EukrasianDiagnosis, Diagnosis, Haima, Diagnosis, Diagnosis, Toxikon]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.AdderstingStack]

    def sgeTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    sgetest10 = test("Addersting test 4", sgeTest10TestFunction, sgeTest10ValidationFunction)
    sgeTestSuite.addTest(sgetest10)

    return sgeTestSuite

######################################
#        Machinist testSuite         #
######################################

def generateMCHTestSuite() -> testSuite:

    mchTestSuite = testSuite("Machinist test suite")

    # Opener requirement, end time and potency test 1

    def mchTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Reassemble,WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, 
                    SlugShot, GaussRound, Ricochet,CleanShot, Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton, Hypercharge, HeatBlast, Ricochet, 
                    HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, WaitAbility(60)]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def mchTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 82.52, 11050]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest1 = test("Opener requirement, end time and potency 1", mchTest1TestFunction, mchTest1ValidationFunction)
    mchTestSuite.addTest(mchtest1)

    # Heat blast test

    def mchTest2TestFunction() -> None:
        """Heat blast test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ricochet, Ricochet, Hypercharge, HeatBlast, GaussRound, GaussRound]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RicochetStack, round(player.RicochetCD,2), player.GaussRoundStack, round(player.GaussRoundCD,2)]

    def mchTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1, 14.95, 1, 29.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest2 = test("Hypercharge test 1 - Heat blast", mchTest2TestFunction, mchTest2ValidationFunction)
    mchTestSuite.addTest(mchtest2)

    # Heat blast test

    def mchTest3TestFunction() -> None:
        """Heat blast test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ricochet, Ricochet, GaussRound, Hypercharge, HeatBlast, HeatBlast,GaussRound]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RicochetStack, round(player.RicochetCD,2), player.GaussRoundStack, round(player.GaussRoundCD,2)]

    def mchTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2, 28.45,2, 30]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest3 = test("Hypercharge test 2 - Heat blast", mchTest3TestFunction, mchTest3ValidationFunction)
    mchTestSuite.addTest(mchtest3)

    # Heat blast test

    def mchTest4TestFunction() -> None:
        """Heat blast test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ricochet, Ricochet, Hypercharge, HeatBlast, Ricochet, HeatBlast, Ricochet, HeatBlast]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RicochetStack, round(player.RicochetCD,2), player.GaussRoundStack, round(player.GaussRoundCD,2)]

    def mchTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 11.97, 3, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest4 = test("Hypercharge test 3 - Heat blast", mchTest4TestFunction, mchTest4ValidationFunction)
    mchTestSuite.addTest(mchtest4)

    # Heat blast test

    def mchTest5TestFunction() -> None:
        """Heat blast test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ricochet, Ricochet, Hypercharge, HeatBlast, Ricochet, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, WaitAbility(0.01)]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RicochetStack, round(player.RicochetCD,2), player.GaussRoundStack, round(player.GaussRoundCD,2)]

    def mchTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1, 25.46, 2, 13.5]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest5 = test("Hypercharge test 4 - Heat blast", mchTest5TestFunction, mchTest5ValidationFunction)
    mchTestSuite.addTest(mchtest5)

    # Wildfire test

    def mchTest6TestFunction() -> None:
        """Wildfire test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Wildfire, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WildFireStack]

    def mchTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [6]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest6 = test("Wildfire test 1", mchTest6TestFunction, mchTest6ValidationFunction)
    mchTestSuite.addTest(mchtest6)

    # Wildfire test

    def mchTest7TestFunction() -> None:
        """Wildfire test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Wildfire, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast, HeatBlast]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WildFireStack]

    def mchTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest7 = test("Wildfire test 2", mchTest7TestFunction, mchTest7ValidationFunction)
    mchTestSuite.addTest(mchtest7)

    # Wildfire test

    def mchTest8TestFunction() -> None:
        """Wildfire test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Wildfire]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WildFireStack]

    def mchTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest8 = test("Wildfire test 3", mchTest8TestFunction, mchTest8ValidationFunction)
    mchTestSuite.addTest(mchtest8)

    # Wildfire test

    def mchTest9TestFunction() -> None:
        """Wildfire test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Wildfire, GaussRound, GaussRound, GaussRound, GaussRound, GaussRound, GaussRound, GaussRound, GaussRound, GaussRound, SplitShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.WildFireStack]

    def mchTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest9 = test("Wildfire test 4", mchTest9TestFunction, mchTest9ValidationFunction)
    mchTestSuite.addTest(mchtest9)

    # Combo test

    def mchTest10TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SplitShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest10 = test("Combo action potency test 1", mchTest10TestFunction, mchTest10ValidationFunction)
    mchTestSuite.addTest(mchtest10)

    # Combo test

    def mchTest11TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [CleanShot, SlugShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest11 = test("Combo action potency test 2", mchTest11TestFunction, mchTest11ValidationFunction)
    mchTestSuite.addTest(mchtest11)

    # Combo test

    def mchTest12TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest12 = test("Combo action potency test 3", mchTest12TestFunction, mchTest12ValidationFunction)
    mchTestSuite.addTest(mchtest12)

    # Combo test

    def mchTest13TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SlugShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest13 = test("Combo action potency test 4", mchTest13TestFunction, mchTest13ValidationFunction)
    mchTestSuite.addTest(mchtest13)

    # Combo test

    def mchTest14TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SlugShot, SplitShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest14 = test("Combo action potency test 5", mchTest14TestFunction, mchTest14ValidationFunction)
    mchTestSuite.addTest(mchtest14)

    # Combo test

    def mchTest15TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, CleanShot, SlugShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest15 = test("Combo action potency test 6", mchTest15TestFunction, mchTest15ValidationFunction)
    mchTestSuite.addTest(mchtest15)

    # Combo test

    def mchTest16TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SplitShot, SlugShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest16 = test("Combo action potency test 7", mchTest16TestFunction, mchTest16ValidationFunction)
    mchTestSuite.addTest(mchtest16)

    # Combo test

    def mchTest17TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SlugShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest17 = test("Combo action potency test 8", mchTest17TestFunction, mchTest17ValidationFunction)
    mchTestSuite.addTest(mchtest17)

    # Combo test

    def mchTest18TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, SlugShot, CleanShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mchTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest18 = test("Combo action potency test 9", mchTest18TestFunction, mchTest18ValidationFunction)
    mchTestSuite.addTest(mchtest18)

    # Automaton test

    def mchTest19TestFunction() -> None:
        """Automaton test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, Automaton, WaitAbility(15), SplitShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        pet = player.Pet
        return [pet.TrueLock, player.TotalPotency]

    def mchTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 2430]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest19 = test("Automaton test 1", mchTest19TestFunction, mchTest19ValidationFunction)
    mchTestSuite.addTest(mchtest19)


    # Automaton test

    def mchTest20TestFunction() -> None:
        """Automaton test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, Automaton, WaitAbility(15), SplitShot, Automaton, Overdrive, WaitAbility(6)]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        pet = player.Pet
        return [pet.TrueLock, player.TotalPotency]

    def mchTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 4140]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest20 = test("Automaton test 2", mchTest20TestFunction, mchTest20ValidationFunction)
    mchTestSuite.addTest(mchtest20)

    # Automaton test

    def mchTest21TestFunction() -> None:
        """Automaton test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SplitShot, Automaton, WaitAbility(15), SplitShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)
        player.BatteryGauge = 100

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        pet = player.Pet
        return [pet.TrueLock, player.TotalPotency]

    def mchTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 3210]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mchtest21 = test("Automaton test 3 - Max Battery Gauge", mchTest21TestFunction, mchTest21ValidationFunction)
    mchTestSuite.addTest(mchtest21)

    return mchTestSuite

######################################
#           Bard testSuite           #
######################################

def generateBRDTestSuite() -> testSuite:

    brdTestSuite = testSuite("Bard test suite")

    # Opener requirement, end time and potency test 1

    def brdTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale,
                    BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, WaitAbility(0.9), EmpyrealArrow, IronJaws, PitchPerfect3, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def brdTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 70.00, 6670]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest1 = test("Opener requirement, end time and potency 1", brdTest1TestFunction, brdTest1ValidationFunction)
    brdTestSuite.addTest(brdtest1)

    # Iron Jaws test

    def brdTest2TestFunction() -> None:
        """This tests Iron jaws reapplying dot
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [IronJaws]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StormbiteDOTTimer, player.CausticbiteDOTTimer]

    def brdTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest2 = test("Iron jaws test 1", brdTest2TestFunction, brdTest2ValidationFunction)
    brdTestSuite.addTest(brdtest2)

    # Iron Jaws test

    def brdTest3TestFunction() -> None:
        """This tests Iron jaws reapplying dot
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Causticbite,IronJaws]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StormbiteDOTTimer, player.CausticbiteDOTTimer]

    def brdTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,45]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest3 = test("Iron jaws test 2", brdTest3TestFunction, brdTest3ValidationFunction)
    brdTestSuite.addTest(brdtest3)

    # Iron Jaws test

    def brdTest4TestFunction() -> None:
        """This tests Iron jaws reapplying dot
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Causticbite,Stormbite, WaitAbility(30), IronJaws]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StormbiteDOTTimer, player.CausticbiteDOTTimer]

    def brdTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [45,45]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest4 = test("Iron jaws test 3", brdTest4TestFunction, brdTest4ValidationFunction)
    brdTestSuite.addTest(brdtest4)

    # Iron Jaws test

    def brdTest5TestFunction() -> None:
        """This tests Iron jaws reapplying dot
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Stormbite,Causticbite, WaitAbility(47.6), IronJaws]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StormbiteDOTTimer, player.CausticbiteDOTTimer]

    def brdTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest5 = test("Iron jaws test 4", brdTest5TestFunction, brdTest5ValidationFunction)
    brdTestSuite.addTest(brdtest5)

    # Iron Jaws test

    def brdTest5TestFunction() -> None:
        """This tests Iron jaws reapplying dot
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Stormbite,Causticbite, WaitAbility(47.6), IronJaws]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StormbiteDOTTimer, player.CausticbiteDOTTimer]

    def brdTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest5 = test("Iron jaws test 4", brdTest5TestFunction, brdTest5ValidationFunction)
    brdTestSuite.addTest(brdtest5)

    # Song test

    def brdTest6TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [WanderingMinuet, WaitAbility(20), BurstShot]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.WanderingMinuet, round(player.SongTimer,2)]

    def brdTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,24.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest6 = test("Song test 1", brdTest6TestFunction, brdTest6ValidationFunction)
    brdTestSuite.addTest(brdtest6)

    # Song test

    def brdTest7TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [WanderingMinuet, WaitAbility(45), BurstShot]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.WanderingMinuet, player.SongTimer]

    def brdTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest7 = test("Song test 2", brdTest7TestFunction, brdTest7ValidationFunction)
    brdTestSuite.addTest(brdtest7)

    # Song test

    def brdTest8TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(7)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Haste, round(player.SongTimer,2), Dummy.ArmyPaeon]

    def brdTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [6.4,38, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest8 = test("Song test 3", brdTest8TestFunction, brdTest8ValidationFunction)
    brdTestSuite.addTest(brdtest8)

    # Song test

    def brdTest9TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(20)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Haste, round(player.SongTimer,2), Dummy.ArmyPaeon]

    def brdTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [16,25.00, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest9 = test("Song test 4", brdTest9TestFunction, brdTest9ValidationFunction)
    brdTestSuite.addTest(brdtest9)

    # Song test

    def brdTest10TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(46)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Haste, round(player.SongTimer,2), Dummy.ArmyPaeon]

    def brdTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest10 = test("Song test 5", brdTest10TestFunction, brdTest10ValidationFunction)
    brdTestSuite.addTest(brdtest10)

    # Song test

    def brdTest11TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WaitAbility(20)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2)]

    def brdTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,25]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest11 = test("Song test 6", brdTest11TestFunction, brdTest11ValidationFunction)
    brdTestSuite.addTest(brdtest11)

    # Song test

    def brdTest12TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WaitAbility(46)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2)]

    def brdTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest12 = test("Song test 7", brdTest12TestFunction, brdTest12ValidationFunction)
    brdTestSuite.addTest(brdtest12)

    # Song test

    def brdTest13TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WaitAbility(20), WanderingMinuet, WaitAbility(0.01)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2), Dummy.WanderingMinuet]

    def brdTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,44.99, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest13 = test("Song test 8", brdTest13TestFunction, brdTest13ValidationFunction)
    brdTestSuite.addTest(brdtest13)

    # Song test

    def brdTest14TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WaitAbility(20), ArmyPaeon, WaitAbility(7)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2), player.Haste]

    def brdTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,38, 6.4]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest14 = test("Song test 9", brdTest14TestFunction, brdTest14ValidationFunction)
    brdTestSuite.addTest(brdtest14)

    # Song test

    def brdTest15TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WaitAbility(20), ArmyPaeon, WaitAbility(7), WanderingMinuet, WaitAbility(0.01)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2), player.Haste, Dummy.WanderingMinuet, Dummy.ArmyPaeon]

    def brdTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,44.99, 1, True,False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest15 = test("Song test 10", brdTest15TestFunction, brdTest15ValidationFunction)
    brdTestSuite.addTest(brdtest15)

    # Song test

    def brdTest16TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [WanderingMinuet, WaitAbility(20), ArmyPaeon, WaitAbility(7), MageBallad, WaitAbility(0.01)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2), player.Haste, Dummy.WanderingMinuet, Dummy.ArmyPaeon]

    def brdTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,44.99, 1, False, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest16 = test("Song test 11", brdTest16TestFunction, brdTest16ValidationFunction)
    brdTestSuite.addTest(brdtest16)

    def brdTest17TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(10), WanderingMinuet, WaitAbility(7), MageBallad, WaitAbility(0.01)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [MageBalladBuff in Dummy.buffList, round(player.SongTimer,2), player.Haste, Dummy.WanderingMinuet]

    def brdTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,44.99, 2, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest17 = test("Song test 12", brdTest17TestFunction, brdTest17ValidationFunction)
    brdTestSuite.addTest(brdtest17)

    def brdTest18TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,BurstShot,RadiantFinale, WaitAbility(1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.02, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest18 = test("Radiant Final test", brdTest18TestFunction, brdTest18ValidationFunction)
    brdTestSuite.addTest(brdtest18)

    def brdTest19TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,MageBallad,BurstShot,RadiantFinale, WaitAbility(1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.02, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest19 = test("Radiant Final test 2", brdTest19TestFunction, brdTest19ValidationFunction)
    brdTestSuite.addTest(brdtest19)

    def brdTest20TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,WanderingMinuet,BurstShot,RadiantFinale, WaitAbility(1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.04, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest20 = test("Radiant Final test 3", brdTest20TestFunction, brdTest20ValidationFunction)
    brdTestSuite.addTest(brdtest20)

    def brdTest21TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,WanderingMinuet,ArmyPaeon,BurstShot,RadiantFinale, WaitAbility(1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.06, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest21 = test("Radiant Final test 4", brdTest21TestFunction, brdTest21ValidationFunction)
    brdTestSuite.addTest(brdtest21)

    def brdTest22TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,WanderingMinuet,ArmyPaeon,BurstShot,RadiantFinale, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.06, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest22 = test("Radiant Final test 5", brdTest22TestFunction, brdTest22ValidationFunction)
    brdTestSuite.addTest(brdtest22)

    def brdTest21TestFunction() -> None:
        """This tests the different song
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,WanderingMinuet,ArmyPaeon,BurstShot,RadiantFinale, WaitAbility(1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.06, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest21 = test("Radiant Final test 4", brdTest21TestFunction, brdTest21ValidationFunction)
    brdTestSuite.addTest(brdtest21)

    def brdTest22TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad,WanderingMinuet,ArmyPaeon,BurstShot,RadiantFinale, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.RadiantFinaleBuff.MultDPS, player.RadiantFinaleBuff in Dummy.buffList]

    def brdTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.06, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest22 = test("Radiant Final test 5", brdTest22TestFunction, brdTest22ValidationFunction)
    brdTestSuite.addTest(brdtest22)

    def brdTest23TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BurstShot, RagingStrike, WaitAbility(19)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RagingStrikeBuff in player.buffList]

    def brdTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest23 = test("Raging Strike test 1", brdTest23TestFunction, brdTest23ValidationFunction)
    brdTestSuite.addTest(brdtest23)

    def brdTest24TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BurstShot, RagingStrike, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RagingStrikeBuff in player.buffList]

    def brdTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest24 = test("Raging Strike test 2", brdTest24TestFunction, brdTest24ValidationFunction)
    brdTestSuite.addTest(brdtest24)

    def brdTest25TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BurstShot, BattleVoice, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.BattleVoice]

    def brdTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest25 = test("Battle Voice test 1", brdTest25TestFunction, brdTest25ValidationFunction)
    brdTestSuite.addTest(brdtest25)

    def brdTest26TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BurstShot, BattleVoice, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Dummy.BattleVoice]

    def brdTest26ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest26 = test("Battle Voice test 2", brdTest26TestFunction, brdTest26ValidationFunction)
    brdTestSuite.addTest(brdtest26)

    def brdTest27TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [MageBallad, WanderingMinuet, WaitAbility(5)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList]

    def brdTest27ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest27 = test("Army Muse test 1", brdTest27TestFunction, brdTest27ValidationFunction)
    brdTestSuite.addTest(brdtest27)

    def brdTest28TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(45),MageBallad, WaitAbility(5)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest28ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True, 12]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest28 = test("Army Muse test 2", brdTest28TestFunction, brdTest28ValidationFunction)
    brdTestSuite.addTest(brdtest28)

    def brdTest29TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(45),MageBallad, WaitAbility(11)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest29ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest29 = test("Army Muse test 3", brdTest29TestFunction, brdTest29ValidationFunction)
    brdTestSuite.addTest(brdtest29)

    def brdTest30TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(45),WanderingMinuet, WaitAbility(5)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest30ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True, 12]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest30 = test("Army Muse test 4", brdTest30TestFunction, brdTest30ValidationFunction)
    brdTestSuite.addTest(brdtest30)

    def brdTest31TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(45),WanderingMinuet, WaitAbility(11)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest31ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest31 = test("Army Muse test 5", brdTest31TestFunction, brdTest31ValidationFunction)
    brdTestSuite.addTest(brdtest31)

    def brdTest32TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(46)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest32ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest32 = test("Army Muse test 6", brdTest32TestFunction, brdTest32ValidationFunction)
    brdTestSuite.addTest(brdtest32)

    def brdTest33TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ArmyPaeon, WaitAbility(46), WaitAbility(30), MageBallad, WaitAbility(0.1)]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [checkArmyEthos in player.EffectCDList, armyMuseCheck in player.EffectCDList, player.Haste]

    def brdTest33ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    brdtest33 = test("Army Muse test 7", brdTest33TestFunction, brdTest33ValidationFunction)
    brdTestSuite.addTest(brdtest33)

    return brdTestSuite

######################################
#           Dancer testSuite           #
######################################

def generateDNCTestSuite() -> testSuite:

    dncTestSuite = testSuite("Dancer test suite")

    # Opener requirement, end time and potency test 1

    def dncTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [StandardStep, Pirouette, Jete, WaitAbility(15), StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment,
                    StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def dncTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 18.49, 5420]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest1 = test("Opener requirement, end time and potency 1", dncTest1TestFunction, dncTest1ValidationFunction)
    dncTestSuite.addTest(dnctest1)

    # Standard Step test

    def dncTest2TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [],Stat, JobEnum.Ninja)
        actionSet = [ClosedPosition(NINPlayer),StandardStep,StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)
        
        
        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360, True, 1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest2 = test("Standard Step test 1", dncTest2TestFunction, dncTest2ValidationFunction)
    dncTestSuite.addTest(dnctest2)

    # Standard Step test

    def dncTest3TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [540, True, 1.02]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest3 = test("Standard Step test 2", dncTest3TestFunction, dncTest3ValidationFunction)
    dncTestSuite.addTest(dnctest3)

    # Standard Step test

    def dncTest4TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,Pirouette,StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [720, True, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest4 = test("Standard Step test 3", dncTest4TestFunction, dncTest4ValidationFunction)
    dncTestSuite.addTest(dnctest4)

    # Standard Step test

    def dncTest5TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,Entrechat,Pirouette,StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [720, True, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest5 = test("Standard Step test 4", dncTest5TestFunction, dncTest5ValidationFunction)
    dncTestSuite.addTest(dnctest5)

    # Standard Step test

    def dncTest6TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,Entrechat,Pirouette,StandardFinish, WaitAbility(59.99)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest6 = test("Standard Step test 5", dncTest6TestFunction, dncTest6ValidationFunction)
    dncTestSuite.addTest(dnctest6)

    # Standard Step test

    def dncTest7TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,Entrechat,Pirouette,StandardFinish, WaitAbility(60.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff]

    def dncTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, None]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest7 = test("Standard Step test 6", dncTest7TestFunction, dncTest7ValidationFunction)
    dncTestSuite.addTest(dnctest7)

    # Standard Step test

    def dncTest8TestFunction() -> None:
        """Standard Step test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),StandardStep, Jete,Entrechat,Pirouette,StandardFinish, WaitAbility(30), Ending]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StandardFinishBuff in NINPlayer.buffList, player.StandardFinishBuff.MultDPS]

    def dncTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest8 = test("Standard Step test 7", dncTest8TestFunction, dncTest8ValidationFunction)
    dncTestSuite.addTest(dnctest8)

    # Devilment

    def dncTest9TestFunction() -> None:
        """Devilment
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [Devilment, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, player.DHRateBonus]

    def dncTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0.2,0.2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest9 = test("Devilment test 1", dncTest9TestFunction, dncTest9ValidationFunction)
    dncTestSuite.addTest(dnctest9)

    # Devilment

    def dncTest10TestFunction() -> None:
        """Devilment
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),Devilment, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, player.DHRateBonus, NINPlayer.CritRateBonus, NINPlayer.DHRateBonus]

    def dncTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0.2,0.2,0.2,0.2]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest10 = test("Devilment test 2", dncTest10TestFunction, dncTest10ValidationFunction)
    dncTestSuite.addTest(dnctest10)

    # Devilment

    def dncTest11TestFunction() -> None:
        """Devilment
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),Devilment, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, player.DHRateBonus, NINPlayer.CritRateBonus, NINPlayer.DHRateBonus]

    def dncTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0,0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest11 = test("Devilment test 3", dncTest11TestFunction, dncTest11ValidationFunction)
    dncTestSuite.addTest(dnctest11)

    # Devilment

    def dncTest12TestFunction() -> None:
        """Devilment
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),Devilment, WaitAbility(10), Ending]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, player.DHRateBonus, NINPlayer.CritRateBonus, NINPlayer.DHRateBonus]

    def dncTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0.2,0.2,0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest12 = test("Devilment test 4", dncTest12TestFunction, dncTest12ValidationFunction)
    dncTestSuite.addTest(dnctest12)

    # Devilment

    def dncTest13TestFunction() -> None:
        """Devilment
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer),Devilment, WaitAbility(10), Ending, WaitAbility(10.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])


        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, player.DHRateBonus, NINPlayer.CritRateBonus, NINPlayer.DHRateBonus]

    def dncTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0,0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest13 = test("Devilment test 5", dncTest13TestFunction, dncTest13ValidationFunction)
    dncTestSuite.addTest(dnctest13)

    # Technical Finish

    def dncTest14TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep, TechnicalFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [350, True, 1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest14 = test("Techincal Finish test 1", dncTest14TestFunction, dncTest14ValidationFunction)
    dncTestSuite.addTest(dnctest14)

    # Technical Finish

    def dncTest15TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete, TechnicalFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [540, True, 1.01]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest15 = test("Techincal Finish test 2", dncTest15TestFunction, dncTest15ValidationFunction)
    dncTestSuite.addTest(dnctest15)

    # Technical Finish

    def dncTest16TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette, TechnicalFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [720, True, 1.02]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest16 = test("Techincal Finish test 3", dncTest16TestFunction, dncTest16ValidationFunction)
    dncTestSuite.addTest(dnctest16)

    # Technical Finish

    def dncTest17TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette,Entrechat, TechnicalFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [900, True, 1.03]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest17 = test("Techincal Finish test 4", dncTest17TestFunction, dncTest17ValidationFunction)
    dncTestSuite.addTest(dnctest17)

    # Technical Finish

    def dncTest18TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette,Entrechat,Emboite, TechnicalFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1200, True, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest18 = test("Techincal Finish test 5", dncTest18TestFunction, dncTest18ValidationFunction)
    dncTestSuite.addTest(dnctest18)

    # Technical Finish

    def dncTest19TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette,Entrechat,Emboite, TechnicalFinish, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff.MultDPS]

    def dncTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 1.05]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest19 = test("Techincal Finish test 6", dncTest19TestFunction, dncTest19ValidationFunction)
    dncTestSuite.addTest(dnctest19)

    # Technical Finish

    def dncTest20TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette,Entrechat,Emboite, TechnicalFinish, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff]

    def dncTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, None]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest20 = test("Techincal Finish test 7", dncTest20TestFunction, dncTest20ValidationFunction)
    dncTestSuite.addTest(dnctest20)

    # Technical Finish

    def dncTest21TestFunction() -> None:
        """Technical Finish
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [TechnicalStep,Jete,Pirouette,Entrechat,Emboite, TechnicalFinish, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.TechnicalFinishBuff in Dummy.buffList, player.TechnicalFinishBuff]

    def dncTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, None]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest21 = test("Techincal Finish test 8", dncTest21TestFunction, dncTest21ValidationFunction)
    dncTestSuite.addTest(dnctest21)

    # Tillana 

    def dncTest21TestFunction() -> None:
        """Tillana
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [ClosedPosition(NINPlayer), Tillana]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.StandardFinishBuff.MultDPS, player.StandardFinishBuff in NINPlayer.buffList]

    def dncTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1.05, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest21 = test("Tillana test 1", dncTest21TestFunction, dncTest21ValidationFunction)
    dncTestSuite.addTest(dnctest21)

    # Combo potency test

    def dncTest22TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [Cascade, Cascade, Fountain]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def dncTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest22 = test("Combo potency test 1", dncTest22TestFunction, dncTest22ValidationFunction)
    dncTestSuite.addTest(dnctest22)

    # Combo potency test

    def dncTest23TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        NINPlayer = Player([], [],Stat, JobEnum.Ninja)

        actionSet = [Fountain]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player, NINPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def dncTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [100]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    dnctest23 = test("Combo potency test 2", dncTest23TestFunction, dncTest23ValidationFunction)
    dncTestSuite.addTest(dnctest23)

    return dncTestSuite

######################################
#           Ninja testSuite          #
######################################

def generateNINTestSuite() -> testSuite:

    ninTestSuite = testSuite("Ninja test suite")

    # Opener requirement, end time and potency test 1

    def ninTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack,
                    AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra,
                    Ten, Chi, Raiton, FleetingRaiju ]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def ninTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 25.21, 11500] 

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest1 = test("Opener requirement, end time and potency 1", ninTest1TestFunction, ninTest1ValidationFunction)
    ninTestSuite.addTest(nintest1)

    # Combo Potency test

    def ninTest2TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SpinningEdge, GustSlash]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [320, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest2 = test("Combo potency and Ninka Generation test 1", ninTest2TestFunction, ninTest2ValidationFunction)
    ninTestSuite.addTest(nintest2)

    # Combo Potency test

    def ninTest3TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SpinningEdge, GustSlash, GustSlash]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest3 = test("Combo potency and Ninka Generation test 2", ninTest3TestFunction, ninTest3ValidationFunction)
    ninTestSuite.addTest(nintest3)

    # Combo Potency test

    def ninTest4TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SpinningEdge, SpinningEdge, GustSlash]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [320, 15]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest4 = test("Combo potency and Ninka Generation test 3", ninTest4TestFunction, ninTest4ValidationFunction)
    ninTestSuite.addTest(nintest4)

    # Combo Potency test

    def ninTest5TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [GustSlash, SpinningEdge, GustSlash]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [320, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest5 = test("Combo potency and Ninka Generation test 4", ninTest5TestFunction, ninTest5ValidationFunction)
    ninTestSuite.addTest(nintest5)

    # Combo Potency test

    def ninTest6TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SpinningEdge, GustSlash, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [440, 25]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest6 = test("Combo potency and Ninka Generation test 5", ninTest6TestFunction, ninTest6ValidationFunction)
    ninTestSuite.addTest(nintest6)

    # Combo Potency test

    def ninTest7TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SpinningEdge, GustSlash, AeolianEdge, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 25]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest7 = test("Combo potency and Ninka Generation test 6", ninTest7TestFunction, ninTest7ValidationFunction)
    ninTestSuite.addTest(nintest7)

    # Combo Potency test

    def ninTest8TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [GustSlash, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge]

    def ninTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest8 = test("Combo potency and Ninka Generation test 7", ninTest8TestFunction, ninTest8ValidationFunction)
    ninTestSuite.addTest(nintest8)

    def ninTest9TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Chi, Ten, Jin, Huton, WaitAbility(40),SpinningEdge, GustSlash, ArmorCrush]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge, round(round(player.HutonTimer,2),2)]

    def ninTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [420, 25, 45.75]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest9 = test("Combo potency and Ninka Generation test 8 - Huton", ninTest9TestFunction, ninTest9ValidationFunction)
    ninTestSuite.addTest(nintest9)

    # Combo Potency test

    def ninTest10TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Chi, Ten, Jin, Huton, WaitAbility(40),SpinningEdge, GustSlash, ArmorCrush, ArmorCrush]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge, round(player.HutonTimer,2)]

    def ninTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 25, 43.63]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest10 = test("Combo potency and Ninka Generation test 9 - Huton", ninTest10TestFunction, ninTest10ValidationFunction)
    ninTestSuite.addTest(nintest10)

    # Combo Potency test

    def ninTest11TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Chi, Ten, Jin, Huton, WaitAbility(40),GustSlash,ArmorCrush]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge, round(player.HutonTimer,2)]

    def ninTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 0,17.87]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest11 = test("Combo potency and Ninka Generation test 10 - Huton", ninTest11TestFunction, ninTest11ValidationFunction)
    ninTestSuite.addTest(nintest11)

    # Combo Potency test

    def ninTest12TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Chi, Ten, Jin, Huton, WaitAbility(40), AeolianEdge, ArmorCrush]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge, round(player.HutonTimer,2)]

    def ninTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 0,17.87]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest12 = test("Combo potency and Ninka Generation test 11 - Huton", ninTest12TestFunction, ninTest12ValidationFunction)
    ninTestSuite.addTest(nintest12)

    # Combo Potency test

    def ninTest13TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Chi, Ten, Jin, Huton, WaitAbility(40), SpinningEdge, GustSlash, AeolianEdge, ArmorCrush]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.NinkiGauge, round(player.HutonTimer,2)]

    def ninTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, 25,13.63]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest13 = test("Combo potency and Ninka Generation test 12 - Huton", ninTest13TestFunction, ninTest13ValidationFunction)
    ninTestSuite.addTest(nintest13)

    # Ninjutsu test

    def ninTest14TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Kassatsu,Ten, Chi, Raiton]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 24617 is damage without Kassatsu
                                # Removing 3405 from total damage that comes from AA. So the remainder is Raiton damage
        return [player.CastingSpell.Potency, player.CastingSpell.DPSBonus, round((player.TotalDamage-3405)/(24617),2)]

    def ninTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [650,1.3, 1.3]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest14 = test("Ninjutsu test 1 - Kassatsu", ninTest14TestFunction, ninTest14ValidationFunction)
    ninTestSuite.addTest(nintest14)

    # Ninjutsu test

    def ninTest15TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Kassatsu,Chi, Ten, HyoshoRanryu]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
                                # Removing 3405 from total damage that comes from AA. So the remainder is Hyosho damage
        return [player.CastingSpell.Potency, player.CastingSpell.DPSBonus, round((player.TotalDamage-3405)/(49234),2)]

    def ninTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1300,1.3, 1.3]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest15 = test("Ninjutsu test 2 - Kassatsu", ninTest15TestFunction, ninTest15ValidationFunction)
    ninTestSuite.addTest(nintest15)

    # Ninjutsu test

    def ninTest16TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Kassatsu]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest16 = test("Ninjutsu test 3 - TenChiJin", ninTest16TestFunction, ninTest16ValidationFunction)
    ninTestSuite.addTest(nintest16)

    # Ninjutsu test

    def ninTest17TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Ten2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [450,5.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest17 = test("Ninjutsu test 4 - TenChiJin", ninTest17TestFunction, ninTest17ValidationFunction)
    ninTestSuite.addTest(nintest17)

    # Ninjutsu test

    def ninTest18TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Chi2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [450,5.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest18 = test("Ninjutsu test 5 - TenChiJin", ninTest18TestFunction, ninTest18ValidationFunction)
    ninTestSuite.addTest(nintest18)

    # Ninjutsu test

    def ninTest19TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Jin2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [450,5.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest19 = test("Ninjutsu test 6 - TenChiJin", ninTest19TestFunction, ninTest19ValidationFunction)
    ninTestSuite.addTest(nintest19)

    # Ninjutsu test

    def ninTest20TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Ten2, Chi2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [650,4.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest20 = test("Ninjutsu test 7 - TenChiJin", ninTest20TestFunction, ninTest20ValidationFunction)
    ninTestSuite.addTest(nintest20)

    # Ninjutsu test

    def ninTest21TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Ten2, Chi2, Jin2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2), player.Suiton]

    def ninTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [500,0, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest21 = test("Ninjutsu test 8 - TenChiJin", ninTest21TestFunction, ninTest21ValidationFunction)
    ninTestSuite.addTest(nintest21)

    # Ninjutsu test

    def ninTest22TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Ten2, Jin2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2)]

    def ninTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [350,4.99]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest22 = test("Ninjutsu test 9 - TenChiJin", ninTest22TestFunction, ninTest22ValidationFunction)
    ninTestSuite.addTest(nintest22)

    # Ninjutsu test

    def ninTest23TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Ten2, Jin2, Chi2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2), player.DotonDOT in player.DOTList]

    def ninTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest23 = test("Ninjutsu test 10 - TenChiJin", ninTest23TestFunction, ninTest23ValidationFunction)
    ninTestSuite.addTest(nintest23)

    # Ninjutsu test

    def ninTest24TestFunction() -> None:
        """Combo potency and ninki gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TenChiJin, Chi2, Jin2, Ten2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.CastingSpell.Potency, round(player.TenChiJinTimer,2), HutonEffect in player.EffectList, player.Haste]

    def ninTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0, True, 15]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest24 = test("Ninjutsu test 11 - TenChiJin", ninTest24TestFunction, ninTest24ValidationFunction)
    ninTestSuite.addTest(nintest24)

    # Mug test

    def ninTest25TestFunction() -> None:
        """Mug test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Mug, SpinningEdge, WaitAbility(10)]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [MugBuff in Dummy.buffList, player.NinkiGauge]

    def ninTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 45]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest25 = test("Mug test 1", ninTest25TestFunction, ninTest25ValidationFunction)
    ninTestSuite.addTest(nintest25)

    # Mug test

    def ninTest26TestFunction() -> None:
        """Mug test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Mug, SpinningEdge, WaitAbility(17.85)]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [MugBuff in Dummy.buffList, player.NinkiGauge]

    def ninTest26ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 45]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest26 = test("Mug test 2", ninTest26TestFunction, ninTest26ValidationFunction)
    ninTestSuite.addTest(nintest26)

    # Mug test

    def ninTest27TestFunction() -> None:
        """Mug test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Mug, SpinningEdge, WaitAbility(20.01)]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [MugBuff in Dummy.buffList, player.NinkiGauge]

    def ninTest27ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 45]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest27 = test("Mug test 3", ninTest27TestFunction, ninTest27ValidationFunction)
    ninTestSuite.addTest(nintest27)

    # Trick attack

    def ninTest28TestFunction() -> None:
        """Trick attack test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ten, Chi, Jin, Suiton, TrickAttack, WaitAbility(13)]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.Suiton, TrickAttackBuff in player.buffList]

    def ninTest28ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest28 = test("Trick Attack test 1", ninTest28TestFunction, ninTest28ValidationFunction)
    ninTestSuite.addTest(nintest28)

    # Trick attack

    def ninTest29TestFunction() -> None:
        """Trick attack test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ten, Chi, Jin, Suiton, TrickAttack, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
                                # The third result is checking if the DPS bonus is in fact being applied. 49234 is damage without Kassatsu (if it was possible)
        return [player.Suiton, TrickAttackBuff in player.buffList]

    def ninTest29ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    nintest29 = test("Trick Attack test 2", ninTest29TestFunction, ninTest29ValidationFunction)
    ninTestSuite.addTest(nintest29)

    return ninTestSuite

######################################
#         Samurai testSuite          #
######################################

def generateSAMTestSuite() -> testSuite:

    samTestSuite = testSuite("Samurai test suite")

    # Opener requirement, end time and potency test 1

    def samTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo, WaitAbility(9), Gekko, Kasha, Ikishoten, Yukikaze, Midare, Senei, KaeshiSetsugekka, Meikyo, Gekko, Shinten, Higanbana, Shinten, OgiNamikiri, Shoha, 
                    KaeshiNamikiri, Kasha, Shinten, Gekko, Gyoten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka, WaitAbility(60)]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def samTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 89.6, 13570]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest1 = test("Opener requirement, end time and potency 1", samTest1TestFunction, samTest1ValidationFunction)
    samTestSuite.addTest(samtest1)

    # Combo potency and gauge test

    def samTest2TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Jinpu]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, FugetsuBuff in player.buffList, player.KenkiGauge]

    def samTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280, True, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest2 = test("Combo potency and gauge test 1", samTest2TestFunction, samTest2ValidationFunction)
    samTestSuite.addTest(samtest2)

    # Combo potency and gauge test

    def samTest3TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Jinpu, WaitAbility(40.01)]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, FugetsuBuff in player.buffList, player.KenkiGauge]

    def samTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest3 = test("Combo potency and gauge test 2", samTest3TestFunction, samTest3ValidationFunction)
    samTestSuite.addTest(samtest3)

    # Combo potency and gauge test

    def samTest4TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Jinpu, Gekko]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.KenkiGauge]

    def samTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380, True, 20]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest4 = test("Combo potency and gauge test 3", samTest4TestFunction, samTest4ValidationFunction)
    samTestSuite.addTest(samtest4)

    # Combo potency and gauge test

    def samTest5TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Jinpu, Hakaze, Gekko]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.KenkiGauge]

    def samTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [170, False, 5]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest5 = test("Combo potency and gauge test 4", samTest5TestFunction, samTest5ValidationFunction)
    samTestSuite.addTest(samtest5)

    # Combo potency and gauge test

    def samTest6TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Gekko, Jinpu]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, FugetsuBuff in player.buffList, player.KenkiGauge]

    def samTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest6 = test("Combo potency and gauge test 5", samTest6TestFunction, samTest6ValidationFunction)
    samTestSuite.addTest(samtest6)

    # Combo potency and gauge test

    def samTest7TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Shifu]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Haste, player.KenkiGauge]

    def samTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280, 13, 10]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest7 = test("Combo potency and gauge test 6", samTest7TestFunction, samTest7ValidationFunction)
    samTestSuite.addTest(samtest7)

    # Combo potency and gauge test

    def samTest8TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Shifu]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Haste, player.KenkiGauge]

    def samTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, 0, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest8 = test("Combo potency and gauge test 7", samTest8TestFunction, samTest8ValidationFunction)
    samTestSuite.addTest(samtest8)

    # Combo potency and gauge test

    def samTest8TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Shifu, Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Ka, player.KenkiGauge, player.Haste]

    def samTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380, True, 20, 13]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest8 = test("Combo potency and gauge test 7", samTest8TestFunction, samTest8ValidationFunction)
    samTestSuite.addTest(samtest8)

    # Combo potency and gauge test

    def samTest9TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Shifu, Kasha, WaitAbility(40)]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Ka, player.KenkiGauge, player.Haste]

    def samTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, True, 20, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest9 = test("Combo potency and gauge test 8", samTest9TestFunction, samTest9ValidationFunction)
    samTestSuite.addTest(samtest9)

    # Combo potency and gauge test

    def samTest10TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Shifu, Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Ka, player.KenkiGauge, player.Haste]

    def samTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [170, False, 0, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest10 = test("Combo potency and gauge test 9", samTest10TestFunction, samTest10ValidationFunction)
    samTestSuite.addTest(samtest10)

    # Combo potency and gauge test

    def samTest11TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Hakaze, Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Setsu, player.KenkiGauge]

    def samTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, True, 20]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest11 = test("Combo potency and gauge test 10", samTest11TestFunction, samTest11ValidationFunction)
    samTestSuite.addTest(samtest11)

    # Combo potency and gauge test

    def samTest12TestFunction() -> None:
        """Combo potency and gauge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Setsu, player.KenkiGauge]

    def samTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, False, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest12 = test("Combo potency and gauge test 11", samTest12TestFunction, samTest12ValidationFunction)
    samTestSuite.addTest(samtest12)

    # Meikyo

    def samTest13TestFunction() -> None:
        """Meikyo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo, Gekko]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.KenkiGauge, FugetsuBuff in player.buffList]

    def samTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380, True, 10, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest13 = test("Meikyo Shisui test 1", samTest13TestFunction, samTest13ValidationFunction)
    samTestSuite.addTest(samtest13)

    # Meikyo

    def samTest14TestFunction() -> None:
        """Meikyo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Ka, player.KenkiGauge, player.Haste]

    def samTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380, True, 20, 13]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest14 = test("Meikyo Shisui test 2", samTest14TestFunction, samTest14ValidationFunction)
    samTestSuite.addTest(samtest14)

    # Meikyo

    def samTest15TestFunction() -> None:
        """Meikyo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Setsu, player.KenkiGauge, player.Haste]

    def samTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, True, 35, 13]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest15 = test("Meikyo Shisui test 3", samTest15TestFunction, samTest15ValidationFunction)
    samTestSuite.addTest(samtest15)

    # Meikyo

    def samTest16TestFunction() -> None:
        """Meikyo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, Yukikaze, WaitAbility(40),Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.KenkiGauge, player.Haste]

    def samTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [170, 35, 0]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest16 = test("Meikyo Shisui test 4", samTest16TestFunction, samTest16ValidationFunction)
    samTestSuite.addTest(samtest16)

    # Iajutsu

    def samTest17TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Higanbana]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.Higanbana in player.DOTList, player.MeditationGauge]

    def samTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [200, False, True,1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest17 = test("Iajutsu test 1", samTest17TestFunction, samTest17ValidationFunction)
    samTestSuite.addTest(samtest17)

    # Iajutsu

    def samTest18TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Higanbana, WaitAbility(60.01)]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.Higanbana in player.DOTList, player.MeditationGauge]

    def samTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False, False,1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest18 = test("Iajutsu test 2", samTest18TestFunction, samTest18ValidationFunction)
    samTestSuite.addTest(samtest18)

    # Iajutsu

    def samTest19TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, TenkaGoken]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.Ka, player.MeditationGauge]

    def samTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, False, False,1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest19 = test("Iajutsu test 3", samTest19TestFunction, samTest19ValidationFunction)
    samTestSuite.addTest(samtest19)

    # Iajutsu

    def samTest20TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, Yukikaze, Midare]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.Ka, player.Setsu, player.MeditationGauge]

    def samTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [640, False, False,False, 1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest20 = test("Iajutsu test 4", samTest20TestFunction, samTest20ValidationFunction)
    samTestSuite.addTest(samtest20)

    # Iajutsu

    def samTest21TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, Yukikaze, Midare, KaeshiSetsugekka]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Getsu, player.Ka, player.Setsu, player.MeditationGauge]

    def samTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [640, False, False,False, 1]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest21 = test("Iajutsu test 5 - Tsubame", samTest21TestFunction, samTest21ValidationFunction)
    samTestSuite.addTest(samtest21)

    # Hagakure

    def samTest22TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Gekko, Kasha, Hagakure, Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.KenkiGauge, player.Ka, player.Setsu, player.Getsu]

    def samTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [55, False, True, False]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest22 = test("Hagakure test 1", samTest22TestFunction, samTest22ValidationFunction)
    samTestSuite.addTest(samtest22)

    # Hagakure

    def samTest23TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meikyo,Hagakure,Gekko, Kasha, Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.KenkiGauge, player.Ka, player.Setsu, player.Getsu]

    def samTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [35, True, True, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest23 = test("Hagakure test 2", samTest23TestFunction, samTest23ValidationFunction)
    samTestSuite.addTest(samtest23)

    # Hagakure

    def samTest24TestFunction() -> None:
        """Iajutsu test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Ikishoten]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.KenkiGauge, player.OgiNamikiriReady]

    def samTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [50, True]   

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    samtest24 = test("Ikishoten test", samTest24TestFunction, samTest24ValidationFunction)
    samTestSuite.addTest(samtest24)

    return samTestSuite

######################################
#          Reaper testSuite          #
######################################

def generateRPRTestSuite() -> testSuite:

    rprTestSuite = testSuite("Reaper test suite")

    # Opener requirement, end time and potency test 1

    def rprTest1TestFunction() -> None:
        """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, PlentifulHarvest, Enshroud, VoidReaping, CrossReaping,LemureSlice, VoidReaping, CrossReaping,
                    LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, HarvestMoon ]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def rprTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 27.2, 9760]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest1 = test("Opener requirement, end time and potency 1", rprTest1TestFunction, rprTest1ValidationFunction)
    rprTestSuite.addTest(rprtest1)

    # Combo Potency and soul gauge generation test

    def rprTest2TestFunction() -> None:
        """Combo Potency and soul gauge generation test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, WaxingSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400, 20]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest2 = test("Combo Potency and soul gauge generation test 1", rprTest2TestFunction, rprTest2ValidationFunction)
    rprTestSuite.addTest(rprtest2)

    # Combo Potency and soul gauge generation test

    def rprTest3TestFunction() -> None:
        """Combo Potency and soul gauge generation test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, WaxingSlice, InfernalSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [500, 30]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest3 = test("Combo Potency and soul gauge generation test 2", rprTest3TestFunction, rprTest3ValidationFunction)
    rprTestSuite.addTest(rprtest3)

    # Combo Potency and soul gauge generation test

    def rprTest4TestFunction() -> None:
        """Combo Potency and soul gauge generation test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [WaxingSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest4 = test("Combo Potency and soul gauge generation test 3", rprTest4TestFunction, rprTest4ValidationFunction)
    rprTestSuite.addTest(rprtest4)

    # Combo Potency and soul gauge generation test

    def rprTest5TestFunction() -> None:
        """Combo Potency and soul gauge generation test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [WaxingSlice, InfernalSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [180,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest5 = test("Combo Potency and soul gauge generation test 4", rprTest5TestFunction, rprTest5ValidationFunction)
    rprTestSuite.addTest(rprtest5)

    # Combo Potency and soul gauge generation test

    def rprTest6TestFunction() -> None:
        """Combo Potency and soul gauge generation test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, InfernalSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [180,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest6 = test("Combo Potency and soul gauge generation test 5", rprTest6TestFunction, rprTest6ValidationFunction)
    rprTestSuite.addTest(rprtest6)

    # SoulSlice test

    def rprTest7TestFunction() -> None:
        """SoulSlice test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, SoulSlice, SoulSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge]

    def rprTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [460,100]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest7 = test("Soulslice test 1", rprTest7TestFunction, rprTest7ValidationFunction)
    rprTestSuite.addTest(rprtest7)

    # Shroud gauge

    def rprTest8TestFunction() -> None:
        """Shroud gauge
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice,SoulSlice, BloodStalk, Gibbet]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [460,10, 10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest8 = test("Shroud Gauge Generation test 1", rprTest8TestFunction, rprTest8ValidationFunction)
    rprTestSuite.addTest(rprtest8)

    # Shroud gauge

    def rprTest9TestFunction() -> None:
        """Shroud gauge
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice,SoulSlice, BloodStalk, Gibbet, SoulSlice, UnveiledGallows, Gallows]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,10, 20]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest9 = test("Shroud Gauge Generation test 2", rprTest9TestFunction, rprTest9ValidationFunction)
    rprTestSuite.addTest(rprtest9)

    # Shroud gauge

    def rprTest10TestFunction() -> None:
        """Shroud gauge
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice,SoulSlice, BloodStalk, Gibbet, SoulSlice, UnveiledGallows, Gallows, WaxingSlice, InfernalSlice, Slice,WaxingSlice, UnveiledGibbet, Gibbet]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,0, 30]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest10 = test("Shroud Gauge Generation test 3", rprTest10TestFunction, rprTest10ValidationFunction)
    rprTestSuite.addTest(rprtest10)

    # Shroud gauge

    def rprTest11TestFunction() -> None:
        """Shroud gauge
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice,SoulSlice, BloodStalk, Gibbet, SoulSlice, UnveiledGallows, Gallows, WaxingSlice, InfernalSlice, Slice,WaxingSlice, UnveiledGibbet, Gibbet,
                    SoulSlice, SoulSlice, UnveiledGallows, Gallows, UnveiledGibbet, Gibbet]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,0, 50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest11 = test("Shroud Gauge Generation test 4", rprTest11TestFunction, rprTest11ValidationFunction)
    rprTestSuite.addTest(rprtest11)

    # Shroud gauge

    def rprTest12TestFunction() -> None:
        """Shroud gauge
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice,SoulSlice, BloodStalk, Gibbet, SoulSlice, UnveiledGallows, Gallows, WaxingSlice, InfernalSlice, Slice,WaxingSlice, UnveiledGibbet, Gibbet,
                    SoulSlice, SoulSlice, UnveiledGallows, Gallows, UnveiledGibbet, Gibbet, Enshroud]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest12 = test("Shroud Gauge Generation test 5", rprTest12TestFunction, rprTest12ValidationFunction)
    rprTestSuite.addTest(rprtest12)

    # Arcane circle

    def rprTest13TestFunction() -> None:
        """Arcane circle
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, ArcaneCircle, WaxingSlice, PlentifulHarvest]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)
        player2 = Player([], [], Stat, JobEnum.Reaper)
        player3 = Player([], [], Stat, JobEnum.Reaper)
        player4 = Player([], [], Stat, JobEnum.Reaper)
        player5 = Player([], [], Stat, JobEnum.Reaper)
        player6 = Player([], [], Stat, JobEnum.Reaper)
        player7 = Player([], [], Stat, JobEnum.Reaper)
        player8 = Player([], [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player, player2, player3, player4, player5, player6, player7, player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [720,20,50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest13 = test("Arcane Circle test 1", rprTest13TestFunction, rprTest13ValidationFunction)
    rprTestSuite.addTest(rprtest13)

    # Arcane circle

    def rprTest14TestFunction() -> None:
        """Arcane circle
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, ArcaneCircle, WaxingSlice, PlentifulHarvest]
        actionSetOther = [Slice, WaxingSlice, Slice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)
        player2 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player3 = Player([], [], Stat, JobEnum.Reaper)
        player4 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player5 = Player([], [], Stat, JobEnum.Reaper)
        player6 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player7 = Player([], [], Stat, JobEnum.Reaper)
        player8 = Player([], [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player, player2, player3, player4, player5, player6, player7, player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [840,20,50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest14 = test("Arcane Circle test 2", rprTest14TestFunction, rprTest14ValidationFunction)
    rprTestSuite.addTest(rprtest14)

    # Arcane circle

    def rprTest15TestFunction() -> None:
        """Arcane circle
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, ArcaneCircle, WaxingSlice, PlentifulHarvest]
        actionSetOther = [Slice, WaxingSlice, Slice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)
        player2 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player3 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player4 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player5 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player6 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player7 = Player(actionSetOther, [], Stat, JobEnum.Reaper)
        player8 = Player(actionSetOther, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player, player2, player3, player4, player5, player6, player7, player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1000,20,50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest15 = test("Arcane Circle test 3", rprTest15TestFunction, rprTest15ValidationFunction)
    rprTestSuite.addTest(rprtest15)

    # Arcane circle

    def rprTest16TestFunction() -> None:
        """Arcane circle
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, ArcaneCircle, WaitAbility(19.95)]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [ArcaneCircleBuff in Dummy.buffList]

    def rprTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest16 = test("Arcane Circle test 4", rprTest16TestFunction, rprTest16ValidationFunction)
    rprTestSuite.addTest(rprtest16)

    # Arcane circle

    def rprTest17TestFunction() -> None:
        """Arcane circle
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Slice, ArcaneCircle, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [ArcaneCircleBuff in Dummy.buffList]

    def rprTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest17 = test("Arcane Circle test 5", rprTest17TestFunction, rprTest17ValidationFunction)
    rprTestSuite.addTest(rprtest17)

    # Gluttony

    def rprTest18TestFunction() -> None:
        """Gluttony test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SoulSlice, Gluttony, Gibbet]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [460,0,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest18 = test("Gluttony test 1", rprTest18TestFunction, rprTest18ValidationFunction)
    rprTestSuite.addTest(rprtest18)

    # Gluttony

    def rprTest19TestFunction() -> None:
        """Gluttony test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SoulSlice, Gluttony, Gibbet, Gallows]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SoulGauge, player.ShroudGauge]

    def rprTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,0,20]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest19 = test("Gluttony test 2", rprTest19TestFunction, rprTest19ValidationFunction)
    rprTestSuite.addTest(rprtest19)

    # Enshroud

    def rprTest20TestFunction() -> None:
        """Enshroud test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Enshroud, VoidReaping]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.LemureGauge, player.VoidShroudGauge]

    def rprTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [460,4,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest20 = test("Enshroud test 1", rprTest20TestFunction, rprTest20ValidationFunction)
    rprTestSuite.addTest(rprtest20)

    # Enshroud

    def rprTest21TestFunction() -> None:
        """Enshroud test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Enshroud, VoidReaping, CrossReaping]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.LemureGauge, player.VoidShroudGauge]

    def rprTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520, 3, 2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest21 = test("Enshroud test 2", rprTest21TestFunction, rprTest21ValidationFunction)
    rprTestSuite.addTest(rprtest21)

    # Enshroud

    def rprTest22TestFunction() -> None:
        """Enshroud test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Enshroud, VoidReaping, CrossReaping, LemureSlice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.LemureGauge, player.VoidShroudGauge]

    def rprTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [240, 3, 0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest22 = test("Enshroud test 3", rprTest22TestFunction, rprTest22ValidationFunction)
    rprTestSuite.addTest(rprtest22)

    # Enshroud

    def rprTest23TestFunction() -> None:
        """Enshroud test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Enshroud, VoidReaping, CrossReaping, LemureSlice, VoidReaping]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.LemureGauge, player.VoidShroudGauge]

    def rprTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520, 2, 1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest23 = test("Enshroud test 4", rprTest23TestFunction, rprTest23ValidationFunction)
    rprTestSuite.addTest(rprtest23)

    # Enshroud

    def rprTest24TestFunction() -> None:
        """Enshroud test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Enshroud, VoidReaping, CrossReaping, LemureSlice, VoidReaping, Communio]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.LemureGauge, player.VoidShroudGauge]

    def rprTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1100, 0,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest24 = test("Enshroud test 5", rprTest24TestFunction, rprTest24ValidationFunction)
    rprTestSuite.addTest(rprtest24)

    # Death design 

    def rprTest25TestFunction() -> None:
        """Death's design
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ShadowOfDeath, WaitAbility(29.98)]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DeathDesignBuff in player.buffList, round(player.DeathDesignTimer,2)]

    def rprTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 0.02]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest25 = test("Death's Design test 1", rprTest25TestFunction, rprTest25ValidationFunction)
    rprTestSuite.addTest(rprtest25)

    # Death design 

    def rprTest26TestFunction() -> None:
        """Death's design
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ShadowOfDeath, WaitAbility(29.98), ShadowOfDeath]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DeathDesignBuff in player.buffList, round(player.DeathDesignTimer,2)]

    def rprTest26ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,30.01]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest26 = test("Death's Design test 2", rprTest26TestFunction, rprTest26ValidationFunction)
    rprTestSuite.addTest(rprtest26)

    # Death design 

    def rprTest27TestFunction() -> None:
        """Death's design
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ShadowOfDeath, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DeathDesignBuff in player.buffList, round(player.DeathDesignTimer,2)]

    def rprTest27ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest27 = test("Death's Design test 3", rprTest27TestFunction, rprTest27ValidationFunction)
    rprTestSuite.addTest(rprtest27)

    # Death design 

    def rprTest28TestFunction() -> None:
        """Death's design
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [ShadowOfDeath, WaitAbility(30.01), ShadowOfDeath, ShadowOfDeath, ShadowOfDeath]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [DeathDesignBuff in player.buffList, round(player.DeathDesignTimer,2)]

    def rprTest28ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,60]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    rprtest28 = test("Death's Design test 4", rprTest28TestFunction, rprTest28ValidationFunction)
    rprTestSuite.addTest(rprtest28)

    return rprTestSuite

######################################
#          Dragoon testSuite         #
######################################

def generateDRGTestSuite() -> testSuite:

    drgTestSuite = testSuite("Dragoon test suite")

    # Opener requirement, end time and potency test 1

    def drgTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, WheelingThrust, Geirskogul, LifeSurge, FangAndClaw, HighJump, RaidenThrust,
                    DragonFireDive, VorpalThrust, LifeSurge, MirageDive, HeavenThrust, SpineshafterDive, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, 
                    WheelingThrust, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def drgTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 82.49, 9420]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest1 = test("Opener requirement, end time and potency 1", drgTest1TestFunction, drgTest1ValidationFunction)
    drgTestSuite.addTest(drgtest1)

    # Combo Potency test

    def drgTest2TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, VorpalThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drgTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest2 = test("Combo potency test 1", drgTest2TestFunction, drgTest2ValidationFunction)
    drgTestSuite.addTest(drgtest2)

    # Combo Potency test

    def drgTest3TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust,TrueThrust, VorpalThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drgTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest3 = test("Combo potency test 2", drgTest3TestFunction, drgTest3ValidationFunction)
    drgTestSuite.addTest(drgtest3)

    # Combo Potency test

    def drgTest4TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust,TrueThrust, VorpalThrust, HeavenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.FangAndClaw]

    def drgTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [480, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest4 = test("Combo potency test 3", drgTest4TestFunction, drgTest4ValidationFunction)
    drgTestSuite.addTest(drgtest4)

    # Combo Potency test

    def drgTest5TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [VorpalThrust, HeavenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.FangAndClaw, player.TotalPotency]

    def drgTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [100, False, 230 + 90]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest5 = test("Combo potency test 4", drgTest5TestFunction, drgTest5ValidationFunction)
    drgTestSuite.addTest(drgtest5)

    # Combo Potency test

    def drgTest6TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust,TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.FangAndClaw, player.WheelInMotion, player.DraconianFire]

    def drgTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, False, True, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest6 = test("Combo potency test 5", drgTest6TestFunction, drgTest6ValidationFunction)
    drgTestSuite.addTest(drgtest6)

    # Combo Potency test

    def drgTest7TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust,TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.FangAndClaw, player.WheelInMotion, player.DraconianFire]

    def drgTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400, False, False, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest7 = test("Combo potency test 6", drgTest7TestFunction, drgTest7ValidationFunction)
    drgTestSuite.addTest(drgtest7)

    # Combo Potency test

    def drgTest8TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList]

    def drgTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [250, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest8 = test("Combo potency test 7", drgTest8TestFunction, drgTest8ValidationFunction)
    drgTestSuite.addTest(drgtest8)

    # Combo Potency test

    def drgTest9TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList]

    def drgTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest9 = test("Combo potency test 8", drgTest9TestFunction, drgTest9ValidationFunction)
    drgTestSuite.addTest(drgtest9)

    # Combo Potency test

    def drgTest10TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, TrueThrust, Disembowel]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList]

    def drgTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [250, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest10 = test("Combo potency test 9", drgTest10TestFunction, drgTest10ValidationFunction)
    drgTestSuite.addTest(drgtest10)

    # Combo Potency test

    def drgTest11TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, ChaoticSpring]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList, player.ChaoticSpringDOT in player.DOTList]

    def drgTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, True, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest11 = test("Combo potency test 10", drgTest11TestFunction, drgTest11ValidationFunction)
    drgTestSuite.addTest(drgtest11)

    # Combo Potency test

    def drgTest12TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, ChaoticSpring, WaitAbility(24.02)]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList, player.ChaoticSpringDOT in player.DOTList, player.WheelInMotion]

    def drgTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, True, False, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest12 = test("Combo potency test 11", drgTest12TestFunction, drgTest12ValidationFunction)
    drgTestSuite.addTest(drgtest12)

    # Combo Potency test

    def drgTest13TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, ChaoticSpring, WheelingThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.WheelInMotion, player.FangAndClaw, player.DraconianFire]

    def drgTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300, False, True, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest13 = test("Combo potency test 12", drgTest13TestFunction, drgTest13ValidationFunction)
    drgTestSuite.addTest(drgtest13)

    # Combo Potency test

    def drgTest14TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.WheelInMotion, player.FangAndClaw, player.DraconianFire]

    def drgTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400, False, False, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest14 = test("Combo potency test 13", drgTest14TestFunction, drgTest14ValidationFunction)
    drgTestSuite.addTest(drgtest14)

    # Combo Potency test

    def drgTest15TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Disembowel]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList]

    def drgTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest15 = test("Combo potency test 14", drgTest15TestFunction, drgTest15ValidationFunction)
    drgTestSuite.addTest(drgtest15)

    # Combo Potency test

    def drgTest16TestFunction() -> None:
        """Combo potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Disembowel, ChaoticSpring]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, PowerSurgeBuff in player.buffList, player.ChaoticSpringDOT in player.DOTList, player.WheelInMotion]

    def drgTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140, False, False, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest16 = test("Combo potency test 15", drgTest16TestFunction, drgTest16ValidationFunction)
    drgTestSuite.addTest(drgtest16)

    # Life surge test

    def drgTest17TestFunction() -> None:
        """Life surge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [LifeSurge]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.NextCrit]

    def drgTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest17 = test("Life Surge test 1", drgTest17TestFunction, drgTest17ValidationFunction)
    drgTestSuite.addTest(drgtest17)

    # Life surge test

    def drgTest18TestFunction() -> None:
        """Life surge test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [LifeSurge, TrueThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.NextCrit]

    def drgTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest18 = test("Life Surge test 2", drgTest18TestFunction, drgTest18ValidationFunction)
    drgTestSuite.addTest(drgtest18)

    # Raiden Thrust

    def drgTest19TestFunction() -> None:
        """Raiden Thrust
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DraconianFire, player.CastingSpell.Potency, player.FirstmindGauge]

    def drgTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 280, 1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest19 = test("Firstmind's Focus test 1", drgTest19TestFunction, drgTest19ValidationFunction)
    drgTestSuite.addTest(drgtest19)

    # Raiden Thrust

    def drgTest20TestFunction() -> None:
        """Raiden Thrust
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DraconianFire, player.CastingSpell.Potency, player.FirstmindGauge]

    def drgTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 280, 1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest20 = test("Firstmind's Focus test 2", drgTest20TestFunction, drgTest20ValidationFunction)
    drgTestSuite.addTest(drgtest20)

    # Raiden Thrust

    def drgTest21TestFunction() -> None:
        """Raiden Thrust
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust,
                    Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DraconianFire, player.CastingSpell.Potency, player.FirstmindGauge]

    def drgTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 280, 2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest21 = test("Firstmind's Focus test 3", drgTest21TestFunction, drgTest21ValidationFunction)
    drgTestSuite.addTest(drgtest21)

    # Raiden Thrust

    def drgTest22TestFunction() -> None:
        """Raiden Thrust
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust,
                    Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DraconianFire, player.CastingSpell.Potency, player.FirstmindGauge, PowerSurgeBuff in player.buffList, player.ChaoticSpringDOT in player.DOTList]

    def drgTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 280, 2, True, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest22 = test("Firstmind's Focus test 4", drgTest22TestFunction, drgTest22ValidationFunction)
    drgTestSuite.addTest(drgtest22)

    # Raiden Thrust

    def drgTest23TestFunction() -> None:
        """Raiden Thrust
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TrueThrust, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust,
                    Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, WyrmwindThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DraconianFire, player.CastingSpell.Potency, player.FirstmindGauge, PowerSurgeBuff in player.buffList, player.ChaoticSpringDOT in player.DOTList]

    def drgTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 420, 0, True, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest23 = test("Firstmind's Focus test 5", drgTest23TestFunction, drgTest23ValidationFunction)
    drgTestSuite.addTest(drgtest23)

    # Life Of the dragon

    def drgTest24TestFunction() -> None:
        """Life of the dragon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HighJump, MirageDive, HighJump, MirageDive]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DragonGauge, player.LifeOfTheDragon]

    def drgTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest24 = test("Life Of the Dragon test 1", drgTest24TestFunction, drgTest24ValidationFunction)
    drgTestSuite.addTest(drgtest24)

    # Life Of the dragon

    def drgTest25TestFunction() -> None:
        """Life of the dragon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HighJump, MirageDive, HighJump, MirageDive, Geirskogul]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DragonGauge, player.LifeOfTheDragon]

    def drgTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest25 = test("Life Of the Dragon test 2", drgTest25TestFunction, drgTest25ValidationFunction)
    drgTestSuite.addTest(drgtest25)

    # Life Of the dragon

    def drgTest26TestFunction() -> None:
        """Life of the dragon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HighJump, MirageDive, HighJump, MirageDive, Geirskogul, WaitAbility(30.02), Geirskogul]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DragonGauge, player.LifeOfTheDragon]

    def drgTest26ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest26 = test("Life Of the Dragon test 3", drgTest26TestFunction, drgTest26ValidationFunction)
    drgTestSuite.addTest(drgtest26)

    # Battle Littany

    def drgTest27TestFunction() -> None:
        """Battle Littany
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BattleLitany, WaitAbility(14.99)]
        ninplayer = Player([], [], Stat, JobEnum.Ninja)
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player,ninplayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, ninplayer.CritRateBonus]

    def drgTest27ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0.1,0.1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest27 = test("Battle Litany test 1", drgTest27TestFunction, drgTest27ValidationFunction)
    drgTestSuite.addTest(drgtest27)

    # Battle Littany

    def drgTest28TestFunction() -> None:
        """Battle Littany
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BattleLitany, WaitAbility(15.02)]
        ninplayer = Player([], [], Stat, JobEnum.Ninja)
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player,ninplayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CritRateBonus, ninplayer.CritRateBonus]

    def drgTest28ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest28 = test("Battle Litany test 2", drgTest28TestFunction, drgTest28ValidationFunction)
    drgTestSuite.addTest(drgtest28)

    # Battle Littany

    def drgTest29TestFunction() -> None:
        """Battle Littany
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        ninplayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [DragonSight(ninplayer), WaitAbility(19.99)]

        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player,ninplayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RightEyeBuff in player.buffList, LeftEyeBuff in ninplayer.buffList]

    def drgTest29ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest29 = test("Dragon Sight test 1", drgTest29TestFunction, drgTest29ValidationFunction)
    drgTestSuite.addTest(drgtest29)

    # Battle Littany

    def drgTest30TestFunction() -> None:
        """Battle Littany
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        ninplayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [DragonSight(ninplayer), WaitAbility(20.02)]

        player = Player(actionSet, [], Stat, JobEnum.Dragoon)
        

        Event.AddPlayer([player,ninplayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RightEyeBuff in player.buffList, LeftEyeBuff in ninplayer.buffList]

    def drgTest30ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drgtest30 = test("Dragon Sight test 2", drgTest30TestFunction, drgTest30ValidationFunction)
    drgTestSuite.addTest(drgtest30)

    return drgTestSuite

######################################
#           Monk testSuite           #
######################################

def generateMNKTestSuite() -> testSuite:

    mnkTestSuite = testSuite("Monk test suite")

    # Opener requirement, end time and potency test 1

    def mnkTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Meditation,FormShift, DragonKick, TwinSnakes, RiddleOfFire, Demolish, TheForbiddenChakra, Bootshine, Brotherhood, PerfectBalance, DragonKick, RiddleOfWind, Bootshine, DragonKick,
                    ElixirField, Bootshine, PerfectBalance, TwinSnakes, DragonKick, Demolish, RisingPhoenix, WaitAbility(30)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        

        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def mnkTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 53.99, 8120]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest1 = test("Opener requirement, end time and potency 1", mnkTest1TestFunction, mnkTest1ValidationFunction)
    mnkTestSuite.addTest(mnktest1)

    # Combo test

    def mnkTest2TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DragonKick,Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.GuaranteedCrit]

    def mnkTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [210, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest2 = test("Combo test 1", mnkTest2TestFunction, mnkTest2ValidationFunction)
    mnkTestSuite.addTest(mnktest2)

    # Combo test

    def mnkTest3TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TrueStrike, SnapPunch, DragonKick, Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.GuaranteedCrit]

    def mnkTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [310, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest3 = test("Combo test 2", mnkTest3TestFunction, mnkTest3ValidationFunction)
    mnkTestSuite.addTest(mnktest3)

    # Combo test

    def mnkTest4TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TwinSnakes]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, DisciplinedFistBuff in player.buffList]

    def mnkTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest4 = test("Combo test 3", mnkTest4TestFunction, mnkTest4ValidationFunction)
    mnkTestSuite.addTest(mnktest4)

    # Combo test

    def mnkTest5TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TwinSnakes, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, DisciplinedFistBuff in player.buffList]

    def mnkTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest5 = test("Combo test 4", mnkTest5TestFunction, mnkTest5ValidationFunction)
    mnkTestSuite.addTest(mnktest5)

    # Combo test

    def mnkTest6TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [TwinSnakes]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, DisciplinedFistBuff in player.buffList]

    def mnkTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [280, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest6 = test("Combo test 5", mnkTest6TestFunction, mnkTest6ValidationFunction)
    mnkTestSuite.addTest(mnktest6)

    # Combo test

    def mnkTest7TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TrueStrike, Demolish]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.DemolishDOT in player.DOTList]

    def mnkTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [130, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest7 = test("Combo test 6", mnkTest7TestFunction, mnkTest7ValidationFunction)
    mnkTestSuite.addTest(mnktest7)

    # Combo test

    def mnkTest8TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TrueStrike, Demolish, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.DemolishDOT in player.DOTList]

    def mnkTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest8 = test("Combo test 7", mnkTest8TestFunction, mnkTest8ValidationFunction)
    mnkTestSuite.addTest(mnktest8)

    # Combo test

    def mnkTest9TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, TrueStrike, DragonKick, Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def mnkTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [210]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest9 = test("Combo test 8", mnkTest9TestFunction, mnkTest9ValidationFunction)
    mnkTestSuite.addTest(mnktest9)

    # Combo test

    def mnkTest10TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, Demolish]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList]

    def mnkTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest10 = test("Combo test 9", mnkTest10TestFunction, mnkTest10ValidationFunction)
    mnkTestSuite.addTest(mnktest10)

    # Combo test

    def mnkTest11TestFunction() -> None:
        """Combo test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, Demolish, TwinSnakes, DragonKick]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList]

    def mnkTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest11 = test("Combo test 10", mnkTest11TestFunction, mnkTest11ValidationFunction)
    mnkTestSuite.addTest(mnktest11)

    # Perfect Balance

    def mnkTest12TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, TwinSnakes, Demolish]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, True,[False, 1,2,3, False]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest12 = test("Perfect Balance test 1", mnkTest12TestFunction, mnkTest12ValidationFunction)
    mnkTestSuite.addTest(mnktest12)

    # Perfect Balance

    def mnkTest13TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, TwinSnakes, Bootshine, Demolish]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, True, True, [False, 1,2,1, False]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest13 = test("Perfect Balance test 2", mnkTest13TestFunction, mnkTest13ValidationFunction)
    mnkTestSuite.addTest(mnktest13)

    # Perfect Balance

    def mnkTest14TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, DragonKick, TrueStrike, Demolish]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False, [False, 1,1,2, False]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest14 = test("Perfect Balance test 3", mnkTest14TestFunction, mnkTest14ValidationFunction)
    mnkTestSuite.addTest(mnktest14)

    # Perfect Balance

    def mnkTest15TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, DragonKick, DragonKick, ElixirField, Demolish, TwinSnakes]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False, [True, 0,0,0, False]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest15 = test("Perfect Balance test 4 - Masterful Blitz", mnkTest15TestFunction, mnkTest15ValidationFunction)
    mnkTestSuite.addTest(mnktest15)

    # Perfect Balance

    def mnkTest16TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, Bootshine, TrueStrike, SnapPunch, RisingPhoenix, TwinSnakes, DragonKick]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, False, True, [False, 0,0,0, True]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest16 = test("Perfect Balance test 5 - Masterful Blitz", mnkTest16TestFunction, mnkTest16ValidationFunction)
    mnkTestSuite.addTest(mnktest16)

    # Perfect Balance

    def mnkTest17TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, TrueStrike, SnapPunch, RisingPhoenix, Demolish, TwinSnakes]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False, [False, 0,0,0, True]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest17 = test("Perfect Balance test 6 - Masterful Blitz", mnkTest17TestFunction, mnkTest17ValidationFunction)
    mnkTestSuite.addTest(mnktest17)

    # Perfect Balance

    def mnkTest18TestFunction() -> None:
        """Perfect Balance
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bootshine, PerfectBalance, DragonKick, TrueStrike, SnapPunch, RisingPhoenix, Demolish, TwinSnakes,
                    Bootshine, PerfectBalance, DragonKick, DragonKick, DragonKick, ElixirField, Demolish, TwinSnakes,
                    PerfectBalance, DragonKick, DragonKick, DragonKick, PhantomRush]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DemolishDOT in player.DOTList, LeadenFistEffect in player.EffectList, DisciplinedFistBuff in player.buffList, player.MasterGauge]

    def mnkTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, True, False, [False, 0,0,0, False]]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest18 = test("Perfect Balance test 7 - Masterful Blitz", mnkTest18TestFunction, mnkTest18ValidationFunction)
    mnkTestSuite.addTest(mnktest18)

    # 	Six-sided Star

    def mnkTest19TestFunction() -> None:
        """	Six-sided Star
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SixSidedStar, Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [round(Event.TimeStamp,2), player.CastingSpell.Potency]

    def mnkTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3.19, 210]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest19 = test("Six-sided Star test 1", mnkTest19TestFunction, mnkTest19ValidationFunction)
    mnkTestSuite.addTest(mnktest19)

    # 	Brotherhood test

    def mnkTest20TestFunction() -> None:
        """	Brotherhood test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Brotherhood, WaitAbility(14.99)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        player2 = Player([], [], Stat, JobEnum.Monk)
        player3 = Player([], [], Stat, JobEnum.Monk)
        player4 = Player([], [], Stat, JobEnum.Monk)
        player5 = Player([], [], Stat, JobEnum.Monk)
        player6 = Player([], [], Stat, JobEnum.Monk)
        player7 = Player([], [], Stat, JobEnum.Monk)
        player8 = Player([], [], Stat, JobEnum.Monk)
        Event.AddPlayer([player,player2,player3,player4,player5,player6,player7,player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [BrotherhoodBuff in player.buffList,BrotherhoodBuff in player2.buffList,BrotherhoodBuff in player3.buffList,BrotherhoodBuff in player4.buffList,BrotherhoodBuff in player5.buffList
                ,BrotherhoodBuff in player6.buffList,BrotherhoodBuff in player7.buffList,BrotherhoodBuff in player8.buffList]

    def mnkTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,True,True,True,True,True,True,True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest20 = test("Brotherhood test 1", mnkTest20TestFunction, mnkTest20ValidationFunction)
    mnkTestSuite.addTest(mnktest20)

    # 	Brotherhood test

    def mnkTest21TestFunction() -> None:
        """	Brotherhood test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Brotherhood, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        player2 = Player([], [], Stat, JobEnum.Monk)
        player3 = Player([], [], Stat, JobEnum.Monk)
        player4 = Player([], [], Stat, JobEnum.Monk)
        player5 = Player([], [], Stat, JobEnum.Monk)
        player6 = Player([], [], Stat, JobEnum.Monk)
        player7 = Player([], [], Stat, JobEnum.Monk)
        player8 = Player([], [], Stat, JobEnum.Monk)
        Event.AddPlayer([player,player2,player3,player4,player5,player6,player7,player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [BrotherhoodBuff in player.buffList,BrotherhoodBuff in player2.buffList,BrotherhoodBuff in player3.buffList,BrotherhoodBuff in player4.buffList,BrotherhoodBuff in player5.buffList
                ,BrotherhoodBuff in player6.buffList,BrotherhoodBuff in player7.buffList,BrotherhoodBuff in player8.buffList]

    def mnkTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False,False,False,False,False,False,False,False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest21 = test("Brotherhood test 2", mnkTest21TestFunction, mnkTest21ValidationFunction)
    mnkTestSuite.addTest(mnktest21)

    # 	Brotherhood test

    def mnkTest22TestFunction() -> None:
        """	Brotherhood test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Brotherhood, Bootshine]
        otherActionSet = [WaitAbility(2), Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        player2 = Player([], [], Stat, JobEnum.Monk)
        player3 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player4 = Player([], [], Stat, JobEnum.Monk)
        player5 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player6 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player7 = Player([], [], Stat, JobEnum.Monk)
        player8 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        Event.AddPlayer([player,player2,player3,player4,player5,player6,player7,player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.MaxChakraGate, round(player.ExpectedChakraGate,2)]

    def mnkTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [5, 1.8]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest22 = test("Brotherhood test 3", mnkTest22TestFunction, mnkTest22ValidationFunction)
    mnkTestSuite.addTest(mnktest22)

    # 	Brotherhood test

    def mnkTest23TestFunction() -> None:
        """	Brotherhood test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Brotherhood, Bootshine, WaitAbility(15.02), Bootshine]
        otherActionSet = [WaitAbility(2), Bootshine, WaitAbility(15.02), Bootshine]
        player = Player(actionSet, [], Stat, JobEnum.Monk)
        player2 = Player([], [], Stat, JobEnum.Monk)
        player3 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player4 = Player([], [], Stat, JobEnum.Monk)
        player5 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player6 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        player7 = Player([], [], Stat, JobEnum.Monk)
        player8 = Player(otherActionSet, [], Stat, JobEnum.Monk)
        Event.AddPlayer([player,player2,player3,player4,player5,player6,player7,player8])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.MaxChakraGate, round(player.ExpectedChakraGate,2)]

    def mnkTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [5, 1.8]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest23 = test("Brotherhood test 4", mnkTest23TestFunction, mnkTest23ValidationFunction)
    mnkTestSuite.addTest(mnktest23)

    # Riddle of Fire 

    def mnkTest24TestFunction() -> None:
        """	Riddle of Fire
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RiddleOfFire]
        player = Player(actionSet, [], Stat, JobEnum.Monk)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RiddleOfFireBuff in player.buffList]

    def mnkTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest24 = test("Riddle of Fire test 1", mnkTest24TestFunction, mnkTest24ValidationFunction)
    mnkTestSuite.addTest(mnktest24)

    # Riddle of Fire 

    def mnkTest25TestFunction() -> None:
        """	Riddle of Fire
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RiddleOfFire, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Monk)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [RiddleOfFireBuff in player.buffList]

    def mnkTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    mnktest25 = test("Riddle of Fire test 2", mnkTest25TestFunction, mnkTest25ValidationFunction)
    mnkTestSuite.addTest(mnktest25)

    return mnkTestSuite

######################################
#          Warrior testSuite         #
######################################

def generateWARTestSuite() -> testSuite:

    warTestSuite = testSuite("Warrior test suite")

    # Opener requirement, end time and potency test 1

    def warTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Tomahawk, Infuriate, HeavySwing, Maim, StormEye, InnerRelease, InnerChaos, Upheaval, Onslaught, PrimalRend, Infuriate, InnerChaos, Onslaught, FellCleave, Onslaught, FellCleave,
                    FellCleave, HeavySwing, Maim, StormPath, FellCleave, Infuriate, InnerChaos]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def warTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 34.99, 8720]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest1 = test("Opener requirement, end time and potency 1", warTest1TestFunction, warTest1ValidationFunction)
    warTestSuite.addTest(wartest1)

    # Combo Potency test

    def warTest2TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest2 = test("Combo Potency test 1", warTest2TestFunction, warTest2ValidationFunction)
    warTestSuite.addTest(wartest2)

    # Combo Potency test

    def warTest3TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim, Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [150,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest3 = test("Combo Potency test 2", warTest3TestFunction, warTest3ValidationFunction)
    warTestSuite.addTest(wartest3)

    # Combo Potency test

    def warTest4TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, HeavySwing,Maim, Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [150,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest4 = test("Combo Potency test 3", warTest4TestFunction, warTest4ValidationFunction)
    warTestSuite.addTest(wartest4)

    # Combo Potency test

    def warTest5TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, HeavySwing,Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest5 = test("Combo Potency test 4", warTest5TestFunction, warTest5ValidationFunction)
    warTestSuite.addTest(wartest4)

    # Combo Potency test

    def warTest6TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim,StormPath]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge, SurgingTempestBuff in player.buffList]

    def warTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [440,30, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest6 = test("Combo Potency test 5", warTest6TestFunction, warTest6ValidationFunction)
    warTestSuite.addTest(wartest6)

    # Combo Potency test

    def warTest7TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Maim,StormPath]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest7 = test("Combo Potency test 6", warTest7TestFunction, warTest7ValidationFunction)
    warTestSuite.addTest(wartest7)

    # Combo Potency test

    def warTest8TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, StormPath]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge, SurgingTempestBuff in player.buffList]

    def warTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest8 = test("Combo Potency test 7", warTest8TestFunction, warTest8ValidationFunction)
    warTestSuite.addTest(wartest8)

    # Combo Potency test

    def warTest9TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim, StormEye]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge, SurgingTempestBuff in player.buffList]

    def warTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [440,20, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest9 = test("Combo Potency test 8", warTest9TestFunction, warTest9ValidationFunction)
    warTestSuite.addTest(wartest9)

    # Combo Potency test

    def warTest10TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim, StormEye, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge, SurgingTempestBuff in player.buffList]

    def warTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,20, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest10 = test("Combo Potency test 9", warTest10TestFunction, warTest10ValidationFunction)
    warTestSuite.addTest(wartest10)

    # Combo Potency test

    def warTest11TestFunction() -> None:
        """Combo Potency test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Maim, StormEye]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge, SurgingTempestBuff in player.buffList]

    def warTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest11 = test("Combo Potency test 10", warTest11TestFunction, warTest11ValidationFunction)
    warTestSuite.addTest(wartest11)

    # Beast Gauge generation/usage

    def warTest12TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim, StormPath,HeavySwing, Maim, StormPath, FellCleave]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest12 = test("Beast Gauge generation/usage test 1", warTest12TestFunction, warTest12ValidationFunction)
    warTestSuite.addTest(wartest12)

    # Beast Gauge generation/usage

    def warTest13TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HeavySwing, Maim, StormPath,HeavySwing, Maim, StormPath, FellCleave, Infuriate, InnerChaos]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [660,10]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest13 = test("Beast Gauge generation/usage test 2", warTest13TestFunction, warTest13ValidationFunction)
    warTestSuite.addTest(wartest13)

    # Beast Gauge generation/usage

    def warTest14TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Infuriate, Infuriate, HeavySwing, Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300,100]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest14 = test("Beast Gauge generation/usage test 3", warTest14TestFunction, warTest14ValidationFunction)
    warTestSuite.addTest(wartest14)

    # Beast Gauge generation/usage

    def warTest15TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Infuriate, Infuriate, HeavySwing, Maim, InnerRelease, FellCleave, FellCleave, FellCleave]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,100]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest15 = test("Beast Gauge generation/usage test 4 - Inner Release", warTest15TestFunction, warTest15ValidationFunction)
    warTestSuite.addTest(wartest15)

    # Beast Gauge generation/usage

    def warTest16TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Infuriate, Infuriate, HeavySwing, Maim, InnerRelease, FellCleave, InnerChaos, FellCleave, FellCleave]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest16 = test("Beast Gauge generation/usage test 5 - Inner Release", warTest16TestFunction, warTest16ValidationFunction)
    warTestSuite.addTest(wartest16)

    # Beast Gauge generation/usage

    def warTest17TestFunction() -> None:
        """Beast Gauge generation/usage
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Infuriate, Infuriate, HeavySwing, Maim, InnerRelease, PrimalRend,FellCleave, InnerChaos, FellCleave, FellCleave]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.BeastGauge]

    def warTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [520,50]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    wartest17 = test("Beast Gauge generation/usage test 6 - Inner Release", warTest17TestFunction, warTest17ValidationFunction)
    warTestSuite.addTest(wartest17)

    return warTestSuite

######################################
#        Gunbreaker testSuite        #
######################################

def generateGNBTestSuite() -> testSuite:

    gnbTestSuite = testSuite("Gunbreaker test suite")

    # Opener requirement, end time and potency test 1

    def gnbTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [LightningShot, KeenEdge, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BlastingZone, BowShock, DoubleDown, RoughDivide, SavageClaw, AbdomenTear,
                    RoughDivide, WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, WaitAbility(50)]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def gnbTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 74.49, 9690]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest1 = test("Opener requirement, end time and potency 1", gnbTest1TestFunction, gnbTest1ValidationFunction)
    gnbTestSuite.addTest(gnbtest1)

    # Combo Potency

    def gnbTest2TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest2 = test("Combo Potency test 1", gnbTest2TestFunction, gnbTest2ValidationFunction)
    gnbTestSuite.addTest(gnbtest2)

    # Combo Potency

    def gnbTest3TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, KeenEdge, BrutalShell]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest3 = test("Combo Potency test 2", gnbTest3TestFunction, gnbTest3ValidationFunction)
    gnbTestSuite.addTest(gnbtest3)

    # Combo Potency

    def gnbTest4TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, BrutalShell]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest4 = test("Combo Potency test 3", gnbTest4TestFunction, gnbTest4ValidationFunction)
    gnbTestSuite.addTest(gnbtest4)

    # Combo Potency

    def gnbTest5TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest5 = test("Combo Potency test 4", gnbTest5TestFunction, gnbTest5ValidationFunction)
    gnbTestSuite.addTest(gnbtest5)

    # Combo Potency

    def gnbTest6TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest6 = test("Combo Potency test 5", gnbTest6TestFunction, gnbTest6ValidationFunction)
    gnbTestSuite.addTest(gnbtest6)

    # Combo Potency

    def gnbTest7TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BrutalShell, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest7 = test("Combo Potency test 6", gnbTest7TestFunction, gnbTest7ValidationFunction)
    gnbTestSuite.addTest(gnbtest7)

    # Combo Potency

    def gnbTest8TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest8 = test("Combo Potency test 7", gnbTest8TestFunction, gnbTest8ValidationFunction)
    gnbTestSuite.addTest(gnbtest8)

    # Combo Potency

    def gnbTest9TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel, KeenEdge,BrutalShell,SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360,2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest9 = test("Combo Potency test 8", gnbTest9TestFunction, gnbTest9ValidationFunction)
    gnbTestSuite.addTest(gnbtest9)

    # Combo Potency

    def gnbTest10TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel, GnashingFang]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [380,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest10 = test("Combo Potency test 9 - Gauge usage/generation", gnbTest10TestFunction, gnbTest10ValidationFunction)
    gnbTestSuite.addTest(gnbtest10)

    # Combo Potency

    def gnbTest11TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel, Bloodfest]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,3]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    # Combo Potency

    def gnbTest12TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [KeenEdge, BrutalShell, SolidBarrel, Bloodfest, GnashingFang, KeenEdge, BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360,3]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest12 = test("Combo Potency test 11 - Gauge usage/generation", gnbTest12TestFunction, gnbTest12ValidationFunction)
    gnbTestSuite.addTest(gnbtest12)

    # Combo Potency

    def gnbTest13TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DemonSlice, DemonSlaughter]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest13 = test("Combo Potency test 12 - Gauge usage/generation", gnbTest13TestFunction, gnbTest13ValidationFunction)
    gnbTestSuite.addTest(gnbtest13)

    # Combo Potency

    def gnbTest14TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DemonSlice, DemonSlaughter,DemonSlice, DemonSlaughter]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [160,2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest14 = test("Combo Potency test 13 - Gauge usage/generation", gnbTest14TestFunction, gnbTest14ValidationFunction)
    gnbTestSuite.addTest(gnbtest14)

    # Combo Potency

    def gnbTest15TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DemonSlice, DemonSlaughter,DemonSlice, DemonSlaughter, DemonSlaughter]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [100,2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest15 = test("Combo Potency test 14 - Gauge usage/generation", gnbTest15TestFunction, gnbTest15ValidationFunction)
    gnbTestSuite.addTest(gnbtest15)

    # Combo Potency

    def gnbTest16TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DemonSlice, DemonSlice,DemonSlaughter, DemonSlaughter]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [100,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest16 = test("Combo Potency test 15 - Gauge usage/generation", gnbTest16TestFunction, gnbTest16ValidationFunction)
    gnbTestSuite.addTest(gnbtest16)

    # Combo Potency

    def gnbTest17TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [DemonSlice, DemonSlaughter,DemonSlice, DemonSlaughter, DoubleDown]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1200,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest17 = test("Combo Potency test 16 - Gauge usage/generation", gnbTest17TestFunction, gnbTest17ValidationFunction)
    gnbTestSuite.addTest(gnbtest17)

    # Combo Potency

    def gnbTest18TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Bloodfest, DoubleDown]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge]

    def gnbTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1200,1]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest18 = test("Combo Potency test 17 - Gauge usage/generation", gnbTest18TestFunction, gnbTest18ValidationFunction)
    gnbTestSuite.addTest(gnbtest18)

    # No Mercy
    def gnbTest19TestFunction() -> None:
        """No Mercy
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [NoMercy, KeenEdge, BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge, NoMercyBuff in player.buffList]

    def gnbTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [360,1, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest19 = test("No Mercy test 1", gnbTest19TestFunction, gnbTest19ValidationFunction)
    gnbTestSuite.addTest(gnbtest19)

    # No Mercy
    def gnbTest20TestFunction() -> None:
        """No Mercy
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [NoMercy,WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.PowderGauge, NoMercyBuff in player.buffList, NoMercyBuff.MultDPS]

    def gnbTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0,0, False,1.2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest20 = test("No Mercy test 2", gnbTest20TestFunction, gnbTest20ValidationFunction)
    gnbTestSuite.addTest(gnbtest20)

    # No Mercy
    def gnbTest21TestFunction() -> None:
        """No Mercy
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BowShock]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BowShockDOT in player.DOTList]

    def gnbTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest21 = test("Bow Shock dot test 1", gnbTest21TestFunction, gnbTest21ValidationFunction)
    gnbTestSuite.addTest(gnbtest21)

    # No Mercy
    def gnbTest22TestFunction() -> None:
        """No Mercy
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BowShock, WaitAbility(15.02)]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BowShockDOT in player.DOTList]

    def gnbTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    gnbtest22 = test("Bow Shock dot test 2", gnbTest22TestFunction, gnbTest22ValidationFunction)
    gnbTestSuite.addTest(gnbtest22)

    return gnbTestSuite

######################################
#          Paladin testSuite         #
######################################

def generatePLDTestSuite() -> testSuite:

    pldTestSuite = testSuite("Paladin test suite")

    # Opener requirement, end time and potency test 1

    def pldTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, 
                    Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, 
                    RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, 
                    Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, 
                    BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def pldTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 87.8, 23780]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest1 = test("Opener requirement, end time and potency 1", pldTest1TestFunction, pldTest1ValidationFunction)
    pldTestSuite.addTest(pldtest1)

    # Combo Potency 

    def pldTest2TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest2 = test("Combo Potency test 1", pldTest2TestFunction, pldTest2ValidationFunction)
    pldTestSuite.addTest(pldtest2)

    # Combo Potency 

    def pldTest3TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, RiotBlade]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest3 = test("Combo Potency test 2", pldTest3TestFunction, pldTest3ValidationFunction)
    pldTestSuite.addTest(pldtest3)

    # Combo Potency 

    def pldTest4TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, FastBlade,RiotBlade, RiotBlade]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest4 = test("Combo Potency test 3", pldTest4TestFunction, pldTest4ValidationFunction)
    pldTestSuite.addTest(pldtest4)

    # Combo Potency 

    def pldTest5TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, FastBlade, RiotBlade]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [300]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest5 = test("Combo Potency test 4", pldTest5TestFunction, pldTest5ValidationFunction)
    pldTestSuite.addTest(pldtest5)

    # Combo Potency 

    def pldTest6TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, RoyalAuthority]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList]

    def pldTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400,3, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest6 = test("Combo Potency test 5", pldTest6TestFunction, pldTest6ValidationFunction)
    pldTestSuite.addTest(pldtest6)

    # Combo Potency 

    def pldTest7TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RiotBlade, RoyalAuthority]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList]

    def pldTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140,0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest7 = test("Combo Potency test 6", pldTest7TestFunction, pldTest7ValidationFunction)
    pldTestSuite.addTest(pldtest7)

    # Combo Potency 

    def pldTest8TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, FastBlade, RiotBlade, RoyalAuthority]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList]

    def pldTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [400,3, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest8 = test("Combo Potency test 7", pldTest8TestFunction, pldTest8ValidationFunction)
    pldTestSuite.addTest(pldtest8)

    # Combo Potency 

    def pldTest9TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, FastBlade, RiotBlade, RoyalAuthority, Atonement,RoyalAuthority]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList]

    def pldTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [140,2, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest9 = test("Combo Potency test 8", pldTest9TestFunction, pldTest9ValidationFunction)
    pldTestSuite.addTest(pldtest9)

    # Combo Potency 

    def pldTest10TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, FastBlade, RiotBlade, RoyalAuthority, Atonement,RoyalAuthority, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList, player.CastingSpell.CastTime]

    def pldTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [450,2, False, 0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest10 = test("Combo Potency test 9", pldTest10TestFunction, pldTest10ValidationFunction)
    pldTestSuite.addTest(pldtest10)

    # Combo Potency 

    def pldTest11TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, FastBlade, RiotBlade, RoyalAuthority, Atonement,RoyalAuthority, HolySpirit, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.SwordOathStack, DivineMightEffect in player.EffectList, player.CastingSpell.CastTime]

    def pldTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [350,2, False, 1.5]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest11 = test("Combo Potency test 10", pldTest11TestFunction, pldTest11ValidationFunction)
    pldTestSuite.addTest(pldtest11)

    # Requiescat

    def pldTest12TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.CastingSpell.CastTime]

    def pldTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [650,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest12 = test("Requiescat test 1", pldTest12TestFunction, pldTest12ValidationFunction)
    pldTestSuite.addTest(pldtest12)

    # Requiescat

    def pldTest13TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, HolySpirit, HolySpirit, HolySpirit, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.CastingSpell.CastTime]

    def pldTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [650,0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest13 = test("Requiescat test 2", pldTest13TestFunction, pldTest13ValidationFunction)
    pldTestSuite.addTest(pldtest13)

    # Requiescat

    def pldTest14TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, HolySpirit, HolySpirit, HolySpirit, HolySpirit, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.CastingSpell.CastTime]

    def pldTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [350,1.5]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest14 = test("Requiescat test 3", pldTest14TestFunction, pldTest14ValidationFunction)
    pldTestSuite.addTest(pldtest14)

    # Requiescat

    def pldTest15TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, HolySpirit, HolySpirit, HolySpirit, HolySpirit, HolySpirit, Confetti]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [420]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest15 = test("Requiescat test 4", pldTest15TestFunction, pldTest15ValidationFunction)
    pldTestSuite.addTest(pldtest15)

    # Requiescat

    def pldTest16TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [920]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest16 = test("Requiescat test 5", pldTest16TestFunction, pldTest16ValidationFunction)
    pldTestSuite.addTest(pldtest16)

    # Requiescat

    def pldTest17TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [720]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest17 = test("Requiescat test 6", pldTest17TestFunction, pldTest17ValidationFunction)
    pldTestSuite.addTest(pldtest17)

    # Requiescat

    def pldTest18TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, HolySpirit, HolySpirit, HolySpirit, BladeFaith]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [220]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest18 = test("Requiescat test 7", pldTest18TestFunction, pldTest18ValidationFunction)
    pldTestSuite.addTest(pldtest18)

    # Requiescat

    def pldTest19TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith, BladeTruth]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [820]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest19 = test("Requiescat test 8", pldTest19TestFunction, pldTest19ValidationFunction)
    pldTestSuite.addTest(pldtest19)

    # Requiescat

    def pldTest20TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith, HolySpirit, HolySpirit,BladeTruth]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [320]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest20 = test("Requiescat test 9", pldTest20TestFunction, pldTest20ValidationFunction)
    pldTestSuite.addTest(pldtest20)

    # Requiescat

    def pldTest21TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith,BladeTruth, BladeValor]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [920]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest21 = test("Requiescat test 10", pldTest21TestFunction, pldTest21ValidationFunction)
    pldTestSuite.addTest(pldtest21)

    # Requiescat

    def pldTest22TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith,BladeTruth, HolySpirit, BladeValor]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [420]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest22 = test("Requiescat test 11", pldTest22TestFunction, pldTest22ValidationFunction)
    pldTestSuite.addTest(pldtest22)

    # Requiescat

    def pldTest23TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [RequestACat, Confetti, BladeFaith,BladeTruth, BladeValor, HolySpirit]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest23ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [350]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest23 = test("Requiescat test 12", pldTest23TestFunction, pldTest23ValidationFunction)
    pldTestSuite.addTest(pldtest23)

    # Requiescat

    def pldTest24TestFunction() -> None:
        """Requiescat
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FastBlade, RiotBlade, RoyalAuthority,RequestACat, Confetti, BladeFaith, HolySpirit,BladeTruth, BladeValor]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def pldTest24ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [920]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest24 = test("Requiescat test 13", pldTest24TestFunction, pldTest24ValidationFunction)
    pldTestSuite.addTest(pldtest24)

    # Fight or Flight

    def pldTest25TestFunction() -> None:
        """Fight or Flight
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FightOrFlight]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [FightOrFlightBuff in player.buffList, FightOrFlightBuff.MultDPS]

    def pldTest25ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True, 1.25]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest25 = test("Fight or Flight test 1", pldTest25TestFunction, pldTest25ValidationFunction)
    pldTestSuite.addTest(pldtest25)

    # Fight or Flight

    def pldTest26TestFunction() -> None:
        """Fight or Flight
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [FightOrFlight, WaitAbility(20.02)]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [FightOrFlightBuff in player.buffList, FightOrFlightBuff.MultDPS]

    def pldTest26ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False, 1.25]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    pldtest26 = test("Fight or Flight test 2", pldTest26TestFunction, pldTest26ValidationFunction)
    pldTestSuite.addTest(pldtest26)

    return pldTestSuite

######################################
#        DarkKnight testSuite        #
######################################

def generateDRKTestSuite() -> testSuite:

    drkTestSuite = testSuite("Dark Knight test suite")

    # Opener requirement, end time and potency test 1

    def drkTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BloodWeapon, WaitAbility(4), HardSlash, EdgeShadow, Delirium, SyphonStrike, Souleater, LivingShadow, SaltedEarth, HardSlash, Shadowbringer, EdgeShadow, Bloodspiller,
                    CarveSpit, Plunge, Bloodspiller, Shadowbringer, EdgeShadow, Bloodspiller, SaltDarkness, EdgeShadow, SyphonStrike ,Plunge, EdgeShadow]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        failedReq = 0
        for event in Event.failedRequirementList: # Counts all fatal requirement failed. Must be 0 for test to pass
            if event.fatal : failedReq += 1

        return [failedReq, Event.TimeStamp, player.TotalPotency]

    def drkTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 22.56, 10730]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest1 = test("Opener requirement, end time and potency 1", drkTest1TestFunction, drkTest1ValidationFunction)
    drkTestSuite.addTest(drktest1)

    # Combo Potency

    def drkTest2TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash, SyphonStrike]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drkTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [260]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest2 = test("Combo Potency test 1", drkTest2TestFunction, drkTest2ValidationFunction)
    drkTestSuite.addTest(drktest2)

    # Combo Potency

    def drkTest3TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,HardSlash, SyphonStrike]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drkTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [260]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest3 = test("Combo Potency test 2", drkTest3TestFunction, drkTest3ValidationFunction)
    drkTestSuite.addTest(drktest3)

    # Combo Potency

    def drkTest4TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,HardSlash, SyphonStrike, SyphonStrike]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drkTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest4 = test("Combo Potency test 3", drkTest4TestFunction, drkTest4ValidationFunction)
    drkTestSuite.addTest(drktest4)

    # Combo Potency

    def drkTest5TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,SyphonStrike, HardSlash, SyphonStrike]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency]

    def drkTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [260]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest5 = test("Combo Potency test 4", drkTest5TestFunction, drkTest5ValidationFunction)
    drkTestSuite.addTest(drktest5)

    # Combo Potency

    def drkTest6TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,SyphonStrike, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [340, 20]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest6 = test("Combo Potency test 5", drkTest6TestFunction, drkTest6ValidationFunction)
    drkTestSuite.addTest(drktest6)

    # Combo Potency

    def drkTest7TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,SyphonStrike, Souleater, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, 20]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest7 = test("Combo Potency test 6", drkTest7TestFunction, drkTest7ValidationFunction)
    drkTestSuite.addTest(drktest7)

    # Combo Potency

    def drkTest8TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash,SyphonStrike, Souleater,HardSlash,SyphonStrike, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [340, 40]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest8 = test("Combo Potency test 7", drkTest8TestFunction, drkTest8ValidationFunction)
    drkTestSuite.addTest(drktest8)

    # Combo Potency

    def drkTest9TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, 0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest9 = test("Combo Potency test 8", drkTest9TestFunction, drkTest9ValidationFunction)
    drkTestSuite.addTest(drktest9)

    # Combo Potency

    def drkTest10TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, 0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest10 = test("Combo Potency test 9", drkTest10TestFunction, drkTest10ValidationFunction)
    drkTestSuite.addTest(drktest10)

    # Combo Potency

    def drkTest11TestFunction() -> None:
        """Combo Potency
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [SyphonStrike, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.Potency, player.Blood]

    def drkTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [120, 0]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest11 = test("Combo Potency test 10", drkTest11TestFunction, drkTest11ValidationFunction)
    drkTestSuite.addTest(drktest11)

    # Darkside test

    def drkTest12TestFunction() -> None:
        """Darkside test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [EdgeShadow]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [EdgeShadowBuff in player.buffList]

    def drkTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest12 = test("Darkside test 1", drkTest12TestFunction, drkTest12ValidationFunction)
    drkTestSuite.addTest(drktest12)

    # Darkside test

    def drkTest12TestFunction() -> None:
        """Darkside test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [EdgeShadow, WaitAbility(30.02)]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [EdgeShadowBuff in player.buffList]

    def drkTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest12 = test("Darkside test 2", drkTest12TestFunction, drkTest12ValidationFunction)
    drkTestSuite.addTest(drktest12)

    # Darkside test

    def drkTest12TestFunction() -> None:
        """Darkside test
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [EdgeShadow, EdgeShadow]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [EdgeShadowBuff in player.buffList, round(player.DarksideTimer,2)]

    def drkTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [True,59.99]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest12 = test("Darkside test 3", drkTest12TestFunction, drkTest12ValidationFunction)
    drkTestSuite.addTest(drktest12)

    # Delirium

    def drkTest13TestFunction() -> None:
        """Delirium
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash, SyphonStrike, Souleater,EdgeShadow, EdgeShadow, Delirium, Bloodspiller]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana, player.Blood, player.DeliriumStacks]

    def drkTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [4200, 20,2]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest13 = test("Delirium test 1", drkTest13TestFunction, drkTest13ValidationFunction)
    drkTestSuite.addTest(drktest13)

    # Delirium

    def drkTest14TestFunction() -> None:
        """Delirium
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HardSlash, SyphonStrike, Souleater,EdgeShadow, EdgeShadow, Delirium, Bloodspiller, Quietus, Bloodspiller, Bloodspiller]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Mana, player.Blood, player.DeliriumStacks, DeliriumEffect in player.EffectList]

    def drkTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [5500, -30,0, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest14 = test("Delirium test 2", drkTest14TestFunction, drkTest14ValidationFunction)
    drkTestSuite.addTest(drktest14)

    # Blood weapon

    def drkTest15TestFunction() -> None:
        """Blood weapon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BloodWeapon, HardSlash, SyphonStrike]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BloodWeaponStacks, player.Blood,BloodWeaponEffect in player.EffectList]

    def drkTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [3, 20, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest15 = test("Bloodweapon test 1", drkTest15TestFunction, drkTest15ValidationFunction)
    drkTestSuite.addTest(drktest15)

    # Blood weapon

    def drkTest16TestFunction() -> None:
        """Blood weapon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BloodWeapon, HardSlash, SyphonStrike, Souleater, Bloodspiller]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BloodWeaponStacks, player.Blood,BloodWeaponEffect in player.EffectList]

    def drkTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [1, 10, True]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest16 = test("Bloodweapon test 2", drkTest16TestFunction, drkTest16ValidationFunction)
    drkTestSuite.addTest(drktest16)

    # Blood weapon

    def drkTest17TestFunction() -> None:
        """Blood weapon
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [BloodWeapon, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)
        
        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BloodWeaponStacks, player.Blood,BloodWeaponEffect in player.EffectList]

    def drkTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [0, 40, False]

        for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

        return passed , expected

    drktest17 = test("Bloodweapon test 3", drkTest17TestFunction, drkTest17ValidationFunction)
    drkTestSuite.addTest(drktest17)

    return drkTestSuite


######################################
#           DOT testSuite            #
######################################

# The DOT testSuite is a randomly generated test suite. We take all party buffs in the game
# and randomly put them before or after the DOT is applied. Every DOT has 7 tests in total.
# Test 1-6 are the same, only there is an increasing amount of buffs before the dot is applied
# and test 7 is test 6 (so all buffs are applied before DOT) and we reapply the DOT.
# The seed is given in order to redo the test in a controlled environment if needed.

def generateDOTTestSuite(setSeed : int = 0) -> testSuite:
                             # Generating random seed
                             # used for the DOT test
    randomSeed = randint(1,999999) if setSeed == 0 else setSeed
    seed(randomSeed)
    dotTestSuite = testSuite("DOT test suite - Seed : " + str(randomSeed))

    # Dot
    # Buff should clip on a dot once it is applied. These test will make sure that this is
    # happening without issues.

    DRGBuff = DragonSight(Player([],[],base_stat, JobEnum.BlackMage))

    buffLookup = {
        SearingLight : SearingLightbuff,
        Embolden : EmboldenBuff,
        Divination : DivinationBuff,
        Mug : MugBuff,
        ArcaneCircle : ArcaneCircleBuff,
        Brotherhood : BrotherhoodBuff,
        ChainStratagem : hitBuff(0.10),
        BattleVoice : hitBuff(0.20, isCrit=False),
        BattleLitany : hitBuff(0.10),
        ArmyPaeon : hitBuff(0.03, isCrit=False),
        MageBallad : MageBalladBuff,
        WanderingMinuet : hitBuff(0.02),
        TechnicalFinish : buff(1.05, "TF"),
        StandardFinish : buff(1.05, "SF"),
        DRGBuff : LeftEyeBuff,
        Potion : None
    }
    buffJobLookup = {
        SearingLight : JobEnum.Summoner,
        Embolden : JobEnum.RedMage,
        Divination : JobEnum.Astrologian,
        Mug : JobEnum.Ninja,
        ArcaneCircle : JobEnum.Reaper,
        Brotherhood : JobEnum.Monk,
        ChainStratagem : JobEnum.Scholar,
        BattleVoice : JobEnum.Bard,
        BattleLitany : JobEnum.Dragoon,
        ArmyPaeon : JobEnum.Bard,
        MageBallad : JobEnum.Bard,
        WanderingMinuet : JobEnum.Bard
    }

    def generateDOTSnapshotTest(buffToApply, buffBeforeDOT : int, buffAfterDOT : int, dotAction, dotPlayerJob,isGround):
        """This function generates random dot clipping test. It is given a seed for reproducibility.
        buffToApply : list(Action) -> List of actions that gives buff to execute in this test
        buffBeforeDOT : int -> Number of buffs to apply before DOT
        buffAFterDOT : int -> Number of buffs to apply after DOT
        """
        indexListBeforeDOT = sample(range(0,len(buffToApply)), buffBeforeDOT)

        buffListBeforeDOT = []
        buffListAfterDOT = []

        expectedSnapshotList = []
        expectedDHBuff = 0
        expectedCritBuff = 0
        snapshotPotion = False

        for i in range(len(buffToApply)):
            if i in indexListBeforeDOT : buffListBeforeDOT.append(buffToApply[i])
            else : buffListAfterDOT.append(buffToApply[i])

        Dummy = Enemy()
        Event = Fight(Dummy, False)

                                # Matching Job type since some jobs require
                                # combo for DOT
        match dotPlayerJob:
            case JobEnum.Monk:
                dotPlayer = Player([WaitAbility(5),Bootshine, TrueStrike, Demolish,WaitAbility(0.1)], [], base_stat, dotPlayerJob)
            case JobEnum.Dragoon:
                dotPlayer = Player([WaitAbility(5),TrueThrust, Disembowel, ChaoticSpring,WaitAbility(0.1)], [], base_stat, dotPlayerJob)
                                # Appending Power Surge which is gained in disembowel
                expectedSnapshotList.append(PowerSurgeBuff)
            case _ :
                dotPlayer = Player([WaitAbility(7), dotAction, WaitAbility(0.1)], [], base_stat, dotPlayerJob)
        Event.AddPlayer([dotPlayer])

                                # If potion is before DOT insert at start of action set.
                                # If after append at the end.
        if Potion in buffListBeforeDOT: 
            dotPlayer.ActionSet.insert(0, Potion)
            snapshotPotion = True
        else : dotPlayer.ActionSet.append(Potion)

        for action in buffListBeforeDOT:
                                # If potion skip since was treated earlier
            if action == Potion : continue
                                # If isGround = True and action is debuff we don't clip.
            if isGround:
                match action.id:
                    case Mug.id | ChainStratagem.id:
                        continue

            match action.id:
                case Devilment.id:
                    newPlayer = Player([ClosedPosition(dotPlayer), Devilment], [], base_stat,JobEnum.Dancer)
                    Event.AddPlayer([newPlayer])
                    expectedCritBuff += 0.2
                    expectedDHBuff += 0.2
                    continue
                case TechnicalFinish.id:
                    newPlayer = Player([TechnicalStep, Pirouette, Entrechat, Jete, Emboite, TechnicalFinish], [], base_stat,JobEnum.Dancer)
                case StandardFinish.id:
                    newPlayer = Player([ClosedPosition(dotPlayer), StandardStep, Jete, Pirouette, StandardFinish], [], base_stat,JobEnum.Dancer)
                case 7398 : # DragonSight
                    newPlayer = Player([DragonSight(dotPlayer)], [], base_stat,JobEnum.Dragoon)
                case _ :
                    newPlayer = Player([action], [], base_stat,buffJobLookup[action])

            if isinstance(buffLookup[action], hitBuff):
                if buffLookup[action].isCrit : expectedCritBuff += buffLookup[action].buff
                else : expectedDHBuff += buffLookup[action].buff
            else : expectedSnapshotList.append(buffLookup[action])
            Event.AddPlayer([newPlayer])

        for action in buffListAfterDOT:
                                # If potion skip since was treated earlier
            if action == Potion : continue
            match action.id:
                case Devilment.id:
                    newPlayer = Player([ClosedPosition(dotPlayer), WaitAbility(12),Devilment], [], base_stat,JobEnum.Dancer)
                case TechnicalFinish.id:
                    newPlayer = Player([WaitAbility(12),TechnicalStep, Pirouette, Entrechat, Jete, Emboite, TechnicalFinish], [], base_stat,JobEnum.Dancer)
                case StandardFinish.id:
                    newPlayer = Player([ClosedPosition(dotPlayer),WaitAbility(12), StandardStep, Jete, Pirouette, StandardFinish], [], base_stat,JobEnum.Dancer)
                case 7398 : # DragonSight
                    newPlayer = Player([WaitAbility(12),DragonSight(dotPlayer)], [], base_stat,JobEnum.Dragoon)
                case _ :
                    newPlayer = Player([WaitAbility(12),action], [], base_stat,buffJobLookup[action])
            Event.AddPlayer([newPlayer])

                                # Sorting by name
        expectedSnapshotList.sort(key=lambda x : x.name)

        return Event, [round(expectedDHBuff,2), round(expectedCritBuff,2),expectedSnapshotList, snapshotPotion], dotPlayer

    def generateDOTTicCountTest(dotDuration : int, dotAction, job : int, dotFieldName : str, resetAfter : float = 0):
        """Generates two functions (test and validate) for tests that count the number of DOT tic.

        Args:
            dotDuration (int): base duration of the dot
            dotAction (Spell): Spell object of the dot
            job (JobEnum): Job Enum of the player doing the dot
            dotFieldName (str): Name of the field in the player's object that contains the DOT object.\
            resetAfter (float) : amount of time to wait until reapplying DOT. If 0 does not reapply.
                                This value should be bigger than 7.5 or 0 in order to avoid any issues
                                with reapplying DOTs that require combo.
        """
        def ticTestFunction():

            Event = Fight(Enemy(), False)
            player = Player([],[], base_stat, job)

            if resetAfter > 0 :
                match job:
                    case JobEnum.Dragoon:
                        player.ActionSet += [TrueThrust, Disembowel, ChaoticSpring,WaitAbility(resetAfter - 5),TrueThrust, Disembowel, ChaoticSpring, WaitAbility(dotDuration + 5)]
                    case JobEnum.Monk:
                        player.ActionSet += [Bootshine, TrueStrike, Demolish,WaitAbility(resetAfter - 4),Bootshine, TrueStrike, Demolish, WaitAbility(dotDuration + 5)]
                    case JobEnum.Samurai:
                        player.ActionSet += [Higanbana,WaitAbility(resetAfter - 1.3),Higanbana, WaitAbility(dotDuration + 5)]
                    case _:
                        match player.RoleEnum:
                            case RoleEnum.Caster:
                                    # Adding swiftcast for isntant DOT cast for SMN/BLM
                                player.ActionSet += [dotAction, WaitAbility(resetAfter),Swiftcast, dotAction,WaitAbility(dotDuration + 5)]
                            case _:
                                player.ActionSet += [dotAction, WaitAbility(resetAfter), dotAction,WaitAbility(dotDuration + 5)]
            else:
                match job:
                    case JobEnum.Dragoon:
                        player.ActionSet += [TrueThrust, Disembowel, ChaoticSpring,WaitAbility(dotDuration + 5)]
                    case JobEnum.Monk:
                        player.ActionSet += [Bootshine, TrueStrike, Demolish,WaitAbility(dotDuration + 5)]
                    case _:
                        player.ActionSet += [dotAction,WaitAbility(dotDuration + 5)]
            
            Event.AddPlayer([player])

            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

                                # This list will receive the DOT object given to the player
            dotPointerList = []

            def getData(Fight):
                """This function is set as the ExtractInfo of the fight. Once it detects
                the DOT is not None, it appends it to the dotPointerList. This lets us keep a reference on it
                even when it gets set to none after the DOT expiration. We can then check the number of tic.
                In order to only append once, we set the ExtractInfo function to "nothing" once we pass once.
                """
                def nothing(Fight):
                    pass
                if Fight.PlayerList[0].__dict__[dotFieldName] != None:
                    dotPointerList.append(Fight.PlayerList[0].__dict__[dotFieldName])
                    Fight.ExtractInfo = nothing

            Event.ExtractInfo = getData

            Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

            return dotPointerList[0].ticAmount
        
        def ticValidFunction(testTic):
            passed = True
            expectedTic = (dotDuration+resetAfter)//3
                                # Adding 1 since we get 1 free TIC at each time we add the DOT.
                                # Since the DOT tic is kind of random (looking at logs)
                                # I made it clip asap. This results in 1 more DOT tic
                                # here (note that this CAN happen in game).
            expectedTic = expectedTic + 1 if resetAfter > 0 else expectedTic
            passed = expectedTic == testTic

            return passed, expectedTic
        
        return ticTestFunction,ticValidFunction

    def generateWholeDOTTest(testName, beforeDot : int, afterDot : int, DoTAction, playerDOTEnum, dotFieldName, isGround=False):
        """Generates test object
        """      
                                # Generating fight with random buff snapshotting
        Event, expected, player = generateDOTSnapshotTest([SearingLight, Embolden, Divination, Mug, ArcaneCircle, Brotherhood, ChainStratagem, 
                                                        BattleVoice, BattleLitany, ArmyPaeon, MageBallad, WanderingMinuet, TechnicalFinish, StandardFinish, Devilment, DRGBuff, Potion], 
                                                        beforeDot, afterDot, DoTAction, playerDOTEnum,isGround)

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True
                                # Sort key used to sort buffSnapshot by name
        sortKey = lambda x : x.name

        def testFunction() -> None:
            Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

            dotObj = player.__dict__[dotFieldName]
            buffList = dotObj.MultBonus
            dhBuff = dotObj.DHBonus
            critBuff = dotObj.CritBonus
            snapshotPotion = dotObj.potSnapshot

            buffList.sort(key=sortKey)

            return [round(dhBuff,2), round(critBuff,2), buffList, snapshotPotion]

        def validFunction(testResult) -> (bool,list):
            passed = True

            for i in range(len(expected[2])):
                if i == len(expected[2]) or i == len(testResult[2]):
                    passed = False 
                    break
                passed = passed and testResult[2][i].isEqual(expected[2][i])

            passed = passed and testResult[0] == expected[0] and testResult[1] == expected[1] and testResult[3] == expected[3]

            return passed, expected

        return test(testName, testFunction, validFunction)

    jobList = [JobEnum.BlackMage,JobEnum.BlackMage,JobEnum.Scholar, JobEnum.Astrologian,JobEnum.WhiteMage,JobEnum.Sage,JobEnum.Bard,JobEnum.Bard, JobEnum.Dragoon, JobEnum.Monk, JobEnum.Samurai, JobEnum.Gunbreaker, JobEnum.Gunbreaker, JobEnum.Summoner, JobEnum.DarkKnight, JobEnum.Ninja]
    dotList = [Thunder3, Thunder4, Biolysis, Combust, Dia, EukrasianDosis, Causticbite, Stormbite, ChaoticSpring, Demolish, Higanbana, BowShock, SonicBreak, Slipstream, SaltedEarth, Doton]
    fieldList = ["Thunder3DOT", "Thunder4DOT", "Biolysis", "CumbustDOT", "Dia", "Eukrasian", "CausticbiteDOT", "StormbiteDOT", "ChaoticSpringDOT", "DemolishDOT", "Higanbana", "BowShockDOT", "SonicBreakDOT", "SlipstreamDOT", "SaltedEarthDOT", "DotonDOT"]
    isGroundList = [False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True]
    dotDurationList = [30, 18, 30, 30, 30, 30, 45, 45, 24, 18, 60, 15, 30, 15, 15, 18]

    for i in range(len(jobList)):
        
        for j in range(0,17,3):
            dotTestSuite.addTest(generateWholeDOTTest(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test " + str(int(j/3)+1) + " (buff Snapshot)", j if j != 15 else 17, (17-j) if j != 15 else 0, 
                                                    dotList[i],jobList[i], fieldList[i], isGround=isGroundList[i]))
            
                                # Adding an additional test that has all buffs before DOT and dot is reapplied.
                                # Some buffs will clip again but we are expecting to loose everything
                                # since we look right away. In other words the buff snapshot hasn't happened
                                # yet.
        def addTestFunction():
            Event, expected, player = generateDOTSnapshotTest([SearingLight, Embolden, Divination, Mug, ArcaneCircle, Brotherhood, ChainStratagem, 
                                                            BattleVoice, BattleLitany, ArmyPaeon, MageBallad, WanderingMinuet, TechnicalFinish, StandardFinish, Devilment, DRGBuff, Potion], 
                                                            17, 0, dotList[i],jobList[i],isGround=isGroundList[i])
            match jobList[i]:
                case JobEnum.Dragoon:
                    player.ActionSet += [TrueThrust, Disembowel, ChaoticSpring]
                case JobEnum.Monk:
                    player.ActionSet += [Bootshine, TrueStrike, Demolish]
                case _:
                    player.ActionSet += [WaitAbility(2),dotList[i]]
            
            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

            Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

            dotObj = player.__dict__[fieldList[i]]
            buffList = dotObj.MultBonus
            dhBuff = dotObj.DHBonus
            critBuff = dotObj.CritBonus
            snapshotPotion = dotObj.potSnapshot

            return [round(dhBuff,2), round(critBuff,2), buffList, snapshotPotion]

        def addValidFunction(testResult):
            passed = True
            expected = [0,0,[], False]

            for i in range(len(expected)) : passed = passed and (expected[i] == testResult[i])

            return passed, expected
        
        dotTestSuite.addTest(test(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test 7 (Reapplying DOT)", addTestFunction, addValidFunction))

                                # Adding additional tet that check for the total number of tic

        tF, vF = generateDOTTicCountTest(dotDurationList[i], dotList[i], jobList[i], fieldList[i])
        dotTestSuite.addTest(test(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test 8 (Counting tic)", tF, vF))
        tF2, vF2 = generateDOTTicCountTest(dotDurationList[i], dotList[i], jobList[i], fieldList[i], resetAfter=7.5) # Should result in 3 more ticks
        dotTestSuite.addTest(test(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test 9 (Counting tic, resetAfter=7.5)", tF2, vF2))
        tF3, vF3 = generateDOTTicCountTest(dotDurationList[i], dotList[i], jobList[i], fieldList[i], resetAfter=8) # Should result in 3 more ticks
        dotTestSuite.addTest(test(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test 10 (Counting tic, resetAfter=8)", tF3, vF3))
        tF4, vF4 = generateDOTTicCountTest(dotDurationList[i], dotList[i], jobList[i], fieldList[i], resetAfter=12.5) # Should result in 5 more ticks
        dotTestSuite.addTest(test(JobEnum.name_for_id(jobList[i]) + " dot test (" + fieldList[i] + ") - test 11 (Counting tic, resetAfter=12.5)", tF4, vF4))

    return dotTestSuite

######################################
#   RestoreFightObject testSuite     #
######################################

# This test suite only tests the function helperCode.RestoreFightObject which is used
# in the website. This is to make sure updating the website to this version does not break it 
# (or more specifically break the backend of it). This tests for both no error thrown and also
# the validity of the restoration.

def generateRFOTestSuite() -> testSuite:

    from ffxivcalc.helperCode.helper_backend import SaveFight, RestoreFightObject

    rfoTestSuite = testSuite("helperCode.RestoreFightObject test suite")

    def rfoTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        actionSet = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, 
                    Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, 
                    RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, 
                    Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, 
                    BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        
        Event.AddPlayer([player])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True


        data = SaveFight(Event, 0, 500, "", saveFile=False)

        restoredFightObj = RestoreFightObject(data)

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,
                Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage]

    def rfoTest1ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest1 = test("RestoreFightObject test 1", rfoTest1TestFunction, rfoTest1ValidationFunction)
    rfoTestSuite.addTest(rfotest1)

    # Test

    def rfoTest2TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 650, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        BLMStat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390} # Stats for BlackMage
        RDMStat = {"MainStat": 3378, "WD": 132, "Det": 1601, "Ten": 400, "SS": 502, "SkS": 400, "Crit": 2514, "DH": 1616} # Stats for RedMage
        SMNStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1342, 'Ten': 400, 'SS': 1411, 'SkS': 400, 'Crit': 2284, 'DH': 1196, 'Piety': 390} # Stats for Summoner

        BLMOpener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
                Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]
        SMNOpener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester, AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]
        RDMOpener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
                Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, 
                Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, 
                Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]
        actionSet = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, 
                    Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, 
                    RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, 
                    Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, 
                    BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        
        player = Player(actionSet, [], Stat, JobEnum.Paladin)
        BLMPlayer = Player(BLMOpener, [], BLMStat, JobEnum.BlackMage)
        RDMPlayer = Player(RDMOpener, [], RDMStat, JobEnum.RedMage)
        SMNPlayer = Player(SMNOpener, [], SMNStat, JobEnum.Summoner)
        
        Event.AddPlayer([player,BLMPlayer,RDMPlayer,SMNPlayer])

        Event.RequirementOn = True
        Event.ShowGraph = False
        Event.IgnoreMana = True


        data = SaveFight(Event, 0, 500, "", saveFile=False)

        restoredFightObj = RestoreFightObject(data)

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, 
                Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage,
                Event.PlayerList[1].TotalPotency,restoredFightObj.PlayerList[1].TotalPotency,Event.PlayerList[1].TotalDamage,restoredFightObj.PlayerList[1].TotalDamage,
                Event.PlayerList[2].TotalPotency,restoredFightObj.PlayerList[2].TotalPotency,Event.PlayerList[2].TotalDamage,restoredFightObj.PlayerList[2].TotalDamage,
                Event.PlayerList[3].TotalPotency,restoredFightObj.PlayerList[3].TotalPotency,Event.PlayerList[3].TotalDamage,restoredFightObj.PlayerList[3].TotalDamage]

    def rfoTest2ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,9):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest2 = test("RestoreFightObject test 2", rfoTest2TestFunction, rfoTest2ValidationFunction)
    rfoTestSuite.addTest(rfotest2)

    # Test

    def rfoTest3TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        SCHStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1412, 'SkS': 400, 'Crit': 2306, 'DH': 440, 'Piety': 390} # Stats for Scholar
        WHMStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for WhiteMage
        ASTStat =  {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 1242, 'SkS': 400, 'Crit': 2502, 'DH': 436, 'Piety': 390} # Stats for Astrologian
        SGEStat = {'MainStat': 3368, 'WD': 132, 'Det': 2047, 'Ten': 400, 'SS': 954, 'SkS': 400, 'Crit': 2502, 'DH': 724, 'Piety': 390} # Stats for Sage

        SCHPlayer = Player([], [], SCHStat, JobEnum.Scholar)
        WHMPlayer = Player([], [], WHMStat, JobEnum.WhiteMage)
        SGEPlayer = Player([], [], SGEStat, JobEnum.Sage)
        ASTPlayer = Player([], [], ASTStat, JobEnum.Astrologian)

        SCHOpener = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, 
                    Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Biolysis, Broil, Broil,
                    Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil]
        WHMOpener = [Glare, ThinAir, Dia, Glare, WaitAbility(1), PresenceOfMind, Glare, Glare, Glare, Glare, Glare, ThinAir, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]
        ASTOpener = [Malefic, Lightspeed, Combust, Bole(SCHPlayer),Malefic, Ewer(WHMPlayer),Malefic, Spire(SGEPlayer),Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic,Spear(ASTPlayer), Malefic, Malefic, Malefic, 
                    Malefic, Malefic,Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,
                    Malefic, Malefic, Malefic]
        SGEOpener = [Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Phlegma, Phlegma, Dosis, Dosis, Dosis, Dosis, Dosis, 
                    Dosis, Dosis, Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, 
                    Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]

        SCHPlayer.ActionSet = SCHOpener
        WHMPlayer.ActionSet = WHMOpener
        ASTPlayer.ActionSet = ASTOpener
        SGEPlayer.ActionSet = SGEOpener
        
        Event.AddPlayer([SCHPlayer,WHMPlayer,SGEPlayer,ASTPlayer])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
        data = SaveFight(Event, 0, 500, "", saveFile=False)

        restoredFightObj = RestoreFightObject(data)

        
        restoredFightObj.RequirementOn = False
        restoredFightObj.ShowGraph = False
        restoredFightObj.IgnoreMana = True
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, 
                Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage,
                Event.PlayerList[1].TotalPotency,restoredFightObj.PlayerList[1].TotalPotency,Event.PlayerList[1].TotalDamage,restoredFightObj.PlayerList[1].TotalDamage,
                Event.PlayerList[2].TotalPotency,restoredFightObj.PlayerList[2].TotalPotency,Event.PlayerList[2].TotalDamage,restoredFightObj.PlayerList[2].TotalDamage,
                Event.PlayerList[3].TotalPotency,restoredFightObj.PlayerList[3].TotalPotency,Event.PlayerList[3].TotalDamage,restoredFightObj.PlayerList[3].TotalDamage]

    def rfoTest3ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,9):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest3 = test("RestoreFightObject test 3", rfoTest3TestFunction, rfoTest3ValidationFunction)
    rfoTestSuite.addTest(rfotest3)

    # Test

    def rfoTest4TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        NINStat = {'MainStat': 3378, 'WD': 132, 'Det': 1666, 'Ten': 400, 'SS': 400, 'SkS': 714, 'Crit': 2595, 'DH': 1258, 'Piety': 390} # Stats for Ninja
        SAMStat =  {'MainStat': 3367, 'WD': 132, 'Det': 1248, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2587, 'DH': 1422, 'Piety': 390} # Stats for Samurai
        DRGStat =  {'MainStat': 3378, 'WD': 132, 'Det': 1726, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2567, 'DH': 1540, 'Piety': 390} # Stats for Dragoon
        MNKStat = {'MainStat': 3378, 'WD': 132, 'Det': 1464, 'Ten': 400, 'SS': 400, 'SkS': 889, 'Crit': 2606, 'DH': 1274, 'Piety': 390} # Stats for Monk
        RPRStat = {'MainStat': 3378, 'WD': 132, 'Det': 1870, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2567, 'DH': 1360, 'Piety': 390} # Stats for Reaper

        NINPlayer = Player([], [], NINStat, JobEnum.Ninja)
        SAMPlayer = Player([], [], SAMStat, JobEnum.Samurai)
        DRGPlayer = Player([], [], DRGStat, JobEnum.Dragoon)
        RPRPlayer = Player([], [], RPRStat, JobEnum.Reaper)
        MNKPlayer = Player([], [], MNKStat, JobEnum.Monk)

        Event.AddPlayer([NINPlayer,SAMPlayer,DRGPlayer,RPRPlayer,MNKPlayer])

        SAMOpener = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha]
        DRGOpener = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
                    LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
                    HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
                    Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
                    Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
                    Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive, RaidenThrust, WyrmwindThrust, VorpalThrust, Nastrond, HeavenThrust,
                    FangAndClaw, WheelingThrust]

        MNKOpener = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra, RisingPhoenix, RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, RisingPhoenix, TheForbiddenChakra, DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish, DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes, RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine, TwinSnakes, DragonKick, DragonKick, DragonKick, DragonKick ]
        NINOpener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju, FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        RPROpener = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows, SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon ]

        
        NINPlayer.ActionSet = NINOpener
        SAMPlayer.ActionSet = SAMOpener
        DRGPlayer.ActionSet = DRGOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        data = SaveFight(Event, 0, 500, "", saveFile=False)
        restoredFightObj = RestoreFightObject(data)

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        restoredFightObj.RequirementOn = False
        restoredFightObj.ShowGraph = False
        restoredFightObj.IgnoreMana = True
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, 
                Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage,
                Event.PlayerList[1].TotalPotency,restoredFightObj.PlayerList[1].TotalPotency,Event.PlayerList[1].TotalDamage,restoredFightObj.PlayerList[1].TotalDamage,
                Event.PlayerList[2].TotalPotency,restoredFightObj.PlayerList[2].TotalPotency,Event.PlayerList[2].TotalDamage,restoredFightObj.PlayerList[2].TotalDamage,
                Event.PlayerList[3].TotalPotency,restoredFightObj.PlayerList[3].TotalPotency,Event.PlayerList[3].TotalDamage,restoredFightObj.PlayerList[3].TotalDamage,
                Event.PlayerList[4].TotalPotency,restoredFightObj.PlayerList[4].TotalPotency,Event.PlayerList[4].TotalDamage,restoredFightObj.PlayerList[4].TotalDamage]

    def rfoTest4ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,11):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest4 = test("RestoreFightObject test 4", rfoTest4TestFunction, rfoTest4ValidationFunction)
    rfoTestSuite.addTest(rfotest4)

    # Test

    def rfoTest5TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        DRKStat = {'MainStat': 3338, 'WD': 132, 'Det': 1901, 'Ten': 529, 'SS': 400, 'SkS': 591, 'Crit': 2627, 'DH': 976, 'Piety': 390} # Stats for DarkKnight
        WARStat = {'MainStat': 3338, 'WD': 132, 'Det': 2023, 'Ten': 529, 'SS': 400, 'SkS': 948, 'Crit': 2481, 'DH': 652, 'Piety': 390} # Stats for Warrior
        WARStat = {'MainStat': 3338, 'WD': 132, 'Det': 2076, 'Ten': 529, 'SS': 400, 'SkS': 934, 'Crit': 2586, 'DH': 508, 'Piety': 390} # Stats for Warrior
        PLDStat = {'MainStat': 3328, 'WD': 132, 'Det': 2182, 'Ten': 529, 'SS': 400, 'SkS': 400, 'Crit': 2540, 'DH': 976, 'Piety': 390}# Stats for Paladin
        GNBStat = {'MainStat': 3338, 'WD': 132, 'Det': 1944, 'Ten': 529, 'SS': 400, 'SkS': 1462, 'Crit': 2262, 'DH': 436, 'Piety': 390}# Stats for Gunbreaker

        DRKPlayer = Player([], [], DRKStat, JobEnum.DarkKnight)
        WARPlayer = Player([], [], WARStat, JobEnum.Warrior)
        PLDPlayer = Player([], [], PLDStat, JobEnum.Paladin)
        GNBPlayer = Player([], [], GNBStat, JobEnum.Gunbreaker)

        Event.AddPlayer([DRKPlayer,WARPlayer,PLDPlayer,GNBPlayer])

        DRKOpener = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
                    HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
                    SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
                    Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
                    Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash ]
        WAROpener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                    FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                    HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                    FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]
        PLDOpener = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        GNBOpener = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown, RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, BrutalShell, NoMercy, RoughDivide, GnashingFang, JugularRip, DoubleDown, BlastingZone, RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel]

        DRKPlayer.ActionSet = DRKOpener
        WARPlayer.ActionSet = WAROpener
        PLDPlayer.ActionSet = PLDOpener
        GNBPlayer.ActionSet = GNBOpener

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        data = SaveFight(Event, 0, 500, "", saveFile=False)
        restoredFightObj = RestoreFightObject(data)

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        restoredFightObj.RequirementOn = False
        restoredFightObj.ShowGraph = False
        restoredFightObj.IgnoreMana = True
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, 
                Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage,
                Event.PlayerList[1].TotalPotency,restoredFightObj.PlayerList[1].TotalPotency,Event.PlayerList[1].TotalDamage,restoredFightObj.PlayerList[1].TotalDamage,
                Event.PlayerList[2].TotalPotency,restoredFightObj.PlayerList[2].TotalPotency,Event.PlayerList[2].TotalDamage,restoredFightObj.PlayerList[2].TotalDamage,
                Event.PlayerList[3].TotalPotency,restoredFightObj.PlayerList[3].TotalPotency,Event.PlayerList[3].TotalDamage,restoredFightObj.PlayerList[3].TotalDamage]

    def rfoTest5ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,9):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest5 = test("RestoreFightObject test 5", rfoTest5TestFunction, rfoTest5ValidationFunction)
    rfoTestSuite.addTest(rfotest5)

    # Test

    def rfoTest6TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)


        MCHStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2557, 'DH': 1432, 'Piety': 390} # Stats for Machinist
        BRDStat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2598, 'DH': 1252, 'Piety': 390} # Stats for Bard
        DNCStat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390} # Stats for Dancer

        MCHPlayer = Player([], [], MCHStat, JobEnum.Machinist)
        BRDPlayer = Player([], [], BRDStat, JobEnum.Bard)
        DNCPlayer = Player([], [], DNCStat, JobEnum.Dancer)

        Event.AddPlayer([MCHPlayer,BRDPlayer,DNCPlayer])

        BRDOpener = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]#,MageBallad, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, ArmyPaeon, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]
        MCHOpener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
                    Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
                    HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                    CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                    Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
                    GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]
        DNCOpener = [ClosedPosition(MCHPlayer),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]

        MCHPlayer.ActionSet = MCHOpener
        BRDPlayer.ActionSet = BRDOpener
        DNCPlayer.ActionSet = DNCOpener

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True
        
        data = SaveFight(Event, 0, 500, "", saveFile=False)
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)
        restoredFightObj = RestoreFightObject(data)

        

        restoredFightObj.RequirementOn = False
        restoredFightObj.ShowGraph = False
        restoredFightObj.IgnoreMana = True
        restoredFightObj.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, restoredFightObj.TimeStamp, #[89.99, 89.99
                Event.PlayerList[0].TotalPotency,restoredFightObj.PlayerList[0].TotalPotency,Event.PlayerList[0].TotalDamage,restoredFightObj.PlayerList[0].TotalDamage,#21650, 21650, 751042, 751042,
                Event.PlayerList[1].TotalPotency,restoredFightObj.PlayerList[1].TotalPotency,Event.PlayerList[1].TotalDamage,restoredFightObj.PlayerList[1].TotalDamage,#20100, 20100, 858422, 938710,
                Event.PlayerList[2].TotalPotency,restoredFightObj.PlayerList[2].TotalPotency,Event.PlayerList[2].TotalDamage,restoredFightObj.PlayerList[2].TotalDamage]

    def rfoTest6ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,7):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    rfotest6 = test("RestoreFightObject test 6", rfoTest6TestFunction, rfoTest6ValidationFunction)
    rfoTestSuite.addTest(rfotest6)

    return rfoTestSuite


######################################
#      preBakedFight testSuite       #
######################################

# This test suite tests the validity of preBakedFight simulations.
# It will compare the endTime, the DPS/TP/TD of the player we are preBaking the fight for.

# Speed seems to affect end time (waitAbility)

def generatePBFTestSuite() -> testSuite:

    from ffxivcalc.GearSolver.Solver import computeDamageValue

    pbfTestSuite = testSuite("PreBakedFight simulation test suite")

    # Test

    def pbfTest1TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1844, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2557, 'DH': 1396, 'Piety': 390} # Stats for Dancer

        player = Player([], [], stat, JobEnum.Dancer)

        DNCOpener = [StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]

        player.ActionSet = DNCOpener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, randomDamageDict, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)



        return [ExpectedDamage,round(comparedEvent.PlayerList[0].TotalDamage/comparedEvent.TimeStamp,2), duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest1ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest1 = test("preBakedFight test 1 - Dancer", pbfTest1TestFunction, pbfTest1ValidationFunction)
    pbfTestSuite.addTest(pbftest1)

    # Test

    def pbfTest2TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.BlackMage)

        Opener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
                Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest2ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest2 = test("preBakedFight test 2 - Blackmage", pbfTest2TestFunction, pbfTest2ValidationFunction)
    pbfTestSuite.addTest(pbftest2)

    # Test

    def pbfTest3TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Summoner)

        Opener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest3ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest3 = test("preBakedFight test 3 - Summoner", pbfTest3TestFunction, pbfTest3ValidationFunction)
    pbfTestSuite.addTest(pbftest3)

    # Test

    def pbfTest4TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.RedMage)

        Opener = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
                Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, 
                Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, 
                Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest4ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest4 = test("preBakedFight test 4 - Redmage", pbfTest4TestFunction, pbfTest4ValidationFunction)
    pbfTestSuite.addTest(pbftest4)

    # Test

    def pbfTest5TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Scholar)

        Opener = [Broil, Biolysis, Aetherflow, Broil, Swiftcast, Broil, ChainStratagem, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, 
                Broil, Dissipation, Broil, EnergyDrain, Broil, EnergyDrain, Broil, EnergyDrain, Broil, Broil, Broil, Biolysis, Broil, Broil,
                Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil,Broil, Broil]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest5ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest5 = test("preBakedFight test 5 - Scholar", pbfTest5TestFunction, pbfTest5ValidationFunction)
    pbfTestSuite.addTest(pbftest5)

    # Test

    def pbfTest6TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.WhiteMage)

        Opener = [Glare, ThinAir, Dia, Glare, WaitAbility(1), PresenceOfMind, Glare, Glare, Glare, Glare, Glare, ThinAir, Glare, Glare, Glare, Glare, 
                Glare, Glare, Dia, Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare,Glare]


        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest6ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest6 = test("preBakedFight test 6 - Whitemage", pbfTest6TestFunction, pbfTest6ValidationFunction)
    pbfTestSuite.addTest(pbftest6)

    # Test

    def pbfTest7TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Astrologian)

        Opener = [Malefic, Lightspeed, Combust, Malefic, Malefic, Divination, Malefic, MinorArcana, Astrodyne, Malefic, LordOfCrown, Malefic, Malefic, Malefic, Malefic, 
                Malefic, Malefic,Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,
                Malefic, Malefic, Malefic]


        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest7ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest7 = test("preBakedFight test 7 - Astrologian", pbfTest7TestFunction, pbfTest7ValidationFunction)
    pbfTestSuite.addTest(pbftest7)

    # Test

    def pbfTest8TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Sage)

        Opener = [Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Phlegma, Phlegma, Dosis, Dosis, Dosis, Dosis, Dosis, 
                Dosis, Dosis, Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, 
                Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]


        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest8ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest8 = test("preBakedFight test 8 - Sage", pbfTest8TestFunction, pbfTest8ValidationFunction)
    pbfTestSuite.addTest(pbftest8)

    # Test

    def pbfTest9TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Bard)

        Opener = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, BattleVoice, 
                BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, BurstShot, PitchPerfect3, BurstShot, 
                RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, 
                BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest9ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest9 = test("preBakedFight test 9 - Bard", pbfTest9TestFunction, pbfTest9ValidationFunction)
    pbfTestSuite.addTest(pbftest9)

    # Test

    def pbfTest10TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Machinist)

        Opener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
                Reassemble, WaitAbility(2.2),ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
                HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
                GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest10ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest10 = test("preBakedFight test 10 - Machinist", pbfTest10TestFunction, pbfTest10ValidationFunction)
    pbfTestSuite.addTest(pbftest10)

    # Test

    def pbfTest11TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Samurai)

        Opener =[Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten,
                Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka,
                Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu,
                Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka,
                Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest11ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest11 = test("preBakedFight test 11 - Samurai", pbfTest11TestFunction, pbfTest11ValidationFunction)
    pbfTestSuite.addTest(pbftest11)

    # Test

    def pbfTest12TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Dragoon)
        NINPlayer = Player([], [], stat, JobEnum.Ninja)

        Opener = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
                LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
                HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
                Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
                Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
                Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive, RaidenThrust, WyrmwindThrust, VorpalThrust, Nastrond, HeavenThrust,
                FangAndClaw, WheelingThrust]

        player.ActionSet = Opener

        Event.AddPlayer([player,NINPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest12ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest12 = test("preBakedFight test 12 - Dragoon", pbfTest12TestFunction, pbfTest12ValidationFunction)
    pbfTestSuite.addTest(pbftest12)

    # Test

    def pbfTest13TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Monk)

        Opener = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra, RisingPhoenix,
                RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, RisingPhoenix, TheForbiddenChakra,
                DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish,
                DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes,
                RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine, TwinSnakes, DragonKick, DragonKick, DragonKick, DragonKick ]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest13ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest13 = test("preBakedFight test 13 - Monk", pbfTest13TestFunction, pbfTest13ValidationFunction)
    pbfTestSuite.addTest(pbftest13)

    # Test

    def pbfTest14TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Ninja)

        Opener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi,
                TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra,
                FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge,
                GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, 
                GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju,
                FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest14ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest14 = test("preBakedFight test 14 - Ninja", pbfTest14TestFunction, pbfTest14ValidationFunction)
    pbfTestSuite.addTest(pbftest14)

    # Test

    def pbfTest15TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Reaper)

        Opener = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, WaitAbility(0.01),Potion, PlentifulHarvest, Enshroud, CrossReaping, VoidReaping, 
                LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, Gibbet, ShadowOfDeath, Slice, 
                WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows, SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, 
                VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon ]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest15ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest15 = test("preBakedFight test 15 - Reaper", pbfTest15TestFunction, pbfTest15ValidationFunction)
    pbfTestSuite.addTest(pbftest15)

    # Test

    def pbfTest16TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.DarkKnight)

        Opener = [BloodWeapon,WaitAbility(5),TBN(player), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
                HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
                SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
                Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
                Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash ]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest16ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest16 = test("preBakedFight test 16 - DarkKnight", pbfTest16TestFunction, pbfTest16ValidationFunction)
    pbfTestSuite.addTest(pbftest16)

    # Test

    def pbfTest17TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Warrior)

        Opener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest17ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest17 = test("preBakedFight test 17 - Warrior", pbfTest17TestFunction, pbfTest17ValidationFunction)
    pbfTestSuite.addTest(pbftest17)

    # Test

    def pbfTest18TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Paladin)

        Opener = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, CircleScorn, Expiacion,
                Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, Atonement, FastBlade, RiotBlade, RoyalAuthority,
                Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, HolySpirit, RoyalAuthority, Atonement, Atonement, Atonement, FastBlade,
                RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, Confetti, BladeFaith, Intervene, BladeTruth, Intervene, BladeValor, HolySpirit, RoyalAuthority,
                HolySpirit, Atonement ]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest18ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest18 = test("preBakedFight test 18 - Paladin", pbfTest18TestFunction, pbfTest18ValidationFunction)
    pbfTestSuite.addTest(pbftest18)

    # Test

    def pbfTest19TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Gunbreaker)

        Opener = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown, RoughDivide, SavageClaw, 
                AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, 
                GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, 
                SolidBarrel,KeenEdge, BrutalShell, NoMercy, RoughDivide, GnashingFang, JugularRip, DoubleDown, BlastingZone, RoughDivide, SavageClaw, AbdomenTear, WickedTalon,
                EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel]

        player.ActionSet = Opener

        Event.AddPlayer([player])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage, duration, comparedEvent.TimeStamp,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest19ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest19 = test("preBakedFight test 19 - Gunbreaker", pbfTest19TestFunction, pbfTest19ValidationFunction)
    pbfTestSuite.addTest(pbftest19)

    # Test

    def pbfTest20TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Ninja)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi,
                TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra,
                FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge,
                GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, 
                GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju,
                FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest20ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest20 = test("preBakedFight test 20 - Ninja Dance partner", pbfTest20TestFunction, pbfTest20ValidationFunction)
    pbfTestSuite.addTest(pbftest20)

    # Test

    def pbfTest21TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Ninja)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi,
                TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra,
                FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge,
                GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, 
                GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju,
                FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest21ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest21 = test("preBakedFight test 21 - Ninja + Dance partner + Dragoon buff", pbfTest21TestFunction, pbfTest21ValidationFunction)
    pbfTestSuite.addTest(pbftest21)

    # Test

    def pbfTest22TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Ninja)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)
        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)

        Opener = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, PhantomKamaitachi,
                TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, Jin2, Meisui, FleetingRaiju, Bhavacakra,
                FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge,
                GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, 
                GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju,
                FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(20), Bole(player)]


        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        

        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer, RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest22ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest22 = test("preBakedFight test 22 - Ninja + Dance partner + Dragoon buff + Astro card + Other buff", pbfTest22TestFunction, pbfTest22ValidationFunction)
    pbfTestSuite.addTest(pbftest22)

    # Test

    def pbfTest23TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Machinist)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
                Reassemble, WaitAbility(2.2),ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
                HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
                GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest23ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest23 = test("preBakedFight test 23 - Machinist Dance partner", pbfTest23TestFunction, pbfTest23ValidationFunction)
    pbfTestSuite.addTest(pbftest23)

    # Test

    def pbfTest24TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Machinist)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
                Reassemble, WaitAbility(2.2),ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
                HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
                GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest24ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest24 = test("preBakedFight test 24 - Machinist + Dance partner + Dragoon buff", pbfTest24TestFunction, pbfTest24ValidationFunction)
    pbfTestSuite.addTest(pbftest24)

    # Test

    def pbfTest25TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Machinist)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)

        Opener = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
                Reassemble, WaitAbility(2.2),ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
                HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
                Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
                GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(10),Divination, WaitAbility(10), Bole(player)]

        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)
        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener
        

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer,RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest25ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest25 = test("preBakedFight test 25 - Machinist + Dance partner + Dragoon buff + astro card + Other buff", pbfTest25TestFunction, pbfTest25ValidationFunction)
    pbfTestSuite.addTest(pbftest25)

    # Test

    def pbfTest26TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Summoner)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3, Summon, FountainOfFire, FountainOfFire, EnergyDrainSMN, Enkindle, FountainOfFire, 
                Fester, FountainOfFire, Fester,FountainOfFire,  Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest26ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest26 = test("preBakedFight test 26 - Summoner Dance partner", pbfTest26TestFunction, pbfTest26ValidationFunction)
    pbfTestSuite.addTest(pbftest26)

    # Test

    def pbfTest27TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Summoner)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3, Summon, FountainOfFire, FountainOfFire, EnergyDrainSMN, Enkindle, FountainOfFire, 
                Fester, FountainOfFire, Fester,FountainOfFire,  Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest27ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest27 = test("preBakedFight test 27 - Summoner + Dance partner + Dragoon buff", pbfTest27TestFunction, pbfTest27ValidationFunction)
    pbfTestSuite.addTest(pbftest27)

    # Test

    def pbfTest28TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Summoner)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)

        Opener = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3, Summon, FountainOfFire, FountainOfFire, EnergyDrainSMN, Enkindle, FountainOfFire, 
                Fester, FountainOfFire, Fester,FountainOfFire,  Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz,
                Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(20), Bole(player)]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)
        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer,RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest28ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest28 = test("preBakedFight test 28 - Summoner + Dance partner + Dragoon buff + astro card + Other buff", pbfTest28TestFunction, pbfTest28ValidationFunction)
    pbfTestSuite.addTest(pbftest28)

    # Test

    def pbfTest29TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.DarkKnight)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [BloodWeapon,WaitAbility(5),TBN(player), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
                HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
                SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
                Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
                Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater,
                HardSlash , SyphonStrike, Souleater]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest29ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest29 = test("preBakedFight test 29 - DarkKnight Dance partner", pbfTest29TestFunction, pbfTest29ValidationFunction)
    pbfTestSuite.addTest(pbftest29)

    # Test

    def pbfTest30TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.DarkKnight)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [BloodWeapon,WaitAbility(5),TBN(player), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
                HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
                SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
                Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
                Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater,
                HardSlash , SyphonStrike, Souleater]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest30ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest30 = test("preBakedFight test 30 - DarkKnight + Dance partner + Dragoon buff", pbfTest30TestFunction, pbfTest30ValidationFunction)
    pbfTestSuite.addTest(pbftest30)

    # Test

    def pbfTest31TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.DarkKnight)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)

        Opener = [BloodWeapon,WaitAbility(5),TBN(player), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
                HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
                SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
                Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
                Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater, HardSlash , SyphonStrike, Souleater,
                HardSlash , SyphonStrike, Souleater]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(20), Bole(player)]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)
        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer,RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest31ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest31 = test("preBakedFight test 31 - DarkKnight + Dance partner + Dragoon buff + astro card + Other buff", pbfTest31TestFunction, pbfTest31ValidationFunction)
    pbfTestSuite.addTest(pbftest31)

    # Test

    def pbfTest32TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.BlackMage)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
                Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest32ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest32 = test("preBakedFight test 32 - Blackmage Dance partner", pbfTest32TestFunction, pbfTest32ValidationFunction)
    pbfTestSuite.addTest(pbftest32)

    # Test

    def pbfTest33TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.BlackMage)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
                Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest33ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest33 = test("preBakedFight test 33 - Blackmage + Dance partner + Dragoon buff", pbfTest33TestFunction, pbfTest33ValidationFunction)
    pbfTestSuite.addTest(pbftest33)

    # Test

    def pbfTest34TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.BlackMage)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)

        Opener = [SharpCast, Fire3, Thunder3, Fire4, Triplecast, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
                Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
                Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(20), Bole(player)]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)
        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer,RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest34ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest34 = test("preBakedFight test 34 - Blackmage + Dance partner + Dragoon buff + astro card + Other buff", pbfTest34TestFunction, pbfTest34ValidationFunction)
    pbfTestSuite.addTest(pbftest34)

    ###############


    ###############


    # Test

    def pbfTest35TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Warrior)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)

        Opener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath,
                HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath]
        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]


        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener

        Event.AddPlayer([player, dncPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest35ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest35 = test("preBakedFight test 35 - Warrior Dance partner", pbfTest35TestFunction, pbfTest35ValidationFunction)
    pbfTestSuite.addTest(pbftest35)

    # Test

    def pbfTest36TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Warrior)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)

        Opener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath,
                HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency]

    def pbfTest36ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest36 = test("preBakedFight test 36 - Warrior + Dance partner + Dragoon buff", pbfTest36TestFunction, pbfTest36ValidationFunction)
    pbfTestSuite.addTest(pbftest36)

    # Test

    def pbfTest37TestFunction() -> None:
        """
        """

        Dummy = Enemy()
        Event = Fight(Dummy, False)
        stat = {'MainStat': 3378, 'WD': 132, 'Det': 1885, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2598, 'DH': 1252, 'Piety': 390}

        player = Player([], [], stat, JobEnum.Warrior)
        dncPlayer = Player([], [], stat, JobEnum.Dancer)
        drgPlayer = Player([], [], stat, JobEnum.Dragoon)
        astPlayer = Player([], [], stat, JobEnum.Astrologian)

        Opener = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath,
                HeavySwing, Maim, StormPath, HeavySwing, Maim, StormPath]

        
        DNCOpener = [ClosedPosition(player),StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite, TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, Fountain, FountainFall]
        drgOpener = [DragonSight(player), BattleLitany]
        astOpener = [Bole(player), WaitAbility(20), Bole(player)]

        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        RDMPlayer = Player([], [], stat, JobEnum.RedMage)
        SCHPlayer = Player([], [], stat, JobEnum.Scholar)
        RPRPlayer = Player([], [], stat, JobEnum.Reaper)
        MNKPlayer = Player([], [], stat, JobEnum.Monk)
        RDMOpener = [WaitAbility(15), Embolden]
        SCHOpener = [WaitAbility(7), ChainStratagem]
        RPROpener = [ArcaneCircle]
        MNKOpener = [WaitAbility(30), Brotherhood]
        RDMPlayer.ActionSet = RDMOpener
        SCHPlayer.ActionSet = SCHOpener
        RPRPlayer.ActionSet = RPROpener
        MNKPlayer.ActionSet = MNKOpener
        player.ActionSet = Opener
        dncPlayer.ActionSet = DNCOpener
        drgPlayer.ActionSet = drgOpener
        astPlayer.ActionSet = astOpener

        Event.AddPlayer([player, dncPlayer, drgPlayer, astPlayer,RDMPlayer, SCHPlayer, RPRPlayer, MNKPlayer])

        comparedEvent = Event.deepCopy()

        Event.SavePreBakedAction = True
        Event.PlayerIDSavePreBakedAction = 1
        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        comparedEvent.RequirementOn = False
        comparedEvent.ShowGraph = False
        comparedEvent.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)
        comparedEvent.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(stat, player.JobMod, player.RoleEnum == RoleEnum.Tank, player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer)
        ExpectedDamage, expectedTotalDamage, duration, potency = Event.SimulatePreBakedFight(0, player.baseMainStat,f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=1,getInfo = True)


        return [ duration, comparedEvent.TimeStamp, 
                expectedTotalDamage,comparedEvent.PlayerList[0].TotalDamage,potency, comparedEvent.PlayerList[0].TotalPotency,]

    def pbfTest37ValidationFunction(testResults) -> (bool, list):
        passed = True

        for i in range(0,3):
            passed = passed and testResults[2*i] == testResults[2*i + 1]

        return passed , testResults

    pbftest37 = test("preBakedFight test 37 - Warrior + Dance partner + Dragoon buff + astro card + Other buff", pbfTest37TestFunction, pbfTest37ValidationFunction)
    pbfTestSuite.addTest(pbftest37)

    return pbfTestSuite

######################################
#      GCD timer testSuite       #
######################################

# This test suite tests the GCD timer of a player under certain effect and tests the AA delay if it applies.
# These tests are randomly generated given a seed that can be set by changing the value under here. 
# The randomness is to select a SpS/SkS value and a random autoDelay (if it applies) since testing all different values might be redundant but also
# a bit long. Going for random testing here is in my opinion the best way.

def generateGCDTestSuite(setSeed : int = 0) -> testSuite:

    randomSeed = randint(1,999999) if setSeed == 0 else setSeed
    seed(randomSeed)
    gcdTestSuite = testSuite(f"GCD timer simulation test suite - seed {randomSeed}")


    def __computeGCDAndAATimer(spdValue : int, hasteAmount : int, autoHasteAmount : int, weaponDelay : int) -> (float, float):
        """
        This function computes the GCD timer assuming a base GCD of 2.5 seconds and
        the weaponDelay given a base weaponDelay.
        spdValue : int -> Speed stat's value
        hasteAmount : int -> Amount of haste affecting the GCD timer
        autoHasteAmount : int -> Amount of haste affecting the weaponDelay only.
        weaponDelay : int -> Weapon delay in milli seconds.
        """
        reductionRatio = (1000 - math.floor(130 * (spdValue-400) / 1900))/1000
        gcdTimer = floor(floor(floor((2500 * reductionRatio)) * (100 - hasteAmount)/100)/10)/100

        aaMultHaste = int((100-hasteAmount) * (100-autoHasteAmount)/100)
        curDelay = floor(floor(weaponDelay * (aaMultHaste)/100)/10)/100

        return gcdTimer, curDelay

    # generateGCDTest() generates a gcd test with a random SpS/SkS value.

    def generateGCDTest(testPlayer, gcdAction,hasteAction,actionHasteAmount : int, autoHasteAmount : int, baseHaste : int, testAA : bool, testSeed : int = randomSeed):
        """
        This function generates a random gcd timer test using the seed given.
        testPlayer : Player -> player object to test
        hasteAction : Spell -> Action to have the player perform
        actionHasteAmount : int -> Haste amount gained by that action.
        autoHasteAmount : int -> Amount of haste gained for autos.
        baseHaste : int -> Base haste amount. Usually coming from traits
        testAA : bool -> True if want to test for aaDelay too.
        """
                                # Sampling SPD value between 400-3500
                                # and weaponDelay between 2.00-3.00 seconds
        randomSPD = randint(400,3500)
        randomDelay = randint(200,300) * 10 if testAA else 3000

        def testFunction() -> list:
            testPlayer.setStat(base_stat)

            isCaster = testPlayer.RoleEnum == RoleEnum.Caster or testPlayer.RoleEnum == RoleEnum.Healer
            testPlayer.Stat["SS" if isCaster else "SkS"] = randomSPD
            testPlayer.baseDelay = round(randomDelay/1000,2)
                                    # Changing player field if required
            match testPlayer.JobEnum:
                case JobEnum.Astrologian:
                    testPlayer.Celestial , testPlayer.Solar, testPlayer.Lunar = True, True, True
                case JobEnum.Samurai:
                    testPlayer.EffectList.append(HakazeEffect)
                case _:
                    pass

                                    # Creating all event and simulating them. Taking results to compare later in test and validation
                                    # function of the test.
            Dummy = Enemy()
            Event = Fight(Dummy, False)

            testResult = []
            expectedResult = []

                                    # Doing hasteAction and then gcd.
                                    # Should expect gcd timer to be affected by action.
            Event.AddPlayer([deepcopy(testPlayer)])
            Event.PlayerList[0].ActionSet = [hasteAction, gcdAction]

            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

            Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

            gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, actionHasteAmount + baseHaste, 0, randomDelay)

            testResult += [Event.PlayerList[0].CastingSpell.RecastTime]
            expectedResult += [gcdTimer]

                                    # Should affect recast time
            Event = Fight(Dummy, False)
            Event.AddPlayer([deepcopy(testPlayer)])
            Event.PlayerList[0].ActionSet = [gcdAction, hasteAction, gcdAction]

            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

            Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

            gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, actionHasteAmount + baseHaste, 0, randomDelay)

            testResult += [Event.PlayerList[0].CastingSpell.RecastTime]
            expectedResult += [gcdTimer]

                                    # Should not affect recast time
            Event = Fight(Dummy, False)
            Event.AddPlayer([deepcopy(testPlayer)])
            Event.PlayerList[0].ActionSet = [gcdAction, hasteAction, WaitAbility(65), gcdAction]

            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

            Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

            gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, 0 + baseHaste, 0, randomDelay)

            testResult += [Event.PlayerList[0].CastingSpell.RecastTime]
            expectedResult += [gcdTimer]

                                    # Should not affect recast time
            Event = Fight(Dummy, False)
            Event.AddPlayer([deepcopy(testPlayer)])
            Event.PlayerList[0].ActionSet = [hasteAction, WaitAbility(65), gcdAction]

            Event.RequirementOn = False
            Event.ShowGraph = False
            Event.IgnoreMana = True

            Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

            gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, 0 + baseHaste, 0, randomDelay)

            testResult += [Event.PlayerList[0].CastingSpell.RecastTime]
            expectedResult += [gcdTimer]


            if testAA:
                                    # Should not affect weaponDelay
                Event = Fight(Dummy, False)
                Event.AddPlayer([deepcopy(testPlayer)])
                Event.PlayerList[0].ActionSet = [gcdAction,hasteAction, WaitAbility(0.1)]

                Event.RequirementOn = False
                Event.ShowGraph = False
                Event.IgnoreMana = True

                Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

                gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, actionHasteAmount + baseHaste, autoHasteAmount, randomDelay)

                testResult += [Event.PlayerList[0].currentDelay]
                expectedResult += [aaDelay]

                                    # Should not affect weaponDelay
                Event = Fight(Dummy, False)
                Event.AddPlayer([deepcopy(testPlayer)])
                Event.PlayerList[0].ActionSet = [gcdAction,hasteAction, WaitAbility(65)]

                Event.RequirementOn = False
                Event.ShowGraph = False
                Event.IgnoreMana = True

                Event.SimulateFight(0.01, 500, False, n=0,PPSGraph=False, showProgress=False,computeGraph=False)

                gcdTimer, aaDelay = __computeGCDAndAATimer(randomSPD, 0 + baseHaste, 0, randomDelay)

                testResult += [Event.PlayerList[0].currentDelay]
                expectedResult += [aaDelay]

            testResult = list(map(lambda x : round(x,2),testResult))

            return testResult, expectedResult
        
        def validationFunction(result) -> (bool, list):
            passed = True
            testResult = result[0]
            expected = result[1]

            for i in range(len(result)): passed = passed and (testResult[i]== expected[i])

            return passed, expected
        
        return testFunction, validationFunction, randomSPD, randomDelay

    # Generating test

    playerTestList = [JobEnum.BlackMage, JobEnum.WhiteMage, JobEnum.Astrologian, JobEnum.Ninja, JobEnum.Samurai,JobEnum.Monk, JobEnum.Summoner, JobEnum.Gunbreaker, JobEnum.Scholar, JobEnum.Reaper]
    hasteActionTestList = [LeyLines, PresenceOfMind, Astrodyne, Huton, Shifu, RiddleOfWind, WaitAbility(1), WaitAbility(1), WaitAbility(1), WaitAbility(1)]
    actionHasteAmountList = [15, 20, 10, 15, 13, 0, 0, 0, 0, 0]
    aaHasteAmountList = [0, 0, 0, 0, 0, 50, 0, 0, 0, 0]
    baseHasteAmountList = [0, 0, 0, 0, 0, 20, 0, 0, 0, 0]
    actionTestList = [Xenoglossy, Dia, Combust, ArmorCrush, Enpi, Bootshine, Titan, DoubleDown, Broil, Slice]
    testAAList = [False, False, False, True, True, True, False, True, False, True]

    # Number of tests to be performed per job
    n = 5

    for i,job in enumerate(playerTestList):
        testPlayer = Player([], [], base_stat, job)
        for j in range(n):
            tF, vF, randomSPD, randomDelay = generateGCDTest(testPlayer, actionTestList[i], hasteActionTestList[i], actionHasteAmountList[i],
                                    aaHasteAmountList[i], baseHasteAmountList[i],  testAAList[i])
            
            gcdTestSuite.addTest(test("GCD timer " + ("+ AA delay " if testAAList[i] else "") + f" for {JobEnum.name_for_id(job)} test {j+1} - SPD : {randomSPD} + wDelay : {randomDelay}", tF, vF))

    return gcdTestSuite


######################################
# TimeStamp, Dot/Buff timer estimate #
######################################

# This functionality aims to estimate the timestamp of a player
# to situate oneself while using the app or building a rotation.
# Since this is an estimate the tests will simply be :
# Simulate the fight and check within a certain margin of error that 
# the estimate is in agreement.
#{"currentTimeStamp" : round(curTimeStamp,2), "untilNextGCD" : round(finalGCDLockTimer,2), "dotTimer" : round(curDOTTimer,2), "buffTimer" : round(curBuffTimer,2)}


errorAmount = 0.5
errorAmountBigger = 1.5

def isClose(a : float,b : float, error : int) -> bool:
    """This function returns true if a and b are within error of each other
    """
    return abs(a - b) <= error

def generateTimerEstimateTestSuite() -> testSuite:

    timerEstimateTestSuite = testSuite("TimerEstimateTestSuite - errorAmount : " + str(errorAmount) + " errorAmountBigger : " + str(errorAmountBigger))

    def teTest1TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Biolysis, Broil]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BiolysisTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest1ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest1 = test("Scholar DOT and Timestamp estimate test 1 ", teTest1TestFunction, teTest1ValidationFunction)
    timerEstimateTestSuite.addTest(teTest1)

    def teTest2TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Biolysis, Broil, Broil, Broil, Broil]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BiolysisTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest2ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest2 = test("Scholar DOT and Timestamp estimate test 2 ", teTest2TestFunction, teTest2ValidationFunction)
    timerEstimateTestSuite.addTest(teTest2)

    def teTest3TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Biolysis, Broil, Broil, Broil, Broil,Broil, Biolysis]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BiolysisTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest3ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest3 = test("Scholar DOT and Timestamp estimate test 3 ", teTest3TestFunction, teTest3ValidationFunction)
    timerEstimateTestSuite.addTest(teTest3)

    def teTest4TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Biolysis, Broil, Broil, Broil, Broil,Broil, Biolysis, Broil,Broil, Ruin]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BiolysisTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest4ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest4 = test("Scholar DOT and Timestamp estimate test 4 ", teTest4TestFunction, teTest4ValidationFunction)
    timerEstimateTestSuite.addTest(teTest4)

    def teTest13TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Biolysis, Broil, Broil, Broil, Broil,Broil, Biolysis, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil, Broil]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.BiolysisTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest13ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest13 = test("Scholar DOT and Timestamp estimate test 5 ", teTest13TestFunction, teTest13ValidationFunction)
    timerEstimateTestSuite.addTest(teTest13)

    def teTest5TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest5ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest5 = test("Whitemage DOT and Timestamp estimate test 1 ", teTest5TestFunction, teTest5ValidationFunction)
    timerEstimateTestSuite.addTest(teTest5)

    def teTest6TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia, Glare, Glare, Glare, Glare, Glare, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest6ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest6 = test("Whitemage DOT and Timestamp estimate test 2 ", teTest6TestFunction, teTest6ValidationFunction)
    timerEstimateTestSuite.addTest(teTest6)

    def teTest7TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest7ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest7 = test("Whitemage DOT and Timestamp estimate test 3 ", teTest7TestFunction, teTest7ValidationFunction)
    timerEstimateTestSuite.addTest(teTest7)

    def teTest8TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 716, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Dia, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest8ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest8 = test("Whitemage DOT and Timestamp estimate test 4 ", teTest8TestFunction, teTest8ValidationFunction)
    timerEstimateTestSuite.addTest(teTest8)

    def teTest9TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 800, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia,Glare, PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare,
        Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest9ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest9 = test("Whitemage DOT and Timestamp estimate - Presence of mind test 1 ", teTest9TestFunction, teTest9ValidationFunction)
    timerEstimateTestSuite.addTest(teTest9)

    def teTest10TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 800, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia,PresenceOfMind, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare,
        Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest10ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest10 = test("Whitemage DOT and Timestamp estimate - Presence of mind test 2 ", teTest10TestFunction, teTest10ValidationFunction)
    timerEstimateTestSuite.addTest(teTest10)

    def teTest11TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 800, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia,PresenceOfMind, Glare, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest11ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest11 = test("Whitemage DOT and Timestamp estimate - Presence of mind test 3 ", teTest11TestFunction, teTest11ValidationFunction)
    timerEstimateTestSuite.addTest(teTest11)


    def teTest12TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 800, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Dia,PresenceOfMind, Glare, Glare, Glare, Dia, Glare, Glare, Glare, Glare, Glare]
        player = Player(actionSet, [], Stat, JobEnum.WhiteMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.DiaTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest12ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest12 = test("Whitemage DOT and Timestamp estimate - Presence of mind test 4 ", teTest12TestFunction, teTest12ValidationFunction)
    timerEstimateTestSuite.addTest(teTest12)

    def teTest14TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 900, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Eukrasia, EukrasianDosis, Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EukrasianTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest14ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest14 = test("Sage DOT and Timestamp estimate test 1 ", teTest14TestFunction, teTest14ValidationFunction)
    timerEstimateTestSuite.addTest(teTest14)

    def teTest15TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 900, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EukrasianTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest15ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest15 = test("Sage DOT and Timestamp estimate test 2 ", teTest15TestFunction, teTest15ValidationFunction)
    timerEstimateTestSuite.addTest(teTest15)

    def teTest16TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 900, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis,Dosis, Eukrasia, EukrasianDosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EukrasianTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest16ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest16 = test("Sage DOT and Timestamp estimate test 3 ", teTest16TestFunction, teTest16ValidationFunction)
    timerEstimateTestSuite.addTest(teTest16)

    def teTest17TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 900, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis,Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EukrasianTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest17ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest17 = test("Sage DOT and Timestamp estimate test 4 ", teTest17TestFunction, teTest17ValidationFunction)
    timerEstimateTestSuite.addTest(teTest17)

    def teTest18TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 900, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis,Dosis, Eukrasia, EukrasianDosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis, Dosis]
        player = Player(actionSet, [], Stat, JobEnum.Sage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.EukrasianTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest18ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest18 = test("Sage DOT and Timestamp estimate test 5 ", teTest18TestFunction, teTest18ValidationFunction)
    timerEstimateTestSuite.addTest(teTest18)


    def teTest19TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Combust, Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest19ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest19 = test("Astrologian DOT and Timestamp estimate test 1 ", teTest19TestFunction, teTest19ValidationFunction)
    timerEstimateTestSuite.addTest(teTest19)

    def teTest20TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, ]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest20ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest20 = test("Astrologian DOT and Timestamp estimate test 2 ", teTest20TestFunction, teTest20ValidationFunction)
    timerEstimateTestSuite.addTest(teTest20)

    def teTest21TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Combust ]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest21ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest21 = test("Astrologian DOT and Timestamp estimate test 3 ", teTest21TestFunction, teTest21ValidationFunction)
    timerEstimateTestSuite.addTest(teTest21)

    def teTest22TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Combust ]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest22ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest22 = test("Astrologian DOT and Timestamp estimate test 4 ", teTest22TestFunction, teTest22ValidationFunction)
    timerEstimateTestSuite.addTest(teTest22)


    def teTest23TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic,Malefic, Malefic,Malefic, Malefic,Malefic, Malefic ]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest23ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest23 = test("Astrologian DOT and Timestamp estimate test 5 ", teTest23TestFunction, teTest23ValidationFunction)
    timerEstimateTestSuite.addTest(teTest23)

    def teTest24TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [Malefic, Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Arcanum(NINPlayer, "Celestial", True), Astrodyne, Malefic,
                     Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest24ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest24 = test("Astrologian DOT and Timestamp estimate - Astrodyne test 1 ", teTest24TestFunction, teTest24ValidationFunction)
    timerEstimateTestSuite.addTest(teTest24)


    def teTest25TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [Malefic, Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Arcanum(NINPlayer, "Celestial", True), Astrodyne, Malefic,
                     Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Combust,Malefic,Malefic,Malefic,Malefic,Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest25ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest25 = test("Astrologian DOT and Timestamp estimate - Astrodyne test 2 ", teTest25TestFunction, teTest25ValidationFunction)
    timerEstimateTestSuite.addTest(teTest25)

    def teTest26TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [Arcanum(NINPlayer, "Solar", True),Arcanum(NINPlayer, "Lunar", True),Arcanum(NINPlayer, "Celestial", True), Astrodyne, Malefic,
                     Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Malefic,Combust,Malefic,Malefic,Malefic,Malefic,Malefic]
        player = Player(actionSet, [], Stat, JobEnum.Astrologian)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CumbustDOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest26ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest26 = test("Astrologian DOT and Timestamp estimate - Astrodyne test 3 ", teTest26TestFunction, teTest26ValidationFunction)
    timerEstimateTestSuite.addTest(teTest26)

    def teTest27TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Thunder3, Fire1, Fire1, Fire1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest27ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest27 = test("Blackmage DOT and Timestamp estimate test 1", teTest27TestFunction, teTest27ValidationFunction)
    timerEstimateTestSuite.addTest(teTest27)
    
    def teTest28TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Fire1,Thunder3, Fire1, Fire1, Fire1, Fire4, Fire4, Despair]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest28ValidationFunction(testResults) -> (bool, list):
        passed = True   

        for i in range(0,len(testResults),2): passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest28 = test("Blackmage DOT and Timestamp estimate test 2", teTest28TestFunction, teTest28ValidationFunction)
    timerEstimateTestSuite.addTest(teTest28)

    def teTest29TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Thunder3, Fire1, Fire1, Fire1, Fire4, Fire4, Despair, Xenoglossy, Thunder3, WaitAbility(15), Fire4, Fire1, Fire1, Fire1, Fire1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest29ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest29 = test("Blackmage DOT and Timestamp estimate test 3", teTest29TestFunction, teTest29ValidationFunction)
    timerEstimateTestSuite.addTest(teTest29)

    def teTest30TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [SharpCast, Fire3, Thunder3, Fire4, Fire4, Potion, Fire4, Amplifier, LeyLines, Fire4, Swiftcast, Despair, 
             Manafront,Triplecast, Fire4, Despair, Transpose, Paradox, Xenoglossy, Thunder3, Transpose, Fire3, Fire4, Fire4, Fire4, Despair, 
             Blizzard3, Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
             Blizzard3, Thunder3,Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
             Blizzard3, Thunder3,Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair,
             Blizzard3, Thunder3,Blizzard4,Paradox, Fire3, Fire4, Fire4, Fire4, Paradox, Fire4, Fire4, Fire4, Despair]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"],estimate['detectedInFire'],estimate['detectedInIce']]

    def teTest30ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults)-2,2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmountBigger)

        passed = passed and testResults[-2] == True and testResults[-1] == False
        return passed , testResults

    teTest30 = test("Blackmage DOT and Timestamp estimate test 4 - Leylines (error < 1.5)", teTest30TestFunction, teTest30ValidationFunction)
    timerEstimateTestSuite.addTest(teTest30)

    def teTest31TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Fire3, LeyLines,Thunder3, Blizzard3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"],estimate['detectedInFire'],estimate['detectedInIce']]

    def teTest31ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults)-2,2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        passed = passed and testResults[-2] == True and testResults[-1] == False
        return passed , testResults

    teTest31 = test("Blackmage DOT and Timestamp estimate test 5 - Leylines", teTest31TestFunction, teTest31ValidationFunction)
    timerEstimateTestSuite.addTest(teTest31)


    def teTest32TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Fire3, LeyLines,Thunder3, Blizzard3,Paradox, Transpose, Swiftcast, Fire3, Fire4]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.Thunder3DOTTimer, estimate["dotTimer"], Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"],estimate['detectedInFire'],estimate['detectedInIce']]

    def teTest32ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults)-2,2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        passed = passed and testResults[-2] == True and testResults[-1] == False
        return passed , testResults

    teTest32 = test("Blackmage DOT and Timestamp estimate test 6 - Leylines", teTest32TestFunction, teTest32ValidationFunction)
    timerEstimateTestSuite.addTest(teTest32)

    def teTest33TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder, Embolden, Manafication, EnchantedRiposte, Fleche, EnchantedZwerchhau, 
             Contre, EnchantedRedoublement, Corps, Engagement, Verholy, Corps, Engagement, Scorch, Resolution, Verstone, Verareo, Verfire, Verthunder, 
             Acceleration, Verareo, Verstone, Verthunder, Fleche, Jolt, Verthunder, Verfire, Verareo, Contre, Jolt, Verareo, Engagement, Corps, Verstone, 
             Verthunder, EnchantedRiposte, EnchantedZwerchhau, EnchantedRedoublement, Fleche, Verflare, Scorch, Resolution]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], False, estimate['dualCast']]

    def teTest33ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest33 = test("Redmage Timestamp estimate test 1", teTest33TestFunction, teTest33ValidationFunction)
    timerEstimateTestSuite.addTest(teTest33)

    def teTest34TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo, Swiftcast,Acceleration, Verthunder, Potion,Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], False, estimate['dualCast']]

    def teTest34ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest34 = test("Redmage Timestamp estimate test 2", teTest34TestFunction, teTest34ValidationFunction)
    timerEstimateTestSuite.addTest(teTest34)

    def teTest35TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 950, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Verthunder, Verareo,Verstone, Swiftcast,Acceleration, Verthunder, Potion,Verthunder]
        player = Player(actionSet, [], Stat, JobEnum.RedMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], True, estimate['dualCast']]

    def teTest35ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest35 = test("Redmage Timestamp estimate test 3", teTest35TestFunction, teTest35ValidationFunction)
    timerEstimateTestSuite.addTest(teTest35)

    def teTest36TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 523, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                    AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream, Emerald, Emerald, Emerald, Emerald, Titan, Topaz, Mountain, Topaz, 
                    Mountain, Topaz, Mountain, Topaz, Mountain, Ifrit, Cyclone, Strike, Ruby, Ruby, Ruin4, Ruin3]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest36ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest36 = test("Summoner Timestamp estimate test 1", teTest36TestFunction, teTest36ValidationFunction)
    timerEstimateTestSuite.addTest(teTest36)

    def teTest37TestFunction() -> None:
 

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 523, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Ruin3, Summon, SearingLight, AstralImpulse, AstralImpulse, AstralImpulse, EnergyDrainSMN, Enkindle, AstralImpulse, Deathflare, Fester,
                    AstralImpulse, Fester, AstralImpulse, Garuda, Swiftcast, Slipstream]
        player = Player(actionSet, [], Stat, JobEnum.Summoner)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest37ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest37 = test("Summoner Timestamp estimate test 2", teTest37TestFunction, teTest37ValidationFunction)
    timerEstimateTestSuite.addTest(teTest37)

    def teTest37TestFunction() -> None:


        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, 
                     PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, 
                     Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, 
                     SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, 
                     Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, 
                     Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju, FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest37ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest37 = test("Ninja Timestamp estimate test 1", teTest37TestFunction, teTest37ValidationFunction)
    timerEstimateTestSuite.addTest(teTest37)

    def teTest38TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Huton,SpinningEdge, GustSlash, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge,
                    GustSlash, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest38ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest38 = test("Ninja Timestamp estimate test 2", teTest38TestFunction, teTest38ValidationFunction)
    timerEstimateTestSuite.addTest(teTest38)

    def teTest39TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Jin, Chi, Ten, Huton, Hide, Ten, Chi, Jin, WaitAbility(5), Suiton, Kassatsu, SpinningEdge, Potion, GustSlash, Mug, Bunshin, 
                     PhantomKamaitachi, TrickAttack, AeolianEdge, DreamWithinADream, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, TenChiJin, Ten2, Chi2, 
                     Jin2, Meisui, FleetingRaiju, Bhavacakra, FleetingRaiju, Bhavacakra, Ten, Chi, Raiton, FleetingRaiju, SpinningEdge, GustSlash, AeolianEdge, 
                     SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, GustSlash, ArmorCrush, Bhavacakra, SpinningEdge, GustSlash, AeolianEdge, SpinningEdge, 
                     Ten, Chi, Jin, Suiton, GustSlash, AeolianEdge, Kassatsu, SpinningEdge, GustSlash, AeolianEdge, TrickAttack, SpinningEdge, DreamWithinADream, 
                     Bhavacakra, Ten, Jin, HyoshoRanryu, Ten, Chi, Raiton, Ten, Chi, Raiton, FleetingRaiju, FleetingRaiju, GustSlash, ArmorCrush, SpinningEdge, GustSlash, AeolianEdge]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest39ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest39 = test("Ninja Timestamp estimate test 3", teTest39TestFunction, teTest39ValidationFunction)
    timerEstimateTestSuite.addTest(teTest39)

    def teTest40TestFunction() -> None:


        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 889, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra,
                     RisingPhoenix, RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, 
                     RisingPhoenix, TheForbiddenChakra, DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick,
                     TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish, DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, 
                     DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes, RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine,
                     TwinSnakes, Demolish, DragonKick, DragonKick, DragonKick]
        player = Player(actionSet, [], Stat, JobEnum.Monk)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DemolishDOTTimer, estimate["dotTimer"],
                player.DisciplinedFistTimer, estimate["buffTimer"]]

    def teTest40ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest40 = test("Monk DOT,buff and Timestamp estimate test 1", teTest40TestFunction, teTest40ValidationFunction)
    timerEstimateTestSuite.addTest(teTest40)

    def teTest41TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 889, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra,
                     RisingPhoenix, RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, 
                     RisingPhoenix, TheForbiddenChakra, DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick,
                     TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish, DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, 
                     DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes, RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine,
                     TwinSnakes, Demolish, DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick]
        player = Player(actionSet, [], Stat, JobEnum.Monk)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DemolishDOTTimer, estimate["dotTimer"],
                player.DisciplinedFistTimer, estimate["buffTimer"]]

    def teTest41ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest41 = test("Monk DOT,buff and Timestamp estimate test 2", teTest41TestFunction, teTest41ValidationFunction)
    timerEstimateTestSuite.addTest(teTest41)

    def teTest42TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [DragonKick, PerfectBalance, TwinSnakes, RiddleOfFire, Demolish, WaitAbility(1), Potion, Bootshine, Brotherhood, TheForbiddenChakra,
                     RisingPhoenix, RiddleOfWind, DragonKick, TheForbiddenChakra, PerfectBalance, Bootshine, SnapPunch, TheForbiddenChakra, TwinSnakes, 
                     RisingPhoenix, TheForbiddenChakra, DragonKick, TrueStrike, TheForbiddenChakra, Demolish, Bootshine, TwinSnakes, SnapPunch, DragonKick,
                     TrueStrike, SnapPunch, Bootshine, TwinSnakes, Demolish, DragonKick, TrueStrike, SnapPunch, TheForbiddenChakra, Bootshine, TwinSnakes, SnapPunch, 
                     DragonKick, TrueStrike, Demolish, Bootshine, TwinSnakes, RiddleOfFire, DragonKick, Bootshine, TheForbiddenChakra, DragonKick, ElixirField, Bootshine,
                     TwinSnakes, Demolish, DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick,DragonKick, DragonKick, DragonKick]
        player = Player(actionSet, [], Stat, JobEnum.Monk)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DemolishDOTTimer, estimate["dotTimer"],
                player.DisciplinedFistTimer, estimate["buffTimer"]]

    def teTest42ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest42 = test("Monk DOT,buff and Timestamp estimate test 3", teTest42TestFunction, teTest42ValidationFunction)
    timerEstimateTestSuite.addTest(teTest42)


    def teTest43TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, 
                     Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, 
                     Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, 
                     Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Shinten, Hakaze, Yukikaze, Shinten, Midare,
                     KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.HiganbanaTimer, estimate["dotTimer"],
                player.FugetsuTimer, estimate["buffTimer"]]

    def teTest43ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest43 = test("Samurai DOT,buff and Timestamp estimate test 1", teTest43TestFunction, teTest43ValidationFunction)
    timerEstimateTestSuite.addTest(teTest43)


    def teTest44TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, 
                     Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, 
                     Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, 
                     Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Higanbana, Shinten, Hakaze, Yukikaze, Shinten, Midare,
                     KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.HiganbanaTimer, estimate["dotTimer"],
                player.FugetsuTimer, estimate["buffTimer"]]

    def teTest44ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest44 = test("Samurai DOT,buff and Timestamp estimate test 2", teTest44TestFunction, teTest44ValidationFunction)
    timerEstimateTestSuite.addTest(teTest44)


    def teTest45TestFunction() -> None:


        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, 
                     Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, 
                     Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, 
                     Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Higanbana, Shinten, Hakaze, Yukikaze, Shinten, Midare,
                     KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha, WaitAbility(10), Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.HiganbanaTimer, estimate["dotTimer"],
                player.FugetsuTimer, estimate["buffTimer"]]

    def teTest45ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest45 = test("Samurai DOT,buff and Timestamp estimate test 3", teTest45TestFunction, teTest45ValidationFunction)
    timerEstimateTestSuite.addTest(teTest45)

    def teTest46TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 976, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, 
                     Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.HiganbanaTimer, estimate["dotTimer"],
                player.FugetsuTimer, estimate["buffTimer"]]

    def teTest46ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest46 = test("Samurai DOT,buff and Timestamp estimate test 4", teTest46TestFunction, teTest46ValidationFunction)
    timerEstimateTestSuite.addTest(teTest46)

    def teTest47TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2200, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko, WaitAbility(1), Potion, Kasha, Ikishoten, Yukikaze, Midare, KaeshiSetsugekka, Senei, Meikyo, Gekko, Shinten, 
                     Higanbana, Shinten, Gekko, Shinten, OgiNamikiri, Shoha, KaeshiNamikiri, Kasha, Shinten, Hakaze, Yukikaze, Midare, KaeshiSetsugekka, 
                     Shinten, Hakaze, Jinpu, Gekko, Shinten, Hakaze, Shifu, Kasha, Hakaze, Shinten, Yukikaze, Midare, Hakaze, Jinpu, Gekko, Hakaze, Shifu, 
                     Kasha, Shinten, Hakaze, Yukikaze, Shinten, Meikyo, Kasha, Kasha, Shinten, Shoha, Gekko, Higanbana, Shinten, Hakaze, Yukikaze, Shinten, Midare,
                     KaeshiSetsugekka, Hakaze, Yukikaze, Hakaze, Shinten, Shifu, Kasha, WaitAbility(10), Yukikaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.HiganbanaTimer, estimate["dotTimer"],
                player.FugetsuTimer, estimate["buffTimer"]]

    def teTest47ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest47 = test("Samurai DOT,buff and Timestamp estimate test 5", teTest47TestFunction, teTest47ValidationFunction)
    timerEstimateTestSuite.addTest(teTest47)

    def teTest48TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping, 
                     VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet, 
                     Gibbet, ShadowOfDeath, Slice]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DeathDesignTimer, estimate["buffTimer"]]

    def teTest48ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest48 = test("Reaper buff and Timestamp estimate test 1", teTest48TestFunction, teTest48ValidationFunction)
    timerEstimateTestSuite.addTest(teTest48)

    def teTest49TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping,
                     VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet,
                     Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows,
                     SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DeathDesignTimer, estimate["buffTimer"]]

    def teTest49ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest49 = test("Reaper buff and Timestamp estimate test 2", teTest49TestFunction, teTest49ValidationFunction)
    timerEstimateTestSuite.addTest(teTest49)

    def teTest50TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Soulsow, Harpe, ShadowOfDeath, ArcaneCircle, SoulSlice, SoulSlice, Potion, PlentifulHarvest, Enshroud, CrossReaping,
                     VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, Gluttony, Gibbet, Gallows, UnveiledGibbet,
                     Gibbet, ShadowOfDeath, Slice, WaxingSlice, InfernalSlice, Slice, WaxingSlice, InfernalSlice, UnveiledGallows, Gallows,
                     SoulSlice, UnveiledGibbet, Gibbet, Enshroud, CrossReaping, VoidReaping, LemureSlice, CrossReaping, VoidReaping, LemureSlice, Communio, HarvestMoon]
        player = Player(actionSet, [], Stat, JobEnum.Reaper)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DeathDesignTimer, estimate["buffTimer"]]

    def teTest50ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest50 = test("Reaper buff and Timestamp estimate test 3", teTest50TestFunction, teTest50ValidationFunction)
    timerEstimateTestSuite.addTest(teTest50)

    def teTest51TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
                     LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
                     HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
                     Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
                     Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
                     Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive, RaidenThrust, WyrmwindThrust, VorpalThrust, Nastrond, HeavenThrust,
                     FangAndClaw, WheelingThrust]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.PowerSurgeTimer, estimate["buffTimer"]]

    def teTest51ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest51 = test("Dragoon buff and Timestamp estimate test 1", teTest51TestFunction, teTest51ValidationFunction)
    timerEstimateTestSuite.addTest(teTest51)

    def teTest52TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
                     LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
                     HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
                     Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
                     Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
                     Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.PowerSurgeTimer, estimate["buffTimer"]]

    def teTest52ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest52 = test("Dragoon buff and Timestamp estimate test 2", teTest52TestFunction, teTest52ValidationFunction)
    timerEstimateTestSuite.addTest(teTest52)

    def teTest53TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2222, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        NINPlayer = Player([], [], Stat, JobEnum.Ninja)
        actionSet = [TrueThrust, Disembowel, LanceCharge, DragonSight(NINPlayer), ChaoticSpring, BattleLitany, Geirskogul, WheelingThrust, HighJump,
                     LifeSurge, FangAndClaw, DragonFireDive, SpineshafterDive, RaidenThrust, MirageDive, SpineshafterDive, VorpalThrust, LifeSurge,
                     HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust, Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw,
                     Geirskogul, RaidenThrust, HighJump, MirageDive, VorpalThrust, HeavenThrust, FangAndClaw, WheelingThrust, RaidenThrust, WyrmwindThrust,
                     Disembowel, ChaoticSpring, WheelingThrust, FangAndClaw, RaidenThrust, LanceCharge, VorpalThrust, LifeSurge, Geirskogul, HeavenThrust,
                     Nastrond, HighJump, FangAndClaw, Stardiver, WheelingThrust, MirageDive]
        player = Player(actionSet, [], Stat, JobEnum.Dragoon)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.PowerSurgeTimer, estimate["buffTimer"]]

    def teTest53ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest53 = test("Dragoon buff and Timestamp estimate test 3", teTest53TestFunction, teTest53ValidationFunction)
    timerEstimateTestSuite.addTest(teTest53)


    def teTest54TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 1200, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown,
                     RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, 
                     KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, 
                     WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel,KeenEdge, 
                     BrutalShell, NoMercy, RoughDivide, GnashingFang, JugularRip, DoubleDown, BlastingZone, RoughDivide, SavageClaw, AbdomenTear, 
                     WickedTalon, EyeGouge, SolidBarrel, BurstStrike, Hypervelocity, KeenEdge, BrutalShell, SolidBarrel]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest54ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest54 = test("Gunbreaker Timestamp estimate test 1", teTest54TestFunction, teTest54ValidationFunction)
    timerEstimateTestSuite.addTest(teTest54)

    def teTest55TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown,
                     RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, 
                     KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, 
                     WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, Hypervelocity]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest55ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest55 = test("Gunbreaker Timestamp estimate test 2", teTest55TestFunction, teTest55ValidationFunction)
    timerEstimateTestSuite.addTest(teTest55)


    def teTest56TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [KeenEdge, Potion, BrutalShell, NoMercy, Bloodfest, GnashingFang, JugularRip, SonicBreak, BowShock, BlastingZone, DoubleDown,
                     RoughDivide, SavageClaw, AbdomenTear, WickedTalon, EyeGouge, RoughDivide, SolidBarrel, BurstStrike, Hypervelocity, 
                     KeenEdge, BrutalShell, SolidBarrel, KeenEdge, BrutalShell, GnashingFang, JugularRip,SavageClaw, AbdomenTear, BlastingZone, 
                     WickedTalon, EyeGouge, SolidBarrel, KeenEdge, BrutalShell, SolidBarrel, Hypervelocity]
        player = Player(actionSet, [], Stat, JobEnum.Gunbreaker)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest56ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest56 = test("Gunbreaker Timestamp estimate test 3", teTest56TestFunction, teTest56ValidationFunction)
    timerEstimateTestSuite.addTest(teTest56)

    def teTest57TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, 
                     CircleScorn, Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, 
                     Atonement, FastBlade, RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, 
                     HolySpirit, RoyalAuthority, Atonement, Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, 
                     Confetti, BladeFaith, Intervene, BladeTruth, Intervene, BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest57ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest57 = test("Paladin Timestamp estimate test 1", teTest57TestFunction, teTest57ValidationFunction)
    timerEstimateTestSuite.addTest(teTest57)

    def teTest58TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 800, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HolySpirit, FastBlade, RiotBlade, WaitAbility(1), Potion, RoyalAuthority, FightOrFlight, RequestACat, GoringBlade, 
                     CircleScorn, Expiacion, Confetti, Intervene, BladeFaith, Intervene, BladeTruth, BladeValor, HolySpirit, Atonement, Atonement, 
                     Atonement, FastBlade, RiotBlade, RoyalAuthority, Atonement, CircleScorn, Expiacion, Atonement, Atonement, FastBlade, RiotBlade, 
                     HolySpirit, RoyalAuthority, Atonement, Atonement, Atonement, FastBlade, RiotBlade, FightOrFlight, RequestACat, GoringBlade, Expiacion, 
                     Confetti, BladeFaith, Intervene, BladeTruth, Intervene, BladeValor, HolySpirit, RoyalAuthority, HolySpirit, Atonement ]
        player = Player(actionSet, [], Stat, JobEnum.Paladin)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]

    def teTest58ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest58 = test("Paladin Timestamp estimate test 2", teTest58TestFunction, teTest58ValidationFunction)
    timerEstimateTestSuite.addTest(teTest58)

    def teTest59TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        DRKPlayer = Player([], [], Stat, JobEnum.DarkKnight)
        actionSet = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
            HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
			SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
			Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
			Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DarksideTimer, estimate['buffTimer']]

    def teTest59ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest59 = test("Darkknight buff and Timestamp estimate test 1", teTest59TestFunction, teTest59ValidationFunction)
    timerEstimateTestSuite.addTest(teTest59)

    def teTest60TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        DRKPlayer = Player([], [], Stat, JobEnum.DarkKnight)
        actionSet = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
            HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
			SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, HardSlash, HardSlash, HardSlash, HardSlash, HardSlash, HardSlash]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], 2.5, estimate["untilNextGCD"], player.DarksideTimer, estimate['buffTimer']]
         # Hardcodes a 2.5 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest60ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest60 = test("Darkknight buff and Timestamp estimate test 2", teTest60TestFunction, teTest60ValidationFunction)
    timerEstimateTestSuite.addTest(teTest60)

    def teTest61TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 3000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        DRKPlayer = Player([], [], Stat, JobEnum.DarkKnight)
        actionSet = [BloodWeapon,WaitAbility(5),TBN(DRKPlayer), HardSlash, EdgeShadow, Delirium, SyphonStrike, WaitAbility(1), Potion, Souleater, LivingShadow, SaltedEarth, 
            HardSlash, Shadowbringer, EdgeShadow, Bloodspiller, EdgeShadow, CarveSpit, Bloodspiller, Plunge, EdgeShadow, Bloodspiller, SaltDarkness, Shadowbringer, 
			SyphonStrike, EdgeShadow, Plunge,Souleater, HardSlash, SyphonStrike, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, SyphonStrike, 
			Plunge, Souleater, Bloodspiller, HardSlash, SyphonStrike, Souleater, HardSlash, BloodWeapon, SyphonStrike, Delirium, Bloodspiller, Bloodspiller, EdgeShadow, 
			Bloodspiller, Bloodspiller, CarveSpit, Souleater, EdgeShadow, HardSlash ]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], player.DarksideTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest61ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest61 = test("Darkknight buff and Timestamp estimate test 3 ", teTest61TestFunction, teTest61ValidationFunction)
    timerEstimateTestSuite.addTest(teTest61)

    def teTest65TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HardSlash, EdgeShadow, HardSlash, HardSlash]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer,estimate["untilNextGCD"], player.DarksideTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest65ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest65 = test("DarkKnight buff and Timestamp estimate test 4 ", teTest65TestFunction, teTest65ValidationFunction)
    timerEstimateTestSuite.addTest(teTest65)

    def teTest66TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [EdgeShadow, HardSlash, HardSlash]
        player = Player(actionSet, [], Stat, JobEnum.DarkKnight)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer,estimate["untilNextGCD"], player.DarksideTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest66ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest66 = test("DarkKnight buff and Timestamp estimate test 5 ", teTest66TestFunction, teTest66ValidationFunction)
    timerEstimateTestSuite.addTest(teTest66)

    def teTest62TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                                 FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                                 HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                                 FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer,estimate["untilNextGCD"], player.SurgingTempestTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest62ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest62 = test("Warrior buff and Timestamp estimate test 1 ", teTest62TestFunction, teTest62ValidationFunction)
    timerEstimateTestSuite.addTest(teTest62)

    def teTest63TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Tomahawk, Infuriate, HeavySwing, Upheaval ,Maim, WaitAbility(1), Potion, StormEye, InnerRelease, Onslaught, InnerChaos, Onslaught, PrimalRend,Onslaught, 
                                 FellCleave, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath, FellCleave, Infuriate, Upheaval, InnerChaos, HeavySwing, Maim, StormEye, 
                                 HeavySwing, Maim, StormPath, FellCleave, HeavySwing, Maim, Onslaught, StormEye , HeavySwing, Upheaval, Maim, StormPath, InnerRelease, PrimalRend, FellCleave, 
                                 FellCleave, Onslaught, FellCleave, FellCleave, Infuriate, InnerChaos, HeavySwing, Maim, StormPath]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer,estimate["untilNextGCD"], player.SurgingTempestTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest63ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest63 = test("Warrior buff and Timestamp estimate test 2 ", teTest63TestFunction, teTest63ValidationFunction)
    timerEstimateTestSuite.addTest(teTest63)


    def teTest64TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Tomahawk, InnerRelease, Maim, Maim]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer,estimate["untilNextGCD"], player.SurgingTempestTimer, estimate['buffTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest64ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest64 = test("Warrior buff and Timestamp estimate test 3 ", teTest64TestFunction, teTest64ValidationFunction)
    timerEstimateTestSuite.addTest(teTest64)


    def teTest67TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, 
                     BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, 
                     BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, 
                     RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], max(player.StormbiteDOTTimer, player.CausticbiteDOTTimer), estimate['dotTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest67ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest67 = test("Bard DOTand Timestamp estimate test 1 ", teTest67TestFunction, teTest67ValidationFunction)
    timerEstimateTestSuite.addTest(teTest67)


    def teTest68TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, 
                     BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, IronJaws, RefulgentArrow, BurstShot, EmpyrealArrow, 
                     BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, 
                     RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, IronJaws,RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], max(player.StormbiteDOTTimer, player.CausticbiteDOTTimer), estimate['dotTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest68ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest68 = test("Bard DOTand Timestamp estimate test 2 ", teTest68TestFunction, teTest68ValidationFunction)
    timerEstimateTestSuite.addTest(teTest68)

    def teTest69TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, WaitAbility(40), EmpyrealArrow]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], max(player.StormbiteDOTTimer, player.CausticbiteDOTTimer), estimate['dotTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest69ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest69 = test("Bard DOTand Timestamp estimate test 3 ", teTest69TestFunction, teTest69ValidationFunction)
    timerEstimateTestSuite.addTest(teTest69)

    def teTest70TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Stormbite, WanderingMinuet, RagingStrike, Causticbite, EmpyrealArrow, WaitAbility(40), EmpyrealArrow, IronJaws, BlastArrow,
                     BlastArrow, BlastArrow, ArmyPaeon, BlastArrow, BlastArrow, BlastArrow, BlastArrow, BlastArrow, BlastArrow, BlastArrow, BlastArrow, BlastArrow]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], max(player.StormbiteDOTTimer, player.CausticbiteDOTTimer), estimate['dotTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest70ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],5)
            # Hardcoded 5 because ArmyPaeon on Bard is a really big difference
        return passed , testResults

    teTest70 = test("Bard DOTand Timestamp estimate test 4 (< 5)", teTest70TestFunction, teTest70ValidationFunction)
    timerEstimateTestSuite.addTest(teTest70)

    def teTest71TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Stormbite, ArmyPaeon, RagingStrike, Causticbite, EmpyrealArrow, BloodLetter, RefulgentArrow, RadiantFinale, 
                     BattleVoice, BurstShot, Barrage, RefulgentArrow, Sidewinder, BurstShot, RefulgentArrow, BurstShot, EmpyrealArrow, 
                     BurstShot, PitchPerfect3, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, 
                     RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow, BurstShot, RefulgentArrow,
                     BurstShot, RefulgentArrow,BurstShot, RefulgentArrow,BurstShot, RefulgentArrow,BurstShot, RefulgentArrow,BurstShot, RefulgentArrow]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"], max(player.StormbiteDOTTimer, player.CausticbiteDOTTimer), estimate['dotTimer']]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest71ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],5)
            # Hardcoded 5 because ArmyPaeon on Bard is a really big difference
        return passed , testResults

    teTest71 = test("Bard DOTand Timestamp estimate test 5 (< 5)", teTest71TestFunction, teTest71ValidationFunction)
    timerEstimateTestSuite.addTest(teTest71)

    def teTest72TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
			Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
			HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot, SplitShot, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			Automaton, CleanShot, SplitShot, SlugShot, CleanShot, Drill, SplitShot, Hypercharge, HeatBlast, GaussRound, HeatBlast, Ricochet, HeatBlast, 
			GaussRound, HeatBlast, Ricochet, HeatBlast, Reassemble, ChainSaw, GaussRound, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest72ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest72 = test("Machinist and Timestamp estimate test 1", teTest72TestFunction, teTest72ValidationFunction)
    timerEstimateTestSuite.addTest(teTest72)

    def teTest73TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 479, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
			Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
			HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest73ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest73 = test("Machinist Timestamp estimate test 2", teTest73TestFunction, teTest73ValidationFunction)
    timerEstimateTestSuite.addTest(teTest73)

    def teTest74TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Reassemble, WaitAbility(5), AirAnchor, GaussRound, Ricochet, Drill, BarrelStabilizer, SplitShot, SlugShot, GaussRound, Ricochet, CleanShot, 
			Reassemble, WaitAbility(2.2), Wildfire, ChainSaw, Automaton,Hypercharge, HeatBlast, Ricochet, HeatBlast, GaussRound, HeatBlast, Ricochet, 
			HeatBlast, GaussRound, HeatBlast, Ricochet, Drill, GaussRound, Ricochet, SplitShot, Ricochet, SlugShot, CleanShot, SplitShot, SlugShot, 
			CleanShot, SplitShot,  AirAnchor, Drill, SlugShot, CleanShot]
        player = Player(actionSet, [], Stat, JobEnum.Machinist)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest74ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest74 = test("Machinist Timestamp estimate test 3", teTest74TestFunction, teTest74ValidationFunction)
    timerEstimateTestSuite.addTest(teTest74)

    def teTest75TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite,
                    TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, 
                    Jete, Pirouette, StandardFinish, Cascade, SaberDance, ReverseCascade, Fountain, FountainFall, Cascade, SaberDance, ReverseCascade, 
                    Fountain, FountainFall, Cascade, ReverseCascade, StandardStep, Emboite, Jete, StandardFinish, SaberDance, Fountain, Cascade, Fountain, 
                    FountainFall, Flourish, FanDance3, SaberDance, FanDance4, FountainFall, ReverseCascade, FanDance1, FanDance3, Cascade, ReverseCascade, 
                    Fountain, FountainFall]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest75ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest75 = test("Dancer Timestamp estimate test 1", teTest75TestFunction, teTest75ValidationFunction)
    timerEstimateTestSuite.addTest(teTest75)

    def teTest76TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [StandardStep, Pirouette, Jete, StandardFinish, TechnicalStep, Pirouette, Jete, Entrechat, Emboite,
                    TechnicalFinish, Devilment, StarfallDance, Flourish, FanDance3, Tillana, FanDance4, FountainFall, FanDance1, FanDance3, StandardStep, 
                    Jete, Pirouette, StandardFinish]
        player = Player(actionSet, [], Stat, JobEnum.Dancer)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.GCDLockTimer, estimate["untilNextGCD"]]
         # Hardcodes a 0 for untilNextGCD since livingshadow furthers the fight. So the until next GCD the estimate returns is right after the DRK finishes, not after living shadow finishes

    def teTest76ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest76 = test("Dancer Timestamp estimate test 2", teTest76TestFunction, teTest76ValidationFunction)
    timerEstimateTestSuite.addTest(teTest76)

    def teTest77TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Hakaze,Meikyo, Gekko, Hakaze]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.FugetsuTimer, estimate["buffTimer"]]

    def teTest77ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest77 = test("Samurai additional test 1", teTest77TestFunction, teTest77ValidationFunction)
    timerEstimateTestSuite.addTest(teTest77)

    def teTest78TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Meikyo, Gekko]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.FugetsuTimer, estimate["buffTimer"]]
    

    def teTest78ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest78 = test("Samurai additional test 2", teTest78TestFunction, teTest78ValidationFunction)
    timerEstimateTestSuite.addTest(teTest78)

    def teTest79TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Gekko, Meikyo, Gekko]
        player = Player(actionSet, [], Stat, JobEnum.Samurai)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"], player.FugetsuTimer, estimate["buffTimer"]]
         
    def teTest79ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest79 = test("Samurai additional test 3", teTest79TestFunction, teTest79ValidationFunction)
    timerEstimateTestSuite.addTest(teTest79)

    def teTest80TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [0, estimate["currentTimeStamp"]]
    # Hardcoded value of 0 since we want the estimate to be 0 since it will start when the lb applies damage
         
    def teTest80ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest80 = test("Limit Break additional test 1", teTest80TestFunction, teTest80ValidationFunction)
    timerEstimateTestSuite.addTest(teTest80)

    def teTest81TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Xenoglossy,CasterLB3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"]]
         
    def teTest81ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest81 = test("Limit Break additional test 2", teTest81TestFunction, teTest81ValidationFunction)
    timerEstimateTestSuite.addTest(teTest81)

    def teTest82TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Xenoglossy,CasterLB3, Blizzard3, Fire3, Fire4, Fire4, Fire4, CasterLB2]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"]]
         
    def teTest82ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest82 = test("Limit Break additional test 3", teTest82TestFunction, teTest82ValidationFunction)
    timerEstimateTestSuite.addTest(teTest82)

    def teTest83TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [Xenoglossy,CasterLB3, Blizzard3, Fire3, Fire4, Fire4, Fire4, CasterLB2, Fire3, Fire4, Fire4, CasterLB1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        estimate = player.computeTimeStamp()
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [Event.TimeStamp, estimate["currentTimeStamp"]]
         
    def teTest83ValidationFunction(testResults) -> (bool, list):
        passed = True   
        for i in range(0,len(testResults),2): 
            passed = passed and isClose(testResults[i],testResults[i+1],errorAmount)

        return passed , testResults

    teTest83 = test("Limit Break additional test 4", teTest83TestFunction, teTest83ValidationFunction)
    timerEstimateTestSuite.addTest(teTest83)

    return timerEstimateTestSuite

######################################
#         Limit break test           #
######################################

def generateLimitBreakTestSuite():

    lbTestSuite = testSuite("Limit Break test suite")

    def lbTest1TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest1ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.1,5.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest1 = test("Limit Break casting/recasting time test 1 - CasterLB1", lbTest1TestFunction, lbTest1ValidationFunction)
    lbTestSuite.addTest(lbTest1)

    def lbTest2TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 12321, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB1]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest2ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.1,5.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest2 = test("Limit Break casting/recasting time test 2 - CasterLB1", lbTest2TestFunction, lbTest2ValidationFunction)
    lbTestSuite.addTest(lbTest2)

    def lbTest3TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB2]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest3ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.1,8.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest3 = test("Limit Break casting/recasting time test 3 - CasterLB2", lbTest3TestFunction, lbTest3ValidationFunction)
    lbTestSuite.addTest(lbTest3)

    def lbTest4TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB2]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest4ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.1,8.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest4 = test("Limit Break casting/recasting time test 4 - CasterLB2", lbTest4TestFunction, lbTest4ValidationFunction)
    lbTestSuite.addTest(lbTest4)

    def lbTest5TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest5ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [12.6,12.6]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest5 = test("Limit Break casting/recasting time test 5 - CasterLB3", lbTest5TestFunction, lbTest5ValidationFunction)
    lbTestSuite.addTest(lbTest5)

    def lbTest6TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [CasterLB3]
        player = Player(actionSet, [], Stat, JobEnum.BlackMage)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest6ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [12.6,12.6]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest6 = test("Limit Break casting/recasting time test 6 - CasterLB3", lbTest6TestFunction, lbTest6ValidationFunction)
    lbTestSuite.addTest(lbTest6)


    def lbTest7TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB1]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest7ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.86,5.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest7 = test("Limit Break casting/recasting time test 7 - MeleeLB1", lbTest7TestFunction, lbTest7ValidationFunction)
    lbTestSuite.addTest(lbTest7)

    def lbTest8TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 12321, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB1]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest8ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.86,5.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest8 = test("Limit Break casting/recasting time test 8 - MeleeLB1", lbTest8TestFunction, lbTest8ValidationFunction)
    lbTestSuite.addTest(lbTest8)

    def lbTest9TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest9ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [6.86,6.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest9 = test("Limit Break casting/recasting time test 9 - MeleeLB2", lbTest9TestFunction, lbTest9ValidationFunction)
    lbTestSuite.addTest(lbTest9)

    def lbTest10TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB2]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest10ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [6.86,6.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest10 = test("Limit Break casting/recasting time test 10 - MeleeLB2", lbTest10TestFunction, lbTest10ValidationFunction)
    lbTestSuite.addTest(lbTest10)

    def lbTest11TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB3]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest11ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.20,8.20]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest11 = test("Limit Break casting/recasting time test 11 - MeleeLB3", lbTest11TestFunction, lbTest11ValidationFunction)
    lbTestSuite.addTest(lbTest11)

    def lbTest12TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [MeleeLB3]
        player = Player(actionSet, [], Stat, JobEnum.Ninja)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest12ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.20,8.20]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest12 = test("Limit Break casting/recasting time test 12 - MeleeLB3", lbTest12TestFunction, lbTest12ValidationFunction)
    lbTestSuite.addTest(lbTest12)

    def lbTest13TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB1]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest13ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [1.93,1.93]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest13 = test("Limit Break casting/recasting time test 13 - TankLB1", lbTest13TestFunction, lbTest13ValidationFunction)
    lbTestSuite.addTest(lbTest13)

    def lbTest14TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 12321, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB1]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest14ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [1.93,1.93]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest14 = test("Limit Break casting/recasting time test 14 - TankLB1", lbTest14TestFunction, lbTest14ValidationFunction)
    lbTestSuite.addTest(lbTest14)

    def lbTest15TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB2]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest15ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [3.86,3.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest15 = test("Limit Break casting/recasting time test 15 - TankLB2", lbTest15TestFunction, lbTest15ValidationFunction)
    lbTestSuite.addTest(lbTest15)

    def lbTest16TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB2]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest16ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [3.86,3.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest16 = test("Limit Break casting/recasting time test 16 - TankLB2", lbTest16TestFunction, lbTest16ValidationFunction)
    lbTestSuite.addTest(lbTest16)

    def lbTest17TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB3]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest17ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [3.86,3.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest17 = test("Limit Break casting/recasting time test 17 - TankLB3", lbTest17TestFunction, lbTest17ValidationFunction)
    lbTestSuite.addTest(lbTest17)

    def lbTest18TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [TankLB3]
        player = Player(actionSet, [], Stat, JobEnum.Warrior)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest18ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [3.86,3.86]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest18 = test("Limit Break casting/recasting time test 18 - TankLB3", lbTest18TestFunction, lbTest18ValidationFunction)
    lbTestSuite.addTest(lbTest18)

    def lbTest19TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB1]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest19ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [4.1,4.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest19 = test("Limit Break casting/recasting time test 19 - HealerLB1", lbTest19TestFunction, lbTest19ValidationFunction)
    lbTestSuite.addTest(lbTest19)

    def lbTest20TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 12321, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB1]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest20ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [4.1,4.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest20 = test("Limit Break casting/recasting time test 20 - HealerLB1", lbTest20TestFunction, lbTest20ValidationFunction)
    lbTestSuite.addTest(lbTest20)

    def lbTest21TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB2]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest21ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [7.13,7.13]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest21 = test("Limit Break casting/recasting time test 21 - HealerLB2", lbTest21TestFunction, lbTest21ValidationFunction)
    lbTestSuite.addTest(lbTest21)

    def lbTest22TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB2]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest22ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [7.13,7.13]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest22 = test("Limit Break casting/recasting time test 22 - HealerLB2", lbTest22TestFunction, lbTest22ValidationFunction)
    lbTestSuite.addTest(lbTest22)

    def lbTest23TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB3]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest23ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [10.10,10.10]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest23 = test("Limit Break casting/recasting time test 23 - HealerLB3", lbTest23TestFunction, lbTest23ValidationFunction)
    lbTestSuite.addTest(lbTest23)

    def lbTest24TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [HealerLB3]
        player = Player(actionSet, [], Stat, JobEnum.Scholar)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest24ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [10.10,10.10]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest24 = test("Limit Break casting/recasting time test 24 - HealerLB3", lbTest24TestFunction, lbTest24ValidationFunction)
    lbTestSuite.addTest(lbTest24)

    def lbTest25TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB1]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest25ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.1,5.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest25 = test("Limit Break casting/recasting time test 25 - RangedLB1", lbTest25TestFunction, lbTest25ValidationFunction)
    lbTestSuite.addTest(lbTest25)

    def lbTest26TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 12321, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB1]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest26ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [5.1,5.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest26 = test("Limit Break casting/recasting time test 26 - RangedLB1", lbTest26TestFunction, lbTest26ValidationFunction)
    lbTestSuite.addTest(lbTest26)

    def lbTest27TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB2]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest27ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [6.1,6.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest27 = test("Limit Break casting/recasting time test 27 - RangedLB2", lbTest27TestFunction, lbTest27ValidationFunction)
    lbTestSuite.addTest(lbTest27)

    def lbTest28TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB2]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest28ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [6.1,6.1]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest28 = test("Limit Break casting/recasting time test 28 - RangedLB2", lbTest28TestFunction, lbTest28ValidationFunction)
    lbTestSuite.addTest(lbTest28)

    def lbTest29TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 436, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB3]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest29ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.20,8.20]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest29 = test("Limit Break casting/recasting time test 29 - RangedLB3", lbTest29TestFunction, lbTest29ValidationFunction)
    lbTestSuite.addTest(lbTest29)

    def lbTest30TestFunction() -> None:

        Dummy = Enemy()
        Event = Fight(Dummy, False)

        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 9999, 'SkS': 9999, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        actionSet = [RangedLB3]
        player = Player(actionSet, [], Stat, JobEnum.Bard)

        Event.AddPlayer([player])

        Event.RequirementOn = False
        Event.ShowGraph = False
        Event.IgnoreMana = True

        
        Event.SimulateFight(0.01, 500, False, PPSGraph=False, showProgress=False,computeGraph=False)

        return [player.CastingSpell.CastTime,player.CastingSpell.RecastTime]
         
    def lbTest30ValidationFunction(testResults) -> (bool, list):
        passed = True   

        expected = [8.20,8.20]

        for index in range(len(testResults)): 
            passed = passed and testResults[index] == expected[index]

        return passed , expected

    lbTest30 = test("Limit Break casting/recasting time test 30 - RangedLB3", lbTest30TestFunction, lbTest30ValidationFunction)
    lbTestSuite.addTest(lbTest30)


    return lbTestSuite

######################################
#            FFLogs test             #
######################################

# This will check that the created fight's player have the correct action set.
# Will only check up to around 2:30 of the fight as this is around when the rotation should begin anew.


def generateFFLogsTestSuite():
    
    fflogTestSuite = testSuite("FFLogs test suite.")
    from ffxivcalc.Request.FFLogs_api import getSingleFightData
    import os
    os.environ["FFLOGS_CLIENT_ID"] = "9b8e6c18-39d6-4ae0-91c7-e9221e699769"
    os.environ["FFLOGS_CLIENT_SECRET"] = "u0j8e1aIygCejB6HiBJFJcr0RB1MSIkVkLdgxDox"
    # TODO Check new name for enkindle/summon phoenix doesn't fuck with anything in app (icon name)

    logging.getLogger("urllib3").level = logging.ERROR
    def ffTest1TestFunction() -> None:

        data = getSingleFightData("", "", "RQwfx3vATFWGahJc", "8")
        ffLogFight = RestoreFightObject(data)

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.CasterActions, ActionEnum.BlackMageActions) 
            for action in ffLogFight.PlayerList[6].ActionSet
        ]

    def ffTest1ValidationFunction(testResults) -> (bool, list):
        passed = True

        blmActionName = ['Sharpcast','FireIII', 'ThunderIII', 'FireIV', 'Triplecast', 'FireIV', 'Amplifier', 'LeyLines', 'FireIV', 'Potion', 'FireIV', 'Sharpcast', 'Triplecast', 'Despair', 'Manafont', 'FireIV', 'Swiftcast', 'Despair',
                         'Transpose','Paradox','Xenoglossy','ThunderIII','Transpose','FireIII','FireIV','FireIV','FireIV','Despair','BlizzardIII','BlizzardIV','Paradox','Sharpcast','FireIII','FireIV','FireIV','ThunderIII', 'Sharpcast', 'FireIV','Paradox','FireIV','FireIV','FireIV','Despair','Xenoglossy','Transpose',
                         'Paradox','Sharpcast','ThunderIII','Swiftcast','Transpose','FireIII','FireIV','FireIV','FireIV','Despair','BlizzardIII','BlizzardIV','Paradox','Manaward','FireIII','Sharpcast', 'FireIV', 'FireIV', 'ThunderIII', 'FireIV', 'Paradox', 'FireIV', 'Xenoglossy', 'Triplecast', 'FireIV', 'FireIV', 'Despair',
                          'Transpose', 'Paradox', 'LucidDreaming', 'Xenoglossy', 'Amplifier', 'Xenoglossy','Surecast', 'Sharpcast', 'ThunderIII', 'Transpose', 'Swiftcast', 'FireIII', 'Triplecast', 'FireIV', 'FireIV', 'LeyLines', 'FireIV', 'Despair', 'Xenoglossy', 'Manafont', 'FireIV', 'Despair', 'BlizzardIII', 'Paradox', 'BlizzardIV', 'FireIII']
        failedTest = []
        for i in range(0,len(blmActionName)): 
            if blmActionName[i] != testResults[i]:
                passed = False
                failedTest.append((i, blmActionName[i], testResults[i]))

        return passed , failedTest

    ffTest1 = test("FFLogs test 1 - Blackmage test : (RQwfx3vATFWGahJc,8)", ffTest1TestFunction, ffTest1ValidationFunction)
    fflogTestSuite.addTest(ffTest1)

    def ffTest2TestFunction() -> None:

        data = getSingleFightData("", "", "bzfjTDV7gBGx1Y3m", "10")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.BlackMage
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.CasterActions, ActionEnum.BlackMageActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest2ValidationFunction(testResults) -> (bool, list):
        passed = True

        blmActionName = ['LeyLines', 'Sharpcast', 'FireIII','ThunderIII', 'FireIV', 'Triplecast','FireIV','Sharpcast','Amplifier','FireIV','Swiftcast','LucidDreaming','FireIV','Manaward','Addle','Despair','Manafont','Triplecast',
                         'FireIV','Despair','Transpose','Paradox','Xenoglossy','ThunderIII','Transpose','FireIII','Sharpcast','FireIV','FireIV','FireIV','Despair','BlizzardIII','BlizzardIV','Paradox','FireIII','FireIV','FireIV',
                         'ThunderIII','Sharpcast','FireIV','Paradox','FireIV','FireIV','FireIV','Xenoglossy','Swiftcast','Despair','Transpose','Paradox','Sharpcast','ThunderIII','Transpose','FireIII','FireIV','FireIV','Triplecast','FireIV','FireIV','Despair','BlizzardIII',
                         'BlizzardIV','Paradox','Sharpcast','FireIII','FireIV','ThunderIII','Potion','FireIV','FireIV','Paradox','Xenoglossy','LeyLines','FireIV','FireIV','FireIV','Despair','Xenoglossy','Amplifier','LucidDreaming','Xenoglossy',
                         'Manafont','Sharpcast','FireIV','Xenoglossy','Swiftcast','Despair','Transpose','ThunderIII','Paradox', 'Triplecast', 'Transpose', 'FireIII', 'FireIV', 'FireIV', 'FireIV', 'Despair']
        failedTest = []
        for i in range(0,len(blmActionName)): 
            if blmActionName[i] != testResults[i]:
                passed = False
                failedTest.append((i, blmActionName[i], testResults[i]))

        return passed , failedTest

    ffTest2 = test("FFLogs test 2 - Blackmage test : (bzfjTDV7gBGx1Y3m,10)", ffTest2TestFunction, ffTest2ValidationFunction)
    fflogTestSuite.addTest(ffTest2)

    def ffTest3TestFunction() -> None:

        data = getSingleFightData("", "", "Mkj7gynfpDBGHacW", "5")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.RedMage
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.CasterActions, ActionEnum.RedMageActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest3ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions = ['Verthunder','Verareo','Acceleration','Swiftcast','Verthunder','Fleche','Contre','Verthunder','Embolden','Manafication','EnchantedRiposte','Engagement','EnchantedZwerchhau','Corps','EnchantedRedoublement','Corps','Engagement','Verholy','LucidDreaming','Scorch','Resolution','Addle','Verfire','Verthunder','Verstone','Verareo','Fleche','Jolt','Verareo',
                        'Jolt','Verthunder','Contre','Jolt','Verareo','Engagement','Jolt','Verthunder','Corps','Jolt','Verareo','Fleche','Acceleration','Verthunder','Verstone','Verareo','EnchantedRiposte','EnchantedZwerchhau','EnchantedRedoublement',
                        'Verflare','Scorch','Resolution','Contre','Verstone','Verareo','Fleche','Verfire','Verthunder','Engagement','Verstone','Verareo','LucidDreaming','Verfire','Verthunder','Verstone','Verthunder',
                        'Corps','Verfire','Verareo','Fleche','Acceleration','Verareo','Swiftcast','Verthunder','Contre','Verstone','Verareo','EnchantedRiposte','EnchantedZwerchhau','EnchantedRedoublement','Manafication','Verflare',
                        'Potion','Scorch','Resolution','Embolden','Engagement','EnchantedRiposte','Fleche','EnchantedZwerchhau','Corps','EnchantedRedoublement','Verholy','Scorch','Resolution','EnchantedRiposte','EnchantedZwerchhau','EnchantedRedoublement',
                        'Contre','Verflare','Scorch','Resolution','Acceleration','Verareo','Fleche']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest3 = test("FFLogs test 3 - Redmage test : (Mkj7gynfpDBGHacW,5)", ffTest3TestFunction, ffTest3ValidationFunction)
    fflogTestSuite.addTest(ffTest3)

    def ffTest4TestFunction() -> None:

        data = getSingleFightData("", "", "YbDaH9C6dNVJAh8T", "67")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Summoner
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.CasterActions, ActionEnum.SummonerActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest4ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions = ['RuinIII','SummonBahamut','SearingLight','AstralImpulse','Potion','AstralImpulse','EnergyDrain','AstralImpulse','Fester','AstralImpulse','EnkindleBahamut','Deathflare','AstralImpulse','Fester', 'LucidDreaming','AstralImpulse','Titan','Topaz','Mountain',
                            'Topaz','Mountain','Topaz','Mountain','Topaz','Mountain','Garuda','Swiftcast','Slipstream','Emerald','Emerald','Emerald','Emerald','Ifrit','Ruby','Ruby','Cyclone','Strike','RuinIII','RuinIV','SummonPhoenix','FountainOfFire','FountainOfFire','EnergyDrain','FountainOfFire','EnkindlePhoenix','FountainOfFire','Rekindle',
                            'FountainOfFire','FountainOfFire','LucidDreaming']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest4 = test("FFLogs test 4 - Summoner test : (YbDaH9C6dNVJAh8T,67)", ffTest4TestFunction, ffTest4ValidationFunction)
    fflogTestSuite.addTest(ffTest4)

    def ffTest5TestFunction() -> None:

        data = getSingleFightData("", "", "ytpwWPVGd8ZfzgTD", "18")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Scholar
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.HealerActions, ActionEnum.ScholarActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest5ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Potion','BroilIV','Biolysis', 'Dissipation','BroilIV','Swiftcast','BroilIV','ChainStratagem','EnergyDrain',
                            'BroilIV','EnergyDrain','BroilIV','EnergyDrain','BroilIV','Aetherflow','BroilIV','EnergyDrain','BroilIV','EnergyDrain','Biolysis','EnergyDrain','LucidDreaming',
                            'BroilIV','BroilIV','BroilIV','BroilIV','BroilIV','BroilIV','BroilIV','BroilIV','Protraction','BroilIV','BroilIV',
                            'BroilIV','Biolysis','BroilIV','BroilIV','BroilIV','BroilIV','SummonSeraph','BroilIV','Consolation','BroilIV','BroilIV','BroilIV',
                            'Consolation', 'BroilIV', 'WhisperingDawn', 'BroilIV', 'Aetherflow', 'BroilIV', 'Biolysis', 'BroilIV', 'BroilIV',
                            'FeyBlessing', 'BroilIV', 'LucidDreaming', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'Biolysis',
                            'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'BroilIV', 'FeyIllumination', 'BroilIV', 'ChainStratagem', 
                            'BroilIV', 'EnergyDrain', 'BroilIV', 'EnergyDrain', 'BroilIV', 'EnergyDrain', 'Biolysis', 'Aetherflow','EnergyDrain','BroilIV','EnergyDrain','BroilIV','EnergyDrain','BroilIV',
                            'BroilIV','Expedient','BroilIV','LucidDreaming','BroilIV']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest5 = test("FFLogs test 5 - Scholar test : (ytpwWPVGd8ZfzgTD,18)", ffTest5TestFunction, ffTest5ValidationFunction)
    fflogTestSuite.addTest(ffTest5)

    def ffTest6TestFunction() -> None:

        data = getSingleFightData("", "", "Mk4ZR1KGQjBnJYmN", "2")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.WhiteMage
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.HealerActions, ActionEnum.WhiteMageActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest6ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Glare','Dia','Potion','Glare','Temperance','Glare','PresenceOfMind','Glare','Assize','Glare','LucidDreaming',
                            'Glare','Asylum','Glare','ThinAir','Glare','Glare','Glare','Glare','Glare','Glare','Glare','Dia','AfflatusRapture','Glare','Glare',
                            'ThinAir','Glare','Glare','Glare','Glare','Assize','Glare','Glare','Glare','DivineBenison','Glare','Dia',
                            'Glare','Glare','Bell','Glare','PlenaryIndulgence','AfflatusRapture','Glare','LucidDreaming','Glare','Glare','Glare','Glare','Glare','Glare',
                            'Dia','Assize','Glare','ThinAir','AfflatusRapture','AfflatusMisery','Glare','Glare','Asylum','AfflatusRapture','Glare',
                            'Glare','Glare','Glare','Glare','Dia','Glare','AfflatusRapture','Glare','PresenceOfMind',
                            'AfflatusRapture','AfflatusMisery','Assize','Glare','Glare','LucidDreaming','Glare','Glare','Glare']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest6 = test("FFLogs test 6 - Whitemage test : (Mk4ZR1KGQjBnJYmN,2)", ffTest6TestFunction, ffTest6ValidationFunction)
    fflogTestSuite.addTest(ffTest6)

    def ffTest7TestFunction() -> None:

        data = getSingleFightData("", "", "N2WfcJa8hnG9FL4k", "5")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Sage
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.HealerActions, ActionEnum.SageActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest7ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Potion', 'Dosis','Eukrasia','EukrasianDosis','Dosis','LucidDreaming','Dosis','Phlegma','Kerachole','Phlegma',
                            'Dosis','Physis','Dosis','Dosis','Dosis','Dosis','Dosis','Dosis','Eukrasia','EukrasianDosis','Dosis','Dosis','Dosis','Dosis','Dosis','Haima',
                            'Dosis','Dosis','Dosis','Taurochole','Dosis','Dosis','Dosis','Panhaima','Eukrasia','EukrasianDosis','Dosis','Dosis','LucidDreaming','Dosis',
                            'Ixochole','Dosis','Kerachole','Dosis','Dosis','Toxikon','Dosis','Dosis','Phlegma','Dosis','Eukrasia','EukrasianDosis','Dosis','Dosis','Swiftcast','Pneuma',
                            'Dosis','Dosis','Dosis','Dosis','Dosis','Dosis','Kerachole','Dosis','Dosis','Eukrasia','EukrasianDosis','Dosis','Physis','Dosis','Dosis','Dosis','LucidDreaming',
                            'Dosis','Taurochole','Phlegma','Phlegma','Dosis','Dosis','Kerachole','Dosis']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest7 = test("FFLogs test 7 - Sage test : (N2WfcJa8hnG9FL4k,5)", ffTest7TestFunction, ffTest7ValidationFunction)
    fflogTestSuite.addTest(ffTest7)

    def ffTest8TestFunction() -> None:

        data = getSingleFightData("", "", "L2tQ41WZCPbYa7wX", "2")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Astrologian
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.HealerActions, ActionEnum.AstrologianActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest8ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Potion','EarthlyStar','Draw','Malefic','Lightspeed', 'Combust','Balance','Draw','Malefic','MinorArcana','Ewer','Malefic','Divination',
                            'Draw','Malefic','Spear','Astrodyne','Malefic','LordOfCrown','Malefic','StellarDetonation','Malefic','Malefic','Malefic','Malefic','CollectiveUnconscious','Malefic','Malefic','Malefic',
                            'Combust','Draw','Malefic','CelestialOpposition','Malefic','LucidDreaming','Malefic','CelestialIntersection','Malefic','Exaltation','Malefic','Malefic','Malefic','Malefic','Malefic',
                            'Malefic','Malefic','Combust','Macrocosmos','Horoscope','Malefic','Malefic','Spear','MinorArcana','Malefic','EarthlyStar','Malefic','Malefic','Malefic','Malefic','LadyOfCrown','Malefic','Draw','Malefic','Malefic','Combust',
                            'Malefic','Malefic','Malefic','LucidDreaming','Malefic','CelestialOpposition','Malefic','Malefic','CelestialIntersection','Malefic','Malefic','CelestialIntersection','Malefic','CollectiveUnconscious','Malefic','Malefic','Combust',
                            'Bole','Malefic','Lightspeed','Malefic','Draw','Divination','Malefic','Ewer','Astrodyne','Malefic','Draw','MinorArcana','Malefic','Balance','EarthlyStar','Malefic','Malefic']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest8 = test("FFLogs test 8 - Astrologian test : (L2tQ41WZCPbYa7wX,2)", ffTest8TestFunction, ffTest8ValidationFunction)
    fflogTestSuite.addTest(ffTest8)

    def ffTest9TestFunction() -> None:

        data = getSingleFightData("", "", "ZDamRAJ7dqzCW816", "1")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Gunbreaker
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.TankActions, ActionEnum.GunbreakerActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest9ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['KeenEdge','NoMercy','Bloodfest','GnashingFang','JugularRip','BlastingZone','SonicBreak','RoughDivide','BowShock','DoubleDown','RoughDivide','SavageClaw','AbdomenTear','RoyalGuard','WickedTalon','EyeGouge','BrutalShell','SolidBarrel','BurstStrike','Hypervelocity','Reprisal','KeenEdge','BrutalShell','SolidBarrel','KeenEdge','Rampart','Camouflage',
                            'GnashingFang','JugularRip','BlastingZone','SavageClaw','AbdomenTear','WickedTalon','EyeGouge','BrutalShell','Provoke','SolidBarrel','HeartOfCorundum','KeenEdge','BrutalShell','SolidBarrel','Shirk','KeenEdge','BrutalShell',
                            'SolidBarrel','KeenEdge','NoMercy','GnashingFang','JugularRip','BlastingZone','SonicBreak','RoughDivide','BowShock','DoubleDown','RoughDivide','SavageClaw','AbdomenTear','WickedTalon','EyeGouge']
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest9 = test("FFLogs test 9 - Gunbreaker test : (ZDamRAJ7dqzCW816,1)", ffTest9TestFunction, ffTest9ValidationFunction)
    fflogTestSuite.addTest(ffTest9)

    def ffTest10TestFunction() -> None:

        data = getSingleFightData("", "", "ZDamRAJ7dqzCW816", "1")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Warrior
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.TankActions, ActionEnum.WarriorActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest10ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Defiance','Tomahawk','Infuriate','Vengeance','HeavySwing','Maim','Potion','StormEye','InnerRelease','Reprisal','InnerChaos','Infuriate','InnerChaos','Upheaval','Onslaught','PrimalRend','Onslaught','FellCleave','FellCleave',
                            'Onslaught','FellCleave','HeavySwing','Maim','StormPath','FellCleave','Infuriate','InnerChaos','Rampart','HeavySwing','ThrillOfBattle','Maim','StormEye','Upheaval','HeavySwing','Bloodwhetting','Maim','StormPath','Provoke',
                            'FellCleave','HeavySwing','Maim','StormPath','HeavySwing','Maim','StormEye','InnerRelease','FellCleave','Onslaught','PrimalRend','Upheaval','FellCleave','Infuriate','InnerChaos','FellCleave','FellCleave'
]
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest10 = test("FFLogs test 10 - Warrior test : (ZDamRAJ7dqzCW816,1)", ffTest10TestFunction, ffTest10ValidationFunction)
    fflogTestSuite.addTest(ffTest10)

    def ffTest11TestFunction() -> None:

        data = getSingleFightData("", "", "c8Y7D6GZ1r9fbjaT", "1")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Paladin
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.TankActions, ActionEnum.PaladinActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest11ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['HolySpirit','FastBlade','Potion','RiotBlade','FightOrFlight','Requiescat','GoringBlade','Expiacion','CircleOfScorn','RoyalAuthority','Intervene','IronWill','Confiteor','Intervene','BladeOfFaith','BladeOfTruth','BladeOfValor',
                            'HolySpirit','Reprisal','Atonement','Atonement','Atonement','FastBlade','RiotBlade','Rampart','Sentinel','RoyalAuthority','Expiacion','CircleOfScorn','FastBlade','RiotBlade','Provoke','HolySheltron','Atonement','Atonement',
                            'Atonement','HolySpirit','Shirk','RoyalAuthority','FastBlade','RiotBlade','Atonement','Atonement','FightOrFlight','Requiescat','GoringBlade','Expiacion','Intervene','Confiteor','CircleOfScorn','Intervene','BladeOfFaith',
                            'BladeOfTruth','BladeOfValor','HolySpirit','Intervention'
]
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest11 = test("FFLogs test 11 - Paladin test : (c8Y7D6GZ1r9fbjaT,1)", ffTest11TestFunction, ffTest11ValidationFunction)
    fflogTestSuite.addTest(ffTest11)

    def ffTest12TestFunction() -> None:

        data = getSingleFightData("", "", "c8Y7D6GZ1r9fbjaT", "1")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.DarkKnight
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.TankActions, ActionEnum.DarkKnightActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest12ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Grit','Unmend','BloodWeapon','Delirium','HardSlash','EdgeOfShadow','DarkMissionary','SyphonStrike','Potion','Souleater','LivingShadow','SaltedEarth','Bloodspiller','EdgeOfShadow','Shadowbringer','Bloodspiller','CarveAndSpit','Plunge','Bloodspiller','EdgeOfShadow','Shadowbringer','HardSlash','EdgeOfShadow','SaltAndDarkness','SyphonStrike','EdgeOfShadow','Plunge','Souleater','HardSlash','SyphonStrike','Rampart',
                            'Souleater','Bloodspiller','HardSlash','SyphonStrike','Souleater','Oblation','HardSlash','DarkMind','SyphonStrike','TheBlackestNight','Souleater','Bloodspiller','Provoke','HardSlash','SyphonStrike','Souleater','HardSlash',
                            'BloodWeapon','Delirium','SyphonStrike','Souleater','Bloodspiller','EdgeOfShadow','Bloodspiller','EdgeOfShadow','Bloodspiller','CarveAndSpit','Plunge','Bloodspiller','EdgeOfShadow','Plunge','HardSlash','Reprisal']
                                    
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest12 = test("FFLogs test 12 - DarkKnight test : (c8Y7D6GZ1r9fbjaT,1)", ffTest12TestFunction, ffTest12ValidationFunction)
    fflogTestSuite.addTest(ffTest12)

    def ffTest13TestFunction() -> None:

        data = getSingleFightData("", "", "8vPCHArRBWkQ6Gdb", "5")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Reaper
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.MeleeActions, ActionEnum.ReaperActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest13ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Soulsow','Harpe','ShadowOfDeath','Potion','LegSweep','SoulSlice','ArcaneCircle','Gluttony','Gallows','Gibbet','ArcaneCrest','PlentifulHarvest','Enshroud','VoidReaping','CrossReaping','LemureSlice','VoidReaping','CrossReaping','LemureSlice','Communio',
                            'SoulSlice','UnveiledGallows','Feint','Gallows','HarvestMoon','Slice','ShadowOfDeath','SoulSlice','UnveiledGibbet','Gibbet','WaxingSlice','InfernalSlice','LegSweep','Slice','WaxingSlice','UnveiledGallows','Gallows','InfernalSlice',
                            'ShadowOfDeath','Slice','WaxingSlice','InfernalSlice','TrueNorth','ArcaneCrest','SoulSlice','Gluttony','Gibbet','Gallows','Slice','UnveiledGibbet','Gibbet','WaxingSlice','InfernalSlice','Enshroud','ShadowOfDeath', 'LegSweep',
                            'VoidReaping','CrossReaping','LemureSlice','VoidReaping','CrossReaping','LemureSlice','Communio'
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest13 = test("FFLogs test 13 - Reaper test : (8vPCHArRBWkQ6Gdb,5)", ffTest13TestFunction, ffTest13ValidationFunction)
    fflogTestSuite.addTest(ffTest13)

    def ffTest14TestFunction() -> None:

        data = getSingleFightData("", "", "8vPCHArRBWkQ6Gdb", "5")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Ninja
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.MeleeActions, ActionEnum.NinjaActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest14ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Huton','Suiton','Kassatsu','SpinningEdge','Potion','GustSlash','Mug','Bunshin','PhantomKamaitachi','TrickAttack','AeolianEdge','DreamWithinADream','Ten','Jin','HyoshoRanryu','Ten','Chi','Raiton','TenChiJin','Ten2','Chi2','Jin2','Meisui','FleetingRaiju','Bhavacakra','FleetingRaiju','Bhavacakra',
                            'Ten','Chi','Raiton','FleetingRaiju','SpinningEdge','GustSlash','AeolianEdge','SpinningEdge','GustSlash','AeolianEdge','SpinningEdge','GustSlash','ArmorCrush','SpinningEdge','Bhavacakra','GustSlash','Ten','Chi','Jin',
                            'Suiton','AeolianEdge','SpinningEdge','GustSlash','AeolianEdge','Kassatsu','SpinningEdge','Bhavacakra','GustSlash','TrueNorth','AeolianEdge','TrickAttack','Ten','Jin','HyoshoRanryu','DreamWithinADream','Ten','Chi','Raiton',
                            'Bhavacakra','FleetingRaiju','Ten','Chi','Raiton','FleetingRaiju','SpinningEdge','GustSlash','ArmorCrush'

            
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest14 = test("FFLogs test 14 - Ninja test : (8vPCHArRBWkQ6Gdb,5)", ffTest14TestFunction, ffTest14ValidationFunction)
    fflogTestSuite.addTest(ffTest14)

    def ffTest15TestFunction() -> None:

        data = getSingleFightData("", "", "j4WazfhqMvgd1LJY", "10")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Monk
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.MeleeActions, ActionEnum.MonkActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest15ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Thunderclap','DragonKick','Potion','TwinSnakes','RiddleOfFire','Demolish','TheForbiddenChakra','Bootshine','Brotherhood','PerfectBalance','DragonKick','RiddleOfWind','Bootshine','TheForbiddenChakra','DragonKick','ElixirField',
                            'TheForbiddenChakra','Bootshine','PerfectBalance','TwinSnakes','TheForbiddenChakra','DragonKick','Demolish','TheForbiddenChakra','RisingPhoenix','Bootshine','Feint','TrueStrike','SnapPunch','DragonKick','TwinSnakes','SnapPunch',
                            'Bootshine','TrueStrike','Demolish','DragonKick','TwinSnakes','SnapPunch','Bootshine','TheForbiddenChakra','TrueStrike','SnapPunch','DragonKick','TwinSnakes','Demolish','Bootshine','PerfectBalance','DragonKick','RiddleOfFire',
                            'Bootshine','RiddleOfEarth','DragonKick','PhantomRush','Bootshine','TheForbiddenChakra','TwinSnakes','Demolish','Bloodbath','DragonKick','Mantra','TrueStrike','TrueNorth','SnapPunch','Bootshine','TwinSnakes','SnapPunch',
                            'DragonKick','TrueStrike','Demolish','Bootshine','TrueStrike','SnapPunch','DragonKick','TheForbiddenChakra','TwinSnakes','RiddleOfWind','SnapPunch','Bootshine','TrueStrike','Demolish','DragonKick','TwinSnakes','SnapPunch',
                            'Bootshine','TrueStrike','SnapPunch','DragonKick','PerfectBalance','RiddleOfFire','DragonKick','Demolish','Brotherhood','TwinSnakes','RisingPhoenix','TheForbiddenChakra','DragonKick','PerfectBalance','Bootshine','TheForbiddenChakra','DragonKick','Bootshine','TheForbiddenChakra',
                            'ElixirField','DragonKick'
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest15 = test("FFLogs test 15 - Dhedge test : (j4WazfhqMvgd1LJY,10)", ffTest15TestFunction, ffTest15ValidationFunction)
    fflogTestSuite.addTest(ffTest15)

    def ffTest16TestFunction() -> None:

        data = getSingleFightData("", "", "j4WazfhqMvgd1LJY", "10")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Samurai
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.MeleeActions, ActionEnum.SamuraiActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest16ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Meikyo','Gekko','Potion','Kasha','Ikishoten','Yukikaze','Feint','Midare','Senei','KaeshiSetsugekka','ThirdEye','Meikyo','Kasha','Gyoten','Shinten','Higanbana','Shinten','OgiNamikiri','Shoha','KaeshiNamikiri','Gekko','Shinten',
                            'Kasha','Gyoten','Hakaze','Yukikaze','ThirdEye','Shinten','Midare','KaeshiSetsugekka','Hakaze','Yukikaze','Hakaze','Shifu','Kasha','Hakaze','Shinten','Jinpu','Shinten','Gekko','Midare','Hakaze','Yukikaze','Hakaze','Shinten','Shifu',
                            'Kasha','ThirdEye','Hakaze','Jinpu','Shinten','Gekko','Shinten','Midare','Meikyo','Kasha','Shoha','Higanbana','Gekko','ThirdEye','Kasha','Hakaze','Shinten','Yukikaze','Shinten','Midare','Shinten','KaeshiSetsugekka'

]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest16 = test("FFLogs test 16 - Samurai test : (j4WazfhqMvgd1LJY,10)", ffTest16TestFunction, ffTest16ValidationFunction)
    fflogTestSuite.addTest(ffTest16)

    def ffTest17TestFunction() -> None:

        data = getSingleFightData("", "", "C176W2JQNqKYd4FR", "15")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Dragoon
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.MeleeActions, ActionEnum.DragoonActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest17ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['ElusiveJump','TrueThrust','Disembowel','LanceCharge','DragonSight','ChaoticSpring','BattleLitany','Geirskogul','WheelingThrust','HighJump','LifeSurge','FangAndClaw','SpineshatterDive','DragonFireDive','RaidenThrust',
                            'SpineshatterDive','MirageDive','VorpalThrust','LifeSurge','HeavenThrust','FangAndClaw','Feint','WheelingThrust','RaidenThrust','WyrmwindThrust','Disembowel','ChaoticSpring','WheelingThrust','FangAndClaw','Geirskogul',
                            'RaidenThrust','HighJump','MirageDive','VorpalThrust','HeavenThrust','FangAndClaw','WheelingThrust','RaidenThrust','WyrmwindThrust','Disembowel','ChaoticSpring','WheelingThrust','FangAndClaw','RaidenThrust','LanceCharge',
                            'VorpalThrust','LifeSurge','Geirskogul','HeavenThrust','Nastrond','HighJump','FangAndClaw','MirageDive','WheelingThrust','Stardiver','RaidenThrust','WyrmwindThrust','Disembowel','Nastrond','TrueNorth','ChaoticSpring',
                            'WheelingThrust','FangAndClaw','RaidenThrust','Nastrond','VorpalThrust','HeavenThrust'

]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest17 = test("FFLogs test 17 - Dragoon test : (C176W2JQNqKYd4FR,15)", ffTest17TestFunction, ffTest17ValidationFunction)
    fflogTestSuite.addTest(ffTest17)

    def ffTest18TestFunction() -> None:

        data = getSingleFightData("", "", "wxZFthf69kj8KpqB", "8")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Machinist
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.RangedActions, ActionEnum.MachinistActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest18ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Reassemble','Potion','AirAnchor','Ricochet','GaussRound','Drill','BarrelStabilizer','SplitShot','Dismantle','SlugShot','Ricochet','GaussRound','CleanShot','Reassemble','Wildfire','ChainSaw','Automaton','Hypercharge',
                            'HeatBlast','Ricochet','HeatBlast','GaussRound','HeatBlast','Ricochet','HeatBlast','GaussRound','HeatBlast','Ricochet','Drill','GaussRound','Ricochet','SplitShot','GaussRound','SlugShot','CleanShot','SplitShot','SlugShot',
                            'CleanShot','AirAnchor','Drill','SplitShot','SlugShot','CleanShot','SplitShot','SlugShot','Automaton','CleanShot','SplitShot','Ricochet','Tactician','Drill','GaussRound','Hypercharge','HeatBlast','Ricochet','HeatBlast','GaussRound',
                            'HeatBlast','Ricochet','HeatBlast','GaussRound','HeatBlast','Reassemble','ChainSaw','Ricochet','GaussRound'
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
            failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest18 = test("FFLogs test 18 - Machinist test : (wxZFthf69kj8KpqB,8)", ffTest18TestFunction, ffTest18ValidationFunction)
    fflogTestSuite.addTest(ffTest18)

    def ffTest19TestFunction() -> None:

        data = getSingleFightData("", "", "kHqB6mgPZYycxJvb", "41")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Bard
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.RangedActions, ActionEnum.BardActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest19ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['Stormbite','WanderingMinuet','RagingStrikes','Causticbite','EmpyrealArrow','Bloodletter','RefulgentArrow','BattleVoice','RadiantFinale','BurstShot','Sidewinder','Barrage','RefulgentArrow','Bloodletter','PitchPerfect','BurstShot',
                            'Bloodletter','BurstShot','PitchPerfect','RefulgentArrow','EmpyrealArrow','Bloodletter','IronJaws','PitchPerfect','RefulgentArrow','BurstShot','BurstShot','BurstShot','PitchPerfect','BurstShot','EmpyrealArrow','Bloodletter',
                            'RefulgentArrow','BurstShot','PitchPerfect','RefulgentArrow','BurstShot','PitchPerfect','MageBallad','BurstShot','BurstShot','EmpyrealArrow','Bloodletter','BurstShot','BurstShot','Bloodletter','BurstShot','Bloodletter','ApexArow','Bloodletter','BlastArow','BurstShot','EmpyrealArrow','Bloodletter','IronJaws',
                            'Troubadour','Bloodletter','RefulgentArrow','Sidewinder','NatureMinne','BurstShot','BurstShot','Bloodletter','BurstShot','BurstShot','ArmyPaeon','EmpyrealArrow','BurstShot','Bloodletter','BurstShot','RefulgentArrow',
                            'BurstShot','BurstShot','BurstShot','BurstShot','EmpyrealArrow','BurstShot','RefulgentArrow','BurstShot','BurstShot','BurstShot','BurstShot','Potion','IronJaws','EmpyrealArrow','BurstShot','Bloodletter','RefulgentArrow',
                            'BurstShot','BurstShot','BurstShot','RefulgentArrow','WanderingMinuet','BurstShot','RagingStrikes','EmpyrealArrow','RefulgentArrow','BurstShot','BattleVoice','RadiantFinale','ApexArow','Sidewinder','Barrage','BlastArow',
                            'Bloodletter','PitchPerfect','RefulgentArrow','Bloodletter','IronJaws','Bloodletter'
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest19 = test("FFLogs test 19 - Bard test : (kHqB6mgPZYycxJvb,41)", ffTest19TestFunction, ffTest19ValidationFunction)
    fflogTestSuite.addTest(ffTest19)


    def ffTest20TestFunction() -> None:

        data = getSingleFightData("", "", "2KBhtxLJH47vrCRj", "17")
        ffLogFight = RestoreFightObject(data)

        playerIndex = [i 
                       for i in range(len(ffLogFight.PlayerList))
                       if ffLogFight.PlayerList[i].JobEnum == JobEnum.Dancer
                       ][0]

        return [
            ActionEnum.name_for_id(action.id, ActionEnum.RangedActions, ActionEnum.DancerActions) 
            for action in ffLogFight.PlayerList[playerIndex].ActionSet
            if action.id != 212
        ]

    def ffTest20ValidationFunction(testResults) -> (bool, list):
        passed = True

        expectedActions =  ['ClosedPosition','StandardStep','Jete','Entrechat','Potion','StandardFinish','Flourish','TechnicalStep','Jete','Entrechat','Emboite','Pirouette','TechnicalFinish','Devilment','Tillana','FanDanceIV','StarfallDance','FanDanceIII','ReverseCascade',
                            'FanDanceI','FanDanceIII','StandardStep','Entrechat','Emboite','StandardFinish','SaberDance','FountainFall','SaberDance','Cascade','SaberDance','ReverseCascade','Fountain','Cascade','Fountain','FountainFall','StandardStep',
                            'Pirouette','Jete','StandardFinish','ReverseCascade','SaberDance','Cascade','Fountain','Cascade','Flourish','SaberDance','FanDanceIV','Fountain','FountainFall','FanDanceIII','ReverseCascade','Cascade','StandardStep',
                            'Pirouette','Jete','StandardFinish','Fountain','FountainFall','Cascade','CuringWaltz','Fountain','FountainFall','SaberDance','Cascade','ReverseCascade','Fountain','FanDanceI','SaberDance','StandardStep','Entrechat','Emboite','StandardFinish',
                            'Cascade','ReverseCascade','FanDanceI','Fountain','Cascade','Fountain','Flourish','TechnicalStep','Entrechat','Pirouette','Jete','Emboite','TechnicalFinish','Devilment','SaberDance','FanDanceIV','FanDanceIII','StarfallDance','FanDanceI','FanDanceIII','Tillana','FanDanceI','SaberDance','FanDanceIII','FanDanceI'
]                   
        failedTest = []
        for i in range(0,len(expectedActions)): 
            if expectedActions[i] != testResults[i]:
                passed = False
                failedTest.append((i, expectedActions[i], testResults[i]))

        return passed , failedTest

    ffTest20 = test("FFLogs test 20 - Dancer test : (2KBhtxLJH47vrCRj,17)", ffTest20TestFunction, ffTest20ValidationFunction)
    fflogTestSuite.addTest(ffTest20)

    return fflogTestSuite

######################################
#         Prepull length test        #
######################################

# This will check the found prepull length.

def generatePrepullLengthTestSuite():

    pLTestSuite = testSuite("Prepull length test suite.")

    def plTest1TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, WaitAbility(15), Fire3]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest1ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [18.5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest1 = test("Prepull length test 1", plTest1TestFunction, plTest1ValidationFunction)
    pLTestSuite.addTest(plTest1)

    def plTest2TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, WaitAbility(15), Fire3]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest2ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [18.5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest2 = test("Prepull length test 2", plTest2TestFunction, plTest2ValidationFunction)
    pLTestSuite.addTest(plTest2)

    def plTest3TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 3000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, WaitAbility(15), Fire3]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest3ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [17.88]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest3 = test("Prepull length test 3", plTest3TestFunction, plTest3ValidationFunction)
    pLTestSuite.addTest(plTest3)

    def plTest4TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 3000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, WaitAbility(15), Fire1]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest4ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [17.05]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest4 = test("Prepull length test 4", plTest4TestFunction, plTest4ValidationFunction)
    pLTestSuite.addTest(plTest4)

    def plTest5TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 3000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, WaitAbility(15), Xenoglossy]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest5ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [15]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest5 = test("Prepull length test 5", plTest5TestFunction, plTest5ValidationFunction)
    pLTestSuite.addTest(plTest5)

    def plTest6TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [SharpCast, Thunder3,  WaitAbility(15), Xenoglossy]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest6ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2.39]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest6 = test("Prepull length test 6", plTest6TestFunction, plTest6ValidationFunction)
    pLTestSuite.addTest(plTest6)

    def plTest7TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [Thunder3,  WaitAbility(15), Xenoglossy]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest7ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [2.39]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest7 = test("Prepull length test 7", plTest7TestFunction, plTest7ValidationFunction)
    pLTestSuite.addTest(plTest7)

    def plTest8TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 1000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.RedMage)

        player.ActionSet = [Verthunder, Verareo]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest8ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [4.79]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest8 = test("Prepull length test 8.", plTest8TestFunction, plTest8ValidationFunction)
    pLTestSuite.addTest(plTest8)

    def plTest9TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Scholar)

        player.ActionSet = [Succor,  Broil]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest9ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [4.00]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest9 = test("Prepull length test 9.", plTest9TestFunction, plTest9ValidationFunction)
    pLTestSuite.addTest(plTest9)

    def plTest10TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 400, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Scholar)

        player.ActionSet = [Succor, Adloquium,  Biolysis, WaitAbility(5), Broil]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest10ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [5.00]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest10 = test("Prepull length test 10.", plTest10TestFunction, plTest10ValidationFunction)
    pLTestSuite.addTest(plTest10)

    def plTest11TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Monk)

        player.ActionSet = [PerfectBalance, WaitAbility(10), Bootshine, Bootshine]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest11ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [10]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest11 = test("Prepull length test 11.", plTest11TestFunction, plTest11ValidationFunction)
    pLTestSuite.addTest(plTest11)

    def plTest12TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Monk)

        player.ActionSet = [PerfectBalance, WaitAbility(10), Thunderclap, WaitAbility(5), Bootshine]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest12ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [10]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest12 = test("Prepull length test 12.", plTest12TestFunction, plTest12ValidationFunction)
    pLTestSuite.addTest(plTest12)

    def plTest13TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.DarkKnight)

        player.ActionSet = [WaitAbility(6.2), HardSlash, HardSlash]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest13ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [6.2]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest13 = test("Prepull length test 13.", plTest13TestFunction, plTest13ValidationFunction)
    pLTestSuite.addTest(plTest13)

    def plTest14TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.DarkKnight)

        player.ActionSet = [WaitAbility(6.2), LivingShadow, HardSlash]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest14ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [6.2]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest14 = test("Prepull length test 14.", plTest14TestFunction, plTest14ValidationFunction)
    pLTestSuite.addTest(plTest14)

    def plTest15TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Scholar)

        player.ActionSet = [Indomitability, Lustrate, Excogitation, WaitAbility(5), Swiftcast, Broil]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest15ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest15 = test("Prepull length test 15.", plTest15TestFunction, plTest15ValidationFunction)
    pLTestSuite.addTest(plTest15)

    def plTest16TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.RedMage)

        player.ActionSet = [Acceleration, WaitAbility(10), Verthunder]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest16ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [10]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest16 = test("Prepull length test 16.", plTest16TestFunction, plTest16ValidationFunction)
    pLTestSuite.addTest(plTest16)

    def plTest17TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.BlackMage)

        player.ActionSet = [Triplecast, WaitAbility(8), Fire3]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest17ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [8]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest17 = test("Prepull length test 17.", plTest17TestFunction, plTest17ValidationFunction)
    pLTestSuite.addTest(plTest17)

    def plTest18TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.RedMage)

        player.ActionSet = [Acceleration, WaitAbility(8), Fleche]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest18ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [8]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest18 = test("Prepull length test 18.", plTest18TestFunction, plTest18ValidationFunction)
    #pLTestSuite.addTest(plTest18)

    def plTest19TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Dancer)

        player.ActionSet = [TechnicalStep, Jete, Pirouette, WaitAbility(10), TechnicalFinish]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength().values())

        return result


    def plTest19ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [13.5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest19 = test("Prepull length test 19.", plTest19TestFunction, plTest19ValidationFunction)
    pLTestSuite.addTest(plTest19)

    def plTest20TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Dancer)

        player.ActionSet = [TechnicalStep, Jete, Pirouette, WaitAbility(10), TechnicalFinish, StandardStep, Pirouette, StandardFinish]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength(ignoreFirstTechnicalFinish=True).values())

        return result


    def plTest20ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [17.5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest20 = test("Prepull length test 20.", plTest20TestFunction, plTest20ValidationFunction)
    pLTestSuite.addTest(plTest20)

    def plTest21TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Dancer)

        player.ActionSet = [TechnicalStep, Jete, Pirouette, WaitAbility(10), TechnicalFinish, StandardStep, Pirouette, StandardFinish, WaitAbility(10), Cascade]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength(ignoreFirstTechnicalFinish=True, ignoreFirstStandardFinish=True).values())

        return result


    def plTest21ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [29]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest21 = test("Prepull length test 21.", plTest21TestFunction, plTest21ValidationFunction)
    pLTestSuite.addTest(plTest21)

    def plTest22TestFunction() -> None:

        fight = Fight(Enemy(), False)
        Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 5000, 'SkS': 2000, 'Crit': 2514, 'DH': 1402, 'Piety': 390}
        player = Player([], [], Stat, JobEnum.Dancer)

        player.ActionSet = [StandardStep, Pirouette, StandardFinish, WaitAbility(10),TechnicalStep, Jete, Pirouette, WaitAbility(10), TechnicalFinish]

        fight.AddPlayer([player])

        result = list(fight.getPlayerPrepullLength(ignoreFirstTechnicalFinish=False, ignoreFirstStandardFinish=True).values())

        return result


    def plTest22ValidationFunction(testResults) -> (bool, list):
        passed = True
        expected = [27.5]

        for i, test in enumerate(expected):
            passed = passed and test == testResults[i]

        return passed , expected

    plTest22 = test("Prepull length test 22.", plTest22TestFunction, plTest22ValidationFunction)
    pLTestSuite.addTest(plTest22)

    return pLTestSuite


    
def executeTests(setSeed : int = 0, testSuiteName : str = "", level=logging.DEBUG) -> int:
                             # Silence the main_logging and
                             # unmute the test_logging
                             # so we only see test results
                             # in log.
    main_logging.setLevel(level=logging.ERROR) 
    test_logging.setLevel(level=level)
    failedTestDict = {}
    if len(testSuiteName) == 0:
        # Execute all tests
        pb = ProgressBar.init(28, "Initializing test suites")

        blmTestSuite = generateBLMTestSuite()
        rdmTestSuite = generateRDMTestSuite()
        smnTestSuite = generateSMNTestSuite()
        whmTestSuite = generateWHMTestSuite()
        astTestSuite = generateASTTestSuite()
        sgeTestSuite = generateSGETestSuite()
        schTestSuite = generateSCHTestSuite()
        mchTestSuite = generateMCHTestSuite()
        brdTestSuite = generateBRDTestSuite()
        dncTestSuite = generateDNCTestSuite()
        ninTestSuite = generateNINTestSuite()
        samTestSuite = generateSAMTestSuite()
        rprTestSuite = generateRPRTestSuite()
        drgTestSuite = generateDRGTestSuite()
        mnkTestSuite = generateMNKTestSuite()
        warTestSuite = generateWARTestSuite()
        gnbTestSuite = generateGNBTestSuite()
        pldTestSuite = generatePLDTestSuite()
        drkTestSuite = generateDRKTestSuite()
        dotTestSuite = generateDOTTestSuite(setSeed=setSeed)
        rfoTestSuite = generateRFOTestSuite()
        pbfTestSuite = generatePBFTestSuite()
        gcdTestSuite = generateGCDTestSuite(setSeed=setSeed)
        teTestSuite = generateTimerEstimateTestSuite()
        lbTestSuite = generateLimitBreakTestSuite()
        fflogTestSuite = generateFFLogsTestSuite()
        plTestSuite = generatePrepullLengthTestSuite()

        pb.setName(blmTestSuite.testSuiteName)
        next(pb)
        failedTestDict[blmTestSuite.testSuiteName] = blmTestSuite.executeTestSuite()
        pb.setName(rdmTestSuite.testSuiteName)
        next(pb)
        failedTestDict[rdmTestSuite.testSuiteName] = rdmTestSuite.executeTestSuite()
        pb.setName(smnTestSuite.testSuiteName)
        next(pb)
        failedTestDict[smnTestSuite.testSuiteName] = smnTestSuite.executeTestSuite()
        pb.setName(whmTestSuite.testSuiteName)
        next(pb)
        failedTestDict[whmTestSuite.testSuiteName] = whmTestSuite.executeTestSuite()
        pb.setName(astTestSuite.testSuiteName)
        next(pb)
        failedTestDict[astTestSuite.testSuiteName] = astTestSuite.executeTestSuite()
        pb.setName(sgeTestSuite.testSuiteName)
        next(pb)
        failedTestDict[sgeTestSuite.testSuiteName] = sgeTestSuite.executeTestSuite()
        pb.setName(schTestSuite.testSuiteName)
        next(pb)
        failedTestDict[schTestSuite.testSuiteName] = schTestSuite.executeTestSuite()
        pb.setName(mchTestSuite.testSuiteName)
        next(pb)
        failedTestDict[mchTestSuite.testSuiteName] = mchTestSuite.executeTestSuite()
        pb.setName(brdTestSuite.testSuiteName)
        next(pb)
        failedTestDict[brdTestSuite.testSuiteName] = brdTestSuite.executeTestSuite()
        pb.setName(dncTestSuite.testSuiteName)
        next(pb)
        failedTestDict[dncTestSuite.testSuiteName] = dncTestSuite.executeTestSuite()
        pb.setName(ninTestSuite.testSuiteName)
        next(pb)
        failedTestDict[ninTestSuite.testSuiteName] = ninTestSuite.executeTestSuite()
        pb.setName(samTestSuite.testSuiteName)
        next(pb)
        failedTestDict[samTestSuite.testSuiteName] = samTestSuite.executeTestSuite()
        pb.setName(rprTestSuite.testSuiteName)
        next(pb)
        failedTestDict[rprTestSuite.testSuiteName] = rprTestSuite.executeTestSuite()
        pb.setName(drgTestSuite.testSuiteName)
        next(pb)
        failedTestDict[drgTestSuite.testSuiteName] = drgTestSuite.executeTestSuite()
        pb.setName(mnkTestSuite.testSuiteName)
        next(pb)
        failedTestDict[mnkTestSuite.testSuiteName] = mnkTestSuite.executeTestSuite()
        pb.setName(warTestSuite.testSuiteName)
        next(pb)
        failedTestDict[warTestSuite.testSuiteName] = warTestSuite.executeTestSuite()
        pb.setName(gnbTestSuite.testSuiteName)
        next(pb)
        failedTestDict[gnbTestSuite.testSuiteName] = gnbTestSuite.executeTestSuite()
        pb.setName(pldTestSuite.testSuiteName)
        next(pb)
        failedTestDict[pldTestSuite.testSuiteName] = pldTestSuite.executeTestSuite()
        pb.setName(drkTestSuite.testSuiteName)
        next(pb)
        failedTestDict[drkTestSuite.testSuiteName] = drkTestSuite.executeTestSuite()
        pb.setName(dotTestSuite.testSuiteName)
        next(pb)
        failedTestDict[dotTestSuite.testSuiteName] = dotTestSuite.executeTestSuite()
        pb.setName(rfoTestSuite.testSuiteName)
        next(pb)
        failedTestDict[rfoTestSuite.testSuiteName] = rfoTestSuite.executeTestSuite()
        pb.setName(pbfTestSuite.testSuiteName)
        next(pb)
        failedTestDict[pbfTestSuite.testSuiteName] = pbfTestSuite.executeTestSuite()
        pb.setName(gcdTestSuite.testSuiteName)
        next(pb)
        failedTestDict[gcdTestSuite.testSuiteName] = gcdTestSuite.executeTestSuite()
        pb.setName(teTestSuite.testSuiteName)
        next(pb)
        failedTestDict[teTestSuite.testSuiteName] = teTestSuite.executeTestSuite()
        pb.setName(lbTestSuite.testSuiteName)
        next(pb)
        failedTestDict[lbTestSuite.testSuiteName] = lbTestSuite.executeTestSuite()
        pb.setName(fflogTestSuite.testSuiteName)
        next(pb)
        failedTestDict[fflogTestSuite.testSuiteName] = fflogTestSuite.executeTestSuite()
        pb.setName(plTestSuite.testSuiteName)
        next(pb)
        failedTestDict[plTestSuite.testSuiteName] = plTestSuite.executeTestSuite()
        next(pb)

    else:
        match testSuiteName:
            case "BLM":
                blmTestSuite = generateBLMTestSuite()
                print(f"Executing {blmTestSuite.testSuiteName}")
                failedTestDict[blmTestSuite.testSuiteName] = blmTestSuite.executeTestSuite()
            case "RDM":
                rdmTestSuite = generateRDMTestSuite()
                print(f"Executing {rdmTestSuite.testSuiteName}")
                failedTestDict[rdmTestSuite.testSuiteName] = rdmTestSuite.executeTestSuite()
            case "SMN":
                smnTestSuite = generateSMNTestSuite()
                print(f"Executing {smnTestSuite.testSuiteName}")
                failedTestDict[smnTestSuite.testSuiteName] = smnTestSuite.executeTestSuite()
            case "SCH":
                schTestSuite = generateSCHTestSuite()
                print(f"Executing {schTestSuite.testSuiteName}")
                failedTestDict[schTestSuite.testSuiteName] = schTestSuite.executeTestSuite()
            case "SGE":
                sgeTestSuite = generateSGETestSuite()
                print(f"Executing {sgeTestSuite.testSuiteName}")
                failedTestDict[sgeTestSuite.testSuiteName] = sgeTestSuite.executeTestSuite()
            case "AST":
                astTestSuite = generateASTTestSuite()
                print(f"Executing {astTestSuite.testSuiteName}")
                failedTestDict[astTestSuite.testSuiteName] = astTestSuite.executeTestSuite()
            case "WHM":
                whmTestSuite = generateWHMTestSuite()
                print(f"Executing {whmTestSuite.testSuiteName}")
                failedTestDict[whmTestSuite.testSuiteName] = whmTestSuite.executeTestSuite()
            case "MCH":
                mchTestSuite = generateMCHTestSuite()
                print(f"Executing {mchTestSuite.testSuiteName}")
                failedTestDict[mchTestSuite.testSuiteName] = mchTestSuite.executeTestSuite()
            case "BRD":
                brdTestSuite = generateBRDTestSuite()
                print(f"Executing {brdTestSuite.testSuiteName}")
                failedTestDict[brdTestSuite.testSuiteName] = brdTestSuite.executeTestSuite()
            case "DNC":
                dncTestSuite = generateDNCTestSuite()
                print(f"Executing {dncTestSuite.testSuiteName}")
                failedTestDict[dncTestSuite.testSuiteName] = dncTestSuite.executeTestSuite()
            case "NIN":
                ninTestSuite = generateNINTestSuite()
                print(f"Executing {ninTestSuite.testSuiteName}")
                failedTestDict[ninTestSuite.testSuiteName] = ninTestSuite.executeTestSuite()
            case "RPR":
                rprTestSuite = generateRPRTestSuite()
                print(f"Executing {rprTestSuite.testSuiteName}")
                failedTestDict[rprTestSuite.testSuiteName] = rprTestSuite.executeTestSuite()
            case "DRG":
                drgTestSuite = generateDRGTestSuite()
                print(f"Executing {drgTestSuite.testSuiteName}")
                failedTestDict[drgTestSuite.testSuiteName] = drgTestSuite.executeTestSuite()
            case "SAM":
                samTestSuite = generateSAMTestSuite()
                print(f"Executing {samTestSuite.testSuiteName}")
                failedTestDict[samTestSuite.testSuiteName] = samTestSuite.executeTestSuite()
            case "MNK":
                mnkTestSuite = generateMNKTestSuite()
                print(f"Executing {mnkTestSuite.testSuiteName}")
                failedTestDict[mnkTestSuite.testSuiteName] = mnkTestSuite.executeTestSuite()
            case "DRK":
                DRKTestSuite = generateDRKTestSuite()
                print(f"Executing {DRKTestSuite.testSuiteName}")
                failedTestDict[DRKTestSuite.testSuiteName] = DRKTestSuite.executeTestSuite()
            case "GNB":
                gnbTestSuite = generateGNBTestSuite()
                print(f"Executing {gnbTestSuite.testSuiteName}")
                failedTestDict[gnbTestSuite.testSuiteName] = gnbTestSuite.executeTestSuite()
            case "PLD":
                pldTestSuite = generatePLDTestSuite()
                print(f"Executing {pldTestSuite.testSuiteName}")
                failedTestDict[pldTestSuite.testSuiteName] = pldTestSuite.executeTestSuite()
            case "WAR":
                warTestSuite = generateWARTestSuite()
                print(f"Executing {warTestSuite.testSuiteName}")
                failedTestDict[warTestSuite.testSuiteName] = warTestSuite.executeTestSuite()
            case "DOT":
                dotTestSuite = generateDOTTestSuite(setSeed=setSeed)
                print(f"Executing {dotTestSuite.testSuiteName}")
                failedTestDict[dotTestSuite.testSuiteName] = dotTestSuite.executeTestSuite()
            case "RFO":
                rfoTestSuite = generateRFOTestSuite()
                print(f"Executing {rfoTestSuite.testSuiteName}")
                failedTestDict[rfoTestSuite.testSuiteName] = rfoTestSuite.executeTestSuite()
            case "PBF":
                pbfTestSuite = generatePBFTestSuite()
                print(f"Executing {pbfTestSuite.testSuiteName}")
                failedTestDict[pbfTestSuite.testSuiteName] = pbfTestSuite.executeTestSuite()
            case "GCD":
                gcdTestSuite = generateGCDTestSuite(setSeed=setSeed)
                print(f"Executing {gcdTestSuite.testSuiteName}")
                failedTestDict[gcdTestSuite.testSuiteName] = gcdTestSuite.executeTestSuite()
            case "TES":
                teTestSuite = generateTimerEstimateTestSuite()
                print(f"Executing {teTestSuite.testSuiteName}")
                failedTestDict[teTestSuite.testSuiteName] = teTestSuite.executeTestSuite()
            case "LB":
                lbTestSuite = generateLimitBreakTestSuite()
                print(f"Executing {lbTestSuite.testSuiteName}")
                failedTestDict[lbTestSuite.testSuiteName] = lbTestSuite.executeTestSuite()
            case "FFLOG":
                fflogTestSuite = generateFFLogsTestSuite()
                print(f"Executing {fflogTestSuite.testSuiteName}")
                failedTestDict[fflogTestSuite.testSuiteName] = fflogTestSuite.executeTestSuite()
            case "PLT":
                plTestSuite = generateFFLogsTestSuite()
                print(f"Executing {plTestSuite.testSuiteName}")
                failedTestDict[plTestSuite.testSuiteName] = plTestSuite.executeTestSuite()

    totalFailedTest = 0

    for key in failedTestDict:
        if not failedTestDict[key][0]:
            print(key + " had " + str(failedTestDict[key][1]) + " failed tests.")
            totalFailedTest += failedTestDict[key][1]

    if totalFailedTest == 0:
        print("Completed without errors. See logs for info.")
    else:
        print("Completed. See logs for info.")
    return 0

if __name__ == "__main__":
    level = logging.DEBUG 
    main_logging.setLevel(level=logging.ERROR) 
    test_logging.setLevel(level=level)
    logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
    generatePrepullLengthTestSuite().executeTestSuite()
