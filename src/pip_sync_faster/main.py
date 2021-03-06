import hashlib
import json
import os
import sys
from argparse import ArgumentParser
from functools import cached_property
from importlib.metadata import version
from pathlib import Path
from subprocess import CalledProcessError, run


class SrcFile:
    def __init__(self, path):
        self.path = path

    @cached_property
    def abspath(self):
        return os.path.abspath(self.path)

    @cached_property
    def contents_hash(self):
        hash_ = hashlib.sha512()
        with open(self.abspath, "rb") as file:
            hash_.update(file.read())
        return hash_.hexdigest()


def pip_sync_maybe(src_files, args):
    cached_hashes_path = Path(os.environ["VIRTUAL_ENV"]) / "pip_sync_faster.json"

    try:
        with open(cached_hashes_path, "r", encoding="utf8") as cached_hashes_file:
            cached_hashes = json.load(cached_hashes_file)
    except FileNotFoundError:
        cached_hashes = {}

    src_files = [SrcFile(src_file) for src_file in src_files]

    for src_file in src_files:
        if src_file.contents_hash != cached_hashes.get(src_file.abspath):
            break
    else:
        # All of the source files already had matching hashes in the cache.
        return

    # One or more of the source files was either missing from the cache or had
    # a non-matching hash in the cache.
    try:
        run(["pip-sync"] + args, check=True)
    except CalledProcessError as err:
        sys.exit(err.returncode)
    else:
        # pip-sync succeeded so update the cache.
        for src_file in src_files:
            cached_hashes[src_file.abspath] = src_file.contents_hash

        with open(cached_hashes_path, "w", encoding="utf8") as cached_hashes_file:
            json.dump(cached_hashes, cached_hashes_file)


def entry_point():
    parser = ArgumentParser()
    parser.add_argument("--version", action="store_true")
    parser.add_argument("src_files", nargs="*")

    args = parser.parse_known_args()

    if args[0].version:
        print(f"pip-sync-faster, version {version('pip-sync-faster')}")

    pip_sync_maybe(args[0].src_files, sys.argv[1:])
