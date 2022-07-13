import sys
from argparse import ArgumentParser
from importlib.metadata import version


def hello_world():
    return "Hello, world!"


def entry_point():  # pragma: nocover
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(version("pip-sync-faster"))
        sys.exit()
