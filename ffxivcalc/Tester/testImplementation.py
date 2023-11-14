"""
This file will contain the test code of every test.

It also contains the code for the testSuite class

A testSuite is a compilation of different tests that are testing a similar thing.

EX : A Blackmage testSuite, etc.

"""
from ffxivcalc.Fight import Fight
from ffxivcalc.Jobs.Player import Player
from ffxivcalc.Jobs.PlayerEnum import *
from ffxivcalc.Enemy import Enemy
from ffxivcalc.helperCode.Progress import ProgressBar

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

main_logging = logging.getLogger("ffxivcalc")
test_logging = main_logging.getChild("Testing")

level = logging.DEBUG 
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
main_logging.setLevel(level=logging.ERROR) 
test_logging.setLevel(level=logging.DEBUG)
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

        testResults = self.testFunction()

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

    def executeTestSuite(self):
        test_logging.debug("Executing test suite -> " + self.testSuiteName)
        success = True
        x = len(self.testList)
        for test in self.testList: success = test.executeTest() and success

        if not success : test_logging.error("Testsuite " + self.testSuiteName + " had at least one fail test. See above.")
        else : test_logging.debug(self.testSuiteName + " completed without errors.")


######################################
#       Blackmage testSuite          #
######################################

blmTestSuite = testSuite("Blackmage test suite")

# Opener requirement, end time and potency test 1

def blmTest1TestFunction() -> None:
    """This test will try the opener of a blackmage. It will test for failed requirements but will not check for mana.
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
    expected = [0, 85.61, 9349]    

    for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

    return passed , expected

blmtest1 = test("Opener requirement, end time and potency 1", blmTest1TestFunction, blmTest1ValidationFunction)
blmTestSuite.addTest(blmtest1)

# Opener requirement, end time and potency test 2
            
def blmTest2TestFunction() -> None:
    """This test will try the opener of a blackmage. It will test for failed requirements but will not check for mana.
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

######################################
#         Redmage testSuite          #
######################################

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
    expected = [0, 32.47, 8730]    

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


######################################
#         Summoner testSuite         #
######################################

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
    expected = [0, 80.18, 9530]    

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
    expected = [0, 105.88, 14510]    

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

######################################
#          Scholar testSuite         #
######################################

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

######################################
#          Whitemage testSuite       #
######################################

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
    expected = [0, 37.15, 6330]    

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

######################################
#          Astrologian testSuite     #
######################################

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
                Malefic, Malefic,Combust, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, 
			    Malefic, Malefic, Malefic, Malefic, Malefic, Malefic, Malefic]
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
    expected = [0, 66.92, 7800]   

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

######################################
#            Sage testSuite          #
######################################

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
    expected = [0, 51.37, 8000]   

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
    expected = [1]   

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

######################################
#        Machinist testSuite         #
######################################

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
    expected = [0, 82.51, 11050]   

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
    expected = [2, 28.46,2, 30]   

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
    expected = [0, 11.99, 3, 0]   

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
    expected = [1, 25.49, 2, 13.51]   

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
    expected = [True, 2350]   

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

######################################
#           Bard testSuite           #
######################################

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
    expected = [0, 70.73, 6670]   

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
    expected = [True,24.27]   

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
    expected = [16,25.01, True]   

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
    expected = [True,25.01]   

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
    expected = [False,44.99, 0, True,False]   

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
    expected = [True,44.99, 0, False, False]   

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
    expected = [True,44.99, 0, False]   

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

######################################
#           Dancer testSuite           #
######################################

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
    expected = [0, 18.38, 5420]   

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

######################################
#           Ninja testSuite          #
######################################

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
    expected = [0, 25.08, 11410]   

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
    expected = [420, 25, 45.76]   

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
    expected = [200, 25, 43.64]   

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
    expected = [200, 0,17.88]   

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
    expected = [200, 0,17.88]   

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
    expected = [200, 25,13.64]   

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
    return [player.CastingSpell.Potency, player.CastingSpell.DPSBonus, round(player.TotalDamage/(24617),2)]

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
    return [player.CastingSpell.Potency, player.CastingSpell.DPSBonus, round(player.TotalDamage/(49234),2)]

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
    expected = [650,5]   

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
    expected = [350,5]   

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

######################################
#         Samurai testSuite          #
######################################

samTestSuite = testSuite("Samurai test suite")

# Opener requirement, end time and potency test 1

def samTest1TestFunction() -> None:
    """This test will try the opener of a scholar. It will test for failed requirements but will not check for mana.
    """

    Dummy = Enemy()
    Event = Fight(Dummy, False)
    Stat = {'MainStat': 3378, 'WD': 132, 'Det': 1601, 'Ten': 400, 'SS': 400, 'SkS': 508, 'Crit': 2514, 'DH': 1402, 'Piety': 390}

    actionSet = [Meikyo, WaitAbility(9), Gekko, Kasha, Ikishoten, Yukikaze, Midare, Senei, KaeshiSetsugekka, Meikyo, Gekko, Shinten, Higanbana, Shinten, OgiNamikiri, Shoha, 
                 KaeshiNamikiri, Kasha, Shinten, Gekko, Gyoten, Hakaze, Yukikaze, Shinten, Midare, KaeshiSetsugekka, WaitAbility(50)]
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
    expected = [0, 79.26, 13030]

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

    actionSet = [Meikyo,Gekko, Higanbana, WaitAbility(60)]
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

######################################
#          Reaper testSuite          #
######################################

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
    expected = [0, 27.17, 9760]

    for i in range(len(testResults)): passed = passed and (expected[i] == testResults[i])

    return passed , expected

rprtest1 = test("Opener requirement, end time and potency 1", rprTest1TestFunction, rprTest1ValidationFunction)
rprTestSuite.addTest(rprtest1)

# Combo Potency and Gauge generation test

def rprTest2TestFunction() -> None:
    """Combo Potency and Gauge generation test
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

rprtest2 = test("Combo Potency and Gauge generation test 1", rprTest2TestFunction, rprTest2ValidationFunction)
rprTestSuite.addTest(rprtest2)

# Combo Potency and Gauge generation test

def rprTest3TestFunction() -> None:
    """Combo Potency and Gauge generation test
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

rprtest3 = test("Combo Potency and Gauge generation test 2", rprTest3TestFunction, rprTest3ValidationFunction)
rprTestSuite.addTest(rprtest3)

# Combo Potency and Gauge generation test

def rprTest4TestFunction() -> None:
    """Combo Potency and Gauge generation test
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

rprtest4 = test("Combo Potency and Gauge generation test 3", rprTest4TestFunction, rprTest4ValidationFunction)
rprTestSuite.addTest(rprtest4)

# Combo Potency and Gauge generation test

def rprTest5TestFunction() -> None:
    """Combo Potency and Gauge generation test
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

rprtest5 = test("Combo Potency and Gauge generation test 4", rprTest5TestFunction, rprTest5ValidationFunction)
rprTestSuite.addTest(rprtest5)

rprTestSuite.executeTestSuite()

if False:
    pb = ProgressBar.init(12, "Executing test suite")
    blmTestSuite.executeTestSuite()
    next(pb)
    rdmTestSuite.executeTestSuite()
    next(pb)
    smnTestSuite.executeTestSuite()
    next(pb)
    whmTestSuite.executeTestSuite()
    next(pb)
    astTestSuite.executeTestSuite()
    next(pb)
    sgeTestSuite.executeTestSuite()
    next(pb)
    schTestSuite.executeTestSuite()
    next(pb)
    mchTestSuite.executeTestSuite()
    next(pb)
    brdTestSuite.executeTestSuite()
    next(pb)
    dncTestSuite.executeTestSuite()
    next(pb)
    ninTestSuite.executeTestSuite()
    next(pb)
    samTestSuite.executeTestSuite()
    next(pb)
    print("Completed. See logs for info.")

