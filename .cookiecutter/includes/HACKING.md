
Testing Manually
----------------

Normally if you wanted to test a command manually in dev you'd do so through
tox, for example:

```terminal
$ tox -qe dev --run-command 'pip-sync-faster --help'
usage: pip-sync-faster [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --version
```

But there's a problem with running `pip-sync-faster` commands in this way: a
command like `tox -e dev --run-command 'pip-sync-faster requirements.txt'` will
run `pip-sync requirements.txt` and `pip-sync` will sync the
current virtualenv (`.tox/dev/`) with the `requirements.txt` file. Everything
in `requirements.txt` will get installed into `.tox/dev/`, which you probably
don't want. Even worse everything _not_ in `requirements.txt` will get
_removed_ from `.tox/dev/` including `pip-sync-faster` itself!

To avoid this problem run `pip-sync-faster` in a temporary virtualenv instead.
This installs the contents of `requirements.txt` into the temporary venv so
your `.tox/dev/` env doesn't get messed up. And it does not install
`pip-sync-faster` into the temporary venv so there's no issue with `pip-sync`
uninstalling `pip-sync-faster`:

```terminal
# Make a temporary directory.
tempdir=$(mktemp -d)

# Create a virtualenv in the temporary directory.
python3 -m venv $tempdir

# Activate the virtualenv.
source $tempdir/bin/activate

# Install pip-tools in the virtualenv (pip-sync-faster needs pip-tools).
pip install pip-tools

# Call pip-sync-faster to install a requirements file into the temporary virtualenv.
PYTHONPATH=src python3 -m pip_sync_faster /path/to/requirements.txt

# When you're done testing deactivate the temporary virtualenv.
deactivate
```
