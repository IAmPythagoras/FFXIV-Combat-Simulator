"""CLI entrypoint for FFXIV-Combat-Simulator"""
from argparse import ArgumentParser
from sys import exit

from ffxivcalc import __name__ as prog
from ffxivcalc.UI.SimulationInput import ExecuteMemoryCode as fight_main
from ffxivcalc.Tester.Tester import Tester
from ffxivcalc.UI.TUI import TUI_draw

def get_parser() -> ArgumentParser:
    """Defines all the cli arguments to be parsed

    :return: An ArgumentParser object
    """
    parser = ArgumentParser(prog=prog)

    # Running in code simulation
    parser.add_argument('-code_simulation', '--code-simulation', type=bool, default=False)
    parser.add_argument('-s', '--step-size', type=float, default=0.01)
    parser.add_argument('-l', '--time-limit', type=int, default=1000)

    # Running tester
    parser.add_argument('-run_tests', '--run_tests', type=bool, default=False)

    # Running tester
    parser.add_argument('-TUI', '--TUI_open', type=bool, default=False)


    # subparsers should be added here for tui/gui/etc functionality
    return parser


def main() -> int:
    """
    Entrypoint into the cli. Can be called with ``python -mffxivcalc``

    :return: Return code, for use with cli programs to indicate success/failure
    """
    parser = get_parser()
    args = parser.parse_args()
    #input(args)

    if args.code_simulation:
        fight_main(False, time_unit=args.step_size, TimeLimit=args.time_limit)
    elif args.run_tests:
        Tester("test_layout.json").Test()
    elif args.TUI_open:
        TUI_draw()
    return 0


if __name__ == '__main__':
    exit(main())