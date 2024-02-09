__version__ = '0.8.901'

"""
Update history :

0.8.901 :
    - Fixed some 'computeActionTimer()' issues on Samurai with Meikyo/Gekko interaction, an issue where only having 1 GCD would return wrong estimated time stamp.

0.8.900 :
    - Added 'computeActionTimer()' which returns an estimate of a player's timeStamp/DOT timer/buf timer.
      This function can be called on a player object and will return a dictionnary containing the estimates.
    - Added tests to test 'computeActionTimer' functionality.
    - Fixed mitigation amount issue (higher than 1 values) (PR by Apollo)
    - Fixed Samurai Higanbana DOT potency (was 60, fixed to 45) (PR by Apollo)
    - Moved some gcdTiming computation to the Player object (see Fight.py)
    - Removed lock in various places

0.8.800 :
    - Made changes to work with web app
    - Added ways to remove pB or redirect the output
    - Fixed etro import issues
    - BiSSolver now makes a deepcopy of the gear space so it can be reused
    - Fixed pb issues, fixed fight import issues.
    - Added 'ShowProgress' option to 'SimulateFight()' that lets enables the print of the loading bar
    - Various other bug fixes

0.8.700 :
    - Made PyPi package.

0.8.60 :
    - Added more accurate AA, weapon delay, haste affecting delay.
    - Fixed DOT/AA issues
    - Added AA delay, GCD timer and more DOT tests.
    - Added cli "tests" command to run test suites.
    

"""
