from argparse import ArgumentParser
from importlib.metadata import version
from subprocess import CalledProcessError

from pip_sync_faster.sync import sync


def cli(_argv=None):  # pylint:disable=inconsistent-return-statements
    parser = ArgumentParser(
        description="Synchronize the active venv with requirements.txt files."
    )
    parser.add_argument(
        "--version", action="store_true", help="show the version and exit"
    )
    parser.add_argument(
        "src_files", nargs="*", help="the requirements.txt files to synchronize"
    )

    args = parser.parse_known_args(_argv)

    if args[0].version:
        print(f"pip-sync-faster, version {version('pip-sync-faster')}")
        return

    try:
        sync(args[0].src_files)
    except CalledProcessError as err:
        return err.returncode
