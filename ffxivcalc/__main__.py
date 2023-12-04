"""CLI entrypoint for FFXIV-Combat-Simulator"""
from argparse import ArgumentParser
from pathlib import Path
from sys import exit
import logging

from ffxivcalc import __name__ as prog
from ffxivcalc.UI.SimulationInput import ExecuteMemoryCode as fight_main
from ffxivcalc.Tester.testImplementation import executeTests
from ffxivcalc.UI.TUI import TUI_draw

__logger__ = logging.getLogger("ffxivcalc") # root logger

def get_parser() -> ArgumentParser:
    """Defines all the cli arguments to be parsed
    :return: An ArgumentParser object
    """
    verbose_help = " -v (Displays on terminal logging at level ERROR), -vv (Displays on terminal logging at level WARNING), -vvv (Creates a log file that has logging level DEBUG)"
    parser = ArgumentParser(prog=prog)
    parser.add_argument('-v', '--verbose', action='count', default=0, help=verbose_help)
    subparsers = parser.add_subparsers(help='action to perform', dest='action')

    # Running in code simulation
    simulation_parser = subparsers.add_parser('simulate')
    simulation_parser.add_argument('-code_simulation', '--code-simulation', type=bool, default=False)
    simulation_parser.add_argument('-s', '--step-size', type=float, default=0.01)
    simulation_parser.add_argument('-l', '--time-limit', type=int, default=1000)

    # Running tester
    test_parser = subparsers.add_parser('tests')
    seed_help = "-s XXXXXX (sets the given seed for the execution of the tests. Relevant to DOT and AA test suite. Sets the seed for both the DOT and AA test suite.)"
    test_parser.add_argument('-s', '--seed', type=int, default=0, help=seed_help) # argument to specify seed for DOT and aa test suite.
                                                                  # The same seed is given to both test if specified.
    name_help = "-n XXXXX (Name of a specific test suite to run. If not specified runs all the test suites. If invalid name returns an error).\nA valid name is the 3 letters of the test suite's name."
    test_parser.add_argument('n', '--name', type=str, default="", help=name_help) # Specifies te name of the test suites we want to run. 

    # Running tui
    subparsers.add_parser('tui')

    return parser


def main() -> int:
    """
    Entrypoint into the cli. Can be called with ``python -m ffxivcalc``
    :return: Return code, for use with cli programs to indicate success/failure
    """
    parser = get_parser()
    args = parser.parse_args()

    if args.verbose > 0:
        match args.verbose:
            case 1: # displays error and above
                level = logging.ERROR
                logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',level=level)
            case 2: # displays warning and above
                level = logging.WARNING
                logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',level=level)
            case 3: # saves everything to a save file
                level = logging.DEBUG
                logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
            case _: # more than 3 V is too much, save as case 3
                level = logging.DEBUG
                logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
        __logger__.setLevel(level=level) 

    match args.action:
        case 'simulate':
            fight_main(False, time_unit=args.step_size, TimeLimit=args.time_limit)
        case 'tests':
            executeTests(setSeed=args.seed, testSuiteName=args.name)
        case 'tui':
            TUI_draw()
        case _: # default case
            parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())