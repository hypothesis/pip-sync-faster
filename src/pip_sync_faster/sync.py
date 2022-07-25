import hashlib
import json
import sys
from os import environ
from os.path import abspath
from pathlib import Path
from subprocess import run


def get_hash(path):
    """Return the hash of the given file."""
    hashobj = hashlib.sha512()

    with open(path, "rb") as file:
        hashobj.update(file.read())

    return hashobj.hexdigest()


def get_hashes(paths):
    """Return a dict mapping the given files to their hashes."""
    return {abspath(path): get_hash(abspath(path)) for path in paths}


def sync(src_files):
    cached_hashes_path = Path(environ["VIRTUAL_ENV"]) / "pip_sync_faster.json"

    try:
        with open(cached_hashes_path, "r", encoding="utf-8") as handle:
            cached_hashes = json.load(handle)
    except FileNotFoundError:
        cached_hashes = {}

    hashes = get_hashes(src_files)

    if hashes == cached_hashes:
        return

    # The hashes did not match the cached ones. This can happen if:
    #
    # * This is the first time that pip-sync-faster has been called for this venv
    # * One or more of the requirements files has changed
    # * pip-sync-faster was called with a different set of requirements files

    run(["pip-sync", *sys.argv[1:]], check=True)

    # Replace the cached hashes file with one containing the correct hashes for
    # the requirements files that pip-sync-faster was called with this time.
    with open(cached_hashes_path, "w", encoding="utf-8") as handle:
        json.dump(hashes, handle)
