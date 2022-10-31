"""CLI entrypoint for FFXIV-Combat-Simulator"""
from argparse import ArgumentParser
from sys import exit

from ffxivppscalc import __name__ as prog
from ffxivppscalc.SimulationInput import ExecuteMemoryCode as fight_main


def get_parser() -> ArgumentParser:
    """Defines all the cli arguments to be parsed

    :return: An ArgumentParser object
    """
    parser = ArgumentParser(prog=prog)
    parser.add_argument('-s', '--step-size', type=float, default=0.01)
    parser.add_argument('-l', '--time-limit', type=int, default=1000)

    # subparsers should be added here for tui/gui/etc functionality
    return parser


def main() -> int:
    """Entrypoint into the cli. Can be called with ``python -mffxivppscalc``

    :return: Return code, for use with cli programs to indicate success/failure
    """
    parser = get_parser()
    args = parser.parse_args()
    print(args)

    fight_main(time_unit=args.step_size, TimeLimit=args.time_limit)
    return 0


if __name__ == '__main__':
    exit(main())