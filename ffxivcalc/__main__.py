"""CLI entrypoint for FFXIV-Combat-Simulator"""
from argparse import ArgumentParser
from pathlib import Path
from sys import exit
import logging

from ffxivcalc import __name__ as prog
from ffxivcalc.UI.SimulationInput import ExecuteMemoryCode as fight_main
from ffxivcalc.Tester.Tester import Tester
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
    test_parser.add_argument('json', type=Path, help='path to Tester folder', nargs='?', default='ffxivcalc/Tester')

    # Running tui
    subparsers.add_parser('tui')

    return parser


def main() -> int:
    """
    Entrypoint into the cli. Can be called with ``python -mffxivcalc``
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
        __logger__.setLevel(level=level) # __logger__ = logging.getLogger("ffxivcalc") 

    match args.action:
        case 'simulate':
            fight_main(False, time_unit=args.step_size, TimeLimit=args.time_limit)
        case 'tests':
            Tester(args.json).Test()
        case 'tui':
            TUI_draw()
        case _: # default case
            parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())